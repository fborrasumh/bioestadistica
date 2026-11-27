"""Diapositivas del Módulo 4 · Probabilidad (temas 140 a 190)."""
import math

import numpy as np

from .estilo import (AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt)

DIAPOS = {
    140: [
        dict(ancla="1. Caso clínico", titulo="Consejo genético: dos portadores de fibrosis quística", fig="punnett",
             ideas=["Cada hijo recibe un alelo de cada progenitor, al azar: cuatro combinaciones igual de probables.",
                    "P(hijo afectado) = 1/4; P(portador sano) = 1/2; P(sano no portador) = 1/4.",
                    "No se puede predecir un embarazo concreto, pero sí cuantificar la incertidumbre."]),
        dict(ancla="2.3 Axiomas y reglas", titulo="Unión, intersección y complementario", fig="venn",
             ideas=["P(A o B) = P(A) + P(B) − P(A y B): si no se resta la intersección, se cuenta dos veces.",
                    "P(no A) = 1 − P(A): el atajo para calcular «al menos uno»."]),
        dict(ancla="2.4 Técnicas de recuento", titulo="Tres hijos: ¿al menos uno afectado?", fig="arbol",
             ideas=["Con sucesos independientes, las probabilidades se multiplican a lo largo de cada rama.",
                    "P(al menos uno) = 1 − P(ninguno) = 1 − (3/4)³ ≈ 0,58."],
             pregunta="¿Por qué no es 1/4 + 1/4 + 1/4 = 3/4?"),
    ],
    150: [
        dict(ancla="1. Caso clínico", titulo="Lucía tiene una mamografía positiva: ¿qué probabilidad hay de cáncer?", fig="arbol",
             ideas=["De 1.000 mujeres, 10 tienen cáncer y 9 dan positivo; de las 990 sanas, 89 dan positivo.",
                    "Entre las 98 con mamografía positiva, solo 9 tienen cáncer: <b>alrededor del 9 %</b>, no el 90 %."],
             pregunta="Antes de calcular: ¿qué respondería la mayoría de la gente?"),
        dict(ancla="2.1 Probabilidad condicionada", titulo="Condicionar es cambiar el universo", fig="condicionada",
             ideas=["P(A | B) solo mira dentro de B: P(A | B) = P(A y B) / P(B).",
                    "P(positivo | cáncer) = 0,90 no es lo mismo que P(cáncer | positivo) ≈ 0,09."]),
        dict(ancla="2.4 Frecuencias naturales", titulo="1.000 mujeres que se criban", fig="iconos",
             ideas=["Las frecuencias naturales hacen visible lo que el teorema de Bayes calcula.",
                    "Con una prevalencia baja, la mayoría de los positivos son falsos positivos."]),
        dict(ancla="2.5 Odds y cocientes", titulo="Probabilidad previa → posterior con el cociente de probabilidad",
             codigo=r'''
import numpy as np
import matplotlib.pyplot as plt

previa = np.linspace(0.001, 0.999, 400)
plt.figure(figsize=(10, 5))
for cp, color in [(10, "firebrick"), (3, "darkorange"), (1, "gray"), (0.3, "seagreen"), (0.1, "steelblue")]:
    odds_post = previa / (1 - previa) * cp
    plt.plot(previa, odds_post / (1 + odds_post), lw=2.5, color=color, label=f"CP = {cp}")
plt.axvline(0.01, color="black", ls=":", lw=1.5)
plt.text(0.02, 0.92, "Lucía: probabilidad previa 1 %", fontsize=12)
plt.xlabel("Probabilidad previa")
plt.ylabel("Probabilidad posterior")
plt.title("El mismo resultado vale más o menos según la probabilidad previa", fontweight="bold")
plt.legend()
plt.show()
''',
             ideas=["Odds posterior = odds previa × cociente de probabilidad (CP).",
                    "Un CP de 10 cambia mucho la decisión con una previa intermedia y poco con una previa muy baja."]),
    ],
    160: [
        dict(ancla="1. Caso clínico", titulo="NT-proBNP: ¿dónde ponemos el punto de corte?", fig="corte",
             ideas=["Enfermos y sanos se solapan: ningún corte separa perfectamente.",
                    "Bajar el corte → más sensibilidad y más falsos positivos; subirlo → más especificidad y más falsos negativos."]),
        dict(ancla="2.1 La tabla 2 × 2", titulo="La tabla 2 × 2 y sus cuatro índices", fig="tabla",
             ideas=["Sensibilidad y especificidad se leen por <b>columnas</b> (según la enfermedad).",
                    "Los valores predictivos se leen por <b>filas</b> (según el resultado) y dependen de la prevalencia."]),
        dict(ancla="2.4 Punto de corte y curva ROC", titulo="La curva ROC resume todos los puntos de corte", fig="roc",
             ideas=["Cada punto es un corte: sensibilidad frente a 1 − especificidad.",
                    "El área bajo la curva (AUC) es la probabilidad de que un enfermo tenga un valor mayor que un sano."]),
    ],
    170: [
        dict(ancla="1. Caso clínico", titulo="Ocho infecciones en marzo: ¿brote o azar?",
             codigo=r'''
from scipy import stats
import matplotlib.pyplot as plt

x = range(0, 13)
p = stats.poisson.pmf(x, 3)
plt.figure(figsize=(10, 4.5))
plt.bar(x, p, color=["firebrick" if k >= 8 else "steelblue" for k in x])
plt.xlabel("Infecciones de herida quirúrgica en un mes")
plt.ylabel("Probabilidad")
plt.title(f"Si la media sigue siendo 3: P(8 o más) = {stats.poisson.sf(7, 3):.3f}", fontweight="bold")
plt.xticks(x)
plt.show()
''',
             ideas=["Si nada hubiera cambiado, 8 o más casos ocurrirían en 1 de cada 80 meses, aproximadamente.",
                    "Es raro bajo el modelo de azar: justifica investigar, no prueba un brote."]),
        dict(ancla="2.2 La distribución binomial", titulo="Binomial: aciertos en n ensayos independientes", fig="binomial",
             ideas=["n ensayos, misma probabilidad p, independientes: número de éxitos ~ B(n, p).",
                    "Media n·p; varianza n·p·(1 − p)."]),
        dict(ancla="2.3 La distribución de Poisson", titulo="Poisson: recuentos de sucesos raros", fig="poisson",
             ideas=["Número de sucesos en un intervalo de tiempo o espacio, sin máximo fijo.",
                    "Media = varianza = λ. Si la varianza es mucho mayor, hay sobredispersión (contagios, conglomerados)."]),
    ],
    180: [
        dict(ancla="1. Caso clínico", titulo="Javier, sano, con dos valores «fuera de rango»", fig="intervalo",
             ideas=["El intervalo de referencia contiene al 95 % central de los <b>sanos</b>: un 5 % de sanos queda fuera.",
                    "Fuera del intervalo significa «poco frecuente en sanos», no «enfermo»."]),
        dict(ancla="2.2 La distribución normal", titulo="La regla 68 – 95 – 99,7", fig="regla",
             ideas=["La normal queda definida por su media μ y su desviación típica σ.",
                    "μ ± 1,96 σ contiene al 95 % de los valores."]),
        dict(ancla="2.3 Tipificación", titulo="Tipificar: ¿a cuántas desviaciones de la media está?", fig="z",
             ideas=["z = (x − μ) / σ pone en la misma escala variables con unidades distintas.",
                    "|z| > 1,96 → fuera del 95 % central."]),
        dict(ancla="2.4 Intervalos de referencia", titulo="20 parámetros: lo raro es que todo salga normal", fig="veinte",
             ideas=["Con 20 parámetros independientes, P(al menos uno fuera) = 1 − 0,95²⁰ ≈ 64 %.",
                    "Por eso un valor ligeramente alterado y aislado en un sano suele no tener importancia."]),
    ],
    190: [
        dict(ancla="1. Caso clínico", titulo="Cada residente obtiene una media distinta",
             codigo=r'''
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(190)
poblacion = rng.lognormal(1.8, 0.5, 20000)        # estancias del hospital (asimétrica)
medias = [rng.choice(poblacion, 30).mean() for _ in range(200)]
fig, ejes = plt.subplots(1, 2, figsize=(13, 4.2))
ejes[0].hist(poblacion, bins=60, color="lightsteelblue", ec="steelblue")
ejes[0].set_title("Población: estancias de todos los pacientes", fontweight="bold")
ejes[0].set_xlabel("Días")
ejes[1].hist(medias, bins=25, color="darkorange", ec="white")
ejes[1].set_title("Medias de 200 residentes (30 historias cada uno)", fontweight="bold")
ejes[1].set_xlabel("Estancia media (días)")
for e in ejes:
    e.axvline(poblacion.mean(), color="firebrick", lw=2.5, ls="--")
plt.tight_layout()
plt.show()
''',
             ideas=["La media varía de una muestra a otra: es la <b>distribución muestral</b>.",
                    "Su desviación típica es el <b>error estándar</b>: mide cuánto se equivoca una muestra típica."]),
        dict(ancla="2.1 El método de Monte Carlo", titulo="Monte Carlo: el tablero de Galton simulado",
             codigo=r'''
import numpy as np
import matplotlib.pyplot as plt
from math import comb

rng = np.random.default_rng(1964)
filas, bolas = 12, 3000
casilla = rng.binomial(filas, 0.5, size=bolas)       # cada clavo: izquierda o derecha con p = 0,5
plt.figure(figsize=(10, 4.5))
plt.hist(casilla, bins=np.arange(-0.5, filas + 1.5), color="steelblue", ec="white", label="Simulación")
plt.plot(range(filas + 1), [bolas * comb(filas, k) / 2 ** filas for k in range(filas + 1)], "o-", color="firebrick", lw=2, label="Teoría (binomial)")
plt.xlabel("Casilla final")
plt.ylabel("Bolas")
plt.title("3.000 bolas que caen por 12 filas de clavos", fontweight="bold")
plt.legend()
plt.show()
''',
             ideas=["Simular muchas veces un proceso aleatorio permite estimar probabilidades sin fórmulas.",
                    "La simulación coincide con la teoría: es una forma de comprobar un cálculo."]),
        dict(ancla="2.4 El teorema central", titulo="Teorema central del límite", fig="tcl",
             ideas=["Aunque la variable sea asimétrica, la media de muestras grandes se distribuye casi como una normal.",
                    "Por eso los intervalos de confianza y las pruebas del Módulo 5 funcionan con muchas variables clínicas."]),
    ],
}


@figura(140, "punnett")
def _():
    fig, ax = lienzo(12, 5)
    ax.text(22, 92, "Padre portador (Aa)", ha="center", fontsize=15, color=AZUL, fontweight="bold")
    ax.text(3, 50, "Madre\nportadora\n(Aa)", ha="center", va="center", fontsize=15, color=ROJO, fontweight="bold")
    for j, a in enumerate("Aa"):
        ax.text(17 + j * 12, 80, a, ha="center", fontsize=20, color=AZUL, fontweight="bold")
    for i, b in enumerate("Aa"):
        ax.text(9, 62 - i * 26, b, ha="center", fontsize=20, color=ROJO, fontweight="bold")
        for j, a in enumerate("Aa"):
            g = "".join(sorted(a + b))
            col = "#F7D9D5" if g == "aa" else ("#FDEFD9" if g == "Aa" else "#D5EFDF")
            ax.add_patch(plt.Rectangle((11 + j * 12, 50 - i * 26), 12, 24, fc=col, ec=TINTA, lw=2))
            ax.text(17 + j * 12, 62 - i * 26, g, ha="center", va="center", fontsize=20, color=TINTA)
    for k, (t, c) in enumerate([("AA  sano no portador: 1/4", VERDE), ("Aa  portador sano: 2/4 = 1/2", NARANJA), ("aa  fibrosis quística: 1/4", ROJO)]):
        ax.text(48, 70 - k * 16, t, fontsize=18, color=c, fontweight="bold", va="center")
    return fig


@figura(140, "venn")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    xx, yy = np.meshgrid(np.linspace(0, 12, 480), np.linspace(0, 6, 240))
    A = (xx - 4.3) ** 2 + (yy - 3) ** 2 < 2.4 ** 2
    B = (xx - 7.0) ** 2 + (yy - 3) ** 2 < 2.4 ** 2
    img = np.full(A.shape + (4,), 0.0)
    img[A & ~B] = [0.27, 0.51, 0.71, 0.55]; img[B & ~A] = [0.85, 0.51, 0.0, 0.5]; img[A & B] = [0.75, 0.22, 0.17, 0.75]
    ax.imshow(img, extent=(0, 12, 0, 6), origin="lower")
    ax.text(3.2, 3, "Fumador", ha="center", fontsize=16, color=TINTA, fontweight="bold")
    ax.text(8.2, 3, "EPOC", ha="center", fontsize=16, color=TINTA, fontweight="bold")
    ax.text(5.65, 3, "A y B", ha="center", fontsize=14, color="white", fontweight="bold")
    ax.text(10.2, 5.2, "P(A o B) = P(A) + P(B) − P(A y B)", fontsize=15, color=TINTA, ha="center")
    ax.set_xlim(0, 13); ax.axis("off")
    return fig


@figura(140, "arbol")
def _():
    fig, ax = lienzo(12, 5.8)
    niveles = [[(8, 50)]]
    for n in range(1, 4):
        niveles.append([(8 + n * 22, 50 + (k - (2 ** n - 1) / 2) * 84 / 2 ** n) for k in range(2 ** n)])
    for n in range(1, 4):
        for k, (x, y) in enumerate(niveles[n]):
            px, py = niveles[n - 1][k // 2]
            af = k % 2 == 1
            ax.plot([px, x], [py, y], color=ROJO if af else AZUL, lw=2)
            ax.text((px + x) / 2, (py + y) / 2 + 1.5, "1/4" if af else "3/4", fontsize=11, color=ROJO if af else AZUL, ha="center")
    for k, (x, y) in enumerate(niveles[3]):
        n_af = bin(k).count("1")
        p = (1 / 4) ** n_af * (3 / 4) ** (3 - n_af)
        ax.text(x + 2, y, f"{n_af} afectado{'s' if n_af != 1 else ''}: {p * 64:.0f}/64", fontsize=12.5, va="center", color=TINTA if n_af else VERDE, fontweight="bold" if not n_af else "normal")
    ax.text(70, 96, "P(ninguno) = 27/64   →   P(al menos uno) = 37/64 ≈ 0,58", ha="center", fontsize=15, color=ROJO, fontweight="bold", va="top")
    return fig


def _arbol_frecuencias(ax, total, nombres, enf, sp, fp, etq_pos, etq_neg):
    caja(ax, 1, 42, 15, 16, f"{total:,}".replace(",", "."), tam=18, negrita=True)
    caja(ax, 30, 70, 18, 14, f"{enf} {nombres[0]}", tam=14, color=ROJO, relleno="#FBE5E1")
    caja(ax, 30, 16, 18, 14, f"{total - enf} {nombres[1]}", tam=14)
    flecha(ax, 17, 54, 29, 76); flecha(ax, 17, 46, 29, 24)
    vals = [(enf_p := round(enf * sp), "#FBE5E1", ROJO, 85), (enf - enf_p, "white", GRIS, 63), (fp_n := round((total - enf) * fp), "#FDEFD9", NARANJA, 31), (total - enf - fp_n, "white", GRIS, 9)]
    textos = [etq_pos + " (VP)", etq_neg + " (FN)", etq_pos + " (FP)", etq_neg + " (VN)"]
    for (v, rel, col, y), t in zip(vals, textos):
        caja(ax, 62, y, 20, 9, f"{v} {t}", tam=13, color=col, relleno=rel)
    for y0, ys in [(77, (89, 67)), (23, (35, 13))]:
        for y in ys:
            flecha(ax, 49, y0, 61, y)
    return vals[0][0], vals[2][0]


@figura(150, "arbol")
def _():
    fig, ax = lienzo(12, 5.8)
    vp, fp = _arbol_frecuencias(ax, 1000, ("con cáncer", "sin cáncer"), 10, 0.9, 0.09, "positivas", "negativas")
    ax.text(92, 55, f"VPP =\n{vp} / ({vp} + {fp})\n≈ {vp / (vp + fp):.0%}", ha="center", va="center", fontsize=17, color=ROJO, fontweight="bold")
    return fig


@figura(150, "condicionada")
def _():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4))
    for ax, (t, foco) in zip(axs, [("Todas las mujeres", False), ("Solo las que dan positivo", True)]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_aspect("equal")
        ax.add_patch(plt.Rectangle((0, 0), 10, 10, fc="white" if foco else AZUL_CLARO, ec=TINTA, lw=2, alpha=0.4 if foco else 1))
        ax.add_patch(plt.Rectangle((0, 0), 10, 2.2, fc="#FDEFD9", ec=NARANJA, lw=3 if foco else 1.5))
        ax.add_patch(plt.Rectangle((0, 0), 1.0, 2.2, fc=ROJO, ec=ROJO))
        ax.text(5.5, 1.1, "positivas (B)", ha="center", va="center", fontsize=14, color=TINTA)
        ax.text(1.3, 2.6, "← cáncer y positiva", ha="left", fontsize=11, color=ROJO)
        ax.set_title(t, fontsize=16)
    axs[1].text(5, 6.2, "P(cáncer | positiva)\n= área roja / área naranja\n≈ 9 %", ha="center", fontsize=15, color=TINTA)
    return fig


@figura(150, "iconos")
def _():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    n = 1000
    col = np.array([AZUL_CLARO] * n, dtype=object)
    col[:9] = ROJO; col[9] = TINTA; col[10:99] = NARANJA
    rng = np.random.default_rng(15)
    orden = rng.permutation(n)
    xs, ys = np.arange(n) % 50, np.arange(n) // 50
    ax.scatter(xs[orden], ys[orden], c=list(col), s=34)
    ax.set_xlim(-1, 75); ax.set_ylim(-1, 20); ax.axis("off"); ax.set_aspect("equal")
    for k, (t, c) in enumerate([("9 con cáncer y positivas", ROJO), ("1 con cáncer y negativa", TINTA), ("89 sin cáncer y positivas", NARANJA), ("901 sin cáncer y negativas", AZUL)]):
        ax.scatter([52], [17 - k * 3.2], c=c, s=120)
        ax.text(53.5, 17 - k * 3.2, t, va="center", fontsize=15, color=TINTA)
    ax.text(52, 2.5, "De 98 positivas,\nsolo 9 tienen cáncer", fontsize=16, color=ROJO, fontweight="bold")
    return fig


@figura(160, "corte")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    x = np.linspace(0, 9.5, 600)
    sano = np.exp(-(x - np.log(150)) ** 2 / 2) / np.sqrt(2 * np.pi)
    ic = np.exp(-(x - np.log(900)) ** 2 / 2) / np.sqrt(2 * np.pi)
    c = np.log(400)
    ax.plot(x, sano, color=AZUL, lw=2.5, label="Sin insuficiencia cardíaca")
    ax.plot(x, ic, color=ROJO, lw=2.5, label="Con insuficiencia cardíaca")
    ax.fill_between(x, 0, sano, where=x >= c, color=NARANJA, alpha=0.45, label="Falsos positivos")
    ax.fill_between(x, 0, ic, where=x < c, color=TINTA, alpha=0.35, label="Falsos negativos")
    ax.axvline(c, color=TINTA, lw=2.5, ls="--")
    ax.text(c + 0.1, 0.41, "corte: 400 pg/mL", fontsize=14)
    ticks = [10, 50, 150, 400, 900, 3000, 10000]
    ax.set_xticks(np.log(ticks), [str(t) for t in ticks]); ax.set_yticks([])
    ax.set_xlabel("NT-proBNP (pg/mL, escala logarítmica)")
    ax.legend(loc="upper left", fontsize=12)
    return fig


@figura(160, "tabla")
def _():
    fig, ax = lienzo(12, 5.5)
    ax.text(45, 92, "Enfermo", ha="center", fontsize=16, fontweight="bold", color=TINTA)
    ax.text(70, 92, "Sano", ha="center", fontsize=16, fontweight="bold", color=TINTA)
    ax.text(18, 69, "Prueba +", ha="center", fontsize=16, fontweight="bold", color=TINTA)
    ax.text(18, 44, "Prueba −", ha="center", fontsize=16, fontweight="bold", color=TINTA)
    for (x, y, t, c) in [(33, 60, "VP", "#D5EFDF"), (58, 60, "FP", "#FDEFD9"), (33, 35, "FN", "#F7D9D5"), (58, 35, "VN", "#D5EFDF")]:
        ax.add_patch(plt.Rectangle((x, y), 24, 22, fc=c, ec=TINTA, lw=2))
        ax.text(x + 12, y + 11, t, ha="center", va="center", fontsize=22, fontweight="bold", color=TINTA)
    ax.text(45, 24, "Sensibilidad =\nVP / (VP + FN)", ha="center", va="top", fontsize=14, color=AZUL)
    ax.text(70, 24, "Especificidad =\nVN / (VN + FP)", ha="center", va="top", fontsize=14, color=AZUL)
    ax.text(84, 71, "VPP = VP / (VP + FP)", fontsize=14, color=ROJO, va="center")
    ax.text(84, 46, "VPN = VN / (VN + FN)", fontsize=14, color=ROJO, va="center")
    ax.set_xlim(0, 115)
    return fig


@figura(160, "roc")
def _():
    fig, ax = plt.subplots(figsize=(7.5, 6))
    rng = np.random.default_rng(16)
    sano, enf = rng.normal(np.log(150), 1, 4000), rng.normal(np.log(900), 1, 4000)
    cortes = np.linspace(2, 10, 200)
    se = [(enf >= c).mean() for c in cortes]
    fpr = [(sano >= c).mean() for c in cortes]
    ax.plot(fpr, se, color=AZUL, lw=3)
    ax.fill_between(fpr, se, color=AZUL_CLARO, alpha=0.6)
    ax.plot([0, 1], [0, 1], "--", color=GRIS)
    for c, t in [(np.log(125), "125"), (np.log(400), "400"), (np.log(2000), "2000")]:
        s, f = (enf >= c).mean(), (sano >= c).mean()
        ax.plot(f, s, "o", ms=11, color=ROJO)
        ax.annotate(f"corte {t}", (f, s), xytext=(10, -18), textcoords="offset points", fontsize=13)
    ax.text(0.55, 0.3, "AUC ≈ 0,90", fontsize=17, color=AZUL, fontweight="bold")
    ax.text(0.55, 0.47, "azar (AUC = 0,5)", fontsize=12, color=GRIS, rotation=38)
    ax.set_xlabel("1 − especificidad (falsos positivos)"); ax.set_ylabel("Sensibilidad")
    return fig


@figura(170, "binomial")
def _():
    from scipy import stats
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    for ax, (n, p, t) in zip(axs, [(10, 0.3, "10 pacientes, p = 0,3"), (20, 0.7, "20 pacientes, p = 0,7"), (40, 0.82, "40 preguntas a una IA, p = 0,82")]):
        k = np.arange(n + 1)
        ax.bar(k, stats.binom.pmf(k, n, p), color=AZUL)
        ax.set_title(f"B({n}; {p:g})\n{t}", fontsize=14)
        ax.set_xlabel("Éxitos")
    axs[0].set_ylabel("Probabilidad")
    plt.tight_layout()
    return fig


@figura(170, "poisson")
def _():
    from scipy import stats
    fig, ax = plt.subplots(figsize=(12, 4.2))
    k = np.arange(0, 16)
    for desp, (lam, c) in zip([-0.27, 0, 0.27], [(1, AZUL), (3, NARANJA), (8, ROJO)]):
        ax.bar(k + desp, stats.poisson.pmf(k, lam), width=0.27, color=c, label=f"λ = {lam}")
    ax.set_xticks(k); ax.set_xlabel("Número de sucesos en el intervalo"); ax.set_ylabel("Probabilidad"); ax.legend()
    return fig


@figura(180, "intervalo")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    x = np.linspace(-4, 4, 500)
    y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(x, y, color=AZUL, lw=3)
    ax.fill_between(x, y, where=np.abs(x) <= 1.96, color=AZUL_CLARO)
    ax.fill_between(x, y, where=np.abs(x) > 1.96, color=ROJO, alpha=0.6)
    ax.text(0, 0.15, "95 % de los sanos\n(intervalo de referencia)", ha="center", fontsize=16, color=TINTA)
    for s in (-1, 1):
        ax.annotate("2,5 % de sanos\nmarcados en negrita", xy=(s * 2.4, 0.01), xytext=(s * 3.1, 0.17), ha="center", fontsize=13, color=ROJO,
                    arrowprops=dict(arrowstyle="->", color=ROJO))
    ax.set_xticks([-1.96, 0, 1.96], ["μ − 1,96σ", "μ", "μ + 1,96σ"]); ax.set_yticks([])
    ax.set_xlabel("Valor del parámetro en personas sanas")
    return fig


@figura(180, "regla")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    x = np.linspace(-4, 4, 500)
    y = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)
    for k, c, a in [(3, "#DCE8F3", 1), (2, "#9DC3E6", 1), (1, "#4682B4", 0.9)]:
        ax.fill_between(x, y, where=np.abs(x) <= k, color=c, alpha=a)
    ax.plot(x, y, color=TINTA, lw=2)
    for k, t, h in [(1, "68 %", 0.43), (2, "95 %", 0.50), (3, "99,7 %", 0.57)]:
        ax.annotate("", xy=(-k, h), xytext=(k, h), arrowprops=dict(arrowstyle="<->", lw=1.8, color=TINTA))
        ax.text(0, h + 0.008, t, ha="center", fontsize=15, color=TINTA, fontweight="bold")
    ax.set_xticks(range(-3, 4), ["μ−3σ", "μ−2σ", "μ−σ", "μ", "μ+σ", "μ+2σ", "μ+3σ"]); ax.set_yticks([]); ax.set_ylim(0, 0.63)
    return fig


@figura(180, "z")
def _():
    fig, ax = lienzo(12, 3.8)
    for y, etq, vals in [(70, "Hemoglobina (g/dL)\nμ = 13,5; σ = 1", ["10,5", "11,5", "12,5", "13,5", "14,5", "15,5", "16,5"]), (25, "z", ["−3", "−2", "−1", "0", "1", "2", "3"])]:
        ax.plot([30, 98], [y, y], color=TINTA, lw=2)
        ax.text(1, y, etq, va="center", fontsize=15, color=TINTA, fontweight="bold")
        for k, v in enumerate(vals):
            x = 32 + k * 10.8
            ax.plot([x, x], [y - 3, y + 3], color=TINTA, lw=2)
            ax.text(x, y + 6 if y > 50 else y - 10, v, ha="center", fontsize=14, color=TINTA)
    flecha(ax, 42.8, 66, 42.8, 30, color=ROJO)
    ax.text(45, 48, "Hb 11,5 → z = (11,5 − 13,5) / 1 = −2", fontsize=15, color=ROJO, fontweight="bold")
    return fig


@figura(180, "veinte")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    k = np.arange(1, 41)
    p = 1 - 0.95 ** k
    ax.plot(k, p, color=AZUL, lw=3)
    ax.plot(20, 1 - 0.95 ** 20, "o", ms=13, color=ROJO)
    ax.annotate(f"20 parámetros: {1 - 0.95 ** 20:.0%}", (20, 1 - 0.95 ** 20), xytext=(24, 0.45), fontsize=16, color=ROJO, arrowprops=dict(arrowstyle="->", color=ROJO, lw=2))
    ax.set_xlabel("Parámetros analizados en una persona sana"); ax.set_ylabel("P(al menos uno fuera de rango)")
    ax.set_ylim(0, 1)
    return fig


@figura(190, "tcl")
def _():
    rng = np.random.default_rng(19)
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.6))
    pob = rng.lognormal(1.8, 0.7, 100000)
    axs[0].hist(pob[pob < 40], bins=60, color=GRIS)
    axs[0].set_title("Población (asimétrica)", fontsize=14)
    for ax, n in zip(axs[1:], [2, 10, 30]):
        m = rng.choice(pob, (5000, n)).mean(axis=1)
        ax.hist(m, bins=50, color=AZUL)
        ax.set_title(f"Medias de muestras de n = {n}", fontsize=14)
    for ax in axs:
        ax.set_yticks([])
    plt.tight_layout()
    return fig
