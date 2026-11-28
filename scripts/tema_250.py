from plantilla import Cuaderno

c = Cuaderno("Tema_250_Inferencia_sobre_medias_pruebas_t_independientes_y_relacionadas.ipynb")

c.cabecera(
    250,
    "Inferencia sobre medias: pruebas t para muestras independientes y relacionadas",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Elegir entre la prueba *t* para una muestra, para dos muestras independientes y para muestras relacionadas.
2. Aplicar la prueba *t* de Welch y saber por qué es la opción recomendada para dos grupos independientes.
3. Estimar la diferencia de medias con su intervalo de confianza y el tamaño del efecto (*d* de Cohen).
4. Comprobar las condiciones de aplicación de forma gráfica y razonada.
5. Reconocer cuándo conviene una alternativa no paramétrica.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: las tres pruebas t | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En la cohorte cardiovascular, el colesterol HDL medio es de unos 49 mg/dL en los hombres y de unos 58 mg/dL en las mujeres. Antes de proponer puntos de corte distintos por sexo en el protocolo del centro, el equipo quiere saber dos cosas. ¿Es real esa diferencia en la población? ¿**De qué tamaño** es?

Además, una enfermera ha medido la presión arterial a 30 hipertensos **antes y después** de 8 semanas de un programa de reducción de sal. Quiere saber si la PAS ha bajado.

Las dos preguntas comparan **medias**, pero la segunda usa los **mismos** pacientes dos veces. Cada una requiere una versión distinta de la prueba *t* de Student.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Las tres pruebas t")
c.md("""
| Prueba | Pregunta | Hipótesis nula | Ejemplo |
| --- | --- | --- | --- |
| *t* para una muestra | ¿La media es distinta de un valor de referencia? | μ = μ₀ | ¿La HbA1c media de nuestros diabéticos difiere del objetivo del 7 %? |
| *t* para dos muestras independientes | ¿Difieren las medias de dos grupos distintos? | μ₁ = μ₂ | HDL en hombres y mujeres |
| *t* para muestras relacionadas (apareadas) | ¿Cambia la media en los mismos individuos? | μ de las diferencias = 0 | PAS antes y después del programa |

En todas, el estadístico tiene la misma estructura:

$$t = \\frac{\\text{diferencia observada} - \\text{diferencia bajo } H_0}{\\text{error estándar de la diferencia}}$$
""")
c.titulo(3, "2.2 Welch o Student clásica")
c.diagrama('Simulación con medias iguales y varianzas distintas: la t clásica da muchos más falsos positivos que el 5 % nominal; Welch, alrededor del 5 %.', nombre="e2_2")
c.md("""
La prueba *t* clásica para dos muestras supone que las **varianzas son iguales** en los dos grupos. La versión de **Welch** no lo supone y ajusta los grados de libertad. Cuando las varianzas son iguales, las dos dan casi lo mismo; cuando no lo son, la clásica puede equivocarse. Por eso se recomienda usar **Welch por defecto**, sin contrastar antes la igualdad de varianzas.
""")
c.titulo(3, "2.3 Muestras relacionadas")
c.md("""
Con datos apareados se calcula para cada paciente la **diferencia** (después − antes) y se aplica la *t* para una muestra a esas diferencias. La prueba apareada elimina la variabilidad entre pacientes. Por eso es mucho más potente que comparar los dos momentos como grupos independientes (igual que McNemar frente a la *z* en el Tema 240).
""")
c.titulo(3, "2.4 Condiciones de aplicación")
c.diagrama('Tres comprobaciones antes de la prueba t: independencia, normalidad o n ≥ 30 y ausencia de atípicos extremos, con la alternativa de cada una.')
c.md("""
| Condición | Cómo valorarla | Si no se cumple |
| --- | --- | --- |
| Observaciones independientes (dentro de cada grupo) | Por el diseño | Otro método (datos agrupados, medidas repetidas) |
| Normalidad de la variable (o de las diferencias) | Histograma y gráfico Q-Q; con *n* ≥ 30 por grupo la prueba es robusta por el teorema central del límite | Transformación (logaritmo) o prueba no paramétrica |
| Ausencia de atípicos extremos | Diagrama de caja | Revisar si son errores (Tema 100); prueba no paramétrica |

Los contrastes formales de normalidad (Shapiro-Wilk) tienen poco valor: con muestras pequeñas casi nunca detectan nada, y con muestras grandes detectan desviaciones irrelevantes.
""")
c.titulo(3, "2.5 Tamaño del efecto: d de Cohen")
c.diagrama('Tres pares de curvas normales con d de Cohen 0,2, 0,5 y 0,8 y su solapamiento.', nombre="e2_5")
c.md("""
$$d = \\frac{\\bar{x}_1 - \\bar{x}_2}{s_{\\text{conjunta}}}$$

Expresa la diferencia en unidades de desviación típica. Orientación habitual: 0,2 pequeño, 0,5 mediano, 0,8 grande. Para decidir la relevancia clínica, sin embargo, importa más la diferencia en las **unidades originales** (mg/dL, mmHg) comparada con la mínima diferencia clínicamente importante.
""")

c.titulo(2, "3. Demostración: las tres pruebas t (20 min)")
c.titulo(3, "3.1 Dos muestras independientes: HDL por sexo")
c.code("""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")
hdl = cohorte.dropna(subset=["hdl_mg_dl"])
hombres = hdl.loc[hdl["sexo"] == "Hombre", "hdl_mg_dl"]
mujeres = hdl.loc[hdl["sexo"] == "Mujer", "hdl_mg_dl"]

print(hdl.groupby("sexo")["hdl_mg_dl"].agg(["count", "mean", "std"]).round(1))

fig, ejes = plt.subplots(1, 2, figsize=(10, 4))
sns.boxplot(data=hdl, x="sexo", y="hdl_mg_dl", ax=ejes[0])
ejes[0].set_ylabel("HDL (mg/dL)")
for grupo, color in [(hombres, "steelblue"), (mujeres, "indianred")]:
    stats.probplot(grupo, plot=ejes[1])
ejes[1].set_title("Gráfico Q-Q de los dos grupos")
plt.tight_layout()
plt.show()
""")
c.md("""
Los diagramas de caja muestran distribuciones razonablemente simétricas y los puntos del gráfico Q-Q siguen aproximadamente una recta. Con más de 170 pacientes por grupo, la prueba *t* es además robusta a desviaciones moderadas de la normalidad.
""")
c.code("""
welch = stats.ttest_ind(mujeres, hombres, equal_var=False)
clasica = stats.ttest_ind(mujeres, hombres, equal_var=True)
ic = welch.confidence_interval()

n1, n2 = len(mujeres), len(hombres)
s_conjunta = np.sqrt(((n1 - 1) * mujeres.var() + (n2 - 1) * hombres.var()) / (n1 + n2 - 2))
d = (mujeres.mean() - hombres.mean()) / s_conjunta

print(f"Diferencia (mujeres − hombres): {mujeres.mean() - hombres.mean():.1f} mg/dL "
      f"(IC 95 %: {ic.low:.1f} a {ic.high:.1f})")
print(f"Welch:   t = {welch.statistic:.2f}, gl = {welch.df:.0f}, p = {welch.pvalue:.1e}")
print(f"Clásica: t = {clasica.statistic:.2f}, gl = {clasica.df:.0f}, p = {clasica.pvalue:.1e}")
print(f"d de Cohen = {d:.2f}")
""")
c.md("""
**Cómo se comunica:** «El HDL medio fue de 58,4 mg/dL (DE 12,5) en mujeres y de 48,8 mg/dL (DE 9,7) en hombres. Diferencia de 9,6 mg/dL (IC 95 %: 7,3 a 11,9; prueba *t* de Welch, *p* < 0,001; *d* = 0,86)».

Una diferencia de casi 10 mg/dL es grande y clínicamente relevante. Por eso las guías usan umbrales de HDL bajo distintos por sexo (< 40 mg/dL en hombres y < 50 mg/dL en mujeres).
""")

c.titulo(3, "3.2 Muestras relacionadas: el programa de reducción de sal")
c.code("""
rng = np.random.default_rng(seed=250)
antes = rng.normal(148, 14, 30).round()
despues = (antes - rng.normal(5, 6, 30)).round()
diferencias = despues - antes

apareada = stats.ttest_rel(despues, antes)
ic = apareada.confidence_interval()
print(f"PAS media antes: {antes.mean():.1f} · después: {despues.mean():.1f} mmHg")
print(f"Cambio medio: {diferencias.mean():.1f} mmHg (IC 95 %: {ic.low:.1f} a {ic.high:.1f})")
print(f"t apareada: t = {apareada.statistic:.2f}, gl = {apareada.df:.0f}, p = {apareada.pvalue:.1e}")

uno = stats.ttest_1samp(diferencias, 0)
print(f"t para una muestra sobre las diferencias: t = {uno.statistic:.2f}, p = {uno.pvalue:.1e} (idéntica)")
""")
c.code("""
fig, ejes = plt.subplots(1, 2, figsize=(10, 4))
for a, d_ in zip(antes, despues):
    ejes[0].plot([0, 1], [a, d_], color="gray", alpha=0.5)
ejes[0].set_xticks([0, 1], ["Antes", "Después"])
ejes[0].set_ylabel("PAS (mmHg)")
ejes[0].set_title("Cada línea es un paciente")
ejes[1].hist(diferencias, bins=10, color="lightsteelblue", edgecolor="white")
ejes[1].axvline(0, color="black", linestyle="--")
ejes[1].set_xlabel("Cambio de PAS (mmHg)")
ejes[1].set_title("Distribución de las diferencias")
plt.tight_layout()
plt.show()
""")

c.titulo(3, "3.3 El error de ignorar el apareamiento")
c.code("""
indep = stats.ttest_ind(despues, antes, equal_var=False)
print(f"Como si fueran grupos independientes: p = {indep.pvalue:.3f}")
print(f"Prueba apareada (correcta):           p = {apareada.pvalue:.1e}")
print(f"DE de la PAS entre pacientes: {antes.std(ddof=1):.1f} · DE de las diferencias: {diferencias.std(ddof=1):.1f} mmHg")
""")
c.md("""
La variabilidad **entre pacientes** (DE de unos 13 mmHg) es mucho mayor que la variabilidad del **cambio** dentro de cada paciente. La prueba apareada la elimina; la independiente la deja como ruido y no detecta el efecto.

Como en el Tema 240: sin grupo control no se puede atribuir la reducción al programa. Parte puede deberse a la regresión a la media, porque se eligieron pacientes con la PAS alta.
""")

c.titulo(3, "3.4 Una muestra: HbA1c de los diabéticos frente al objetivo")
c.code("""
analiticas = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/analiticas.csv")
datos = cohorte.merge(analiticas, on="id")
hba1c = datos.loc[datos["diabetes"] == "Sí", "hba1c_pct"].dropna()

r = stats.ttest_1samp(hba1c, popmean=7.0)
ic = r.confidence_interval()
print(f"Diabéticos con HbA1c: {len(hba1c)}")
print(f"HbA1c media: {hba1c.mean():.2f} % (IC 95 %: {ic.low:.2f} a {ic.high:.2f})")
print(f"Frente al objetivo del 7 %: t = {r.statistic:.2f}, p = {r.pvalue:.3f}")
print(f"Pacientes por encima del objetivo: {(hba1c > 7).mean():.0%}")
""")
c.md("""
La media está por encima del objetivo. Pero el dato clínicamente útil es también **qué proporción de pacientes** no lo alcanza. Una media cercana al objetivo puede esconder a muchos pacientes mal controlados.
""")

c.titulo(3, "Ampliación: cuando la normalidad falla")
c.md("""
Con muestras pequeñas y variables muy asimétricas (como la creatinina o el NT-proBNP), hay dos opciones:

- **Transformar** la variable con el logaritmo y aplicar la *t* a los logaritmos. La diferencia de medias de los logaritmos, exponenciada, es un **cociente de medias geométricas**.
- Usar una prueba **no paramétrica**: Mann-Whitney para dos grupos independientes y Wilcoxon de los rangos con signo para datos apareados (Tema 260).
""")
c.code("""
creatinina = datos.dropna(subset=["creatinina_mg_dl"])
diab = creatinina.loc[creatinina["diabetes"] == "Sí", "creatinina_mg_dl"]
no_diab = creatinina.loc[creatinina["diabetes"] == "No", "creatinina_mg_dl"]

r_log = stats.ttest_ind(np.log(diab), np.log(no_diab), equal_var=False)
ic = r_log.confidence_interval()
cociente = np.exp(np.log(diab).mean() - np.log(no_diab).mean())
print(f"Cociente de medias geométricas (diabéticos / no diabéticos): {cociente:.2f} "
      f"(IC 95 %: {np.exp(ic.low):.2f} a {np.exp(ic.high):.2f}), p = {r_log.pvalue:.3f}")
print(f"Mann-Whitney: p = {stats.mannwhitneyu(diab, no_diab).pvalue:.3f}")
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Usar la *t* para muestras independientes con datos apareados.**

**Contrastar la igualdad de varianzas para elegir la prueba.** Usa Welch directamente.

**Exigir un Shapiro-Wilk no significativo** con muestras grandes: la *t* es robusta.

**Dar solo el valor p.** Da las medias, la diferencia, su IC y el tamaño del efecto.

**Hacer muchas pruebas *t* entre varios grupos** en lugar de un análisis de la varianza (Tema 260).
""")

c.titulo(3, "Ampliación: Comparar las varianzas de dos grupos")
c.md("""
La *t* clásica supone que los dos grupos tienen la **misma varianza**. Hay dos pruebas para comprobarlo:

- **Prueba F:** compara el cociente de las dos varianzas. Exige normalidad.
- **Prueba de Levene:** es más robusta si los datos no son normales.

En ambas, H₀ dice que las varianzas son iguales. Muchos autores recomiendan usar **Welch siempre**: funciona bien con varianzas iguales y con varianzas distintas. Así la decisión no depende de otra prueba previa.

**En tus materiales SIMUSTAT:** [Tema 400. Contraste de dos medias poblacionales](https://colab.research.google.com/drive/1URRViPWC_adC8BGr6Kn_Z8fjV4UGjgcA), apartado 2.
""")
c.code("""
f = mujeres.var() / hombres.var()
gl1, gl2 = len(mujeres) - 1, len(hombres) - 1
p_f = 2 * min(stats.f.sf(f, gl1, gl2), stats.f.cdf(f, gl1, gl2))
lev = stats.levene(mujeres, hombres)

print(f"DE del HDL: mujeres {mujeres.std():.1f} | hombres {hombres.std():.1f} mg/dL")
print(f"Prueba F:   F = {f:.2f}, p = {p_f:.3f}")
print(f"Levene:     W = {lev.statistic:.2f}, p = {lev.pvalue:.3f}")
""")
c.md("""
Si las varianzas difieren, la *t* clásica puede dar un valor p erróneo. Welch, en cambio, sigue siendo válida. Usa la comparación de varianzas para describir los grupos, no para elegir la prueba.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 250 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** elegir la prueba *t* adecuada para seis diseños y calcular a mano un estadístico *t*.
2. **Misión clínica (con pistas):** comparar el IMC entre diabéticos y no diabéticos de la cohorte. Dar la diferencia, el IC 95 %, la *d* de Cohen y una frase de resultados.
3. **Misión reto (con asistente):** pedir al asistente el análisis de un ensayo antes-después, detectar si ha usado la prueba equivocada y corregirla.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("Se mide la glucemia a 25 pacientes antes y después de un tratamiento. ¿Qué prueba usas?", [
        ("t para muestras relacionadas", True, "Correcto: son los mismos pacientes medidos dos veces."),
        ("t de Welch para muestras independientes", False, "Ignoraría el apareamiento y perdería potencia."),
        ("Ji cuadrado", False, "La variable es cuantitativa."),
        ("McNemar", False, "McNemar es para variables binarias apareadas."),
    ]),
    ("¿Por qué se recomienda la prueba t de Welch para dos grupos independientes?", [
        ("Porque no supone varianzas iguales y funciona bien tanto si lo son como si no", True, "Correcto: evita contrastar antes la igualdad de varianzas."),
        ("Porque no supone normalidad", False, "Welch también se basa en la distribución t."),
        ("Porque sirve para datos apareados", False, "Es para muestras independientes."),
        ("Porque siempre da valores p más pequeños", False, "No es así."),
    ]),
    ("Una diferencia de medias de PAS es de 4 mmHg (IC 95 %: −1 a 9). ¿Qué concluyes?", [
        ("No es estadísticamente significativa; el efecto real podría ser nulo o de hasta 9 mmHg", True, "Correcto: el IC contiene el 0."),
        ("La diferencia es de 4 mmHg con seguridad", False, "4 mmHg es la estimación puntual."),
        ("El tratamiento empeora la PAS", False, "El IC incluye valores en los dos sentidos."),
        ("Es significativa porque 4 > 0", False, "La significación depende del IC."),
    ]),
    ("¿Qué expresa una d de Cohen de 0,8?", [
        ("Una diferencia de medias de 0,8 desviaciones típicas, considerada grande", True, "Correcto."),
        ("Una diferencia de 0,8 en las unidades de la variable", False, "La d está estandarizada."),
        ("Una probabilidad del 80 % de que la diferencia sea real", False, "No es una probabilidad."),
        ("Una correlación de 0,8", False, "No es una correlación."),
    ]),
    ("Con 12 pacientes por grupo y una variable muy asimétrica con atípicos, ¿qué es lo más adecuado?", [
        ("Transformar con logaritmos o usar la prueba de Mann-Whitney", True, "Correcto: con muestras pequeñas la t no es robusta a esa asimetría."),
        ("La t clásica, porque n es pequeño", False, "Con n pequeño la normalidad importa más."),
        ("Eliminar los atípicos y hacer la t", False, "Solo se eliminan si son errores comprobados."),
        ("La t apareada", False, "Los grupos son independientes."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- *t* para una muestra, para dos independientes (Welch) o para relacionadas, según el diseño.
- La *t* apareada es la *t* para una muestra aplicada a las diferencias.
- Da siempre la diferencia de medias con su IC y el tamaño del efecto.
- Con *n* moderado la *t* es robusta; con *n* pequeño y asimetría, logaritmos o pruebas no paramétricas.
- Antes-después sin grupo control no demuestra causalidad.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Prueba *t* para una muestra | Contraste de una media frente a un valor de referencia |
| Prueba *t* para dos muestras independientes | Contraste de la igualdad de las medias de dos grupos distintos |
| Prueba *t* de Welch | Versión de la *t* para dos muestras que no supone varianzas iguales |
| Prueba *t* para muestras relacionadas | Contraste de la media de las diferencias apareadas frente a 0 |
| Gráfico Q-Q | Gráfico que compara los cuantiles de los datos con los de una distribución normal |
| *d* de Cohen | Diferencia de medias dividida por la desviación típica conjunta |
| Media geométrica | Exponencial de la media de los logaritmos |
| Prueba de Mann-Whitney | Alternativa no paramétrica a la *t* para dos muestras independientes |
""")

c.titulo(2, "Para saber más")
c.md("""
- Ruxton GD. The unequal variance t-test is an underused alternative to Student's t-test and the Mann-Whitney U test. *Behav Ecol*. 2006;17(4):688-690. doi:[10.1093/beheco/ark016](https://doi.org/10.1093/beheco/ark016)
- Bland JM, Altman DG. Transformations, means, and confidence intervals. *BMJ*. 1996;312(7038):1079. doi:[10.1136/bmj.312.7038.1079](https://doi.org/10.1136/bmj.312.7038.1079)
- SIMUSTAT Unidigital UMH. [Tema 400. Contraste de dos medias poblacionales](https://colab.research.google.com/drive/1URRViPWC_adC8BGr6Kn_Z8fjV4UGjgcA). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(250)
print(c.guardar("../cuadernos"))
