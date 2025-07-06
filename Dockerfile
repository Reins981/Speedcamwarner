FROM ubuntu:22.04

WORKDIR /app

# COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y \
    libatlas-base-dev \
    autoconf \
    automake \
    libtool \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

RUN pip3 install --upgrade buildozer
RUN pip3 install cython==0.29.36

RUN apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    build-essential \ 
    libsqlite3-dev \ 
    sqlite3 \
    bzip2 \
    libbz2-dev \
    libffi-dev \
    openjdk-11-jdk \
    unzip \
    cmake

ENTRYPOINT ["buildozer"]
CMD ["android", "clean"]