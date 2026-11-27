"""Diapositivas del Módulo 5 · Generalización de conclusiones (temas 200 a 300)."""
import numpy as np

from .estilo import (AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt)

URL_LIMPIA = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv"


def _wilson(x, n, z=1.96):
    p = x / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    s = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - s, c + s


DIAPOS = {
    200: [
        dict(ancla="1. Caso clínico", titulo="74 de 120 hipertensos controlados: ¿cumplimos el objetivo del 65 %?", fig="caso",
             ideas=["61,7 % es una estimación: con otros 120 pacientes saldría otra cifra.",
                    "El IC 95 % (52,7 % a 69,9 %) incluye el objetivo: con 120 pacientes no se puede afirmar ni negar que se cumpla."]),
        dict(ancla="2.4 Qué significa", titulo="El 95 % se refiere al método, no a un intervalo concreto", fig="cien",
             ideas=["Si cada residente calcula su IC 95 %, unos 95 de cada 100 intervalos contienen el valor real.",
                    "Nadie sabe si su intervalo es de los que fallan: por eso se habla de confianza."]),
        dict(ancla="2.5 De qué depende la anchura", titulo="Más pacientes, intervalo más estrecho (pero despacio)", fig="anchura",
             ideas=["La anchura depende de 1/√n: para reducirla a la mitad hay que multiplicar n por 4.",
                    "También crece con la variabilidad y con el nivel de confianza."]),
    ],
    210: [
        dict(ancla="1. Caso clínico", titulo="5 mmHg de diferencia, p = 0,03: ¿qué significa?", fig="permutacion",
             ideas=["Si el fármaco no hiciera nada, ¿con qué frecuencia el azar daría una diferencia así o mayor?",
                    "Esa frecuencia es el <b>valor p</b>. No es la probabilidad de que el fármaco no funcione."]),
        dict(ancla="2.3 Errores y potencia", titulo="Dos errores posibles y la potencia", fig="errores",
             ideas=["α: rechazar H₀ siendo cierta (falso positivo). β: no detectar un efecto real (falso negativo).",
                    "Potencia = 1 − β: la probabilidad de detectar el efecto. Aumenta con n y con el tamaño del efecto."]),
        dict(ancla="2.4 Contraste e intervalo", titulo="El intervalo de confianza dice más que el valor p", fig="ic_p",
             ideas=["Si el IC 95 % de la diferencia no contiene el 0, p < 0,05; si lo contiene, p > 0,05.",
                    "Pero solo el IC dice si el efecto puede ser clínicamente relevante o trivial."],
             pregunta="¿Cuál de estos cuatro estudios cambiaría vuestra práctica?"),
    ],
    220: [
        dict(ancla="1. Caso clínico", titulo="Tabaquismo en la cohorte: ¿distinto del 22 %? ¿distinto entre sexos?", fig="caso",
             ideas=["Una proporción frente a un valor de referencia: prueba binomial.",
                    "Dos proporciones de grupos distintos: diferencia con su IC y prueba z (o ji cuadrado)."]),
        dict(ancla="2.3 Qué prueba usar", titulo="Qué prueba usar con proporciones", fig="decision",
             ideas=["La pregunta clave: ¿son los mismos pacientes (apareados) o grupos distintos?",
                    "Con frecuencias esperadas pequeñas, Fisher."]),
    ],
    230: [
        dict(ancla="1. Caso clínico", titulo="«Reduce un 33 % el riesgo de infarto»", fig="caso",
             ideas=["Del 3 % al 2 %: la reducción <b>relativa</b> es del 33 %; la <b>absoluta</b>, de 1 punto.",
                    "Hay que tratar a 100 personas durante 5 años para evitar un infarto (NNT = 100)."],
             pregunta="¿Cuál de las dos cifras necesita vuestro paciente para decidir?"),
        dict(ancla="2.2 Medidas de asociación", titulo="La misma reducción relativa, NNT muy distintos", fig="nnt",
             ideas=["El efecto relativo suele ser parecido en pacientes de distinto riesgo; el beneficio absoluto, no.",
                    "Por eso las guías tratan según el <b>riesgo absoluto</b> (SCORE2), no solo según el colesterol."]),
        dict(ancla="2.3 Qué medida según el diseño", titulo="Cohortes frente a casos y controles", fig="disenos",
             ideas=["En cohortes y ensayos se sigue a los pacientes y se cuentan eventos: RR, DR, NNT.",
                    "En casos y controles el investigador fija cuántos casos incluye: solo la OR."]),
    ],
    240: [
        dict(ancla="1. Caso clínico", titulo="Dos modelos de IA, los mismos 200 casos", fig="caso",
             ideas=["Los casos en que aciertan (o fallan) los dos no dicen cuál es mejor.",
                    "McNemar solo compara los <b>pares discordantes</b>: 22 frente a 8."]),
        dict(ancla="2.3 Acuerdo y concordancia", titulo="Kappa: el acuerdo que no se debe al azar", fig="kappa",
             ideas=["Kappa = (acuerdo observado − acuerdo esperado por azar) / (1 − acuerdo esperado).",
                    "En escalas ordinales (niveles de triaje), kappa ponderada."]),
        dict(ancla="2.4 Asociación no es concordancia", titulo="Asociación perfecta, concordancia nula", fig="asociacion",
             ideas=["Si un observador puntúa siempre un nivel más que otro, están perfectamente asociados y nunca coinciden.",
                    "La ji cuadrado mide asociación; kappa, concordancia."]),
    ],
    250: [
        dict(ancla="1. Caso clínico", titulo="HDL en hombres y mujeres de la cohorte",
             codigo=f'''
import pandas as pd
import matplotlib.pyplot as plt

datos = pd.read_csv("{URL_LIMPIA}").dropna(subset=["hdl_mg_dl"])
grupos = [datos.loc[datos["sexo"] == s, "hdl_mg_dl"] for s in ["Hombre", "Mujer"]]
plt.figure(figsize=(9, 4.5))
plt.boxplot(grupos, widths=0.5, patch_artist=True, boxprops=dict(facecolor="lightsteelblue"), medianprops=dict(color="firebrick", lw=2))
for i, g in enumerate(grupos, start=1):
    plt.scatter([i] * len(g) + (pd.Series(range(len(g))) % 7 - 3) * 0.03, g, s=8, alpha=0.4, color="steelblue")
    plt.text(i + 0.3, g.mean(), f"media {{g.mean():.1f}}", fontsize=12, va="center")
plt.xticks([1, 2], ["Hombres", "Mujeres"])
plt.ylabel("HDL (mg/dL)")
plt.title("¿Diferencia real o azar del muestreo? ¿De qué tamaño?", fontweight="bold")
plt.show()
''',
             ideas=["Dos grupos distintos de pacientes: prueba t de Welch.",
                    "Se comunica la diferencia de medias con su IC, el valor p y el tamaño del efecto."]),
        dict(ancla="2.1 Las tres pruebas t", titulo="Tres pruebas t para tres diseños", fig="tres",
             ideas=["Una media frente a un valor de referencia · dos grupos independientes · los mismos pacientes dos veces.",
                    "El diseño, no los datos, decide la prueba."]),
        dict(ancla="2.3 Muestras relacionadas", titulo="Antes y después en los mismos pacientes", fig="apareados",
             ideas=["La variabilidad entre pacientes es mucho mayor que la del cambio dentro de cada paciente.",
                    "La prueba apareada analiza las diferencias: elimina esa variabilidad y gana potencia."]),
    ],
    260: [
        dict(ancla="1. Caso clínico", titulo="Buscar hasta encontrar algo «significativo»", fig="multiples",
             ideas=["Con 20 comparaciones sin ningún efecto real, la probabilidad de algún p < 0,05 es del 64 %.",
                    "Lo que se encuentra buscando sin plan es una hipótesis, no una conclusión."]),
        dict(ancla="2.2 El ANOVA", titulo="ANOVA: variabilidad entre grupos frente a dentro de los grupos", fig="anova",
             ideas=["F = varianza entre grupos / varianza dentro de los grupos.",
                    "Un ANOVA significativo dice que alguna media difiere; Tukey dice cuáles."]),
        dict(ancla="2.4 Pruebas no paramétricas", titulo="Las pruebas no paramétricas trabajan con rangos", fig="rangos",
             ideas=["Ordenan los valores y usan su posición: no suponen normalidad y resisten a los atípicos.",
                    "Útiles con muestras pequeñas, datos muy asimétricos y escalas ordinales (dolor, Rankin)."]),
    ],
    270: [
        dict(ancla="1. Caso clínico", titulo="PAS y creatinina: ¿o es la edad?", fig="confusion",
             ideas=["En toda la cohorte, más PAS se asocia con más creatinina.",
                    "Dentro de cada grupo de edad, la relación casi desaparece: la edad confundía la asociación."]),
        dict(ancla="2.1 La regresión lineal simple", titulo="La recta de regresión", fig="recta",
             ideas=["Pendiente: cambio medio de Y por cada unidad de X.",
                    "Mínimos cuadrados: la recta que hace mínima la suma de los residuos al cuadrado."]),
        dict(ancla="2.4 Condiciones del modelo", titulo="Mirar los residuos", fig="residuos",
             ideas=["Una nube sin patrón: el modelo es adecuado.",
                    "Una curva indica falta de linealidad; un embudo, varianza no constante."]),
    ],
    280: [
        dict(ancla="2.1 Por qué no una recta", titulo="Para un evento sí/no: la curva logística", fig="logistica",
             ideas=["Una recta puede dar probabilidades negativas o mayores de 1.",
                    "La regresión logística modela el logaritmo de la odds y devuelve probabilidades entre 0 y 1."]),
        dict(ancla="2.2 Los coeficientes", titulo="Los resultados se leen como odds ratios ajustadas", fig="forest",
             ideas=["OR > 1: más odds de evento; OR < 1: menos; IC que cruza el 1: no significativa.",
                    "Para variables cuantitativas, OR por un incremento clínico: por 10 años, por 10 mmHg."]),
        dict(ancla="2.3 Cuántas variables", titulo="Pocos eventos por variable: coeficientes inestables", fig="epv",
             ideas=["Lo que limita el modelo es el número de eventos, no el de pacientes (orientación: ≥ 10 por variable).",
                    "Con pocos eventos, la OR estimada varía muchísimo entre muestras y tiende a exagerarse."]),
    ],
    290: [
        dict(ancla="1. Caso clínico", titulo="«Exactitud del 89 %»: ¿impresiona?", fig="exactitud",
             ideas=["Si el evento ocurre en el 11 %, decir siempre «no habrá evento» acierta el 89 %.",
                    "Hay que preguntar por la discriminación, la calibración y con qué pacientes se midieron."]),
        dict(ancla="2.2 Rendimiento aparente", titulo="El rendimiento aparente es optimista", fig="aparente",
             ideas=["Un modelo evaluado con sus propios datos de entrenamiento se ha adaptado también a su ruido.",
                    "Lo que cuenta es el rendimiento en pacientes reservados y, mejor aún, de otro centro."]),
        dict(ancla="2.3 Discriminación y calibración", titulo="Discriminar no es estar bien calibrado", fig="calibracion",
             ideas=["Discriminación: ordenar bien a los pacientes por su riesgo (AUC).",
                    "Calibración: que un 20 % predicho sea un 20 % observado. Sin ella, el riesgo absoluto engaña."]),
    ],
    300: [
        dict(ancla="1. Caso clínico", titulo="«El café reduce un 30 % la mortalidad»", fig="cafe",
             ideas=["Es un estudio observacional: «se asoció con», no «reduce».",
                    "Aunque fuera causal, la diferencia absoluta sería de unos 2 puntos en 10 años."]),
        dict(ancla="2.2 Los tres grandes sesgos", titulo="Precisión no es validez", fig="diana",
             ideas=["El tamaño muestral controla el azar (precisión); los sesgos (validez) no se arreglan con más pacientes.",
                    "Un estudio enorme y sesgado da una respuesta precisa y equivocada."]),
        dict(ancla="2.4 Evaluar la mejora recursiva", titulo="Para mejorar y para medir hacen falta dos conjuntos de casos", fig="mejora",
             ideas=["Se mejora con unos casos y se mide, una sola vez, con otros reservados.",
                    "Vale para un prompt, un modelo de IA… y para tu propio aprendizaje con los informes de la app."]),
    ],
}


@figura(200, "caso")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.4))
    li, ls = _wilson(74, 120)
    ax.errorbar(74 / 120, 0, xerr=[[74 / 120 - li], [ls - 74 / 120]], fmt="o", ms=14, color=AZUL, capsize=10, lw=3)
    ax.axvline(0.65, color=ROJO, ls="--", lw=2.5)
    ax.text(0.651, 0.3, "objetivo 65 %", color=ROJO, fontsize=15)
    ax.text(0.46, -0.4, f"61,7 % (IC 95 %: {li:.1%} a {ls:.1%})".replace(".", ","), ha="left", fontsize=15, color=AZUL)
    ax.set_xlim(0.45, 0.8); ax.set_ylim(-0.6, 0.6); ax.set_yticks([])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_xlabel("Proporción de hipertensos controlados")
    return fig


@figura(200, "cien")
def _():
    rng = np.random.default_rng(200)
    fig, ax = plt.subplots(figsize=(12, 5))
    from scipy import stats
    fallos = 0
    for i in range(40):
        m = rng.normal(130, 15, 25)
        li, ls = stats.t.interval(0.95, 24, m.mean(), m.std(ddof=1) / 5)
        ok = li <= 130 <= ls
        fallos += not ok
        ax.plot([li, ls], [i, i], color=AZUL if ok else ROJO, lw=2.5)
        ax.plot(m.mean(), i, "o", color=AZUL if ok else ROJO, ms=4)
    ax.axvline(130, color=TINTA, ls="--", lw=2)
    ax.set_xlabel("PAS media (mmHg)"); ax.set_yticks([]); ax.set_ylabel("40 residentes, 25 pacientes cada uno")
    ax.set_title(f"μ = 130 mmHg: {40 - fallos} de 40 intervalos lo contienen", fontsize=16)
    return fig


@figura(200, "anchura")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ns = [30, 60, 120, 240, 480, 960]
    for i, n in enumerate(ns):
        li, ls = _wilson(round(0.617 * n), n)
        ax.plot([li, ls], [i, i], color=AZUL, lw=4)
        ax.plot(0.617, i, "o", color=AZUL, ms=9)
        ax.text(ls + 0.01, i, f"±{(ls - li) / 2:.1%}".replace(".", ","), va="center", fontsize=13, color=TINTA)
    ax.set_yticks(range(len(ns)), [f"n = {n}" for n in ns])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_xlabel("IC 95 % de una proporción del 61,7 %")
    return fig


@figura(210, "permutacion")
def _():
    rng = np.random.default_rng(210)
    d = rng.normal(0, 2.25, 20000)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.hist(d, bins=80, color=AZUL_CLARO, ec="white")
    ax.hist(d[np.abs(d) >= 5], bins=80, color=ROJO)
    ax.axvline(5, color=ROJO, lw=2.5); ax.axvline(-5, color=ROJO, lw=2, ls="--")
    ax.text(5.3, ax.get_ylim()[1] * 0.6, "observada:\n5 mmHg", color=ROJO, fontsize=15)
    ax.text(0, ax.get_ylim()[1] * 0.25, "Diferencias que da el azar\nsi el fármaco no hiciera nada", ha="center", fontsize=14, color=TINTA)
    ax.set_xlabel("Diferencia de medias entre grupos (mmHg)"); ax.set_yticks([])
    ax.set_title("Valor p = proporción en rojo ≈ 0,03", fontsize=16)
    return fig


@figura(210, "errores")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    x = np.linspace(-4, 7, 600)
    f0 = np.exp(-x ** 2 / 2); f1 = np.exp(-(x - 2.5) ** 2 / 2)
    c = 1.96
    ax.plot(x, f0, color=AZUL, lw=2.5); ax.plot(x, f1, color=VERDE, lw=2.5)
    ax.fill_between(x, f0, where=x >= c, color=ROJO, alpha=0.6, label="α: falso positivo")
    ax.fill_between(x, f1, where=x < c, color=NARANJA, alpha=0.5, label="β: falso negativo")
    ax.fill_between(x, f1, where=x >= c, color=VERDE, alpha=0.2, label="Potencia = 1 − β")
    ax.axvline(c, color=TINTA, ls="--", lw=2)
    ax.text(0, 1.04, "Si H₀ es cierta\n(no hay efecto)", ha="center", fontsize=14, color=AZUL)
    ax.text(2.7, 1.04, "Si hay efecto real", ha="center", fontsize=14, color=VERDE)
    ax.text(c + 0.05, 0.75, "umbral de\nsignificación", fontsize=12)
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(0, 1.25); ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    ax.set_xlabel("Estadístico del contraste")
    return fig


@figura(210, "ic_p")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    estudios = [("A: n grande, efecto trivial", 0.8, 0.3, 1.3, "p < 0,001"), ("B: efecto relevante y preciso", 8, 5, 11, "p < 0,001"),
                ("C: pequeño e impreciso", 6, -1, 13, "p = 0,09"), ("D: preciso, sin efecto", 0.5, -1.5, 2.5, "p = 0,6")]
    ax.axvspan(5, 15, color=VERDE, alpha=0.1)
    ax.text(10, 3.55, "relevante (≥ 5 mmHg)", ha="center", fontsize=13, color=VERDE)
    for i, (t, m, li, ls, p) in enumerate(estudios[::-1]):
        ax.plot([li, ls], [i, i], color=AZUL, lw=4); ax.plot(m, i, "o", color=AZUL, ms=10)
        ax.text(ls + 0.4, i, p, va="center", fontsize=13)
    ax.axvline(0, color=TINTA, lw=2)
    ax.set_yticks(range(4), [e[0] for e in estudios[::-1]], fontsize=14)
    ax.set_xlabel("Diferencia de PAS (mmHg) con su IC 95 %"); ax.set_xlim(-3, 16); ax.set_ylim(-0.5, 3.8)
    return fig


@figura(220, "caso")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    datos = [("Toda la cohorte", 91, 391), ("Hombres", 55, 194), ("Mujeres", 36, 197)]
    for i, (t, x, n) in enumerate(datos[::-1]):
        li, ls = _wilson(x, n)
        ax.errorbar(x / n, i, xerr=[[x / n - li], [ls - x / n]], fmt="o", ms=12, capsize=8, lw=3, color=[AZUL, ROJO, TINTA][::-1][i])
        ax.text(ls + 0.01, i, f"{x / n:.1%}".replace(".", ","), va="center", fontsize=14)
    ax.axvline(0.22, color=NARANJA, ls="--", lw=2.5)
    ax.text(0.222, 2.4, "referencia 22 %", color=NARANJA, fontsize=14)
    ax.set_yticks(range(3), [d[0] for d in datos[::-1]], fontsize=15)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.set_xlabel("Prevalencia de tabaquismo (IC 95 % de Wilson)"); ax.set_ylim(-0.5, 2.8)
    return fig


@figura(220, "decision")
def _():
    fig, ax = lienzo(12, 5.5)
    caja(ax, 36, 82, 28, 11, "¿Cuántas proporciones?", tam=15, negrita=True)
    caja(ax, 3, 52, 26, 14, "Una frente a un valor\n→ binomial exacta", tam=14, relleno="white")
    caja(ax, 52, 54, 34, 11, "Dos: ¿los mismos pacientes?", tam=15)
    caja(ax, 34, 20, 22, 14, "Sí (apareados)\n→ McNemar", tam=14, relleno="white", color=NARANJA)
    caja(ax, 64, 26, 32, 11, "No: ¿esperadas ≥ 5?", tam=15)
    caja(ax, 58, 1, 18, 13, "Sí → z o\nji cuadrado", tam=14, relleno="white", color=VERDE)
    caja(ax, 80, 1, 18, 13, "No →\nFisher", tam=14, relleno="white", color=ROJO)
    flecha(ax, 44, 81, 18, 67); flecha(ax, 56, 81, 68, 66); flecha(ax, 62, 53, 47, 35); flecha(ax, 74, 53, 80, 38); flecha(ax, 75, 25, 68, 15); flecha(ax, 85, 25, 89, 15)
    return fig


@figura(230, "caso")
def _():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax, (t, k, c) in zip(axs, [("Placebo: 3 de cada 100", 3, ROJO), ("Fármaco: 2 de cada 100", 2, ROJO)]):
        cols = [c if i < k else AZUL_CLARO for i in range(100)]
        ax.scatter(np.arange(100) % 10, np.arange(100) // 10, c=cols, s=230, edgecolors=GRIS)
        ax.set_title(t, fontsize=17); ax.axis("off"); ax.set_aspect("equal")
    fig.text(0.5, 0.02, "Reducción relativa: (3 − 2) / 3 = 33 %   ·   Reducción absoluta: 1 punto   ·   NNT = 1 / 0,01 = 100 (5 años)",
             ha="center", fontsize=14, color=TINTA)
    return fig


@figura(230, "nnt")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    basal = np.array([0.03, 0.06, 0.12, 0.24])
    nnt = 1 / (basal / 3)
    b = ax.bar([f"{x:.0%}" for x in basal], nnt, color=[ROJO, NARANJA, AZUL, VERDE])
    for r, v in zip(b, nnt):
        ax.text(r.get_x() + r.get_width() / 2, v + 2, f"NNT = {v:.0f}", ha="center", fontsize=15, fontweight="bold")
    ax.set_xlabel("Riesgo basal a 5 años (con la misma reducción relativa del 33 %)"); ax.set_ylabel("NNT"); ax.set_ylim(0, 115)
    return fig


@figura(230, "disenos")
def _():
    fig, ax = lienzo(12, 5)
    ax.text(25, 92, "Cohortes y ensayos", ha="center", fontsize=17, fontweight="bold", color=TINTA)
    caja(ax, 3, 52, 18, 18, "Expuestos\ny no expuestos", tam=13)
    caja(ax, 30, 52, 18, 18, "¿Evento?\n(se cuenta)", tam=13)
    flecha(ax, 22, 61, 29, 61, color=AZUL)
    ax.text(25.5, 74, "tiempo", ha="center", fontsize=12, color=AZUL)
    ax.text(25, 36, "Riesgo calculable:\nRR, DR, NNT (y OR)", ha="center", fontsize=15, color=AZUL)
    ax.text(75, 92, "Casos y controles", ha="center", fontsize=17, fontweight="bold", color=TINTA)
    caja(ax, 53, 52, 18, 18, "¿Exposición\nprevia?", tam=13)
    caja(ax, 80, 52, 18, 18, "Casos y\ncontroles\n(se eligen)", tam=13, color=NARANJA, relleno="#FDEFD9")
    flecha(ax, 79, 61, 72, 61, color=NARANJA)
    ax.text(75.5, 74, "se mira atrás", ha="center", fontsize=12, color=NARANJA)
    ax.text(75, 36, "El investigador fija cuántos\ncasos incluye: solo la OR", ha="center", fontsize=15, color=NARANJA)
    return fig


@figura(240, "caso")
def _():
    fig, ax = lienzo(12, 4.6)
    ax.text(50, 92, "Modelo anterior", ha="center", fontsize=16, fontweight="bold", color=TINTA)
    ax.text(38, 82, "acierta", ha="center", fontsize=15, color=TINTA); ax.text(62, 82, "falla", ha="center", fontsize=15, color=TINTA)
    ax.text(14, 62, "Modelo nuevo\nacierta", ha="center", fontsize=15, color=TINTA); ax.text(14, 32, "Modelo nuevo\nfalla", ha="center", fontsize=15, color=TINTA)
    for (x, y, v, d) in [(26, 50, 140, False), (50, 50, 22, True), (26, 20, 8, True), (50, 20, 30, False)]:
        ax.add_patch(plt.Rectangle((x, y), 24, 28, fc="#FDEFD9" if d else "#EEEEEE", ec=TINTA, lw=2))
        ax.text(x + 12, y + 14, str(v), ha="center", va="center", fontsize=24, fontweight="bold", color=NARANJA if d else GRIS)
    ax.text(88, 50, "Solo cuentan los\npares discordantes:\n22 frente a 8\n\nMcNemar exacta:\np = 0,016", ha="center", va="center", fontsize=15, color=TINTA)
    return fig


@figura(240, "kappa")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    po, pe = 0.78, 0.59
    ax.barh([0], [pe], color=GRIS, label="acuerdo esperado por azar (59 %)")
    ax.barh([0], [po - pe], left=[pe], color=VERDE, label="acuerdo más allá del azar")
    ax.barh([0], [1 - po], left=[po], color="#EEEEEE", label="desacuerdo")
    ax.annotate("", xy=(pe, 0.5), xytext=(1, 0.5), arrowprops=dict(arrowstyle="<->", lw=2))
    ax.text((pe + 1) / 2, 0.58, "acuerdo posible más allá del azar: 1 − 0,59", ha="center", fontsize=13)
    ax.text(0.5, -0.75, "κ = (0,78 − 0,59) / (1 − 0,59) ≈ 0,46  →  concordancia moderada", ha="center", fontsize=16, color=TINTA, fontweight="bold")
    ax.set_xlim(0, 1); ax.set_ylim(-1, 1); ax.set_yticks([])
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.legend(loc="upper left", fontsize=12, ncol=3, bbox_to_anchor=(0, 1.25))
    return fig


@figura(240, "asociacion")
def _():
    rng = np.random.default_rng(24)
    a = rng.integers(1, 5, 60)
    b = a + 1
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(a + rng.uniform(-0.15, 0.15, 60), b + rng.uniform(-0.15, 0.15, 60), s=60, color=AZUL, alpha=0.7)
    ax.plot([0.5, 5.5], [0.5, 5.5], "--", color=VERDE, lw=2, label="coincidencia perfecta")
    ax.set_xlabel("Nivel de gravedad: enfermera"); ax.set_ylabel("Nivel de gravedad: asistente")
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6)); ax.legend(loc="upper left")
    ax.set_title("Siempre un nivel más: asociación perfecta, κ < 0", fontsize=15)
    return fig


@figura(250, "tres")
def _():
    rng = np.random.default_rng(25)
    fig, axs = plt.subplots(1, 3, figsize=(13, 4))
    x = rng.normal(7.4, 0.9, 40)
    axs[0].scatter(rng.uniform(-0.1, 0.1, 40), x, color=AZUL, s=20); axs[0].axhline(7, color=ROJO, ls="--", lw=2)
    axs[0].text(0.12, 7.05, "objetivo 7 %", color=ROJO, fontsize=12); axs[0].set_title("Una muestra\nfrente a un valor", fontsize=14)
    axs[0].set_xticks([]); axs[0].set_ylabel("HbA1c (%)")
    g1, g2 = rng.normal(49, 10, 40), rng.normal(58, 12, 40)
    axs[1].boxplot([g1, g2], widths=0.5); axs[1].set_xticks([1, 2], ["Hombres", "Mujeres"]); axs[1].set_title("Dos grupos\nindependientes", fontsize=14)
    axs[1].set_ylabel("HDL (mg/dL)")
    antes = rng.normal(150, 12, 15); despues = antes - rng.normal(5, 4, 15)
    for a, d in zip(antes, despues):
        axs[2].plot([0, 1], [a, d], "o-", color=AZUL, alpha=0.6)
    axs[2].set_xticks([0, 1], ["Antes", "Después"]); axs[2].set_title("Los mismos pacientes\ndos veces", fontsize=14); axs[2].set_ylabel("PAS (mmHg)")
    plt.tight_layout()
    return fig


@figura(250, "apareados")
def _():
    rng = np.random.default_rng(250)
    antes = rng.normal(148, 13, 30).round(); despues = (antes - rng.normal(5, 6, 30)).round()
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.4))
    axs[0].boxplot([antes, despues], widths=0.5); axs[0].set_xticks([1, 2], ["Antes", "Después"])
    axs[0].set_title("Como grupos independientes:\nlas cajas casi se solapan", fontsize=14); axs[0].set_ylabel("PAS (mmHg)")
    axs[1].hist(despues - antes, bins=10, color=AZUL_CLARO, ec=AZUL); axs[1].axvline(0, color=ROJO, lw=2, ls="--")
    axs[1].set_title("Como diferencias de cada paciente:\ncasi todas por debajo de 0", fontsize=14); axs[1].set_xlabel("Cambio de PAS (mmHg)")
    plt.tight_layout()
    return fig


@figura(260, "multiples")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    k = np.array([1, 3, 5, 10, 20, 40])
    p = 1 - 0.95 ** k
    b = ax.bar([str(x) for x in k], p, color=[AZUL] + [NARANJA] * 3 + [ROJO] * 2)
    for r, v in zip(b, p):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.02, f"{v:.0%}", ha="center", fontsize=15, fontweight="bold")
    ax.set_xlabel("Número de comparaciones sin ningún efecto real"); ax.set_ylabel("P(al menos un p < 0,05)"); ax.set_ylim(0, 1.05)
    return fig


@figura(260, "anova")
def _():
    rng = np.random.default_rng(26)
    fig, ax = plt.subplots(figsize=(12, 4.6))
    medias = [122, 126, 133]
    nombres = ["Normopeso", "Sobrepeso", "Obesidad"]
    todos = []
    for i, (m, n) in enumerate(zip(medias, nombres)):
        y = rng.normal(m, 14, 40)
        todos += list(y)
        ax.scatter(i + rng.uniform(-0.15, 0.15, 40), y, s=18, color=AZUL, alpha=0.5)
        ax.plot([i - 0.3, i + 0.3], [y.mean()] * 2, color=ROJO, lw=4)
    g = np.mean(todos)
    ax.axhline(g, color=TINTA, ls="--", lw=2)
    ax.text(-0.85, g + 1.5, "media global", fontsize=13)
    ax.annotate("", xy=(2.4, g), xytext=(2.4, 133), arrowprops=dict(arrowstyle="<->", color=ROJO, lw=2))
    ax.text(2.45, (g + 133) / 2, "entre\ngrupos", color=ROJO, fontsize=13, va="center")
    ax.annotate("", xy=(-0.42, 100), xytext=(-0.42, 145), arrowprops=dict(arrowstyle="<->", color=AZUL, lw=2))
    ax.text(-0.88, 108, "dentro\ndel\ngrupo", color=AZUL, fontsize=13, va="center")
    ax.set_xticks(range(3), nombres); ax.set_ylabel("PAS (mmHg)"); ax.set_xlim(-0.9, 2.9)
    return fig


@figura(260, "rangos")
def _():
    fig, ax = lienzo(12, 3.8)
    vals = [3, 4, 4, 5, 6, 32]
    rangos = [1, 2.5, 2.5, 4, 5, 6]
    ax.text(2, 75, "Valores (días):", fontsize=16, color=TINTA, va="center")
    ax.text(2, 35, "Rangos:", fontsize=16, color=TINTA, va="center")
    for i, (v, r) in enumerate(zip(vals, rangos)):
        x = 32 + i * 11
        caja(ax, x, 66, 8, 18, str(v), tam=18, negrita=True, color=ROJO if v == 32 else AZUL, relleno="#FBE5E1" if v == 32 else AZUL_CLARO)
        caja(ax, x, 26, 8, 18, f"{r:g}", tam=18, negrita=True, relleno="white")
        flecha(ax, x + 4, 64, x + 4, 46)
    ax.text(50, 6, "El valor extremo (32) solo cuenta como «el mayor»; los empates comparten rango", ha="center", fontsize=14, color=GRIS)
    return fig


@figura(270, "confusion")
def _():
    rng = np.random.default_rng(27)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    colores = [AZUL, NARANJA, ROJO]
    xs, ys = [], []
    for k, (edad, c) in enumerate(zip(["< 55 años", "55-70 años", "> 70 años"], colores)):
        pas = rng.normal(118 + 14 * k, 9, 50)
        cr = 0.75 + 0.18 * k + 0.0015 * (pas - pas.mean()) + rng.normal(0, 0.07, 50)
        ax.scatter(pas, cr, s=22, color=c, alpha=0.7, label=edad)
        b = np.polyfit(pas, cr, 1); xx = np.linspace(pas.min(), pas.max(), 10)
        ax.plot(xx, np.polyval(b, xx), color=c, lw=2.5)
        xs += list(pas); ys += list(cr)
    b = np.polyfit(xs, ys, 1); xx = np.linspace(min(xs), max(xs), 10)
    ax.plot(xx, np.polyval(b, xx), "--", color=TINTA, lw=3, label="toda la cohorte (sin ajustar)")
    ax.set_xlabel("PAS (mmHg)"); ax.set_ylabel("Creatinina (mg/dL)"); ax.legend(fontsize=12)
    ax.set_title("Datos ilustrativos", fontsize=12, color=GRIS)
    return fig


@figura(270, "recta")
def _():
    rng = np.random.default_rng(270)
    x = rng.uniform(40, 85, 25); y = 92 + 0.56 * x + rng.normal(0, 9, 25)
    b1, b0 = np.polyfit(x, y, 1)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    for xi, yi in zip(x, y):
        ax.plot([xi, xi], [yi, b0 + b1 * xi], color=ROJO, lw=1.2, alpha=0.7)
    ax.scatter(x, y, color=AZUL, s=40, zorder=3)
    xx = np.linspace(38, 88, 10); ax.plot(xx, b0 + b1 * xx, color=TINTA, lw=3)
    ax.annotate("", xy=(70, b0 + b1 * 70), xytext=(60, b0 + b1 * 60), arrowprops=dict(arrowstyle="-", lw=0))
    ax.plot([60, 70, 70], [b0 + b1 * 60, b0 + b1 * 60, b0 + b1 * 70], color=VERDE, lw=2.5)
    ax.text(71, b0 + b1 * 65, f"+10 años → +{10 * b1:.1f} mmHg\n(pendiente = {b1:.2f})", color=VERDE, fontsize=14, va="center")
    ax.text(40, max(y) - 2, "residuos (en rojo): lo que la recta no explica", color=ROJO, fontsize=13)
    ax.set_xlabel("Edad (años)"); ax.set_ylabel("PAS (mmHg)")
    return fig


@figura(270, "residuos")
def _():
    rng = np.random.default_rng(271)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=False)
    x = rng.uniform(0, 10, 150)
    for ax, (t, r, c) in zip(axs, [("Sin patrón: adecuado", rng.normal(0, 1, 150), VERDE), ("Curva: falta linealidad", (x - 5) ** 2 / 4 - 2 + rng.normal(0, 0.6, 150), ROJO),
                                  ("Embudo: varianza no constante", rng.normal(0, 1, 150) * (0.2 + x / 4), NARANJA)]):
        ax.scatter(x, r, s=12, color=c); ax.axhline(0, color=TINTA, lw=1.5)
        ax.set_title(t, fontsize=14); ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel("Valores ajustados"); ax.set_ylabel("Residuos")
    plt.tight_layout()
    return fig


@figura(280, "logistica")
def _():
    rng = np.random.default_rng(28)
    edad = rng.uniform(40, 88, 300)
    p = 1 / (1 + np.exp(-(-7.4 + 0.085 * edad)))
    y = rng.random(300) < p
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.scatter(edad, y + rng.uniform(-0.03, 0.03, 300), s=12, color=AZUL, alpha=0.5)
    xx = np.linspace(20, 100, 200)
    b = np.polyfit(edad, y.astype(float), 1)
    ax.plot(xx, np.polyval(b, xx), "--", color=GRIS, lw=2.5, label="recta (puede salir de 0-1)")
    ax.plot(xx, 1 / (1 + np.exp(-(-7.4 + 0.085 * xx))), color=ROJO, lw=3, label="curva logística")
    ax.axhline(0, color=TINTA, lw=0.8); ax.axhline(1, color=TINTA, lw=0.8)
    ax.set_xlabel("Edad (años)"); ax.set_ylabel("Probabilidad de evento a 5 años"); ax.legend(loc="upper left")
    return fig


@figura(280, "forest")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    filas = [("Edad (por 10 años)", 2.0, 1.4, 2.9), ("PAS (por 10 mmHg)", 1.3, 1.05, 1.6), ("Mujer", 0.45, 0.22, 0.9),
             ("Diabetes", 1.5, 0.7, 3.2), ("Fumador", 1.4, 0.7, 2.8)]
    for i, (t, o, li, ls) in enumerate(filas[::-1]):
        sig = li > 1 or ls < 1
        ax.plot([li, ls], [i, i], color=AZUL if sig else GRIS, lw=3.5)
        ax.plot(o, i, "s", ms=11, color=AZUL if sig else GRIS)
    ax.axvline(1, color=ROJO, ls="--", lw=2)
    ax.set_xscale("log"); ax.set_xticks([0.25, 0.5, 1, 2, 4], ["0,25", "0,5", "1", "2", "4"])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_yticks(range(len(filas)), [f[0] for f in filas[::-1]], fontsize=14)
    ax.set_xlabel("Odds ratio ajustada (IC 95 %, escala logarítmica)")
    ax.set_title("Ejemplo ilustrativo: en gris, IC que incluyen el 1", fontsize=13, color=GRIS)
    return fig


@figura(280, "epv")
def _():
    rng = np.random.default_rng(280)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    real = 1.20
    for i, (n, epv) in enumerate([(300, "≈ 4"), (1000, "≈ 13"), (5000, "≈ 65")]):
        ors = []
        for _ in range(300):
            x = rng.normal(0, 1, n)
            p = 1 / (1 + np.exp(-(-2.3 + np.log(real) * x)))
            y = rng.random(n) < p
            a, b = x[y], x[~y]
            beta = (a.mean() - b.mean()) / np.var(x)
            ors.append(np.exp(beta))
        ors = np.array(ors)
        lo, hi = np.percentile(ors, [5, 95])
        ax.plot([lo, hi], [i, i], color=AZUL, lw=6, solid_capstyle="round")
        ax.text(hi * 1.02, i, f"{lo:.2f} a {hi:.2f}".replace(".", ","), va="center", fontsize=13)
    ax.axvline(real, color=ROJO, ls="--", lw=2); ax.text(real * 1.005, 2.45, "OR real = 1,20", color=ROJO, fontsize=13)
    ax.set_yticks(range(3), ["300 pacientes\n(EPV ≈ 4)", "1.000 pacientes\n(EPV ≈ 13)", "5.000 pacientes\n(EPV ≈ 65)"], fontsize=13)
    ax.set_xlabel("OR estimada en 300 muestras simuladas (90 % central)"); ax.set_ylim(-0.5, 2.8)
    return fig


@figura(290, "exactitud")
def _():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
    axs[0].bar(["Siempre «no»", "Modelo del folleto"], [0.89, 0.89], color=[GRIS, AZUL])
    axs[0].set_title("Exactitud", fontsize=15); axs[0].set_ylim(0, 1)
    axs[1].bar(["Siempre «no»", "Modelo del folleto"], [0.5, 0.72], color=[GRIS, AZUL])
    axs[1].set_title("AUC (en pacientes reservados)", fontsize=15); axs[1].set_ylim(0, 1)
    for ax in axs:
        for r in ax.patches:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 0.02, f"{r.get_height():.2f}".replace(".", ","), ha="center", fontsize=15)
    fig.text(0.5, -0.02, "Con un evento en el 11 % de los pacientes, la exactitud no distingue un modelo de no hacer nada (valores ilustrativos)", ha="center", fontsize=12, color=GRIS)
    plt.tight_layout()
    return fig


@figura(290, "aparente")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    grupos = ["Datos de entrenamiento\n(aparente)", "Pacientes reservados\n(validación interna)", "Otro hospital\n(validación externa)"]
    rl, rf = [0.80, 0.72, 0.70], [1.00, 0.61, 0.60]
    x = np.arange(3)
    ax.bar(x - 0.18, rl, 0.36, color=AZUL, label="Regresión logística")
    ax.bar(x + 0.18, rf, 0.36, color=NARANJA, label="Bosque aleatorio (IA)")
    ax.axhline(0.5, color=GRIS, ls="--"); ax.text(2.45, 0.51, "azar", color=GRIS)
    ax.set_xticks(x, grupos, fontsize=13); ax.set_ylabel("AUC"); ax.set_ylim(0.4, 1.05); ax.legend(loc="upper right")
    ax.set_title("Valores ilustrativos, del orden de los del cuaderno", fontsize=12, color=GRIS)
    return fig


@figura(290, "calibracion")
def _():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    p = np.linspace(0.02, 0.6, 8)
    for ax, (t, o, c) in zip(axs, [("Bien calibrado", p, VERDE), ("Discrimina igual, pero infraestima", np.clip(p * 1.6, 0, 1), ROJO)]):
        ax.plot([0, 1], [0, 1], "--", color=GRIS)
        ax.plot(p, o, "o-", color=c, lw=2.5, ms=9)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_title(t, fontsize=15)
        ax.set_xlabel("Riesgo predicho"); ax.set_ylabel("Proporción observada")
    plt.tight_layout()
    return fig


@figura(300, "cafe")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.bar(["Sin café", "3 o más cafés/día"], [8.0, 5.7], color=[GRIS, AZUL], width=0.5)
    for i, v in enumerate([8.0, 5.7]):
        ax.text(i, v + 0.2, f"{v:.1f} %".replace(".", ","), ha="center", fontsize=17, fontweight="bold")
    ax.text(1.45, 6.6, "HR 0,70: «un 30 % menos»\n= unos 2,3 puntos en 10 años\n≈ 43 personas para «evitar»\nuna muerte (si fuera causal)", fontsize=14, color=TINTA, va="center")
    ax.set_ylabel("Mortalidad a 10 años (%)"); ax.set_ylim(0, 9.5); ax.set_xlim(-0.5, 2.6)
    ax.set_title("Mortalidad basal supuesta del 8 %, para ilustrar", fontsize=12, color=GRIS)
    return fig


@figura(300, "diana")
def _():
    rng = np.random.default_rng(30)
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.9))
    for ax, (t, cx, sd) in zip(axs, [("Preciso y válido", 0, 0.12), ("Impreciso pero válido\n(muestra pequeña)", 0, 0.45),
                                    ("Preciso pero sesgado\n(muestra grande y sesgada)", 0.55, 0.12), ("Impreciso y sesgado", 0.55, 0.45)]):
        for r, c in [(1, "#F7D9D5"), (0.66, "white"), (0.33, "#F7D9D5")]:
            ax.add_patch(plt.Circle((0, 0), r, fc=c, ec=ROJO))
        pts = rng.normal(0, sd, (15, 2)) + [cx, 0.25 if cx else 0]
        ax.scatter(pts[:, 0], pts[:, 1], color=AZUL, s=30, zorder=3)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(t, fontsize=13)
    plt.tight_layout()
    return fig


@figura(300, "mejora")
def _():
    fig, ax = lienzo(12, 4.6)
    caja(ax, 3, 30, 30, 40, "Casos de desarrollo\n\nse usan para mejorar\nel prompt, el modelo\no tu forma de estudiar", tam=14)
    caja(ax, 67, 30, 30, 40, "Casos reservados\n\nse usan una sola vez,\nal final, para medir", tam=14, color=VERDE, relleno="#E3F4EA")
    ax.text(18, 80, "mejorar → probar → corregir (ciclo)", ha="center", fontsize=13, color=AZUL)
    flecha(ax, 35, 50, 65, 50, color=GRIS, texto="versión final", tam=14)
    ax.text(50, 12, "Si los casos reservados se usan para decidir, dejan de medir (Goodhart)", ha="center", fontsize=14, color=ROJO)
    return fig
