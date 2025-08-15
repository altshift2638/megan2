# Megan All-In-One — OFFLINE (CPU, llama.cpp)

This version (v2.0.3) fixes the Alpine package error by **removing libexecinfo-dev**
and compiling llama-cpp-python with **GGML_BACKTRACE=OFF**.

## Install
- Add this repo to **Add-on Store → Repositories**, install **Megan AI (Offline) v2.0.3**, Start.
- First run auto-downloads TinyLlama GGUF to `/data/models`.
- Web UI: `http://<HA_IP>:8000/demo`. Health: `/health`.

If build still fails, please paste the first 40 lines of the log.
