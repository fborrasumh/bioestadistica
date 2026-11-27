from plantilla import Cuaderno

c = Cuaderno("Tema_210_Contraste_de_hipotesis_significacion_errores_y_potencia.ipynb")

c.cabecera(
    210,
    "Fundamentos del contraste de hipótesis: significación estadística, errores y potencia",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Plantear la hipótesis nula y la alternativa de una pregunta clínica.
2. Definir e interpretar correctamente el **valor p**.
3. Distinguir los errores de tipo I y de tipo II, y definir la **potencia** de un estudio.
4. Relacionar un contraste de hipótesis con el intervalo de confianza correspondiente.
5. Distinguir significación estadística de relevancia clínica.
6. Calcular el tamaño muestral necesario para alcanzar una potencia dada, y reconocer el riesgo de las comparaciones múltiples.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: contrastar por simulación y con fórmulas | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un laboratorio presenta un nuevo antihipertensivo. En un ensayo con 40 pacientes por grupo, la presión sistólica bajó de media **8 mmHg** con el fármaco y **3 mmHg** con placebo. El resumen del artículo concluye: «diferencia estadísticamente significativa, *p* = 0,03».

Tres preguntas que un médico debe saber hacerse:

1. ¿Qué significa exactamente *p* = 0,03? (Pista: **no** es la probabilidad de que el fármaco no funcione.)
2. Una diferencia de 5 mmHg, ¿es clínicamente relevante? ¿Con qué precisión se ha estimado?
3. Si el ensayo hubiera dado *p* = 0,20, ¿demostraría que el fármaco no sirve?

El **contraste de hipótesis** es el método que usan casi todos los ensayos clínicos para decidir si una diferencia observada puede atribuirse al azar. Es también el concepto estadístico peor interpretado de la literatura médica.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Las hipótesis")
c.diagrama('Flujo del contraste: plantear H₀ y H₁, suponer H₀, calcular p, comparar con α y decidir.')
c.md("""
| Hipótesis | Qué afirma | En el caso |
| --- | --- | --- |
| **Nula** ($H_0$) | No hay efecto ni diferencia: lo observado se debe al azar | La reducción media de la PAS es igual con fármaco y con placebo |
| **Alternativa** ($H_1$) | Hay un efecto o una diferencia | Las reducciones medias son distintas |

El contraste supone que $H_0$ es cierta y mide hasta qué punto los datos son **compatibles** con ella. Si son muy poco compatibles, se rechaza $H_0$.

El contraste es **bilateral** si $H_1$ admite diferencias en cualquier sentido, y **unilateral** si solo en uno. En Medicina se usan casi siempre contrastes bilaterales.
""")
c.titulo(3, "2.2 El valor p")
c.md("""
El **valor p** es la probabilidad de obtener un resultado **igual o más extremo** que el observado **si la hipótesis nula fuera cierta**.

- *p* pequeño: los datos serían raros si $H_0$ fuera cierta; hay evidencia contra $H_0$.
- *p* grande: los datos son compatibles con $H_0$; **no** demuestra que $H_0$ sea cierta.

Por convenio, se fija un **nivel de significación** α = 0,05: si *p* < α, se dice que el resultado es «estadísticamente significativo». El umbral es arbitrario; *p* = 0,049 y *p* = 0,051 aportan prácticamente la misma evidencia.

**Lo que el valor p NO es:**

| Afirmación errónea | Por qué es errónea |
| --- | --- |
| «Es la probabilidad de que $H_0$ sea cierta» | Se calcula **suponiendo** que $H_0$ es cierta |
| «1 − *p* es la probabilidad de que el fármaco funcione» | El mismo error en sentido inverso |
| «Un *p* pequeño indica un efecto grande» | Con muestras grandes, efectos mínimos dan *p* muy pequeños |
| «*p* > 0,05 demuestra que no hay efecto» | Puede faltar potencia: ausencia de evidencia no es evidencia de ausencia |
""")
c.titulo(3, "2.3 Errores y potencia")
c.md("""
| | $H_0$ es cierta (no hay efecto) | $H_0$ es falsa (hay efecto) |
| --- | --- | --- |
| **Se rechaza $H_0$** | **Error de tipo I** (falso positivo), probabilidad α | Decisión correcta, probabilidad 1 − β = **potencia** |
| **No se rechaza $H_0$** | Decisión correcta | **Error de tipo II** (falso negativo), probabilidad β |

La **potencia** es la probabilidad de detectar un efecto que realmente existe. Los ensayos clínicos se diseñan habitualmente con una potencia del 80 % o del 90 %. Aumenta con:

- Un tamaño muestral mayor.
- Un efecto real mayor.
- Una variabilidad menor.
- Un α mayor (a costa de más falsos positivos).
""")
c.titulo(3, "2.4 Contraste e intervalo de confianza")
c.md("""
Un contraste bilateral con α = 0,05 y el IC del 95 % dan la misma información sobre el valor nulo: **si el IC 95 % de una diferencia no contiene el 0, *p* < 0,05**, y viceversa. Pero el IC dice además **cuánto** puede valer el efecto. Por eso las guías de publicación piden dar siempre el intervalo, y no solo el valor p.
""")

c.titulo(2, "3. Demostración: contrastar por simulación y con fórmulas (20 min)")
c.titulo(3, "3.1 Los datos del ensayo")
c.code("""
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=197)
farmaco = rng.normal(8, 10, 40).round(1)     # reducción de PAS (mmHg)
placebo = rng.normal(3, 10, 40).round(1)

diferencia_observada = farmaco.mean() - placebo.mean()
print(f"Reducción media: fármaco {farmaco.mean():.1f} mmHg · placebo {placebo.mean():.1f} mmHg")
print(f"Diferencia observada: {diferencia_observada:.1f} mmHg")
""")

c.titulo(3, "3.2 El valor p por simulación: la prueba de permutaciones")
c.md("""
Si $H_0$ fuera cierta, la etiqueta «fármaco» o «placebo» sería irrelevante: cada paciente habría tenido la misma reducción con cualquiera de los dos. Podemos **barajar las etiquetas** muchas veces y ver qué diferencias produce el azar por sí solo. El valor p es la proporción de barajados con una diferencia tan grande o mayor que la observada.
""")
c.code("""
todos = np.concatenate([farmaco, placebo])
diferencias_azar = []
for _ in range(10_000):
    barajado = rng.permutation(todos)
    diferencias_azar.append(barajado[:40].mean() - barajado[40:].mean())
diferencias_azar = np.array(diferencias_azar)

p_permutacion = (np.abs(diferencias_azar) >= abs(diferencia_observada)).mean()

plt.figure(figsize=(7, 4))
plt.hist(diferencias_azar, bins=60, color="lightsteelblue", edgecolor="white")
plt.axvline(diferencia_observada, color="firebrick", label=f"Observada: {diferencia_observada:.1f} mmHg")
plt.axvline(-diferencia_observada, color="firebrick", linestyle="--")
plt.xlabel("Diferencia de medias si H₀ fuera cierta (mmHg)")
plt.ylabel("Frecuencia")
plt.title(f"Distribución bajo H₀ · valor p ≈ {p_permutacion:.3f}")
plt.legend()
plt.show()
""")

c.titulo(3, "3.3 El mismo contraste con la fórmula: la prueba t")
c.md("""
La prueba *t* de Student para dos muestras independientes (Tema 250) llega al mismo resultado sin simular. Calculamos también el IC 95 % de la diferencia.
""")
c.code("""
resultado = stats.ttest_ind(farmaco, placebo)
ic = resultado.confidence_interval(confidence_level=0.95)

print(f"Prueba t: t = {resultado.statistic:.2f}, p = {resultado.pvalue:.3f}")
print(f"Valor p por permutación: {p_permutacion:.3f}")
print(f"Diferencia: {diferencia_observada:.1f} mmHg (IC 95 %: {ic.low:.1f} a {ic.high:.1f})")
""")
c.md("""
**Interpretación completa:** el fármaco redujo la PAS una media de unos 5 mmHg más que el placebo. Si en realidad no hubiera diferencia, una diferencia así de grande ocurriría en pocos ensayos de cada cien. El IC 95 % indica que el efecto real podría estar entre algo más de 0 y unos 10 mmHg. Es compatible con un efecto clínicamente pequeño y con uno relevante.
""")

c.titulo(3, "3.4 Si H₀ es cierta, el 5 % de los estudios sale «significativo»")
c.md("""
Simulamos 10.000 ensayos de un fármaco que **no hace nada**: los dos grupos salen de la misma población.
""")
c.code("""
valores_p = np.array([stats.ttest_ind(rng.normal(3, 10, 40), rng.normal(3, 10, 40)).pvalue
                      for _ in range(10_000)])

print(f"Ensayos con p < 0,05: {(valores_p < 0.05).mean():.1%}")

plt.figure(figsize=(7, 3.5))
plt.hist(valores_p, bins=20, color="lightsteelblue", edgecolor="white")
plt.axvline(0.05, color="firebrick", linestyle="--", label="α = 0,05")
plt.xlabel("Valor p")
plt.ylabel("Número de ensayos")
plt.title("Bajo H₀, los valores p se reparten de manera uniforme")
plt.legend()
plt.show()
""")
c.md("""
Es el **error de tipo I**: con α = 0,05, uno de cada 20 ensayos de un fármaco inútil saldrá significativo. Si se publican solo esos (**sesgo de publicación**), la literatura sobreestima la eficacia.
""")

c.titulo(3, "3.5 La potencia")
c.md("""
Ahora el fármaco **sí** reduce la PAS 5 mmHg más que el placebo. ¿Qué proporción de ensayos lo detecta según el número de pacientes por grupo?
""")
c.code("""
tamanos = [10, 20, 40, 64, 100, 150]
potencias = []
for n in tamanos:
    p = np.array([stats.ttest_ind(rng.normal(8, 10, n), rng.normal(3, 10, n)).pvalue for _ in range(2000)])
    potencias.append((p < 0.05).mean())
    print(f"n = {n:>3} por grupo: potencia ≈ {potencias[-1]:.0%}")

plt.figure(figsize=(7, 4))
plt.plot(tamanos, potencias, marker="o")
plt.axhline(0.8, color="gray", linestyle="--", label="Potencia del 80 %")
plt.xlabel("Pacientes por grupo")
plt.ylabel("Potencia")
plt.ylim(0, 1)
plt.title("Potencia para detectar una diferencia de 5 mmHg (σ = 10)")
plt.legend()
plt.show()
""")
c.md("""
Con 40 pacientes por grupo, la potencia es de alrededor del 60 %: **cuatro de cada diez ensayos como el del caso no habrían detectado un efecto real**. Un resultado no significativo en un estudio con poca potencia no permite concluir nada.
""")

c.titulo(3, "3.6 El tamaño muestral para una potencia dada")
c.md("""
La biblioteca `statsmodels` calcula el tamaño muestral a partir del **tamaño del efecto** estandarizado (*d* de Cohen = diferencia / σ), α y la potencia deseada.
""")
c.code("""
from statsmodels.stats.power import TTestIndPower

analisis = TTestIndPower()
d = 5 / 10
for potencia in [0.8, 0.9]:
    n = analisis.solve_power(effect_size=d, alpha=0.05, power=potencia)
    print(f"Potencia {potencia:.0%}: {np.ceil(n):.0f} pacientes por grupo")
""")

c.titulo(3, "3.7 Significación estadística no es relevancia clínica")
c.md("""
Con una muestra enorme, una diferencia trivial resulta «muy significativa»:
""")
c.code("""
grande_a = rng.normal(130.0, 15, 20_000)
grande_b = rng.normal(130.8, 15, 20_000)
r = stats.ttest_ind(grande_a, grande_b)
ic = r.confidence_interval()
print(f"Diferencia: {grande_b.mean() - grande_a.mean():.2f} mmHg · p = {r.pvalue:.2e}")
print(f"IC 95 % de la diferencia: {-ic.high:.2f} a {-ic.low:.2f} mmHg")
""")
c.md("""
Una diferencia de menos de 1 mmHg es estadísticamente significativa, pero **clínicamente irrelevante**. La pregunta clínica no es «¿*p* < 0,05?», sino «¿es el efecto lo bastante grande para importar al paciente, y con qué precisión lo conocemos?».
""")

c.titulo(3, "Ampliación: comparaciones múltiples")
c.md("""
Supón un estudio que compara 20 variables entre dos grupos sin ninguna diferencia real. La probabilidad de encontrar **al menos una** con *p* < 0,05 es $1 - 0{,}95^{20} \\approx 0{,}64$ (Temas 140 y 180). Buscar hasta encontrar algo significativo se llama *p-hacking*. Lo veremos en el Tema 260, junto con las correcciones.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Interpretar *p* como la probabilidad de que $H_0$ sea cierta.**

**Concluir «no hay diferencias» a partir de *p* > 0,05** sin valorar la potencia ni el intervalo de confianza.

**Confundir significación estadística con importancia clínica.**

**Dar solo el valor p**, sin la estimación del efecto y su intervalo.

**Decidir la hipótesis o el tipo de contraste después de ver los datos.**

**Tratar 0,05 como una frontera mágica:** *p* = 0,049 y *p* = 0,051 son prácticamente la misma evidencia.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 210 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** identificar interpretaciones correctas e incorrectas del valor p en frases tomadas de artículos.
2. **Misión clínica (con pistas):** calcular el valor p de una diferencia de HbA1c entre dos pautas, por permutación y con la prueba *t*. Interpretar su IC.
3. **Misión reto (con asistente):** calcular con el asistente el tamaño muestral de un ensayo y comprobarlo por simulación de la potencia. Redactar la justificación para el comité de ética.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("Un ensayo obtiene p = 0,03. ¿Qué significa?", [
        ("Que, si no hubiera diferencia real, un resultado tan extremo ocurriría en el 3 % de los estudios", True, "Correcto: es la definición del valor p."),
        ("Que hay un 3 % de probabilidad de que el fármaco no funcione", False, "El valor p se calcula suponiendo H₀ cierta; no da la probabilidad de H₀."),
        ("Que hay un 97 % de probabilidad de que el fármaco funcione", False, "Es el mismo error en sentido inverso."),
        ("Que el efecto del fármaco es grande", False, "El valor p no mide el tamaño del efecto."),
    ]),
    ("Un ensayo con 30 pacientes por grupo no encuentra diferencias significativas (p = 0,25). ¿Qué puede concluirse?", [
        ("Que no hay evidencia suficiente; el estudio puede no tener potencia para detectar el efecto", True, "Correcto: ausencia de evidencia no es evidencia de ausencia."),
        ("Que el fármaco no es eficaz", False, "Un estudio pequeño puede no detectar un efecto real."),
        ("Que los dos tratamientos son equivalentes", False, "Demostrar equivalencia exige otro diseño."),
        ("Que hay un 25 % de probabilidad de que sean iguales", False, "Esa no es la interpretación del valor p."),
    ]),
    ("¿Qué es la potencia de un estudio?", [
        ("La probabilidad de detectar un efecto que realmente existe", True, "Correcto: 1 − β."),
        ("La probabilidad de un falso positivo", False, "Eso es α, el error de tipo I."),
        ("El tamaño del efecto observado", False, "La potencia es una probabilidad, no un efecto."),
        ("La probabilidad de que H₀ sea cierta", False, "La potencia se calcula suponiendo que H₁ es cierta."),
    ]),
    ("La diferencia de PAS entre dos tratamientos es 6 mmHg (IC 95 %: −1 a 13). ¿Qué puedes decir del valor p bilateral?", [
        ("Es mayor de 0,05, porque el intervalo contiene el 0", True, "Correcto: un IC 95 % que incluye el valor nulo equivale a p > 0,05."),
        ("Es menor de 0,05", False, "Para eso el IC no debería contener el 0."),
        ("Es exactamente 0,05", False, "Eso ocurriría si un extremo del IC estuviera justo en 0."),
        ("No se puede saber nada", False, "La relación entre IC y contraste lo permite."),
    ]),
    ("Se comparan 10 variables entre dos grupos que en realidad no difieren. ¿Qué probabilidad hay de al menos un resultado con p < 0,05?", [
        ("Alrededor del 40 %", True, "Correcto: 1 − 0,95¹⁰ ≈ 0,40."),
        ("El 5 %", False, "Ese es el riesgo de cada comparación por separado."),
        ("El 50 %", False, "Sería 10 × 0,05, pero las probabilidades no se suman así."),
        ("El 0,5 %", False, "El riesgo aumenta con el número de comparaciones."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- El contraste mide la compatibilidad de los datos con $H_0$; el valor p **no** es la probabilidad de que $H_0$ sea cierta.
- *p* > 0,05 no demuestra la ausencia de efecto, sobre todo si la potencia es baja.
- α es el riesgo de falso positivo; β, el de falso negativo; 1 − β es la potencia.
- El intervalo de confianza da la misma decisión que el contraste y, además, la magnitud del efecto.
- Significación estadística no es relevancia clínica.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Hipótesis nula ($H_0$) | Afirmación de ausencia de efecto o diferencia |
| Hipótesis alternativa ($H_1$) | Afirmación de que existe efecto o diferencia |
| Valor p | Probabilidad de un resultado igual o más extremo que el observado si $H_0$ fuera cierta |
| Nivel de significación (α) | Umbral de *p* por debajo del cual se rechaza $H_0$ |
| Error de tipo I | Rechazar $H_0$ siendo cierta (falso positivo) |
| Error de tipo II | No rechazar $H_0$ siendo falsa (falso negativo) |
| Potencia | Probabilidad de rechazar $H_0$ cuando es falsa |
| Tamaño del efecto | Magnitud de la diferencia, con frecuencia estandarizada (*d* de Cohen) |
| Prueba de permutaciones | Contraste que obtiene la distribución bajo $H_0$ barajando las etiquetas de los grupos |
| *p-hacking* | Multiplicar análisis hasta obtener un resultado significativo |
""")

c.titulo(2, "Para saber más")
c.md("""
- Wasserstein RL, Lazar NA. The ASA statement on p-values: context, process, and purpose. *Am Stat*. 2016;70(2):129-133.
- Altman DG, Bland JM. Absence of evidence is not evidence of absence. *BMJ*. 1995;311(7003):485.
- Greenland S, *et al.* Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. *Eur J Epidemiol*. 2016;31(4):337-350.
""")

c.pie(210)
print(c.guardar("../cuadernos"))
