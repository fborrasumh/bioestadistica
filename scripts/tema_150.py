from plantilla import Cuaderno

c = Cuaderno("Tema_150_Probabilidad_condicionada_y_teorema_de_Bayes.ipynb")

c.cabecera(
    150,
    "Probabilidad condicionada, independencia y teorema de Bayes en el razonamiento clínico",
    "Módulo 4. Probabilidad",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 4 se hace **a mano**. Resuelve primero cada ejercicio con papel y calculadora, y usa el código solo para comprobar.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Calcular e interpretar una probabilidad condicionada a partir de una tabla de contingencia.
2. Comprobar si dos sucesos son independientes.
3. Aplicar la regla de la multiplicación y el teorema de la probabilidad total.
4. Aplicar el teorema de Bayes para pasar de la probabilidad **preprueba** a la **posprueba**.
5. Resolver problemas de Bayes con **frecuencias naturales** y diagramas de árbol.
6. Usar las *odds* y los cocientes de probabilidad para actualizar un diagnóstico.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: Bayes en la consulta | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
**Lucía**, de 50 años y sin síntomas, se hace una mamografía de cribado. El resultado es **positivo**. Pregunta: «¿Qué probabilidad hay de que tenga cáncer de mama?».

Datos del programa de cribado (cifras redondeadas, de uso docente):

- La prevalencia de cáncer de mama en mujeres de su edad que se criban es del **1 %**.
- Si una mujer tiene cáncer, la mamografía es positiva en el **90 %** de los casos.
- Si no lo tiene, la mamografía es positiva (falso positivo) en el **9 %** de los casos.

Cuando a médicos en ejercicio se les plantea esta pregunta, muchos responden que la probabilidad es de alrededor del 90 %. La respuesta correcta es de **alrededor del 9 %**: de cada 100 mujeres con mamografía positiva, unas 91 no tienen cáncer.

Este error tiene un nombre, la **falacia de la tasa base**, y consecuencias reales: ansiedad, biopsias innecesarias y decisiones mal informadas. El teorema de Bayes es la herramienta para no cometerlo.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Probabilidad condicionada")
c.md("""
La probabilidad de A **sabiendo que** ha ocurrido B:

$$P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}$$

Saber que ha ocurrido B **reduce el espacio muestral** a los casos de B. Por ejemplo, P(evento | diabetes) es la proporción de diabéticos que tienen un evento cardiovascular.

**Cuidado con el orden:** P(positivo | cáncer) = 0,90 no es lo mismo que P(cáncer | positivo) ≈ 0,09. Confundirlas es la esencia de la falacia del caso.
""")
c.titulo(3, "2.2 Independencia")
c.md("""
A y B son **independientes** si saber que ocurrió uno no cambia la probabilidad del otro:

$$P(A \\mid B) = P(A) \\quad\\Longleftrightarrow\\quad P(A \\cap B) = P(A) \\cdot P(B)$$
""")
c.titulo(3, "2.3 Multiplicación, probabilidad total y Bayes")
c.md("""
**Regla de la multiplicación:** $P(A \\cap B) = P(A \\mid B)\\, P(B)$

**Probabilidad total.** Si los sucesos $E$ y $\\bar{E}$ (enfermo y no enfermo) reparten todo el espacio muestral:

$$P(+) = P(+ \\mid E)\\,P(E) + P(+ \\mid \\bar{E})\\,P(\\bar{E})$$

**Teorema de Bayes:**

$$P(E \\mid +) = \\frac{P(+ \\mid E)\\,P(E)}{P(+ \\mid E)\\,P(E) + P(+ \\mid \\bar{E})\\,P(\\bar{E})}$$

| Término | Nombre clínico |
| --- | --- |
| $P(E)$ | Probabilidad **preprueba** (prevalencia o sospecha clínica) |
| $P(+ \\mid E)$ | **Sensibilidad** de la prueba |
| $P(+ \\mid \\bar{E})$ | Tasa de falsos positivos (1 − especificidad) |
| $P(E \\mid +)$ | Probabilidad **posprueba**, o valor predictivo positivo |
""")
c.titulo(3, "2.4 Frecuencias naturales")
c.md("""
El teorema de Bayes se entiende mucho mejor con **frecuencias naturales**, como propone Gerd Gigerenzer. En lugar de probabilidades, imagina 1.000 personas concretas.

```
                         1.000 mujeres
                  ┌─────────────┴─────────────┐
             10 con cáncer               990 sin cáncer
           ┌──────┴──────┐             ┌──────┴──────┐
        9 positivas  1 negativa    89 positivas  901 negativas

   Positivas en total: 9 + 89 = 98   →   P(cáncer | +) = 9 / 98 ≈ 9 %
```
""")
c.titulo(3, "2.5 Odds y cocientes de probabilidad")
c.md("""
Las ***odds*** expresan la probabilidad como cociente entre que ocurra y que no ocurra:

$$\\text{odds} = \\frac{p}{1 - p} \\qquad p = \\frac{\\text{odds}}{1 + \\text{odds}}$$

El **cociente de probabilidad positivo** (LR+, *likelihood ratio*) resume el poder de un resultado positivo:

$$LR^{+} = \\frac{\\text{sensibilidad}}{1 - \\text{especificidad}}$$

El teorema de Bayes queda en una multiplicación:

$$\\text{odds posprueba} = \\text{odds preprueba} \\times LR$$

Un LR+ mayor de 10 suele modificar mucho la probabilidad; uno cercano a 1, casi nada.
""")

c.titulo(2, "3. Demostración: Bayes en la consulta (20 min)")
c.titulo(3, "3.1 Probabilidad condicionada en la cohorte")
c.code("""
import pandas as pd
import numpy as np

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")

tabla = pd.crosstab(cohorte["diabetes"], cohorte["evento_cv_5a"], margins=True, margins_name="Total")
tabla
""")
c.code("""
evento = cohorte["evento_cv_5a"] == 1
diabetes = cohorte["diabetes"] == "Sí"

p_evento = evento.mean()
p_evento_si_diabetes = (evento & diabetes).sum() / diabetes.sum()
p_evento_si_no_diabetes = (evento & ~diabetes).sum() / (~diabetes).sum()

print(f"P(evento)                = {p_evento:.3f}")
print(f"P(evento | diabetes)     = {p_evento_si_diabetes:.3f}")
print(f"P(evento | sin diabetes) = {p_evento_si_no_diabetes:.3f}")
""")
c.md("""
Saber que el paciente es diabético **cambia** la probabilidad de evento: en la cohorte, diabetes y evento cardiovascular no son independientes.
""")

c.titulo(3, "3.2 Probabilidad total")
c.md("""
**A mano:** la probabilidad global de evento es la media de las probabilidades condicionadas, ponderada por el peso de cada grupo.
""")
c.code("""
p_diabetes = diabetes.mean()
p_total = p_evento_si_diabetes * p_diabetes + p_evento_si_no_diabetes * (1 - p_diabetes)
print(f"Por la probabilidad total: {p_total:.3f}  ·  Directamente: {p_evento:.3f}")
""")

c.titulo(3, "3.3 El caso de Lucía con el teorema de Bayes")
c.code('''
def bayes(preprueba, sensibilidad, falsos_positivos):
    """Probabilidad posprueba tras un resultado positivo."""
    verdaderos = sensibilidad * preprueba
    falsos = falsos_positivos * (1 - preprueba)
    return verdaderos / (verdaderos + falsos)


p = bayes(preprueba=0.01, sensibilidad=0.90, falsos_positivos=0.09)
print(f"P(cáncer | mamografía positiva) = {p:.3f}")
''')
c.md("""
**A mano:** (0,90 × 0,01) / (0,90 × 0,01 + 0,09 × 0,99) = 0,009 / (0,009 + 0,0891) = 0,009 / 0,0981 ≈ 0,092.
""")

c.titulo(3, "3.4 Comprobación con frecuencias naturales y simulación")
c.code("""
rng = np.random.default_rng(seed=150)
n = 1_000_000

cancer = rng.random(n) < 0.01
positiva = np.where(cancer, rng.random(n) < 0.90, rng.random(n) < 0.09)

print(f"Mujeres con mamografía positiva: {positiva.sum():,}")
print(f"De ellas, con cáncer: {(positiva & cancer).sum():,}")
print(f"P(cáncer | +) simulada: {(positiva & cancer).sum() / positiva.sum():.3f}")
""")

c.titulo(3, "3.5 La misma prueba en otro contexto")
c.md("""
La probabilidad posprueba depende **tanto de la prueba como de la probabilidad preprueba**. La misma mamografía en una mujer con un nódulo palpable (probabilidad preprueba alta) significa algo muy distinto:
""")
c.code("""
import matplotlib.pyplot as plt

preprueba = np.linspace(0.001, 0.99, 300)
posprueba = bayes(preprueba, 0.90, 0.09)

plt.figure(figsize=(6.5, 4.5))
plt.plot(preprueba, posprueba)
plt.plot([0, 1], [0, 1], linestyle=":", color="gray", label="Sin prueba (posprueba = preprueba)")
for p0, texto in [(0.01, "Cribado (1 %)"), (0.30, "Nódulo palpable (30 %)")]:
    plt.scatter(p0, bayes(p0, 0.90, 0.09), color="firebrick", zorder=3)
    plt.annotate(f"{texto}: {bayes(p0, 0.90, 0.09):.0%}", (p0, bayes(p0, 0.90, 0.09)),
                 textcoords="offset points", xytext=(10, -12))
plt.xlabel("Probabilidad preprueba")
plt.ylabel("Probabilidad posprueba tras un positivo")
plt.title("Una prueba positiva según el contexto clínico")
plt.legend(loc="lower right")
plt.show()
""")

c.titulo(3, "3.6 Odds y cociente de probabilidad")
c.md("""
**A mano**, con la sensibilidad del 90 % y una especificidad del 91 %:

- LR+ = 0,90 / 0,09 = 10
- Odds preprueba (1 %) = 0,01 / 0,99 ≈ 0,0101
- Odds posprueba = 0,0101 × 10 = 0,101
- Probabilidad posprueba = 0,101 / 1,101 ≈ 0,092
""")
c.code("""
def a_odds(p):
    return p / (1 - p)

def a_probabilidad(odds):
    return odds / (1 + odds)

lr_positivo = 0.90 / 0.09
odds_post = a_odds(0.01) * lr_positivo
print(f"LR+ = {lr_positivo:.0f} · odds posprueba = {odds_post:.3f} · probabilidad = {a_probabilidad(odds_post):.3f}")
""")

c.titulo(3, "3.7 Dos pruebas seguidas")
c.diagrama('Cadena: preprueba 1 %, tras la mamografía positiva 9 %, tras la ecografía positiva 45 %.')
c.md("""
Supón que a Lucía se le hace una segunda prueba independiente y también es positiva. Entonces la probabilidad posprueba de la primera es la preprueba de la segunda. Supongamos una ecografía con LR+ = 8:
""")
c.code("""
odds_tras_ecografia = odds_post * 8
print(f"Tras mamografía y ecografía positivas: {a_probabilidad(odds_tras_ecografia):.2f}")
""")
c.md("""
Encadenar pruebas así solo es válido si son **condicionalmente independientes**, es decir, si no fallan por las mismas razones. Dos pruebas de imagen que se equivocan con los mismos tejidos densos no lo son del todo.
""")

c.titulo(3, "Ampliación: la falacia del fiscal")
c.md("""
Confundir P(A | B) con P(B | A) no es un error exclusivo de la medicina. En algunos juicios se han confundido dos probabilidades. Una es «la probabilidad de esta coincidencia de ADN si el acusado es inocente». La otra es «la probabilidad de que el acusado sea inocente dada la coincidencia». En clínica, es confundir:

- «El 90 % de los pacientes con infarto tiene dolor torácico», P(dolor | infarto), con
- «El 90 % de los pacientes con dolor torácico tiene un infarto», P(infarto | dolor), que es mucho menor.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Ignorar la prevalencia** al interpretar un resultado positivo (falacia de la tasa base).

**Confundir P(A | B) con P(B | A).**

**Aplicar la sensibilidad y especificidad de un estudio hospitalario a un cribado poblacional** sin ajustar la probabilidad preprueba.

**Encadenar pruebas que no son independientes** como si lo fueran.

**Confundir *odds* y probabilidad:** unas *odds* de 1 equivalen a una probabilidad de 0,5, no de 1.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 150 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** resolver a mano tres problemas de Bayes con frecuencias naturales y árbol.
2. **Misión clínica (con pistas):** calcular la probabilidad posprueba de trombosis venosa profunda con un dímero D positivo. Hacerlo en pacientes con probabilidad clínica baja y alta.
3. **Misión reto (con asistente):** pedir al asistente que resuelva el caso de Lucía. Comprobar si comete la falacia de la tasa base y verificar su resultado por simulación.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde a mano, sin asistente y sin ejecutar código.")
c.quiz([
    ("En una cohorte de 200 fumadores, 30 tienen EPOC. ¿Qué es 30/200?", [
        ("P(EPOC | fumador)", True, "Correcto: la proporción de EPOC dentro de los fumadores."),
        ("P(fumador | EPOC)", False, "Para eso haría falta saber cuántos pacientes con EPOC hay en total."),
        ("P(EPOC y fumador)", False, "Para eso haría falta el total de la cohorte, incluidos los no fumadores."),
        ("P(EPOC)", False, "Es la prevalencia solo entre fumadores, no en toda la población."),
    ]),
    ("Una enfermedad tiene una prevalencia del 2 %. Una prueba tiene sensibilidad del 100 % y un 10 % de falsos positivos. En 1.000 personas, ¿cuántos positivos tienen la enfermedad?", [
        ("20 de 118", True, "Correcto: 20 enfermos positivos y 98 falsos positivos (10 % de 980)."),
        ("20 de 20", False, "Faltan los 98 falsos positivos entre los 980 sanos."),
        ("100 de 118", False, "Solo hay 20 enfermos entre 1.000 personas."),
        ("18 de 100", False, "Revisa el árbol: 2 % de 1.000 son 20 enfermos."),
    ]),
    ("Una prueba tiene un LR+ de 1. ¿Qué ocurre con la probabilidad tras un resultado positivo?", [
        ("No cambia", True, "Correcto: multiplicar las odds por 1 las deja igual; la prueba no aporta información."),
        ("Se duplica", False, "Eso no ocurre con ningún LR en general, y menos con LR = 1."),
        ("Pasa a ser del 100 %", False, "Solo una prueba perfecta daría certeza."),
        ("Pasa a ser del 50 %", False, "La probabilidad posprueba depende de la preprueba."),
    ]),
    ("¿Qué probabilidad corresponde a unas odds de 1?", [
        ("0,5", True, "Correcto: p = 1 / (1 + 1)."),
        ("1", False, "Odds de 1 significan «tantos casos a favor como en contra»."),
        ("0,1", False, "Revisa la fórmula p = odds / (1 + odds)."),
        ("0", False, "Unas odds de 0 corresponderían a probabilidad 0."),
    ]),
    ("La misma prueba positiva, ¿en qué paciente aumenta más la probabilidad absoluta de enfermedad?", [
        ("En quien tiene una probabilidad preprueba intermedia", True, "Correcto: los cambios absolutos son mayores en el rango medio; en los extremos la prueba aporta poco."),
        ("En quien tiene una probabilidad preprueba muy baja", False, "Incluso tras un positivo, la probabilidad posprueba suele seguir siendo baja."),
        ("En quien tiene una probabilidad preprueba muy alta", False, "Ya era muy probable: queda poco margen para aumentar."),
        ("En todos por igual", False, "Las odds se multiplican por igual, pero el cambio en probabilidad depende del punto de partida."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- $P(A \\mid B) = P(A \\cap B) / P(B)$, y no es lo mismo que $P(B \\mid A)$.
- El teorema de Bayes combina la probabilidad preprueba con la información de la prueba.
- Un resultado positivo en una población de baja prevalencia es, muchas veces, un falso positivo.
- Las frecuencias naturales (1.000 personas) hacen evidente el razonamiento bayesiano.
- Con *odds*: odds posprueba = odds preprueba × LR.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Probabilidad condicionada | Probabilidad de un suceso sabiendo que ha ocurrido otro |
| Probabilidad preprueba | Probabilidad de enfermedad antes de conocer el resultado de la prueba |
| Probabilidad posprueba | Probabilidad de enfermedad tras conocer el resultado |
| Teorema de la probabilidad total | Descomposición de una probabilidad en la suma ponderada de probabilidades condicionadas |
| Teorema de Bayes | Fórmula que invierte una probabilidad condicionada |
| Frecuencias naturales | Representación de probabilidades como números de personas de un grupo |
| *Odds* | Cociente entre la probabilidad de que ocurra un suceso y la de que no ocurra |
| Cociente de probabilidad (LR) | Cuánto multiplica un resultado las odds de enfermedad |
| Falacia de la tasa base | Error de ignorar la prevalencia al interpretar una prueba |
""")

c.titulo(2, "Para saber más")
c.md("""
- Gigerenzer G, *et al.* Helping doctors and patients make sense of health statistics. *Psychol Sci Public Interest*. 2007;8(2):53-96. doi:[10.1111/j.1539-6053.2008.00033.x](https://doi.org/10.1111/j.1539-6053.2008.00033.x)
- Deeks JJ, Altman DG. Diagnostic tests 4: likelihood ratios. *BMJ*. 2004;329(7458):168-169. doi:[10.1136/bmj.329.7458.168](https://doi.org/10.1136/bmj.329.7458.168)
- Fagan TJ. Nomogram for Bayes's theorem. *N Engl J Med*. 1975;293(5):257. doi:[10.1056/NEJM197507312930513](https://doi.org/10.1056/NEJM197507312930513)
""")

c.pie(150)
print(c.guardar("../cuadernos"))
