from plantilla import Cuaderno

c = Cuaderno("Tema_230_Tablas_de_contingencia_y_medidas_de_asociacion_RR_OR_y_NNT.ipynb")

c.cabecera(
    230,
    "Análisis de tablas de contingencia y medidas de asociación epidemiológica: riesgo relativo, odds ratio y número necesario a tratar",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Aplicar e interpretar la prueba ji cuadrado de independencia en tablas de contingencia.
2. Calcular e interpretar el **riesgo relativo** (RR), la **odds ratio** (OR) y la **diferencia de riesgos**, con sus intervalos de confianza.
3. Elegir la medida de asociación según el diseño del estudio (cohortes, ensayo clínico o casos y controles).
4. Calcular e interpretar el **número necesario a tratar** (NNT).
5. Distinguir la reducción relativa del riesgo de la reducción absoluta, y reconocer cómo se usa cada una para comunicar resultados.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: medidas de asociación con Python | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un titular de prensa dice: «Un nuevo fármaco **reduce un 33 % el riesgo de infarto**». Un paciente de 58 años con colesterol moderadamente alto te pregunta si debería tomarlo.

En el ensayo, a los 5 años tuvieron un infarto el **3 %** de los pacientes con placebo y el **2 %** de los tratados. Las dos frases siguientes describen el mismo resultado:

- «El fármaco reduce el riesgo un 33 %» (reducción **relativa**).
- «El fármaco reduce el riesgo en 1 punto porcentual. Hay que tratar a **100 pacientes durante 5 años** para evitar un infarto» (reducción **absoluta** y NNT).

La primera impresiona más; la segunda es la que necesita el paciente para decidir, teniendo en cuenta los efectos adversos y el coste. Hoy aprenderás a calcular y a interpretar todas estas medidas.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 La tabla 2 × 2")
c.diagrama('Tabla 2 × 2 con las fórmulas de riesgo y odds de cada fila, y del RR y la OR.', nombre="e2_1")
c.md("""
| | Evento sí | Evento no | Total |
| --- | --- | --- | --- |
| **Expuestos** | *a* | *b* | *a* + *b* |
| **No expuestos** | *c* | *d* | *c* + *d* |

- Riesgo en expuestos: $R_1 = a/(a+b)$. Riesgo en no expuestos: $R_0 = c/(c+d)$.
- Odds en expuestos: $a/b$. Odds en no expuestos: $c/d$.
""")
c.titulo(3, "2.2 Medidas de asociación")
c.md("""
| Medida | Fórmula | Valor nulo | Interpretación |
| --- | --- | --- | --- |
| Riesgo relativo (RR) | $R_1 / R_0$ | 1 | Cuántas veces más riesgo tienen los expuestos |
| Odds ratio (OR) | $(a \\cdot d)/(b \\cdot c)$ | 1 | Cociente de odds; se parece al RR si el evento es raro (< 10 %) |
| Diferencia de riesgos (DR) | $R_1 - R_0$ | 0 | Exceso (o reducción) absoluto de riesgo |
| Reducción relativa del riesgo (RRR) | $1 - RR$ | 0 | Proporción del riesgo que elimina el tratamiento |
| Número necesario a tratar (NNT) | $1 / |DR|$ | ∞ | Pacientes que hay que tratar para evitar un evento |

Si el tratamiento **aumenta** el riesgo de un efecto adverso, $1/DR$ se llama **número necesario para dañar** (NND).
""")
c.titulo(3, "2.3 Qué medida según el diseño")
c.md("""
| Diseño | ¿Se puede calcular el riesgo? | Medida |
| --- | --- | --- |
| Cohortes y ensayos clínicos | Sí: se sigue a los pacientes y se cuentan los eventos | RR, DR, NNT (y OR) |
| Casos y controles | No: el investigador fija cuántos casos y controles incluye | **Solo la OR** |
| Transversal | Prevalencias, no riesgos | Razón de prevalencias u OR |
""")
c.titulo(3, "2.4 La ji cuadrado de independencia")
c.diagrama('Flujo: tabla observada, tabla esperada (fila × columna / N) y estadístico ji cuadrado.')
c.md("""
Contrasta $H_0$: «las dos variables cualitativas son independientes». Compara las frecuencias observadas con las **esperadas** si fueran independientes:

$$\\chi^2 = \\sum \\frac{(O - E)^2}{E}, \\qquad E = \\frac{\\text{total de fila} \\times \\text{total de columna}}{N}$$

Sirve para tablas de cualquier tamaño (*r* × *c*), con (*r* − 1)(*c* − 1) grados de libertad. Exige frecuencias esperadas ≥ 5 en la mayoría de las casillas; si no, Fisher (Tema 220).
""")

c.titulo(2, "3. Demostración: medidas de asociación con Python (20 min)")
c.titulo(3, "3.1 Diabetes y eventos cardiovasculares en la cohorte")
c.code("""
import numpy as np
import pandas as pd
from scipy import stats

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")

tabla = pd.crosstab(cohorte["diabetes"], cohorte["evento_cv_5a"], margins=True)
tabla.columns = ["Sin evento", "Con evento", "Total"]
tabla = tabla.loc[["Sí", "No", "All"]].rename(index={"All": "Total"})
tabla
""")
c.md("""
**A mano:** riesgo en diabéticos = 13/74 = 0,176; en no diabéticos = 35/326 = 0,107.

- RR = 0,176 / 0,107 = **1,64**: los diabéticos tienen un riesgo un 64 % mayor.
- DR = 0,176 − 0,107 = **0,068**: 6,8 eventos más por cada 100 diabéticos en 5 años.
- OR = (13 × 291) / (61 × 35) = **1,77**.
""")

c.titulo(3, "3.2 Las medidas con sus intervalos de confianza")
c.code("""
from statsmodels.stats.contingency_tables import Table2x2

# Filas: expuestos (diabetes) y no expuestos; columnas: evento sí y evento no
a, b = 13, 61
c_, d = 35, 291
t = Table2x2(np.array([[a, b], [c_, d]]))

rr, (rr_li, rr_ls) = t.riskratio, t.riskratio_confint()
or_, (or_li, or_ls) = t.oddsratio, t.oddsratio_confint()
r1, r0 = a / (a + b), c_ / (c_ + d)

print(f"Riesgo en diabéticos: {r1:.1%} · en no diabéticos: {r0:.1%}")
print(f"RR = {rr:.2f} (IC 95 %: {rr_li:.2f} a {rr_ls:.2f})")
print(f"OR = {or_:.2f} (IC 95 %: {or_li:.2f} a {or_ls:.2f})")
print(f"DR = {r1 - r0:.1%}")

chi2, p, gl, esperadas = stats.chi2_contingency([[a, b], [c_, d]], correction=False)
print(f"Ji cuadrado = {chi2:.2f}, gl = {gl}, p = {p:.3f}")
""")
c.md("""
**Interpretación:** el riesgo de evento cardiovascular a 5 años fue mayor en los diabéticos (RR estimado 1,64). Pero el IC 95 % incluye el 1 y la ji cuadrado no es significativa. Con 74 diabéticos, la cohorte **no tiene potencia** para confirmar un aumento de riesgo que la literatura sí ha establecido con estudios mucho mayores. Fíjate en que la OR (1,77) es algo mayor que el RR. El evento afecta al 12 % de la cohorte, y con esa frecuencia la OR ya exagera un poco la asociación.
""")

c.titulo(3, "3.3 Una función propia para cualquier tabla 2 × 2")
c.code("""
def medidas_2x2(a, b, c, d, z=1.96):
    \"\"\"a, b: expuestos con y sin evento; c, d: no expuestos con y sin evento.\"\"\"
    r1, r0 = a / (a + b), c / (c + d)
    rr = r1 / r0
    ee_log_rr = np.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
    or_ = (a * d) / (b * c)
    ee_log_or = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    dr = r1 - r0
    ee_dr = np.sqrt(r1 * (1 - r1) / (a + b) + r0 * (1 - r0) / (c + d))
    return {
        "RR": (rr, rr * np.exp(-z * ee_log_rr), rr * np.exp(z * ee_log_rr)),
        "OR": (or_, or_ * np.exp(-z * ee_log_or), or_ * np.exp(z * ee_log_or)),
        "DR": (dr, dr - z * ee_dr, dr + z * ee_dr),
    }

for medida, (valor, li, ls) in medidas_2x2(13, 61, 35, 291).items():
    print(f"{medida}: {valor:.3f} (IC 95 %: {li:.3f} a {ls:.3f})")
""")
c.md("""
Los IC del RR y de la OR se calculan en **escala logarítmica** y luego se exponencian: por eso son asimétricos alrededor de la estimación.
""")

c.titulo(3, "3.4 Un ensayo clínico: RRR, RAR y NNT")
c.md("""
Ensayo hipotético de una estatina en prevención primaria: 2.000 pacientes por grupo, seguidos 5 años.
""")
c.code("""
eventos_trat, n_trat = 160, 2000      # 8 %
eventos_plac, n_plac = 240, 2000      # 12 %

r_t, r_p = eventos_trat / n_trat, eventos_plac / n_plac
rr = r_t / r_p
rar = r_p - r_t
nnt = 1 / rar

ee = np.sqrt(r_t * (1 - r_t) / n_trat + r_p * (1 - r_p) / n_plac)
rar_li, rar_ls = rar - 1.96 * ee, rar + 1.96 * ee

print(f"Riesgo: tratados {r_t:.1%} · placebo {r_p:.1%}")
print(f"RR = {rr:.2f} · Reducción relativa del riesgo = {1 - rr:.0%}")
print(f"Reducción absoluta del riesgo = {rar:.1%} (IC 95 %: {rar_li:.1%} a {rar_ls:.1%})")
print(f"NNT = {nnt:.0f} (IC 95 %: {1 / rar_ls:.0f} a {1 / rar_li:.0f}) durante 5 años")
""")
c.md("""
**Cómo se comunica a un paciente:** «De cada 100 personas como usted que no toman el fármaco, unas 12 tendrán un evento cardiovascular en 5 años. Con el fármaco, unas 8. Hay que tratar a unas 25 personas durante 5 años para evitar un evento».

El IC del NNT se obtiene invirtiendo los límites del IC de la reducción absoluta.
""")

c.titulo(3, "3.5 La misma RRR, NNT muy distintos")
c.md("""
El efecto relativo de un tratamiento suele ser parecido en pacientes de distinto riesgo basal, pero el beneficio absoluto **depende del riesgo de partida**.
""")
c.code("""
rrr = 1 / 3
print(f"Reducción relativa del riesgo constante: {rrr:.0%}\\n")
print(f"{'Riesgo basal a 5 años':>24} {'Riesgo con tratamiento':>24} {'RAR':>7} {'NNT':>6}")
for basal in [0.03, 0.06, 0.12, 0.24]:
    tratado = basal * (1 - rrr)
    print(f"{basal:>24.0%} {tratado:>24.1%} {basal - tratado:>7.1%} {1 / (basal - tratado):>6.0f}")
""")
c.md("""
El paciente del caso, con un riesgo del 3 %, tiene un NNT de 100; uno de alto riesgo, con un 24 %, de 13. Por eso las guías de prevención cardiovascular recomiendan tratar según el **riesgo absoluto** estimado (escalas como SCORE2). No basta con el valor del colesterol.
""")

c.titulo(3, "3.6 Tablas mayores: centro de salud y eventos")
c.code("""
tabla_centros = pd.crosstab(cohorte["centro"], cohorte["evento_cv_5a"])
chi2, p, gl, esperadas = stats.chi2_contingency(tabla_centros)
print(tabla_centros, "\\n")
print(f"Ji cuadrado = {chi2:.2f}, gl = {gl}, p = {p:.3f}")
print(f"Frecuencia esperada mínima: {esperadas.min():.1f}")
print((tabla_centros[1] / tabla_centros.sum(axis=1)).round(3).rename("Riesgo"))
""")

c.titulo(3, "Ampliación: casos y controles, solo la OR")
c.md("""
En un estudio de casos y controles se eligen, por ejemplo, 100 pacientes con infarto y 200 sin infarto, y se pregunta si fumaban. El número de casos lo fija el investigador, así que el «riesgo» de la tabla no estima el riesgo real. La OR, en cambio, no depende de esa elección:
""")
c.code("""
# Expuestos (fumadores): 45 casos y 50 controles; no expuestos: 55 casos y 150 controles
for controles_por_caso in [2, 4]:
    a, c_ = 45, 55
    b, d = 50 * controles_por_caso // 2, 150 * controles_por_caso // 2
    m = medidas_2x2(a, b, c_, d)
    print(f"{controles_por_caso} controles por caso: «RR» = {m['RR'][0]:.2f} · OR = {m['OR'][0]:.2f}")
""")
c.md("""
Al duplicar el número de controles, el falso «RR» cambia; la OR no. En casos y controles, solo la OR tiene sentido.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Calcular un RR en un estudio de casos y controles.**

**Interpretar la OR como un RR cuando el evento es frecuente:** la OR exagera la asociación.

**Comunicar solo la reducción relativa del riesgo.** Da siempre la absoluta y el NNT.

**Dar el NNT sin el período de tiempo.** Un NNT de 25 a 5 años no es un NNT de 25 a 1 año.

**Interpretar una asociación como causal.** La cohorte es observacional: la asociación entre diabetes y eventos puede estar confundida, por ejemplo, por la edad (Tema 270).
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 230 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** calcular a mano el RR, la OR, la RAR y el NNT de tres tablas 2 × 2 de ensayos publicados.
2. **Misión clínica (con pistas):** estimar con IC el RR de evento cardiovascular de los fumadores y de los hipertensos tratados de la cohorte. Interpretarlos.
3. **Misión reto (con asistente):** una nota de prensa da solo la reducción relativa del riesgo. Reescribirla con el asistente para que incluya la absoluta y el NNT. Comprobar los números.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("En un ensayo, el evento ocurre en el 10 % con placebo y en el 6 % con tratamiento. ¿Cuál es el NNT?", [
        ("25", True, "Correcto: RAR = 0,10 − 0,06 = 0,04; NNT = 1/0,04 = 25."),
        ("40", False, "Esa sería la reducción relativa en porcentaje."),
        ("4", False, "El NNT es el inverso de la RAR expresada como proporción."),
        ("1,67", False, "Ese es el cociente de riesgos 10/6."),
    ]),
    ("En el mismo ensayo (10 % frente a 6 %), ¿cuál es la reducción relativa del riesgo?", [
        ("40 %", True, "Correcto: RR = 0,6; RRR = 1 − 0,6 = 0,4."),
        ("4 %", False, "Esa es la reducción absoluta."),
        ("60 %", False, "Ese es el riesgo relativo expresado en porcentaje."),
        ("25 %", False, "25 es el NNT."),
    ]),
    ("En un estudio de casos y controles sobre tabaco y cáncer de vejiga, ¿qué medida de asociación debes usar?", [
        ("La odds ratio", True, "Correcto: en casos y controles no se puede estimar el riesgo."),
        ("El riesgo relativo", False, "El número de casos lo fija el investigador, así que los riesgos no son estimables."),
        ("El NNT", False, "El NNT requiere riesgos absolutos."),
        ("La diferencia de riesgos", False, "También requiere riesgos."),
    ]),
    ("Un estudio da un RR de 1,8 (IC 95 %: 0,9 a 3,6). ¿Qué concluyes?", [
        ("La asociación no es estadísticamente significativa; los datos son compatibles con ningún efecto o con uno grande", True, "Correcto: el IC del RR contiene el 1."),
        ("El factor duplica el riesgo de forma significativa", False, "El IC incluye el 1."),
        ("El factor protege", False, "El RR estimado es mayor que 1."),
        ("El IC está mal calculado porque es asimétrico", False, "El IC del RR es asimétrico por construirse en escala logarítmica."),
    ]),
    ("Un tratamiento con la misma reducción relativa del riesgo se aplica a un paciente de riesgo basal del 2 % y a otro del 20 %. ¿En cuál es menor el NNT?", [
        ("En el de riesgo basal del 20 %", True, "Correcto: la reducción absoluta es 10 veces mayor, y el NNT 10 veces menor."),
        ("En el de riesgo basal del 2 %", False, "Con poco riesgo de partida, el beneficio absoluto es pequeño."),
        ("Es igual en los dos", False, "El NNT depende del riesgo basal."),
        ("No se puede saber sin la OR", False, "Basta con el riesgo basal y la RRR."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La ji cuadrado contrasta la independencia de dos variables cualitativas.
- RR y DR en cohortes y ensayos; en casos y controles, solo la OR.
- La OR se parece al RR solo si el evento es raro.
- Comunica siempre la reducción absoluta y el NNT, con su período de tiempo, además de la relativa.
- El beneficio absoluto de un tratamiento depende del riesgo basal del paciente.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Tabla de contingencia | Tabla de frecuencias cruzadas de dos variables cualitativas |
| Riesgo | Proporción de individuos que presentan el evento en un período |
| Odds | Cociente entre los que presentan el evento y los que no |
| Riesgo relativo (RR) | Cociente de riesgos entre expuestos y no expuestos |
| Odds ratio (OR) | Cociente de odds entre expuestos y no expuestos |
| Diferencia de riesgos (DR) | Diferencia de riesgos entre expuestos y no expuestos |
| Reducción relativa del riesgo (RRR) | 1 − RR, cuando el tratamiento reduce el riesgo |
| Reducción absoluta del riesgo (RAR) | Diferencia de riesgos entre control y tratamiento |
| Número necesario a tratar (NNT) | Inverso de la RAR: pacientes a tratar para evitar un evento |
| Número necesario para dañar (NND) | Inverso del aumento absoluto del riesgo de un efecto adverso |
""")

c.titulo(2, "Para saber más")
c.md("""
- Laupacis A, Sackett DL, Roberts RS. An assessment of clinically useful measures of the consequences of treatment. *N Engl J Med*. 1988;318(26):1728-1733. doi:[10.1056/NEJM198806303182605](https://doi.org/10.1056/NEJM198806303182605)
- Altman DG. Confidence intervals for the number needed to treat. *BMJ*. 1998;317(7168):1309-1312. doi:[10.1136/bmj.317.7168.1309](https://doi.org/10.1136/bmj.317.7168.1309)
- SCORE2 working group and ESC Cardiovascular risk collaboration. SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe. *Eur Heart J*. 2021;42(25):2439-2454. doi:[10.1093/eurheartj/ehab309](https://doi.org/10.1093/eurheartj/ehab309)
""")

c.pie(230)
print(c.guardar("../cuadernos"))
