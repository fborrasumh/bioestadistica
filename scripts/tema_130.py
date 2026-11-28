from plantilla import Cuaderno

c = Cuaderno("Tema_130_Analisis_bivariante_asociacion_y_correlacion.ipynb")

c.cabecera(
    130,
    "Análisis bivariante y representación gráfica de datos clínicos: asociación y correlación",
    "Módulo 3. Procesado inicial de datos",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Elegir el gráfico y el resumen adecuados según el tipo de las dos variables que se relacionan.
2. Calcular e interpretar los coeficientes de correlación de Pearson y de Spearman.
3. Reconocer las limitaciones de la correlación: relaciones no lineales, valores atípicos y variables de confusión.
4. Comparar una variable cuantitativa entre grupos con diagramas de caja y de violín.
5. Representar la relación entre dos variables categóricas con barras de porcentajes.
6. Construir un mapa de calor de correlaciones con Seaborn.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: relacionar variables clínicas | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un titular de prensa afirma: «Los países que más chocolate consumen tienen más premios Nobel». La correlación es real: se publicó en una revista médica de prestigio en 2012, en tono deliberadamente irónico. Pero nadie diría que comer chocolate hace ganar un Nobel: ambos se asocian a la riqueza de los países.

En el registro cardiovascular ocurre algo parecido. Al cruzar la presión arterial sistólica con la creatinina aparece una correlación positiva. ¿La hipertensión daña el riñón? ¿O ambas aumentan con la **edad**?

Medir la relación entre dos variables es el primer paso para estudiar factores de riesgo. Interpretarla bien exige recordar siempre que **asociación no es causalidad**.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Qué gráfico y qué resumen")
c.md("""
| Variables | Gráfico | Resumen | Ejemplo clínico |
| --- | --- | --- | --- |
| Cuantitativa y cuantitativa | Dispersión | Correlación de Pearson o Spearman | Edad y presión arterial |
| Cualitativa y cuantitativa | Cajas o violín por grupo | Media o mediana por grupo | HDL según sexo |
| Cualitativa y cualitativa | Barras de porcentajes | Tabla de contingencia | Tabaco y evento cardiovascular |
""")
c.titulo(3, "2.2 Los coeficientes de correlación")
c.md("""
El **coeficiente de correlación de Pearson** (*r*) mide la intensidad de la relación **lineal** entre dos variables cuantitativas:

$$r = \\frac{\\sum (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum (x_i - \\bar{x})^2 \\sum (y_i - \\bar{y})^2}}$$

- Va de −1 a +1. El signo indica el sentido; el valor absoluto, la intensidad.
- *r* = 0 indica ausencia de relación **lineal**, no ausencia de relación.
- Es sensible a los valores atípicos.

El **coeficiente de Spearman** (ρ) aplica la misma fórmula a los **rangos** (posiciones) de los datos. Mide relaciones **monótonas** (que siempre crecen o siempre decrecen, aunque no sea en línea recta) y es robusto frente a valores atípicos. Se usa también con variables ordinales.

| Valor absoluto | Interpretación orientativa |
| --- | --- |
| < 0,3 | Débil |
| 0,3 a 0,7 | Moderada |
| > 0,7 | Fuerte |

El cuadrado de *r* (*r*²) es la proporción de la variabilidad de una variable que se asocia linealmente con la otra.
""")
c.titulo(3, "2.3 Asociación no es causalidad")
c.diagrama('Cuatro esquemas: X causa Y, Y causa X, Z causa X e Y (confusión) y azar.')
c.md("""
Una correlación entre X e Y puede deberse a:

1. Que X cause Y.
2. Que Y cause X (causalidad inversa).
3. Que una tercera variable Z cause ambas: **confusión**.
4. El azar, sobre todo en muestras pequeñas.

Los criterios de Bradford Hill (1965) y, sobre todo, el diseño del estudio (Tema 230) ayudan a decidir si una asociación puede ser causal.
""")

c.titulo(2, "3. Demostración: relacionar variables clínicas (20 min)")
c.titulo(3, "3.1 Datos")
c.code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATOS = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/"
datos = pd.read_csv(DATOS + "cohorte_limpia.csv").merge(pd.read_csv(DATOS + "analiticas.csv"), on="id", how="left")
print(datos.shape)
""")

c.titulo(3, "3.2 Dos variables cuantitativas: edad y presión sistólica")
c.code("""
plt.figure(figsize=(6, 4.5))
sns.regplot(data=datos, x="edad", y="pas_mmHg", scatter_kws={"alpha": 0.4}, line_kws={"color": "firebrick"})
plt.xlabel("Edad (años)")
plt.ylabel("Presión arterial sistólica (mmHg)")
plt.title("Edad y presión arterial sistólica")
plt.show()

r = datos["edad"].corr(datos["pas_mmHg"])
rho = datos["edad"].corr(datos["pas_mmHg"], method="spearman")
print(f"Pearson r = {r:.2f} · r² = {r**2:.2f} · Spearman ρ = {rho:.2f}")
""")
c.md("""
Correlación positiva y moderada: la PAS tiende a aumentar con la edad. Con *r*² ≈ 0,23, la edad se asocia con casi una cuarta parte de la variabilidad de la PAS. El resto depende de otros factores.
""")

c.titulo(3, "3.3 Las tres trampas de la correlación")
c.md("""
Simulamos tres situaciones para ver por qué **siempre hay que mirar el gráfico** antes de interpretar *r*.
""")
c.code("""
rng = np.random.default_rng(130)
x = rng.uniform(0, 10, 60)
x_atipico = np.append(rng.uniform(0, 5, 59), 25)

casos = {
    "Relación lineal": (x, 2 * x + rng.normal(0, 3, 60)),
    "Relación curva (en U)": (x, (x - 5) ** 2 + rng.normal(0, 2, 60)),
    "Sin relación + un valor atípico": (x_atipico, np.append(rng.normal(10, 2, 59), 40)),
}

fig, ejes = plt.subplots(1, 3, figsize=(13, 3.8))
for eje, (titulo, (xs, ys)) in zip(ejes, casos.items()):
    r = np.corrcoef(xs, ys)[0, 1]
    rho = pd.Series(xs).corr(pd.Series(ys), method="spearman")
    eje.scatter(xs, ys, alpha=0.6)
    eje.set_title(f"{titulo}\\nPearson {r:.2f} · Spearman {rho:.2f}")
plt.tight_layout()
plt.show()
""")
c.md("""
- **Relación curva:** hay una relación muy clara, pero *r* ≈ 0 porque no es lineal. Ocurre, por ejemplo, entre el IMC y la mortalidad, que aumenta en los dos extremos.
- **Un solo valor atípico** fabrica una correlación de Pearson alta en datos sin relación. Spearman apenas se altera.
""")

c.titulo(3, "3.4 La confusión: presión arterial y creatinina")
c.code("""
print(f"PAS y creatinina: r = {datos['pas_mmHg'].corr(datos['creatinina_mg_dl']):.2f}")
print(f"Edad y PAS:       r = {datos['edad'].corr(datos['pas_mmHg']):.2f}")
print(f"Edad y creatinina: r = {datos['edad'].corr(datos['creatinina_mg_dl']):.2f}")
""")
c.md("""
Si la asociación entre PAS y creatinina fuera fruto de la edad, debería **debilitarse al comparar pacientes de edad parecida**. Lo comprobamos dentro de grupos de edad:
""")
c.code("""
datos["grupo_edad"] = pd.cut(datos["edad"], bins=[40, 55, 70, 86], right=False, labels=["40-54", "55-69", "70-85"])

for grupo, sub in datos.groupby("grupo_edad", observed=True):
    r = sub["pas_mmHg"].corr(sub["creatinina_mg_dl"])
    print(f"{grupo} años: r = {r:.2f} (n = {sub['creatinina_mg_dl'].notna().sum()})")
""")
c.md("""
Interpreta el resultado. Si las correlaciones dentro de cada grupo de edad son más débiles que la global, parte de la asociación se explicaba por la edad. Si en algún grupo persiste, puede haber **confusión residual** (dentro de un grupo de 15 años la edad todavía varía) o una relación real. Analizar **estratificando** por la posible variable de confusión es la idea que, en el Tema 270, desarrollaremos con la regresión múltiple.
""")

c.titulo(3, "3.5 Cualitativa y cuantitativa: el HDL según el sexo")
c.code("""
fig, ejes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
sns.boxplot(data=datos, x="sexo", y="hdl_mg_dl", ax=ejes[0])
sns.violinplot(data=datos, x="sexo", y="hdl_mg_dl", ax=ejes[1], inner="quartile")
ejes[0].set_title("Diagrama de caja")
ejes[1].set_title("Diagrama de violín")
for eje in ejes:
    eje.set_xlabel("")
ejes[0].set_ylabel("Colesterol HDL (mg/dL)")
plt.tight_layout()
plt.show()

datos.groupby("sexo")["hdl_mg_dl"].agg(["count", "mean", "std", "median"]).round(1)
""")
c.md("""
El **diagrama de violín** añade a la caja la forma completa de la distribución. Las mujeres tienen, en promedio, un HDL más alto, como se describe en la literatura. En el Tema 250 aprenderemos a decidir si una diferencia entre grupos puede deberse al azar.
""")

c.titulo(3, "3.6 Dos variables cualitativas: diabetes y evento cardiovascular")
c.code("""
porcentajes = pd.crosstab(datos["diabetes"], datos["evento_cv_5a"], normalize="index") * 100
porcentajes.columns = ["Sin evento", "Con evento"]

porcentajes.plot(kind="bar", stacked=True, figsize=(6, 4), color=["lightsteelblue", "firebrick"])
plt.ylabel("Porcentaje de pacientes (%)")
plt.xlabel("Diabetes")
plt.xticks(rotation=0)
plt.title("Evento cardiovascular a 5 años según diabetes")
plt.legend(loc="upper right")
plt.show()

porcentajes.round(1)
""")

c.titulo(3, "3.7 Mapa de calor de correlaciones")
c.code("""
variables = ["edad", "imc", "pas_mmHg", "pad_mmHg", "colesterol_mg_dl", "hdl_mg_dl",
             "glucemia_mg_dl", "hba1c_pct", "creatinina_mg_dl"]
matriz = datos[variables].corr(method="spearman")

plt.figure(figsize=(8, 6.5))
sns.heatmap(matriz, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True)
plt.title("Correlaciones de Spearman entre variables clínicas")
plt.show()
""")
c.md("""
Las correlaciones más fuertes tienen explicación clínica. La glucemia y la HbA1c miden el mismo fenómeno. La PAS y la PAD forman parte de la misma medición. Un mapa de calor sirve para **explorar**, no para concluir: con 36 parejas de variables, alguna correlación aparecerá por puro azar.
""")

c.titulo(3, "Ampliación: matriz de gráficos de dispersión")
c.code("""
sns.pairplot(datos[["edad", "pas_mmHg", "imc", "hba1c_pct", "diabetes"]].dropna(),
             hue="diabetes", plot_kws={"alpha": 0.5}, height=2.2)
plt.show()
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Concluir causalidad a partir de una correlación**, sin considerar la confusión ni la causalidad inversa.

**Interpretar *r* = 0 como ausencia de relación:** solo indica ausencia de relación lineal.

**Calcular la correlación de Pearson sin mirar el gráfico**, cuando un valor atípico o una curva la distorsionan.

**Usar Pearson con variables ordinales** como una escala de dolor: es más adecuado Spearman.

**Buscar correlaciones entre decenas de variables** y presentar solo las «interesantes»: es una forma de pescar resultados casuales.

**Representar dos categóricas con números absolutos** cuando los grupos tienen tamaños muy distintos: se comparan porcentajes.
""")

c.titulo(3, "Ampliación: Kendall y asociación entre variables cualitativas")
c.md("""
La **tau de Kendall** es otra correlación por rangos. Cuenta los pares de pacientes **concordantes** (los dos valores suben a la vez) y **discordantes**. Funciona bien con muestras pequeñas y con muchos empates.

Para dos variables **cualitativas** no hay correlación; hay **asociación**. Se mide a partir de la ji cuadrado (Tema 230):

| Medida | Tabla | Valores |
|---|---|---|
| Coeficiente φ (phi) | 2 × 2 | de 0 a 1 |
| V de Cramér | cualquier tamaño | de 0 a 1 (0 = sin asociación) |

**En tus materiales SIMUSTAT:** [Tema 210. Relación entre variables](https://colab.research.google.com/drive/1a9AGIVjIXXhIXdhwpWX0PiHnJdH212a4), apartado 1 (Kendall) y 2 (φ, V de Cramér).
""")
c.code("""
from scipy import stats

print("Edad y PAS:")
for metodo in ["pearson", "spearman", "kendall"]:
    print(f"  {metodo:9} r = {datos['edad'].corr(datos['pas_mmHg'], method=metodo):.2f}")

def v_cramer(x, y):
    tabla = pd.crosstab(x, y)
    chi2 = stats.chi2_contingency(tabla, correction=False)[0]
    return np.sqrt(chi2 / (tabla.values.sum() * (min(tabla.shape) - 1)))

print("\\nφ tabaco × evento cardiovascular:", round(v_cramer(datos["fumador"], datos["evento_cv_5a"]), 3))
print("V de Cramér centro × diabetes:  ", round(v_cramer(datos["centro"], datos["diabetes"]), 3))
""")
c.md("""
Kendall da valores más bajos que Spearman con los mismos datos; es normal, porque mide otra cosa (pares). Compara siempre coeficientes del mismo tipo. En una tabla 2 × 2, φ y la V de Cramér coinciden.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 130 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** emparejar gráficos de dispersión con su coeficiente de correlación.
2. **Misión clínica (con pistas):** estudiar la relación entre el IMC y la presión arterial, por separado en hombres y mujeres.
3. **Misión reto (con asistente):** pedir al asistente un análisis exploratorio de la cohorte, identificar qué conclusiones causales injustificadas propone y reescribirlas correctamente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("Entre el IMC y la mortalidad se observa una curva en U. ¿Qué valor de r de Pearson es esperable?", [
        ("Cercano a 0", True, "Correcto: la relación existe, pero no es lineal."),
        ("Cercano a 1", False, "Pearson mide relación lineal; una U no lo es."),
        ("Cercano a −1", False, "La relación no es lineal decreciente."),
        ("No se puede calcular", False, "Se puede calcular, pero no describe bien la relación."),
    ]),
    ("¿Qué gráfico es el más adecuado para comparar la glucemia entre diabéticos y no diabéticos?", [
        ("Diagramas de caja por grupo", True, "Correcto: una variable cuantitativa comparada entre categorías."),
        ("Gráfico de dispersión", False, "Se usa con dos variables cuantitativas."),
        ("Barras apiladas de porcentajes", False, "Se usan con dos variables categóricas."),
        ("Mapa de calor", False, "Resume correlaciones entre varias cuantitativas."),
    ]),
    ("En una cohorte, r = 0,45 entre el consumo de café y el infarto. Los bebedores de café fuman más. ¿Qué es lo más prudente concluir?", [
        ("Que la asociación puede deberse, en parte o por completo, al tabaco", True, "Correcto: el tabaco es una posible variable de confusión."),
        ("Que el café causa infartos", False, "Una correlación no demuestra causalidad."),
        ("Que no hay ninguna relación", False, "Hay una asociación; lo que se discute es su causa."),
        ("Que la correlación es fuerte y causal", False, "0,45 es moderada, y no prueba causalidad."),
    ]),
    ("¿En qué situación es preferible el coeficiente de Spearman al de Pearson?", [
        ("Con variables ordinales o con valores atípicos", True, "Correcto: trabaja con rangos y es robusto."),
        ("Siempre que haya más de 100 pacientes", False, "El tamaño muestral no decide la elección."),
        ("Cuando la relación es perfectamente lineal", False, "En ese caso Pearson es adecuado."),
        ("Con dos variables nominales", False, "Para dos nominales se usa una tabla de contingencia."),
    ]),
    ("Si r = 0,6 entre la edad y la PAS, ¿qué proporción de la variabilidad de la PAS se asocia linealmente con la edad?", [
        ("36 %", True, "Correcto: r² = 0,6² = 0,36."),
        ("60 %", False, "r no es una proporción de variabilidad; lo es r²."),
        ("6 %", False, "Revisa el cálculo: 0,6² = 0,36."),
        ("40 %", False, "40 % sería 1 − 0,6."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- El tipo de las dos variables decide el gráfico y el resumen.
- Pearson mide la relación lineal; Spearman, la monótona, y es robusto frente a atípicos.
- Mira siempre el gráfico antes de interpretar un coeficiente.
- Asociación no es causalidad: piensa en la confusión, la causalidad inversa y el azar.
- Estratificar por una posible variable de confusión es el primer paso para controlarla.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Análisis bivariante | Estudio de la relación entre dos variables |
| Correlación de Pearson | Medida de la relación lineal entre dos variables cuantitativas |
| Correlación de Spearman | Correlación calculada sobre los rangos; mide relaciones monótonas |
| Relación monótona | Relación en la que una variable siempre crece, o siempre decrece, cuando la otra aumenta |
| Coeficiente de determinación (*r*²) | Proporción de la variabilidad asociada linealmente con la otra variable |
| Variable de confusión | Variable relacionada con las dos variables estudiadas, que distorsiona su asociación |
| Estratificar | Analizar por separado dentro de categorías de una tercera variable |
| Diagrama de violín | Gráfico que combina el diagrama de caja con la forma de la distribución |
| Mapa de calor | Representación de una matriz con colores según el valor |
""")

c.titulo(2, "Para saber más")
c.md("""
- Messerli FH. Chocolate consumption, cognitive function, and Nobel laureates. *N Engl J Med*. 2012;367(16):1562-1564.
- Hill AB. The environment and disease: association or causation? *Proc R Soc Med*. 1965;58(5):295-300.
- [Galería de ejemplos de Seaborn](https://seaborn.pydata.org/examples/index.html)
- SIMUSTAT Unidigital UMH. [Tema 210. Relación entre variables](https://colab.research.google.com/drive/1a9AGIVjIXXhIXdhwpWX0PiHnJdH212a4). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(130)
print(c.guardar("../cuadernos"))
