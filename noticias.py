# ============================================================
#  CONSOLA DE NOTICIAS DEPORTIVAS  -  Proyecto Final Progra 1
#  Trae las noticias mas recientes de ESPN y las muestra en terminal.
#  Unica libreria externa usada: requests
# ============================================================

import requests  # libreria para pedir datos por internet

# Cada opcion del menu apunta directo a la URL de noticias de ESPN.
# La llave (izquierda) es lo que el usuario escribe; el valor es la direccion.
noticias_url = {
    "1": "https://site.api.espn.com/apis/site/v2/sports/soccer/all/news",
    "2": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news",
    "3": "https://site.api.espn.com/apis/site/v2/sports/racing/f1/news",
    "4": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news",
}

# Nombre bonito de cada deporte para el encabezado de resultados.
nombres = {"1": "SOCCER", "2": "NBA", "3": "FORMULA 1", "4": "NFL",}

# while True mantiene el programa vivo hasta que el usuario decida salir.
while True:
    # ----- 1. Mostrar el menu -----
    print("\n" + "=" * 42)
    print("      CONSOLA DE NOTICIAS DEPORTIVAS")
    print("=" * 42)
    print("  1. Soccer")
    print("  2. NBA")
    print("  3. Formula 1")
    print("  4. NFL")
    print("  5. Salir")
    print("=" * 42)

    opcion = input("Elige una opcion (1-5): ")

    # ----- 2. Salir del programa -----
    if opcion == "5":
        print("Gracias por usar la consola!")
        break  # break rompe el while y termina el programa

    # ----- 3. Validar que la opcion exista en el menu -----
    if opcion not in noticias_url:
        print("Opcion invalida, intenta de nuevo.")
        continue  # continue regresa al inicio del while sin pedir datos

    # ----- 4. Pedir los datos a ESPN -----
    url = noticias_url[opcion]              # busca la direccion en el diccionario
    respuesta = requests.get(url)           # el "mesero" trae los datos
    datos = respuesta.json()                # convierte la respuesta en diccionario

    # La lista de articulos vive dentro de datos["articles"]
    articulos = datos["articles"]

    # ----- 5. Mostrar los resultados formateados -----
    print("\n" + "=" * 42)
    print("   NOTICIAS DE " + nombres[opcion])
    print("=" * 42)

    # enumerate da el numero (1,2,3...) y el articulo al mismo tiempo.
    # articulos[:5] = solo los primeros 5.
    for numero, articulo in enumerate(articulos[:5], start=1):
        titulo = articulo["headline"]
        link = articulo["links"]["web"]["href"]
        print(f"\n{numero}. {titulo}")
        print(f"   Link: {link}")

    print("\n" + "=" * 42)