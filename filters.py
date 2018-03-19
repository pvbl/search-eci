## script que mapea filtros de precios, descuentos y marcas a la url de ElCorte Ingles

brands = { "Apple":102979,
        "Samsung":112395, 
        "Huawei":107952,
        "XIAOMI":193851,
        "Sony":112899,
        "bq":103964,
}

discounts={ "10":133543,
     "20":133544,
     "30":133545,
     "40":133546,
}



__prices = list(range(25,250,25)) + list(range(250,500,50)) + list(range(500,1000,100)) + list(range(1000,1500,250))
__mapps = list(range(20004,20024))

prices_mapper = dict(zip(__prices,__mapps)) 


