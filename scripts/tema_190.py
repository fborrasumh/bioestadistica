from plantilla import Cuaderno

c = Cuaderno("Tema_190_Simulacion_de_Monte_Carlo_y_distribuciones_muestrales.ipynb")

c.cabecera(
    190,
    "Simulación de Monte Carlo y distribuciones muestrales",
    "Módulo 4. Probabilidad",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 4 se hace **a mano**. Resuelve primero cada ejercicio con papel y calculadora, y usa el código solo para comprobar.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Explicar en qué consiste el método de Monte Carlo y para qué sirve.
2. Distinguir la distribución de una variable en la población de la **distribución muestral** de un estadístico.
3. Calcular e interpretar el **error estándar** de una media y de una proporción.
4. Enunciar el **teorema central del límite** y comprobarlo por simulación con datos asimétricos.
5. Explicar cómo influye el tamaño de la muestra en la precisión de una estimación.
6. Medir la variabilidad de las respuestas de un modelo de lenguaje y reconocer la sobredispersión.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: muestras simuladas | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Dos residentes estudian la **estancia hospitalaria** de los pacientes con neumonía de su hospital. Cada uno revisa al azar 30 historias del último año. El primero obtiene una estancia media de 6,2 días; el segundo, de 7,9 días.

¿Se ha equivocado alguno? No necesariamente. **Cada muestra es distinta**, y por tanto también lo es su media. Si un tercer residente revisara otras 30 historias, obtendría un tercer valor.

Esta variabilidad entre muestras no es un defecto: es inevitable, y se puede **cuantificar**. Los intervalos de confianza y los contrastes de hipótesis del Módulo 5 se basan en una idea: cuánto varía una media de una muestra a otra. Hoy lo veremos simulando miles de muestras con el ordenador: el método de **Monte Carlo**.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 El método de Monte Carlo")
c.md("""
Consiste en estimar una cantidad **repitiendo muchas veces un experimento aleatorio simulado** y resumiendo los resultados. Ya lo hemos usado para comprobar cálculos de probabilidad (Temas 140 a 170). Hoy lo usaremos para algo que sería imposible en la realidad: extraer miles de muestras de la misma población.

Se llama así por el casino de Montecarlo. Lo desarrollaron en los años cuarenta Stanislaw Ulam y John von Neumann.
""")
c.titulo(3, "2.2 Población, muestra y distribución muestral")
c.md("""
| Distribución | Qué describe | Su dispersión |
| --- | --- | --- |
| De la variable en la **población** | Cómo varían los **pacientes** | Desviación típica σ |
| De la variable en **una muestra** | Cómo varían los pacientes de esa muestra | Desviación típica muestral *s* |
| **Muestral** de la media | Cómo varía la **media** de una muestra a otra | **Error estándar** |

La **distribución muestral** de un estadístico es la distribución de los valores que tomaría ese estadístico en todas las muestras posibles del mismo tamaño.
""")
c.titulo(3, "2.3 El error estándar")
c.diagrama('Dos histogramas: la PAS de los pacientes (DE 15 mmHg) y las medias de muestras de 25 (EE 3 mmHg).')
c.md("""
| Estadístico | Error estándar |
| --- | --- |
| Media | $EE(\\bar{x}) = \\dfrac{\\sigma}{\\sqrt{n}} \\approx \\dfrac{s}{\\sqrt{n}}$ |
| Proporción | $EE(\\hat{p}) = \\sqrt{\\dfrac{p(1-p)}{n}}$ |

El error estándar disminuye con la raíz cuadrada de *n*: para reducirlo a la mitad hay que **cuadruplicar** la muestra.

**No confundas** la desviación típica (dispersión de los pacientes) con el error estándar (precisión de la media). Al aumentar la muestra, la desviación típica de los pacientes no cambia; el error estándar, sí.
""")
c.titulo(3, "2.4 El teorema central del límite")
c.md("""
Toma muestras de tamaño *n* suficientemente grande de **cualquier** población con media μ y desviación típica σ. La distribución de la media muestral se aproxima a una normal:

$$\\bar{x} \\approx N\\left(\\mu, \\frac{\\sigma}{\\sqrt{n}}\\right)$$

aunque la variable original **no** sea normal. Con distribuciones moderadamente asimétricas suele bastar con *n* ≥ 30; con distribuciones muy asimétricas hace falta más. Este teorema explica por qué la normal aparece en casi toda la inferencia estadística.
""")

c.titulo(2, "3. Demostración: muestras simuladas (20 min)")
c.titulo(3, "3.1 Una población sintética de pacientes")
c.md("""
Creamos una población de 100.000 ingresos por neumonía con una estancia **asimétrica**: la mayoría se va en pocos días y unos pocos permanecen mucho tiempo.
""")
c.code("""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=190)
poblacion = rng.lognormal(mean=np.log(5.5), sigma=0.55, size=100_000).round(1) + 1

mu, sigma = poblacion.mean(), poblacion.std()
print(f"Media poblacional μ = {mu:.2f} días · desviación típica σ = {sigma:.2f} días")

plt.figure(figsize=(7, 4))
plt.hist(poblacion, bins=80, color="lightsteelblue", edgecolor="white")
plt.axvline(mu, color="firebrick", label=f"μ = {mu:.1f} días")
plt.xlim(0, 30)
plt.xlabel("Estancia (días)")
plt.ylabel("Número de pacientes")
plt.title("Población: estancia de 100.000 ingresos por neumonía")
plt.legend()
plt.show()
""")

c.titulo(3, "3.2 Una muestra, dos muestras, diez muestras")
c.code("""
for i in range(1, 11):
    muestra = rng.choice(poblacion, size=30, replace=False)
    print(f"Muestra {i:>2}: media {muestra.mean():.2f} días")
""")
c.md("""
Cada residente obtendría un valor distinto, todos alrededor de μ. ¿Cuánto varían? Lo vemos con 10.000 muestras.
""")

c.titulo(3, "3.3 La distribución muestral de la media")
c.code("""
def medias_muestrales(n, repeticiones=10_000):
    \"\"\"Medias de muchas muestras aleatorias de tamaño n de la población.\"\"\"
    return np.array([rng.choice(poblacion, size=n).mean() for _ in range(repeticiones)])


fig, ejes = plt.subplots(1, 3, figsize=(13, 3.8), sharex=True)
for eje, n in zip(ejes, [5, 30, 120]):
    medias = medias_muestrales(n)
    ee_teorico = sigma / np.sqrt(n)
    eje.hist(medias, bins=60, density=True, color="lightsteelblue", edgecolor="white")
    x = np.linspace(medias.min(), medias.max(), 200)
    eje.plot(x, np.exp(-((x - mu) ** 2) / (2 * ee_teorico ** 2)) / (ee_teorico * np.sqrt(2 * np.pi)),
             color="firebrick", label="Normal del TCL")
    eje.set_title(f"n = {n}\\nEE simulado {medias.std():.2f} · teórico {ee_teorico:.2f}")
    eje.set_xlabel("Media de la muestra (días)")
ejes[0].legend()
plt.tight_layout()
plt.show()
""")
c.md("""
Tres observaciones fundamentales:

1. Las medias se concentran **alrededor de μ**: la media muestral no tiene sesgo.
2. Al aumentar *n*, la distribución se **estrecha**: el error estándar simulado coincide con σ/√*n*.
3. La población es muy asimétrica. Aun así, con *n* = 30 o más, la distribución de la media ya es **casi normal**: es el teorema central del límite. Con *n* = 5 todavía se aprecia la asimetría.
""")

c.titulo(3, "3.4 El 95 % de las medias")
c.md("""
Si las medias siguen aproximadamente una normal, el 95 % de ellas estará a menos de 1,96 errores estándar de μ. Lo comprobamos:
""")
c.code("""
n = 30
medias = medias_muestrales(n)
ee = sigma / np.sqrt(n)
dentro = np.abs(medias - mu) < 1.96 * ee
print(f"Medias a menos de 1,96 EE de μ: {dentro.mean():.1%}")
""")
c.md("""
Esta es la idea del **intervalo de confianza** del Tema 200. Si cada residente construye el intervalo media ± 1,96 EE con su muestra, alrededor del 95 % de esos intervalos contiene el verdadero valor μ.
""")

c.titulo(3, "3.5 Tamaño muestral y precisión")
c.code("""
tamanos = np.array([10, 20, 40, 80, 160, 320, 640])
ee_simulado = [medias_muestrales(n, 3000).std() for n in tamanos]

plt.figure(figsize=(7, 4))
plt.plot(tamanos, ee_simulado, marker="o", label="Simulado")
plt.plot(tamanos, sigma / np.sqrt(tamanos), linestyle="--", label="σ / √n")
plt.xscale("log")
plt.xticks(tamanos, tamanos)
plt.xlabel("Tamaño de la muestra (escala logarítmica)")
plt.ylabel("Error estándar de la media (días)")
plt.title("Cuadruplicar la muestra reduce el error estándar a la mitad")
plt.legend()
plt.show()
""")

c.titulo(3, "3.6 La distribución muestral de una proporción")
c.md("""
Lo mismo ocurre con las proporciones. Si la prevalencia real de diabetes en una población es del 18 %, ¿cuánto varía la prevalencia estimada en muestras de 100 pacientes?

**A mano:** $EE = \\sqrt{0{,}18 \\times 0{,}82 / 100} \\approx 0{,}038$. El 95 % de las muestras dará una prevalencia entre 0,18 ± 1,96 × 0,038. Es decir, entre el 10,5 % y el 25,5 % aproximadamente.
""")
c.code("""
p = 0.18
prevalencias = rng.binomial(n=100, p=p, size=10_000) / 100
print(f"EE simulado: {prevalencias.std():.3f} · teórico: {np.sqrt(p * (1 - p) / 100):.3f}")
print(f"Percentiles 2,5 y 97,5 de la prevalencia estimada: {np.percentile(prevalencias, [2.5, 97.5])}")
""")

c.titulo(3, "3.7 La variabilidad de un modelo de lenguaje")
c.md("""
En el Tema 170 modelamos el número de aciertos de un modelo de IA con una binomial. Ese modelo asume que **todas las preguntas tienen la misma probabilidad de acierto**. En la práctica, unas preguntas son fáciles para el modelo y otras muy difíciles. Simulamos 50 preguntas con dificultad variable y repetimos el «examen» muchas veces.
""")
c.code("""
n_preguntas, repeticiones = 50, 5000

# Probabilidad de acierto de cada pregunta: media 0,8, pero muy desigual
p_pregunta = rng.beta(a=2, b=0.5, size=n_preguntas)
print(f"Probabilidad media de acierto: {p_pregunta.mean():.2f}")

# Cada repetición del examen responde a las mismas 50 preguntas
aciertos_reales = (rng.random((repeticiones, n_preguntas)) < p_pregunta).sum(axis=1)
# Lo que predeciría una binomial con la misma media
aciertos_binomial = rng.binomial(n_preguntas, p_pregunta.mean(), size=repeticiones)

print(f"Varianza con dificultad desigual: {aciertos_reales.var():.2f}")
print(f"Varianza de la binomial:          {aciertos_binomial.var():.2f}")
""")
c.md("""
Aquí ocurre algo contraintuitivo: **repitiendo el mismo examen**, la variabilidad es *menor* que la de la binomial. Las preguntas fáciles se aciertan casi siempre y las difíciles casi nunca. En cambio, supón que cada repetición es un examen de un **área distinta**: unas áreas le resultan fáciles al modelo y otras difíciles. Entonces la probabilidad media de acierto cambia de un examen a otro. La variabilidad es *mayor* que la binomial: es la **sobredispersión**.
""")
c.code("""
p_area = rng.beta(a=8, b=2, size=repeticiones)          # acierto medio de cada área: 0,8 en promedio
examenes_por_area = rng.binomial(n_preguntas, p_area)
p_media = p_area.mean()
print(f"Varianza con exámenes de áreas distintas: {examenes_por_area.var():.2f}")
print(f"Varianza de la binomial con p = {p_media:.2f}:    {n_preguntas * p_media * (1 - p_media):.2f}")
""")
c.md("""
**Conclusión práctica:** antes de aplicar un modelo de probabilidad a los resultados de un modelo de IA, responde a dos preguntas. ¿**Qué** se repite: la misma pregunta, el mismo examen o exámenes distintos? ¿Es realmente constante la probabilidad de acierto?
""")

c.titulo(3, "Ampliación: la misma pregunta, muchas veces, al modelo real")
c.md("""
Con una clave configurada, esta celda repite 10 veces una misma pregunta con temperatura alta y cuenta las respuestas distintas. Sin clave, no hace nada.
""")
c.conexion_ia()
c.code("""
from collections import Counter

pregunta = ("Un paciente con fiebre, tos productiva y crepitantes en la base derecha. "
            "¿Cuál es el diagnóstico más probable? Responde con dos palabras como máximo.")

if cliente is not None:
    respuestas = [preguntar(pregunta, temperatura=1.5).strip().lower().rstrip(".") for _ in range(10)]
    print(Counter(respuestas))
else:
    print("Configura tu clave para hacer el experimento con el modelo real.")
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Confundir desviación típica y error estándar** al leer un artículo. Una media «± 0,4» puede ser una desviación típica muy pequeña o un error estándar con una dispersión grande.

**Pensar que la muestra debe ser una fracción grande de la población.** La precisión depende sobre todo del tamaño absoluto de la muestra, no del porcentaje de la población.

**Aplicar el teorema central del límite a muestras muy pequeñas** de variables muy asimétricas.

**Creer que el TCL hace normales los datos.** Lo que se aproxima a la normal es la **media** de muchas muestras, no la distribución de los pacientes.

**Olvidar que la simulación tiene su propio error:** con pocas repeticiones, el resultado de un Monte Carlo también varía.
""")

c.titulo(3, "Ampliación: Simulación de Monte Carlo y método de la transformación inversa")
c.md("""
Una **simulación de Monte Carlo** estima una probabilidad repitiendo un experimento aleatorio muchas veces en el ordenador. Es la técnica que usa este tema para estudiar la media muestral.

Para simular una distribución cualquiera basta un generador uniforme entre 0 y 1. El **método de la transformación inversa** aplica a cada número uniforme *u* la inversa de la función de distribución. Para una exponencial de media μ: $t = -\\mu \\ln(1-u)$.

**En tus materiales SIMUSTAT:** [Tema 320. Simulación de Monte Carlo y las distribuciones muestrales](https://colab.research.google.com/drive/1IMUU6YaylInQ_SiS6qfUGGpVSYLCcYDd), apartado 1 y 2.
""")
c.code("""
import math

rng = np.random.default_rng(320)
u = rng.uniform(size=100_000)
t = -6 * np.log(1 - u)                  # exponencial de media 6 min (Tema 180)

print(f"Media simulada: {t.mean():.2f} min (teórica: 6)")
print(f"P(T > 15) simulada: {(t > 15).mean():.4f} | exacta: {math.exp(-15 / 6):.4f}")

plt.hist(t, bins=80, density=True, color="steelblue", alpha=0.7, label="Simulación")
x = np.linspace(0, 40, 200)
plt.plot(x, np.exp(-x / 6) / 6, color="orange", lw=2, label="Densidad teórica")
plt.xlim(0, 40)
plt.xlabel("Minutos")
plt.legend()
plt.show()
""")
c.md("""
Con 100.000 repeticiones, la simulación difiere del cálculo exacto en menos de una milésima. Cuando no hay fórmula, la simulación da la respuesta; con más repeticiones, la estimación es más precisa.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 190 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** calcular a mano el error estándar de medias y proporciones con distintos tamaños muestrales.
2. **Misión clínica (con pistas):** simular la distribución muestral de la prevalencia de hipertensión con muestras de 50, 200 y 800 pacientes.
3. **Misión reto (con asistente):** repetir 20 veces una pregunta clínica a un modelo de IA y registrar las respuestas. Discutir si un modelo binomial describe su variabilidad.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde a mano, sin asistente y sin ejecutar código.")
c.quiz([
    ("La PAS de una población tiene σ = 16 mmHg. ¿Cuál es el error estándar de la media en muestras de 64 pacientes?", [
        ("2 mmHg", True, "Correcto: 16 / √64 = 16 / 8."),
        ("16 mmHg", False, "Esa es la desviación típica de los pacientes."),
        ("0,25 mmHg", False, "Eso es 16 / 64: hay que dividir entre la raíz de n."),
        ("4 mmHg", False, "Revisa la raíz cuadrada de 64."),
    ]),
    ("Para reducir a la mitad el error estándar de una media, ¿cuánto hay que aumentar la muestra?", [
        ("Multiplicarla por 4", True, "Correcto: el EE depende de 1/√n, y √4 = 2."),
        ("Multiplicarla por 2", False, "Con el doble de muestra, el EE solo se divide entre √2 ≈ 1,41."),
        ("Sumarle 30 pacientes", False, "El efecto depende de la proporción, no de una cantidad fija."),
        ("No se puede reducir", False, "Aumentar la muestra siempre lo reduce."),
    ]),
    ("¿Qué afirma el teorema central del límite?", [
        ("Que la media muestral se aproxima a una normal con muestras suficientemente grandes, sea cual sea la distribución de la variable", True, "Correcto."),
        ("Que toda variable biológica sigue una distribución normal", False, "Muchas variables no son normales."),
        ("Que con muestras grandes los datos de los pacientes se vuelven normales", False, "Los datos no cambian; es la media la que se aproxima a la normal."),
        ("Que la media muestral es siempre igual a la poblacional", False, "La media muestral varía alrededor de la poblacional."),
    ]),
    ("Una prevalencia real del 50 % se estima con muestras de 100 personas. ¿Cuál es el error estándar de la proporción?", [
        ("0,05", True, "Correcto: √(0,5 × 0,5 / 100) = √0,0025."),
        ("0,5", False, "Esa es la prevalencia, no su error estándar."),
        ("0,25", False, "Eso es p(1 − p); falta dividir entre n y hacer la raíz."),
        ("0,0025", False, "Esa es la varianza; falta la raíz cuadrada."),
    ]),
    ("Al pasar de 50 a 500 pacientes en un estudio, ¿qué ocurre con la desviación típica de la edad de los pacientes?", [
        ("Se mantiene aproximadamente igual", True, "Correcto: la dispersión de los pacientes no depende del tamaño de la muestra."),
        ("Disminuye a un tercio", False, "Eso le ocurre, aproximadamente, al error estándar (√10 ≈ 3,2)."),
        ("Aumenta", False, "No hay motivo para que aumente."),
        ("Se hace cero", False, "Los pacientes siguen teniendo edades distintas."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- El método de Monte Carlo estima cantidades repitiendo muchas veces un experimento simulado.
- La media de una muestra varía de una muestra a otra; su dispersión es el error estándar, σ/√*n*.
- El teorema central del límite hace que la media muestral sea aproximadamente normal con muestras grandes.
- Alrededor del 95 % de las medias muestrales está a menos de 1,96 EE de la media poblacional: es la base del intervalo de confianza.
- Antes de modelar los aciertos de un modelo de IA, hay que comprobar si la probabilidad de acierto es constante.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Método de Monte Carlo | Estimación de una cantidad mediante la repetición de experimentos aleatorios simulados |
| Estadístico | Valor calculado a partir de una muestra |
| Distribución muestral | Distribución de un estadístico en todas las muestras posibles de un mismo tamaño |
| Error estándar | Desviación típica de la distribución muestral de un estadístico |
| Teorema central del límite | Resultado según el cual la media muestral se aproxima a una normal al aumentar *n* |
| Estimador insesgado | Estimador cuya distribución muestral está centrada en el parámetro |
| Sobredispersión | Variabilidad mayor que la que predice el modelo de probabilidad supuesto |
""")

c.titulo(2, "Para saber más")
c.md("""
- Altman DG, Bland JM. Standard deviations and standard errors. *BMJ*. 2005;331(7521):903. doi:[10.1136/bmj.331.7521.903](https://doi.org/10.1136/bmj.331.7521.903)
- Metropolis N, Ulam S. The Monte Carlo method. *J Am Stat Assoc*. 1949;44(247):335-341. doi:[10.1080/01621459.1949.10483310](https://doi.org/10.1080/01621459.1949.10483310)
- SIMUSTAT Unidigital UMH. [Tema 320. Simulación de Monte Carlo y las distribuciones muestrales](https://colab.research.google.com/drive/1IMUU6YaylInQ_SiS6qfUGGpVSYLCcYDd). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(190)
print(c.guardar("../cuadernos"))
