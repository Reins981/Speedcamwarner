FROM python:3.10-slim

WORKDIR /app

# (Optional) Copy your project files
# COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    autoconf \
    automake \
    libtool \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libsqlite3-dev \
    sqlite3 \
    bzip2 \
    libbz2-dev \
    libffi-dev \
    openjdk-17-jdk \
    unzip \
    cmake && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure Java is in PATH
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Python packages
RUN pip install --upgrade pip
RUN pip install --upgrade buildozer
RUN pip install cython==0.29.36

# Entrypoint for Buildozer
ENTRYPOINT ["buildozer"]
CMD ["android", "clean"]
