"""Diapositivas del Módulo 1 · Descubriendo Python (temas 10 a 40)."""
import numpy as np

from .estilo import (AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt, titulo)

DIAPOS = {
    10: [
        dict(ancla="1. Caso clínico", titulo="De Carmen a 3.000 pacientes", fig="escala",
             ideas=["Con <b>una</b> paciente decide el juicio clínico: 148/92 mmHg es hipertensión.",
                    "Con <b>3.000</b> pacientes las preguntas son otras: ¿qué proporción está controlada? ¿funciona el programa?",
                    "Responderlas exige datos, estadística y, hoy, código."],
             pregunta="¿Cómo sabríais si el control de la hipertensión de vuestro centro ha mejorado este año?"),
        dict(ancla="2.2 Población, muestra", titulo="Población y muestra, parámetro y estadístico", fig="poblacion",
             ideas=["La <b>población</b> es todo el grupo que interesa; casi nunca se puede medir entero.",
                    "La <b>muestra</b> es la parte que se mide: de ella sale un <b>estadístico</b> (x̄, p̂).",
                    "La inferencia usa el estadístico para estimar el <b>parámetro</b> (μ, p) de la población."]),
        dict(ancla="2.3 Tipos de variables", titulo="Qué tipo de variable es cada dato", fig="variables",
             ideas=["El tipo de variable decide cómo se resume, cómo se representa y qué prueba se usa.",
                    "Ordinal no es cuantitativa: entre NYHA II y III no hay «una unidad»."]),
        dict(ancla="2.5 Inteligencia artificial", titulo="Tres normas para trabajar con IA", fig="normas_ia",
             ideas=["La IA es una herramienta de trabajo diaria en esta asignatura.",
                    "Estas tres normas se aplican en todos los temas y en los exámenes con Colab."]),
    ],
    20: [
        dict(ancla="1. Caso clínico", titulo="Cada dato tiene su tipo", fig="caso",
             ideas=["Lo que para nosotros es «el peso», para Python puede ser un número o un texto.",
                    "Antes de calcular hay que dar a cada dato su tipo: número, texto, lista… o <b>ausente</b>."]),
        dict(ancla="2.2 Estructuras de datos", titulo="Cuatro formas de agrupar datos", fig="estructuras",
             ideas=["<b>Lista</b>: serie ordenada que cambia (glucemias). <b>Tupla</b>: valores fijos que van juntos (PAS/PAD).",
                    "<b>Diccionario</b>: ficha con campos (edad, sexo…). <b>Conjunto</b>: valores únicos (diagnósticos)."]),
        dict(ancla="3.7 Una cohorte", titulo="Una cohorte es una lista de fichas", fig="cohorte",
             ideas=["Cada paciente es un diccionario; la cohorte, una lista de diccionarios.",
                    "Es exactamente la estructura de una tabla: filas = pacientes, columnas = variables (Tema 100)."]),
    ],
    30: [
        dict(ancla="1. Caso clínico", titulo="Antonio en Urgencias: la escala qSOFA", fig="qsofa",
             ideas=["Cada criterio es una pregunta de sí o no: una <b>comparación</b>.",
                    "La puntuación decide la conducta: es una <b>estructura condicional</b>.",
                    "Escrita en Python, la regla se aplica igual a 1 o a 10.000 pacientes."]),
        dict(ancla="2.2 Operadores lógicos", titulo="and, or, not", fig="logicos",
             ideas=["<b>and</b>: hacen falta las dos condiciones. <b>or</b>: basta con una.",
                    "La hipertensión es «PAS ≥ 140 <b>or</b> PAD ≥ 90»: con and se perderían pacientes."]),
        dict(ancla="2.3 Estructuras condicionales", titulo="if, elif, else: el primer criterio que se cumple gana", fig="imc",
             ideas=["Las categorías se comprueban en orden: solo se ejecuta una rama.",
                    "Los errores típicos están en las fronteras: ¿un IMC de 25 es normal o sobrepeso?"],
             pregunta="¿Qué categoría daría vuestro código a un IMC de exactamente 30?"),
    ],
    40: [
        dict(ancla="1. Caso clínico", titulo="Ocho pacientes, 40 glucemias: ¿quién ha tenido hipoglucemia?",
             codigo=r'''
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(40)
plt.figure(figsize=(10, 4.5))
for p in range(8):
    g = rng.normal(140, 45, rng.integers(4, 7)).clip(45, 300)
    plt.scatter([p + 1] * len(g), g, s=90, c=["firebrick" if x < 70 else "steelblue" for x in g], zorder=3)
plt.axhline(70, color="firebrick", linestyle="--", label="Hipoglucemia: < 70 mg/dL")
plt.xticks(range(1, 9), [f"P{p}" for p in range(1, 9)])
plt.xlabel("Paciente")
plt.ylabel("Glucemia capilar (mg/dL)")
plt.title("Glucemias de las últimas 24 horas", fontweight="bold")
plt.legend()
plt.show()
''',
             ideas=["Revisar a mano cada valor es lento y propenso a errores, y mañana habrá que repetirlo.",
                    "La instrucción es siempre la misma: <b>para cada</b> paciente y <b>para cada</b> glucemia, comprueba si es < 70."]),
        dict(ancla="2.1 El bucle for", titulo="El bucle for recorre la serie elemento a elemento", fig="for",
             ideas=["En cada vuelta, la variable toma el siguiente valor de la lista.",
                    "El cuerpo del bucle (sangrado) se repite tantas veces como elementos haya."]),
        dict(ancla="2.3 El bucle while", titulo="while: repetir mientras se cumpla una condición",
             codigo=r'''
import matplotlib.pyplot as plt

concentracion, umbral, horas, t = 16.0, 1.0, [0], [16.0]
while concentracion >= umbral:          # se repite mientras quede fármaco por encima del umbral
    concentracion = concentracion / 2   # una semivida
    horas.append(horas[-1] + 6)
    t.append(concentracion)
plt.figure(figsize=(10, 4.5))
plt.plot(horas, t, "o-", color="steelblue", linewidth=2.5, markersize=9)
plt.axhline(umbral, color="firebrick", linestyle="--", label="Umbral: el bucle se detiene")
for h, c in zip(horas, t):
    plt.annotate(f"{c:g}", (h, c), textcoords="offset points", xytext=(0, 10), ha="center")
plt.xlabel("Horas (semivida de 6 h)")
plt.ylabel("Concentración (mg/L)")
plt.title(f"El bucle dio {len(horas) - 1} vueltas", fontweight="bold")
plt.legend()
plt.show()
''',
             ideas=["Se usa cuando no se sabe de antemano cuántas vueltas hacen falta.",
                    "Cuidado: si la condición nunca deja de cumplirse, el bucle no termina."]),
        dict(ancla="2.4 Prevalencia", titulo="Prevalencia = casos / total", fig="prevalencia",
             ideas=["Con un contador dentro de un bucle se calcula la primera medida de frecuencia.",
                    "Es una proporción: entre 0 y 1, o entre 0 % y 100 %, y siempre en un momento dado."]),
    ],
}


@figura(10, "escala")
def _():
    fig, ax = lienzo(12, 5)
    caja(ax, 3, 30, 30, 45, "Carmen, 58 años\nPA 148/92 mmHg\nGlucemia 112 mg/dL\n\n→ Juicio clínico", tam=16)
    flecha(ax, 36, 52, 58, 52, color=AZUL, texto="cambio de escala", tam=14)
    xs = [64 + i * 2.8 for i in range(12) for j in range(7)]
    ys = [32 + j * 6 for i in range(12) for j in range(7)]
    ax.scatter(xs, ys, s=70, c=[AZUL if (i + j) % 3 else ROJO for i in range(12) for j in range(7)])
    ax.text(80, 22, "3.000 personas con hipertensión", ha="center", fontsize=16, color=TINTA, fontweight="bold")
    ax.text(80, 12, "¿Qué proporción está controlada? ¿Mejora el programa?", ha="center", fontsize=14, color=TINTA)
    ax.text(80, 4, "→ Bioestadística", ha="center", fontsize=16, color=AZUL, fontweight="bold")
    return fig


@figura(10, "poblacion")
def _():
    fig, ax = lienzo(12, 5.5)
    rng = np.random.default_rng(1)
    ax.add_patch(plt.Circle((25, 50), 23, color=AZUL_CLARO, ec=AZUL, lw=2))
    xy = rng.uniform(-1, 1, (400, 2))
    xy = xy[(xy ** 2).sum(1) < 0.9][:220]
    mues = rng.choice(len(xy), 25, replace=False)
    ax.scatter(25 + 21 * xy[:, 0], 50 + 21 * xy[:, 1], s=12, color=GRIS)
    ax.scatter(25 + 21 * xy[mues, 0], 50 + 21 * xy[mues, 1], s=40, color=ROJO)
    ax.text(25, 96, "Población", ha="center", va="top", fontsize=18, fontweight="bold", color=TINTA)
    ax.text(25, 18, "Parámetro: μ, p (desconocido)", ha="center", fontsize=15, color=TINTA)
    ax.add_patch(plt.Circle((78, 50), 13, color="#FBE5E1", ec=ROJO, lw=2))
    ax.scatter(78 + 10 * rng.uniform(-0.7, 0.7, 25), 50 + 10 * rng.uniform(-0.7, 0.7, 25), s=40, color=ROJO)
    ax.text(78, 80, "Muestra", ha="center", fontsize=18, fontweight="bold", color=TINTA)
    ax.text(78, 26, "Estadístico: x̄, p̂ (calculado)", ha="center", fontsize=15, color=TINTA)
    flecha(ax, 49, 62, 64, 58, color=AZUL, texto="muestreo", curva=-0.2)
    flecha(ax, 64, 40, 49, 38, color=ROJO, texto="inferencia", curva=-0.2)
    return fig


@figura(10, "variables")
def _():
    fig, ax = lienzo(12, 5.5)
    caja(ax, 40, 82, 20, 10, "Variable", negrita=True, tam=17)
    caja(ax, 12, 55, 26, 10, "Cualitativa (categorías)", tam=15)
    caja(ax, 62, 55, 26, 10, "Cuantitativa (números)", tam=15)
    for x, t, e in [(2, "Nominal", "grupo sanguíneo,\nsexo"), (27, "Ordinal", "NYHA I-IV,\nestadio tumoral"),
                    (52, "Discreta", "nº de ingresos,\nnº de hijos"), (77, "Continua", "PAS, peso,\ncolesterol")]:
        caja(ax, x, 26, 20, 10, t, tam=15, negrita=True, relleno="white")
        ax.text(x + 10, 13, e, ha="center", va="center", fontsize=14, color=TINTA)
    flecha(ax, 47, 81, 27, 67); flecha(ax, 53, 81, 74, 67)
    flecha(ax, 22, 54, 12, 38); flecha(ax, 28, 54, 37, 38); flecha(ax, 72, 54, 62, 38); flecha(ax, 78, 54, 87, 38)
    return fig


@figura(10, "normas_ia")
def _():
    fig, ax = lienzo(12, 4.2)
    for i, (t, d, c) in enumerate([("1. Nunca datos de pacientes", "Ni con el nombre quitado:\nsolo datos sintéticos", ROJO),
                                    ("2. La clave, en Secretos", "Nunca escrita en el código\nni en un chat", NARANJA),
                                    ("3. Verifica todo", "Comprueba con un caso que\nsepas calcular a mano", VERDE)]):
        caja(ax, 2 + i * 33.5, 20, 30, 62, f"{t}\n\n{d}", color=c, relleno="white", tam=13.5)
    return fig


@figura(20, "caso")
def _():
    fig, ax = lienzo(12, 5.5)
    filas = [("Edad: 72", "int  (número entero)", AZUL), ('Peso: "81,5"', "str  (texto con coma: no se puede sumar)", NARANJA),
             ('Dx: "  Insuf. cardiaca DESCOMPENSADA "', "str  (sobran espacios y mayúsculas)", NARANJA),
             ("Glucemias: 182, 165, 210, 148, 139", "list  (serie de valores)", VERDE), ("Fracción de eyección: —", "None  (dato ausente)", ROJO)]
    for i, (a, b, c) in enumerate(filas):
        y = 82 - i * 17
        ax.text(2, y, a, fontsize=14, family="monospace", color=TINTA, va="center")
        ax.text(98, y, b, fontsize=15, color=c, va="center", ha="right", fontweight="bold")
    return fig


@figura(20, "estructuras")
def _():
    fig, ax = lienzo(12, 5.5)
    datos = [("Lista  [ ]", "glucemias = [182, 165, 210]", "ordenada · se puede cambiar"),
             ("Tupla  ( )", "pa = (148, 92)", "ordenada · fija"),
             ("Diccionario  { : }", 'ficha = {"edad": 72, "sexo": "H"}', "acceso por clave"),
             ("Conjunto  { }", 'dx = {"HTA", "DM2"}', "sin repetidos · sin orden")]
    for i, (n, e, p) in enumerate(datos):
        x, y = (2 + (i % 2) * 50, 52 - (i // 2) * 46)
        caja(ax, x, y, 45, 38, "", relleno="white")
        ax.text(x + 22.5, y + 30, n, ha="center", fontsize=17, fontweight="bold", color=AZUL)
        ax.text(x + 22.5, y + 18, e, ha="center", fontsize=13.5, family="monospace", color=TINTA)
        ax.text(x + 22.5, y + 6, p, ha="center", fontsize=14, color=GRIS)
    return fig


@figura(20, "cohorte")
def _():
    fig, ax = lienzo(12, 5)
    filas = [("P-01", 72, "H", 148), ("P-02", 65, "M", 132), ("P-03", 80, "M", 155)]
    ax.text(22, 92, "Tabla", ha="center", fontsize=17, fontweight="bold", color=TINTA)
    for j, h in enumerate(["id", "edad", "sexo", "pas"]):
        ax.text(5 + j * 11, 80, h, fontsize=15, fontweight="bold", color=AZUL, ha="center")
    for i, f in enumerate(filas):
        for j, v in enumerate(f):
            ax.text(5 + j * 11, 66 - i * 14, str(v), fontsize=15, ha="center", color=TINTA)
    flecha(ax, 47, 55, 55, 55, color=AZUL)
    ax.text(77, 92, "Lista de diccionarios", ha="center", fontsize=17, fontweight="bold", color=TINTA)
    for i, f in enumerate(filas):
        ax.text(55, 76 - i * 14, f'  {{"id": "{f[0]}", "edad": {f[1]},\n   "sexo": "{f[2]}", "pas": {f[3]}}},', fontsize=11.5, family="monospace", color=TINTA, va="center")
    ax.text(55, 86, "cohorte = [", fontsize=11.5, family="monospace", color=TINTA)
    ax.text(55, 27, "]", fontsize=11.5, family="monospace", color=TINTA)
    ax.text(50, 12, "fila = paciente = diccionario  ·  columna = variable = clave", ha="center", fontsize=15, color=AZUL)
    return fig


@figura(30, "qsofa")
def _():
    fig, ax = lienzo(12, 5.5)
    crit = [("FR ≥ 22 rpm?", "24 → sí"), ("PAS ≤ 100 mmHg?", "96 → sí"), ("¿Estado mental alterado?", "Glasgow 14 → sí")]
    for i, (c, a) in enumerate(crit):
        caja(ax, 2, 72 - i * 28, 34, 16, c, tam=15)
        ax.text(40, 80 - i * 28, a, fontsize=15, color=VERDE, va="center", fontweight="bold")
        flecha(ax, 61, 80 - i * 28, 66, 52)
    caja(ax, 67, 42, 14, 20, "Suma\n3 puntos", tam=16, negrita=True)
    flecha(ax, 82, 52, 88, 52, color=ROJO)
    ax.text(94, 52, "≥ 2:\nalto\nriesgo", ha="center", va="center", fontsize=16, color=ROJO, fontweight="bold")
    return fig


@figura(30, "logicos")
def _():
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (op, f) in zip(axs, [("A and B", lambda a, b: a and b), ("A or B", lambda a, b: a or b), ("not A", None)]):
        ax.axis("off")
        ax.set_title(op, fontsize=19)
        if f:
            vals = [(a, b, f(a, b)) for a in (True, False) for b in (True, False)]
            ax.table(cellText=[[str(a), str(b), str(r)] for a, b, r in vals], colLabels=["A", "B", op], loc="center",
                     cellColours=[["white", "white", "#D5EFDF" if r else "#F7D9D5"] for *_, r in vals]).scale(1, 2.4)
        else:
            ax.table(cellText=[["True", "False"], ["False", "True"]], colLabels=["A", "not A"], loc="center",
                     cellColours=[["white", "#F7D9D5"], ["white", "#D5EFDF"]]).scale(1, 2.4)
    for ax in axs:
        for t in ax.tables:
            t.set_fontsize(15)
    return fig


@figura(30, "imc")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    bandas = [(15, 18.5, "Bajo peso", "#9DC3E6"), (18.5, 25, "Normal", "#A9D18E"), (25, 30, "Sobrepeso", "#FFD966"), (30, 40, "Obesidad", "#F4B183")]
    for a, b, t, c in bandas:
        ax.axvspan(a, b, color=c)
        ax.text((a + b) / 2, 0.6, t, ha="center", fontsize=17, fontweight="bold", color=TINTA)
    for x in (18.5, 25, 30):
        ax.axvline(x, color=TINTA, lw=2)
        ax.text(x, 0.12, f"{x:g}", ha="center", fontsize=15, color=TINTA, bbox=dict(fc="white", ec="none"))
    ax.annotate("IMC = 25 → sobrepeso\n(el límite va a la\ncategoría superior)", xy=(25, 0.3), xytext=(31, 0.2),
                fontsize=14, arrowprops=dict(arrowstyle="->", lw=2), color=ROJO)
    ax.set_xlim(15, 40); ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xlabel("IMC (kg/m²)")
    ax.spines["left"].set_visible(False)
    return fig


@figura(40, "for")
def _():
    fig, ax = lienzo(12, 4.5)
    vals = [182, 65, 210, 148, 58]
    for i, v in enumerate(vals):
        caja(ax, 6 + i * 13, 55, 10, 18, str(v), color=ROJO if v < 70 else AZUL, relleno="#F7D9D5" if v < 70 else AZUL_CLARO, tam=18, negrita=True)
        ax.text(11 + i * 13, 82, f"vuelta {i + 1}", ha="center", fontsize=13, color=GRIS)
    flecha(ax, 8, 46, 68, 46, color=GRIS, texto=None)
    ax.text(38, 38, "el bucle recorre la lista de izquierda a derecha", ha="center", fontsize=13, color=GRIS)
    ax.text(73, 70, "for g in glucemias:\n    if g < 70:\n        hipos += 1", fontsize=16, family="monospace", color=TINTA, va="center")
    ax.text(73, 30, "Resultado: hipos = 2", fontsize=17, color=ROJO, fontweight="bold")
    return fig


@figura(40, "prevalencia")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.8))
    rng = np.random.default_rng(4)
    casos = set(rng.choice(100, 32, replace=False))
    for k in range(100):
        ax.add_patch(plt.Circle((k % 20, 4 - k // 20), 0.38, color=ROJO if k in casos else AZUL_CLARO, ec=AZUL if k not in casos else ROJO))
    ax.set_xlim(-1, 32); ax.set_ylim(-1, 5); ax.set_aspect("equal"); ax.axis("off")
    ax.text(21, 3.8, "32 casos", fontsize=19, color=ROJO, fontweight="bold")
    ax.text(21, 2.8, "100 pacientes", fontsize=19, color=AZUL, fontweight="bold")
    ax.text(21, 0.6, "Prevalencia = 32 / 100\n= 0,32 = 32 %", fontsize=18, color=TINTA)
    return fig
