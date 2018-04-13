# Introduccion
Busca objetos y los filtra de la pagina del corte Ingles. Funciona como API.
# Instalación y levantamiento de la API

```
$ virtualenv venv -p python3
$ source venv/bin/activate
$ pip -r requirements.txt
$ python3 webhook.py
```



# Rutas de la API
<url>/webhook: Devuelve para DialogFlow el formato de JSON preciso dando información de un móvil determinado.
<url>/searcheci: devuelve una lista de items de móviles a partir de hacer una peticion POST con los parametros descritos en la siguiente sección.
<url>/returnItem: devuelve los resultados generados a partir de hacer una peticion POST con los parametros descritos.
	

## parametros del POST
El JSON que se envía en el body del POST tiene la forma:
```
{
  "result": 
      {"parameters":
            {
                param_1k:param_1v,
                param_2k:param_2v,
                param_3k:param_3v
                
            }
  }
}
```
Donde los parámetros a modificar en el JSON son los que se encuentran dentro del campo parameters. Esto se ha realizado por motivos de cómo envía los datos de Dialogflow.

 
### Ruta <url>/searcheci
- item: producto a filtrar (ej. samsung, móvil (para caso genérico), iphone...)
- price\_min: precio minimo de los productos.
- price\_max: precio máximo de los productos.
- discount: precio minimo.
- limit: el número de productos a ser mostrados
- inbound: exactamente el numero del producto deseado (observado anteriormente)

### Ruta <url>/returnItem
- href: ruta del producto: (Ej. "href":"https://www.elcorteingles.es/moda/A23426124-chaqueta-de-mujer-tintoretto-con-cinturon-y-cuello-alto/")



# Errores y cosas a tener en cuenta para futuras versiones
- filtrar por precio no está bien. El corte Inglés tiene 19 categorías de división de precios variables entre máximo y mínimo. El primero máximo y mínimo es desconocido. No tengo claro si sucede lo mismo con discount.
- He probado con pocas categorías y subcategorías diferentes a moviles, sería necesario verificar que funciona bien.
- A un futuro estaría bien añadir page, category, subcategory en el JSON de request. (Sencillo)



