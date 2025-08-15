# Megan All-In-One — OFFLINE (CPU, llama.cpp)

Single GitHub repo containing:
- **Home Assistant Add-on** (`/megan_ai`) – runs a local LLM with `llama-cpp-python` on CPU. Web UI at `/demo`.
- **HACS Integration** (`/custom_components/megan_conversation`) – registers Megan as a Conversation Agent.

## Install (Add-on Store)
1. In Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories → Add** this repo URL.
2. Install **Megan AI (Offline)** (v2.0.2).  
3. Start it. First run downloads **TinyLlama-1.1B Chat** GGUF to `/data/models` (persistent).  
4. Open **Web UI**: `http://<HA_IP>:8000/demo`.

## Install (HACS)
1. HACS → Integrations → ⋮ → **Custom repositories → Add** this same repo URL (Category: *Integration*).
2. Install **Megan Conversation Agent** → *Add Integration* (keep `http://homeassistant.local:8000/chat`).
3. **Settings → Voice Assistants → Default conversation agent → Megan (Local)**.

## Options (Add-on → Configuration)
- `PERSONA_NAME`, `PERSONA_PROMPT`
- `N_THREADS` (CPU threads), `N_CTX` (context tokens)
- `TEMPERATURE`, `TOP_P`
- `MODEL_FILE` – filename under `/addons_config/megan_ai/models/` (host) to use instead of default
- `MODEL_URL` – auto-download alternative GGUF on first start

## Troubleshooting
- If build fails with C/C++ errors: this image uses Alpine deps + Ninja + execinfo fix. Make sure you’re on v2.0.2.
- If `/demo` shows “Thinking…”: check Add-on **Logs** – first run may be downloading a model.
