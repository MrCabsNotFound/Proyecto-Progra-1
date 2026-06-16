# CLAUDE.md — Consola de Noticias Deportivas

## Qué es este proyecto
Proyecto final de **Programación 1** (universidad). Es una aplicación de
**terminal** en Python que muestra un menú, deja elegir un deporte, trae
noticias en vivo desde la API pública de ESPN y las muestra formateadas.
Se entrega en GitHub y se defiende **en vivo** ante el profesor.

- Autor: Santiago
- Carpeta del proyecto: `/Users/MrCabs/Documents/Proyecto-Progra-1/`
- Archivo principal: `noticias.py`

## Stack y restricciones (importante respetarlas)
- Python 3.14, editor VS Code (en macOS se usa `python3` y `pip3`).
- **Única librería externa permitida: `requests`.** No agregar otras.
- El código debe quedar entre **50 y 70 líneas** incluyendo comentarios.
- Todo debe poder explicarse en una defensa oral.

## API que usa
ESPN, endpoints públicos (no necesitan API key ni headers):
- Soccer: `https://site.api.espn.com/apis/site/v2/sports/soccer/all/news`
- NBA: `https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news`
- F1: `https://site.api.espn.com/apis/site/v2/sports/racing/f1/news`
- NFL: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/news`

La respuesta llega como JSON; los datos viven en `datos["articles"]`.
Cada artículo trae `["headline"]` (título) y `["links"]["web"]["href"]` (link).

## Decisiones ya tomadas (no rehacer sin avisar)
- **Se descartó la API de Reddit.** Reddit bloqueaba las peticiones y
  devolvía contenido que no era JSON, rompiendo `.json()`. Además ESPN no
  necesita headers. Costo del cambio: ESPN no tiene "votos" (eso era de
  Reddit), así que se muestra solo título + link.
- La estructura del programa es: diccionario opción→URL, `while True` para
  el menú, `if/break` para salir, `if not in/continue` para validar,
  `for` con `enumerate` y slice `[:5]` para mostrar las primeras 5 noticias.

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

## Gotcha conocido
No nombrar ningún archivo `requests.py`: choca con la librería `requests`
y causa un error de auto-importación.
