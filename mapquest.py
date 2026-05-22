# -*- coding: utf-8 -*-
import requests
import sys

# Forzar UTF-8 en la salida de la consola
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjU4ZmI0NjM5NGMxZDQ3NGY5ZDMzYzBjYzM0MjA2N2M1IiwiaCI6Im11cm11cjY0In0="
BASE_URL = "https://api.openrouteservice.org"
CONSUMO_L_POR_KM = 8 / 100  # 8 litros cada 100 km

def obtener_coordenadas(ciudad):
    url = f"{BASE_URL}/geocode/search"
    headers = {"Authorization": API_KEY}
    params = {
        "text": ciudad,
        "boundary.country": "CL",
        "size": 1
    }
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    coords = data["features"][0]["geometry"]["coordinates"]
    return coords

def obtener_ruta(origen, destino):
    coords_origen = obtener_coordenadas(origen)
    coords_destino = obtener_coordenadas(destino)
    url = f"{BASE_URL}/v2/directions/driving-car/json"
    headers = {"Authorization": API_KEY, "Content-Type": "application/json"}
    body = {
        "coordinates": [coords_origen, coords_destino],
        "language": "es"
    }
    r = requests.post(url, headers=headers, json=body)
    return r.json()

def convertir_duracion(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = segundos % 60
    return horas, minutos, segs

def mostrar_resultado(origen, destino):
    print(f"\n  Calculando ruta de {origen} a {destino}...")
    ruta = obtener_ruta(origen, destino)

    resumen = ruta["routes"][0]["summary"]
    distancia_km = resumen["distance"] / 1000
    horas, minutos, segs = convertir_duracion(resumen["duration"])
    combustible = distancia_km * CONSUMO_L_POR_KM
    pasos = ruta["routes"][0]["segments"][0]["steps"]

    print("\n" + "=" * 55)
    print(f"  Origen      : {origen}")
    print(f"  Destino     : {destino}")
    print("=" * 55)
    print(f"  Distancia   : {distancia_km:.2f} km")
    print(f"  Duracion    : {horas} h {minutos} min {segs:.2f} seg")
    print(f"  Combustible : {combustible:.2f} litros")
    print("=" * 55)
    print("\n  NARRATIVA DEL VIAJE:")
    print("-" * 55)
    for i, paso in enumerate(pasos, 1):
        dist_paso = paso["distance"] / 1000
        print(f"  {i}. {paso['instruction']} ({dist_paso:.2f} km)")
    print("=" * 55)

def main():
    print("=" * 55)
    print("     CALCULADORA DE RUTAS - OpenRouteService")
    print("=" * 55)
    print("  Ingrese 'q' en cualquier momento para salir")
    print("=" * 55)

    while True:
        print()
        origen = input("  Ciudad de Origen  : ").strip()
        if origen.lower() == "q":
            print("\n  Saliendo del programa. Hasta luego!\n")
            break

        destino = input("  Ciudad de Destino : ").strip()
        if destino.lower() == "q":
            print("\n  Saliendo del programa. Hasta luego!\n")
            break

        try:
            mostrar_resultado(origen, destino)
        except Exception:
            print("\n  Error: No se pudo calcular la ruta.")
            print("  Verifique los nombres de las ciudades e intente de nuevo.")

        print()
        continuar = input("  Presione Enter para continuar o 'q' para salir: ").strip()
        if continuar.lower() == "q":
            print("\n  Saliendo del programa. Hasta luego!\n")
            break

if __name__ == "__main__":
    main()
