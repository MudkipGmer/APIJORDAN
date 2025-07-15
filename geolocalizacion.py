
import requests
import json

resultados = []

print("Escribe una IP pública (o escribe 'exit' para terminar):")

while True:
    ip = input("IP: ").strip()

    if ip.lower() == "exit":
        break

    if not ip:
        print("No ingresaste ninguna IP. Intenta de nuevo.")
        continue

    url = f"http://ip-api.com/json/{ip}"

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            print(f"No se pudo conectar correctamente. Código HTTP: {response.status_code}")
            continue

        try:
            data = response.json()
        except ValueError:
            print("La respuesta no es un JSON válido.")
            continue

        if data.get('status') == 'success':
            info = {
                'IP': ip,
                'País': data.get('country', ''),
                'Región': data.get('regionName', ''),
                'ISP': data.get('isp', ''),
                'Coordenadas': {
                    'Latitud': data.get('lat', ''),
                    'Longitud': data.get('lon', '')
                }
            }
            resultados.append(info)
            print(json.dumps(info, indent=4, ensure_ascii=False))
        else:
            mensaje = data.get('message', 'No se obtuvo información válida.')
            print(f"No se pudo obtener información para la IP {ip}: {mensaje}")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

# Guardar resultados en JSON si hay datos
if resultados:
    try:
        with open("resultados_ips.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=4, ensure_ascii=False)
        print("Resultados guardados en 'resultados_ips.json'")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
else:
    print("No se guardó ningún archivo porque no se obtuvieron resultados válidos.")
