from plantilla import Cuaderno

c = Cuaderno("Tema_170_Variables_aleatorias_discretas_binomial_y_Poisson.ipynb")

c.cabecera(
    170,
    "Variables aleatorias discretas: distribuciones binomial y de Poisson",
    "Módulo 4. Probabilidad",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 4 se hace **a mano**. Resuelve primero cada ejercicio con papel y calculadora, y usa el código solo para comprobar.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Definir variable aleatoria discreta, función de probabilidad y función de distribución.
2. Calcular la esperanza y la varianza de una variable discreta.
3. Reconocer cuándo un recuento clínico sigue una distribución **binomial** y calcular sus probabilidades.
4. Reconocer cuándo sigue una distribución de **Poisson** y calcular sus probabilidades.
5. Usar la distribución de Poisson para valorar si un número de casos es inusualmente alto.
6. Calcular estas probabilidades a mano y comprobarlas con `scipy.stats`.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: binomial y Poisson | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
El servicio de Medicina Preventiva de un hospital registra una media de **3 infecciones de herida quirúrgica al mes** en Cirugía General. En marzo se registran **8**.

La supervisora pregunta si hay que activar el protocolo de **brote**. Ocho casos son más que tres. Pero el número de infecciones varía de un mes a otro por puro azar: algunos meses habrá 1 y otros 5. La pregunta correcta es: **si nada hubiera cambiado, ¿con qué frecuencia veríamos 8 o más casos en un mes?**

Para responderla necesitamos un **modelo de probabilidad para recuentos**. Los recuentos son variables aleatorias discretas: casos, ingresos, respuestas a un tratamiento, efectos adversos. Dos distribuciones describen la mayoría de ellos en medicina: la **binomial** y la de **Poisson**.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Variable aleatoria discreta")
c.md("""
Una **variable aleatoria** asigna un número a cada resultado de un experimento aleatorio. Es **discreta** si toma valores aislados, normalmente recuentos: 0, 1, 2…

| Concepto | Definición |
| --- | --- |
| Función de probabilidad | $P(X = k)$ para cada valor *k* |
| Función de distribución | $F(k) = P(X \\le k)$, la probabilidad acumulada |
| Esperanza (media) | $E(X) = \\sum k \\cdot P(X = k)$ |
| Varianza | $\\text{Var}(X) = \\sum (k - E(X))^2 \\cdot P(X = k)$ |
""")
c.titulo(3, "2.2 La distribución binomial")
c.md("""
Cuenta el número de **éxitos** en *n* ensayos cuando:

1. El número de ensayos *n* es fijo.
2. Cada ensayo tiene dos resultados posibles (éxito o fracaso).
3. La probabilidad de éxito *p* es la misma en todos.
4. Los ensayos son independientes.

$$P(X = k) = \\binom{n}{k}\\, p^k\\, (1-p)^{n-k} \\qquad E(X) = np \\qquad \\text{Var}(X) = np(1-p)$$

**Ejemplos clínicos:** pacientes que responden a un tratamiento entre 20 tratados. Hijos enfermos entre 3 de una pareja de portadores. Preguntas acertadas por un modelo de IA entre 50.
""")
c.titulo(3, "2.3 La distribución de Poisson")
c.md("""
Cuenta el número de **sucesos** que ocurren en un intervalo de tiempo o de espacio cuando:

1. Los sucesos ocurren de forma independiente.
2. Ocurren con una tasa media constante λ.
3. Dos sucesos no ocurren exactamente a la vez.

$$P(X = k) = \\frac{e^{-\\lambda}\\, \\lambda^k}{k!} \\qquad E(X) = \\lambda \\qquad \\text{Var}(X) = \\lambda$$

**Ejemplos clínicos:** infecciones al mes en un servicio, ingresos en la UCI por noche, casos anuales de una enfermedad rara en una provincia.

Si *n* es grande y *p* pequeña (por ejemplo, *n* ≥ 50 y *np* ≤ 5), la binomial se aproxima por una Poisson con λ = *np*.
""")

c.titulo(2, "3. Demostración: binomial y Poisson (20 min)")
c.titulo(3, "3.1 Una variable discreta a mano: hijos enfermos")
c.md("""
Una pareja de portadores de fibrosis quística (Tema 140) tiene 3 hijos. *X* = número de hijos enfermos sigue una binomial con *n* = 3 y *p* = 1/4.

**A mano:**

| *k* | $\\binom{3}{k}$ | $P(X = k)$ |
| --- | --- | --- |
| 0 | 1 | 1 × (3/4)³ = 27/64 ≈ 0,422 |
| 1 | 3 | 3 × (1/4) × (3/4)² = 27/64 ≈ 0,422 |
| 2 | 3 | 3 × (1/4)² × (3/4) = 9/64 ≈ 0,141 |
| 3 | 1 | (1/4)³ = 1/64 ≈ 0,016 |

$E(X) = 3 \\times 1/4 = 0{,}75$ hijos enfermos de media.
""")
c.code("""
from scipy import stats
import numpy as np

X = stats.binom(n=3, p=0.25)
for k in range(4):
    print(f"P(X = {k}) = {X.pmf(k):.3f}")
print(f"Media: {X.mean():.2f} · Varianza: {X.var():.4f}")
""")
c.md("""
`scipy.stats` define cada distribución como un objeto con métodos:

| Método | Calcula |
| --- | --- |
| `.pmf(k)` | $P(X = k)$ |
| `.cdf(k)` | $P(X \\le k)$ |
| `.sf(k)` | $P(X > k) = 1 - P(X \\le k)$ |
| `.mean()`, `.var()` | Esperanza y varianza |
| `.rvs(size, random_state)` | Valores simulados |
""")

c.titulo(3, "3.2 Respuesta a un tratamiento")
c.md("""
Un antihipertensivo controla la presión arterial en el 60 % de los pacientes. Se trata a 20. ¿Qué probabilidad hay de que **al menos 15** queden controlados?

$$P(X \\ge 15) = 1 - P(X \\le 14)$$
""")
c.code("""
import matplotlib.pyplot as plt

X = stats.binom(n=20, p=0.6)
print(f"P(X ≥ 15) = {X.sf(14):.3f}")
print(f"Esperados: {X.mean():.0f} controlados · desviación típica: {X.std():.2f}")

k = np.arange(0, 21)
colores = ["firebrick" if valor >= 15 else "steelblue" for valor in k]
plt.figure(figsize=(7, 4))
plt.bar(k, X.pmf(k), color=colores)
plt.xlabel("Pacientes controlados de 20")
plt.ylabel("Probabilidad")
plt.title("Binomial(n = 20, p = 0,6); en rojo, P(X ≥ 15)")
plt.show()
""")
c.md("""
**Cuidado con «al menos»:** $P(X \\ge 15) = 1 - P(X \\le 14)$, por eso se usa `.sf(14)` y no `.sf(15)`.
""")

c.titulo(3, "3.3 El modelo de IA ante 50 preguntas")
c.md("""
Un modelo de lenguaje acierta, según su fabricante, el 80 % de las preguntas de un banco de preguntas de examen. Le planteamos 50 preguntas y acierta 34. Si el 80 % fuera cierto, ¿sería raro acertar 34 o menos?
""")
c.code("""
aciertos = stats.binom(n=50, p=0.80)
print(f"Aciertos esperados: {aciertos.mean():.0f} de 50")
print(f"P(X ≤ 34) = {aciertos.cdf(34):.4f}")
""")
c.md("""
Si la tasa real fuera del 80 %, acertar 34 o menos ocurriría en solo un 3 % de las series de 50 preguntas. Hay motivos para dudar de esa tasa en **nuestras** preguntas. Este razonamiento es el germen del contraste de hipótesis del Tema 210.

En el Tema 190 veremos que, si la dificultad de las preguntas es muy desigual, la binomial puede no ser el modelo adecuado.
""")

c.titulo(3, "3.4 Infecciones al mes: la distribución de Poisson")
c.md("""
**A mano**, con λ = 3 infecciones al mes:

- $P(X = 0) = e^{-3} \\approx 0{,}050$
- $P(X = 3) = e^{-3} \\cdot 3^3 / 3! = 0{,}050 \\times 27/6 \\approx 0{,}224$
""")
c.code("""
infecciones = stats.poisson(mu=3)
print(f"P(X = 0) = {infecciones.pmf(0):.3f}")
print(f"P(X = 3) = {infecciones.pmf(3):.3f}")

k = np.arange(0, 13)
plt.figure(figsize=(7, 4))
plt.bar(k, infecciones.pmf(k), color=["firebrick" if valor >= 8 else "steelblue" for valor in k])
plt.xlabel("Infecciones de herida quirúrgica en un mes")
plt.ylabel("Probabilidad")
plt.title("Poisson(λ = 3); en rojo, 8 o más casos")
plt.show()
""")

c.titulo(3, "3.5 ¿Es un brote?")
c.code("""
p_8_o_mas = infecciones.sf(7)
print(f"P(X ≥ 8 | λ = 3) = {p_8_o_mas:.4f}")
print(f"Esperaríamos un mes así aproximadamente una vez cada {1 / p_8_o_mas:.0f} meses")
""")
c.md("""
Ver 8 o más infecciones en un mes, si la tasa siguiera siendo 3, ocurriría aproximadamente una vez cada 7 años. Es lo bastante improbable como para **investigar**: revisar técnicas, quirófanos y microorganismos. La estadística no confirma el brote, pero sí indica que el exceso difícilmente es casual.

Comprobamos el resultado simulando 10.000 meses:
""")
c.code("""
meses = infecciones.rvs(size=10_000, random_state=170)
print(f"Meses con 8 o más infecciones: {(meses >= 8).mean():.4f}")
print(f"Media simulada: {meses.mean():.2f} · Varianza simulada: {meses.var():.2f}")
""")
c.md("""
Observa que la media y la varianza simuladas son casi iguales, como corresponde a una Poisson.
""")

c.titulo(3, "3.6 La aproximación de Poisson a la binomial")
c.diagrama('Decisión: éxitos en n ensayos fijos, binomial; sucesos con tasa λ, Poisson; con n ≥ 50 y np ≤ 5, λ = np.')
c.md("""
Un fármaco produce una reacción adversa grave en 1 de cada 1.000 pacientes. En un hospital se trata a 2.000. ¿Qué probabilidad hay de ver al menos un caso?
""")
c.code("""
exacta = stats.binom(n=2000, p=0.001).sf(0)
aproximada = stats.poisson(mu=2000 * 0.001).sf(0)
print(f"Binomial exacta:       {exacta:.4f}")
print(f"Aproximación de Poisson: {aproximada:.4f}  (λ = np = 2)")
print(f"A mano: 1 − e^(−2) = {1 - np.exp(-2):.4f}")
""")

c.titulo(3, "Ampliación: la regla del tres")
c.md("""
Si en un estudio con *n* pacientes **no** aparece ningún efecto adverso, ¿podemos decir que el riesgo es cero? No. La **regla del tres** dice que, con un 95 % de confianza, el riesgo real es menor de 3/*n*. Se deduce de la binomial: el riesgo *p* más alto compatible con 0 casos cumple $(1-p)^n = 0{,}05$.
""")
c.code("""
for n in [30, 100, 1000]:
    p_maximo = 1 - 0.05 ** (1 / n)
    print(f"n = {n:>4}: límite exacto {p_maximo:.4f} · regla del tres {3 / n:.4f}")
""")
c.md("""
Un ensayo con 300 pacientes sin ningún caso de hepatotoxicidad solo permite afirmar que el riesgo es probablemente menor del 1 %. Por eso los efectos adversos raros se descubren después de la comercialización, en la farmacovigilancia.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Usar la binomial cuando los ensayos no son independientes**, por ejemplo, contar infecciones entre pacientes de la misma habitación durante un brote.

**Usar la binomial cuando *p* no es constante**, como en preguntas de dificultad muy distinta.

**Equivocarse con «al menos» y «más de»:** $P(X \\ge 15) = 1 - P(X \\le 14)$.

**Aplicar la Poisson a recuentos con varianza mucho mayor que la media** (sobredispersión), habitual cuando la tasa varía entre periodos o unidades.

**Concluir que un riesgo es cero** porque no se ha observado ningún caso.
""")

c.titulo(3, "Ampliación: La distribución geométrica")
c.md("""
La **distribución geométrica** cuenta cuántos intentos hacen falta hasta el **primer éxito**. Cada intento es independiente y tiene la misma probabilidad de éxito *p*.

- Probabilidad de acertar justo en el intento *k*: $(1-p)^{k-1}\\,p$.
- Número medio de intentos: $1/p$.

**Ejemplo:** una enfermera canaliza una vía periférica con éxito en el 60 % de los intentos (*p* = 0,6) en un paciente con venas difíciles.

**En tus materiales SIMUSTAT:** [Tema 290. Variables aleatorias discretas](https://colab.research.google.com/drive/15moQecMrAv4YYAcljLCkNV0M9Z3apCVn), apartado 6.
""")
c.code("""
p = 0.6
X = stats.geom(p)                       # X = intentos hasta el primer éxito
for k in range(1, 5):
    print(f"P(X = {k}) = {X.pmf(k):.3f}")
print(f"P(X ≤ 3) = {X.cdf(3):.3f}")
print(f"Media = {X.mean():.2f} intentos")

k = np.arange(1, 9)
plt.bar(k, X.pmf(k), color="steelblue")
plt.xlabel("Intento en que se consigue la vía")
plt.ylabel("Probabilidad")
plt.title("Distribución geométrica, p = 0,6")
plt.show()
""")
c.md("""
La probabilidad más alta está siempre en el primer intento y después baja. El modelo supone que *p* no cambia; en la práctica, tras varios fallos la vena puede empeorar y *p* baja.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 170 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** decidir si cada recuento clínico es binomial, de Poisson o ninguno de los dos, y justificarlo.
2. **Misión clínica (con pistas):** calcular la probabilidad de 4 o más ingresos en la UCI en una noche con λ = 1,8. Hacerlo a mano y con `scipy.stats`.
3. **Misión reto (con asistente):** simular los aciertos de un modelo de IA en 40 preguntas. Comparar la distribución simulada con la binomial teórica.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde a mano, sin asistente y sin ejecutar código.")
c.quiz([
    ("Un tratamiento es eficaz en el 70 % de los pacientes. En 10 pacientes, ¿cuántos esperas que respondan?", [
        ("7", True, "Correcto: la esperanza de una binomial es np = 10 × 0,7."),
        ("10", False, "No todos responden: la probabilidad de respuesta es 0,7."),
        ("2,1", False, "Esa es la varianza, np(1 − p)."),
        ("0,7", False, "Esa es la probabilidad de que responda un paciente."),
    ]),
    ("¿Qué recuento sigue mejor una distribución de Poisson?", [
        ("Número de llamadas al 112 por cardiopatía isquémica en una hora", True, "Correcto: sucesos independientes en un intervalo de tiempo con una tasa media."),
        ("Número de curados de 30 pacientes tratados", False, "Tiene un número fijo de ensayos: es binomial."),
        ("Peso de un recién nacido", False, "Es una variable continua."),
        ("Grupo sanguíneo de un donante", False, "Es una variable categórica."),
    ]),
    ("En una Poisson con λ = 2, ¿cuánto vale P(X = 0)?", [
        ("e⁻² ≈ 0,135", True, "Correcto: e^(−λ) λ⁰ / 0! = e^(−2)."),
        ("0", False, "Que no ocurra ningún suceso es perfectamente posible."),
        ("0,5", False, "Revisa la fórmula: e^(−2) ≈ 0,135."),
        ("2", False, "Una probabilidad no puede ser mayor que 1."),
    ]),
    ("¿Cómo se calcula P(X ≥ 6) con scipy.stats para una binomial?", [
        ("X.sf(5)", True, "Correcto: sf(k) = P(X > k), y X > 5 equivale a X ≥ 6."),
        ("X.sf(6)", False, "sf(6) = P(X > 6) = P(X ≥ 7)."),
        ("X.cdf(6)", False, "cdf(6) = P(X ≤ 6)."),
        ("X.pmf(6)", False, "pmf(6) = P(X = 6), solo ese valor."),
    ]),
    ("En un ensayo con 150 pacientes no aparece ningún caso de anafilaxia. ¿Qué puede afirmarse con un 95 % de confianza?", [
        ("Que el riesgo es probablemente menor del 2 %", True, "Correcto: regla del tres, 3 / 150 = 0,02."),
        ("Que el riesgo es cero", False, "No haber visto casos no demuestra que no existan."),
        ("Que el riesgo es menor de 1 de cada 150", False, "La regla del tres da 3/n, no 1/n."),
        ("Nada: con cero casos no se puede calcular nada", False, "La regla del tres da un límite superior."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Una variable aleatoria discreta se describe con su función de probabilidad, su esperanza y su varianza.
- **Binomial**: éxitos en *n* ensayos independientes con la misma *p*; media *np*.
- **Poisson**: sucesos en un intervalo con tasa λ; media y varianza iguales a λ.
- Un recuento muy improbable bajo el modelo habitual es una señal para investigar, no una prueba definitiva.
- No observar casos no demuestra que el riesgo sea cero (regla del tres).
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Variable aleatoria discreta | Variable que toma valores aislados, normalmente recuentos |
| Función de probabilidad | Probabilidad de cada valor de la variable |
| Función de distribución | Probabilidad acumulada hasta un valor |
| Esperanza | Valor medio de una variable aleatoria a largo plazo |
| Distribución binomial | Número de éxitos en *n* ensayos independientes con probabilidad constante |
| Distribución de Poisson | Número de sucesos en un intervalo con una tasa media constante |
| Tasa (λ) | Número medio de sucesos por unidad de tiempo o espacio |
| Sobredispersión | Situación en la que la varianza observada es mayor que la prevista por el modelo |
| Regla del tres | Si no hay casos en *n* sujetos, el riesgo es probablemente menor de 3/*n* |
""")

c.titulo(2, "Para saber más")
c.md("""
- Hanley JA, Lippman-Hand A. If nothing goes wrong, is everything all right? Interpreting zero numerators. *JAMA*. 1983;249(13):1743-1745.
- [Documentación de scipy.stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- SIMUSTAT Unidigital UMH. [Tema 290. Variables aleatorias discretas](https://colab.research.google.com/drive/15moQecMrAv4YYAcljLCkNV0M9Z3apCVn). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(170)
print(c.guardar("../cuadernos"))
