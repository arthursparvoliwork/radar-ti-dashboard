FROM python:3.12-slim
WORKDIR /app
COPY backend/ .
RUN pip install flask flask-cors
ENV PORT=8080
EXPOSE 8080
CMD ["python", "-c", "import os; os.environ.setdefault('PORT','8080'); exec(open('app.py').read().replace('debug=True', 'host=\"0.0.0.0\", port=int(os.environ.get(\"PORT\",8080)), debug=False'))"]
