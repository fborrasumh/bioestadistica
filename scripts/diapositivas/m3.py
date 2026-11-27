"""Diapositivas del Módulo 3 · Procesado inicial de datos (temas 90 a 130)."""
import numpy as np

from .estilo import (AZUL, AZUL_CLARO, GRIS, NARANJA, ROJO, TINTA, VERDE, caja, figura, flecha, lienzo, plt)

URL_COHORTE = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_cardiovascular.csv"

DIAPOS = {
    90: [
        dict(ancla="1. Caso clínico", titulo="«Funciona» no es lo mismo que «es correcto»", fig="curb",
             ideas=["El código del asistente se ejecuta sin errores… y se equivoca justo en las fronteras.",
                    "Solo lo descubre quien tiene casos de prueba escritos a partir de la definición clínica."]),
        dict(ancla="2.1 El ciclo de mejora recursiva", titulo="El ciclo de mejora recursiva", fig="ciclo",
             ideas=["Especificar y escribir las pruebas <b>antes</b> de pedir el código.",
                    "Generar, ejecutar, verificar y corregir, hasta cumplir un criterio de parada.",
                    "El humano decide la especificación y cuándo el resultado es aceptable."]),
        dict(ancla="2.4 La ley de Goodhart", titulo="Ley de Goodhart: cuando la prueba se convierte en objetivo", fig="goodhart",
             ideas=["Si se corrige mirando siempre las mismas pruebas, el código acaba ajustado a ellas.",
                    "El rendimiento real se mide con <b>pruebas reservadas</b>, que no se usaron para corregir."]),
    ],
    100: [
        dict(ancla="1. Caso clínico", titulo="Un peso medio de 78 kg… con un paciente de 680 kg",
             codigo=f'''
import pandas as pd
import matplotlib.pyplot as plt

datos = pd.read_csv("{URL_COHORTE}")
peso = datos["peso_kg"].dropna()
fig, ejes = plt.subplots(1, 2, figsize=(13, 4.2))
ejes[0].hist(peso, bins=60, color="steelblue")
ejes[0].set_title("Peso registrado (kg)", fontweight="bold")
ejes[0].annotate("680 kg", xy=(680, 1), xytext=(520, 40), fontsize=13, color="firebrick", arrowprops=dict(arrowstyle="->", color="firebrick"))
ejes[0].annotate("7,4 kg", xy=(7.4, 1), xytext=(60, 60), fontsize=13, color="firebrick", arrowprops=dict(arrowstyle="->", color="firebrick"))
ejes[0].set_xlabel("kg"); ejes[0].set_ylabel("Pacientes")
problemas = {{"Peso ausente": datos["peso_kg"].isna().sum(), "Sexo con varias grafías": datos["sexo"].nunique() - 2,
             "Pacientes duplicados": datos.duplicated("id").sum(), "PAD > PAS": (datos["pad_mmHg"] > datos["pas_mmHg"]).sum()}}
ejes[1].barh(list(problemas), list(problemas.values()), color="firebrick")
ejes[1].set_title("Otros problemas del registro", fontweight="bold")
plt.tight_layout()
plt.show()
''',
             ideas=["Una media se calcula siempre, aunque los datos estén mal: ningún error impide hacer la cuenta.",
                    "Antes de analizar, se limpia, y cada decisión queda documentada en un registro de limpieza."]),
        dict(ancla="2.1 Pandas y el DataFrame", titulo="Anatomía de un DataFrame", fig="dataframe",
             ideas=["Filas = pacientes; columnas = variables; cada columna es una <b>Series</b> con su tipo.",
                    "NaN marca un dato ausente: pandas lo excluye de las medias y lo cuenta con .isna()."]),
        dict(ancla="2.3 Errores de registro", titulo="¿Error de registro o valor atípico real?", fig="plausible",
             ideas=["Un error es imposible o incoherente: se corrige si se puede justificar o se convierte en NaN.",
                    "Un atípico real es extremo pero posible: se conserva. Eliminarlo sesga el análisis."]),
    ],
    110: [
        dict(ancla="1. Caso clínico", titulo="La información está repartida en tres tablas", fig="fuentes",
             ideas=["La cohorte, las analíticas y los centros se relacionan por una <b>clave</b>: id o centro.",
                    "Antes de unir hay que comprobar las claves: ¿hay pacientes sin analítica? ¿analíticas sin paciente?"]),
        dict(ancla="2.1 Unir tablas", titulo="Tres formas de unir dos tablas", fig="joins",
             ideas=["<b>inner</b>: solo los que están en las dos. <b>left</b>: todos los de la izquierda. <b>outer</b>: todos.",
                    "La unión elegida cambia el número de pacientes, y con él los denominadores."],
             pregunta="Si queréis el porcentaje de diabéticos con HbA1c ≥ 8 %, ¿qué unión usaríais?"),
        dict(ancla="2.3 Tablas de contingencia", titulo="Tabla de contingencia: dos variables cualitativas", fig="contingencia",
             ideas=["Cruza dos variables y cuenta los pacientes de cada combinación.",
                    "Los porcentajes por fila responden a «¿qué proporción de cada centro…?»."]),
    ],
    120: [
        dict(ancla="1. Caso clínico", titulo="Once estancias por neumonía: ¿media o mediana?",
             codigo=r'''
import matplotlib.pyplot as plt
import numpy as np

estancias = [3, 4, 4, 5, 5, 5, 6, 6, 7, 8, 32]
plt.figure(figsize=(12, 3.6))
y = [0.1 * sum(1 for e in estancias[:i] if e == x) for i, x in enumerate(estancias)]
plt.scatter(estancias, y, s=220, color=["firebrick" if e == 32 else "steelblue" for e in estancias], zorder=3)
plt.axvline(np.mean(estancias), color="darkorange", lw=3, label=f"Media = {np.mean(estancias):.1f} días")
plt.axvline(np.median(estancias), color="seagreen", lw=3, label=f"Mediana = {np.median(estancias):.0f} días")
plt.yticks([]); plt.ylim(-0.2, 0.6); plt.xlabel("Estancia (días)")
plt.title("Un solo paciente con complicaciones desplaza la media", fontweight="bold")
plt.legend(loc="upper center")
plt.show()
''',
             ideas=["La media se desplaza hacia el valor extremo; la mediana no.",
                    "Para planificar camas, la «estancia típica» la describe mejor la mediana con su dispersión."]),
        dict(ancla="2.2 Dispersión", titulo="El diagrama de caja resume la distribución", fig="caja",
             ideas=["La caja va del primer al tercer cuartil: contiene el 50 % central (RIC).",
                    "Los puntos más allá de 1,5 RIC se señalan como posibles atípicos: hay que revisarlos, no borrarlos."]),
        dict(ancla="2.3 Forma", titulo="La forma decide el resumen", fig="forma",
             ideas=["Simétrica: media ≈ mediana → media y DE.",
                    "Asimétrica: la media se va hacia la cola → mediana y RIC."]),
    ],
    130: [
        dict(ancla="1. Caso clínico", titulo="Chocolate y premios Nobel; presión arterial y creatinina", fig="confusion",
             ideas=["Una correlación real puede deberse a una tercera variable que influye en las dos.",
                    "En el registro, la edad eleva a la vez la PAS y la creatinina."],
             pregunta="¿Qué otra variable podría explicar que dos medidas clínicas suban juntas?"),
        dict(ancla="2.1 Qué gráfico", titulo="Qué gráfico y qué resumen según las variables", fig="que_grafico",
             ideas=["El tipo de las dos variables decide el gráfico y la medida de asociación."]),
        dict(ancla="2.2 Los coeficientes", titulo="Cómo se ve cada coeficiente de correlación", fig="r",
             ideas=["r mide solo la relación <b>lineal</b>, de −1 a 1.",
                    "Una U perfecta puede dar r ≈ 0: mira siempre el gráfico."]),
    ],
}


@figura(90, "curb")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.axis("off")
    filas = [["Mujer, 65 años, PAD 60 mmHg", "2 (edad ≥ 65; PAD ≤ 60)", "0", "✗"], ["Varón, 70 años, PAS 120, PAD 80", "1", "1", "✓"],
             ["Varón, 50 años, FR 30 rpm", "1", "0", "✗"]]
    t = ax.table(cellText=filas, colLabels=["Paciente de prueba", "Esperado (definición)", "Código del asistente", ""], loc="center",
                 cellColours=[["white"] * 3 + ["#D5EFDF" if f[3] == "✓" else "#F7D9D5"] for f in filas], colWidths=[0.42, 0.3, 0.22, 0.06])
    t.auto_set_font_size(False); t.set_fontsize(15); t.scale(1, 2.6)
    ax.set_title("El código no da ningún error… pero falla en las fronteras", fontsize=17)
    return fig


@figura(90, "ciclo")
def _():
    fig, ax = lienzo(12, 6)
    pasos = ["1. Especificar\n(guía clínica)", "2. Escribir las\npruebas", "3. Generar el\ncódigo (IA)", "4. Ejecutar y\nverificar", "5. Corregir\n(o pedir corrección)"]
    ang = np.linspace(90, 90 - 360, 6)[:-1]
    pos = [(50 + 33 * np.cos(np.radians(a)), 50 + 38 * np.sin(np.radians(a))) for a in ang]
    for (x, y), t in zip(pos, pasos):
        caja(ax, x - 11, y - 8, 22, 16, t, tam=14, color=NARANJA if "IA" in t else AZUL, relleno="#FDEFD9" if "IA" in t else AZUL_CLARO)
    for i in range(5):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % 5]
        flecha(ax, x1 + (x2 - x1) * 0.3, y1 + (y2 - y1) * 0.3, x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7, color=GRIS)
    ax.text(50, 50, "¿Pasan todas\nlas pruebas?\n→ parar", ha="center", va="center", fontsize=15, color=VERDE, fontweight="bold")
    return fig


@figura(90, "goodhart")
def _():
    fig, ax = plt.subplots(figsize=(12, 4.3))
    it = np.arange(1, 7)
    des = [55, 70, 82, 92, 100, 100]
    res = [52, 64, 71, 74, 72, 70]
    ax.plot(it, des, "o-", lw=3, ms=9, color=AZUL, label="Pruebas usadas para corregir")
    ax.plot(it, res, "o-", lw=3, ms=9, color=ROJO, label="Pruebas reservadas")
    ax.fill_between(it, res, des, color=ROJO, alpha=0.08)
    ax.text(4.6, 85, "optimismo", color=ROJO, fontsize=15)
    ax.set_xlabel("Iteración del ciclo de mejora"); ax.set_ylabel("Casos correctos (%)"); ax.set_ylim(40, 105)
    ax.legend(loc="lower right")
    return fig


@figura(100, "dataframe")
def _():
    fig, ax = lienzo(12, 5)
    cols = ["id", "sexo", "edad", "peso_kg", "pas_mmHg"]
    filas = [["CV-001", "Mujer", 67, 72.5, 138], ["CV-002", "Hombre", 54, "NaN", 125], ["CV-003", "Mujer", 71, 64.0, 152]]
    for j, c in enumerate(cols):
        caja(ax, 14 + j * 15, 70, 13, 9, c, tam=14, negrita=True, relleno="white" if j != 3 else "#FDEFD9", color=NARANJA if j == 3 else AZUL)
        for i, f in enumerate(filas):
            v = str(f[j])
            ax.text(20.5 + j * 15, 58 - i * 13, v, ha="center", fontsize=15, color=ROJO if v == "NaN" else TINTA, fontweight="bold" if v == "NaN" else "normal")
    for i in range(3):
        ax.text(7, 58 - i * 13, str(i), ha="center", fontsize=15, color=GRIS)
    ax.text(7, 82, "índice", ha="center", fontsize=13, color=GRIS)
    ax.text(65.5, 92, "Series: datos[\"peso_kg\"]  (float)", ha="center", fontsize=14, color=NARANJA)
    ax.text(50, 14, "NaN = dato ausente  ·  datos.shape → (filas, columnas)  ·  datos.dtypes → tipo de cada columna", ha="center", fontsize=14, color=TINTA)
    return fig


@figura(100, "plausible")
def _():
    fig, ax = lienzo(12, 5.5)
    caja(ax, 34, 80, 32, 12, "¿Es fisiológicamente posible?", tam=15, negrita=True)
    caja(ax, 3, 42, 30, 20, "No → error de registro\npeso 680 kg · PAD > PAS", color=ROJO, relleno="#FBE5E1", tam=14)
    caja(ax, 52, 50, 44, 12, "Sí → ¿encaja con el paciente?", tam=15)
    caja(ax, 3, 6, 30, 20, "¿Corrección justificable?\nsí: corregir (1,63 → 163 cm)\nno: convertir en NaN", color=ROJO, relleno="white", tam=13)
    caja(ax, 52, 12, 20, 22, "Sí → atípico real:\nse conserva\n(glucemia 520 en\ncetoacidosis)", color=VERDE, relleno="#E3F4EA", tam=12.5)
    caja(ax, 76, 12, 20, 22, "Dudoso →\nrevisar la\nhistoria", color=NARANJA, relleno="#FDEFD9", tam=13)
    flecha(ax, 42, 79, 22, 63); flecha(ax, 58, 79, 70, 63); flecha(ax, 18, 41, 18, 27); flecha(ax, 66, 49, 62, 35); flecha(ax, 80, 49, 85, 35)
    return fig


@figura(110, "fuentes")
def _():
    fig, ax = lienzo(12, 5)
    tablas = [(3, "cohorte", ["id", "centro", "edad", "diabetes"]), (37, "analiticas", ["id", "hba1c", "creatinina", "ldl"]), (71, "centros", ["centro", "tipo", "población"])]
    for x, n, cs in tablas:
        caja(ax, x, 22, 26, 58, "", relleno="white")
        ax.text(x + 13, 72, n, ha="center", fontsize=17, fontweight="bold", color=AZUL)
        for i, c in enumerate(cs):
            ax.text(x + 13, 60 - i * 10, c, ha="center", fontsize=15, color=ROJO if c in ("id", "centro") else TINTA, fontweight="bold" if c in ("id", "centro") else "normal")
    flecha(ax, 30, 60, 36, 60, color=ROJO, texto="id", tam=14)
    ax.annotate("", xy=(84, 21), xytext=(16, 21), arrowprops=dict(arrowstyle="-|>", color=ROJO, lw=2, connectionstyle="arc3,rad=0.25"))
    ax.set_ylim(-12, 100)
    ax.text(50, -10, "centro", ha="center", fontsize=14, color=ROJO)
    return fig


@figura(110, "joins")
def _():
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    xx, yy = np.meshgrid(np.linspace(0, 10, 400), np.linspace(0, 7, 280))
    A = (xx - 3.8) ** 2 + (yy - 3.5) ** 2 < 2.4 ** 2
    B = (xx - 6.2) ** 2 + (yy - 3.5) ** 2 < 2.4 ** 2
    for ax, (n, m, k) in zip(axs, [("inner", A & B, 358), ("left", A, 400), ("outer", A | B, 402)]):
        ax.imshow(np.where(m, 1.0, np.nan), extent=(0, 10, 0, 7), origin="lower", cmap="Blues", vmin=0, vmax=1.6, alpha=0.9)
        ax.contour(xx, yy, A, levels=[0.5], colors=TINTA, linewidths=2)
        ax.contour(xx, yy, B, levels=[0.5], colors=TINTA, linewidths=2)
        ax.text(2.4, 3.5, "cohorte", ha="center", fontsize=11); ax.text(7.6, 3.5, "analíticas", ha="center", fontsize=11)
        ax.set_title(f'how="{n}"\n{k} filas', fontsize=16); ax.axis("off"); ax.set_aspect("equal")
    return fig


@figura(110, "contingencia")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.axis("off")
    filas = [["CS Norte (urbano)", "38", "12", "50", "24 %"], ["CS Sur (urbano)", "41", "9", "50", "18 %"], ["CS Centro (rural)", "22", "13", "35", "37 %"], ["Total", "101", "34", "135", "25 %"]]
    t = ax.table(cellText=filas, colLabels=["Diabéticos de…", "HbA1c < 8 %", "HbA1c ≥ 8 %", "Total", "% mal control"], loc="center",
                 cellColours=[["white"] * 4 + ["#FDEFD9"]] * 3 + [["#EEE"] * 5], colWidths=[0.28, 0.18, 0.18, 0.14, 0.2])
    t.auto_set_font_size(False); t.set_fontsize(15); t.scale(1, 2.5)
    ax.set_title("Datos ilustrativos", fontsize=13, color=GRIS)
    return fig


@figura(120, "caja")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    datos = [3, 4, 4, 5, 5, 5, 6, 6, 7, 8, 32]
    ax.boxplot(datos, orientation="horizontal", widths=0.5, patch_artist=True,
               boxprops=dict(facecolor=AZUL_CLARO, color=AZUL, lw=2), medianprops=dict(color=ROJO, lw=3),
               flierprops=dict(marker="o", markersize=12, markerfacecolor=ROJO))
    q1, q3 = np.percentile(datos, [25, 75])
    for x, t, xt, yt in [(q1, "Q1", 2, 1.55), (5, "mediana", 9, 1.55), (q3, "Q3", 13, 1.35), (8, "bigote", 15, 1.05)]:
        ax.annotate(t, xy=(x, 1.25 if t != "bigote" else 1.0), xytext=(xt, yt), fontsize=14, color=TINTA, arrowprops=dict(arrowstyle="->", color=GRIS))
    ax.text(32, 1.3, "posible atípico\n(> Q3 + 1,5 RIC)", ha="center", fontsize=14, color=ROJO)
    ax.annotate("", xy=(q1, 0.68), xytext=(q3, 0.68), arrowprops=dict(arrowstyle="<->", color=VERDE, lw=2))
    ax.text((q1 + q3) / 2, 0.52, "RIC = Q3 − Q1", ha="center", fontsize=14, color=VERDE)
    ax.set_yticks([]); ax.set_xlabel("Estancia (días)"); ax.set_ylim(0.4, 1.65)
    return fig


@figura(120, "forma")
def _():
    rng = np.random.default_rng(12)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8))
    for ax, (t, x) in zip(axs, [("Simétrica (PAS)", rng.normal(130, 15, 3000)), ("Asimétrica a la derecha (estancia)", rng.lognormal(1.7, 0.5, 3000)),
                               ("Asimétrica a la izquierda (edad al morir)", 95 - rng.lognormal(2.5, 0.5, 3000))]):
        ax.hist(x, bins=45, color=AZUL_CLARO, ec=AZUL)
        ax.axvline(np.mean(x), color=NARANJA, lw=3, label="media")
        ax.axvline(np.median(x), color=VERDE, lw=3, ls="--", label="mediana")
        ax.set_title(t, fontsize=14); ax.set_yticks([])
    axs[0].legend(fontsize=12)
    plt.tight_layout()
    return fig


@figura(130, "confusion")
def _():
    fig, ax = lienzo(12, 4.8)
    for x0, (z, a, b) in [(0, ("Riqueza del país", "Chocolate", "Premios Nobel")), (52, ("Edad", "PAS", "Creatinina"))]:
        caja(ax, x0 + 14, 72, 20, 12, z, tam=15, negrita=True, color=NARANJA, relleno="#FDEFD9")
        caja(ax, x0 + 1, 20, 18, 12, a, tam=15)
        caja(ax, x0 + 29, 20, 18, 12, b, tam=15)
        flecha(ax, x0 + 20, 71, x0 + 12, 33, color=NARANJA); flecha(ax, x0 + 28, 71, x0 + 36, 33, color=NARANJA)
        ax.annotate("", xy=(x0 + 28, 26), xytext=(x0 + 20, 26), arrowprops=dict(arrowstyle="<->", ls="--", color=GRIS, lw=2))
        ax.text(x0 + 24, 9, "correlación", ha="center", fontsize=13, color=GRIS)
    return fig


@figura(130, "que_grafico")
def _():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.axis("off")
    filas = [["Cuantitativa + cuantitativa", "Dispersión", "r de Pearson o ρ de Spearman", "Edad y PAS"],
             ["Cualitativa + cuantitativa", "Cajas por grupo", "Diferencia de medias o medianas", "HDL según sexo"],
             ["Cualitativa + cualitativa", "Barras agrupadas", "Tabla de contingencia, %", "Diabetes y evento"]]
    t = ax.table(cellText=filas, colLabels=["Variables", "Gráfico", "Resumen", "Ejemplo"], loc="center", colWidths=[0.29, 0.18, 0.35, 0.2], cellLoc="center")
    t.auto_set_font_size(False); t.set_fontsize(13); t.scale(1, 2.8)
    return fig


@figura(130, "r")
def _():
    rng = np.random.default_rng(13)
    fig, axs = plt.subplots(1, 5, figsize=(14, 3.2))
    x = rng.normal(0, 1, 150)
    for ax, r in zip(axs[:4], [-0.9, 0, 0.5, 0.95]):
        y = r * x + np.sqrt(1 - r ** 2) * rng.normal(0, 1, 150)
        ax.scatter(x, y, s=12, color=AZUL)
        ax.set_title(f"r = {np.corrcoef(x, y)[0, 1]:.2f}", fontsize=15)
    y = x ** 2 + rng.normal(0, 0.3, 150)
    axs[4].scatter(x, y, s=12, color=ROJO)
    axs[4].set_title(f"U: r = {np.corrcoef(x, y)[0, 1]:.2f}", fontsize=15, color=ROJO)
    for ax in axs:
        ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    return fig
