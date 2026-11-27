"""Diagramas de los cuadernos (uno por tema): sustituyen explicaciones largas por un esquema.
Se dibujan con figuras.py en ../figuras/tema_XXX_esquema.png y se insertan con Cuaderno.diagrama()."""
import math

import numpy as np

from .estilo import AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt, titulo

BLANCO = "white"
TEMAS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230,
         240, 250, 260, 270, 280, 290, 300]


def si_no(ax, x, y, texto, color):
    ax.text(x, y, texto, ha="center", va="center", fontsize=13, color=color, fontweight="bold")


@figura(0, "esquema")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "Cuenta el orden de ejecución, no el orden en la página")
    caja(ax, 4, 58, 40, 14, "[1]  dosis_mg = 500", relleno=BLANCO)
    caja(ax, 4, 36, 40, 14, "[3]  print(dosis_mg)   →  250", relleno=BLANCO, color=NARANJA)
    caja(ax, 4, 14, 40, 14, "[2]  dosis_mg = 250", relleno=BLANCO)
    ax.text(24, 6, "Orden en la página: de arriba abajo", ha="center", fontsize=13, color=GRIS)
    caja(ax, 56, 50, 40, 22, "El número [n] dice cuándo\nse ejecutó la celda.\nLa celda [3] usa el último\nvalor ejecutado: 250.", tam=14)
    caja(ax, 56, 14, 40, 26, "¿Resultados extraños?\nEntorno de ejecución →\nReiniciar sesión →\nEjecutar todo", tam=14,
         relleno=BLANCO, color=VERDE)
    flecha(ax, 44, 21, 44, 41, color=NARANJA, curva=-0.6)
    return fig


@figura(10, "esquema")
def _():
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "Pedir ayuda al asistente con seguridad")
    caja(ax, 1, 56, 17, 18, "Escribe la\npetición", tam=14)
    caja(ax, 23, 54, 22, 22, "¿Identifica a\nalguien? (nombre,\nNHC, datos reales)", tam=13)
    caja(ax, 23, 14, 22, 18, "Quita los datos:\nusa variables\n(peso_kg, talla_m)", tam=13, relleno=BLANCO, color=ROJO)
    caja(ax, 51, 56, 18, 18, "Pide código\ny explicación", tam=14)
    caja(ax, 74, 56, 24, 18, "Compara con un\ncaso conocido", tam=14)
    caja(ax, 74, 14, 24, 18, "¿Coincide?\nNo → averigua por qué\nSí → úsalo", tam=13, relleno=BLANCO, color=VERDE)
    flecha(ax, 18, 65, 23, 65)
    flecha(ax, 34, 54, 34, 32, color=ROJO)
    si_no(ax, 38, 43, "Sí", ROJO)
    flecha(ax, 45, 65, 51, 65)
    si_no(ax, 48, 70, "No", VERDE)
    flecha(ax, 45, 23, 56, 55, curva=0.2)
    flecha(ax, 69, 65, 74, 65)
    flecha(ax, 86, 56, 86, 32)
    return fig


@figura(20, "esquema")
def _():
    fig, ax = lienzo(12, 4.6)
    titulo(ax, "De texto a número: el peso exportado")
    caja(ax, 2, 50, 18, 18, '"81,5"\n(str)', tam=16, color=ROJO, relleno=BLANCO)
    caja(ax, 40, 50, 18, 18, '"81.5"\n(str)', tam=16, color=NARANJA, relleno=BLANCO)
    caja(ax, 78, 50, 18, 18, "81.5\n(float)", tam=16, color=VERDE, relleno=BLANCO)
    flecha(ax, 20, 59, 40, 59, texto='.replace(",", ".")', color=TINTA)
    flecha(ax, 58, 59, 78, 59, texto="float()", color=TINTA)
    caja(ax, 10, 8, 34, 18, "int(81.9) → 81\nquita los decimales", tam=14, relleno=BLANCO, color=ROJO)
    caja(ax, 56, 8, 34, 18, "round(81.9) → 82\nredondea", tam=14, relleno=BLANCO, color=VERDE)
    return fig


@figura(30, "esquema")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.2))
    for y, op, cerrado, color in [(1, "fr_rpm >= 22", True, VERDE), (0, "fr_rpm > 22", False, NARANJA)]:
        ax.plot([22, 30], [y, y], lw=6, color=color, solid_capstyle="butt")
        ax.plot(22, y, "o", ms=16, mfc=color if cerrado else "white", mec=color, mew=3)
        ax.text(15.5, y, op, fontsize=17, va="center", family="monospace", color=TINTA)
        ax.text(30.4, y, "True" if cerrado else "False con FR = 22", fontsize=14, va="center", color=color)
    ax.axvline(22, color=GRIS, ls=":", lw=1.5)
    ax.set_xlim(15, 35)
    ax.set_ylim(-0.7, 1.7)
    ax.set_yticks([])
    ax.set_xticks(range(18, 31, 2))
    ax.set_xlabel("Frecuencia respiratoria (rpm)")
    ax.spines["left"].set_visible(False)
    ax.set_title("El valor frontera: ● se incluye, ○ se excluye", fontweight="bold")
    ax.text(15.5, 1.5, "Recuerda: = asigna, == compara", fontsize=13, color=ROJO)
    return fig


@figura(40, "esquema")
def _():
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "Acumulador y contador: glucemias 110, 65, 140 mg/dL")
    caja(ax, 1, 58, 22, 20, "ANTES del bucle\ntotal = 0\nn_hipo = 0", tam=14, relleno=BLANCO)
    caja(ax, 30, 58, 36, 20, "DENTRO, en cada vuelta\ntotal += glucemia\nsi glucemia < 70: n_hipo += 1", tam=14)
    caja(ax, 73, 58, 26, 20, "DESPUÉS\nmedia = total / 3", tam=14, relleno=BLANCO)
    flecha(ax, 23, 68, 30, 68)
    flecha(ax, 66, 68, 73, 68)
    ax.text(48, 52, "↻ se repite con cada valor de la serie", ha="center", fontsize=13, color=GRIS)
    filas = [("vuelta", "glucemia", "total", "n_hipo"), ("inicio", "—", "0", "0"), ("1", "110", "110", "0"),
             ("2", "65", "175", "1"), ("3", "140", "315", "1")]
    for i, fila in enumerate(filas):
        for j, v in enumerate(fila):
            ax.text(18 + j * 18, 44 - i * 9, v, ha="center", fontsize=14, color=TINTA if i else AZUL,
                    fontweight="bold" if i == 0 or (i == 3 and j == 3) else "normal")
    ax.text(90, 8, "media = 105", ha="center", fontsize=15, color=VERDE, fontweight="bold")
    return fig


@figura(50, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "Verificar una función propuesta por el asistente")
    caja(ax, 1, 52, 20, 22, "Función del\nasistente:\n(pas + pad) / 2", tam=13)
    caja(ax, 26, 52, 22, 22, "Caso conocido\n120/80 mmHg\nesperado: 93,3", tam=13, relleno=BLANCO)
    caja(ax, 53, 52, 20, 22, "Resultado\n100,0", tam=15, relleno=BLANCO, color=ROJO)
    caja(ax, 78, 52, 21, 22, "✗ No coincide:\ncalcula la media\naritmética", tam=13, relleno=BLANCO, color=ROJO)
    caja(ax, 30, 8, 40, 20, "Corrige: pad + (pas − pad) / 3\nassert → 93,3 ✓", tam=14, relleno=BLANCO, color=VERDE)
    for x1, x2 in [(21, 26), (48, 53), (73, 78)]:
        flecha(ax, x1, 63, x2, 63)
    flecha(ax, 88, 52, 70, 22, curva=-0.2)
    return fig


@figura(60, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "Módulos: importar antes de usar")
    caja(ax, 36, 66, 28, 14, "Tu cuaderno\nimport …", tam=15, negrita=True)
    mods = [("math\nraíces, logaritmos", 2, AZUL), ("statistics\nmedia, mediana", 22, AZUL), ("random\nazar sencillo", 42, AZUL),
            ("numpy\nmuchos datos", 62, NARANJA), ("matplotlib\ngráficos", 82, NARANJA)]
    for texto, x, color in mods:
        caja(ax, x, 26, 16, 18, texto, tam=12, relleno=BLANCO, color=color)
        flecha(ax, 50, 66, x + 8, 44, color=GRIS)
    ax.text(31, 14, "Vienen con Python", ha="center", fontsize=13, color=AZUL)
    ax.text(80, 14, "Externos (Colab ya los trae)", ha="center", fontsize=13, color=NARANJA)
    ax.text(50, 3, "¿Falta un módulo externo?  →  %pip install nombre", ha="center", fontsize=14, color=TINTA)
    return fig


@figura(70, "esquema")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "¿Con qué modo abro el fichero?")
    caja(ax, 34, 66, 32, 14, "¿Qué quieres hacer?", tam=15, negrita=True)
    caja(ax, 1, 28, 28, 20, 'Leer\n"r"\nerror si no existe', tam=14, relleno=BLANCO)
    caja(ax, 36, 28, 28, 20, 'Añadir al final\n"a"\nconserva lo anterior', tam=14, relleno=BLANCO, color=VERDE)
    caja(ax, 71, 28, 28, 20, 'Escribir desde cero\n"w"\nBORRA lo anterior', tam=14, relleno=BLANCO, color=ROJO)
    for x in (15, 50, 85):
        flecha(ax, 50, 66, x, 48)
    ax.text(50, 12, 'Siempre: with open(nombre, modo, encoding="utf-8")', ha="center", fontsize=14, family="monospace")
    ax.text(50, 3, "En Colab el fichero se borra al cerrar la sesión: descárgalo o guárdalo en Drive", ha="center",
            fontsize=13, color=NARANJA)
    return fig


@figura(80, "esquema")
def _():
    fig, ax = lienzo(12, 5.6)
    caja(ax, 36, 40, 28, 18, "Toda respuesta\nse verifica", tam=17, negrita=True, color=ROJO, relleno=BLANCO)
    lims = [("Alucinación", 4, 76), ("Fecha de corte", 38, 80), ("Variabilidad", 72, 76),
            ("Sesgos", 4, 6), ("Complacencia", 38, 2), ("Cálculo poco fiable", 72, 6)]
    for texto, x, y in lims:
        caja(ax, x, y, 24, 12, texto, tam=14)
        flecha(ax, x + 12, y + (0 if y > 50 else 12), 50, 58 if y > 50 else 40, color=GRIS)
    return fig


@figura(90, "esquema")
def _():
    fig, ax = lienzo(12, 5.8)
    titulo(ax, "Ciclo de mejora recursiva: cuándo parar", y=99)
    caja(ax, 2, 60, 18, 14, "El modelo\ngenera código", tam=13)
    caja(ax, 26, 60, 18, 14, "Ejecutar las\npruebas", tam=13)
    caja(ax, 50, 58, 20, 18, "¿Todas\nsuperadas?", tam=14)
    caja(ax, 78, 60, 20, 14, "FIN: objetivo\ncumplido", tam=13, relleno=BLANCO, color=VERDE)
    caja(ax, 50, 26, 20, 18, "¿Intentos\nagotados o\nmismo código?", tam=13)
    caja(ax, 78, 28, 20, 14, "FIN: revisar\na mano", tam=13, relleno=BLANCO, color=ROJO)
    caja(ax, 14, 26, 26, 18, "Devolver al modelo\nqué casos fallan\ny por qué", tam=13, relleno=BLANCO, color=NARANJA)
    flecha(ax, 20, 67, 26, 67)
    flecha(ax, 44, 67, 50, 67)
    flecha(ax, 70, 67, 78, 67)
    si_no(ax, 74, 71, "Sí", VERDE)
    flecha(ax, 60, 58, 60, 44)
    si_no(ax, 64, 51, "No", ROJO)
    flecha(ax, 70, 35, 78, 35)
    si_no(ax, 74, 39, "Sí", ROJO)
    flecha(ax, 50, 35, 40, 35)
    si_no(ax, 45, 39, "No", NARANJA)
    flecha(ax, 20, 44, 11, 60)
    return fig


@figura(100, "esquema")
def _():
    fig, ax = lienzo(12, 5.6)
    titulo(ax, "Valores perdidos: antes de actuar, ¿por qué faltan?")
    caja(ax, 36, 70, 28, 12, "Dato ausente (NaN)", tam=15, negrita=True)
    datos = [("Completamente\nal azar", "Eliminar no sesga;\nsolo reduce n", VERDE, 2),
             ("Al azar\ncondicionado", "Tener en cuenta las\nvariables de las que\ndepende", NARANJA, 36),
             ("No al azar", "Cualquier tratamiento\nsimple sesga", ROJO, 70)]
    for mec, cons, color, x in datos:
        caja(ax, x, 40, 28, 16, mec, tam=14, color=color)
        caja(ax, x, 12, 28, 18, cons, tam=13, relleno=BLANCO, color=color)
        flecha(ax, 50, 70, x + 14, 56)
        flecha(ax, x + 14, 40, x + 14, 30, color=color)
    ax.text(50, 2, "Nunca rellenes con cero una variable clínica", ha="center", fontsize=14, color=ROJO, fontweight="bold")
    return fig


@figura(110, "esquema")
def _():
    from matplotlib.patches import Ellipse
    fig, ax = lienzo(12, 5)
    titulo(ax, "Comprobar las claves antes de unir: conjuntos de id")
    ax.add_patch(Ellipse((38, 46), 46, 62, fc=AZUL_CLARO, ec=AZUL, lw=2.5, alpha=0.8))
    ax.add_patch(Ellipse((62, 46), 46, 62, fc="#FBE9D2", ec=NARANJA, lw=2.5, alpha=0.7))
    ax.text(28, 80, "cohorte", fontsize=16, color=AZUL, fontweight="bold", ha="center")
    ax.text(72, 80, "analíticas", fontsize=16, color=NARANJA, fontweight="bold", ha="center")
    ax.text(25, 46, "Sin analítica\ncohorte − analíticas", ha="center", fontsize=13)
    ax.text(50, 46, "En las\ndos", ha="center", fontsize=14, fontweight="bold")
    ax.text(75, 46, "Fuera de cohorte\nanalíticas − cohorte", ha="center", fontsize=13)
    ax.text(50, 4, 'Antes, comprueba que id es único en cada tabla: .is_unique', ha="center", fontsize=14, color=TINTA)
    return fig


@figura(120, "esquema")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "¿Qué resumen uso para una variable cuantitativa?")
    caja(ax, 30, 56, 40, 20, "Mira el histograma y el\ndiagrama de caja: ¿simétrica\ny sin valores extremos?", tam=14)
    caja(ax, 3, 10, 36, 20, "media ± DE", tam=18, negrita=True, relleno=BLANCO, color=VERDE)
    caja(ax, 61, 10, 36, 20, "mediana [Q1–Q3]", tam=18, negrita=True, relleno=BLANCO, color=NARANJA)
    flecha(ax, 40, 56, 21, 30)
    si_no(ax, 26, 46, "Sí", VERDE)
    flecha(ax, 60, 56, 79, 30)
    si_no(ax, 74, 46, "No", NARANJA)
    return fig


@figura(130, "esquema")
def _():
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
    paneles = [("X causa Y", [("X", "Y")], False), ("Causalidad inversa", [("Y", "X")], False),
               ("Confusión", [("Z", "X"), ("Z", "Y")], True), ("Azar", [], False)]
    pos = {"X": (20, 30), "Y": (80, 30), "Z": (50, 80)}
    for ax, (tit, aristas, con_z) in zip(axs, paneles):
        ax.set_xlim(0, 100), ax.set_ylim(0, 100), ax.axis("off")
        ax.set_title(tit, fontsize=15, fontweight="bold", color=TINTA)
        nodos = ["X", "Y"] + (["Z"] if con_z else [])
        for n in nodos:
            ax.add_patch(plt.Circle(pos[n], 11, fc=AZUL_CLARO if n != "Z" else "#FBE9D2", ec=AZUL if n != "Z" else NARANJA, lw=2))
            ax.text(*pos[n], n, ha="center", va="center", fontsize=17, fontweight="bold", color=TINTA)
        for a, b in aristas:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            d = math.hypot(x2 - x1, y2 - y1)
            k = 12 / d
            flecha(ax, x1 + (x2 - x1) * k, y1 + (y2 - y1) * k, x2 - (x2 - x1) * k, y2 - (y2 - y1) * k, color=TINTA)
        if tit == "Azar":
            ax.text(50, 30, "~", ha="center", va="center", fontsize=30, color=GRIS)
            ax.text(50, 8, "muestras pequeñas", ha="center", fontsize=12, color=GRIS)
    fig.suptitle("Cuatro explicaciones de una correlación entre X e Y", fontsize=18, fontweight="bold", color=TINTA)
    fig.tight_layout()
    return fig


@figura(140, "esquema")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Tres formas de entender la probabilidad")
    caja(ax, 2, 42, 28, 30, "Clásica\nfavorables / posibles\n\n1/4 en el cruce\nde dos portadores", tam=13)
    caja(ax, 36, 42, 28, 30, "Frecuentista\nfrecuencia a largo plazo\n\ncomplicaciones en\n10.000 cirugías", tam=13)
    caja(ax, 70, 42, 28, 30, "Subjetiva\ngrado de creencia\n\n«70 % de que sea\nuna neumonía»", tam=13, relleno=BLANCO)
    flecha(ax, 16, 42, 50, 42, curva=0.45, color=VERDE)
    ax.text(33, 10, "Ley de los grandes números: al repetir mucho,\nla frecuencia relativa se acerca a la probabilidad",
            ha="center", fontsize=13, color=VERDE)
    return fig


@figura(150, "esquema")
def _():
    fig, ax = lienzo(12, 4.6)
    titulo(ax, "Dos pruebas positivas seguidas: se multiplican las odds")
    p0 = 0.01
    o1 = p0 / (1 - p0) * (0.90 / 0.09)
    p1 = o1 / (1 + o1)
    o2 = o1 * 8
    p2 = o2 / (1 + o2)
    for x, p, et in [(2, p0, "Preprueba"), (40, p1, "Tras la\nmamografía +"), (78, p2, "Tras la\necografía +")]:
        caja(ax, x, 40, 20, 26, f"{et}\n{p * 100:.0f} %", tam=15, relleno=BLANCO,
             color=VERDE if p > 0.3 else AZUL)
    flecha(ax, 22, 53, 40, 53, texto="odds × LR+ 10", color=TINTA)
    flecha(ax, 60, 53, 78, 53, texto="odds × LR+ 8", color=TINTA)
    ax.text(50, 14, "La posprueba de una prueba es la preprueba de la siguiente.\n"
            "Solo vale si las pruebas no fallan por las mismas razones.", ha="center", fontsize=13, color=NARANJA)
    return fig


@figura(160, "esquema")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Dos reglas: qué resultado es concluyente")
    caja(ax, 2, 40, 44, 34, "SnNOut\nSensibilidad muy alta\n+ resultado Negativo\n→ DESCARTA", tam=15, color=VERDE, relleno=BLANCO)
    caja(ax, 54, 40, 44, 34, "SpPIn\nEspecificidad muy alta\n+ resultado Positivo\n→ CONFIRMA", tam=15, color=NARANJA, relleno=BLANCO)
    ax.text(24, 24, "Útil para cribar", ha="center", fontsize=15, color=VERDE, fontweight="bold")
    ax.text(76, 24, "Útil para confirmar", ha="center", fontsize=15, color=NARANJA, fontweight="bold")
    ax.text(50, 6, "Pocos falsos negativos  ·  pocos falsos positivos", ha="center", fontsize=13, color=GRIS)
    return fig


@figura(170, "esquema")
def _():
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "¿Binomial o Poisson?")
    caja(ax, 28, 66, 44, 16, "¿Qué cuentas?", tam=15, negrita=True)
    caja(ax, 1, 30, 40, 24, "Éxitos en n ensayos fijos,\ncon la misma p en cada uno\n(responden 7 de 20)", tam=13)
    caja(ax, 59, 30, 40, 24, "Sucesos en un tiempo o\nun espacio, con tasa λ\n(infecciones al mes)", tam=13)
    caja(ax, 1, 2, 40, 16, "Binomial(n, p)", tam=16, negrita=True, relleno=BLANCO, color=AZUL)
    caja(ax, 59, 2, 40, 16, "Poisson(λ)", tam=16, negrita=True, relleno=BLANCO, color=NARANJA)
    flecha(ax, 40, 66, 21, 54)
    flecha(ax, 60, 66, 79, 54)
    flecha(ax, 21, 30, 21, 18)
    flecha(ax, 79, 30, 79, 18)
    flecha(ax, 41, 10, 59, 10, color=VERDE)
    ax.text(50, 22, "si n ≥ 50 y np ≤ 5:\nλ = np", ha="center", fontsize=13, color=VERDE)
    return fig


@figura(180, "esquema")
def _():
    fig, ax = lienzo(12, 5.2)
    titulo(ax, "Cómo construir un intervalo de referencia")
    caja(ax, 2, 60, 28, 18, "Muestra de individuos\nde referencia SANOS\n(≥ 120 por grupo)", tam=13)
    caja(ax, 38, 60, 26, 18, "¿Variable normal?\n(gráfico Q-Q)", tam=14)
    caja(ax, 70, 62, 29, 16, "media ± 1,96 DE", tam=15, relleno=BLANCO, color=VERDE)
    caja(ax, 52, 16, 47, 20, "Percentiles 2,5 y 97,5\n(no paramétrico)", tam=15, relleno=BLANCO, color=NARANJA)
    flecha(ax, 30, 69, 38, 69)
    flecha(ax, 64, 70, 70, 70)
    si_no(ax, 67, 74, "Sí", VERDE)
    flecha(ax, 51, 60, 70, 36)
    si_no(ax, 57, 48, "No", NARANJA)
    caja(ax, 2, 14, 40, 22, "Media ± 1,96 DE con datos\nasimétricos: límite inferior\nmuy bajo o imposible", tam=13,
         relleno=BLANCO, color=ROJO)
    return fig


@figura(190, "esquema")
def _():
    rng = np.random.default_rng(190)
    pac = rng.normal(130, 15, 400)
    medias = rng.normal(130, 15 / math.sqrt(25), 400)
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.hist(pac, bins=30, alpha=0.55, color=AZUL, label="PAS de los pacientes: DE = 15 mmHg")
    ax.hist(medias, bins=30, alpha=0.8, color=NARANJA, label="Medias de muestras de n = 25: EE = 15/√25 = 3 mmHg")
    ax.set_xlabel("Presión arterial sistólica (mmHg)")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title("La DE describe a los pacientes; el EE, la precisión de la media", fontweight="bold")
    ax.set_ylim(0, ax.get_ylim()[1] * 1.45)
    ax.legend(loc="upper left", fontsize=12, frameon=False)
    ax.text(178, 30, "×4 pacientes\n→ EE a la mitad", fontsize=13, color=NARANJA, ha="right")
    return fig


@figura(200, "esquema")
def _():
    x, n, z = 1, 20, 1.96
    p = x / n
    ee = math.sqrt(p * (1 - p) / n)
    wald = (p - z * ee, p + z * ee)
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    m = z / (1 + z * z / n) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    wilson = (c - m, c + m)
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.axvspan(-0.1, 0, color=ROJO, alpha=0.12)
    ax.text(-0.05, 1.55, "imposible", ha="center", color=ROJO, fontsize=13)
    for y, (a, b), nom, col in [(1, wald, "Wald", ROJO), (0, wilson, "Wilson", VERDE)]:
        ax.plot([a, b], [y, y], lw=6, color=col)
        ax.plot(p, y, "o", ms=12, color=TINTA)
        ax.text(b + 0.01, y, f"{nom}: {a:.3f} a {b:.3f}".replace(".", ",").replace("-", "−"), va="center", fontsize=14, color=col)
    ax.set_xlim(-0.1, 0.5)
    ax.set_ylim(-0.6, 1.8)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Proporción")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",").replace("-", "−")))
    ax.set_title("1 caso de 20 (5 %): Wald da un límite negativo; Wilson, no", fontweight="bold")
    return fig


@figura(210, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "La lógica de un contraste de hipótesis")
    pasos = ["Plantea H₀\n(sin efecto)\ny H₁", "Supón que\nH₀ es cierta", "Calcula el valor p:\n¿son los datos\ncompatibles con H₀?"]
    for i, t in enumerate(pasos):
        caja(ax, 1 + i * 24, 52, 20, 24, t, tam=13)
        flecha(ax, 21 + i * 24, 64, 25 + i * 24, 64)
    caja(ax, 73, 52, 26, 24, "¿p < α (0,05)?", tam=15)
    caja(ax, 52, 8, 22, 20, "Rechaza H₀", tam=15, relleno=BLANCO, color=VERDE)
    caja(ax, 78, 8, 21, 20, "No rechaza H₀", tam=15, relleno=BLANCO, color=NARANJA)
    flecha(ax, 80, 52, 63, 28)
    si_no(ax, 68, 42, "Sí", VERDE)
    flecha(ax, 88, 52, 88, 28)
    si_no(ax, 92, 40, "No", NARANJA)
    ax.text(24, 18, "Da siempre también el IC:\nel tamaño del efecto importa", ha="center", fontsize=13, color=TINTA)
    return fig


@figura(220, "esquema")
def _():
    obs = np.array([[1, 14], [6, 9]])
    esp = obs.sum(1, keepdims=True) * obs.sum(0, keepdims=True) / obs.sum()
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Ensayo piloto: frecuencias esperadas si no hubiera diferencia")
    ax.text(40, 74, "Náuseas", ha="center", fontsize=15, fontweight="bold")
    ax.text(64, 74, "Sin náuseas", ha="center", fontsize=15, fontweight="bold")
    for i, grupo in enumerate(["Pauta A (15)", "Pauta B (15)"]):
        ax.text(14, 56 - i * 24, grupo, ha="center", va="center", fontsize=15, fontweight="bold")
        for j in range(2):
            col = ROJO if esp[i, j] < 5 else VERDE
            caja(ax, 30 + j * 24, 46 - i * 24, 20, 18, f"O = {obs[i, j]}\nE = {esp[i, j]:.1f}".replace(".", ","),
                 tam=14, color=col, relleno=BLANCO)
    caja(ax, 80, 26, 19, 36, "E < 5\n→ prueba\nexacta de\nFisher", tam=14, color=ROJO, relleno=BLANCO)
    ax.text(50, 2, "E = total de fila × total de columna / N", ha="center", fontsize=13, color=GRIS)
    return fig


@figura(230, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "Ji cuadrado: comparar lo observado con lo esperado")
    caja(ax, 2, 40, 28, 30, "Tabla observada\nO", tam=16)
    caja(ax, 38, 40, 28, 30, "Tabla esperada si\nfueran independientes\nE = fila × columna / N", tam=13, relleno=BLANCO)
    caja(ax, 74, 40, 24, 30, "χ² = Σ (O − E)² / E\ngl = (r − 1)(c − 1)", tam=13)
    flecha(ax, 30, 55, 38, 55)
    flecha(ax, 66, 55, 74, 55)
    ax.text(50, 20, "O muy distinto de E → χ² grande → p pequeño", ha="center", fontsize=15, color=TINTA)
    ax.text(50, 6, "Si muchas E < 5 → Fisher (Tema 220)", ha="center", fontsize=14, color=ROJO)
    return fig


@figura(240, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "McNemar: solo cuentan los pares discordantes")
    ax.text(40, 78, "B acierta", ha="center", fontsize=15, fontweight="bold")
    ax.text(66, 78, "B falla", ha="center", fontsize=15, fontweight="bold")
    ax.text(14, 60, "A acierta", ha="center", fontsize=15, fontweight="bold")
    ax.text(14, 34, "A falla", ha="center", fontsize=15, fontweight="bold")
    caja(ax, 30, 50, 20, 20, "a\nambos aciertan", tam=13, color=GRIS, relleno="#EEEEEE", txt=GRIS)
    caja(ax, 56, 50, 20, 20, "b\nsolo A acierta", tam=14, color=NARANJA, relleno=BLANCO, negrita=True)
    caja(ax, 30, 24, 20, 20, "c\nsolo B acierta", tam=14, color=NARANJA, relleno=BLANCO, negrita=True)
    caja(ax, 56, 24, 20, 20, "d\nambos fallan", tam=13, color=GRIS, relleno="#EEEEEE", txt=GRIS)
    ax.text(90, 47, "χ² = (b − c)²\n/ (b + c)", ha="center", fontsize=15, color=TINTA)
    ax.text(50, 6, "Si b + c < 25: versión exacta (binomial de b en b + c, p = 0,5)", ha="center", fontsize=13, color=GRIS)
    return fig


@figura(250, "esquema")
def _():
    fig, ax = lienzo(12, 5.6)
    titulo(ax, "Antes de la prueba t: comprobar las condiciones", y=99)
    caja(ax, 1, 60, 26, 20, "¿Observaciones\nindependientes?\n(por el diseño)", tam=13)
    caja(ax, 36, 60, 28, 20, "¿Normal o n ≥ 30\npor grupo?\n(histograma, Q-Q)", tam=13)
    caja(ax, 72, 60, 27, 20, "¿Sin atípicos\nextremos?\n(diagrama de caja)", tam=13)
    caja(ax, 72, 26, 27, 16, "Prueba t", tam=16, negrita=True, relleno=BLANCO, color=VERDE)
    caja(ax, 1, 20, 26, 22, "Otro método\n(datos agrupados,\nmedidas repetidas)", tam=13, relleno=BLANCO, color=ROJO)
    caja(ax, 36, 20, 28, 22, "Logaritmo o prueba\nno paramétrica;\natípicos: ¿errores?", tam=13, relleno=BLANCO, color=NARANJA)
    flecha(ax, 27, 70, 36, 70)
    flecha(ax, 64, 70, 72, 70)
    flecha(ax, 85, 60, 85, 42)
    si_no(ax, 31, 74, "Sí", VERDE), si_no(ax, 68, 74, "Sí", VERDE), si_no(ax, 89, 51, "Sí", VERDE)
    flecha(ax, 14, 60, 14, 42, color=ROJO)
    flecha(ax, 50, 60, 50, 42, color=NARANJA)
    flecha(ax, 76, 60, 60, 42, color=NARANJA)
    si_no(ax, 18, 51, "No", ROJO), si_no(ax, 54, 51, "No", NARANJA), si_no(ax, 73, 48, "No", NARANJA)
    return fig


@figura(260, "esquema")
def _():
    p = [0.003, 0.014, 0.018, 0.30]
    k, alfa = len(p), 0.05
    fig, ax = lienzo(12, 5.4)
    titulo(ax, "Cuatro comparaciones (α = 0,05): Bonferroni frente a Holm")
    for j, cab in enumerate(["p ordenado", "Bonferroni: p < α/4", "Holm: p < α/(k − i + 1)"]):
        ax.text(16 + j * 32, 80, cab, ha="center", fontsize=14, fontweight="bold", color=TINTA)
    seguir = True
    for i, pi in enumerate(p):
        y = 66 - i * 15
        ax.text(16, y, f"{pi:.3f}".replace(".", ","), ha="center", fontsize=15)
        b = pi < alfa / k
        ax.text(48, y, f"< {alfa / k:.4f}".replace(".", ",") + ("  ✓" if b else "  ✗"), ha="center", fontsize=14,
                color=VERDE if b else ROJO)
        u = alfa / (k - i)
        h = seguir and pi < u
        seguir = h
        ax.text(80, y, f"< {u:.4f}".replace(".", ",") + ("  ✓" if h else "  ✗"), ha="center", fontsize=14,
                color=VERDE if h else ROJO)
    ax.text(48, 4, "1 significativa", ha="center", fontsize=15, color=TINTA, fontweight="bold")
    ax.text(80, 4, "3 significativas", ha="center", fontsize=15, color=TINTA, fontweight="bold")
    return fig


@figura(270, "esquema")
def _():
    fig, ax = lienzo(12, 4.8)
    titulo(ax, "Confusión por indicación: la flecha va al revés")
    caja(ax, 2, 50, 24, 18, "PAS elevada", tam=15)
    caja(ax, 38, 50, 24, 18, "Tratamiento\nantihipertensivo", tam=14)
    flecha(ax, 26, 61, 38, 61, color=VERDE)
    ax.text(32, 72, "el médico trata", ha="center", fontsize=12, color=VERDE)
    flecha(ax, 38, 54, 26, 54, color=ROJO)
    ax.text(32, 44, "✗ el modelo lo lee así:\n«los tratados tienen\nla PAS 17 mmHg mayor»", ha="center", fontsize=12, color=ROJO, va="top")
    caja(ax, 70, 66, 28, 14, "Caso difícil", tam=14)
    caja(ax, 66, 26, 16, 16, "Usa el\nasistente", tam=13, relleno=BLANCO)
    caja(ax, 84, 26, 15, 16, "Peor\nevolución", tam=13, relleno=BLANCO)
    flecha(ax, 78, 66, 74, 42)
    flecha(ax, 90, 66, 91, 42)
    ax.text(84, 14, "El asistente no hace daño,\npero la asociación aparece", ha="center", fontsize=12, color=NARANJA, va="top")
    return fig


@figura(280, "esquema")
def _():
    fig, ax = lienzo(12, 4.6)
    titulo(ax, "De los coeficientes a la probabilidad de un paciente")
    caja(ax, 1, 46, 28, 22, "z = β₀ + β₁x₁ + β₂x₂ + …\n(logaritmo de las odds)", tam=13)
    caja(ax, 37, 46, 24, 22, "odds = eᶻ", tam=16)
    caja(ax, 69, 46, 30, 22, "p = odds / (1 + odds)", tam=15, relleno=BLANCO, color=VERDE)
    flecha(ax, 29, 57, 37, 57)
    flecha(ax, 61, 57, 69, 57)
    z = -2.0
    o = math.exp(z)
    ax.text(50, 24, f"Ejemplo: z = −2  →  odds = {o:.3f}  →  p = {o / (1 + o):.3f}".replace(".", ","), ha="center",
            fontsize=15, color=TINTA)
    ax.text(50, 6, "Cada coeficiente exponenciado, eᵝ, es una odds ratio", ha="center", fontsize=14, color=NARANJA)
    return fig


@figura(290, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "Validación cruzada con 5 particiones")
    for i in range(5):
        y = 74 - i * 14
        ax.text(8, y + 5, f"Ronda {i + 1}", ha="center", va="center", fontsize=13)
        for j in range(5):
            ev = i == j
            ax.add_patch(plt.Rectangle((16 + j * 13, y), 12, 10, fc=NARANJA if ev else AZUL_CLARO, ec="white", lw=2))
        ax.text(86, y + 5, "→ AUC", va="center", fontsize=13, color=TINTA)
    ax.add_patch(plt.Rectangle((16, 2), 4, 4, fc=AZUL_CLARO))
    ax.text(21, 4, "ajustar el modelo", va="center", fontsize=12)
    ax.add_patch(plt.Rectangle((48, 2), 4, 4, fc=NARANJA))
    ax.text(53, 4, "evaluarlo", va="center", fontsize=12)
    ax.text(86, 4, "5 AUC: media y variación", ha="center", va="center", fontsize=13, color=VERDE)
    return fig


@figura(300, "esquema")
def _():
    fig, ax = lienzo(12, 5)
    titulo(ax, "¿Puede el diseño demostrar causalidad?")
    caja(ax, 25, 62, 50, 16, "¿Asigna el investigador la exposición?", tam=15, negrita=True)
    caja(ax, 2, 18, 42, 28, "Sí, al azar\nEnsayo clínico aleatorizado\nPuede demostrar causalidad\nGuía CONSORT", tam=14,
         relleno=BLANCO, color=VERDE)
    caja(ax, 56, 18, 42, 28, "No\nCohortes, casos y controles,\ntransversal: con mucha cautela\nGuía STROBE", tam=14,
         relleno=BLANCO, color=NARANJA)
    flecha(ax, 40, 62, 23, 46)
    flecha(ax, 60, 62, 77, 46)
    ax.text(77, 6, "El estudio del café está aquí", ha="center", fontsize=13, color=NARANJA, fontweight="bold")
    return fig
