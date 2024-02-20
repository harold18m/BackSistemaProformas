# Usar una imagen base de Python
FROM python:3.8-slim-buster

# Establecer un directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos e instalar las dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Definir el comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]