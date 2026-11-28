from plantilla import Cuaderno

c = Cuaderno("Tema_120_Estadistica_descriptiva_univariante.ipynb")

c.cabecera(
    120,
    "Estadística descriptiva univariante: medidas de tendencia central, dispersión y forma",
    "Módulo 3. Procesado inicial de datos",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Calcular e interpretar la media, la mediana y la moda.
2. Calcular e interpretar el rango, la varianza, la desviación típica, el rango intercuartílico y el coeficiente de variación.
3. Describir la forma de una distribución: simetría y asimetría.
4. Elegir el resumen adecuado según la forma de la distribución: media y desviación típica, o mediana y rango intercuartílico.
5. Representar una variable cuantitativa con un histograma y un diagrama de caja.
6. Redactar la descripción de una variable como en la «Tabla 1» de un artículo.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: describir variables clínicas | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un hospital quiere conocer la **estancia** de los pacientes ingresados por neumonía. Revisa 11 ingresos (sintéticos) y obtiene, en días:

**3, 4, 4, 5, 5, 5, 6, 6, 7, 8, 32**

El paciente de 32 días tuvo complicaciones y pasó por la UCI. La media es 7,7 días; la mediana, 5 días.

La gerencia quiere usar la cifra para planificar camas. Si dice «la estancia media es de casi 8 días», sobreestima lo que ocurre a la mayoría de los pacientes. Si dice «la estancia típica es de 5 días» y la acompaña de su dispersión, describe mejor la realidad.

Elegir bien el **resumen** de una variable no es un detalle técnico: cambia las decisiones que se toman con él.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Tendencia central")
c.diagrama('Decisión: si la variable es simétrica y sin valores extremos, media ± DE; si no, mediana [Q1–Q3].')
c.md("""
| Medida | Definición | Ventaja | Inconveniente |
| --- | --- | --- | --- |
| **Media** $\\bar{x}$ | Suma de los valores dividida entre su número | Usa toda la información | Muy sensible a los valores extremos |
| **Mediana** | Valor central de los datos ordenados (percentil 50) | Robusta frente a valores extremos | Ignora la magnitud de los extremos |
| **Moda** | Valor más frecuente | Útil en variables categóricas | Puede no ser única |

$$\\bar{x} = \\frac{1}{n}\\sum_{i=1}^{n} x_i$$
""")
c.titulo(3, "2.2 Dispersión")
c.md("""
| Medida | Definición | Se acompaña de |
| --- | --- | --- |
| Rango | Máximo − mínimo | — |
| **Varianza** $s^2$ | Media de las desviaciones al cuadrado respecto a la media (dividiendo entre $n-1$) | — |
| **Desviación típica** $s$ | Raíz cuadrada de la varianza; en las unidades de la variable | Media |
| **Rango intercuartílico** (RIC) | Q3 − Q1: amplitud del 50 % central de los datos | Mediana |
| Coeficiente de variación | $s / \\bar{x}$, en porcentaje: dispersión relativa | Comparar variables con distintas unidades |

$$s = \\sqrt{\\frac{1}{n-1}\\sum_{i=1}^{n}(x_i - \\bar{x})^2}$$

Se divide entre $n-1$, y no entre $n$, por una razón. En una muestra, la media se calcula con los mismos datos. Por eso, las desviaciones respecto a ella tienden a ser algo menores que respecto a la media real de la población.
""")
c.titulo(3, "2.3 Forma")
c.md("""
| Forma | Relación entre media y mediana | Ejemplo clínico |
| --- | --- | --- |
| Simétrica | Media ≈ mediana | Presión arterial sistólica, talla |
| Asimétrica a la derecha (positiva) | Media > mediana | Estancia hospitalaria, creatinina, triglicéridos |
| Asimétrica a la izquierda (negativa) | Media < mediana | Edad en una unidad de geriatría, puntuación de Apgar |

**Regla para la Tabla 1 de un artículo:**

- Variable aproximadamente simétrica: **media ± desviación típica**.
- Variable asimétrica o con valores extremos: **mediana [Q1–Q3]**, es decir, mediana y rango intercuartílico.
""")

c.titulo(2, "3. Demostración: describir variables clínicas (20 min)")
c.titulo(3, "3.1 Cálculo a mano y comprobación")
c.md("""
Con las 11 estancias del caso, calculamos paso a paso y comprobamos con Python.
""")
c.code("""
import numpy as np
import pandas as pd

estancias = pd.Series([3, 4, 4, 5, 5, 5, 6, 6, 7, 8, 32])

n = len(estancias)
media = estancias.sum() / n
desviaciones = estancias - media
varianza = (desviaciones ** 2).sum() / (n - 1)
desviacion_tipica = varianza ** 0.5

print(f"n = {n}")
print(f"Media: {media:.2f} días")
print(f"Varianza: {varianza:.2f} días²")
print(f"Desviación típica: {desviacion_tipica:.2f} días")
""")
c.code("""
print(f"Pandas → media {estancias.mean():.2f}, desviación típica {estancias.std():.2f}")
print(f"Mediana: {estancias.median()} días · Moda: {estancias.mode().tolist()} días")
""")
c.md("""
La mediana es el sexto de los 11 valores ordenados: 5 días. La moda también es 5: aparece tres veces.
""")

c.titulo(3, "3.2 Cuartiles, rango intercuartílico y efecto del valor extremo")
c.code("""
q1, q3 = estancias.quantile([0.25, 0.75])
print(f"Q1 = {q1} · Q3 = {q3} · RIC = {q3 - q1} días")
print(f"Rango: {estancias.min()} a {estancias.max()} días")

sin_extremo = estancias[estancias < 32]
print(f"\\nSin el paciente de 32 días: media {sin_extremo.mean():.2f} · mediana {sin_extremo.median()}")
print(f"Con él:                       media {estancias.mean():.2f} · mediana {estancias.median()}")
""")
c.md("""
Un solo paciente desplaza la media más de 2 días; la mediana apenas cambia. Por eso, en variables con valores extremos, la mediana y el RIC describen mejor lo típico.
""")

c.titulo(3, "3.3 Describir una variable del registro")
c.code("""
DATOS = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/"
cohorte = pd.read_csv(DATOS + "cohorte_limpia.csv")
analiticas = pd.read_csv(DATOS + "analiticas.csv")
datos = cohorte.merge(analiticas, on="id", how="left")


def describir(serie, unidad):
    \"\"\"Resumen descriptivo completo de una variable cuantitativa.\"\"\"
    q1, q3 = serie.quantile([0.25, 0.75])
    return pd.Series({
        "n": serie.notna().sum(),
        "media": serie.mean(),
        "desviación típica": serie.std(),
        "mediana": serie.median(),
        "Q1": q1,
        "Q3": q3,
        "mínimo": serie.min(),
        "máximo": serie.max(),
        "CV (%)": serie.std() / serie.mean() * 100,
        "asimetría": serie.skew(),
    }, name=f"{serie.name} ({unidad})").round(2)


pd.concat([
    describir(datos["pas_mmHg"], "mmHg"),
    describir(datos["creatinina_mg_dl"], "mg/dL"),
    describir(datos["glucemia_mg_dl"], "mg/dL"),
], axis=1)
""")
c.md("""
El coeficiente de **asimetría** es cercano a 0 en distribuciones simétricas. Es positivo si hay cola a la derecha y negativo si la cola está a la izquierda. La PAS es casi simétrica (media ≈ mediana); la creatinina y la glucemia son asimétricas a la derecha (media > mediana).
""")

c.titulo(3, "3.4 Histograma con media y mediana")
c.code("""
import matplotlib.pyplot as plt

fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
for eje, variable, unidad in zip(ejes, ["pas_mmHg", "creatinina_mg_dl"], ["mmHg", "mg/dL"]):
    serie = datos[variable].dropna()
    eje.hist(serie, bins=25, color="lightsteelblue", edgecolor="white")
    eje.axvline(serie.mean(), color="firebrick", label=f"Media {serie.mean():.2f}")
    eje.axvline(serie.median(), color="black", linestyle="--", label=f"Mediana {serie.median():.2f}")
    eje.set_xlabel(f"{variable} ({unidad})")
    eje.set_ylabel("Número de pacientes")
    eje.legend()
ejes[0].set_title("Distribución simétrica")
ejes[1].set_title("Distribución asimétrica a la derecha")
plt.tight_layout()
plt.show()
""")

c.titulo(3, "3.5 Diagrama de caja")
c.md("""
El **diagrama de caja** (*boxplot*) resume la distribución en cinco números. La caja va de Q1 a Q3 y la línea interior es la mediana. Los bigotes llegan hasta el último valor dentro de 1,5 × RIC. Los puntos aislados son los valores atípicos según el criterio de Tukey (Tema 100).
""")
c.code("""
plt.figure(figsize=(6, 4))
plt.boxplot(datos["creatinina_mg_dl"].dropna(), widths=0.5)
plt.ylabel("Creatinina sérica (mg/dL)")
plt.xticks([])
plt.title("Diagrama de caja de la creatinina")
plt.show()
""")
c.md("""
Comparar grupos con diagramas de caja es muy eficaz:
""")
c.code("""
grupos = [datos.loc[datos["centro"] == centro, "pas_mmHg"].dropna() for centro in ["CS Norte", "CS Sur", "CS Centro"]]
plt.figure(figsize=(7, 4))
plt.boxplot(grupos)
plt.xticks([1, 2, 3], ["CS Norte", "CS Sur", "CS Centro"])
plt.ylabel("Presión arterial sistólica (mmHg)")
plt.title("PAS por centro de salud")
plt.show()
""")

c.titulo(3, "3.6 La descripción para la Tabla 1")
c.code("""
def tabla1(serie, unidad, decimales=1):
    \"\"\"Devuelve media ± DE si la variable es aproximadamente simétrica, y mediana [Q1-Q3] si no.\"\"\"
    s = serie.dropna()
    if abs(s.skew()) < 0.5:
        return f"{s.mean():.{decimales}f} ± {s.std():.{decimales}f} {unidad}"
    q1, q3 = s.quantile([0.25, 0.75])
    return f"{s.median():.{decimales}f} [{q1:.{decimales}f}–{q3:.{decimales}f}] {unidad}"


for variable, unidad, d in [("edad", "años", 1), ("pas_mmHg", "mmHg", 1),
                            ("imc", "kg/m²", 1), ("creatinina_mg_dl", "mg/dL", 2)]:
    print(f"{variable:>18}: {tabla1(datos[variable], unidad, d)}")
""")
c.md("""
El umbral de 0,5 para el coeficiente de asimetría es una **regla práctica**, no un criterio universal. La decisión final se toma también mirando el histograma y con criterio clínico.
""")

c.titulo(3, "Ampliación: la trampa de numpy y la desviación típica")
c.md("""
Pandas divide entre $n - 1$ (desviación típica **muestral**), pero `numpy.std()` divide por defecto entre $n$ (poblacional). Con muestras pequeñas la diferencia se nota. Un asistente de IA puede usar cualquiera de las dos sin avisar.
""")
c.code("""
print(f"pandas .std():          {estancias.std():.3f}")
print(f"numpy np.std():         {np.std(estancias):.3f}   ← divide entre n")
print(f"numpy np.std(ddof=1):   {np.std(estancias, ddof=1):.3f}")
""")

c.titulo(3, "Ampliación: la regla de la media ± 2 desviaciones típicas")
c.md("""
En una distribución **aproximadamente normal**, alrededor del 95 % de los valores están entre la media − 2 DE y la media + 2 DE. En una distribución asimétrica esta regla falla, y a veces da límites imposibles:
""")
c.code("""
print(f"Estancias: media − 2 DE = {estancias.mean() - 2 * estancias.std():.1f} días  ← una estancia negativa no existe")
""")
c.md("""
Atención a «media ± DE» en una variable que no puede ser negativa. Si la DE es mayor que la mitad de la media, la distribución es asimétrica. Ese resumen no es el adecuado.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Describir con media ± DE una variable claramente asimétrica**, como la estancia o la creatinina.

**Confundir la desviación típica con el error estándar.** La DE describe la dispersión de los pacientes; el error estándar, la precisión de la media. Lo veremos en el Tema 200.

**Eliminar valores extremos reales para que la media «quede mejor».**

**Comparar dispersiones de variables con unidades distintas** con la DE en lugar del coeficiente de variación.

**Dar demasiados decimales:** una presión arterial media de 127,4183 mmHg aparenta una precisión que la medición no tiene.
""")

c.titulo(3, "Ampliación: La curtosis")
c.md("""
La asimetría dice hacia qué lado está la cola. La **curtosis** dice cuánto peso tienen las colas: cuántos valores extremos hay comparado con una normal.

pandas calcula el **exceso de curtosis** (`.kurt()`). Vale 0 en una normal. Si es positivo, hay más valores extremos que en una normal (colas pesadas). Si es negativo, hay menos (colas ligeras).

**En tus materiales SIMUSTAT:** [Tema 200. Análisis descriptivo de variables](https://colab.research.google.com/drive/1dfJOHT5wc2pnlZKbkqWTzqOQ0fLK7kdN), apartado 5 (medidas de forma).
""")
c.code("""
for variable in ["pas_mmHg", "glucemia_mg_dl", "hdl_mg_dl"]:
    x = cohorte[variable].dropna()
    print(f"{variable:16}  asimetría = {x.skew():5.2f}   exceso de curtosis = {x.kurt():5.2f}")
""")
c.md("""
Una curtosis alta avisa de que hay valores extremos. En ese caso, revisa si son errores (Tema 100). Si son reales, la media y la DE resumen mal la variable: usa la mediana y el RIC.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 120 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** calcular a mano la media, la mediana y la desviación típica de 7 valores de hemoglobina.
2. **Misión clínica (con pistas):** describir el colesterol LDL y la HbA1c de la cohorte y decidir el resumen adecuado para cada una.
3. **Misión reto (con asistente):** pedir al asistente la descripción de cuatro variables, comprobar si usa $n$ o $n-1$ y corregir los resúmenes inadecuados.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("Las estancias de 5 pacientes son 2, 3, 3, 4 y 18 días. ¿Cuál es la mediana?", [
        ("3 días", True, "Correcto: es el valor central de los datos ordenados."),
        ("6 días", False, "Esa es la media, que arrastra el valor de 18 días."),
        ("4 días", False, "4 es el cuarto valor, no el central."),
        ("16 días", False, "Ese es el rango."),
    ]),
    ("¿Cómo debe describirse la creatinina de una cohorte con una clara asimetría a la derecha?", [
        ("Mediana [Q1–Q3]", True, "Correcto: la mediana y el RIC son robustos frente a la cola de valores altos."),
        ("Media ± desviación típica", False, "En variables asimétricas, la media y la DE describen mal lo típico."),
        ("Moda", False, "La moda sola no describe la dispersión."),
        ("Mínimo y máximo", False, "El rango depende solo de los dos valores extremos."),
    ]),
    ("En una muestra, la media es 7,7 y la mediana 5. ¿Qué forma tiene probablemente la distribución?", [
        ("Asimétrica a la derecha", True, "Correcto: unos pocos valores altos elevan la media por encima de la mediana."),
        ("Simétrica", False, "En una distribución simétrica media y mediana son parecidas."),
        ("Asimétrica a la izquierda", False, "En ese caso la media sería menor que la mediana."),
        ("No se puede saber nada", False, "La relación entre media y mediana es un buen indicio de la forma."),
    ]),
    ("¿Por qué la desviación típica muestral divide entre n − 1?", [
        ("Porque las desviaciones respecto a la media muestral tienden a ser menores que respecto a la poblacional", True, "Correcto: dividir entre n − 1 corrige esa infraestimación."),
        ("Para que el resultado sea siempre un número entero", False, "No tiene que ver con los enteros."),
        ("Porque se excluye el valor máximo", False, "Se usan todos los valores."),
        ("Es una convención sin justificación", False, "Tiene una justificación estadística: corregir el sesgo."),
    ]),
    ("Quieres comparar la variabilidad del peso (kg) y de la glucemia (mg/dL) en la cohorte. ¿Qué medida usas?", [
        ("El coeficiente de variación", True, "Correcto: es una medida relativa, sin unidades."),
        ("La desviación típica", False, "Está en las unidades de cada variable y no son comparables."),
        ("La varianza", False, "Tiene las unidades al cuadrado: todavía menos comparable."),
        ("El rango", False, "Depende de las unidades y de los extremos."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La media usa todos los datos pero se deja arrastrar por los extremos; la mediana es robusta.
- La desviación típica acompaña a la media; el rango intercuartílico, a la mediana.
- La forma de la distribución decide el resumen: media ± DE si es simétrica, mediana [Q1–Q3] si es asimétrica.
- El histograma y el diagrama de caja muestran lo que los números resumen.
- Comprueba siempre si el cálculo de la desviación típica divide entre $n$ o $n-1$.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Media | Suma de los valores dividida entre su número |
| Mediana | Valor que deja la mitad de los datos por debajo y la mitad por encima |
| Moda | Valor más frecuente |
| Percentil | Valor que deja por debajo un porcentaje dado de los datos |
| Cuartiles | Percentiles 25 (Q1), 50 (Q2, la mediana) y 75 (Q3) |
| Varianza | Media de las desviaciones al cuadrado respecto a la media |
| Desviación típica | Raíz cuadrada de la varianza |
| Coeficiente de variación | Desviación típica dividida entre la media |
| Asimetría | Grado en que una distribución se aparta de la simetría |
| Diagrama de caja | Gráfico que resume la distribución con la mediana, los cuartiles y los valores atípicos |
""")

c.titulo(2, "Para saber más")
c.md("""
- Altman DG, Bland JM. Quartiles, quintiles, centiles, and other quantiles. *BMJ*. 1994;309(6960):996.
- Altman DG, Bland JM. Standard deviations and standard errors. *BMJ*. 2005;331(7521):903.
- [Pandas: estadística descriptiva](https://pandas.pydata.org/docs/user_guide/basics.html#descriptive-statistics)
""")

c.pie(120)
print(c.guardar("../cuadernos"))
