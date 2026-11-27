from plantilla import Cuaderno

c = Cuaderno("Tema_280_Modelo_de_regresion_logistica.ipynb")

c.cabecera(
    280,
    "Modelo de regresión logística",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Explicar por qué la regresión lineal no sirve para una variable de respuesta binaria y cómo la resuelve la función logística.
2. Ajustar un modelo de regresión logística e interpretar sus coeficientes como **odds ratios ajustadas** con su IC 95 %.
3. Expresar la OR de una variable cuantitativa para un incremento clínicamente útil (10 años, 10 mmHg).
4. Calcular con el modelo la probabilidad de un evento para un paciente concreto.
5. Valorar si el número de eventos es suficiente para el número de variables del modelo.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: el riesgo cardiovascular de la cohorte | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En el Tema 230 vimos que, en la cohorte, los diabéticos tienen más eventos cardiovasculares a 5 años (OR cruda 1,77). Pero los diabéticos son, de media, algo mayores que los no diabéticos, y la edad es el factor de riesgo cardiovascular más potente. ¿Cuánto de ese exceso de riesgo se debe a la diabetes y cuánto a la edad?

Además, el equipo quiere una herramienta sencilla. Se introducen la edad, el sexo, la presión arterial, el tabaco y la diabetes de un paciente. La herramienta da su **probabilidad** de evento a 5 años. Es la lógica de las escalas de riesgo como SCORE2 o Framingham.

Las dos tareas se hacen con la **regresión logística**: estimar efectos ajustados de factores de riesgo y predecir la probabilidad de un evento binario. Es el modelo multivariante más usado en la investigación clínica.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Por qué no una recta")
c.md("""
Si la respuesta es 0/1 (evento sí o no), una recta no sirve, por dos razones. Puede predecir «probabilidades» negativas o mayores de 1. Y el efecto de cada factor no puede ser igual en toda la escala. Pasar del 1 % al 2 % de riesgo no es lo mismo que pasar del 50 % al 51 %.

La regresión logística modela el **logaritmo de la odds** (logit) como una combinación lineal de los predictores:

$$\\ln\\left(\\frac{p}{1-p}\\right) = \\beta_0 + \\beta_1 X_1 + \\dots + \\beta_k X_k$$

y la probabilidad se recupera con la **función logística**, que siempre da valores entre 0 y 1:

$$p = \\frac{1}{1 + e^{-(\\beta_0 + \\beta_1 X_1 + \\dots + \\beta_k X_k)}}$$
""")
c.titulo(3, "2.2 Los coeficientes son logaritmos de odds ratios")
c.md("""
| Coeficiente | Exponenciado | Interpretación |
| --- | --- | --- |
| $\\beta_j$ de una variable binaria | $e^{\\beta_j}$ = OR | Odds del evento en la categoría frente a la de referencia, a igualdad de las demás variables |
| $\\beta_j$ de una variable cuantitativa | $e^{\\beta_j}$ = OR por unidad | Multiplicación de la odds por cada unidad más |
| La misma, para *k* unidades | $e^{k \\beta_j}$ | OR por *k* unidades (por ejemplo, por 10 años) |

Una OR > 1 indica más odds de evento; < 1, menos; = 1, ninguna asociación. Como en el Tema 230, si el evento no es raro, la OR exagera el riesgo relativo.
""")
c.titulo(3, "2.3 Cuántas variables caben en el modelo")
c.md("""
Lo que limita una regresión logística no es el número de pacientes sino el número de **eventos** (o de no eventos, si son menos). La regla clásica pide al menos **10 eventos por variable** (EPV). Con menos, los coeficientes son inestables y exagerados (sobreajuste), y el modelo predice peor en pacientes nuevos (Tema 290). Las recomendaciones actuales para modelos predictivos calculan el tamaño muestral necesario de forma más precisa (Riley *et al.*, 2020).
""")

c.titulo(2, "3. Demostración: el riesgo cardiovascular de la cohorte (20 min)")
c.titulo(3, "3.1 La curva logística: edad y evento")
c.code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")
cohorte["evento"] = cohorte["evento_cv_5a"]

m_edad = smf.logit("evento ~ edad", data=cohorte).fit(disp=0)
lineal = smf.ols("evento ~ edad", data=cohorte).fit()

x = np.linspace(20, 100, 200)
plt.figure(figsize=(7, 4.5))
plt.scatter(cohorte["edad"], cohorte["evento"] + np.random.default_rng(280).uniform(-0.03, 0.03, len(cohorte)),
            alpha=0.25, s=12, label="Pacientes (0 = sin evento, 1 = evento)")
plt.plot(x, m_edad.predict(pd.DataFrame({"edad": x})), color="firebrick", label="Regresión logística")
plt.plot(x, lineal.predict(pd.DataFrame({"edad": x})), color="gray", linestyle="--", label="Recta (inadecuada)")
plt.axhline(0, color="black", linewidth=0.5)
plt.xlabel("Edad (años)")
plt.ylabel("Probabilidad de evento a 5 años")
plt.legend()
plt.show()

print(f"La recta predice a los 25 años una probabilidad de {lineal.predict(pd.DataFrame({'edad': [25]}))[0]:.3f}")
""")
c.md("""
Fuera del rango de los datos, la recta predice una probabilidad **negativa**. La curva logística se mantiene entre 0 y 1 y crece de forma multiplicativa con la edad.
""")

c.titulo(3, "3.2 La OR de la edad")
c.code("""
b = m_edad.params["edad"]
li, ls = m_edad.conf_int().loc["edad"]
print(f"Coeficiente β = {b:.4f}")
print(f"OR por año: {np.exp(b):.3f} (IC 95 %: {np.exp(li):.3f} a {np.exp(ls):.3f})")
print(f"OR por 10 años: {np.exp(10 * b):.2f} (IC 95 %: {np.exp(10 * li):.2f} a {np.exp(10 * ls):.2f})")
""")
c.md("""
Cada año multiplica la odds de evento por 1,085; cada **10 años**, por más de 2. Expresar la OR por 10 años es más útil clínicamente que por un año. Ojo: la OR por 10 años es $e^{10\\beta}$, no 10 veces la OR por año.
""")

c.titulo(3, "3.3 ¿Diabetes o edad? La OR ajustada")
c.code("""
def tabla_or(modelo):
    ic = modelo.conf_int()
    return pd.DataFrame({
        "OR": np.exp(modelo.params),
        "IC 95 % inf.": np.exp(ic[0]),
        "IC 95 % sup.": np.exp(ic[1]),
        "p": modelo.pvalues,
    }).drop(index="Intercept").round(3)

cruda = smf.logit("evento ~ diabetes", data=cohorte).fit(disp=0)
ajustada = smf.logit("evento ~ diabetes + edad", data=cohorte).fit(disp=0)
print("Diabéticos: edad media", cohorte.groupby("diabetes")["edad"].mean().round(1).to_dict())
print("\\nOR cruda:")
print(tabla_or(cruda))
print("\\nOR ajustada por edad:")
print(tabla_or(ajustada))
""")
c.md("""
La OR de la diabetes baja de 1,77 a 1,48 al ajustar por edad. Parte del exceso de riesgo de los diabéticos de la cohorte se debía a que eran mayores. Con 48 eventos, el IC sigue siendo muy ancho. No permite confirmar el efecto propio de la diabetes, que en estudios grandes está bien establecido.
""")

c.titulo(3, "3.4 El modelo multivariante")
c.code("""
completo = smf.logit("evento ~ edad + sexo + fumador + diabetes + pas_mmHg + hdl_mg_dl", data=cohorte).fit(disp=0)
eventos = int(completo.model.endog.sum())
predictores = len(completo.params) - 1
print(f"Pacientes en el modelo: {int(completo.nobs)} · eventos: {eventos} · predictores: {predictores} "
      f"· eventos por variable: {eventos / predictores:.1f}")
tabla_or(completo)
""")
c.code("""
for variable, k, unidad in [("edad", 10, "10 años"), ("pas_mmHg", 10, "10 mmHg"), ("hdl_mg_dl", 10, "10 mg/dL")]:
    b = completo.params[variable]
    li, ls = completo.conf_int().loc[variable]
    print(f"{variable:>10}: OR por {unidad} = {np.exp(k * b):.2f} (IC 95 %: {np.exp(k * li):.2f} a {np.exp(k * ls):.2f})")
""")
c.md("""
**Cómo se comunica:** «En el análisis multivariante, tres variables se asociaron de forma independiente con el evento cardiovascular a 5 años. Fueron la edad (OR 2,06 por cada 10 años), la PAS (OR 1,55 por cada 10 mmHg) y el sexo masculino (OR para mujeres 0,34)».

Dos advertencias:

- Con unos 7 eventos por variable, el modelo está por debajo de la regla de 10 EPV: los coeficientes pueden estar **sobrestimados**. La OR de la PAS es probablemente mayor que la real.
- El tabaco o el HDL no salen significativos, pero eso **no** significa que no sean factores de riesgo. Con 43 eventos, el modelo no tiene potencia para detectarlos.
""")

c.titulo(3, "3.5 La probabilidad de un paciente")
c.diagrama('Pasos: z = β₀ + β₁x₁ + …, odds = eᶻ, p = odds / (1 + odds); con z = −2, p = 0,119.')
c.code("""
pacientes = pd.DataFrame({
    "edad": [52, 72],
    "sexo": ["Mujer", "Hombre"],
    "fumador": ["No", "Sí"],
    "diabetes": ["No", "Sí"],
    "pas_mmHg": [125, 155],
    "hdl_mg_dl": [60, 38],
})
pacientes["probabilidad"] = completo.predict(pacientes)
for _, f in pacientes.iterrows():
    print(f"{f['sexo']} de {f['edad']} años, fumador {f['fumador']}, diabetes {f['diabetes']}, PAS {f['pas_mmHg']}, "
          f"HDL {f['hdl_mg_dl']}: probabilidad de evento a 5 años {f['probabilidad']:.1%}")
""")
c.md("""
Es lo que hacen las calculadoras de riesgo cardiovascular. Pero este modelo se ha construido con 358 pacientes y 43 eventos. Y no se ha **validado** en pacientes distintos de los que se usaron para ajustarlo. Antes de usarlo con un paciente real habría que comprobar su discriminación y su calibración en otra muestra (Tema 290). Las escalas de las guías se han desarrollado con cientos de miles de personas.
""")

c.titulo(3, "Ampliación: el sobreajuste con pocos eventos")
c.md("""
Simulamos muchas cohortes de distinto tamaño, todas con una OR real de la PAS de 1,20 por 10 mmHg. Después, vemos qué OR estima el modelo.
""")
c.code("""
rng = np.random.default_rng(seed=280)

def simular(n):
    edad = rng.uniform(40, 85, n)
    pas = 110 + 0.5 * (edad - 40) + rng.normal(0, 14, n)
    logit = -7.4 + 0.07 * edad + np.log(1.20) / 10 * (pas - 120)
    evento = rng.random(n) < 1 / (1 + np.exp(-logit))
    datos = pd.DataFrame({"evento": evento.astype(int), "edad": edad, "pas": pas})
    for _ in range(4):  # cuatro variables de ruido, sin relación con el evento
        datos[f"ruido{_}"] = rng.normal(0, 1, n)
    m = smf.logit("evento ~ edad + pas + ruido0 + ruido1 + ruido2 + ruido3", data=datos).fit(disp=0)
    return evento.sum() / 6, np.exp(10 * m.params["pas"])

for n in [300, 1000, 5000]:
    resultados = np.array([simular(n) for _ in range(150)])
    print(f"n = {n:>4}: eventos por variable ≈ {resultados[:, 0].mean():5.1f} · "
          f"mediana de la OR estimada = {np.median(resultados[:, 1]):.2f} · "
          f"rango central del 90 %: {np.percentile(resultados[:, 1], 5):.2f} a {np.percentile(resultados[:, 1], 95):.2f}")
""")
c.md("""
Con pocos eventos por variable, la OR estimada varía muchísimo de una cohorte a otra. Con unos 4 EPV, una cohorte puede obtener una OR «protectora» de 0,84 y otra una de 1,60. La real es 1,20. Las que salen significativas suelen ser las más exageradas. Con miles de pacientes, se concentra alrededor del valor real (1,20). El tamaño muestral de un modelo se decide **antes** de ajustarlo.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Interpretar la OR como un riesgo relativo** cuando el evento es frecuente.

**Dar la OR de una variable cuantitativa por unidad** cuando la unidad es diminuta (por mg/dL o por año); exprésala por un incremento clínico.

**Meter demasiadas variables para los eventos disponibles.**

**Seleccionar las variables por su significación** en análisis univariantes previos. Elígelas por conocimiento clínico.

**Usar las probabilidades del modelo en la clínica sin validarlo.**

**Interpretar las OR ajustadas de un estudio observacional como efectos causales.**
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 280 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** convertir coeficientes en OR, OR por unidad en OR por 10 unidades, y logit en probabilidad.
2. **Misión clínica (con pistas):** estimar la OR del tabaco sobre el evento, cruda y ajustada por edad y sexo, e interpretar el cambio.
3. **Misión reto (con asistente):** pedir al asistente un modelo con todas las variables de la cohorte y calcular los eventos por variable. Proponer un modelo más sencillo, justificado clínicamente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("En una regresión logística, el coeficiente del tabaco es 0,69. ¿Cuál es la OR?", [
        ("Aproximadamente 2", True, "Correcto: e^0,69 ≈ 2,0."),
        ("0,69", False, "El coeficiente es el logaritmo de la OR."),
        ("1,69", False, "La OR no es 1 + β."),
        ("0,5", False, "Eso sería e^(−0,69)."),
    ]),
    ("La OR de la edad es 1,07 por año. ¿Cuál es la OR por 10 años?", [
        ("Aproximadamente 1,97", True, "Correcto: 1,07¹⁰ ≈ 1,97."),
        ("10,7", False, "Las OR se multiplican, no se suman."),
        ("1,7", False, "Eso sería sumar 10 × 0,07 a 1."),
        ("0,7", False, "Revisa cómo se combinan las OR."),
    ]),
    ("¿Qué significa una OR ajustada de 1,48 para la diabetes en un modelo con la edad?", [
        ("Que a igualdad de edad, la odds de evento de los diabéticos es 1,48 veces la de los no diabéticos", True, "Correcto: es una OR ajustada."),
        ("Que el 48 % de los diabéticos tiene un evento", False, "La OR no es una probabilidad."),
        ("Que la diabetes causa un 48 % más de eventos", False, "Es una asociación ajustada, no necesariamente causal."),
        ("Que la diabetes es significativa", False, "La significación depende del IC."),
    ]),
    ("Un modelo tiene 30 eventos y 8 variables. ¿Qué problema tiene?", [
        ("Pocos eventos por variable: riesgo de sobreajuste y coeficientes inestables", True, "Correcto: menos de 4 eventos por variable."),
        ("Ninguno, si hay 1.000 pacientes", False, "Lo que limita es el número de eventos."),
        ("Que las OR no se pueden calcular", False, "Se calculan, pero son poco fiables."),
        ("Que hay que usar regresión lineal", False, "La respuesta sigue siendo binaria."),
    ]),
    ("¿Por qué no se usa la regresión lineal para predecir un evento binario?", [
        ("Porque puede predecir probabilidades menores de 0 o mayores de 1", True, "Correcto: la función logística mantiene la probabilidad entre 0 y 1."),
        ("Porque la regresión lineal no admite variables cualitativas", False, "Sí las admite como indicadoras."),
        ("Porque la regresión lineal no tiene IC", False, "Sí los tiene."),
        ("Porque la regresión logística siempre da coeficientes mayores", False, "No es el motivo."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La regresión logística modela el logit de la probabilidad de un evento binario.
- $e^{\\beta}$ es la OR ajustada; para variables cuantitativas, exprésala por un incremento clínico ($e^{k\\beta}$).
- El modelo permite estimar la probabilidad de evento de un paciente, pero antes hay que validarlo.
- El número de eventos limita el número de variables (como orientación, 10 eventos por variable).
- Un factor no significativo en un modelo pequeño no queda descartado.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Regresión logística | Modelo para una respuesta binaria que relaciona el logit de la probabilidad con los predictores |
| Logit | Logaritmo de la odds: $\\ln(p / (1 - p))$ |
| Función logística | Función que transforma el logit en una probabilidad entre 0 y 1 |
| Odds ratio ajustada | OR de una variable controlando por las demás variables del modelo |
| Eventos por variable (EPV) | Número de eventos dividido por el número de predictores del modelo |
| Sobreajuste | Ajuste excesivo a la muestra, que exagera los efectos y empeora la predicción en datos nuevos |
| Probabilidad predicha | Probabilidad de evento que el modelo asigna a un paciente según sus características |
""")

c.titulo(2, "Para saber más")
c.md("""
- Peduzzi P, Concato J, Kemper E, Holford TR, Feinstein AR. A simulation study of the number of events per variable in logistic regression analysis. *J Clin Epidemiol*. 1996;49(12):1373-1379.
- Riley RD, *et al.* Calculating the sample size required for developing a clinical prediction model. *BMJ*. 2020;368:m441.
- Sperandei S. Understanding logistic regression analysis. *Biochem Med (Zagreb)*. 2014;24(1):12-18.
""")

c.pie(280)
print(c.guardar("../cuadernos"))
