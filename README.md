# Prueba Tecnica 

Esta es una API creada con **FastAPI**, que permite registrar usuarios con validación de datos, persistencia en **MongoDB** y generación de tokens de autenticación **JWT**. El sistema está **contenedorizado con Docker** para facilitar su despliegue.

## Estructura del Proyecto
```
api_user/
├── app/
│ ├── main.py # Punto de entrada FastAPI
│ ├── models.py # Esquemas Pydantic
│ ├── db.py # Conexión MongoDB
│ ├── auth.py # Generación de JWT
│ └── utils.py # Hasheo de contraseñas
├── tests/ # Pruebas unitarias
│ └── test_users.py
├── requirements.txt # Librerías Python
├── Dockerfile # Imagen python
├── docker-compose.yml # Levanta proyecto API y MongoDB
├── .env # Variables secretas (no subir a Git)
└── README.md # Documentación del proyecto
```

### Pre-requisitos 

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)
- Opcional: Python 3.9+ y `pip` para entorno local


## Instrucciones de ejecución
#### 1.- Clonar Repositorio 
```
git clone https://github.com/tu_usuario/api_user.git
cd api_user

```
#### 2.- Variables de Entorno (`.env`)
Antes de ejecutar el docker build debes crear un archivo `.env` con el siguiente contenido en la carpeta api_user:

```env
MONGO_URI=mongodb://mongo:27017
JWT_SECRET=supersecreta123
JWT_ALGORITHM=HS256
```
#### 3.- Construir y levantar contenedores
```
docker-compose up --build
```
Esto iniciará:

FastAPI en: http://localhost:8000

MongoDB en: localhost:27017


#### 4.- Disponibilidad de endpoint

***POST /users***
##### Ejemplo de Request : 
```
{
  "name": "Juan Rodriguez",
  "email": "juan@rodriguez.org",
  "password": "Hunter22",
  "phones": [
    {
      "number": "1234567",
      "citycode": "1",
      "contrycode": "57"
    }
  ]
}
```
##### Ejemplo de Response : 
```
{
  "id": "uuid",
  "created": "2025-07-30T15:00:00.000Z",
  "modified": "2025-07-30T15:00:00.000Z",
  "last_login": "2025-07-30T15:00:00.000Z",
  "token": "jwt_token",
  "isactive": true,
  "name": "Juan Rodriguez",
  "email": "juan@rodriguez.org",
  "phones": [
    {
      "number": "1234567",
      "citycode": "1",
      "contrycode": "57"
    }
  ]
}

```
#### 5.- Ejecucion de Pruebas

```
docker-compose exec app pytest
```
#### Descripcion de pruebas : 
  - Registro exitoso de usuario
  - Validación de email duplicado
  - Validación de formato de email
  - Validación de clave (regex)

### 📌 Validaciones incluidas
✅ Correo electrónico: formato usuario@dominio.cl

✅ Clave: al menos una mayúscula, letras minúsculas y dos números

✅ Mensajes de error en formato JSON: {"mensaje": "texto"}

✅ Protección JWT integrada (generación de token en registro)

### 🛡️ Seguridad
- Hasheo de contraseñas con bcrypt (passlib)

- Tokens JWT firmados y almacenados en base

- Claves secretas y URI ocultas en .env
