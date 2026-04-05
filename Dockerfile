FROM python:3.11-slim
#@cantarellabots
# Install system dependencies
# ffmpeg is required for merging formats
# wget is required for downloading N_m3u8DL-RE
# git is required for pip install from git
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install N_m3u8DL-RE
RUN wget https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.1-beta/N_m3u8DL-RE_Beta_linux-x64_20240828.tar.gz && \
    tar -xzf N_m3u8DL-RE_Beta_linux-x64_20240828.tar.gz && \
    mv N_m3u8DL-RE_Beta_linux-x64/N_m3u8DL-RE /usr/local/bin/ && \
    rm -rf N_m3u8DL-RE_Beta_linux-x64* && \
    chmod +x /usr/local/bin/N_m3u8DL-RE

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "run.sh"]
