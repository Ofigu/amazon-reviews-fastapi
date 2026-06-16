FROM python:3.12-alpine
WORKDIR /api
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]
