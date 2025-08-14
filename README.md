# Megan All-In-One — OFFLINE (TinyLlama / llama.cpp)

This repo contains:
- **Home Assistant Add-on** (`megan_ai/`) — runs a local LLM with llama.cpp (CPU) and serves a web demo + API.
- **HACS Integration** (`custom_components/megan_conversation/`) — registers Megan as a Conversation Agent.

## Install (Add-on)
1. Add this repo URL in **Settings → Add-ons → Add-on Store → ⋮ → Repositories → Add**.
2. Install **Megan AI (Offline)**.
3. Start it. On first start it will download the model to `/data/models`.
4. Open **Web UI**: `http://<HA_IP>:8000/demo`.

## Notes
This 2.0.1 patch fixes build failures on Alpine by adding `libexecinfo-dev` and `ninja`, and disabling GGML backtrace.
