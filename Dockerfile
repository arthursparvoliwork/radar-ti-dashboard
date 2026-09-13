FROM python:3.12-slim
WORKDIR /app
COPY backend/ ./backend/
COPY database/ ./database/
RUN pip install flask flask-cors gunicorn
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "backend.app:app"]
