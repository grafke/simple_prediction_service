FROM python:3.7.6
RUN apt-get update
RUN apt-get install -y ffmpeg

# Configure Filesystem
COPY ./app /app
COPY ./resources /resources
COPY ./uploads /uploads
COPY requirements.txt .

RUN pip install -r ./requirements.txt

# Deploy application
EXPOSE 8000

ENV ENVIRONMENT ENV

CMD ["uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"]