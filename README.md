# OxiGo - Aplicacion Web
 *© 2025 OxiGo. Todos los derechos reservados.*

 Este repositorio contiene la aplicación web de *OxiGo*.
## Principales colaboradores:
1. Fédor Tikhomirov
2. Adrián Jauregui Felipe
---
# Enlace a la página web: *[OxiGo](http://13.37.194.239:8000/)*

## API Endpoints
La Web utiliza *Python* para su backend, haciendo uso de la librería FastAPI.
+ ### /v1/users/register
  + Permite el registro de usuarios
  + Método HTTP: POST
+ ### /v1/users/login
  + Permite el inicio de sesión
  + Método HTTP: POST
+ ### /v1/users/update
  + Permite la actualización de datos de usuario
  + Método HTTP: PUT
+ ### /v1/data/bind
  + Permite la vinculación de un sensor a un usuario
  + Método HTTP: POST
+ ### /v1/data/reading
  + Permite el guardado de lecturas de sensor
  + Método HTTP: POST
---

## TESTS
Para los tests se ha usado la librería Pytest.

### Para ejecutar los tests se necesita:

1. Acceder a la instancia EC2 por SSH (explicado abajo)

2. Abrir el entorno virtual de Python (explicado abajo)

3. Acceder al directorio donde se encuentra la APP:
```bash
cd /home/ubuntu/app/
```
4. Ejecutar el comando de los tests:
```bash
PYTHONPATH=. pytest tests/ -v
```