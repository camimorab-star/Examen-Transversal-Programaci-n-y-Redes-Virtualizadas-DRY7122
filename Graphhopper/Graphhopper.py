import requests

API_KEY = "5ab30ae3-0092-434b-ab0a-d0674891d692"

GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"


def salir(valor):
    return valor.lower() == "s"


def obtener_coordenadas(ciudad, pais):
    parametros = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    respuesta = requests.get(GEOCODE_URL, params=parametros)

    if respuesta.status_code != 200:
        print("Error al consultar la API de geocodificación.")
        return None

    datos = respuesta.json()

    if len(datos["hits"]) == 0:
        print(f"No se encontraron coordenadas para {ciudad}, {pais}.")
        return None

    punto = datos["hits"][0]["point"]

    return {
        "lat": punto["lat"],
        "lng": punto["lng"],
        "nombre": datos["hits"][0].get("name", ciudad),
        "pais": pais
    }


def elegir_transporte():
    print("\nSeleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")
    print("s. Salir")

    opcion = input("Ingrese una opción: ")

    if salir(opcion):
        return "salir"

    if opcion == "1":
        return "car"
    elif opcion == "2":
        return "bike"
    elif opcion == "3":
        return "foot"
    else:
        print("Opción inválida. Se usará auto por defecto, porque incluso el código se cansó de esperar claridad.")
        return "car"


def nombre_transporte(transporte):
    if transporte == "car":
        return "Auto"
    elif transporte == "bike":
        return "Bicicleta"
    elif transporte == "foot":
        return "Caminando"
    return "Desconocido"


def convertir_duracion(ms):
    segundos = int(ms / 1000)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return horas, minutos, segundos


def calcular_ruta(origen, destino, transporte):
    parametros = {
        "point": [
            f"{origen['lat']},{origen['lng']}",
            f"{destino['lat']},{destino['lng']}"
        ],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(ROUTE_URL, params=parametros)

    if respuesta.status_code != 200:
        print("Error al consultar la ruta en GraphHopper.")
        print(respuesta.text)
        return None

    datos = respuesta.json()

    if "paths" not in datos or len(datos["paths"]) == 0:
        print("No se pudo calcular la ruta.")
        return None

    return datos["paths"][0]


def mostrar_resultado(origen, destino, transporte, ruta):
    distancia_km = ruta["distance"] / 1000
    distancia_millas = distancia_km * 0.621371

    horas, minutos, segundos = convertir_duracion(ruta["time"])
    print(f"Ciudad de Origen: {origen['nombre']}, Chile")
    print(f"Ciudad de Destino: {destino['nombre']}, Perú")
    print(f"Medio de transporte: {nombre_transporte(transporte)}")
    print(f"Distancia en kilómetros: {distancia_km:.2f} km")
    print(f"Distancia en millas: {distancia_millas:.2f} mi")
    print(f"Duración del viaje: {horas} horas, {minutos} minutos, {segundos} segundos")

    print("\n========== NARRATIVA DEL VIAJE ==========")
    instrucciones = ruta.get("instructions", [])
    if len(instrucciones) == 0:
        print("No se encontraron instrucciones para la ruta.")
    else:
        for i, instruccion in enumerate(instrucciones, start=1):
            texto = instruccion.get("text", "Sin instrucción")
            distancia = instruccion.get("distance", 0) / 1000
            tiempo = instruccion.get("time", 0)
            h, m, s = convertir_duracion(tiempo)
            print(f"{i}. {texto}")
            print(f"   Distancia: {distancia:.2f} km")
            print(f"   Tiempo estimado: {h} h {m} min {s} seg")
def main():
    while True:
        print("\n========================================")
        print("Consulta de viaje Chile - Perú con GraphHopper")
        print("Ingrese 's' para salir en cualquier momento.")
        print("========================================")
        ciudad_origen = input("Ciudad de Origen en Chile: ")
        if salir(ciudad_origen):
            print("Programa finalizado.")
            break
        ciudad_destino = input("Ciudad de Destino en Perú: ")
        if salir(ciudad_destino):
            print("Programa finalizado.")
            break
        transporte = elegir_transporte()
        if transporte == "salir":
            print("Programa finalizado.")
            break
        origen = obtener_coordenadas(ciudad_origen, "Chile")
        if origen is None:
            continue
        destino = obtener_coordenadas(ciudad_destino, "Perú")
        if destino is None:
            continue
        ruta = calcular_ruta(origen, destino, transporte)
        if ruta is None:
            continue
        mostrar_resultado(origen, destino, transporte, ruta)
if __name__ == "__main__":
    main()