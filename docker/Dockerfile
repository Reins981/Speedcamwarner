# Use a base image with Python 3.10 and Debian Bullseye
FROM python:3.10-bullseye

# Set noninteractive mode to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
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
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    build-essential \
    libsqlite3-dev \ 
    sqlite3 \ 
    bzip2 \ 
    libbz2-dev \
    libffi-dev \
    cmake \
    zip \ 
    unzip \ 
    openjdk-17-jdk


# Install buildozer
RUN pip install --upgrade pip
RUN pip install --upgrade buildozer
RUN pip install cython==0.29.33

# Ensure Java is in PATH
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Expose necessary ports if required (e.g., for debugging)
EXPOSE 5000

# Keep the container running
ENTRYPOINT ["buildozer", "-v"]
