FROM ubuntu:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-setuptools && \
    apt-get clean

WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies and CLI tool
RUN pip3 install -r requirements.txt && \
    pip3 install .

# Default command (can be overridden)
CMD ["task-cli", "--help"]
