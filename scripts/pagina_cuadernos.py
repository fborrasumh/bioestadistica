"""Genera ../cuadernos.html: la página con los 31 cuadernos de Colab, enlazada desde la app Bioestadística.

Uso: python3 pagina_cuadernos.py   (también la ejecuta publicar.sh)
"""
import glob
import html
import os
import re

import nbformat

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = "fborrasumh/bioestadistica"
MODULOS = [
    (0, 0, "Antes de empezar", "Guía del entorno: léela antes de la primera sesión."),
    (10, 40, "Módulo 1. Descubriendo Python", "Examen E1, a mano."),
    (50, 80, "Módulo 2. Programando con IA", "Examen E2, a mano."),
    (90, 130, "Módulo 3. Procesado inicial de datos", "Examen E3, con Colab."),
    (140, 190, "Módulo 4. Probabilidad", "Examen E4, a mano."),
    (200, 300, "Módulo 5. Generalización de conclusiones", "Examen E5, con Colab."),
]


def cuadernos():
    for f in sorted(glob.glob(os.path.join(AQUI, "..", "cuadernos", "Tema_*.ipynb"))):
        nb = nbformat.read(f, 4)
        m = re.search(r"Tema (\d+)\. (.+?)</font>", nb.cells[0].source)
        diapos = sum("border-left:8px" in c.source for c in nb.cells if c.cell_type == "markdown")
        yield int(m.group(1)), m.group(2), os.path.basename(f), diapos


def tarjeta(n, titulo, fichero, diapos):
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/cuadernos/{fichero}"
    github = f"https://github.com/{REPO}/blob/main/cuadernos/{fichero}"
    extra = f'<span class="chip">{diapos} diapositivas</span>' if diapos else '<span class="chip">Lectura previa</span>'
    practica = '<a class="btn ghost" href="./">Practicar en la app</a>' if n else ""
    return f"""<article class="card" data-busca="{html.escape(f'tema {n} {titulo}'.lower())}">
  <p class="num">Tema {n}</p>
  <h3>{html.escape(titulo)}</h3>
  <p class="meta">{extra}</p>
  <div class="acc"><a class="btn" href="{colab}" target="_blank" rel="noopener">Abrir en Colab ↗</a><a class="btn ghost" href="{github}" target="_blank" rel="noopener">Ver en GitHub ↗</a>{practica}</div>
</article>"""


def main():
    lista = list(cuadernos())
    bloques = []
    for a, b, nombre, nota in MODULOS:
        tarjetas = "\n".join(tarjeta(*c) for c in lista if a <= c[0] <= b)
        bloques.append(f'<section class="mod"><h2>{nombre}</h2><p class="nota">{nota}</p><div class="grid">\n{tarjetas}\n</div></section>')
    pagina = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:">
<title>Cuadernos · Bioestadística (1964) · Medicina UMH</title>
<meta name="description" content="Los 31 cuadernos de Colab de Bioestadística (1964), 2.º de Medicina, Universidad Miguel Hernández de Elche. Fernando Borrás Rocher. CC BY 4.0.">
<style>
:root{{--tinta:#0F2237;--suave:#5D7691;--azul:#C8461F;--naranja:#E4572E;--fondo:#F4F6FA;--borde:#D9E2EC}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--tinta);background:var(--fondo);line-height:1.5}}
a{{color:var(--azul)}}
.top{{background:#0F2237;position:sticky;top:0;z-index:2}}
.top .in{{max-width:1180px;margin:0 auto;padding:10px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
.logo{{font-weight:800;font-size:21px;text-decoration:none;color:#fff;font-family:Georgia,serif}}
.logo em{{font-style:normal;color:var(--naranja)}}
.top input{{flex:1;min-width:200px;padding:10px 14px;border:1px solid #33475B;border-radius:10px;font-size:16px;background:#16304A;color:#fff}}
.top input::placeholder{{color:#9FB0C3}}
main{{max-width:1180px;margin:0 auto;padding:20px}}
.hero h1{{font-size:clamp(26px,4vw,38px);margin:10px 0 6px}}
.hero p{{color:var(--suave);max-width:820px;margin:0 0 6px;font-size:17px}}
.mod{{margin-top:30px}}
.mod h2{{font-size:22px;margin:0;border-left:6px solid var(--naranja);padding-left:12px}}
.nota{{color:var(--suave);margin:4px 0 12px 18px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}}
.card{{background:#fff;border:1px solid var(--borde);border-radius:14px;padding:16px 18px;display:flex;flex-direction:column}}
.card .num{{margin:0;font-weight:700;color:var(--azul);font-size:14px;letter-spacing:.03em}}
.card h3{{margin:4px 0 8px;font-size:17px;line-height:1.35}}
.meta{{margin:0 0 12px}}
.chip{{display:inline-block;font-size:13px;background:#EAF1F8;color:var(--suave);border-radius:999px;padding:2px 10px}}
.acc{{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap}}
.btn{{display:inline-block;padding:9px 13px;border-radius:9px;background:var(--azul);color:#fff;text-decoration:none;font-weight:600;font-size:14px;min-height:40px}}
.btn.ghost{{background:#fff;color:var(--azul);border:1px solid var(--borde)}}
.btn:focus-visible,.top input:focus-visible,.logo:focus-visible{{outline:3px solid #F2A900;outline-offset:2px}}
.oculto{{display:none}}
#vacio{{color:var(--suave)}}
footer{{max-width:1180px;margin:30px auto;padding:0 20px;color:var(--suave);font-size:14px}}
</style>
</head>
<body>
<div class="top"><div class="in">
  <a class="logo" href="./">Bio<em>estadística</em></a>
  <input id="busca" type="search" placeholder="Buscar un tema: Bayes, regresión, pandas…" aria-label="Buscar un tema">
  <a class="btn" href="./">← Volver a la app</a>
</div></div>
<main>
<div class="hero">
  <h1>Cuadernos de la asignatura</h1>
  <p>Bioestadística (1964) · 2.º del Grado en Medicina · Universidad Miguel Hernández de Elche · Curso 2027-2028.</p>
  <p>Un cuaderno de Colab por sesión de 50 minutos, con diapositivas para la clase y el desarrollo para el estudio. Abre el cuaderno y guarda tu copia con <b>Archivo → Guardar una copia en Drive</b>; después practica sus tres misiones en la app.</p>
</div>
{chr(10).join(bloques)}
<p id="vacio" class="oculto">Ningún tema coincide con la búsqueda.</p>
</main>
<footer>Fernando Borrás Rocher · ORCID <a href="https://orcid.org/0000-0002-5519-4573">0000-0002-5519-4573</a> · Contenidos con licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es">CC BY 4.0</a> · Todos los datos de los cuadernos son sintéticos · <a href="https://github.com/{REPO}">Repositorio</a></footer>
<script>
const caja = document.getElementById('busca');
const norm = s => s.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
caja.addEventListener('input', () => {{
  const q = norm(caja.value.trim());
  let visibles = 0;
  document.querySelectorAll('.card').forEach(c => {{ const ok = !q || norm(c.dataset.busca).includes(q); c.classList.toggle('oculto', !ok); visibles += ok; }});
  document.querySelectorAll('.mod').forEach(m => m.classList.toggle('oculto', !m.querySelector('.card:not(.oculto)')));
  document.getElementById('vacio').classList.toggle('oculto', visibles > 0);
}});
</script>
</body>
</html>
"""
    salida = os.path.join(AQUI, "..", "cuadernos.html")
    open(salida, "w", encoding="utf-8").write(pagina)
    print(f"cuadernos.html: {len(lista)} cuadernos")


if __name__ == "__main__":
    main()
