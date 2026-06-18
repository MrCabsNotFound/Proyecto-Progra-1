#  DASHBOARD DE NOTICIAS DEPORTIVAS — Proyecto Final Progra 1
#  Clima · Tipo de cambio · Quote del día · Noticias ESPN
#
#  Librerías externas:
#    - requests  → para todas las llamadas a internet
#    - rich      → para la interfaz visual en terminal
#
#  Funciones de requests usadas:
#    1. requests.head  → verifica conexión antes de arrancar
#    2. requests.get   → trae clima, cambio, quote y noticias
#    3. requests.post  → guarda favoritos en Discord

import requests
from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich.text    import Text
from rich.rule    import Rule
from rich         import box
from config import OPENWEATHER_KEY, EXCHANGERATE_KEY, DISCORD_WEBHOOK

CIUDAD = "Guatemala City,GT"

# ── SETUP ─────────────────────────────────────────────────────
console = Console()

# ── DICCIONARIOS ──────────────────────────────────────────────
NOTICIAS_URL = {
    "1": "https://site.api.espn.com/apis/site/v2/sports/soccer/all/news",
    "2": "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news",
    "3": "https://site.api.espn.com/apis/site/v2/sports/racing/f1/news",
    "4": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news",
    "5": "https://site.api.espn.com/apis/site/v2/sports/tennis/news",
}

NOMBRES = {
    "1": "⚽  SOCCER",
    "2": "🏀  NBA",
    "3": "🏎️   FORMULA 1",
    "4": "🏈  NFL",
    "5": "🎾  TENNIS",
}

CLIMA_EMOJIS = {
    "clear"   : "☀️ ",
    "cloud"   : "☁️ ",
    "rain"    : "🌧️ ",
    "storm"   : "⛈️ ",
    "snow"    : "❄️ ",
    "mist"    : "🌫️ ",
    "fog"     : "🌫️ ",
    "drizzle" : "🌦️ ",
}

def get_emoji_clima(descripcion):
    """Devuelve el emoji que corresponde a la condición del clima."""
    for clave, emoji in CLIMA_EMOJIS.items():
        if clave in descripcion.lower():
            return emoji
    return "🌡️ "


#  FUNCIÓN 1 ── requests.head
#  Hace una petición liviana (solo headers, sin descargar datos)
#  para verificar que hay internet antes de arrancar el programa.
def verificar_conexion():
    try: #Intenta esto
        requests.head("https://www.cloudflare.com", timeout=5)
        return True #Si llegó acá, perfecto
    except requests.exceptions.RequestException:
        return False #Si no algo falló


#  FUNCIÓN 2 ── requests.get
#  Trae datos de 3 APIs distintas para el dashboard,
#  y también se usa para traer las noticias de ESPN.
def obtener_dashboard():
    """Trae clima, tipo de cambio y quote del día."""

    # 1. Clima — OpenWeatherMap
    url_clima   = (f"https://api.openweathermap.org/data/2.5/weather"
                   f"?q={CIUDAD}&appid={OPENWEATHER_KEY}&units=metric&lang=es")
    datos_clima = requests.get(url_clima).json()
    temperatura = datos_clima["main"]["temp"]
    descripcion = datos_clima["weather"][0]["description"].capitalize()
    humedad     = datos_clima["main"]["humidity"]

    # 2. Tipo de cambio — ExchangeRate API
    url_cambio   = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_KEY}/latest/USD"
    datos_cambio = requests.get(url_cambio).json()
    gtq          = datos_cambio["conversion_rates"]["GTQ"]
    eur          = datos_cambio["conversion_rates"]["EUR"]

    # 3. Quote del día — ZenQuotes (sin API key)
    datos_quote = requests.get("https://zenquotes.io/api/random").json()[0]
    quote       = datos_quote["q"]
    autor       = datos_quote["a"]

    return temperatura, descripcion, humedad, gtq, eur, quote, autor


def obtener_noticias(url):
    """Trae las noticias del deporte seleccionado desde ESPN."""
    datos = requests.get(url).json()
    return datos["articles"]


#  FUNCIÓN 3 ── requests.post
#  Envía el artículo favorito a un canal de Discord real
#  a través de un webhook, creando un mensaje visible al instante.
def guardar_favorito(titular, deporte, link):
    """Postea el artículo favorito a Discord via webhook."""
    mensaje = {
        "username": "Dashboard Deportivo 🏆",
        "content" : (f"⭐ **Nuevo favorito guardado**\n"
                     f"🏅 Deporte: {deporte}\n"
                     f"📰 {titular}\n"
                     f"🔗 {link}")
    }
    r = requests.post(DISCORD_WEBHOOK, json=mensaje)
    return r.status_code == 204   # 204 = Discord confirmó que lo recibió


#FUNCIONES DE DISPLAY

def mostrar_dashboard(temperatura, descripcion, humedad, gtq, eur, quote, autor):
    """Construye y muestra el panel principal del dashboard."""

    emoji = get_emoji_clima(descripcion)

    contenido = Text(justify="left")
    contenido.append(f"\n  {emoji} Clima en Guatemala City\n", style="bold cyan")
    contenido.append(f"     {temperatura:.1f}°C  ·  {descripcion}  ·  Humedad {humedad}%\n\n", style="white")

    contenido.append("  💵 Tipo de cambio\n", style="bold green")
    contenido.append(f"     1 USD  =  {gtq:.4f} GTQ\n", style="white")
    contenido.append(f"     1 USD  =  {eur:.4f} EUR\n\n", style="white")

    contenido.append("  💬 Quote del día\n", style="bold yellow")
    contenido.append(f'     "{quote}"\n', style="italic white")
    contenido.append(f"      — {autor}\n", style="dim white")

    console.print(Panel(
        contenido,
        title     = "[bold white]🌍  DASHBOARD GUATEMALA[/bold white]",
        subtitle  = "[dim]datos en vivo[/dim]",
        border_style = "bright_blue",
        padding   = (0, 2),
    ))


def mostrar_menu():
    """Muestra el menú de selección de deportes."""
    console.print()
    console.print(Rule("[bold white]NOTICIAS DEPORTIVAS[/bold white]", style="bright_blue"))
    console.print()
    console.print("   [cyan bold]1.[/cyan bold]  ⚽  Soccer")
    console.print("   [cyan bold]2.[/cyan bold]  🏀  NBA")
    console.print("   [cyan bold]3.[/cyan bold]  🏎️   Formula 1")
    console.print("   [cyan bold]4.[/cyan bold]  🏈  NFL")
    console.print("   [cyan bold]5.[/cyan bold]  🎾  Tennis")
    console.print("   [cyan bold]6.[/cyan bold]  🚪  Salir")
    console.print()


def mostrar_noticias(articulos, deporte):
    """Muestra las noticias en una tabla y ofrece guardar un favorito."""

    tabla = Table(
        title        = f"Últimas noticias — {deporte}",
        box          = box.ROUNDED,
        border_style = "bright_blue",
        title_style  = "bold white",
        show_lines   = True,
    )
    tabla.add_column("#",       style="bold cyan", width=4, justify="center")
    tabla.add_column("Titular", style="white",     min_width=60)

    top5 = articulos[:5]
    for i, art in enumerate(top5, start=1):
        tabla.add_row(str(i), art["headline"])

    console.print()
    console.print(tabla)

    # Opción de guardar favorito → requests.post
    console.print()
    console.print("  [dim]¿Guardar alguna en Discord? Escribí el número o Enter para saltar:[/dim]")
    eleccion = input("  → ").strip()

    if eleccion.isdigit() and 1 <= int(eleccion) <= len(top5):
        articulo = top5[int(eleccion) - 1]
        titular  = articulo["headline"]
        link     = articulo.get("links", {}).get("web", {}).get("href", "")

        with console.status("[bold cyan]Enviando a Discord...[/bold cyan]"):
            exito = guardar_favorito(titular, deporte, link)

        if exito:
            console.print(f"\n  [bold green]✅ ¡Guardado en Discord![/bold green]")
            console.print(f"  [dim]{titular}[/dim]\n")
        else:
            console.print("\n  [bold red]❌ Error al enviar. Revisá el webhook en el código.[/bold red]\n")


# ── MAIN ──────────────────────────────────────────────────────
def main():
    console.clear()

    # 1. Verificar conexión con requests.head
    with console.status("[bold cyan]Verificando conexión...[/bold cyan]"):
        conectado = verificar_conexion()

    if not conectado:
        console.print(Panel(
            "[bold red]Sin conexión a internet. Revisá tu red e intentá de nuevo.[/bold red]",
            border_style="red"
        ))
        return

    # 2. Cargar dashboard con requests.get
    with console.status("[bold cyan]Cargando dashboard...[/bold cyan]"):
        temperatura, descripcion, humedad, gtq, eur, quote, autor = obtener_dashboard()

    mostrar_dashboard(temperatura, descripcion, humedad, gtq, eur, quote, autor)

    # 3. Loop del menú de noticias
    activo = True
    while activo:
        mostrar_menu()
        opcion = input("  Elegí una opción (1-6): ").strip()

        if opcion == "6":
            console.print()
            console.print(Panel(
                "[bold cyan]¡Hasta luego! 👋[/bold cyan]",
                border_style="bright_blue",
                expand=False
            ))
            console.print()
            activo = False

        elif opcion in NOTICIAS_URL:
            with console.status("[bold cyan]Cargando noticias...[/bold cyan]"):
                articulos = obtener_noticias(NOTICIAS_URL[opcion])
            mostrar_noticias(articulos, NOMBRES[opcion])

        else:
            console.print("\n  [bold red]Opción inválida. Intentá con un número del 1 al 6.[/bold red]")


if __name__ == "__main__":
    main()
