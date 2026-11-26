"""Regenera la tabla «Cuadernos disponibles» del README a partir de los cuadernos."""
import glob
import re
import nbformat

filas = []
for ruta in sorted(glob.glob("../cuadernos/Tema_*.ipynb")):
    nb = nbformat.read(ruta, 4)
    m = re.search(r"Tema (\d+)\. (.+?)</font>", nb.cells[0].source)
    numero, titulo = m.group(1), m.group(2)
    fichero = ruta.split("/")[-1]
    if numero == "0":
        titulo += " (lectura previa obligatoria)"
    enlace = f"https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/{fichero}"
    filas.append(f"| {numero} | {titulo} | [Colab]({enlace}) |")

tabla = "| Tema | Título | Abrir |\n| --- | --- | --- |\n" + "\n".join(filas) + "\n"
readme = open("../README.md").read()
readme = re.sub(r"(## Cuadernos disponibles\n\n)\| Tema \| Título \| Abrir \|\n(?:\|.*\|\n)+", r"\g<1>" + tabla.replace("\\", "\\\\"), readme)
open("../README.md", "w").write(readme)
print(f"{len(filas)} cuadernos en el README")
