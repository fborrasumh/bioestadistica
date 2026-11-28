"""Plantilla común de los cuadernos de Bioestadística (1964, UMH).

Autor: Fernando Borrás Rocher. Cada script tema_XXX.py usa estas funciones
para generar su cuaderno en cuadernos/.
"""
import os
import html
import pprint
import nbformat as nbf

try:
    from diapositivas import DIAPOS
except ImportError:  # sin diapositivas, el cuaderno se genera igual
    DIAPOS = {}

REPO = "fborrasumh/bioestadistica"
APP = "https://fborrasumh.github.io/bioestadistica/"


def retos_app(numero):
    """Títulos de las tres misiones del tema, leídos de app/src (la app es la fuente)."""
    import glob, re
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app", "src")
    tit = {}
    for f in sorted(glob.glob(os.path.join(raiz, "[1-5]0_*.js"))):
        s = open(f, encoding="utf-8").read()
        for m in re.finditer(r"QZ\('m(\d+)-(\d)', \d+, \d, '((?:[^'\\]|\\.)*)'", s):
            tit[(int(m[1]), int(m[2]))] = m[3]
        for m in re.finditer(r"M\(\{id: 'm(\d+)-(\d)'.*?\n\s*t: E\('((?:[^'\\]|\\.)*)'\)", s):
            tit[(int(m[1]), int(m[2]))] = m[3]
    return [tit[(numero, k)].replace("\\'", "'") for k in (1, 2, 3)]
COLOR = "steelblue"
FIGURAS = f"https://raw.githubusercontent.com/{REPO}/main/figuras"


class Cuaderno:
    def __init__(self, fichero):
        self.fichero = fichero
        self.celdas = []
        self.numero = None
        self.usadas = set()

    def md(self, texto):
        self.celdas.append(nbf.v4.new_markdown_cell(texto.strip()))

    def code(self, texto, oculta=False):
        celda = nbf.v4.new_code_cell(texto.strip())
        if oculta:
            celda.metadata["cellView"] = "form"
        self.celdas.append(celda)

    def titulo(self, nivel, texto):
        self.md(f"{'#' * nivel} <font color='{COLOR}'>{texto}</font>")
        for i, d in enumerate(DIAPOS.get(self.numero, [])):
            if i not in self.usadas and texto.startswith(d["ancla"]):
                self.usadas.add(i)
                self.diapositiva(d)
                if d.get("desarrollo", True):
                    self.md("#### Desarrollo para el estudio")

    def diapositiva(self, d):
        """Celda grande para proyectar: título, figura (PNG del repo, foto con licencia libre o gráfico
        de una celda oculta) y 2-4 ideas. El desarrollo queda debajo, en una sección plegable."""
        partes = [f'<p style="font-size:30px;font-weight:700;color:#1F3B57;margin:0 0 12px 0">{d["titulo"]}</p>']
        if d.get("fig"):
            partes.append(f'<img src="{FIGURAS}/tema_{self.numero:03d}_{d["fig"]}.png" width="{d.get("ancho", 780)}" '
                          f'alt="{html.escape(d.get("alt", d["titulo"]))}">')
        if d.get("foto"):
            url, credito, ancho = d["foto"]
            partes.append(f'<img src="{url}" width="{ancho}" alt="{html.escape(d.get("alt", d["titulo"]))}">'
                          f'<p style="font-size:13px;color:#667;margin:4px 0 0 0">{credito}</p>')
        if d.get("ideas"):
            items = "".join(f"<li>{x}</li>" for x in d["ideas"])
            partes.append(f'<ul style="font-size:21px;line-height:1.55;margin:14px 0 0 0">{items}</ul>')
        if d.get("pregunta"):
            partes.append(f'<p style="font-size:21px;margin:14px 0 0 0;color:#8A4B08"><b>Pregunta para la clase:</b> {d["pregunta"]}</p>')
        self.md('<div style="border-left:8px solid #4682B4;background:#F3F7FB;padding:18px 26px;border-radius:8px">'
                + "".join(partes) + "</div>")
        if d.get("codigo"):
            self.code(f"#@title {d.get('titulo_codigo', 'Figura: ' + d['titulo'])}\n" + d["codigo"].strip(), oculta=True)

    def diagrama(self, alt, ancho=760, nombre="esquema"):
        """Inserta un diagrama del tema (figuras/tema_XXX_<nombre>.png), con texto alternativo."""
        self.md(f'<img src="{FIGURAS}/tema_{self.numero:03d}_{nombre}.png" width="{ancho}" alt="{html.escape(alt)}">')

    def cabecera(self, numero, titulo, modulo, duracion, practica=True, nota=""):
        badge = (
            f'<a href="https://colab.research.google.com/github/{REPO}/blob/main/cuadernos/{self.fichero}" '
            'target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" '
            'alt="Abrir en Colab"/></a>'
        )
        linea_practica = (
            f"**Retos en la app:** [las tres misiones del Tema {numero}]({APP}#tema-{numero})\n\n" if practica else ""
        )
        self.numero = numero
        self.practica = practica
        self.md(f"""
{badge}

# <font color='{COLOR}'>Tema {numero}. {titulo}</font>

**Bioestadística (1964) · Grado en Medicina · 2.º curso · Curso 2027-2028**

**{modulo}**

**Autor:** Fernando Borrás Rocher · Universidad Miguel Hernández de Elche · ORCID [0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573)

**Duración:** {duracion}

{linea_practica}{nota}**Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Todos los pacientes y datos de este cuaderno son sintéticos.

*Antes de trabajar, guarda tu copia: **Archivo → Guardar una copia en Drive**.*
""")

    def configuracion(self):
        self.titulo(2, "Configuración del cuaderno")
        self.md("Ejecuta esta celda al empezar. Instala el módulo de preguntas interactivas y prepara el cuaderno.\n\n"
                "**Para dar la clase con el cuaderno:** antes de empezar, usa **Entorno de ejecución → Ejecutar todo**. Así se dibujan los gráficos. "
                "Las celdas con borde azul son las diapositivas. Debajo de cada una está el desarrollo del bloque; pliégalo con la flecha de su título. "
                "El índice (☰, a la izquierda) sirve para saltar de un bloque a otro.")
        self.code("""
#@title Ejecutar configuración
%pip install -q jupyterquiz==2.9.6.4
from jupyterquiz import display_quiz
print("Cuaderno configurado")
""", oculta=True)

    def conexion_ia(self):
        """Celdas de conexión con Gemini y función preguntar(); sin clave, cliente = None."""
        self.md("""
Esta celda prepara la conexión con el modelo de lenguaje (Tema 80). Lee la clave de Secretos sin mostrarla. Si no hay clave, el cuaderno funciona con respuestas de ejemplo. Si el modelo indicado ya no existe, cambia la variable `MODELO`.
""")
        self.code('''
%pip install -q google-genai

MODELO = "gemini-2.5-flash"

try:
    from google.colab import userdata
    from google import genai
    from google.genai import types
    cliente = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))
    print("Conexión preparada con el modelo", MODELO)
except Exception as error:
    cliente = None
    print("Sin clave o fuera de Colab: se usarán respuestas de ejemplo.", type(error).__name__)


def preguntar(prompt, temperatura=0.2):
    """Envía un prompt al modelo y devuelve su texto (None si no hay conexión)."""
    if cliente is None:
        return None
    respuesta = cliente.models.generate_content(
        model=MODELO,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperatura),
    )
    return respuesta.text
''')

    def quiz(self, preguntas):
        """preguntas: lista de (enunciado, [(respuesta, correcta, explicacion), ...]),
        con una sola respuesta correcta por pregunta."""
        datos = [
            {
                "question": enunciado,
                "type": "multiple_choice",
                "answers": [
                    {"answer": r, "correct": c, "feedback": f} for r, c, f in respuestas
                ],
            }
            for enunciado, respuestas in preguntas
        ]
        self.code(
            "#@title Pregunta interactiva\n"
            f"preguntas = {pprint.pformat(datos, width=100, sort_dicts=False)}\n"
            "display_quiz(preguntas)",
            oculta=True,
        )

    def pie(self, numero):
        if getattr(self, "practica", False):
            r = retos_app(numero)
            self.md(f"""
## <font color='{COLOR}'>Retos de este tema en la app</font>

Practica lo que has visto con las tres misiones del Tema {numero} en la app **Bioestadística**. Cuentan para la evaluación continua.

1. **Básica (sin ayuda):** {r[0]}
2. **Clínica (con pistas):** {r[1]}
3. **Reto (con asistente de IA):** {r[2]}

<a href="{APP}#tema-{numero}" target="_blank" style="display:inline-block;padding:10px 18px;background:#C8461F;color:#fff;border-radius:8px;font-weight:bold;text-decoration:none">Abrir los retos del Tema {numero} en la app ↗</a>
""")
        self.md(f"""
---
*Tema {numero} · Bioestadística (1964) · Grado en Medicina · Universidad Miguel Hernández de Elche · Fernando Borrás Rocher · CC BY 4.0*
""")

    def guardar(self, carpeta="cuadernos"):
        nb = nbf.v4.new_notebook()
        nb["cells"] = self.celdas
        nb["metadata"] = {
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        }
        ruta = f"{carpeta}/{self.fichero}"
        nbf.write(nb, ruta)
        return ruta
