from plantilla import Cuaderno

c = Cuaderno("Tema_260_Comparacion_de_mas_de_dos_grupos_ANOVA_y_pruebas_no_parametricas.ipynb")

c.cabecera(
    260,
    "Comparación de más de dos grupos: análisis de la varianza y pruebas no paramétricas",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Explicar por qué no se deben hacer muchas pruebas *t* para comparar más de dos grupos.
2. Aplicar e interpretar el **análisis de la varianza (ANOVA) de un factor** y su tamaño del efecto (η²).
3. Identificar qué grupos difieren con **comparaciones post hoc** (Tukey) y corregir las comparaciones múltiples (Bonferroni y Holm).
4. Aplicar las pruebas no paramétricas de **Mann-Whitney**, **Wilcoxon** y **Kruskal-Wallis** cuando proceda.
5. Reconocer el *p-hacking* y la importancia de registrar el análisis antes de ver los datos.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: ANOVA, post hoc y alternativas | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En la cohorte cardiovascular, la presión sistólica media parece aumentar con el peso: unos 122 mmHg en los pacientes con normopeso, 126 en los que tienen sobrepeso y 133 en los obesos. Un residente propone comparar los grupos de dos en dos con tres pruebas *t*.

Otro residente, revisando la base de datos, ha comparado la glucemia entre los tres centros de salud, después el colesterol, después el HDL, el IMC, la PAS… y ha encontrado que la glucemia «sale significativa» (*p* = 0,04). Quiere enviarlo a un congreso.

Los dos tienen el mismo problema: **cuantas más comparaciones se hacen, más probable es encontrar un resultado significativo por azar**. Hoy veremos cómo comparar varios grupos con una sola prueba, cómo localizar después las diferencias y cómo protegerse de los falsos positivos.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 El problema de las comparaciones múltiples")
c.md("""
Si cada prueba tiene α = 0,05 y las hipótesis nulas son ciertas, la probabilidad de **al menos un falso positivo** en *k* pruebas independientes es $1 - 0{,}95^k$:

| Comparaciones | Probabilidad de al menos un falso positivo |
| --- | --- |
| 1 | 5 % |
| 3 (tres grupos dos a dos) | 14 % |
| 10 (cinco grupos dos a dos) | 40 % |
| 20 | 64 % |
""")
c.titulo(3, "2.2 El ANOVA de un factor")
c.md("""
Contrasta con **una sola prueba** $H_0$: μ₁ = μ₂ = … = μₖ. Descompone la variabilidad total en dos partes:

- **Entre grupos**: cuánto se alejan las medias de los grupos de la media global.
- **Dentro de los grupos**: cuánto varían los pacientes alrededor de la media de su grupo.

$$F = \\frac{\\text{varianza entre grupos}}{\\text{varianza dentro de los grupos}}$$

Si $H_0$ es cierta, *F* será cercano a 1. Un *F* grande indica que las medias difieren más de lo que explicaría la variabilidad entre pacientes. El tamaño del efecto es $\\eta^2$ = SC entre / SC total: la proporción de la variabilidad explicada por el grupo.

Un ANOVA significativo dice que **al menos una media es distinta**, pero no cuál. Para eso se hacen las **comparaciones post hoc**, que controlan el error global (Tukey para todas las parejas).

**Condiciones:** independencia, normalidad aproximada en cada grupo y varianzas parecidas. Si las varianzas difieren mucho, se usa el **ANOVA de Welch**.
""")
c.titulo(3, "2.3 Correcciones por comparaciones múltiples")
c.md("""
| Método | Cómo funciona | Característica |
| --- | --- | --- |
| Bonferroni | Multiplica cada *p* por el número de comparaciones *k* | Sencillo, muy conservador |
| Holm | Ordena los *p* y aplica umbrales escalonados | Siempre al menos tan potente como Bonferroni; recomendado |
| Tukey | Específico para todas las parejas tras un ANOVA | El estándar post hoc |
""")
c.titulo(3, "2.4 Pruebas no paramétricas")
c.md("""
Trabajan con los **rangos** (el orden) de los datos en lugar de con sus valores, así que no suponen normalidad y son robustas a los atípicos. Contrastan si una distribución tiende a dar valores mayores que otra.

| Diseño | Paramétrica | No paramétrica |
| --- | --- | --- |
| Dos grupos independientes | *t* de Welch | **Mann-Whitney** |
| Dos medidas apareadas | *t* apareada | **Wilcoxon** de los rangos con signo |
| Más de dos grupos independientes | ANOVA | **Kruskal-Wallis** |

Úsalas con muestras pequeñas y distribuciones muy asimétricas, con atípicos que no son errores o con variables **ordinales** (escalas de dolor, de Rankin, niveles de triaje).
""")

c.titulo(2, "3. Demostración: ANOVA, post hoc y alternativas (20 min)")
c.titulo(3, "3.1 PAS según la categoría de IMC")
c.code("""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")
categorias = ["Normopeso", "Sobrepeso", "Obesidad"]
cohorte["categoria_imc"] = pd.cut(cohorte["imc"], [0, 25, 30, 100], labels=categorias, right=False)
datos = cohorte.dropna(subset=["pas_mmHg", "categoria_imc"])

print(datos.groupby("categoria_imc", observed=True)["pas_mmHg"].agg(["count", "mean", "std"]).round(1))

plt.figure(figsize=(7, 4))
sns.boxplot(data=datos, x="categoria_imc", y="pas_mmHg", order=categorias)
plt.xlabel("Categoría de IMC (< 25 · 25 a 29,9 · ≥ 30 kg/m²)")
plt.ylabel("PAS (mmHg)")
plt.show()
""")
c.md("""
Las desviaciones típicas son parecidas (la mayor no llega a 1,5 veces la menor) y las distribuciones son razonablemente simétricas: el ANOVA clásico es adecuado.
""")

c.titulo(3, "3.2 El ANOVA")
c.code("""
grupos = [datos.loc[datos["categoria_imc"] == k, "pas_mmHg"] for k in categorias]
anova = stats.f_oneway(*grupos)

media_global = datos["pas_mmHg"].mean()
sc_entre = sum(len(g) * (g.mean() - media_global) ** 2 for g in grupos)
sc_total = ((datos["pas_mmHg"] - media_global) ** 2).sum()
k, n = len(grupos), len(datos)

print(f"F = {anova.statistic:.2f} con {k - 1} y {n - k} grados de libertad, p = {anova.pvalue:.1e}")
print(f"η² = {sc_entre / sc_total:.3f}")
""")
c.md("""
Hay evidencia de que la PAS media no es igual en las tres categorías. Pero η² indica que la categoría de IMC explica solo una pequeña parte de la variabilidad de la PAS entre pacientes: influyen muchos otros factores (edad, tratamiento, sal, genética). Esto es habitual en Medicina: un factor puede tener un efecto real y relevante sobre la media sin explicar gran parte de la variabilidad individual.
""")

c.titulo(3, "3.3 ¿Qué grupos difieren? Tukey")
c.code("""
tukey = stats.tukey_hsd(*grupos)
ic = tukey.confidence_interval(confidence_level=0.95)
for i in range(k):
    for j in range(i + 1, k):
        print(f"{categorias[j]:>10} − {categorias[i]:<10}: {-tukey.statistic[i, j]:5.1f} mmHg "
              f"(IC 95 %: {-ic.high[i, j]:5.1f} a {-ic.low[i, j]:5.1f}) · p ajustada = {tukey.pvalue[i, j]:.4f}")
""")

c.md("""
Los obesos tienen una PAS media unos 11 mmHg mayor que los pacientes con normopeso y unos 7 mmHg mayor que los que tienen sobrepeso. La diferencia entre sobrepeso y normopeso (4 mmHg) no alcanza la significación tras el ajuste: su IC incluye el 0.
""")

c.titulo(3, "3.4 La alternativa no paramétrica: Kruskal-Wallis")
c.code("""
kw = stats.kruskal(*grupos)
print(f"Kruskal-Wallis: H = {kw.statistic:.2f}, p = {kw.pvalue:.1e}")
print("Medianas:", datos.groupby("categoria_imc", observed=True)["pas_mmHg"].median().to_dict())
""")
c.md("""
Con datos bien comportados, el ANOVA y Kruskal-Wallis llegan a la misma conclusión. El ANOVA aporta además las diferencias de medias con sus intervalos, que son más fáciles de interpretar clínicamente.
""")

c.titulo(3, "3.5 La búsqueda del residente: corregir las comparaciones múltiples")
c.code("""
from statsmodels.stats.multitest import multipletests

variables = ["pas_mmHg", "pad_mmHg", "colesterol_mg_dl", "hdl_mg_dl", "glucemia_mg_dl", "imc", "peso_kg", "edad"]
valores_p = []
for v in variables:
    x = cohorte.dropna(subset=[v])
    valores_p.append(stats.f_oneway(*[x.loc[x["centro"] == ce, v] for ce in x["centro"].unique()]).pvalue)

_, p_bonf, _, _ = multipletests(valores_p, method="bonferroni")
_, p_holm, _, _ = multipletests(valores_p, method="holm")
resultados = pd.DataFrame({"p sin corregir": valores_p, "p Bonferroni": p_bonf, "p Holm": p_holm}, index=variables)
resultados.round(3)
""")
c.md("""
La glucemia «significativa» deja de serlo al tener en cuenta que se han hecho 8 comparaciones. Con 8 variables sin ninguna diferencia real, lo esperable es que alguna salga con *p* < 0,05 un tercio de las veces. El resultado puede ser real, pero es una **hipótesis para un nuevo estudio**, no una conclusión.
""")

c.titulo(3, "3.6 Simulación: el p-hacking funciona")
c.code("""
rng = np.random.default_rng(seed=260)
estudios_con_hallazgo = 0
for _ in range(2000):
    # 20 variables sin ninguna diferencia real entre 3 centros de 50 pacientes
    p = [stats.f_oneway(*rng.normal(0, 1, (3, 50))).pvalue for _ in range(20)]
    estudios_con_hallazgo += min(p) < 0.05
print(f"Estudios con al menos un «hallazgo» significativo: {estudios_con_hallazgo / 2000:.0%}")
""")
c.md("""
Casi dos de cada tres estudios encuentran algo «significativo» en datos que son puro ruido. Es la razón de que los ensayos clínicos deban **registrar** su variable principal y su plan de análisis antes de empezar (ClinicalTrials.gov, EU CTR), y de que los análisis no previstos se presenten como exploratorios.
""")

c.titulo(3, "Ampliación: Mann-Whitney y Wilcoxon")
c.md("""
Dolor en una escala de 0 a 10 tras dos técnicas analgésicas en 14 y 15 pacientes (variable ordinal, muestras pequeñas), y en 12 pacientes antes y después de una sesión de fisioterapia.
""")
c.code("""
tecnica_a = np.array([2, 3, 3, 4, 2, 5, 3, 1, 4, 3, 2, 6, 3, 2])
tecnica_b = np.array([4, 5, 6, 3, 5, 7, 4, 6, 5, 8, 4, 5, 6, 3, 5])
mw = stats.mannwhitneyu(tecnica_a, tecnica_b)
print(f"Medianas: A {np.median(tecnica_a):.0f} · B {np.median(tecnica_b):.0f} · Mann-Whitney p = {mw.pvalue:.4f}")

antes = np.array([7, 6, 8, 5, 7, 9, 6, 7, 8, 6, 5, 7])
despues = np.array([5, 5, 6, 5, 4, 7, 6, 5, 6, 4, 4, 6])
w = stats.wilcoxon(despues, antes)
print(f"Mediana del cambio: {np.median(despues - antes):.1f} puntos · Wilcoxon p = {w.pvalue:.4f}")
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Hacer todas las pruebas *t* dos a dos** sin corregir.

**Concluir qué grupos difieren a partir del ANOVA**, sin post hoc.

**Buscar significación variable tras variable** y presentar solo la que sale.

**Creer que las pruebas no paramétricas «no tienen supuestos»:** requieren independencia, y Mann-Whitney compara distribuciones, no exactamente medianas.

**Usar pruebas no paramétricas por defecto** con muestras grandes y datos razonables: se pierde la estimación del efecto en unidades clínicas.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 260 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** elegir la prueba adecuada para ocho diseños y calcular la probabilidad de falsos positivos con *k* comparaciones.
2. **Misión clínica (con pistas):** comparar la PAS entre los cuatro grupos de edad de la cohorte con ANOVA y Tukey, y redactar el resultado.
3. **Misión reto (con asistente):** pedir al asistente que «encuentre algo significativo» en la cohorte, aplicar la corrección de Holm a todo lo que haya probado y escribir el párrafo de limitaciones.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("Quieres comparar la HbA1c media entre cuatro pautas de insulina. ¿Qué análisis haces?", [
        ("Un ANOVA y, si es significativo, comparaciones post hoc de Tukey", True, "Correcto: una sola prueba global y después las parejas con control del error."),
        ("Seis pruebas t, una por pareja", False, "La probabilidad de algún falso positivo sería cercana al 26 %."),
        ("Una ji cuadrado", False, "La variable es cuantitativa."),
        ("McNemar", False, "McNemar es para proporciones apareadas."),
    ]),
    ("Un ANOVA da p = 0,002. ¿Qué puedes concluir?", [
        ("Que al menos una media difiere de las demás", True, "Correcto: para saber cuáles hacen falta las comparaciones post hoc."),
        ("Que todas las medias son distintas entre sí", False, "Puede que solo un grupo difiera."),
        ("Que el factor explica el 99,8 % de la variabilidad", False, "Eso lo indica η², no el valor p."),
        ("Que la diferencia es clínicamente relevante", False, "Hay que ver la magnitud de las diferencias."),
    ]),
    ("Haces 5 contrastes y obtienes p = 0,012 en uno. Con la corrección de Bonferroni, ¿cuál es su valor p ajustado?", [
        ("0,06", True, "Correcto: 0,012 × 5 = 0,06, que ya no es menor de 0,05."),
        ("0,012", False, "Hay que ajustar por el número de comparaciones."),
        ("0,0024", False, "Se multiplica por k, no se divide."),
        ("0,05", False, "Revisa la regla."),
    ]),
    ("Comparas la puntuación de la escala de Rankin (0 a 6) entre tres tratamientos con 15 pacientes cada uno. ¿Qué prueba usas?", [
        ("Kruskal-Wallis", True, "Correcto: variable ordinal y más de dos grupos independientes."),
        ("ANOVA", False, "Con una escala ordinal de pocos valores, mejor una prueba de rangos."),
        ("Wilcoxon de los rangos con signo", False, "Es para dos medidas apareadas."),
        ("Mann-Whitney", False, "Es para dos grupos."),
    ]),
    ("¿Por qué deben registrarse los ensayos clínicos y su análisis principal antes de empezar?", [
        ("Para evitar elegir después de ver los datos la variable o el análisis que salen significativos", True, "Correcto: protege frente al p-hacking y al sesgo de publicación."),
        ("Porque así el valor p es siempre menor", False, "No modifica el valor p."),
        ("Para poder usar pruebas no paramétricas", False, "No tiene relación."),
        ("Para no tener que corregir por comparaciones múltiples", False, "Si hay varias variables principales, sigue siendo necesario corregir."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Comparar *k* grupos dos a dos multiplica los falsos positivos.
- El ANOVA contrasta con una sola prueba si alguna media difiere; Tukey localiza qué parejas.
- Con muchas comparaciones, corrige con Holm (o Bonferroni).
- Mann-Whitney, Wilcoxon y Kruskal-Wallis para variables ordinales, muestras pequeñas o datos muy asimétricos.
- Lo que se encuentra buscando sin plan es una hipótesis, no una conclusión.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Análisis de la varianza (ANOVA) | Contraste de la igualdad de las medias de más de dos grupos |
| Estadístico *F* | Cociente entre la varianza entre grupos y la varianza dentro de los grupos |
| η² (eta cuadrado) | Proporción de la variabilidad total explicada por el factor |
| Comparaciones post hoc | Comparaciones entre parejas de grupos tras un ANOVA significativo, con control del error |
| Prueba de Tukey | Método post hoc para todas las parejas de grupos |
| Corrección de Bonferroni | Ajuste que multiplica cada valor p por el número de comparaciones |
| Método de Holm | Ajuste escalonado de los valores p, más potente que Bonferroni |
| Prueba de Kruskal-Wallis | Alternativa no paramétrica al ANOVA de un factor |
| Prueba de Wilcoxon de los rangos con signo | Alternativa no paramétrica a la *t* apareada |
| *p-hacking* | Multiplicar los análisis hasta encontrar un resultado significativo |
""")

c.titulo(2, "Para saber más")
c.md("""
- Bland JM, Altman DG. Multiple significance tests: the Bonferroni method. *BMJ*. 1995;310(6973):170.
- Holm S. A simple sequentially rejective multiple test procedure. *Scand J Stat*. 1979;6(2):65-70.
- Simmons JP, Nelson LD, Simonsohn U. False-positive psychology: undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychol Sci*. 2011;22(11):1359-1366.
""")

c.pie(260)
print(c.guardar("../cuadernos"))
