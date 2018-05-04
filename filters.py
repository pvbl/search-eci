## script que mapea filtros de precios, descuentos y marcas a la url de ElCorte Ingles


categories = ['electronica','moda','electrodomesticos','hogar','bebes','juguetes','videojuegos','perfumeria','regalos-originales','libros','supermercado']







#### Electronica
#brands = { "apple":102979,
#        "samsung":112395, 
#        "huawei":107952,
#        "xiaomi":193851,
#        "sony":112899,
#        "bq":103964,
#}
brands={}

#discounts={ 10:133543,
#     20:133544,
#     30:133545,
#     40:133546,
#}

discounts={ 10:"0->11,,",
     20:"11->21,,",
     30:"21->31,,",
     40:"31->41,,",
     50:"41->51,,",
     60:"51->61,,",
     70:"61->71,,",
}


### ojo! no esta bien. ECI mapea en 19 categorias de precios pero son variables entre min y max
__prices = list(range(25,250,25)) + list(range(250,500,50)) + list(range(500,1000,100)) + list(range(1000,1500+250,250))
__mapps=["{0}->{1},,".format(__prices[i],__prices[i+1]) for i in range(len(__prices)-1)]
#__mapps = list(range(20004,20024))

prices_mapper = dict(zip(__prices,__mapps)) 


