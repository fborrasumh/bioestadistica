"""Dibuja las figuras fijas de las diapositivas en ../figuras/tema_XXX_nombre.png.

Uso: python3 figuras.py            (todas)
     python3 figuras.py 150 160    (solo esos temas)
"""
import os
import sys

import matplotlib.pyplot as plt

from diapositivas import DIAPOS, FIGS
from diapositivas.diagramas import TEMAS as ESQUEMAS
from diapositivas.diagramas2 import EXTRA

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "figuras")
os.makedirs(SALIDA, exist_ok=True)
temas = {int(x) for x in sys.argv[1:]}
faltan = []
for tema, lista in sorted(DIAPOS.items()):
    if temas and tema not in temas:
        continue
    for d in lista:
        if not d.get("fig"):
            continue
        f = FIGS.get((tema, d["fig"]))
        if f is None:
            faltan.append(f"{tema}/{d['fig']}")
            continue
        fig = f()
        ruta = os.path.join(SALIDA, f"tema_{tema:03d}_{d['fig']}.png")
        fig.savefig(ruta, facecolor="white")
        plt.close(fig)
        print(ruta.split("/")[-1])
for tema in ESQUEMAS:  # un diagrama por tema (tema_XXX_esquema.png)
    if temas and tema not in temas:
        continue
    fig = FIGS[(tema, "esquema")]()
    ruta = os.path.join(SALIDA, f"tema_{tema:03d}_esquema.png")
    fig.savefig(ruta, facecolor="white")
    plt.close(fig)
    print(ruta.split("/")[-1])
for tema, nombre in EXTRA:  # diagramas de los apartados 2.x (tema_XXX_e2_N.png)
    if temas and tema not in temas:
        continue
    fig = FIGS[(tema, nombre)]()
    ruta = os.path.join(SALIDA, f"tema_{tema:03d}_{nombre}.png")
    fig.savefig(ruta, facecolor="white")
    plt.close(fig)
    print(ruta.split("/")[-1])
if faltan:
    sys.exit("Faltan funciones de figura: " + ", ".join(faltan))
