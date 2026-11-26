from plantilla import Cuaderno

c = Cuaderno("Tema_270_Modelos_de_regresion_lineal_simple_y_multiple.ipynb")

c.cabecera(
    270,
    "Modelos de regresión lineal simple y múltiple",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Ajustar un modelo de regresión lineal simple e interpretar su pendiente, su intervalo de confianza y su R².
2. Ajustar un modelo de regresión lineal **múltiple** con variables cuantitativas y cualitativas, e interpretar cada coeficiente **ajustado** por las demás.
3. Reconocer la **confusión** y usar la regresión múltiple para controlarla.
4. Comprobar las condiciones del modelo con el análisis de los residuos.
5. Reconocer los límites del ajuste estadístico: confusión residual y confusión por indicación.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: de la recta al modelo múltiple | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En la cohorte cardiovascular, los pacientes con la presión sistólica más alta tienen también la creatinina más alta. Un residente lo interpreta como una prueba de que la hipertensión está dañando el riñón de estos pacientes y propone intensificar el tratamiento antihipertensivo para proteger la función renal.

Antes de aceptarlo, hay que preguntarse: ¿hay **otra variable** que eleve a la vez la PAS y la creatinina? La edad es la candidata evidente: con los años sube la presión arterial y disminuye la función renal (Tema 130). Si la edad explica la asociación, entre pacientes de **la misma edad** la PAS y la creatinina no deberían estar relacionadas.

La **regresión lineal múltiple** permite hacer esa comparación «a igualdad de edad» y estimar el efecto de cada variable **ajustado** por las demás.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 La regresión lineal simple")
c.md("""
$$Y = \\beta_0 + \\beta_1 X + \\varepsilon$$

| Elemento | Significado | En PAS = β₀ + β₁ · edad |
| --- | --- | --- |
| β₀ (ordenada en el origen) | Valor medio de *Y* cuando *X* = 0 | PAS a los 0 años: sin sentido clínico, fuera del rango de los datos |
| β₁ (pendiente) | Cambio medio de *Y* por cada unidad de *X* | mmHg que aumenta la PAS por cada año |
| ε (error o residuo) | Lo que el modelo no explica | Variabilidad entre pacientes de la misma edad |
| R² | Proporción de la variabilidad de *Y* explicada por el modelo | Entre 0 y 1 |

Se estima por **mínimos cuadrados**: la recta que hace mínima la suma de los residuos al cuadrado. Para β₁ se calcula un IC 95 % y un contraste de $H_0$: β₁ = 0 (Tema 130 vio la correlación; la regresión además cuantifica cuánto cambia *Y*).
""")
c.titulo(3, "2.2 La regresión lineal múltiple")
c.md("""
$$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\dots + \\beta_k X_k + \\varepsilon$$

Cada coeficiente $\\beta_j$ es el cambio medio de *Y* por unidad de $X_j$ **manteniendo constantes las demás variables del modelo**. Es un efecto **ajustado**.

Las variables **cualitativas** se incluyen como variables indicadoras (0/1): con `sexo`, el coeficiente de «Mujer» es la diferencia media entre mujeres y hombres (la categoría de referencia), a igualdad de las demás variables.
""")
c.titulo(3, "2.3 Confusión")
c.md("""
Una variable es **de confusión** si está asociada a la exposición y al resultado, y no es un paso intermedio entre ambas. Distorsiona la asociación observada.

```
           Edad
         ↙      ↘
      PAS   ···?···   Creatinina
```

Señal de confusión: el coeficiente de la exposición **cambia mucho** al añadir la variable al modelo (como orientación, más de un 10 %).

El ajuste solo controla las variables **medidas e incluidas**. Siempre puede quedar **confusión residual** por variables no medidas o mal medidas. Por eso los estudios observacionales, aun ajustados, no demuestran causalidad, y el ensayo clínico aleatorizado sigue siendo la referencia: la aleatorización reparte por igual también los factores que no se han medido.
""")
c.titulo(3, "2.4 Condiciones del modelo")
c.md("""
| Condición | Cómo comprobarla |
| --- | --- |
| Linealidad | Residuos frente a valores ajustados: sin patrón curvo |
| Independencia de las observaciones | Por el diseño |
| Varianza constante de los residuos (homocedasticidad) | Residuos frente a ajustados: sin forma de embudo |
| Normalidad de los residuos | Gráfico Q-Q de los residuos (importa poco con *n* grande) |
| Sin colinealidad extrema entre predictores | Correlación entre los predictores |
""")

c.titulo(2, "3. Demostración: de la recta al modelo múltiple (20 min)")
c.titulo(3, "3.1 Regresión simple: PAS y edad")
c.code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

cohorte = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_limpia.csv")

simple = smf.ols("pas_mmHg ~ edad", data=cohorte).fit()
b0, b1 = simple.params
li, ls = simple.conf_int().loc["edad"]
print(f"PAS = {b0:.1f} + {b1:.3f} · edad")
print(f"Pendiente: {b1:.3f} mmHg por año (IC 95 %: {li:.3f} a {ls:.3f}), p = {simple.pvalues['edad']:.1e}")
print(f"Por cada 10 años: {10 * b1:.1f} mmHg más")
print(f"R² = {simple.rsquared:.3f} · n = {int(simple.nobs)}")
""")
c.code("""
x = np.linspace(cohorte["edad"].min(), cohorte["edad"].max(), 100)
prediccion = simple.get_prediction(pd.DataFrame({"edad": x})).summary_frame(alpha=0.05)

plt.figure(figsize=(7, 4.5))
plt.scatter(cohorte["edad"], cohorte["pas_mmHg"], alpha=0.35, s=15)
plt.plot(x, prediccion["mean"], color="firebrick", label="Recta ajustada")
plt.fill_between(x, prediccion["mean_ci_lower"], prediccion["mean_ci_upper"], color="firebrick", alpha=0.25,
                 label="IC 95 % de la media")
plt.fill_between(x, prediccion["obs_ci_lower"], prediccion["obs_ci_upper"], color="gray", alpha=0.12,
                 label="Intervalo de predicción 95 % (pacientes)")
plt.xlabel("Edad (años)")
plt.ylabel("PAS (mmHg)")
plt.legend()
plt.show()
""")
c.md("""
Dos bandas distintas: el **IC de la media** (estrecho) dice dónde está la PAS media de los pacientes de cada edad; el **intervalo de predicción** (ancho) dice dónde estará la PAS de **un paciente concreto**. La edad explica alrededor de una cuarta parte de la variabilidad de la PAS: es un predictor importante, pero conocer la edad de un paciente no permite adivinar su presión.
""")

c.titulo(3, "3.2 Regresión múltiple: PAS, edad, IMC, sexo y diabetes")
c.code("""
multiple = smf.ols("pas_mmHg ~ edad + imc + sexo + diabetes", data=cohorte).fit()
tabla = pd.DataFrame({
    "Coeficiente": multiple.params,
    "IC 95 % inf.": multiple.conf_int()[0],
    "IC 95 % sup.": multiple.conf_int()[1],
    "p": multiple.pvalues,
}).round(3)
print(f"n = {int(multiple.nobs)} · R² = {multiple.rsquared:.3f} · R² ajustado = {multiple.rsquared_adj:.3f}")
tabla
""")
c.md("""
**Interpretación de los coeficientes:**

- **Edad:** a igualdad de IMC, sexo y diabetes, cada año más se asocia con una PAS media unos 0,55 mmHg mayor.
- **IMC:** a igualdad de edad, sexo y diabetes, cada kg/m² más se asocia con unos 0,85 mmHg más de PAS: unos 4 mmHg por cada 5 kg/m².
- **Sexo y diabetes:** sus IC incluyen el 0; con estos datos no hay evidencia de diferencias de PAS a igualdad de las demás variables.

Fíjate en que el modelo se ajusta con 380 pacientes, no con 400: los que tienen algún dato perdido se excluyen. Siempre hay que indicar el *n* del modelo.
""")

c.titulo(3, "3.3 Confusión: PAS y creatinina")
c.code("""
analiticas = pd.read_csv("https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/analiticas.csv")
renal = cohorte.merge(analiticas, on="id").dropna(subset=["creatinina_mg_dl"])

cruda = smf.ols("creatinina_mg_dl ~ pas_mmHg", data=renal).fit()
ajustada = smf.ols("creatinina_mg_dl ~ pas_mmHg + edad", data=renal).fit()

for nombre, m in [("Sin ajustar", cruda), ("Ajustado por edad", ajustada)]:
    b = m.params["pas_mmHg"] * 10
    li, ls = m.conf_int().loc["pas_mmHg"] * 10
    print(f"{nombre:>18}: {b:.3f} mg/dL por cada 10 mmHg (IC 95 %: {li:.3f} a {ls:.3f}), p = {m.pvalues['pas_mmHg']:.3f}")

cambio = 1 - ajustada.params["pas_mmHg"] / cruda.params["pas_mmHg"]
print(f"El coeficiente de la PAS se reduce un {cambio:.0%} al ajustar por edad")
""")
c.md("""
Al comparar pacientes de la misma edad, la asociación entre PAS y creatinina se reduce en más de dos tercios y deja de ser significativa: buena parte de la asociación cruda se debía a que los pacientes mayores tienen a la vez la PAS más alta y la creatinina más alta. Que la asociación ajustada sea pequeña en esta cohorte **no** demuestra que la hipertensión no dañe el riñón (lo hace, a largo plazo); demuestra que la asociación cruda no servía como prueba.
""")

c.titulo(3, "3.4 Diagnóstico del modelo: los residuos")
c.code("""
import scipy.stats as stats

fig, ejes = plt.subplots(1, 2, figsize=(10, 4))
ejes[0].scatter(multiple.fittedvalues, multiple.resid, alpha=0.4, s=15)
ejes[0].axhline(0, color="black", linestyle="--")
ejes[0].set_xlabel("PAS ajustada por el modelo (mmHg)")
ejes[0].set_ylabel("Residuo (mmHg)")
ejes[0].set_title("Residuos frente a ajustados")
stats.probplot(multiple.resid, plot=ejes[1])
ejes[1].set_title("Gráfico Q-Q de los residuos")
plt.tight_layout()
plt.show()
""")
c.md("""
Los residuos se reparten de manera homogénea alrededor de 0, sin curvas ni forma de embudo, y siguen aproximadamente la recta del gráfico Q-Q: el modelo lineal es adecuado.
""")

c.titulo(3, "3.5 Una trampa: la confusión por indicación")
c.code("""
indicacion = smf.ols("pas_mmHg ~ edad + imc + hta_tratada", data=cohorte).fit()
b = indicacion.params["hta_tratada[T.Sí]"]
li, ls = indicacion.conf_int().loc["hta_tratada[T.Sí]"]
print(f"Coeficiente del tratamiento antihipertensivo: {b:+.1f} mmHg (IC 95 %: {li:.1f} a {ls:.1f})")
""")
c.md("""
El modelo dice que los pacientes tratados tienen una PAS **unos 17 mmHg mayor**. ¿Los antihipertensivos suben la presión? No: se trata a los que tienen la presión alta. El tratamiento es una **consecuencia** de la PAS elevada, no su causa. Es la **confusión por indicación**, el sesgo más frecuente al evaluar tratamientos con datos observacionales, y la razón por la que la eficacia de un fármaco se demuestra con ensayos aleatorizados.

Lo mismo ocurre al evaluar herramientas de IA con datos de la historia clínica: si los médicos usan más el asistente en los casos difíciles, los casos con asistente tendrán peor evolución sin que el asistente haga daño.
""")

c.titulo(3, "Ampliación: predecir con el modelo")
c.code("""
pacientes = pd.DataFrame({"edad": [45, 70], "imc": [24, 33], "sexo": ["Mujer", "Hombre"], "diabetes": ["No", "Sí"]})
pred = multiple.get_prediction(pacientes).summary_frame(alpha=0.05)
for i, fila in pacientes.iterrows():
    print(f"{fila['sexo']} de {fila['edad']} años, IMC {fila['imc']}, diabetes {fila['diabetes']}: "
          f"PAS esperada {pred.loc[i, 'mean']:.0f} mmHg (intervalo de predicción 95 %: "
          f"{pred.loc[i, 'obs_ci_lower']:.0f} a {pred.loc[i, 'obs_ci_upper']:.0f})")
""")
c.md("""
Los modelos predictivos se tratan en el Tema 290. Ya se ve aquí su límite: aunque el modelo estime bien la media, un paciente individual puede estar muy lejos de ella.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Interpretar un coeficiente ajustado como causal.**

**Ajustar por una variable intermedia** del camino causal (por ejemplo, ajustar el efecto de la obesidad sobre los eventos por la PAS): se elimina parte del efecto que se quiere medir.

**Extrapolar fuera del rango de los datos.** La ordenada en el origen (edad 0) no tiene sentido.

**Confundir el IC de la media con el intervalo de predicción.**

**Incluir demasiadas variables para el tamaño muestral.** Como orientación, al menos 10 a 20 observaciones por predictor.

**Seleccionar las variables por su valor p.** Elígelas por conocimiento clínico, antes de ver los datos.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 270 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** interpretar los coeficientes de cuatro modelos publicados y decidir cuáles son ajustados.
2. **Misión clínica (con pistas):** estimar la asociación entre el IMC y el HDL, crudo y ajustado por sexo, y decidir si hay confusión.
3. **Misión reto (con asistente):** pedir al asistente un modelo para «el efecto del tratamiento antihipertensivo» con los datos de la cohorte, detectar la confusión por indicación y redactar por qué el resultado no es válido.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("En el modelo PAS = 92 + 0,56 · edad, ¿qué significa 0,56?", [
        ("La PAS media aumenta 0,56 mmHg por cada año de edad", True, "Correcto: es la pendiente."),
        ("La correlación entre PAS y edad es 0,56", False, "La pendiente no es la correlación."),
        ("El 56 % de la PAS se debe a la edad", False, "Esa interpretación correspondería a R², y tampoco sería causal."),
        ("La PAS de un recién nacido", False, "Eso sería la ordenada en el origen, sin sentido clínico aquí."),
    ]),
    ("En un modelo múltiple, el coeficiente del IMC es 0,85 mmHg por kg/m². ¿Cómo se interpreta?", [
        ("Por cada kg/m² más, la PAS media es 0,85 mmHg mayor a igualdad de las demás variables del modelo", True, "Correcto: es un efecto ajustado."),
        ("Bajar 1 kg/m² reduce la PAS 0,85 mmHg en cualquier paciente", False, "Es una asociación media observacional, no un efecto causal individual."),
        ("El IMC explica el 85 % de la PAS", False, "El coeficiente no es una proporción explicada."),
        ("Es el efecto sin ajustar del IMC", False, "En un modelo múltiple el coeficiente está ajustado."),
    ]),
    ("Al añadir la edad al modelo, el coeficiente de la PAS sobre la creatinina pasa de 0,11 a 0,03. ¿Qué indica?", [
        ("Que la edad confundía buena parte de la asociación entre PAS y creatinina", True, "Correcto: el coeficiente cambia mucho al ajustar."),
        ("Que la edad es un error de medida", False, "La edad es una variable de confusión."),
        ("Que la PAS protege el riñón", False, "El coeficiente sigue siendo positivo, aunque menor."),
        ("Que el modelo está mal ajustado", False, "Es el resultado esperable si hay confusión."),
    ]),
    ("Los pacientes que reciben estatinas tienen más eventos cardiovasculares que los que no las reciben, incluso ajustando por edad. ¿Cuál es la explicación más probable?", [
        ("Confusión por indicación: se prescriben estatinas a los pacientes de mayor riesgo", True, "Correcto: el tratamiento es un marcador del riesgo basal."),
        ("Las estatinas causan eventos cardiovasculares", False, "Los ensayos aleatorizados demuestran lo contrario."),
        ("El modelo tiene pocos pacientes", False, "El problema es de diseño, no de tamaño."),
        ("Falta normalidad en los residuos", False, "No explica la dirección del efecto."),
    ]),
    ("¿Qué intervalo usas para decir entre qué valores estará la PAS de un paciente concreto según el modelo?", [
        ("El intervalo de predicción", True, "Correcto: incluye la variabilidad individual además de la incertidumbre de la media."),
        ("El IC 95 % de la media", False, "Ese intervalo es para la PAS media de los pacientes con esas características."),
        ("El IC 95 % de la pendiente", False, "Ese intervalo es para el coeficiente."),
        ("El R²", False, "R² no es un intervalo."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La pendiente es el cambio medio de *Y* por unidad de *X*; R², la proporción de variabilidad explicada.
- En la regresión múltiple, cada coeficiente está ajustado por las demás variables del modelo.
- La confusión se detecta cuando el coeficiente cambia mucho al ajustar.
- El ajuste no elimina la confusión residual ni la confusión por indicación.
- Comprueba los residuos e indica siempre el *n* del modelo.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Regresión lineal simple | Modelo que relaciona una variable cuantitativa con un predictor mediante una recta |
| Pendiente (β₁) | Cambio medio de la respuesta por unidad del predictor |
| Mínimos cuadrados | Método que estima los coeficientes minimizando la suma de los residuos al cuadrado |
| Residuo | Diferencia entre el valor observado y el valor ajustado por el modelo |
| R² | Proporción de la variabilidad de la respuesta explicada por el modelo |
| Regresión lineal múltiple | Modelo con varios predictores, cuyos coeficientes están ajustados entre sí |
| Variable indicadora | Variable 0/1 que representa una categoría de una variable cualitativa |
| Confusión | Distorsión de una asociación por una tercera variable asociada a la exposición y al resultado |
| Confusión residual | Confusión que persiste tras el ajuste, por variables no medidas o mal medidas |
| Confusión por indicación | Confusión debida a que el tratamiento se indica según el pronóstico del paciente |
| Intervalo de predicción | Intervalo para el valor de un individuo nuevo |
""")

c.titulo(2, "Para saber más")
c.md("""
- Schneider A, Hommel G, Blettner M. Linear regression analysis: part 14 of a series on evaluation of scientific publications. *Dtsch Arztebl Int*. 2010;107(44):776-782.
- Kyriacou DN, Lewis RJ. Confounding by indication in clinical research. *JAMA*. 2016;316(17):1818-1819.
- Hernán MA, Robins JM. *Causal Inference: What If*. Boca Ratón: Chapman & Hall/CRC; 2020.
""")

c.pie(270)
print(c.guardar("../cuadernos"))
