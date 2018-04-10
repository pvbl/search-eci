# Introduccion
Busca objetos y los filtra de la pagina del corte Ingles. Funciona como API.
# Instalación
```
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip -r requirements.txt
$ python webhook.py
```

# Funcionamiento
<url>/webhook: Devuelve para DF el formato de JSON preciso.
<url>/searcheci: devuelve los resultados generados a partir de hacer una peticion POST con los parametros descritos.

## parametros del POST
- item: producto a filtrar (ej. samsung)
- price\_min: precio minimo en el filtro
- price\_max: precio máximo en el filtro
- discount: si tiene un determinado descuento
- limit: el número de productos a ser mostrados
- inbound: exactamente el numero del producto deseado (observado anteriormente)

