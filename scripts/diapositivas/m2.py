"""Diapositivas del Módulo 2 · Programando con IA (temas 50 a 80)."""
import numpy as np

from .estilo import (AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt)

COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"

DIAPOS = {
    50: [
        dict(ancla="1. Caso clínico", titulo="Rosa: fibrilación auricular, dos cálculos que se repiten cada día", fig="caja",
             ideas=["CHA₂DS₂-VASc orienta la anticoagulación; el aclaramiento de creatinina, la dosis.",
                    "Una <b>función</b> recibe los datos del paciente y devuelve el resultado: se escribe una vez y se usa siempre.",
                    "Una función mal escrita se equivoca con todos los pacientes: hay que probarla."]),
        dict(ancla="2.1 Qué es una función", titulo="Anatomía de una función", fig="anatomia",
             ideas=["<b>def</b>, nombre y parámetros; el cuerpo sangrado; <b>return</b> devuelve el resultado.",
                    "Sin return, la función calcula pero quien la llama recibe None."]),
        dict(ancla="2.3 Casos de prueba", titulo="Los casos de prueba salen de la guía clínica, no del código", fig="pruebas",
             ideas=["Para cada caso: datos de entrada y resultado esperado, calculado a mano.",
                    "Los valores frontera (75 años, 65 años) son los que descubren los errores."]),
    ],
    60: [
        dict(ancla="2. Conceptos clave", titulo="Un gráfico que cambió los hospitales",
             foto=(COMMONS + "Nightingale-mortality.jpg?width=1000",
                   "Florence Nightingale (1858). <i>Diagram of the causes of mortality in the army in the East</i>. "
                   "Dominio público, vía Wikimedia Commons.", 820),
             ideas=["En azul, las muertes por enfermedades evitables; en rojo, por heridas: la mayoría morían de lo primero.",
                    "Con este gráfico Nightingale consiguió reformas sanitarias en los hospitales militares.",
                    "Un buen gráfico clínico se entiende sin explicarlo."], desarrollo=False),
        dict(ancla="2.2 Aleatoriedad y semilla", titulo="Azar reproducible: la semilla", fig="semilla",
             ideas=["El ordenador genera números <b>pseudoaleatorios</b> a partir de una semilla.",
                    "Misma semilla → misma secuencia: la aleatorización se puede auditar y repetir.",
                    "En un ensayo, el azar reparte por igual lo que se ha medido y lo que no."]),
        dict(ancla="2.3 Un buen gráfico clínico", titulo="Lo que no puede faltar en un gráfico clínico", fig="buen_grafico",
             ideas=["Título que diga qué se ve; ejes con <b>unidades</b>; leyenda si hay varias series.",
                    "Referencias clínicas (umbrales) cuando ayudan a interpretar."]),
    ],
    70: [
        dict(ancla="1. Caso clínico", titulo="El CSV que se abrió mal", fig="csv_roto",
             ideas=["Separador «;», coma decimal y tildes en UTF-8: si no se indican al leer, los datos se estropean.",
                    "Los datos viajan en <b>formatos de fichero</b>; conocerlos evita perder información."]),
        dict(ancla="2.2 CSV", titulo="CSV: una tabla escrita como texto", fig="csv",
             ideas=["Una línea por paciente; los campos separados por un carácter.",
                    "La primera línea suele ser la cabecera con los nombres de las variables.",
                    "Un campo vacío es un dato ausente, no un cero."]),
        dict(ancla="2.3 JSON", titulo="JSON: datos anidados, como un resultado de laboratorio HL7 FHIR", fig="json",
             ideas=["Diccionarios dentro de diccionarios, y listas: el formato de las API y de la historia clínica electrónica.",
                    "Para llegar a un dato se sigue el camino de claves: obs[\"valueQuantity\"][\"value\"]."]),
    ],
    80: [
        dict(ancla="1. Caso clínico", titulo="Cinco referencias con DOI… y dos no existen", fig="referencias",
             ideas=["El modelo genera el texto <b>más probable</b>; una referencia plausible lo es, exista o no.",
                    "Todo lo que afirme un modelo de lenguaje se verifica en la fuente."],
             pregunta="¿Cómo comprobaríais en dos minutos si una referencia existe?"),
        dict(ancla="2.1 Cómo genera texto", titulo="Un LLM predice la siguiente palabra", fig="siguiente",
             ideas=["El modelo asigna una probabilidad a cada palabra posible y elige una.",
                    "Repite el proceso palabra a palabra: no consulta una base de datos de hechos."]),
        dict(ancla="2.2 La temperatura", titulo="La temperatura reparte la probabilidad",
             codigo=r'''
import numpy as np
import matplotlib.pyplot as plt

palabras = ["sodio\nhipertónico", "restricción\nhídrica", "tolvaptán", "diuréticos", "esperar"]
logits = np.array([3.0, 2.2, 1.2, 0.6, -0.5])
fig, ejes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
for eje, T in zip(ejes, [0.2, 1.0, 2.0]):
    p = np.exp(logits / T) / np.exp(logits / T).sum()
    eje.bar(range(5), p, color=["firebrick"] + ["steelblue"] * 4)
    eje.set_xticks(range(5), palabras, fontsize=9)
    eje.set_title(f"Temperatura = {T}", fontweight="bold")
ejes[0].set_ylabel("Probabilidad de la siguiente palabra")
plt.suptitle("«El tratamiento de la hiponatremia grave sintomática es…»", fontsize=13)
plt.tight_layout()
plt.show()
''',
             ideas=["Temperatura baja: casi siempre la palabra más probable (respuestas estables).",
                    "Temperatura alta: más variedad y más riesgo de incoherencias.",
                    "Ninguna temperatura garantiza que la respuesta sea verdadera."]),
        dict(ancla="2.4 Qué es una API", titulo="Una API: tu código habla con el modelo", fig="api",
             ideas=["Tu programa envía una petición (prompt + clave) y recibe la respuesta en JSON.",
                    "Cada llamada cuesta dinero o cuota, y lo que envías sale de tu ordenador: nunca datos de pacientes."]),
    ],
}


@figura(50, "caja")
def _():
    fig, ax = lienzo(12, 5)
    for i, t in enumerate(["edad = 78", "mujer = True", "hta = True", "diabetes = True", "ictus = False"]):
        ax.text(2, 82 - i * 14, t, fontsize=15, family="monospace", color=TINTA, va="center")
        flecha(ax, 25, 82 - i * 14, 36, 52, color=GRIS)
    caja(ax, 37, 38, 30, 28, "cha2ds2vasc(...)", tam=18, negrita=True, txt=AZUL)
    flecha(ax, 68, 52, 77, 52, color=AZUL)
    ax.text(87, 58, "5 puntos", ha="center", fontsize=20, fontweight="bold", color=ROJO)
    ax.text(87, 44, "→ anticoagular", ha="center", fontsize=15, color=TINTA)
    ax.text(52, 18, "entradas (parámetros)  →  función  →  salida (return)", ha="center", fontsize=15, color=GRIS)
    return fig


@figura(50, "anatomia")
def _():
    fig, ax = lienzo(12, 5)
    codigo = ['def imc(peso, talla):', '    """IMC en kg/m²."""', '    valor = peso / talla ** 2', '    return round(valor, 1)', '', 'imc(68, 1.63)   # → 25.6']
    for i, l in enumerate(codigo):
        ax.text(3, 86 - i * 13, l, fontsize=17, family="monospace", color=TINTA, va="center")
    notas = [(86, "nombre y parámetros"), (73, "documentación"), (60, "cuerpo (sangrado)"), (47, "valor que devuelve"), (21, "llamada con argumentos")]
    for y, t in notas:
        ax.annotate(t, xy=(60, y), xytext=(72, y), fontsize=15, color=AZUL, va="center", arrowprops=dict(arrowstyle="<-", color=AZUL, lw=1.8))
    return fig


@figura(50, "pruebas")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.axis("off")
    filas = [["Mujer 78 a., HTA, DM", "1+2+1+1 = 5", "5", "✓"], ["Varón 74 a., sin factores", "1", "1", "✓"],
             ["Varón 75 a. (frontera)", "2", "1", "✗  ¿> 75 en vez de ≥ 75?"], ["Mujer 64 a., sin factores", "1", "1", "✓"]]
    t = ax.table(cellText=filas, colLabels=["Caso", "Esperado (a mano)", "Obtenido", "¿Coincide?"], loc="center",
                 cellColours=[["white"] * 3 + ["#D5EFDF" if f[3] == "✓" else "#F7D9D5"] for f in filas], colWidths=[0.32, 0.22, 0.13, 0.33])
    t.auto_set_font_size(False); t.set_fontsize(15); t.scale(1, 2.6)
    return fig


@figura(60, "semilla")
def _():
    fig, ax = lienzo(12, 4.5)
    import random
    for i, (s, c) in enumerate([(1964, AZUL), (1964, AZUL), (2027, NARANJA)]):
        random.seed(s)
        brazos = ["A"] * 5 + ["B"] * 5
        random.shuffle(brazos)
        y = 78 - i * 28
        ax.text(2, y, f"random.seed({s})", fontsize=16, family="monospace", color=c, va="center")
        for k, b in enumerate(brazos):
            caja(ax, 30 + k * 5.5, y - 5, 3.8, 10, b, color=c, relleno="white" if b == "A" else AZUL_CLARO, tam=15, negrita=True)
    ax.text(99, 64, "misma\nsecuencia", ha="right", fontsize=15, color=AZUL, va="center")
    ax.text(99, 22, "otra\nsecuencia", ha="right", fontsize=15, color=NARANJA, va="center")
    return fig


@figura(60, "buen_grafico")
def _():
    fig, ax = plt.subplots(figsize=(12, 5))
    h = np.arange(0, 60, 6)
    tmp = [37.2, 38.4, 39.1, 38.8, 38.0, 37.6, 37.4, 37.0, 36.9, 36.8]
    ax.plot(h, tmp, "o-", color=AZUL, lw=2.5, ms=8, label="Temperatura axilar")
    ax.axhline(38, color=ROJO, ls="--", label="Fiebre (≥ 38 °C)")
    ax.axvline(12, color=GRIS, ls=":", lw=2)
    ax.text(12.8, 36.85, "inicio del antibiótico", color=GRIS, fontsize=13)
    ax.set_title("Curva de temperatura del paciente P-0457")
    ax.set_xlabel("Horas desde el ingreso")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend(loc="upper right")
    for txt, xy, xyt in [("unidades", (-2, 38.0), (4, 36.75)), ("umbral clínico", (50, 38), (44, 38.45))]:
        ax.annotate(txt, xy=xy, xytext=xyt, fontsize=14, color=VERDE, fontweight="bold", arrowprops=dict(arrowstyle="->", color=VERDE, lw=2), annotation_clip=False)
    return fig


@figura(70, "csv_roto")
def _():
    fig, ax = lienzo(12, 4.8)
    ax.text(2, 90, "Fichero (texto)", fontsize=16, fontweight="bold", color=TINTA)
    for i, l in enumerate(["id;edad;peso;dx", "IC-001;72;81,5;Insuficiencia cardíaca", "IC-002;65;77,2;Miocardiopatía"]):
        ax.text(2, 74 - i * 12, l, fontsize=12.5, family="monospace", color=TINTA)
    flecha(ax, 50, 52, 57, 52, color=ROJO)
    ax.text(53.5, 40, "abierto sin\nindicar «;»", ha="center", fontsize=12, color=ROJO)
    ax.text(58, 90, "Hoja de cálculo", fontsize=16, fontweight="bold", color=TINTA)
    for i, l in enumerate(["id;edad;peso;dx", "IC-001;72;81,5;Insuficiencia cardÃ­aca", "IC-002;65;77,2;MiocardiopatÃ­a"]):
        ax.add_patch(plt.Rectangle((58, 70 - i * 12), 41, 10, fc="#FBE5E1" if i else "#EEE", ec=GRIS))
        ax.text(59, 75 - i * 12, l, fontsize=11, family="monospace", color=ROJO, va="center")
    ax.text(78, 26, "todo en una columna · tildes rotas", ha="center", fontsize=14, color=ROJO)
    ax.text(50, 8, 'pd.read_csv("registro.csv", sep=";", decimal=",", encoding="utf-8")', ha="center", fontsize=14, family="monospace", color=VERDE)
    return fig


@figura(70, "csv")
def _():
    fig, ax = lienzo(12, 4.5)
    lineas = [["id", "edad", "peso", "fevi"], ["IC-001", "72", "81,5", "35"], ["IC-002", "65", "77,2", ""]]
    for i, f in enumerate(lineas):
        texto = ";".join(f)
        ax.text(3, 80 - i * 22, texto, fontsize=19, family="monospace", color=AZUL if i == 0 else TINTA, fontweight="bold" if i == 0 else "normal")
        ax.text(3, 80 - i * 22, "".join(c if c == ";" else " " for c in texto), fontsize=19, family="monospace", color=ROJO, fontweight="bold")
    ax.text(62, 80, "← cabecera", fontsize=15, color=AZUL)
    ax.text(62, 58, "← un paciente por línea", fontsize=15, color=TINTA)
    ax.text(62, 36, "← fevi vacía = dato ausente", fontsize=15, color=ROJO)
    ax.text(3, 10, "«;» separa los campos · «,» es la coma decimal", fontsize=15, color=ROJO)
    return fig


@figura(70, "json")
def _():
    fig, ax = lienzo(12, 5.5)
    lineas = [('{', 0), ('"resourceType": "Observation",', 1), ('"code": {"coding": [', 1), ('{"system": "http://loinc.org", "code": "2339-0",', 2),
              ('"display": "Glucose [Mass/volume] in Blood"}', 3), (']},', 1), ('"effectiveDateTime": "2027-03-14T08:30:00+01:00",', 1),
              ('"valueQuantity": {"value": 182, "unit": "mg/dL"}', 1), ('}', 0)]
    for i, (l, n) in enumerate(lineas):
        ax.text(2 + n * 3, 92 - i * 10, l, fontsize=13.5, family="monospace", color=TINTA, va="center")
    ax.text(74, 63, 'obs["code"]["coding"][0]["code"]\n→ "2339-0"', fontsize=13, family="monospace", color=AZUL, va="center")
    ax.text(74, 22, 'obs["valueQuantity"]["value"]\n→ 182', fontsize=13, family="monospace", color=VERDE, va="center")
    return fig


@figura(80, "referencias")
def _():
    fig, ax = lienzo(12, 4.8)
    refs = [("Referencia 1: autores, revista y DOI correctos", "✓ existe y lo respalda", VERDE),
            ("Referencia 2: autores, revista y DOI correctos", "✓ existe y lo respalda", VERDE),
            ("Referencia 3: autores reales, revista real, DOI inventado", "✗ no existe", ROJO),
            ("Referencia 4: título verosímil, DOI de otro artículo", "✗ no existe", ROJO),
            ("Referencia 5: artículo real", "⚠ existe, pero no dice eso", NARANJA)]
    for i, (r, e, c) in enumerate(refs):
        ax.text(2, 86 - i * 17, r, fontsize=14, color=TINTA, va="center")
        ax.text(98, 86 - i * 17, e, fontsize=15, color=c, va="center", ha="right", fontweight="bold")
    return fig


@figura(80, "siguiente")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    p = [0.46, 0.25, 0.12, 0.08, 0.05, 0.04]
    w = ["hipertónico", "restricción", "tolvaptán", "diuréticos", "corregir", "esperar"]
    ax.barh(range(6)[::-1], p, color=[ROJO] + [AZUL] * 5)
    ax.set_yticks(range(6)[::-1], w)
    for i, v in enumerate(p):
        ax.text(v + 0.01, 5 - i, f"{v:.0%}", va="center", fontsize=14)
    ax.set_xlabel("Probabilidad asignada por el modelo")
    ax.set_title("«El tratamiento de la hiponatremia grave sintomática es suero salino…»", fontsize=15)
    ax.set_xlim(0, 0.55)
    return fig


@figura(80, "api")
def _():
    fig, ax = lienzo(12, 4.6)
    caja(ax, 3, 35, 24, 30, "Tu cuaderno\n(Colab)", tam=17, negrita=True)
    caja(ax, 72, 35, 25, 30, "Servidor del\nmodelo (Gemini,\nOpenAI…)", tam=16, negrita=True, color=NARANJA, relleno="#FDEFD9")
    flecha(ax, 28, 60, 71, 60, color=AZUL, texto="petición: prompt + clave (de Secretos)", tam=14)
    flecha(ax, 71, 40, 28, 40, color=VERDE, texto="respuesta en JSON", tam=14)
    ax.text(50, 14, "Lo que envías sale de tu ordenador: nunca datos de pacientes", ha="center", fontsize=15, color=ROJO, fontweight="bold")
    return fig
