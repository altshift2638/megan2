ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Build deps for llama-cpp-python on Alpine
RUN apk add --no-cache python3 py3-pip bash curl jq git build-base cmake ninja libexecinfo-dev

# venv + deps (disable GGML backtrace to avoid execinfo.h requirement)
ENV CMAKE_ARGS="-DGGML_NATIVE=ON -DGGML_BLAS=OFF -DGGML_BACKTRACE=OFF"

RUN python3 -m venv /venv \
 && . /venv/bin/activate \
 && pip install --no-cache-dir --upgrade pip wheel setuptools \
 && pip install --no-cache-dir llama-cpp-python==0.2.84 fastapi uvicorn pydantic httpx

ENV PATH="/venv/bin:$PATH"
WORKDIR /app

COPY server.py /app/server.py

EXPOSE 8000
CMD ["/venv/bin/uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
