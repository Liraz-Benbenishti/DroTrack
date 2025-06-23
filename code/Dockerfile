# Use the official Ubuntu image as the base
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and required system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install tensorflow
RUN python3 -m pip install opencv-python
RUN python3 -m pip install scipy
RUN python3 -m pip install pandas
RUN python3 -m pip install numpy

COPY . /code
COPY ./datasets /datasets

CMD ["python3", "/code/run.py"]