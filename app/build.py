"""Monta ../index.html (app Bioestadística) a partir del motor de PyMedIA y de las misiones de src/.

Uso: python3 build.py
El motor (Python en el navegador, corrección por recálculo, informes, profesorado) es el de PyMedIA 1.0.1,
copiado en base/. Aquí solo se cambian la marca, los temas y las misiones, y se añaden los niveles de ayuda
y los campos «primer intento» y «tras la pista» del informe.
"""
import glob
import json
import os
import re

import nbformat

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "base", "pymedia_1.0.1.html")
CUADERNOS = os.path.join(AQUI, "..", "cuadernos")
SALIDA = os.path.join(AQUI, "..", "index.html")
VERSION = "0.1.0"


def sustituye(html, viejo, nuevo, n=1):
    veces = html.count(viejo)
    assert veces == n, f"Se esperaban {n} apariciones y hay {veces}: {viejo[:90]!r}"
    return html.replace(viejo, nuevo)


def entre(html, ini, fin, nuevo):
    a = html.index(ini)
    b = html.index(fin, a)
    return html[:a] + nuevo + html[b:]


def temas_js():
    filas = []
    for f in sorted(glob.glob(os.path.join(CUADERNOS, "Tema_*.ipynb"))):
        n = int(os.path.basename(f)[5:8])
        if n == 0:
            continue
        nb = nbformat.read(f, 4)
        titulo = re.search(r"Tema (\d+)\. (.+?)</font>", nb.cells[0].source).group(2)
        modulo = 1 if n <= 40 else 2 if n <= 80 else 3 if n <= 130 else 4 if n <= 190 else 5
        filas.append(f"  {{n: {n}, u: '{modulo}', t: L({json.dumps(titulo, ensure_ascii=False)}), "
                     f"cuaderno: colabGH({json.dumps(os.path.basename(f))}), video: ''}}")
    assert len(filas) == 30, len(filas)
    return "const TEMAS = [\n" + ",\n".join(filas) + "\n];"


def misiones_js():
    partes = []
    for f in sorted(glob.glob(os.path.join(AQUI, "src", "*.js"))):
        partes.append(open(f, encoding="utf-8").read())
    js = "\n".join(partes)
    return js.replace("/*@@TEMAS@@*/", temas_js())


PINTA_AYUDA = r"""function pintaAyuda(m, p) {
  const ps = m.pistas || [];
  if (m.ayuda === 'ninguna') { $('mAyuda').innerHTML = `<h3>${esc(t('Misión básica: sin ayuda'))}</h3><p class="help" style="margin:0">${esc(t('Esta misión se resuelve sin pistas ni asistente, como en el examen. Si fallas dos veces, la app te propondrá un refuerzo.'))}</p>`; return; }
  const abiertas = ps.slice(0, p.pistas).map((x, i) => `<div class="pm-diag" style="border-left-color:#C98200;background:#FFF8E6"><b>${esc(t('Pista {0}', i + 1))}</b> · ${esc(txt(x))}</div>`).join('');
  const conIA = m.ayuda === 'ia' && m.k === 'code';
  $('mAyuda').innerHTML = `<h3>${esc(m.ayuda === 'ia' ? t('Misión reto: con asistente') : t('Misión clínica: con pistas'))}</h3>${abiertas}<div class="pm-bar"><button class="btn btn-ghost" id="btnPista" type="button" ${p.pistas >= ps.length ? 'disabled' : ''}>${esc(t('Pista ({0} de {1})', Math.min(p.pistas + 1, ps.length), ps.length))}</button>${conIA ? `<button class="btn btn-ghost" id="btnPistaIA" type="button"><svg class="i"><use href="#i-sparkles"/></svg>${esc(t('Pista del tutor de IA'))}</button>` : ''}</div><p class="help" id="ayudaIA" style="margin:8px 0 0">${esc(conIA ? t('Cada pista reduce las estrellas posibles. La IA es opcional, usa tu clave y nunca recibe la solución.') : t('Cada pista reduce las estrellas posibles.'))}</p>`;
"""


def main():
    html = open(BASE, encoding="utf-8").read()

    # ── marca, portada y pie ──
    html = re.sub(r"<title>.*?</title>", "<title>Bioestadística · Bioestadística con Python e inteligencia artificial para Medicina</title>", html, count=1)
    html = sustituye(html, "<span>PyMed<em>IA</em></span>", "<span>Bio<em>estadística</em></span>")
    html = sustituye(html, 'const APP="pymedia";const APP_NAME="PyMedIA";const LOGO_ICON="cpu";const LANGS_ON=["es", "en", "pt"];',
                     'const APP="bioestadistica";const APP_NAME="Bioestadística";const LOGO_ICON="cpu";const LANGS_ON=["es"];')
    html = re.sub(r'<p class="eyebrow" data-i18n="hero.eyebrow">.*?</p>',
                  '<p class="eyebrow" data-i18n="hero.eyebrow">Bioestadística (1964) · 2.º de Medicina · Universidad Miguel Hernández de Elche</p>', html, count=1)
    html = re.sub(r'<h1 data-i18n="hero.h1">.*?</h1>',
                  '<h1 data-i18n="hero.h1">La práctica de Bioestadística <em>con Python, datos clínicos e inteligencia artificial</em></h1>', html, count=1)
    html = re.sub(r'<p class="lede" data-i18n="hero.lede">.*?</p>',
                  '<p class="lede" data-i18n="hero.lede">Tres misiones por cada uno de los 30 temas: una básica sin ayuda, una clínica con pistas y un reto con asistente de IA. Escribes Python real en tu navegador, el código lo corrige, te explica tus fallos típicos y genera el informe de evaluación continua.</p>', html, count=1)
    html = re.sub(r'<p class="fa-idea">.*?</p>',
                  '<p class="fa-idea">Práctica de los 30 cuadernos de Colab de la asignatura (CC BY 4.0). Motor de corrección basado en PyMedIA, del mismo autor.</p>', html, count=1)
    html = re.sub(r'<p class="sh-lede" data-i18n="s.ruta.lede">.*?</p>',
                  '<p class="sh-lede" data-i18n="s.ruta.lede">Los 30 temas de la asignatura en sus 5 módulos. Cada tema enlaza a su cuaderno de Colab y tiene tres misiones: básica (sin ayuda), clínica (con pistas) y reto (con asistente).</p>', html, count=1)
    html = re.sub(r'<footer class="fa-foot"><hr><p><b>PyMedIA</b>',
                  '<footer class="fa-foot"><hr><p><b>Bioestadística</b>', html, count=1)
    html = sustituye(html, "Cada tema de los cuadernos tiene misiones con casos de consulta, urgencias y planta.",
                     "Cada tema de la asignatura tiene una misión básica, una clínica y un reto.")
    html = sustituye(html, "Son ejercicios para aprender a programar y no sustituyen a las guías clínicas.",
                     "Son ejercicios para aprender bioestadística y no sustituyen a las guías clínicas.")

    # ── Word y ZIP escritos en el propio navegador, sin librerías de internet (módulo 70-report de Forja) ──
    html = entre(html, "/* ── salidas: Word desde Markdown y ZIP", "/* csv con BOM", open(os.path.join(AQUI, "base", "70-report_forja.js"), encoding="utf-8").read() + "\n")

    # ── temas y misiones ──
    html = entre(html, "/* ── mapa de temas del Módulo 1", "/* ══ runner.js", misiones_js() + "\n\n")
    html = sustituye(html, "const VERSION_APP = '1.0.1';", f"const VERSION_APP = '{VERSION}';")

    # ── arnés: tolerancia relativa algo mayor (scipy y pandas pueden diferir en la última cifra) ──
    html = sustituye(html, "if t == 'num': return abs(a['v'] - b['v']) <= 1e-9 * max(1.0, abs(b['v']))",
                     "if t == 'num': return abs(a['v'] - b['v']) <= 1e-6 * max(1.0, abs(b['v']))")

    # ── interfaz ──
    html = sustituye(html, "${esc(t('Unidad {0}', u.u))}", "${esc(t('Módulo {0}', u.u))}")
    html = sustituye(html, """<a href="${videoUrl(x.video)}" target="_blank" rel="noopener">${esc(t('Vídeo'))} ↗</a>""", "")
    html = re.sub(r"const REFUERZO = \{.*?\};", "const REFUERZO = refuerzos();", html, count=1)
    html = re.sub(r"const REF_ERR = \{.*?\};",
                  "const REF_ERR = {SyntaxError: 'm20-2', IndentationError: 'm40-2', NameError: 'm20-2', TypeError: 'm20-2', IndexError: 'm40-2', KeyError: 'm20-2'};", html, count=1)
    html = sustituye(html, "cur: 'm20-1'", "cur: 'm10-2'", n=2)
    html = sustituye(html, "if (!misionPorId(S.cur)) S.cur = 'm20-1';", "if (!misionPorId(S.cur)) S.cur = 'm10-2';")
    html = sustituye(html, "abreMision('m20-1', {ejemplo: true})", "abreMision(EJEMPLO.id, {ejemplo: true})")
    html = re.sub(r"const EJ_CODIGO = .*?;\n", "const EJ_CODIGO = EJEMPLO.code;\n", html, count=1)
    html = re.sub(r"<p>Responde a las cuatro preguntas\.", "<p>Responde a todas las preguntas.", html, count=1)
    html = entre(html, "function pintaAyuda(m, p) {", "  $('btnPista').onclick", PINTA_AYUDA)
    html = sustituye(html, "$('mSub').textContent = t('Tema {0} · {1} · Nivel {2}', m.tema, txt(tm.t), m.nivel);",
                     "$('mSub').textContent = t('Tema {0} · {1} · {2}', m.tema, txt(tm.t), t(NOM_NIVEL[m.nivel]));")

    # ── profesorado: corrección por lotes ──
    html = sustituye(html, '<div class="card" id="profVer"></div>', '<div class="card" id="profLote"></div>\n  <div class="card" id="profVer"></div>')
    html = sustituye(html, "  $('btnExam').onclick = generaExamenes;\n}", "  $('btnExam').onclick = generaExamenes;\n  pintaLote();\n}")

    # ── nombre de los informes: 1964_apellidos_nombre_fecha ──
    html = sustituye(html, """<div class="field"><label for="inAlumno">${esc(t('Nombre o identificador (aparece en el informe)'))}</label><input type="text" id="inAlumno" value="${esc(S.alumno)}" autocomplete="off"></div>""",
                     """<div class="field"><label for="inApe">${esc(t('Apellidos'))}</label><input type="text" id="inApe" value="${esc(partesAlumno().ape)}" autocomplete="family-name"></div><div class="field"><label for="inNom">${esc(t('Nombre'))}</label><input type="text" id="inNom" value="${esc(partesAlumno().nom)}" autocomplete="given-name"><p class="help">${esc(t('Aparecen en el informe y en el nombre del fichero: 1964_apellidos_nombre_fecha.'))}</p></div>""")
    html = sustituye(html, "  $('inAlumno').oninput = () => { S.alumno = $('inAlumno').value; guarda(); };",
                     "  const alNombre = () => { S.apellidos = $('inApe').value.trim(); S.nombre = $('inNom').value.trim(); S.alumno = [S.apellidos, S.nombre].filter(Boolean).join(', '); guarda(); };\n  $('inApe').oninput = alNombre; $('inNom').oninput = alNombre;")
    html = sustituye(html, "$('btnJsonP').onclick = () => dl(`pymedia_${slug(S.alumno || 'informe')}.json`, JSON.stringify(informeJSON(), null, 1), 'application/json');",
                     "$('btnJsonP').onclick = () => { if (exigeNombre()) dl(nombreInforme('json'), JSON.stringify(informeJSON(), null, 1), 'application/json'); };")
    html = sustituye(html, "async function exportaWord() { try { dl(`pymedia_${slug(S.alumno || 'informe')}.docx`,", "async function exportaWord() { if (!exigeNombre()) return; try { dl(nombreInforme('docx'),")
    html = sustituye(html, "function exportaCsv() { dl(`pymedia_${slug(S.alumno || 'informe')}.csv`,", "function exportaCsv() { if (!exigeNombre()) return; dl(nombreInforme('csv'),")
    html = sustituye(html, "alumno: S.alumno, sem: S.sem, puntos: S.puntos,", "alumno: S.alumno, apellidos: partesAlumno().ape, nombre: partesAlumno().nom, sem: S.sem, puntos: S.puntos,")

    # ── informe: primer intento (sin ayudas) y resuelta tras la pista ──
    html = sustituye(html, "  const ej = RUN.ejemplo, p = P(m.id); if (!ej) p.intentos++;\n  const ok = !res.timeout && !res.err && !!res.ok;",
                     "  const ej = RUN.ejemplo, p = P(m.id); if (!ej) p.intentos++;\n  const ok = !res.timeout && !res.err && !!res.ok;\n  if (!ej) marcaPrimero(p, ok);")
    html = sustituye(html, "  p.intentos++; Q.corr = m.quiz.map((q, i) => Q.sel[i] === q.ok);\n  const bien = Q.corr.filter(Boolean).length, todo = bien === m.quiz.length;",
                     "  p.intentos++; Q.corr = m.quiz.map((q, i) => Q.sel[i] === q.ok);\n  const bien = Q.corr.filter(Boolean).length, todo = bien === m.quiz.length;\n  marcaPrimero(p, todo);")
    html = sustituye(html, "t('resultado_visto')], MIS.map(m => { const p = S.prog[m.id] || {}; return [txt(m.t), m.tema, m.nivel,",
                     "t('resultado_visto'), 'id', 'tipo', 'primer_intento', 'tras_pista'], MIS.map(m => { const p = S.prog[m.id] || {}; return [txt(m.t), m.tema, m.nivel,")
    html = sustituye(html, "p.pistas || 0, p.ia || 0, p.totV || 0]; })), 'text/csv;charset=utf-8'); }",
                     "p.pistas || 0, p.ia || 0, p.totV || 0, m.id, NOM_NIVEL[m.nivel], p.prim === undefined ? '' : p.prim ? 1 : 0, p.prim === undefined ? '' : p.done ? 1 : 0]; })), 'text/csv;charset=utf-8'); }")
    html = sustituye(html, "const FMT = 'pymedia-informe';", "const FMT = 'bioestadistica-informe';")
    html = html.replace("no es un informe de PyMedIA", "no es un informe de Bioestadística").replace("No es un informe de PyMedIA", "No es un informe de Bioestadística")
    html = html.replace("'examenes_pymedia.zip'", "'examenes_bioestadistica.zip'")
    html = html.replace("`PyMedIA ${m.id}", "`${APP_NAME} ${m.id}").replace("$course$/top/PyMedIA", "$course$/top/Bioestadistica")
    html = html.replace("· PyMedIA v${VERSION_APP}", "· ${APP_NAME} v${VERSION_APP}")
    html = sustituye(html, "Eres un tutor de programación en Python para estudiantes de Medicina",
                     "Eres un tutor de bioestadística y de Python para estudiantes de 2.º de Medicina")

    restos = [l for l in html.split("\n") if re.search(r"PyMedIA|pymedia", l) and "Motor de corrección basado en PyMedIA" not in l]
    for l in restos:
        print("Aviso, queda una mención:", l.strip()[:120])
    open(SALIDA, "w", encoding="utf-8").write(html)
    print(f"index.html: {len(html) / 1024:.0f} KB · versión {VERSION}")


if __name__ == "__main__":
    main()
