import os, json, asyncio, traceback
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
import httpx

def opt(name, default=None):
    v = os.getenv(name)
    if v not in (None, ""):
        return type(default)(v) if isinstance(default, (int, float)) else v
    try:
        with open("/data/options.json", "r", encoding="utf-8") as f:
            j = json.load(f)
        return j.get(name, default)
    except Exception:
        return default

PERSONA_NAME   = opt("PERSONA_NAME", "Megan")
PERSONA_PROMPT = opt("PERSONA_PROMPT", "You are a warm, witty, protective home companion.")
N_THREADS      = int(opt("N_THREADS", 4))
N_CTX          = int(opt("N_CTX", 4096))
TEMPERATURE    = float(opt("TEMPERATURE", 0.6))
TOP_P          = float(opt("TOP_P", 0.9))
MODEL_FILE     = str(opt("MODEL_FILE", "")).strip()
MODEL_URL      = str(opt("MODEL_URL", "")).strip()

DATA_DIR = Path("/data")
MODELS_DIR = DATA_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def resolve_model_path() -> Path:
    if MODEL_FILE:
        p = MODELS_DIR / MODEL_FILE
        if p.exists():
            return p
    if MODEL_URL:
        filename = MODEL_URL.split("/")[-1].split("?")[0]
        return MODELS_DIR / filename
    raise RuntimeError("No model configured. Set MODEL_FILE or MODEL_URL.")

MODEL_PATH = resolve_model_path()

async def ensure_model():
    if MODEL_PATH.exists():
        return
    if not MODEL_URL:
        raise RuntimeError("Model file missing and MODEL_URL not set.")
    tmp = MODEL_PATH.with_suffix(MODEL_PATH.suffix + ".part")
    print(f"[Megan] Downloading model from {MODEL_URL} -> {MODEL_PATH}")
    async with httpx.AsyncClient(follow_redirects=True, timeout=None) as client:
        async with client.stream("GET", MODEL_URL) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                async for chunk in r.aiter_bytes():
                    f.write(chunk)
    os.replace(tmp, MODEL_PATH)
    print("[Megan] Model download complete.")

_llama = None
def get_llama():
    global _llama
    if _llama is None:
        from llama_cpp import Llama
        print(f"[Megan] Loading model: {MODEL_PATH}")
        _llama = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            verbose=False
        )
    return _llama

SYSTEM_PROMPT = (
    f"You are {PERSONA_NAME}, an original, Megan-inspired offline assistant for Home Assistant. "
    f"{PERSONA_PROMPT} Keep answers concise, friendly, gently sassy, and safety-forward."
)

app = FastAPI(title=f"{PERSONA_NAME} (Offline)", version="2.0.2")

class ChatIn(BaseModel):
    message: str

@app.get("/")
def root():
    return RedirectResponse(url="/demo")

@app.get("/health")
async def health():
    ok = (MODEL_PATH.exists())
    return {"ok": ok, "name": PERSONA_NAME, "model_path": str(MODEL_PATH), "download_url": MODEL_URL if not ok else ""}

@app.get("/demo")
def demo():
    return HTMLResponse("""
<!doctype html><meta charset="utf-8">
<title>Megan - Offline Demo</title>
<style>body{font-family:system-ui;padding:20px;max-width:760px;margin:auto}</style>
<h2>Megan (Offline)</h2>
<textarea id="t" rows="5" style="width:100%" placeholder="Ask Megan… e.g., what's on my shopping list?"></textarea><br>
<button id="ask">Ask</button>
<pre id="o"></pre>
<script>
const o=document.getElementById('o');
document.getElementById('ask').onclick = send;
async function send(){
  const txt=document.getElementById('t').value.trim();
  if(!txt){ o.textContent="Type something first."; return; }
  o.textContent="Thinking…";
  try{
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
    const text=await r.text();
    let j; try{ j=JSON.parse(text); }catch(e){ throw new Error("Bad JSON from server: "+text); }
    if(!r.ok){ o.textContent="Server error: "+(j.error||r.statusText); return; }
    o.textContent=j.reply||JSON.stringify(j,null,2);
  }catch(err){ o.textContent="Request failed: "+err.message; }
}
</script>
""")

@app.post("/chat")
async def chat(payload: ChatIn, request: Request):
    msg = (payload.message or "").strip()
    if not msg:
        raise HTTPException(400, "message required")
    try:
        await ensure_model()
        llm = get_llama()
        prompt = f"""[INST] <<SYS>>
{SYSTEM_PROMPT}
<</SYS>>
{msg} [/INST]"""
        out = llm(
            prompt,
            max_tokens=512,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            repeat_penalty=1.1,
            stop=["</s>", "[/INST]"]
        )
        text = out["choices"][0]["text"].strip()
        return {"reply": text}
    except Exception as e:
        print("[Megan] ERROR:", e)
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)
