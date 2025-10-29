# RRVV - Aplicacion Web
 *© 2025 RRVV Systems. Todos los derechos reservados.*

 Este repositorio contiene la aplicación web de *RRVV Systems*.
## Principales colaboradores:
1. Fédor Tikhomirov
2. Adrián Jauregui Felipe
---
# Enlace a la página web: *[RRVV Systems](http://13.37.194.239:8000/)*

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

## PARA DESARROLLADORES:

### Para acceder a la instancia EC2 en la que se aloja el servidor, ejecutar en **cmd**:
```bash
ssh -i "{Ruta a clave privada de SSH}" ubuntu@{IP de la instancia}
```

### Para acceder a la base de datos una vez dentro de la instancia:
```bash
sudo mysql
```
Seleccionar base de datos:
```sql
USE RRVVDB;
```
Salir de mySQL:

```sql
EXIT;
```

### Para comprobar logs del servidor:
1. Entrar en el entorno virtual de python:
```bash
source venv/bin/activate
```
2. Entrar en el directorio del servidor:
```bash
cd app
```
3. Leer logs:
```bash
cat app.log
```