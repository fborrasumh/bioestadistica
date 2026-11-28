from plantilla import Cuaderno

c = Cuaderno("Tema_160_Evaluacion_de_pruebas_diagnosticas_y_de_cribado.ipynb")

c.cabecera(
    160,
    "Evaluación de pruebas diagnósticas y de cribado: sensibilidad, especificidad y valores predictivos",
    "Módulo 4. Probabilidad",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 4 se hace **a mano**. Resuelve primero cada ejercicio con papel y calculadora, y usa el código solo para comprobar.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Construir la tabla 2 × 2 de una prueba diagnóstica frente a un patrón de referencia.
2. Calcular e interpretar sensibilidad, especificidad, valores predictivos y cocientes de probabilidad.
3. Explicar por qué los valores predictivos dependen de la prevalencia y la sensibilidad y la especificidad no.
4. Elegir un punto de corte para una prueba cuantitativa según su finalidad: cribado o confirmación.
5. Construir e interpretar una curva ROC y su área bajo la curva.
6. Reconocer los sesgos más frecuentes en los estudios de pruebas diagnósticas.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: evaluar una prueba | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En una consulta de Atención Primaria se valora a pacientes con **disnea** de reciente aparición. El péptido natriurético **NT-proBNP** ayuda a decidir si la causa puede ser una **insuficiencia cardiaca**. Es un marcador cuantitativo: los valores altos apuntan a esa causa.

Pero ¿a partir de qué valor se considera «positivo»? Un punto de corte bajo detecta casi todas las insuficiencias cardiacas, a costa de muchos falsos positivos que irán a una ecocardiografía innecesaria. Un punto de corte alto casi no da falsos positivos, pero deja sin diagnosticar a pacientes que sí la tienen.

Ninguna prueba es perfecta. Evaluar la prueba es **cuantificar sus aciertos y sus errores** frente a un **patrón de referencia**: aquí, la ecocardiografía y la valoración por Cardiología. Después, se elige el punto de corte que mejor sirve a su finalidad clínica.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 La tabla 2 × 2")
c.md("""
| | Enfermo (referencia +) | Sano (referencia −) | |
| --- | --- | --- | --- |
| **Prueba +** | VP (verdaderos positivos) | FP (falsos positivos) | VP + FP |
| **Prueba −** | FN (falsos negativos) | VN (verdaderos negativos) | FN + VN |
| | VP + FN | FP + VN | Total |
""")
c.titulo(3, "2.2 Los índices")
c.md("""
| Índice | Fórmula | Pregunta que responde | ¿Depende de la prevalencia? |
| --- | --- | --- | --- |
| **Sensibilidad** | VP / (VP + FN) | De los enfermos, ¿cuántos detecta? | No |
| **Especificidad** | VN / (VN + FP) | De los sanos, ¿cuántos descarta? | No |
| **Valor predictivo positivo** (VPP) | VP / (VP + FP) | Si da positivo, ¿qué probabilidad hay de enfermedad? | **Sí** |
| **Valor predictivo negativo** (VPN) | VN / (VN + FN) | Si da negativo, ¿qué probabilidad hay de no tenerla? | **Sí** |
| LR+ | Se / (1 − Sp) | ¿Cuánto multiplica un positivo las *odds* de enfermedad? | No |
| LR− | (1 − Se) / Sp | ¿Cuánto multiplica un negativo las *odds* de enfermedad? | No |

La sensibilidad y la especificidad son propiedades de la **prueba**. Los valores predictivos son lo que le importa al **paciente**. Dependen de la prevalencia, como vimos con el teorema de Bayes en el Tema 150.
""")
c.titulo(3, "2.3 Dos reglas para recordar")
c.diagrama('SnNOut: sensibilidad alta y negativo descarta. SpPIn: especificidad alta y positivo confirma.')
c.md("""
- **SpPIn**: una prueba muy **Sp**ecífica, si es **P**ositiva, confirma (*rule **in***). Útil para **confirmar**.
- **SnNOut**: una prueba muy **S**e**n**sible, si es **N**egativa, descarta (*rule **out***). Útil para **cribar** y descartar.
""")
c.titulo(3, "2.4 Punto de corte y curva ROC")
c.md("""
En una prueba cuantitativa, bajar el punto de corte aumenta la sensibilidad y disminuye la especificidad, y al revés. La **curva ROC** (*receiver operating characteristic*) representa todos los puntos de corte posibles: sensibilidad (eje Y) frente a 1 − especificidad (eje X).

- El **área bajo la curva** (AUC) va de 0,5 (la prueba no discrimina mejor que el azar) a 1 (discrimina perfectamente). Se interpreta como la probabilidad de que un enfermo elegido al azar tenga un valor más alto que un sano elegido al azar.
- El **índice de Youden** (Se + Sp − 1) identifica el punto de corte que maximiza a la vez sensibilidad y especificidad. No siempre es el más adecuado clínicamente.
""")

c.titulo(2, "3. Demostración: evaluar una prueba (20 min)")
c.titulo(3, "3.1 Una tabla 2 × 2 a mano")
c.md("""
Un estudio evalúa el NT-proBNP con un punto de corte de 125 pg/mL en 400 pacientes con disnea. La referencia confirma insuficiencia cardiaca en 100.

| | IC | No IC | Total |
| --- | --- | --- | --- |
| **NT-proBNP ≥ 125** | 95 | 90 | 185 |
| **NT-proBNP < 125** | 5 | 210 | 215 |
| Total | 100 | 300 | 400 |

**A mano:** Se = 95/100 = 0,95 · Sp = 210/300 = 0,70 · VPP = 95/185 ≈ 0,51 · VPN = 210/215 ≈ 0,98 · LR+ = 0,95/0,30 ≈ 3,2 · LR− = 0,05/0,70 ≈ 0,07.
""")
c.code('''
def indices_diagnosticos(vp, fp, fn, vn):
    """Calcula los índices de una prueba diagnóstica a partir de la tabla 2 × 2."""
    se = vp / (vp + fn)
    sp = vn / (vn + fp)
    return {
        "Sensibilidad": se,
        "Especificidad": sp,
        "VPP": vp / (vp + fp),
        "VPN": vn / (vn + fn),
        "Exactitud": (vp + vn) / (vp + fp + fn + vn),
        "LR+": se / (1 - sp) if sp < 1 else float("inf"),
        "LR−": (1 - se) / sp,
        "Prevalencia": (vp + fn) / (vp + fp + fn + vn),
    }


for indice, valor in indices_diagnosticos(vp=95, fp=90, fn=5, vn=210).items():
    print(f"{indice:>13}: {valor:.3f}")
''')
c.md("""
**Interpretación:** con una sensibilidad del 95 % y un VPN del 98 %, un NT-proBNP **negativo** descarta con bastante seguridad la insuficiencia cardiaca (SnNOut). Un resultado positivo, en cambio, solo acierta en la mitad de los casos (VPP del 51 %): hace falta una ecocardiografía para confirmar.
""")

c.titulo(3, "3.2 La misma prueba con otra prevalencia")
c.md("""
Sensibilidad y especificidad se mantienen; los valores predictivos cambian. Aplicamos Se = 0,95 y Sp = 0,70 a 1.000 pacientes con distintas prevalencias:
""")
c.code("""
import pandas as pd

filas = []
for prevalencia in [0.02, 0.10, 0.25, 0.50]:
    enfermos = 1000 * prevalencia
    sanos = 1000 - enfermos
    vp, fn = 0.95 * enfermos, 0.05 * enfermos
    vn, fp = 0.70 * sanos, 0.30 * sanos
    filas.append({"prevalencia": prevalencia, "VPP": vp / (vp + fp), "VPN": vn / (vn + fn)})

pd.DataFrame(filas).round(3)
""")
c.md("""
Con una prevalencia del 2 %, casi 19 de cada 20 positivos son falsos positivos. Por eso una prueba validada en un hospital (prevalencia alta) rinde peor en un cribado poblacional (prevalencia baja).
""")

c.titulo(3, "3.3 Una prueba cuantitativa: los datos")
c.md("""
Simulamos el NT-proBNP de 400 pacientes con disnea. Sus valores tienen una distribución muy asimétrica (Tema 120), por lo que se representan en escala logarítmica.
""")
c.code("""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=160)
ic = np.array([1] * 100 + [0] * 300)
ntprobnp = np.where(ic == 1,
                    rng.lognormal(np.log(900), 1.0, 400),
                    rng.lognormal(np.log(150), 1.0, 400)).round()

plt.figure(figsize=(7, 4))
bins = np.logspace(0.5, 4.5, 40)
plt.hist(ntprobnp[ic == 0], bins=bins, alpha=0.6, label="Sin insuficiencia cardiaca")
plt.hist(ntprobnp[ic == 1], bins=bins, alpha=0.6, label="Con insuficiencia cardiaca")
plt.axvline(125, color="black", linestyle="--", label="Punto de corte 125 pg/mL")
plt.xscale("log")
plt.xlabel("NT-proBNP (pg/mL, escala logarítmica)")
plt.ylabel("Número de pacientes")
plt.legend()
plt.show()
""")
c.md("""
Las dos distribuciones **se solapan**: cualquier punto de corte deja enfermos a la izquierda (falsos negativos) y sanos a la derecha (falsos positivos).
""")

c.titulo(3, "3.4 El efecto del punto de corte")
c.code("""
filas = []
for corte in [50, 125, 300, 600, 1000]:
    positivo = ntprobnp >= corte
    vp = (positivo & (ic == 1)).sum()
    fp = (positivo & (ic == 0)).sum()
    fn = (~positivo & (ic == 1)).sum()
    vn = (~positivo & (ic == 0)).sum()
    indices = indices_diagnosticos(vp, fp, fn, vn)
    filas.append({"corte (pg/mL)": corte, "Se": indices["Sensibilidad"], "Sp": indices["Especificidad"],
                  "VPP": indices["VPP"], "VPN": indices["VPN"]})

pd.DataFrame(filas).round(2)
""")

c.titulo(3, "3.5 La curva ROC")
c.code("""
cortes = np.unique(ntprobnp)[::-1]
sensibilidad = np.array([((ntprobnp >= k) & (ic == 1)).sum() / (ic == 1).sum() for k in cortes])
especificidad = np.array([((ntprobnp < k) & (ic == 0)).sum() / (ic == 0).sum() for k in cortes])

fpr = np.concatenate([[0], 1 - especificidad, [1]])
tpr = np.concatenate([[0], sensibilidad, [1]])
auc = np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2)   # regla del trapecio

youden = sensibilidad + especificidad - 1
mejor = youden.argmax()

plt.figure(figsize=(5.5, 5.5))
plt.plot(fpr, tpr, label=f"NT-proBNP (AUC = {auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle=":", color="gray", label="Azar (AUC = 0,5)")
plt.scatter(1 - especificidad[mejor], sensibilidad[mejor], color="firebrick", zorder=3,
            label=f"Máximo Youden: {cortes[mejor]:.0f} pg/mL")
plt.xlabel("1 − especificidad (falsos positivos)")
plt.ylabel("Sensibilidad")
plt.title("Curva ROC")
plt.legend(loc="lower right")
plt.show()

print(f"Punto de corte de Youden: {cortes[mejor]:.0f} pg/mL · Se = {sensibilidad[mejor]:.2f} · Sp = {especificidad[mejor]:.2f}")
""")
c.md("""
Comprobamos el área con scikit-learn, la biblioteca de aprendizaje automático más usada:
""")
c.code("""
from sklearn.metrics import roc_auc_score
print(f"AUC con scikit-learn: {roc_auc_score(ic, ntprobnp):.3f}")
""")
c.md("""
**¿Qué punto de corte elegir?** Depende de la finalidad. Para **descartar** insuficiencia cardiaca en Atención Primaria interesa una sensibilidad muy alta, aunque baje la especificidad: un corte bajo, como 125 pg/mL. El punto de Youden es un buen equilibrio estadístico. Pero no tiene en cuenta que un falso negativo es más grave que un falso positivo. El falso negativo es una insuficiencia cardiaca sin diagnosticar; el falso positivo, una ecocardiografía de más.
""")

c.titulo(3, "3.6 Un caso con datos de la cohorte: la HbA1c")
c.md("""
El criterio diagnóstico de diabetes con HbA1c usa un punto de corte de 6,5 %. Evaluamos ese corte en el registro cardiovascular, tomando como referencia el diagnóstico de diabetes registrado.
""")
c.code("""
DATOS = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/"
datos = pd.read_csv(DATOS + "cohorte_limpia.csv").merge(pd.read_csv(DATOS + "analiticas.csv"), on="id")
datos = datos.dropna(subset=["hba1c_pct"])

prueba = datos["hba1c_pct"] >= 6.5
referencia = datos["diabetes"] == "Sí"
print(pd.crosstab(prueba, referencia, rownames=["HbA1c ≥ 6,5 %"], colnames=["Diabetes"]))

vp, fp = (prueba & referencia).sum(), (prueba & ~referencia).sum()
fn, vn = (~prueba & referencia).sum(), (~prueba & ~referencia).sum()
for indice, valor in indices_diagnosticos(vp, fp, fn, vn).items():
    print(f"{indice:>13}: {valor:.3f}")
""")

c.titulo(3, "Ampliación: sesgos en los estudios de pruebas diagnósticas")
c.md("""
| Sesgo | Qué ocurre | Consecuencia |
| --- | --- | --- |
| De espectro | Se estudian enfermos graves y sanos muy sanos | Se sobreestiman Se y Sp |
| De verificación | Solo se aplica la referencia a quienes dan positivo | Se sobreestima la sensibilidad |
| De incorporación | La prueba evaluada forma parte del diagnóstico de referencia | Se sobreestiman Se y Sp |
| De revisión | Quien interpreta una prueba conoce el resultado de la otra | Se sobreestima el acuerdo |

La guía **STARD** (*Standards for Reporting Diagnostic Accuracy*) establece qué debe comunicar un estudio de exactitud diagnóstica para que se puedan valorar estos sesgos. Fíjate en el ejemplo de la HbA1c. Tiene sesgo de incorporación si el diagnóstico registrado de diabetes se basó en la propia HbA1c.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Confundir sensibilidad con valor predictivo positivo.** «La prueba detecta el 95 % de los enfermos» no significa que «el 95 % de los positivos estén enfermos».

**Trasladar valores predictivos** de un estudio a otra población con distinta prevalencia.

**Usar la exactitud global** como único índice. Con una prevalencia del 1 %, una «prueba» que dice siempre «sano» acierta en el 99 % de los casos.

**Elegir el punto de corte solo con el índice de Youden**, sin pensar en las consecuencias clínicas de cada tipo de error.

**Dar la AUC sin la curva:** dos pruebas con la misma AUC pueden comportarse de forma muy distinta en la zona de interés clínico.
""")

c.titulo(3, "Ampliación: Dos pruebas en paralelo o en serie")
c.md("""
Dos pruebas se pueden combinar de dos formas:

| Estrategia | El resultado es positivo si… | Sensibilidad | Especificidad | Uso |
|---|---|---|---|---|
| **En paralelo** | alguna prueba es positiva | sube | baja | descartar (Urgencias) |
| **En serie** | las dos pruebas son positivas | baja | sube | confirmar |

Las fórmulas del código suponen que las pruebas fallan de forma **independiente**. Si fallan en los mismos pacientes, la ganancia real es menor.

**En tus materiales SIMUSTAT:** [Tema 280. Conceptos de probabilidad y su uso en la evaluación de pruebas diagnósticas](https://colab.research.google.com/drive/1Gp4XYiZjO1WChLRRTHugtbQziSoJOR7N), apartado 4.
""")
c.code("""
se1, es1 = 0.85, 0.90     # prueba 1
se2, es2 = 0.75, 0.95     # prueba 2

se_par, es_par = 1 - (1 - se1) * (1 - se2), es1 * es2
se_ser, es_ser = se1 * se2, 1 - (1 - es1) * (1 - es2)

print(f"Prueba 1:    S = {se1:.1%}   E = {es1:.1%}")
print(f"Prueba 2:    S = {se2:.1%}   E = {es2:.1%}")
print(f"En paralelo: S = {se_par:.1%}   E = {es_par:.1%}")
print(f"En serie:    S = {se_ser:.1%}   E = {es_ser:.1%}")
""")
c.md("""
En paralelo se pierden menos enfermos (sensibilidad más alta), pero hay más falsos positivos. En serie ocurre lo contrario. Elige la estrategia según qué error es más grave para el paciente.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 160 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** completar tablas 2 × 2 a partir de enunciados clínicos y calcular a mano sus índices.
2. **Misión clínica (con pistas):** evaluar la troponina de alta sensibilidad en un conjunto sintético de dolor torácico. Elegir un punto de corte para descartar infarto.
3. **Misión reto (con asistente):** pedir al asistente la curva ROC de un marcador. Comprobar a mano la sensibilidad y la especificidad en dos puntos de corte. Justificar el corte elegido.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde a mano, sin asistente y sin ejecutar código.")
c.quiz([
    ("En 200 enfermos, la prueba es positiva en 180. ¿Qué índice has calculado con 180/200?", [
        ("La sensibilidad", True, "Correcto: la proporción de enfermos con prueba positiva."),
        ("El valor predictivo positivo", False, "El VPP se calcula sobre los positivos, no sobre los enfermos."),
        ("La especificidad", False, "La especificidad se calcula sobre los sanos."),
        ("La exactitud", False, "La exactitud usa todos los pacientes."),
    ]),
    ("Una prueba se valida en un hospital con prevalencia del 30 % y se aplica a un cribado con prevalencia del 1 %. ¿Qué índice empeorará?", [
        ("El valor predictivo positivo", True, "Correcto: con menos prevalencia, una mayor parte de los positivos son falsos positivos."),
        ("La sensibilidad", False, "La sensibilidad no depende de la prevalencia."),
        ("La especificidad", False, "La especificidad no depende de la prevalencia."),
        ("El valor predictivo negativo", False, "El VPN, de hecho, mejora al bajar la prevalencia."),
    ]),
    ("Quieres una prueba para descartar una enfermedad grave en Urgencias. ¿Qué propiedad es la más importante?", [
        ("Una sensibilidad muy alta", True, "Correcto: SnNOut, un negativo de una prueba muy sensible descarta."),
        ("Una especificidad muy alta", False, "La especificidad alta sirve para confirmar (SpPIn)."),
        ("Un valor predictivo positivo alto", False, "El VPP es útil para confirmar, no para descartar."),
        ("Una AUC de 0,5", False, "Una AUC de 0,5 significa que la prueba no discrimina."),
    ]),
    ("¿Qué indica una curva ROC con área bajo la curva de 0,5?", [
        ("Que la prueba no discrimina mejor que el azar", True, "Correcto: la curva coincide con la diagonal."),
        ("Que la prueba acierta en la mitad de los enfermos", False, "La AUC no es la sensibilidad."),
        ("Que la prueba es perfecta", False, "Una prueba perfecta tiene AUC = 1."),
        ("Que el mejor punto de corte es la mediana", False, "La AUC no indica el punto de corte."),
    ]),
    ("Una prueba tiene Se = 0,90 y Sp = 0,80. ¿Cuál es su LR+?", [
        ("4,5", True, "Correcto: 0,90 / (1 − 0,80) = 0,90 / 0,20."),
        ("1,125", False, "Eso es 0,90 / 0,80: hay que dividir entre 1 − Sp."),
        ("0,125", False, "Ese es el LR−: (1 − 0,90) / 0,80."),
        ("0,72", False, "Eso es multiplicar Se por Sp."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La tabla 2 × 2 compara la prueba con un patrón de referencia.
- Sensibilidad y especificidad describen la prueba; los valores predictivos dependen de la prevalencia.
- SpPIn para confirmar, SnNOut para descartar.
- En una prueba cuantitativa, el punto de corte intercambia sensibilidad por especificidad; la curva ROC muestra todas las opciones.
- El punto de corte se elige según la finalidad clínica y el coste de cada tipo de error.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Patrón de referencia | Método considerado el mejor disponible para establecer el diagnóstico |
| Sensibilidad | Proporción de enfermos con prueba positiva |
| Especificidad | Proporción de sanos con prueba negativa |
| Valor predictivo positivo | Proporción de positivos que están enfermos |
| Valor predictivo negativo | Proporción de negativos que están sanos |
| Punto de corte | Valor a partir del cual una prueba cuantitativa se considera positiva |
| Curva ROC | Gráfico de sensibilidad frente a 1 − especificidad para todos los puntos de corte |
| AUC | Área bajo la curva ROC; capacidad global de discriminación |
| Índice de Youden | Se + Sp − 1 |
| STARD | Guía para comunicar estudios de exactitud diagnóstica |
""")

c.titulo(2, "Para saber más")
c.md("""
- Altman DG, Bland JM. Diagnostic tests 1: sensitivity and specificity. *BMJ*. 1994;308(6943):1552. doi:[10.1136/bmj.308.6943.1552](https://doi.org/10.1136/bmj.308.6943.1552)
- Altman DG, Bland JM. Diagnostic tests 2: predictive values. *BMJ*. 1994;309(6947):102. doi:[10.1136/bmj.309.6947.102](https://doi.org/10.1136/bmj.309.6947.102)
- Altman DG, Bland JM. Diagnostic tests 3: receiver operating characteristic plots. *BMJ*. 1994;309(6948):188. doi:[10.1136/bmj.309.6948.188](https://doi.org/10.1136/bmj.309.6948.188)
- Bossuyt PM, *et al.* STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. *BMJ*. 2015;351:h5527. doi:[10.1136/bmj.h5527](https://doi.org/10.1136/bmj.h5527)
- SIMUSTAT Unidigital UMH. [Tema 280. Conceptos de probabilidad y su uso en la evaluación de pruebas diagnósticas](https://colab.research.google.com/drive/1Gp4XYiZjO1WChLRRTHugtbQziSoJOR7N). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(160)
print(c.guardar("../cuadernos"))
