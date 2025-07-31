FROM python:3.10
#Establecemos directorio de trabajo
WORKDIR /app
#Copiamos el archivo de requerimientos
COPY requirements.txt .
#actualizamos pip 
RUN pip install --upgrade pip
#Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
