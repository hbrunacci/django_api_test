import requests



# Coloco acá la funcion que obtiene el valor del dolar, podria hacerlo en otra app con auxiliares,
# pero no quiero escalar tanto

def get_dolar_price_today():
    #Todo: Quitar la url de aca y ponerla en un archivo de entorno
    result = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if result.status_code == 200:
        try:
            data = result.json()
            for item in data:
                if item.get('casa').get('nombre') == 'Dolar Blue':
                    decimales = int(item.get('casa').get('decimales'))
                    compra = item.get('casa').get('compra').replace(',', '').replace('.', '')
                    compra = float(compra) / 10 ** decimales
                    venta = item.get('casa').get('venta').replace(',', '').replace('.', '')
                    venta = float(venta) / 10 ** decimales
                    return (compra + venta)/2
        except Exception as e:
            #Todo: logger.debug(e)
            print(e)
            return 0
    else:
        return 0