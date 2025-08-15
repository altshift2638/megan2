ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Enable Alpine edge main to get libexecinfo-dev (execinfo.h)
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

# Build deps for llama-cpp-python
RUN apk add --no-cache python3 py3-pip bash curl jq git build-base cmake ninja libexecinfo-dev

# Compile flags
ENV CMAKE_ARGS="-DGGML_NATIVE=ON -DGGML_BLAS=OFF"

# venv + deps
RUN python3 -m venv /venv \
 && . /venv/bin/activate \
 && pip install --no-cache-dir --upgrade pip wheel setuptools \
 && pip install --no-cache-dir llama-cpp-python==0.2.84 fastapi uvicorn pydantic httpx

ENV PATH="/venv/bin:$PATH"
WORKDIR /app

COPY run.sh /run.sh
COPY server.py /app/server.py
RUN chmod +x /run.sh && sed -i 's/\r$//' /run.sh

EXPOSE 8000
CMD ["/run.sh"]
