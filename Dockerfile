FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8050
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python","app.py"]
