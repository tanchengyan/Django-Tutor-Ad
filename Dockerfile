FROM python:3.12-slim

RUN echo "deb http://mirrors.cloud.tencent.com/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.tencent.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.tencent.com/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.cloud.tencent.com/debian/ bookworm-backports main contrib non-free" >> /etc/apt/sources.list && \
    cat /etc/apt/sources.list
RUN apt-get update -o Acquire::http::Pipeline-Depth=0 -o Acquire::http::No-Cache=true && \
    apt-get install -y \
    libpq-dev gcc netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
# Expose the Django development port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
