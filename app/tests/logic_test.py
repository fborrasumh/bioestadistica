"""Prueba del motor con CPython: para cada misión y N semillas, la solución de referencia aprueba (también los casos
ocultos), cada error típico suspende y se reconoce, y el código de partida de los retos no aprueba.

Uso: python3 tests/logic_test.py [N]     (desde app/, tras python3 build.py)
"""
import json
import os
import subprocess
import sys
import time
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
N = sys.argv[1] if len(sys.argv) > 1 else "8"
SOLO = sys.argv[2] if len(sys.argv) > 2 else None
salida = subprocess.run(["node", os.path.join(AQUI, "specs.js"), os.path.join(AQUI, "..", "..", "index.html"), N],
                        capture_output=True, text=True, check=True).stdout
D = json.loads(salida)
ns = {}
exec(D["harness"], ns)
run_spec = ns["run_spec"]

import matplotlib
matplotlib.use("Agg")

fallos, avisos, cuenta = [], Counter(), Counter()
t0 = time.time()
for c in D["casos"]:
    if SOLO and not c["id"].startswith(SOLO):
        continue
    r = json.loads(run_spec(json.dumps(c["spec"])))
    cuenta[c["tipo"]] += 1
    etiqueta = f'{c["id"]} semilla {c["s"]} {c["tipo"]} {c.get("mut", "")}'
    if "interno" in r:
        fallos.append(f"{etiqueta}: interno {r['interno']}")
        continue
    if c["tipo"] == "sol":
        if not r.get("ok") or r.get("hidden_ok") is False:
            fallos.append(f"{etiqueta}: la solución no aprueba {r.get('err') or [x for x in r['checks'] if not x['ok']][:2]}")
    elif c["tipo"] == "mut":
        if r.get("ok"):
            fallos.append(f"{etiqueta}: el error típico aprueba")
        elif r.get("err"):
            fallos.append(f"{etiqueta}: el error típico da una excepción {r['err']}")
        elif r.get("diag") != c["mut"]:
            avisos[f'{c["id"]} {c["mut"]} → {r.get("diag")}'] += 1
    elif c["tipo"] == "starter":
        if r.get("ok"):
            fallos.append(f"{etiqueta}: el código de partida del reto ya aprueba")
    elif c["tipo"] == "ref":
        if "out" not in r:
            fallos.append(f"{etiqueta}: el programa a predecir falla")
    elif c["tipo"] == "alt":
        if r.get("ok"):
            avisos[f'{c["id"]} {c["mut"]}: la alternativa coincide con la salida real'] += 1

print("Misiones:", D["resumen"]["misiones"], D["resumen"]["porTipo"])
temas = D["resumen"]["porTema"]
incompletos = {k: v for k, v in temas.items() if v != 3}
if incompletos:
    print("Temas sin 3 misiones:", incompletos)
print("Tests mal formados:", [q for q in D["quiz"] if q["malas"] or q["n"] < 4])
print("Casos ejecutados:", dict(cuenta), f"en {time.time() - t0:.0f} s")
for a, n in sorted(avisos.items()):
    print(f"  aviso ({n}×): {a}")
for f in fallos[:40]:
    print("  FALLO:", f)
print("FALLOS:", len(fallos))
sys.exit(1 if fallos else 0)
