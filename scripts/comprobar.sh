#!/bin/bash
# Genera y ejecuta los cuadernos indicados; uso: ./comprobar.sh 020 030
set -e
cd "$(dirname "$0")"
for n in "$@"; do
  salida=$(python3 "tema_$n.py")
  cuaderno="${salida#../}"
  mkdir -p /tmp/ejecucion && cp "../$cuaderno" /tmp/ejecucion/
  (cd /tmp/ejecucion && jupyter nbconvert --to notebook --execute "$(basename "$cuaderno")" --output "/tmp/exec_$n.ipynb" >/dev/null 2>&1)
  python3 - "$n" <<'EOF'
import sys, nbformat
n = sys.argv[1]
nb = nbformat.read(f"/tmp/exec_{n}.ipynb", 4)
errores = [o for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"]
print(f"Tema {n}: {len(nb.cells)} celdas, {len(errores)} errores")
for e in errores:
    print("  ", e.ename, e.evalue)
EOF
done
