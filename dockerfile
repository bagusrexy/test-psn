# Gunakan gambar resmi Python sebagai basis
FROM python:3.8.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py

# Buat direktori untuk aplikasi
# RUN mkdir /app
WORKDIR /app

# Salin file requirements.txt dan instal dependensi
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi ke direktori kerja
COPY . /app/

# Ekspose port 8080
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["flask", "db", "upgrade"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
