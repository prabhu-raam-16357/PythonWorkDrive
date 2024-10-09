# Base image with Ubuntu
FROM ubuntu:20.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y curl wget software-properties-common && \
    apt-get clean

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Java (OpenJDK 17)
RUN apt-get install -y openjdk-17-jdk

# Install Python 3.9 and pip
RUN apt-get install -y python3.9 python3.9-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py && \
    rm get-pip.py

# Verify installations
RUN node -v && npm -v && java -version && python3.9 --version && pip --version

# Set default shell to bash
CMD ["/bin/bash"]
