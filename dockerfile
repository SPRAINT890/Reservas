# Utiliza una imagen base oficial de Python
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /code

# Copia los archivos de requerimientos
COPY Backend/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . /code

# Comando para iniciar la aplicación
CMD ["uvicorn", "Backend.api.user:app", "--host", "0.0.0.0", "--port", "8080"]