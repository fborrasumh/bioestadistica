"""Diagramas de los apartados conceptuales 2.x que no tenían figura.
Cada uno se guarda en ../figuras/tema_XXX_<nombre>.png y se inserta con Cuaderno.diagrama(alt, nombre=...)."""
import math
import os

import numpy as np
import pandas as pd
from scipy import stats

from .diagramas import BLANCO, si_no
from .estilo import AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt, titulo

DATOS = os.path.join(os.path.dirname(__file__), "..", "..", "datos")
EXTRA = [(10, "e2_1"), (10, "e2_4"), (20, "e2_1"), (40, "e2_3"), (50, "e2_2"), (80, "e2_2"), (90, "e2_2"),
         (90, "e2_5"), (110, "e2_2"), (140, "e2_1"), (150, "e2_2"), (150, "e2_3"), (150, "e2_5"), (160, "e2_2"),
         (170, "e2_1"), (180, "e2_1"), (190, "e2_1"), (190, "e2_2"), (200, "e2_1"), (200, "e2_2"), (210, "e2_2"),
         (220, "e2_1"), (220, "e2_2"), (230, "e2_1"), (240, "e2_1"), (250, "e2_2"), (250, "e2_5"), (260, "e2_1"),
         (270, "e2_2"), (270, "e2_3"), (290, "e2_1"), (290, "e2_4"), (300, "e2_3")]


def cohorte():
    return pd.read_csv(os.path.join(DATOS, "cohorte_limpia.csv"))


def coma(x, d=1):
    return f"{x:.{d}f}".replace(".", ",").replace("-", "−")


def sin_ejes(ax):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)


@figura(10, "e2_1")
def _():
    from matplotlib.patches import Circle
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "Medicina basada en la evidencia: tres fuentes")
    for (x, y), texto, col in [((40, 52), "Mejor evidencia\ncientífica", AZUL), ((60, 52), "Experiencia\nclínica", NARANJA),
                              ((50, 34), "Valores del\npaciente", VERDE)]:
        ax.add_patch(Circle((x, y), 17, fc=col, alpha=0.18, ec=col, lw=2))
    ax.text(36, 72, "Mejor evidencia\ncientífica", ha="center", fontsize=13, color=AZUL, fontweight="bold")
    ax.text(70, 72, "Experiencia\nclínica", ha="center", fontsize=13, color=NARANJA, fontweight="bold")
    ax.text(50, 6, "Valores del paciente", ha="center", fontsize=13, color=VERDE, fontweight="bold")
    ax.text(50, 46, "Decisión", ha="center", fontsize=13, fontweight="bold", color=TINTA)
    for i, t in enumerate(["Describir", "Medir la incertidumbre", "Generalizar"]):
        caja(ax, 0, 66 - i * 16, 17, 11, t, tam=11, relleno=BLANCO)
        flecha(ax, 17, 71 - i * 16, 24, 52, color=GRIS)
    ax.text(8.5, 14, "Lo que aporta la\nbioestadística", ha="center", fontsize=12, color=GRIS)
    return fig


@figura(10, "e2_4")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Hoja de cálculo o código: tres ventajas del código")
    filas = [("Reproducibilidad", "Clics que nadie registra", "Mismo código → mismo resultado"),
             ("Escalabilidad", "Cómoda con 30 pacientes", "Igual con 30 que con 300.000"),
             ("Trazabilidad", "Cálculos ocultos en celdas", "Cada paso escrito, como un protocolo")]
    ax.text(48, 82, "Hoja de cálculo", ha="center", fontsize=14, fontweight="bold", color=NARANJA)
    ax.text(81, 82, "Código", ha="center", fontsize=14, fontweight="bold", color=VERDE)
    for i, (v, h, c) in enumerate(filas):
        y = 60 - i * 22
        caja(ax, 1, y, 24, 16, v, tam=13, negrita=True)
        caja(ax, 31, y, 34, 16, h, tam=12, relleno=BLANCO, color=NARANJA)
        caja(ax, 66, y, 33, 16, c, tam=12, relleno=BLANCO, color=VERDE)
    return fig


@figura(20, "e2_1")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "¿Qué tipo de dato es?")
    tipos = [("int", "72", "edad, ingresos", AZUL), ("float", "81.5", "peso, glucemia", AZUL), ("str", '"varón"', "sexo, diagnóstico", NARANJA),
             ("bool", "True", "diabetes sí/no", VERDE), ("None", "None", "dato ausente", ROJO)]
    caja(ax, 35, 70, 30, 12, "Valor clínico", tam=15, negrita=True)
    for i, (t, ej, var, col) in enumerate(tipos):
        x = 1 + i * 20
        caja(ax, x, 32, 18, 24, f"{t}\n{ej}\n{var}", tam=12, color=col, relleno=BLANCO)
        flecha(ax, 50, 70, x + 9, 56, color=GRIS)
    caja(ax, 58, 4, 41, 16, "FEVI no medida → None\nFEVI = 0 % → paciente sin latido", tam=12, color=ROJO, relleno=BLANCO)
    ax.text(28, 12, "El dato ausente no es un cero", ha="center", fontsize=14, color=ROJO, fontweight="bold")
    return fig


@figura(40, "e2_3")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "while: repetir mientras la concentración ≥ 10 mg/L")
    caja(ax, 1, 56, 22, 18, "c = 100\nvidas = 0", tam=13, relleno=BLANCO)
    caja(ax, 30, 54, 24, 22, "¿c ≥ 10?", tam=15)
    caja(ax, 62, 56, 30, 18, "c = c / 2\nvidas += 1", tam=13)
    caja(ax, 30, 14, 24, 18, "Fin del bucle", tam=13, color=VERDE, relleno=BLANCO)
    flecha(ax, 23, 65, 30, 65)
    flecha(ax, 54, 65, 62, 65)
    si_no(ax, 58, 70, "Sí", VERDE)
    ax.text(77, 50, "↺ vuelve a comprobar", ha="center", fontsize=12, color=GRIS)
    flecha(ax, 42, 54, 42, 32)
    si_no(ax, 46, 43, "No", ROJO)
    c, vidas, traza = 100.0, 0, ["100"]
    while c >= 10:
        c, vidas = c / 2, vidas + 1
        traza.append(f"{c:g}".replace(".", ","))
    ax.text(78, 38, " → ".join(traza), ha="center", fontsize=12, color=TINTA)
    ax.text(78, 28, f"{vidas} vidas medias", ha="center", fontsize=14, color=VERDE, fontweight="bold")
    ax.text(78, 12, "Algo debe cambiar dentro del bucle;\nsi no, no termina nunca", ha="center", fontsize=12, color=ROJO)
    return fig


@figura(50, "e2_2")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Una función: una sola fuente de verdad")
    caja(ax, 34, 58, 32, 20, "def cha2ds2_vasc(...):\n    ...\n    return puntos", tam=13)
    for i, t in enumerate(["Consulta", "Informe de alta", "Prueba con casos\nconocidos"]):
        x = 4 + i * 33
        caja(ax, x, 12, 26, 18, t, tam=13, relleno=BLANCO, color=VERDE)
        flecha(ax, 50, 58, x + 13, 30, color=GRIS)
    ax.text(86, 72, "Si la fórmula cambia,\nse corrige aquí\ny vale en todos", ha="center", fontsize=12, color=NARANJA)
    return fig


@figura(80, "e2_2")
def _():
    tokens = ["neumonía", "bronquitis", "asma", "gripe", "COVID-19"]
    logits = np.array([3.0, 2.0, 1.2, 0.8, 0.3])
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for ax, T in zip(axs, [0.2, 1.0, 2.0]):
        p = np.exp(logits / T) / np.exp(logits / T).sum()
        ax.bar(tokens, p, color=[NARANJA] + [AZUL] * 4)
        ax.set_title(f"Temperatura {coma(T)}", fontsize=15, fontweight="bold")
        ax.tick_params(axis="x", rotation=35)
        for i, v in enumerate(p):
            ax.text(i, v + 0.02, f"{v * 100:.0f} %", ha="center", fontsize=11)
        sin_ejes(ax)
    axs[0].set_ylabel("Probabilidad del siguiente token")
    axs[0].set_ylim(0, 1.08)
    fig.suptitle("La misma pregunta: con más temperatura, los tokens poco probables ganan peso", fontsize=15, fontweight="bold")
    fig.tight_layout()
    return fig


@figura(90, "e2_2")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Desarrollo guiado por pruebas: el orden importa")
    pasos = [("1. Especificación", "qué recibe, qué\ndevuelve, reglas"), ("2. Casos de prueba", "de fuentes fiables,\nsin ver código"),
             ("3. Pedir el código", "al asistente"), ("4. Ejecutar\nlas pruebas", "¿todas superadas?")]
    for i, (t, s) in enumerate(pasos):
        x = 1 + i * 25
        caja(ax, x, 48, 22, 28, f"{t}\n\n{s}", tam=12, color=VERDE if i < 2 else AZUL, relleno=BLANCO if i < 2 else AZUL_CLARO)
        if i < 3:
            flecha(ax, x + 22, 62, x + 25, 62)
    flecha(ax, 62, 46, 37, 46, curva=-0.5, color=ROJO)
    ax.text(50, 18, "✗ Escribir las pruebas después de ver el código:\nse escriben pruebas que ese código ya supera", ha="center",
            fontsize=13, color=ROJO)
    return fig


@figura(90, "e2_5")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Antes de ejecutar código generado por IA")
    pasos = ["Léelo,\naunque sea\npor encima", "Entorno\naislado\n(Colab)", "Sin acceso a\nficheros, red o\nDrive si no hace falta",
             "Sin datos\nde pacientes", "Ejecuta"]
    for i, t in enumerate(pasos):
        x = 1 + i * 20
        ultimo = i == len(pasos) - 1
        caja(ax, x, 38, 17, 32, t, tam=12, color=VERDE if ultimo else AZUL, relleno=BLANCO if ultimo else AZUL_CLARO,
             negrita=ultimo)
        if not ultimo:
            flecha(ax, x + 17, 54, x + 20, 54)
    ax.text(50, 14, "Ejecutar código generado es ejecutar código de un desconocido", ha="center", fontsize=14, color=ROJO)
    return fig


@figura(110, "e2_2")
def _():
    c = cohorte()
    etiquetas = ["Bajo peso", "Normopeso", "Sobrepeso", "Obesidad"]
    cat = pd.cut(c["imc"], [0, 18.5, 25, 30, 100], right=False, labels=etiquetas)
    n = cat.value_counts().reindex(etiquetas)
    acum = n.cumsum() / n.sum() * 100
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.bar(etiquetas, n, color=AZUL, alpha=0.85)
    for i, v in enumerate(n):
        ax.text(i, v + 3, f"n = {v}\n{v / n.sum() * 100:.1f} %".replace(".", ","), ha="center", fontsize=12)
    ax.set_ylabel("Frecuencia absoluta (pacientes)")
    ax.set_ylim(0, n.max() * 1.35)
    ax2 = ax.twinx()
    ax2.plot(etiquetas, acum, "o-", color=NARANJA, lw=2.5)
    for i, v in enumerate(acum):
        ax2.text(i + 0.12, v + 3, f"{v:.0f} %", ha="left", color=NARANJA, fontsize=12, fontweight="bold",
                 bbox=dict(fc="white", ec="none", pad=1))
    ax2.set_ylim(0, 110)
    ax2.set_ylabel("Frecuencia acumulada (%)", color=NARANJA)
    ax.set_title(f"IMC en la cohorte (n = {n.sum()} con IMC registrado): la acumulada solo tiene sentido si hay orden",
                 fontweight="bold", fontsize=14)
    return fig


@figura(140, "e2_1")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "Espacio muestral: hijo de dos portadores (Aa × Aa)")
    ax.text(40, 78, "A (madre)", ha="center", fontsize=14, fontweight="bold")
    ax.text(60, 78, "a (madre)", ha="center", fontsize=14, fontweight="bold")
    ax.text(22, 60, "A (padre)", ha="center", fontsize=14, fontweight="bold")
    ax.text(22, 36, "a (padre)", ha="center", fontsize=14, fontweight="bold")
    celdas = [("AA", 30, 50, VERDE), ("Aa", 50, 50, NARANJA), ("aA", 30, 26, NARANJA), ("aa", 50, 26, ROJO)]
    for g, x, y, col in celdas:
        caja(ax, x, y, 18, 20, g, tam=18, negrita=True, color=col, relleno=BLANCO)
    ax.text(72, 66, "Ω = {AA, Aa, aA, aa}", fontsize=13)
    ax.text(72, 54, "Enfermo = {aa} → 1/4", fontsize=13, color=ROJO)
    ax.text(72, 42, "Portador sano = {Aa, aA} → 2/4", fontsize=13, color=NARANJA)
    ax.text(72, 26, "No enfermo (complementario)\n= {AA, Aa, aA} → 3/4", fontsize=13, color=VERDE)
    return fig


@figura(150, "e2_2")
def _():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax, (tit, pa_b, pa_nb) in zip(axs, [("Independientes: P(A | B) = P(A | no B)", 0.3, 0.3),
                                            ("Dependientes: saber B cambia P(A)", 0.6, 0.15)]):
        pb = 0.4
        ax.add_patch(plt.Rectangle((0, 0), pb, pa_b, fc=NARANJA, alpha=0.8))
        ax.add_patch(plt.Rectangle((0, pa_b), pb, 1 - pa_b, fc=AZUL_CLARO))
        ax.add_patch(plt.Rectangle((pb, 0), 1 - pb, pa_nb, fc=NARANJA, alpha=0.5))
        ax.add_patch(plt.Rectangle((pb, pa_nb), 1 - pb, 1 - pa_nb, fc="#EEF3F8"))
        ax.axvline(pb, color="white", lw=3)
        ax.text(pb / 2, -0.08, "B", ha="center", fontsize=14, fontweight="bold")
        ax.text(pb + (1 - pb) / 2, -0.08, "no B", ha="center", fontsize=14, fontweight="bold")
        ax.text(pb / 2, pa_b / 2, f"A\n{pa_b:.0%}".replace("%", " %"), ha="center", va="center", fontsize=13, color="white", fontweight="bold")
        ax.text(pb + (1 - pb) / 2, pa_nb / 2, f"A\n{pa_nb:.0%}".replace("%", " %"), ha="center", va="center", fontsize=13,
                color=TINTA, fontweight="bold")
        ax.set_xlim(0, 1), ax.set_ylim(-0.15, 1), ax.axis("off")
        ax.set_title(tit, fontsize=14, fontweight="bold")
    fig.suptitle("La parte naranja es A. ¿Ocupa la misma proporción en B y en no B?", fontsize=15)
    fig.tight_layout()
    return fig


@figura(150, "e2_3")
def _():
    pe, se, fp = 0.01, 0.90, 0.09
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "Árbol de probabilidades: mamografía de cribado")
    caja(ax, 1, 42, 14, 14, "Mujer\ncribada", tam=13)
    caja(ax, 28, 66, 16, 13, f"Enferma\n{pe:.0%}".replace("%", " %"), tam=12, color=ROJO, relleno=BLANCO)
    caja(ax, 28, 18, 16, 13, f"Sana\n{1 - pe:.0%}".replace("%", " %"), tam=12, color=VERDE, relleno=BLANCO)
    flecha(ax, 15, 49, 28, 72)
    flecha(ax, 15, 49, 28, 25)
    ramas = [(72, se, "+", True, pe * se), (72, 1 - se, "−", False, pe * (1 - se)),
             (25, fp, "+", True, (1 - pe) * fp), (25, 1 - fp, "−", False, (1 - pe) * (1 - fp))]
    for i, (y0, p, s, pos, conj) in enumerate(ramas):
        y = y0 + (9 if i % 2 == 0 else -9)
        flecha(ax, 44, y0, 56, y, color=NARANJA if pos else GRIS, texto=coma(p, 2))
        caja(ax, 56, y - 5, 10, 10, s, tam=15, negrita=True, color=NARANJA if pos else GRIS, relleno=BLANCO)
        ax.text(71, y, coma(conj, 4), va="center", fontsize=13, color=NARANJA if pos else GRIS,
                fontweight="bold" if pos else "normal")
    p_pos = pe * se + (1 - pe) * fp
    ax.text(90, 60, f"P(+) = {coma(pe * se, 4)}\n+ {coma((1 - pe) * fp, 4)}\n= {coma(p_pos, 4)}", ha="center", fontsize=12,
            color=TINTA)
    ax.text(90, 30, f"P(E | +) =\n{coma(pe * se, 4)} / {coma(p_pos, 4)}\n= {pe * se / p_pos * 100:.1f} %".replace(".", ","),
            ha="center", fontsize=13, color=ROJO, fontweight="bold")
    return fig


@figura(150, "e2_5")
def _():
    pre = np.linspace(0.001, 0.999, 400)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    for lr, col in [(10, ROJO), (2, NARANJA), (1, GRIS), (0.5, AZUL), (0.1, VERDE)]:
        o = pre / (1 - pre) * lr
        ax.plot(pre * 100, o / (1 + o) * 100, color=col, lw=2.5, label=f"LR = {coma(lr, 1).replace(',0', '')}")
    ax.set_xlabel("Probabilidad preprueba (%)")
    ax.set_ylabel("Probabilidad posprueba (%)")
    ax.set_title("odds posprueba = odds preprueba × LR: un LR cercano a 1 apenas cambia nada", fontweight="bold")
    ax.legend(frameon=False, fontsize=12)
    sin_ejes(ax)
    return fig


@figura(160, "e2_2")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "De qué casillas sale cada índice")
    ax.text(42, 76, "Enfermo", ha="center", fontsize=14, fontweight="bold")
    ax.text(62, 76, "Sano", ha="center", fontsize=14, fontweight="bold")
    ax.text(24, 58, "Prueba +", ha="center", fontsize=14, fontweight="bold")
    ax.text(24, 36, "Prueba −", ha="center", fontsize=14, fontweight="bold")
    for t, x, y in [("VP", 33, 50), ("FP", 53, 50), ("FN", 33, 28), ("VN", 53, 28)]:
        caja(ax, x, y, 18, 18, t, tam=17, negrita=True, relleno=BLANCO)
    ax.add_patch(plt.Rectangle((32, 26), 20, 44, fill=False, ec=AZUL, lw=3, ls="--"))
    ax.add_patch(plt.Rectangle((52, 26), 20, 44, fill=False, ec=AZUL, lw=3, ls="--"))
    ax.text(42, 13, "Sensibilidad\nVP / (VP + FN)", ha="center", fontsize=12, color=AZUL)
    ax.text(62, 13, "Especificidad\nVN / (VN + FP)", ha="center", fontsize=12, color=AZUL)
    ax.add_patch(plt.Rectangle((31, 49), 42, 20, fill=False, ec=NARANJA, lw=3))
    ax.add_patch(plt.Rectangle((31, 27), 42, 20, fill=False, ec=NARANJA, lw=3))
    ax.text(88, 59, "VPP\nVP / (VP + FP)", ha="center", fontsize=12, color=NARANJA)
    ax.text(88, 37, "VPN\nVN / (VN + FN)", ha="center", fontsize=12, color=NARANJA)
    ax.text(50, 4, "En columna: propiedades de la prueba (no dependen de la prevalencia).   En fila: lo que importa al paciente (sí dependen).",
            ha="center", fontsize=11, color=TINTA)
    return fig


@figura(170, "e2_1")
def _():
    X = stats.binom(3, 0.25)
    k = np.arange(0, 4)
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4))
    axs[0].bar(k, X.pmf(k), color=AZUL)
    for i in k:
        axs[0].text(i, X.pmf(i) + 0.01, coma(X.pmf(i), 3), ha="center", fontsize=12)
    axs[0].set_title("Función de probabilidad P(X = k)", fontweight="bold")
    axs[1].step(np.r_[-0.5, k, 3.5], np.r_[0, X.cdf(k), 1], where="post", color=NARANJA, lw=2.5)
    axs[1].set_ylim(0, 1.08)
    axs[1].set_title("Función de distribución F(k) = P(X ≤ k)", fontweight="bold")
    for ax in axs:
        ax.set_xticks(k)
        ax.set_xlabel("Hijos enfermos de 3 (padres portadores)")
        sin_ejes(ax)
    fig.suptitle(f"X ~ B(3; 0,25): E(X) = {coma(X.mean(), 2)} hijos, Var(X) = {coma(X.var(), 4)}", fontsize=15)
    fig.tight_layout()
    return fig


@figura(180, "e2_1")
def _():
    X = stats.norm(130, 15)
    x = np.linspace(80, 180, 400)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.plot(x, X.pdf(x), color=AZUL, lw=2.5)
    z = x[(x >= 120) & (x <= 140)]
    ax.fill_between(z, X.pdf(z), color=NARANJA, alpha=0.7)
    p = X.cdf(140) - X.cdf(120)
    ax.text(130, X.pdf(130) * 0.45, f"P(120 ≤ PAS ≤ 140)\n= área = {coma(p, 3)}", ha="center", fontsize=13, fontweight="bold")
    ax.axvline(150, color=ROJO, ls=":")
    ax.text(151, X.pdf(130) * 0.8, "P(PAS = 150 exacto) = 0:\nuna línea no tiene área", fontsize=12, color=ROJO)
    ax.set_xlabel("Presión arterial sistólica (mmHg), modelo N(130; 15)")
    ax.set_ylabel("Densidad f(x)")
    ax.set_title("En una variable continua, la probabilidad es un área bajo la curva (área total = 1)", fontweight="bold")
    sin_ejes(ax)
    return fig


@figura(190, "e2_1")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "El método de Monte Carlo")
    pasos = ["Modelo de\nla población", "Simular una\nmuestra al azar", "Calcular el\nestadístico\n(p. ej., la media)", "Guardarlo"]
    for i, t in enumerate(pasos):
        x = 1 + i * 22
        caja(ax, x, 50, 19, 26, t, tam=12)
        if i < 3:
            flecha(ax, x + 19, 63, x + 22, 63)
    flecha(ax, 76, 50, 34, 50, curva=-0.35)
    ax.text(55, 20, "repetir miles de veces", ha="center", fontsize=13, color=GRIS)
    caja(ax, 88, 50, 11, 26, "Distri-\nbución\nde los\nresultados", tam=11, color=VERDE, relleno=BLANCO)
    flecha(ax, 85, 63, 88, 63)
    ax.text(50, 8, "Permite algo imposible en la realidad: extraer miles de muestras de la misma población", ha="center",
            fontsize=13, color=TINTA)
    return fig


@figura(190, "e2_2")
def _():
    rng = np.random.default_rng(1902)
    pobl = rng.lognormal(math.log(100), 0.25, 50_000)
    fig, axs = plt.subplots(1, 3, figsize=(13, 4))
    axs[0].hist(pobl, bins=60, color=AZUL, alpha=0.8)
    axs[0].set_title(f"Población\nσ = {coma(pobl.std())}", fontsize=14, fontweight="bold")
    m = rng.choice(pobl, 30)
    axs[1].hist(m, bins=12, color=NARANJA, alpha=0.8)
    axs[1].set_title(f"Una muestra (n = 30)\ns = {coma(m.std(ddof=1))}", fontsize=14, fontweight="bold")
    medias = rng.choice(pobl, (5000, 30)).mean(1)
    axs[2].hist(medias, bins=50, color=VERDE, alpha=0.8)
    axs[2].set_title(f"Distribución muestral de la media\nEE = {coma(medias.std())} ≈ σ/√30 = {coma(pobl.std() / math.sqrt(30))}",
                     fontsize=14, fontweight="bold")
    for ax in axs:
        ax.set_xlim(40, 200)
        ax.set_yticks([])
        ax.set_xlabel("Glucemia (mg/dL)")
        sin_ejes(ax)
    fig.tight_layout()
    return fig


@figura(200, "e2_1")
def _():
    rng = np.random.default_rng(200)
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
    casos = [("Insesgado y eficiente", 0, 0.12, VERDE), ("Insesgado, poco eficiente", 0, 0.4, NARANJA),
             ("Sesgado y eficiente", 0.45, 0.12, NARANJA), ("Sesgado, poco eficiente", 0.45, 0.4, ROJO)]
    for ax, (t, sesgo, de, col) in zip(axs, casos):
        for r in (1, 0.66, 0.33):
            ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=GRIS, lw=1.5))
        p = rng.normal([sesgo, sesgo * 0.6], de, (25, 2))
        ax.plot(p[:, 0], p[:, 1], "o", color=col, ms=6)
        ax.plot(0, 0, "+", color=TINTA, ms=16, mew=3)
        ax.set_xlim(-1.1, 1.1), ax.set_ylim(-1.1, 1.1), ax.set_aspect("equal"), ax.axis("off")
        ax.set_title(t, fontsize=13, fontweight="bold", color=col)
    fig.suptitle("El centro (+) es el parámetro; cada punto, la estimación de una muestra distinta", fontsize=15)
    fig.tight_layout()
    return fig


@figura(200, "e2_2")
def _():
    x = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.plot(x, stats.norm.pdf(x), color=AZUL, lw=2.5, label="Normal: ±1,96")
    t9 = stats.t.ppf(0.975, 9)
    ax.plot(x, stats.t.pdf(x, 9), color=NARANJA, lw=2.5, label=f"t de Student, 9 gl (n = 10): ±{coma(t9, 2)}")
    for v, col in [(1.96, AZUL), (t9, NARANJA)]:
        for s in (-1, 1):
            ax.axvline(s * v, color=col, ls="--", lw=1.5)
    ax.set_title("Sin σ, la t tiene colas más gruesas y el intervalo es más ancho", fontweight="bold")
    ax.set_yticks([])
    ax.legend(frameon=False, fontsize=12)
    sin_ejes(ax)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: coma(v, 0)))
    return fig


@figura(210, "e2_2")
def _():
    z_obs = 2.1
    x = np.linspace(-4, 4, 400)
    p = 2 * stats.norm.sf(z_obs)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.plot(x, stats.norm.pdf(x), color=AZUL, lw=2.5)
    for s in (-1, 1):
        cola = x[s * x >= z_obs]
        ax.fill_between(cola, stats.norm.pdf(cola), color=NARANJA, alpha=0.8)
    ax.axvline(z_obs, color=TINTA, lw=2)
    ax.text(z_obs + 0.1, 0.25, f"resultado\nobservado\nz = {coma(z_obs)}", fontsize=12)
    ax.text(0, 0.06, f"valor p = suma de las dos colas = {coma(p, 3)}", ha="center", fontsize=14, fontweight="bold", color=NARANJA)
    ax.set_title("La curva es lo que se esperaría SI H₀ FUERA CIERTA", fontweight="bold")
    ax.set_yticks([])
    ax.set_xlabel("Estadístico de contraste")
    sin_ejes(ax)
    return fig


@figura(220, "e2_1")
def _():
    c = cohorte()
    f = c["fumador"].dropna()
    n, x = len(f), int((f == "Sí").sum())
    p0 = 0.22
    k = np.arange(int(n * 0.1), int(n * 0.34))
    pmf = stats.binom.pmf(k, n, p0)
    esperado = n * p0
    extremo = np.abs(k - esperado) >= abs(x - esperado)
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.bar(k, pmf, color=np.where(extremo, NARANJA, AZUL_CLARO), width=1)
    ax.axvline(x, color=TINTA, lw=2)
    ax.text(x + 1, pmf.max() * 0.9, f"observados:\n{x} fumadores de {n}", fontsize=12)
    p = stats.binomtest(x, n, p0).pvalue
    ax.set_title(f"Si H₀ es cierta, los fumadores siguen B({n}; 0,22). Naranja: tan extremos o más (p = {coma(p, 3)})",
                 fontweight="bold", fontsize=13)
    ax.set_xlabel("Número de fumadores en la cohorte")
    ax.set_yticks([])
    sin_ejes(ax)
    return fig


@figura(220, "e2_2")
def _():
    c = cohorte().dropna(subset=["fumador", "sexo"])
    fig, ax = plt.subplots(figsize=(12, 4))
    res = {}
    for i, s in enumerate(["Hombre", "Mujer"]):
        g = c[c["sexo"] == s]["fumador"] == "Sí"
        p, n = g.mean(), len(g)
        ee = math.sqrt(p * (1 - p) / n)
        res[s] = (p, n)
        ax.errorbar(p * 100, i + 1, xerr=1.96 * ee * 100, fmt="o", color=AZUL, ms=10, capsize=6, lw=2)
        ax.text(p * 100, i + 1.25, f"{s}: {p * 100:.0f} % (n = {n})", ha="center", fontsize=12)
    (p1, n1), (p2, n2) = res["Hombre"], res["Mujer"]
    d = p1 - p2
    ee_d = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ax.errorbar(d * 100, 0, xerr=1.96 * ee_d * 100, fmt="s", color=NARANJA, ms=10, capsize=6, lw=2)
    ax.text(d * 100, 0.25, f"Diferencia: {coma(d * 100)} puntos (IC 95 % {coma((d - 1.96 * ee_d) * 100)} a {coma((d + 1.96 * ee_d) * 100)})",
            ha="center", fontsize=12, color=NARANJA)
    ax.axvline(0, color=GRIS, ls=":")
    ax.set_yticks([0, 1, 2], ["Diferencia", "Hombres", "Mujeres"])
    ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("Fumadores (%)")
    ax.set_title("Dos proporciones independientes: lo importante es la diferencia y su IC", fontweight="bold")
    sin_ejes(ax)
    return fig


@figura(230, "e2_1")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "Tabla 2 × 2: el riesgo se lee por filas; las odds, dentro de cada fila")
    ax.text(40, 76, "Evento sí", ha="center", fontsize=14, fontweight="bold")
    ax.text(60, 76, "Evento no", ha="center", fontsize=14, fontweight="bold")
    ax.text(16, 58, "Expuestos", ha="center", fontsize=14, fontweight="bold")
    ax.text(16, 34, "No expuestos", ha="center", fontsize=14, fontweight="bold")
    for t, x, y in [("a", 31, 50), ("b", 51, 50), ("c", 31, 26), ("d", 51, 26)]:
        caja(ax, x, y, 18, 18, t, tam=18, negrita=True, relleno=BLANCO)
    ax.text(84, 63, "R₁ = a / (a + b)\nodds₁ = a / b", ha="center", fontsize=13, color=AZUL)
    ax.text(84, 39, "R₀ = c / (c + d)\nodds₀ = c / d", ha="center", fontsize=13, color=AZUL)
    ax.text(50, 10, "RR = R₁ / R₀        OR = odds₁ / odds₀ = (a·d) / (b·c)", ha="center", fontsize=15, color=NARANJA,
            fontweight="bold")
    return fig


@figura(240, "e2_1")
def _():
    rng = np.random.default_rng(240)
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4))
    a = rng.normal(150, 15, 10)
    axs[0].plot(np.zeros(10) + rng.uniform(-0.08, 0.08, 10), a, "o", color=AZUL, ms=9)
    axs[0].plot(np.ones(10) + rng.uniform(-0.08, 0.08, 10), rng.normal(142, 15, 10), "o", color=NARANJA, ms=9)
    axs[0].set_title("Independientes: dos grupos de pacientes distintos", fontweight="bold", fontsize=13)
    antes = rng.normal(150, 15, 10)
    despues = antes - rng.normal(8, 4, 10)
    for i in range(10):
        axs[1].plot([0, 1], [antes[i], despues[i]], "-", color=GRIS, lw=1.5)
    axs[1].plot(np.zeros(10), antes, "o", color=AZUL, ms=9)
    axs[1].plot(np.ones(10), despues, "o", color=NARANJA, ms=9)
    axs[1].set_title("Apareados: cada línea une al mismo paciente", fontweight="bold", fontsize=13)
    for ax in axs:
        ax.set_xticks([0, 1], ["Antes / grupo A", "Después / grupo B"])
        ax.set_xlim(-0.4, 1.4)
        ax.set_ylabel("PAS (mmHg)")
        sin_ejes(ax)
    fig.suptitle("En el diseño apareado cada paciente se compara consigo mismo", fontsize=15)
    fig.tight_layout()
    return fig


@figura(250, "e2_2")
def _():
    rng = np.random.default_rng(250)
    rep, n1, n2 = 4000, 10, 40
    clas = welch = 0
    for _ in range(rep):
        a, b = rng.normal(0, 20, n1), rng.normal(0, 5, n2)
        clas += stats.ttest_ind(a, b, equal_var=True).pvalue < 0.05
        welch += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05
    fig, ax = plt.subplots(figsize=(12, 4.2))
    v = [clas / rep * 100, welch / rep * 100]
    ax.barh(["t clásica", "t de Welch"], v, color=[ROJO, VERDE])
    for i, x in enumerate(v):
        ax.text(x + 0.5, i, f"{coma(x)} %", va="center", fontsize=14, fontweight="bold")
    ax.axvline(5, color=TINTA, ls="--")
    ax.text(5.3, 1.35, "nominal 5 %", fontsize=12)
    ax.set_xlabel("Falsos positivos con medias iguales (%)")
    ax.set_title(f"Simulación: grupo pequeño muy variable (n = {n1}, DE = 20) frente a grupo grande (n = {n2}, DE = 5)",
                 fontweight="bold", fontsize=13)
    sin_ejes(ax)
    return fig


@figura(250, "e2_5")
def _():
    x = np.linspace(-4, 5.5, 400)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    for ax, (d, t) in zip(axs, [(0.2, "pequeño"), (0.5, "mediano"), (0.8, "grande")]):
        ax.fill_between(x, stats.norm.pdf(x), color=AZUL, alpha=0.4)
        ax.fill_between(x, stats.norm.pdf(x, d), color=NARANJA, alpha=0.4)
        solap = 2 * stats.norm.cdf(-d / 2)
        ax.set_title(f"d = {coma(d)} ({t})\nsolapamiento {solap * 100:.0f} %", fontsize=14, fontweight="bold")
        ax.set_yticks([]), ax.set_xticks([])
        sin_ejes(ax)
    fig.suptitle("d de Cohen: la diferencia de medias medida en desviaciones típicas", fontsize=15)
    fig.tight_layout()
    return fig


@figura(260, "e2_1")
def _():
    k = np.arange(1, 31)
    p = 1 - 0.95 ** k
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.plot(k, p * 100, color=ROJO, lw=2.5)
    for kk in (1, 3, 10, 20):
        v = (1 - 0.95 ** kk) * 100
        ax.plot(kk, v, "o", color=ROJO, ms=9)
        ax.text(kk + 0.6, v + 2, f"{kk}: {v:.0f} %", fontsize=12)
    ax.axhline(5, color=GRIS, ls="--")
    ax.set_xlabel("Número de comparaciones independientes (k)")
    ax.set_ylabel("P(al menos un falso positivo) (%)")
    ax.set_title("Con α = 0,05 en cada prueba y todas las H₀ ciertas: 1 − 0,95ᵏ", fontweight="bold")
    sin_ejes(ax)
    return fig


@figura(270, "e2_2")
def _():
    import statsmodels.formula.api as smf
    c = cohorte().dropna(subset=["pas_mmHg", "edad", "sexo"])
    m = smf.ols("pas_mmHg ~ edad + sexo", data=c).fit()
    fig, ax = plt.subplots(figsize=(12, 4.6))
    edades = np.linspace(c["edad"].min(), c["edad"].max(), 50)
    for s, col in [("Hombre", AZUL), ("Mujer", NARANJA)]:
        g = c[c["sexo"] == s]
        ax.plot(g["edad"], g["pas_mmHg"], "o", color=col, alpha=0.35, ms=5)
        ax.plot(edades, m.predict(pd.DataFrame({"edad": edades, "sexo": s})), color=col, lw=3, label=s)
    b_e, b_m = m.params["edad"], m.params["sexo[T.Mujer]"]
    ax.set_title(f"PAS = {coma(m.params['Intercept'])} + {coma(b_e, 2)}·edad {'+' if b_m >= 0 else '−'} {coma(abs(b_m))}·mujer: "
                 "rectas paralelas", fontweight="bold")
    ax.text(0.02, 0.92, f"β edad = {coma(b_e, 2)} mmHg por año, a igualdad de sexo\n"
            f"β mujer = {coma(b_m)} mmHg: distancia entre las rectas, a igualdad de edad", transform=ax.transAxes,
            fontsize=12, va="top")
    ax.set_xlabel("Edad (años)")
    ax.set_ylabel("PAS (mmHg)")
    ax.legend(frameon=False, loc="lower right")
    sin_ejes(ax)
    return fig


@figura(270, "e2_3")
def _():
    import statsmodels.formula.api as smf
    renal = cohorte().merge(pd.read_csv(os.path.join(DATOS, "analiticas.csv")), on="id").dropna(
        subset=["creatinina_mg_dl", "pas_mmHg", "edad"])
    cruda = smf.ols("creatinina_mg_dl ~ pas_mmHg", data=renal).fit().params["pas_mmHg"] * 10
    ajust = smf.ols("creatinina_mg_dl ~ pas_mmHg + edad", data=renal).fit().params["pas_mmHg"] * 10
    fig = plt.figure(figsize=(12, 4.6))
    ax = fig.add_axes([0, 0, 0.5, 0.9])
    ax.set_xlim(0, 100), ax.set_ylim(0, 100), ax.axis("off")
    caja(ax, 38, 70, 24, 14, "Edad", tam=15, color=NARANJA, relleno=BLANCO, negrita=True)
    caja(ax, 4, 18, 26, 14, "PAS", tam=15)
    caja(ax, 66, 18, 30, 14, "Creatinina", tam=15)
    flecha(ax, 44, 70, 20, 32, color=NARANJA)
    flecha(ax, 56, 70, 80, 32, color=NARANJA)
    flecha(ax, 30, 25, 66, 25, color=GRIS, texto="¿?")
    ax.text(50, 94, "Confusión: la edad causa las dos", ha="center", fontsize=15, fontweight="bold")
    ax2 = fig.add_axes([0.58, 0.15, 0.38, 0.65])
    ax2.bar(["Cruda", "Ajustada\npor edad"], [cruda, ajust], color=[GRIS, AZUL])
    for i, v in enumerate([cruda, ajust]):
        ax2.text(i, v, f"{coma(v, 3)}", ha="center", va="bottom", fontsize=13, fontweight="bold")
    ax2.set_ylabel("Δ creatinina (mg/dL)\npor 10 mmHg de PAS")
    ax2.set_title(f"El coeficiente cambia un {abs(cruda - ajust) / abs(cruda) * 100:.0f} %", fontsize=14, fontweight="bold")
    sin_ejes(ax2)
    return fig


@figura(290, "e2_1")
def _():
    fig, ax = lienzo(12, 5)
    caja(ax, 1, 78, 46, 12, "Explicar: ¿se asocia X con Y?", tam=14, negrita=True)
    caja(ax, 53, 78, 46, 12, "Predecir: ¿qué riesgo tiene este paciente?", tam=14, negrita=True, color=NARANJA, relleno="#FBE9D2")
    caja(ax, 4, 30, 12, 12, "X", tam=16, negrita=True, relleno=BLANCO)
    caja(ax, 32, 30, 12, 12, "Y", tam=16, negrita=True, relleno=BLANCO)
    caja(ax, 18, 56, 12, 12, "Z", tam=16, negrita=True, color=NARANJA, relleno=BLANCO)
    flecha(ax, 16, 36, 32, 36, texto="β con IC")
    flecha(ax, 21, 56, 12, 42, color=NARANJA)
    flecha(ax, 27, 56, 36, 42, color=NARANJA)
    ax.text(24, 4, "Clave: controlar la confusión (Z)", ha="center", fontsize=12, color=TINTA)
    for i, t in enumerate(["edad", "PAS", "tabaco", "…"]):
        caja(ax, 54, 58 - i * 12, 12, 9, t, tam=11, relleno=BLANCO)
        flecha(ax, 66, 62 - i * 12, 74, 44, color=GRIS)
    caja(ax, 74, 36, 12, 14, "Modelo", tam=13)
    caja(ax, 89, 36, 10, 14, "p̂", tam=16, negrita=True, color=VERDE, relleno=BLANCO)
    flecha(ax, 86, 43, 89, 43)
    ax.text(77, 4, "Clave: discriminación y calibración\nen pacientes NUEVOS", ha="center", fontsize=12, color=TINTA)
    ax.axvline(50, color=GRIS, lw=1, ls=":")
    return fig


@figura(290, "e2_4")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "TRIPOD+AI a lo largo de un estudio de predicción")
    etapas = [("Datos", "fuente, fechas,\ninclusión, n,\neventos, perdidos"), ("Variables", "resultado y\nhorizonte;\npredictores"),
              ("Desarrollo", "tipo de modelo,\nhiperparámetros"), ("Evaluación", "discriminación\nY calibración,\ncon IC"),
              ("Equidad", "rendimiento por\nsexo, edad, etnia,\nnivel socioecon."), ("Uso", "población,\nmomento,\ndecisión;\ncódigo abierto")]
    for i, (t, s) in enumerate(etapas):
        x = 1 + i * 16.5
        caja(ax, x, 56, 14.5, 14, t, tam=13, negrita=True)
        caja(ax, x, 18, 14.5, 32, s, tam=11, relleno=BLANCO)
        if i < len(etapas) - 1:
            flecha(ax, x + 14.5, 63, x + 16.5, 63)
    caja(ax, 50.5, 2, 30, 11, "validación interna y externa", tam=12, color=NARANJA, relleno=BLANCO)
    return fig


@figura(300, "e2_3")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "Diez preguntas en cuatro bloques")
    bloques = [("Pregunta y diseño", "1. PICO\n2. Diseño: ¿causal?\n3. Variable principal\nregistrada antes", AZUL),
               ("Resultados", "4. Participantes\ny eventos\n5. Efecto con IC,\nabsoluto y relativo\n6. Relevancia clínica", VERDE),
               ("Sesgos", "7. Selección,\ninformación,\nconfusión\n8. Comparaciones\ny subgrupos", NARANJA),
               ("Aplicación", "9. Validez externa\n10. ¿Conclusiones\nexageradas?", ROJO)]
    for i, (t, s, col) in enumerate(bloques):
        x = 1 + i * 25
        caja(ax, x, 68, 22, 12, t, tam=14, negrita=True, color=col, relleno=BLANCO)
        caja(ax, x, 8, 22, 56, s, tam=12, color=col, relleno=BLANCO)
        if i < 3:
            flecha(ax, x + 22, 74, x + 25, 74)
    return fig
