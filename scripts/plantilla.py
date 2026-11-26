"""Plantilla común de los cuadernos de Bioestadística (1964, UMH).

Autor: Fernando Borrás Rocher. Cada script tema_XXX.py usa estas funciones
para generar su cuaderno en cuadernos/.
"""
import pprint
import nbformat as nbf

REPO = "fborrasumh/bioestadistica"
APP = "https://fborrasumh.github.io/bioestadistica/"
COLOR = "steelblue"


class Cuaderno:
    def __init__(self, fichero):
        self.fichero = fichero
        self.celdas = []

    def md(self, texto):
        self.celdas.append(nbf.v4.new_markdown_cell(texto.strip()))

    def code(self, texto, oculta=False):
        celda = nbf.v4.new_code_cell(texto.strip())
        if oculta:
            celda.metadata["cellView"] = "form"
        self.celdas.append(celda)

    def titulo(self, nivel, texto):
        self.md(f"{'#' * nivel} <font color='{COLOR}'>{texto}</font>")

    def cabecera(self, numero, titulo, modulo, duracion, practica=True, nota=""):
        badge = (
            f'<a href="https://colab.research.google.com/github/{REPO}/blob/main/cuadernos/{self.fichero}" '
            'target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" '
            'alt="Abrir en Colab"/></a>'
        )
        linea_practica = (
            f"**Práctica:** [unidad {numero} de la app Bioestadística]({APP})\n\n" if practica else ""
        )
        self.md(f"""
{badge}

# <font color='{COLOR}'>Tema {numero}. {titulo}</font>

**Bioestadística (1964) · Grado en Medicina · 2.º curso · Curso 2026-2027**

**{modulo}**

**Autor:** Fernando Borrás Rocher · Universidad Miguel Hernández de Elche · ORCID [0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573)

**Duración:** {duracion}

{linea_practica}{nota}**Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Todos los pacientes y datos de este cuaderno son sintéticos.

*Antes de trabajar, guarda tu copia: **Archivo → Guardar una copia en Drive**.*
""")

    def configuracion(self):
        self.titulo(2, "Configuración del cuaderno")
        self.md("Ejecuta esta celda al empezar. Instala el módulo de preguntas interactivas y prepara el cuaderno.")
        self.code("""
#@title Ejecutar configuración
%pip install -q jupyterquiz==2.9.6.4
from jupyterquiz import display_quiz
print("Cuaderno configurado")
""", oculta=True)

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
