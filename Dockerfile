FROM python:3

LABEL maintainer="darmiel <hi@d2a.io>"
LABEL org.opencontainers.image.source="https://github.com/darmiel/todoist-project-allocation"

WORKDIR /usr/src/app

# Requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

CMD [ "python", "./main.py" ]