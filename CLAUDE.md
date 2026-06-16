# CLAUDE.md — Dashboard de Noticias Deportivas

## Qué es este proyecto
Proyecto final de **Programación 1** (universidad). Es una aplicación de
**terminal** en Python que al arrancar muestra un panel en vivo con clima,
tipo de cambio y quote del día, y luego un menú para elegir un deporte y
ver noticias de ESPN. También permite guardar un artículo favorito en
un canal de Discord real via webhook.
Se entrega en GitHub y se defiende **en vivo** ante el profesor.

- Autor: Santiago
- Carpeta del proyecto: `/Users/MrCabs/Documents/Proyecto-Progra-1/`
- Archivo principal: `dashboard_deportivo.py`

## Stack y restricciones (importante respetarlas)
- Python 3.14, editor VS Code (en macOS se usa `python3` y `pip3`).
- **Librerías externas:** `requests` (llamadas a internet) y `rich` (UI en terminal). No agregar otras.
- Instalar con: `pip3 install requests rich`
- El código no tiene límite de líneas fijo, pero **todo debe poder explicarse en una defensa oral.**
- Las 3 funciones de `requests` usadas (requisito del catedrático): `requests.head`, `requests.get`, `requests.post`.

## APIs que usa

### Dashboard (se cargan al inicio, una sola vez)
- **Clima** — OpenWeatherMap: `https://api.openweathermap.org/data/2.5/weather?q=Guatemala City,GT&appid={KEY}&units=metric&lang=es`
  - Requiere API key gratuita en openweathermap.org
  - Campos usados: `datos["main"]["temp"]`, `datos["main"]["humidity"]`, `datos["weather"][0]["description"]`
- **Tipo de cambio** — ExchangeRate API: `https://v6.exchangerate-api.com/v6/{KEY}/latest/USD`
  - Requiere API key gratuita en exchangerate-api.com
  - Campos usados: `datos["conversion_rates"]["GTQ"]`, `datos["conversion_rates"]["EUR"]`
- **Quote del día** — ZenQuotes: `https://zenquotes.io/api/random`
  - Sin API key. Devuelve una lista; el primer elemento tiene `["q"]` (quote) y `["a"]` (autor)

### Noticias (se cargan al elegir un deporte)
ESPN, endpoints públicos (no necesitan API key ni headers):
- Soccer: `https://site.api.espn.com/apis/site/v2/sports/soccer/all/news`
- NBA: `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news`
- F1: `https://site.api.espn.com/apis/site/v2/sports/racing/f1/news`
- NFL: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/news`
- Tennis: `https://site.api.espn.com/apis/site/v2/sports/tennis/news`

La respuesta llega como JSON; los datos viven en `datos["articles"]`.
Cada artículo trae `["headline"]` (título).

### Favoritos (al guardar desde el menú de noticias)
- **Discord Webhook** — URL del canal configurada como constante `DISCORD_WEBHOOK` en el código.
  - Se crea en: Discord → Servidor → Editar canal → Integraciones → Webhooks → Nuevo webhook → Copiar URL
  - `requests.post` envía JSON con `"username"` y `"content"`. Respuesta exitosa: status 204.

## Decisiones ya tomadas (no rehacer sin avisar)
- **Se descartó la API de Reddit.** Reddit bloqueaba las peticiones y
  devolvía contenido que no era JSON, rompiendo `.json()`. Se migró a ESPN.
- **Se agregó `rich` para la UI.** Aunque el requisito original era solo
  `requests`, el catedrático permite librerías adicionales. `rich` maneja
  los paneles, tablas y colores en terminal. No usar `print()` para output
  visual; usar `console.print()`.
- **Discord Webhook como destino del `requests.post`.** Es la forma más
  honesta y visible de usar POST: el resultado aparece en tiempo real en
  un canal de Discord mientras se hace la defensa. Alternativas descartadas:
  `jsonplaceholder.typicode.com` (datos ficticios) y APIs de votación (forzado).
- **`requests.head` para verificar conexión.** Es un patrón profesional real:
  hace una petición sin descargar datos para chequear si el servidor responde.
- La estructura del menú se mantuvo igual que el proyecto original:
  diccionario opción→URL, `while True`, `if/break` para salir, validación con `not in`.
- No nombrar ningún archivo `requests.py`: choca con la librería y causa error de auto-importación.

## Nivel del estudiante (clave para enseñar bien)
- En clase se ha visto formalmente: variables, condicionales, ciclos y
  librerías externas. Diccionarios, listas y funciones van un poco más
  adelante en el curso — al usarlos, explicarlos con cuidado.
- Tiene experiencia práctica con automatizaciones en Python, pero a nivel
  formal de curso es principiante.

## Cómo trabajar con Santiago
- Mostrar primero el código completo funcionando, **luego** explicar línea
  por línea.
- Antes de escribir código, explicar **qué** se va a hacer y **por qué**.
- Usar analogías simples al introducir conceptos nuevos.
- Si algo está mal, **explicar por qué** está mal, no solo corregirlo.
- Al final de cada paso, confirmar que entendió antes de seguir.
- Para esta tarea, actuar como **tutor**, no como piloto automático: el
  estudiante debe poder defender el código él mismo.

## Objetivo a largo plazo
Aprender APIs y automatizaciones para ofrecerlas como **servicio a empresas**.
Cuando algo del proyecto conecte con esa meta, señalarlo.

## Estructura del código (dashboard_deportivo.py)
```
verificar_conexion()   → requests.head  → chequea internet al arrancar
obtener_dashboard()    → requests.get   → clima + cambio + quote (3 APIs)
obtener_noticias(url)  → requests.get   → noticias de ESPN por deporte
guardar_favorito(...)  → requests.post  → postea a Discord
mostrar_dashboard(...) → rich Panel     → pinta el panel principal
mostrar_menu()         → rich Rule      → pinta el menú de deportes
mostrar_noticias(...)  → rich Table     → pinta noticias + maneja favorito
main()                 → loop principal con console.status() para spinners
```
