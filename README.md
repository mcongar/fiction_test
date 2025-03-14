# 📚 Django API Project

Este proyecto es una API REST desarrollada con Django REST Framework (DRF) para la gestión de libros y usuarios, 
utilizando autenticación JWT. Incluye documentación en Swagger con DRF Spectacular.

---

## 🚀 Tecnologías utilizadas
- **Python 3.10+**
- **Django 5.1**
- **Django REST Framework**
- **DRF Spectacular (Swagger)**
- **MySQL 8.0**
- **Docker y Docker Compose**

---

### Levantar el proyecto con Docker
docker-compose up --build

### Aplicar las migraciones
docker-compose exec web python manage.py migrate

### Crear un superusuario
docker-compose exec web python manage.py createsuperuser


### Documentación de la API
- **Django Admin** → http://localhost:8000/admin/

- **Swagger UI** → http://localhost:8000/swagger/

- **Esquema OpenAPI** → http://localhost:8000/schema/