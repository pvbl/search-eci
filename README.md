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
- category: categoria a la que pertenece el producto (ropa,electronica,...) (opcional)
- subcategory: subcategoria a la que pertenece el producto (opcional)
- helper_search: Para evitar que acabe en el land de la pagina, introduccion de un elemento clave que evite esto. P.e. telefono (opcional)
- price\_min: precio minimo de los productos. (opcional)
- price\_max: precio máximo de los productos. (opcional)
- discount: precio minimo. (opcional)
- limit: el número de productos a ser mostrados (opcional)
- inbound: exactamente el numero del producto deseado ej. el numeroo 5 (opcional)



#### Ejemplos 1
Por defecto busca en category='electronica', subcategory = 'moviles-y-smartphones' y helper_search='telefono'.
```
{"result":{
"parameters":{
	"item":"Samsung",
	"limit":5
	}
  }
}
```

#### Ejemplos 2
Buscar articulos en ropa de mujer
```
{"result":{
"parameters":{
    "item":"",
    "category":"moda",
    "subcategory":"",
    "helper_search":"mujer"
   }
  }
}
```


### Ruta <url>/returnItem
- href: ruta URL del producto en ECI 
#### Ejemplo Post
url: localhost:5000/returnItem
method: POST
body
```
{
  "result": 
      {"parameters":
            {
                "href":"https://www.elcorteingles.es/moda/A23426124-chaqueta-de-mujer-tintoretto-con-cinturon-y-cuello-alto/"
                
            }
  }
}
```






# Errores y cosas a tener en cuenta para futuras versiones
- filtrar por precio no está bien. El corte Inglés tiene 19 categorías de división de precios variables entre máximo y mínimo. El primero máximo y mínimo es desconocido. No tengo claro si sucede lo mismo con discount.
- He probado con pocas categorías y subcategorías diferentes a moviles, sería necesario verificar que funciona bien.
- A un futuro estaría bien añadir page, category, subcategory en el JSON de request. (Sencillo)
- Falta introducir SKU para APIstock


