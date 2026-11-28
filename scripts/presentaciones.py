"""Genera ../presentaciones/tema_XXX.html: una presentación por cuaderno (31, con el Tema 0).

Cada diapositiva tiene un modo: «magistral» (clase expositiva), «colab» (práctica guiada en el cuaderno)
o «ambos». En la presentación, el selector de modo deja solo las diapositivas de la sesión que se da.
Así se pueden intercalar sesiones de clase magistral y sesiones de Colab con el mismo material.

Uso: python3 presentaciones.py   (también la ejecuta publicar.sh)
"""
import ast
import glob
import html
import os
import re

import markdown
import nbformat

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = "fborrasumh/bioestadistica"
SALIDA = os.path.join(AQUI, "..", "presentaciones")
RAW_FIG = f"https://raw.githubusercontent.com/{REPO}/main/figuras/"
APP = f"https://fborrasumh.github.io/bioestadistica/"
MODULOS = [(0, 0, "Antes de empezar"), (10, 40, "Módulo 1. Descubriendo Python"), (50, 80, "Módulo 2. Programando con IA"),
           (90, 130, "Módulo 3. Procesado inicial de datos"), (140, 190, "Módulo 4. Probabilidad"),
           (200, 300, "Módulo 5. Generalización de conclusiones")]


def limpia_titulo(s):
    return re.sub(r"<.*?>", "", s.split("\n")[0].lstrip("#").strip()).strip()


def md(texto):
    """Markdown a HTML sin romper las fórmulas LaTeX (KaTeX las dibuja en el navegador)."""
    formulas = []

    def guarda(m):
        formulas.append(m.group(0))
        return f"\x00{len(formulas) - 1}\x00"

    t = re.sub(r"\$\$.+?\$\$|(?<![\\$])\$[^$\n]+?\$", guarda, texto, flags=re.S)
    h = markdown.markdown(t, extensions=["tables", "fenced_code", "sane_lists"])
    h = re.sub(r"\x00(\d+)\x00", lambda m: html.escape(formulas[int(m.group(1))], quote=False), h)
    h = h.replace(RAW_FIG, "../figuras/")
    return re.sub(r'<a href="(http[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', h)


def diapo_cuaderno(src):
    """Lee la diapositiva del cuaderno (div con borde de 8 px) y devuelve título, imágenes, puntos y pregunta."""
    tit = re.search(r"<p[^>]*font-size:30px[^>]*>(.*?)</p>", src, re.S)
    imgs = re.findall(r'<img src="([^"]+)"[^>]*alt="([^"]*)"', src)
    ul = re.search(r"<ul[^>]*>(.*?)</ul>", src, re.S)
    preg = re.search(r"<p[^>]*color:#8A4B08[^>]*>(.*?)</p>", src, re.S)
    puntos = re.findall(r"<li>(.*?)</li>", ul.group(1), re.S) if ul else []
    return dict(titulo=tit.group(1) if tit else "", imgs=[(u.replace(RAW_FIG, "../figuras/"), a) for u, a in imgs],
                puntos=puntos, pregunta=preg.group(1) if preg else "")


def es_diapo(src):
    return src.lstrip().startswith("<div") and "border-left:8px" in src


def imagen_sola(src):
    m = re.fullmatch(r'\s*<img src="([^"]+)"[^>]*alt="([^"]*)"\s*/?>\s*', src, re.S)
    return (m.group(1).replace(RAW_FIG, "../figuras/"), m.group(2)) if m else None


def preguntas_quiz(src):
    if "preguntas" not in src:
        return []
    src = "\n".join(l for l in src.split("\n") if not l.lstrip().startswith(("%", "!")))
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "preguntas":
            return ast.literal_eval(n.value)
    return []


def codigo_visible(src):
    return "\n".join(l for l in src.split("\n") if not l.startswith("#@title")).strip()


def modo_de(titulo, tiene_codigo):
    t = titulo.lower()
    if any(k in t for k in ("autoevaluación", "ideas clave", "glosario", "para saber más", "objetivos")):
        return "ambos"
    if any(k in t for k in ("demostración", "recorrido", "práctica en la app", "reto", "retos de este tema")):
        return "colab"
    if any(k in t for k in ("caso clínico", "conceptos clave", "ampliación")):
        return "magistral"
    return "colab" if tiene_codigo else "magistral"


def secciones(nb):
    """Agrupa las celdas en secciones (##) y apartados (###)."""
    out, sec = [], None
    for c in nb.cells[1:]:
        s = c.source
        if c.cell_type == "markdown" and s.startswith("## "):
            sec = dict(titulo=limpia_titulo(s), apartados=[dict(titulo=None, celdas=[])])
            out.append(sec)
            resto = s.split("\n", 1)[1].strip() if "\n" in s else ""
            if resto:
                sec["apartados"][-1]["celdas"].append(("markdown", resto))
            continue
        if sec is None:
            continue
        if c.cell_type == "markdown" and s.startswith("### "):
            sec["apartados"].append(dict(titulo=limpia_titulo(s), celdas=[]))
            resto = s.split("\n", 1)[1].strip() if "\n" in s else ""
            if resto:
                sec["apartados"][-1]["celdas"].append(("markdown", resto))
            continue
        sec["apartados"][-1]["celdas"].append((c.cell_type, s))
    for sec in out:
        sec["apartados"] = [a for a in sec["apartados"] if a["celdas"] or a["titulo"]]
    return out


def cuerpo_apartado(celdas, con_codigo):
    """HTML de la diapositiva y notas del profesor («Desarrollo para el estudio»)."""
    cuerpo, notas, en_notas, quiz = [], [], False, []
    for tipo, s in celdas:
        if tipo == "code":
            if "display_quiz" in s:
                quiz += preguntas_quiz(s)
                continue
            if s.startswith("#@title Figura") and not con_codigo:
                continue
            destino = notas if en_notas else cuerpo
            destino.append(f'<pre class="code"><code class="language-python">{html.escape(codigo_visible(s))}</code></pre>')
            continue
        if s.strip().startswith("#### Desarrollo para el estudio"):
            en_notas = True
            continue
        if es_diapo(s):
            d = diapo_cuaderno(s)
            h = "".join(f'<figure><img src="{u}" alt="{html.escape(a)}" loading="lazy"></figure>' for u, a in d["imgs"])
            if d["titulo"]:
                h = f'<p class="lema">{d["titulo"]}</p>' + h
            if d["puntos"]:
                h += "<ul class='puntos'>" + "".join(f"<li>{p}</li>" for p in d["puntos"]) + "</ul>"
            if d["pregunta"]:
                h += f'<p class="pregunta">{d["pregunta"]}</p>'
            cuerpo.append(h)
            continue
        img = imagen_sola(s)
        if img:
            # una figura va siempre a la diapositiva, aunque esté en el desarrollo
            cuerpo.append(f'<figure><img src="{img[0]}" alt="{html.escape(img[1])}" loading="lazy"></figure>')
            continue
        (notas if en_notas else cuerpo).append(md(s))
    return "".join(cuerpo), "".join(notas), quiz


def quiz_html(preguntas, ident):
    bloques = []
    for i, q in enumerate(preguntas):
        ops = "".join(
            f'<button type="button" class="op" data-ok="{int(a["correct"])}" data-fb="{html.escape(a.get("feedback", ""))}">'
            f'{html.escape(str(a["answer"]))}</button>' for a in q["answers"])
        bloques.append(f'<div class="quiz" id="{ident}-{i}"><p class="qq">{html.escape(q["question"])}</p>'
                       f'<div class="ops">{ops}</div><p class="fb" aria-live="polite"></p></div>')
    return "".join(bloques)


def construye(f, todos):
    nb = nbformat.read(f, 4)
    portada = nb.cells[0].source
    n = int(re.search(r"Tema (\d+)\.", portada).group(1))
    titulo = re.search(r"Tema \d+\. (.+?)</font>", portada).group(1)
    modulo = next(nom for a, b, nom in MODULOS if a <= n <= b)
    examen = re.search(r"\*\*Evaluación:\*\*(.+)", portada)
    fichero = os.path.basename(f)
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/cuadernos/{fichero}"
    app = f"{APP}#tema-{n}" if n else APP

    D = []  # diapositivas: (modo, bloque, html, notas)

    def diapo(modo, bloque, h, notas="", clase=""):
        D.append((modo, bloque, h, notas, clase))

    secs = secciones(nb)
    obj = next((s for s in secs if s["titulo"].startswith("Objetivos")), None)
    plan = next((s for s in secs if s["titulo"].startswith("Plan de la sesión")), None)

    diapo("ambos", "Portada", f"""<p class="eyebrow">Bioestadística (1964) · Grado en Medicina · Curso 2027-2028</p>
<h1><span class="num">Tema {n}</span>{html.escape(titulo)}</h1>
<p class="mod">{html.escape(modulo)}</p>
{f'<p class="ev"><b>Evaluación:</b> {md(examen.group(1).strip())[3:-4]}</p>' if examen else ''}
<div class="acc"><a class="btn" href="{colab}" target="_blank" rel="noopener">Abrir el cuaderno en Colab ↗</a><a class="btn ghost" href="{app}" target="_blank" rel="noopener">{'Misiones en la app ↗' if n else 'App Bioestadística ↗'}</a></div>
<p class="autor">Fernando Borrás Rocher · Universidad Miguel Hernández de Elche · CC BY 4.0</p>""", clase="portada")

    if obj:
        h, _, _ = cuerpo_apartado(obj["apartados"][0]["celdas"], False)
        diapo("ambos", "Objetivos", "<h2>Objetivos de aprendizaje</h2>" + h)

    # plan: qué bloque va en cada tipo de sesión
    filas = []
    for s in secs:
        m = re.match(r"(\d+)\. (.+?)(?: \((\d+) min\))?$", s["titulo"])
        if m:
            filas.append((m.group(1), m.group(2), m.group(3), modo_de(s["titulo"], any(t == "code" for a in s["apartados"] for t, _ in a["celdas"]))))
    col = lambda modo: "".join(f'<li><b>{num}.</b> {html.escape(t)}{f" <span class=min>{mi} min</span>" if mi else ""}</li>' for num, t, mi, mo in filas if mo in (modo, "ambos"))
    diapo("ambos", "Plan", f"""<h2>Cómo usar esta presentación</h2>
<p>Usa el selector de arriba para dar el tema en <b>una sesión completa</b> o en <b>dos sesiones intercaladas</b>.</p>
<div class="dos"><div class="ses mag"><h3>🎓 Sesión de clase magistral</h3><ul>{col("magistral")}</ul><p class="help">Explica los conceptos, haz la pausa activa y cierra con las ideas clave.</p></div>
<div class="ses lab"><h3>💻 Sesión de Colab</h3><ul>{col("colab")}</ul><p class="help">Cada estudiante abre su copia del cuaderno, predice el resultado y después ejecuta la celda.</p></div></div>
<p class="help">Teclas: ← → para pasar · <kbd>N</kbd> notas del profesor · <kbd>M</kbd> cambiar de modo · <kbd>F</kbd> pantalla completa · <kbd>Esc</kbd> índice.</p>""")

    pausa_hecha = False
    for s in secs:
        tit = s["titulo"]
        if tit.startswith(("Configuración", "Objetivos", "Plan de la sesión", "Contenidos", "Retos de este tema")):
            continue
        tiene_codigo = any(t == "code" and "display_quiz" not in x for a in s["apartados"] for t, x in a["celdas"])
        modo = modo_de(tit, tiene_codigo)
        bloque = re.sub(r"\s*\(\d+ min\)$", "", tit)

        quiz_sec = []
        for a in s["apartados"]:
            con_codigo = modo != "magistral"
            h, notas, quiz = cuerpo_apartado(a["celdas"], con_codigo)
            quiz_sec += quiz
            if not h and not notas:
                continue
            sub = f"<h3>{html.escape(a['titulo'])}</h3>" if a["titulo"] else ""
            modo_a = "magistral" if a["titulo"] and a["titulo"].lower().startswith("ampliación") else modo
            if modo_a == "colab" and "<pre" in h:
                h = f'<p class="colab-cta">▶ En tu cuaderno: <b>{html.escape(a["titulo"] or bloque)}</b>. Antes de ejecutar, escribe qué esperas obtener.</p>' + h
            h2 = "Ampliación" if modo_a != modo else bloque
            diapo(modo_a, h2, f"<h2>{html.escape(h2)}</h2>{sub}{h}", notas, clase="denso" if len(h) > 2600 else "")

        if quiz_sec:
            diapo(modo, bloque, f"<h2>{html.escape(bloque)}</h2><p class='help'>Elige una opción: verás la explicación.</p>" + quiz_html(quiz_sec, f"q{len(D)}"), clase="denso")

        if tit.startswith("2. Conceptos") and not pausa_hecha:
            # pausa activa con la primera pregunta de la autoevaluación
            todas = [q for x in nb.cells if x.cell_type == "code" and "display_quiz" in x.source for q in preguntas_quiz(x.source)]
            if todas:
                diapo("magistral", "Pausa activa", "<h2>Pausa activa</h2><p class='help'>Piensa 30 segundos, comenta con quien tienes al lado y vota.</p>" + quiz_html(todas[:1], "pausa"))
            diapo("magistral", "Puente a Colab", f"""<h2>En la sesión de Colab</h2>
<p>Lo que acabas de ver se comprueba con datos en el cuaderno del Tema {n}.</p>
<ol><li>Abre el cuaderno y guarda tu copia: <b>Archivo → Guardar una copia en Drive</b>.</li><li>Ejecuta la celda de configuración.</li><li>Ve a la demostración y predice cada resultado antes de ejecutar.</li></ol>
<div class="acc"><a class="btn" href="{colab}" target="_blank" rel="noopener">Abrir el cuaderno en Colab ↗</a></div>""")
            pausa_hecha = True

    # cierre con navegación entre temas
    i = [t[0] for t in todos].index(n)
    prev = todos[i - 1] if i > 0 else None
    sig = todos[i + 1] if i + 1 < len(todos) else None
    nav = "".join(f'<a class="btn ghost" href="tema_{t[0]:03d}.html">{lab} Tema {t[0]}</a>' for t, lab in ((prev, "←"), (sig, "→")) if t)
    diapo("ambos", "Cierre", f"""<h2>Para seguir</h2>
<div class="acc"><a class="btn" href="{colab}" target="_blank" rel="noopener">Cuaderno del Tema {n} en Colab ↗</a><a class="btn" href="{app}" target="_blank" rel="noopener">{'Misiones del tema en la app ↗' if n else 'App Bioestadística ↗'}</a><a class="btn ghost" href="../cuadernos.html">Todos los cuadernos</a></div>
<div class="acc">{nav}</div>""", clase="portada")

    secciones_html = []
    for k, (modo, bloque, h, notas, clase) in enumerate(D):
        nt = f'<aside class="notas" hidden><h4>Notas del profesor · desarrollo para el estudio</h4>{notas}</aside>' if notas else ""
        etiqueta = {"magistral": "🎓 Clase magistral", "colab": "💻 Colab", "ambos": ""}[modo]
        secciones_html.append(f'<section class="slide {clase}" data-modo="{modo}" data-bloque="{html.escape(bloque)}" aria-roledescription="diapositiva">'
                              f'{f"<span class=tag-{modo}>{etiqueta}</span>" if etiqueta else ""}<div class="in">{h}</div>{nt}</section>')
    return n, PLANTILLA.replace("@@TITULO@@", html.escape(f"Tema {n}. {titulo}")).replace("@@SLIDES@@", "\n".join(secciones_html)).replace("@@N@@", str(n))


PLANTILLA = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITULO@@ · Presentación · Bioestadística (1964)</title>
<meta name="description" content="Presentación de clase del cuaderno. Modo clase magistral, modo Colab o sesión completa. Fernando Borrás Rocher, UMH. CC BY 4.0.">
<link rel="stylesheet" href="lib/katex.min.css">
<link rel="stylesheet" href="lib/hljs-github.min.css">
<style>
:root{--tinta:#0F2237;--suave:#5D7691;--acento:#C8461F;--naranja:#E4572E;--fondo:#F4F6FA;--borde:#D9E2EC;--mag:#1F5E99;--lab:#1E7A4C}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--tinta);background:var(--fondo);overflow:hidden}
a{color:var(--acento)}
.barra{position:fixed;top:0;left:0;right:0;height:52px;display:flex;align-items:center;gap:10px;padding:0 14px;background:#0F2237;color:#fff;z-index:5}
.barra .logo{font-family:Georgia,serif;font-weight:800;font-size:19px;color:#fff;text-decoration:none;white-space:nowrap}
.barra .logo em{font-style:normal;color:var(--naranja)}
.barra .tt{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#C9D6E3;font-size:14px}
.modos{display:flex;border:1px solid #33475B;border-radius:10px;overflow:hidden}
.modos button,.barra .ico{background:transparent;color:#fff;border:0;padding:8px 11px;font:inherit;font-size:14px;cursor:pointer;min-height:38px}
.modos button[aria-pressed=true]{background:var(--naranja)}
.barra .ico{border:1px solid #33475B;border-radius:10px}
button:focus-visible,a:focus-visible{outline:3px solid #F2A900;outline-offset:2px}
.progreso{position:fixed;top:52px;left:0;height:4px;background:var(--naranja);transition:width .25s;z-index:5}
.deck{position:fixed;top:56px;bottom:46px;left:0;right:0}
.slide{display:none;position:absolute;inset:0;overflow:auto;padding:28px max(4vw,22px) 24px}
.slide.on{display:block;animation:ent .25s ease}
@keyframes ent{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.slide.on{animation:none}.progreso{transition:none}}
.slide .in{max-width:1180px;margin:0 auto;font-size:clamp(17px,1.55vw,23px);line-height:1.5}
.slide.denso .in{font-size:clamp(15px,1.25vw,19px)}
.slide h1{font-size:clamp(30px,3.8vw,52px);line-height:1.12;margin:.2em 0 .3em}
.slide h1 .num{display:block;font-size:.45em;color:var(--acento);letter-spacing:.04em;margin-bottom:.3em}
.slide h2{font-size:clamp(24px,2.6vw,36px);margin:0 0 .4em;border-left:7px solid var(--naranja);padding-left:14px;line-height:1.2}
.slide h3{font-size:1.15em;color:var(--mag);margin:.2em 0 .5em}
.slide.portada .in{display:flex;flex-direction:column;justify-content:center;min-height:100%}
.eyebrow,.autor,.help{color:var(--suave)}
.help{font-size:.85em}
.mod{font-weight:700;color:var(--mag);font-size:1.1em;margin:0}
.lema{font-size:1.45em;font-weight:700;color:#1F3B57;margin:.1em 0 .5em;line-height:1.25}
figure{margin:.4em 0 .8em;text-align:center}
figure img{max-width:100%;max-height:48vh;height:auto;border-radius:8px;background:#fff}
.puntos li{margin:.25em 0}
.pregunta{background:#FFF4E5;border-left:6px solid #C98200;padding:.6em 1em;border-radius:8px;color:#7A4306}
.colab-cta{background:#E8F5EE;border-left:6px solid var(--lab);padding:.5em 1em;border-radius:8px}
pre.code{background:#fff;border:1px solid var(--borde);border-radius:10px;padding:12px 14px;overflow:auto;font-size:.78em;line-height:1.45}
pre.code code{font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;background:none;padding:0}
pre:not(.code){background:#fff;border:1px solid var(--borde);border-radius:10px;padding:10px;overflow:auto;font-size:.75em}
code{background:#EAF1F8;border-radius:4px;padding:0 4px;font-size:.9em}
table{border-collapse:collapse;margin:.5em 0;font-size:.9em;background:#fff}
th,td{border:1px solid var(--borde);padding:6px 10px;text-align:left;vertical-align:top}
th{background:#EAF1F8}
.dos{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:.6em 0}
.ses{background:#fff;border:1px solid var(--borde);border-radius:14px;padding:12px 18px}
.ses.mag{border-top:6px solid var(--mag)}.ses.lab{border-top:6px solid var(--lab)}
.ses h3{margin:.2em 0}.ses.lab h3{color:var(--lab)}
.min{color:var(--suave);font-size:.85em}
.acc{display:flex;gap:10px;flex-wrap:wrap;margin:1em 0}
.btn{display:inline-block;padding:11px 16px;border-radius:10px;background:var(--acento);color:#fff;text-decoration:none;font-weight:600;font-size:.8em}
.btn.ghost{background:#fff;color:var(--acento);border:1px solid var(--borde)}
[class^=tag-]{position:sticky;top:-14px;float:right;font-size:13px;font-weight:700;padding:4px 10px;border-radius:999px;color:#fff;z-index:1}
.tag-magistral{background:var(--mag)}.tag-colab{background:var(--lab)}
.quiz{background:#fff;border:1px solid var(--borde);border-radius:14px;padding:12px 18px;margin:.6em 0}
.qq{font-weight:600;margin:.2em 0 .5em}
.ops{display:grid;gap:8px}
.op{text-align:left;font:inherit;font-size:.9em;padding:10px 14px;border:1px solid var(--borde);border-radius:10px;background:#F8FAFC;cursor:pointer;min-height:44px}
.op:hover{border-color:var(--mag)}
.op.bien{background:#E3F4EA;border-color:var(--lab)}.op.mal{background:#FCE8E4;border-color:var(--acento)}
.fb{margin:.5em 0 0;font-size:.9em}
.notas{max-width:1180px;margin:18px auto 0;background:#FFFBEA;border:1px dashed #C98200;border-radius:12px;padding:10px 18px;font-size:16px;line-height:1.5}
.notas h4{margin:.2em 0;color:#7A4306}
.pie{position:fixed;bottom:0;left:0;right:0;height:46px;display:flex;align-items:center;justify-content:space-between;padding:0 14px;background:#fff;border-top:1px solid var(--borde);font-size:14px;color:var(--suave);z-index:5}
.pie button{font:inherit;padding:7px 14px;border:1px solid var(--borde);border-radius:9px;background:#fff;cursor:pointer;min-height:36px}
#indice{position:fixed;inset:56px 0 46px 0;background:rgba(15,34,55,.96);color:#fff;overflow:auto;padding:24px;z-index:6}
#indice ol{max-width:900px;margin:0 auto;columns:2;gap:30px}
#indice li{margin:4px 0;break-inside:avoid}
#indice a{color:#fff}
#indice .m{font-size:12px;color:#9FB0C3}
@media (max-width:760px){.dos{grid-template-columns:1fr}.barra .tt,.barra .logo{display:none}.barra{gap:6px;padding:0 8px}.barra .ico{padding:6px 8px;font-size:12px}#indice ol{columns:1}.modos button{padding:6px 5px;font-size:12px}}
@media print{.barra,.pie,.progreso{display:none}body{overflow:visible}.deck{position:static}.slide{display:block!important;position:relative;page-break-after:always;overflow:visible}.notas{display:none}}
</style>
</head>
<body>
<header class="barra">
  <a class="logo" href="../cuadernos.html" title="Todos los cuadernos">Bio<em>estadística</em></a>
  <span class="tt">@@TITULO@@</span>
  <div class="modos" role="group" aria-label="Tipo de sesión">
    <button type="button" data-m="todo" aria-pressed="true">Completa</button>
    <button type="button" data-m="magistral" aria-pressed="false">🎓 Magistral</button>
    <button type="button" data-m="colab" aria-pressed="false">💻 Colab</button>
  </div>
  <button class="ico" type="button" id="bNotas" aria-pressed="false" title="Notas del profesor (N)">Notas</button>
  <button class="ico" type="button" id="bIndice" title="Índice (Esc)">Índice</button>
</header>
<div class="progreso" id="prog"></div>
<main class="deck" id="deck">
@@SLIDES@@
</main>
<div id="indice" hidden><ol id="lista"></ol></div>
<footer class="pie"><button type="button" id="bAnt" aria-label="Diapositiva anterior">← Anterior</button><span id="cont" aria-live="polite"></span><button type="button" id="bSig" aria-label="Diapositiva siguiente">Siguiente →</button></footer>
<script src="lib/katex.min.js"></script>
<script src="lib/auto-render.min.js"></script>
<script src="lib/highlight.min.js"></script>
<script>
const $ = id => document.getElementById(id);
const todas = [...document.querySelectorAll('.slide')];
let modo = 'todo', vis = [], pos = 0, notas = false;
const guarda = (k, v) => { try { localStorage.setItem('bioest-pres-' + k, v); } catch (e) {} };
const lee = k => { try { return localStorage.getItem('bioest-pres-' + k); } catch (e) { return null; } };
function filtra(m, mantener) {
  const actual = vis[pos];
  modo = m;
  vis = todas.filter(s => m === 'todo' || s.dataset.modo === 'ambos' || s.dataset.modo === m);
  document.querySelectorAll('.modos button').forEach(b => b.setAttribute('aria-pressed', b.dataset.m === m));
  const i = mantener && actual ? vis.indexOf(actual) : -1;
  pos = i >= 0 ? i : 0;
  pintaIndice(); muestra();
  guarda('modo', m);
}
function muestra() {
  todas.forEach(s => s.classList.remove('on'));
  const s = vis[pos]; if (!s) return;
  s.classList.add('on'); s.scrollTop = 0;
  s.querySelectorAll('.notas').forEach(n => n.hidden = !notas);
  $('cont').textContent = `${pos + 1} / ${vis.length} · ${s.dataset.bloque}`;
  $('prog').style.width = `${(pos + 1) / vis.length * 100}%`;
  $('bAnt').disabled = pos === 0; $('bSig').disabled = pos === vis.length - 1;
  history.replaceState(null, '', `#${modo}-${pos + 1}`);
}
const ir = d => { pos = Math.max(0, Math.min(vis.length - 1, pos + d)); muestra(); };
function pintaIndice() {
  $('lista').innerHTML = vis.map((s, i) => { const h = s.querySelector('h3, h2, h1'); return `<li><a href="#" data-i="${i}">${(h ? h.textContent : s.dataset.bloque)}</a> <span class="m">${s.dataset.bloque}</span></li>`; }).join('');
}
$('lista').addEventListener('click', e => { const a = e.target.closest('a'); if (!a) return; e.preventDefault(); pos = +a.dataset.i; $('indice').hidden = true; muestra(); });
document.querySelectorAll('.modos button').forEach(b => b.onclick = () => filtra(b.dataset.m, true));
$('bAnt').onclick = () => ir(-1); $('bSig').onclick = () => ir(1);
$('bNotas').onclick = () => { notas = !notas; $('bNotas').setAttribute('aria-pressed', notas); muestra(); };
$('bIndice').onclick = () => { $('indice').hidden = !$('indice').hidden; };
document.addEventListener('keydown', e => {
  if (e.target.closest('input,textarea')) return;
  if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); ir(1); }
  else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); ir(-1); }
  else if (e.key === 'Home') { pos = 0; muestra(); } else if (e.key === 'End') { pos = vis.length - 1; muestra(); }
  else if (e.key === 'n' || e.key === 'N') $('bNotas').click();
  else if (e.key === 'f' || e.key === 'F') { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.(); }
  else if (e.key === 'm' || e.key === 'M') { const ms = ['todo', 'magistral', 'colab']; filtra(ms[(ms.indexOf(modo) + 1) % 3], true); }
  else if (e.key === 'Escape') $('bIndice').click();
});
let x0 = null;
$('deck').addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, {passive: true});
$('deck').addEventListener('touchend', e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 60) ir(dx < 0 ? 1 : -1); x0 = null; });
document.addEventListener('click', e => {
  const b = e.target.closest('.op'); if (!b) return;
  const q = b.closest('.quiz');
  q.querySelectorAll('.op').forEach(o => o.classList.remove('bien', 'mal'));
  const ok = b.dataset.ok === '1';
  b.classList.add(ok ? 'bien' : 'mal');
  q.querySelector('.fb').textContent = (ok ? '✓ ' : '✗ ') + b.dataset.fb;
});
window.addEventListener('load', () => {
  if (window.renderMathInElement) renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}], throwOnError: false});
  if (window.hljs) document.querySelectorAll('pre.code code').forEach(c => hljs.highlightElement(c));
});
const h = location.hash.match(/^#(todo|magistral|colab)-(\d+)$/);
const q = new URLSearchParams(location.search).get('modo');
filtra(h ? h[1] : (['todo', 'magistral', 'colab'].includes(q) ? q : (lee('modo') || 'todo')), false);
if (h) { pos = Math.min(vis.length - 1, +h[2] - 1); muestra(); }
</script>
</body>
</html>
"""


def main():
    os.makedirs(SALIDA, exist_ok=True)
    fs = sorted(glob.glob(os.path.join(AQUI, "..", "cuadernos", "Tema_*.ipynb")))
    todos = [(int(os.path.basename(f)[5:8]),) for f in fs]
    for f in fs:
        n, pagina = construye(f, todos)
        with open(os.path.join(SALIDA, f"tema_{n:03d}.html"), "w", encoding="utf-8") as fh:
            fh.write(pagina)
    print(f"{len(fs)} presentaciones en {os.path.relpath(SALIDA)}")


if __name__ == "__main__":
    main()
