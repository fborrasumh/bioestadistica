from plantilla import Cuaderno

c = Cuaderno("Tema_300_Lectura_critica_de_la_evidencia_y_evaluacion_de_la_mejora_recursiva.ipynb")

c.cabecera(
    300,
    "Lectura crítica de la evidencia científica y evaluación de la mejora recursiva",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Leer críticamente el resumen de un estudio clínico con una lista de preguntas sistemática.
2. Identificar el diseño, la pregunta PICO y los principales sesgos (selección, información y confusión).
3. Relacionar cada diseño con su guía de publicación (CONSORT, STROBE, STARD, TRIPOD+AI, PRISMA).
4. Usar un modelo de lenguaje como ayuda en la lectura crítica **verificando** todo lo que afirma.
5. Evaluar con métodos estadísticos si un ciclo de **mejora recursiva** (de un modelo de IA o de tu propio aprendizaje) mejora de verdad.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: leer un resumen y evaluar una mejora | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un paciente llega a la consulta con este titular en el móvil: «Un estudio demuestra que tomar café reduce un 30 % la mortalidad». Lee también el resumen del artículo:

> *Estudio de cohortes prospectivo con 52.000 adultos seguidos 10 años. Los que tomaban 3 o más cafés al día tuvieron una mortalidad menor que los que no tomaban café (HR ajustado 0,70; IC 95 %: 0,62 a 0,79). Los resultados se ajustaron por edad, sexo y tabaco.*

Con lo aprendido en el curso, puedes responder con criterio. Es un **estudio observacional**: no demuestra causalidad. Se ha ajustado por algunos confusores, pero pueden quedar otros; quien toma café puede tener más salud, más ingresos u otros hábitos. El 30 % es una reducción **relativa**; falta el riesgo absoluto. Y el IC indica un efecto preciso, pero precisión no es validez.

Esta última sesión reúne todo el curso. Lee la evidencia con criterio. Aplica ese mismo criterio a la mejora de los modelos de IA **y a tu propio aprendizaje**, con los informes de la app.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 La pregunta PICO y el diseño")
c.diagrama('Decisión: si el investigador asigna la exposición al azar, ensayo aleatorizado; si no, estudio observacional, como el del café.')
c.md("""
| Elemento | Pregunta | En el caso del café |
| --- | --- | --- |
| **P**oblación | ¿En quién? | 52.000 adultos |
| **I**ntervención o exposición | ¿Qué? | 3 o más cafés al día |
| **C**omparación | ¿Frente a qué? | No tomar café |
| **O** (resultado, *outcome*) | ¿Qué se mide? | Mortalidad a 10 años |

| Diseño | ¿Asigna el investigador la exposición? | Puede demostrar causalidad | Guía de publicación |
| --- | --- | --- | --- |
| Ensayo clínico aleatorizado | Sí, al azar | Sí, si está bien hecho | CONSORT |
| Cohortes, casos y controles, transversal | No | Con mucha cautela | STROBE |
| Estudio de pruebas diagnósticas | — | — | STARD |
| Modelo predictivo (también de IA) | — | No pretende | TRIPOD+AI |
| Revisión sistemática y metanálisis | — | Según los estudios incluidos | PRISMA |

Las guías de publicación sirven también para **leer**: cada apartado es una pregunta que el artículo debería responder.
""")
c.titulo(3, "2.2 Los tres grandes sesgos")
c.md("""
| Sesgo | Qué es | Ejemplo |
| --- | --- | --- |
| **Selección** | Los participantes no representan a la población, o los grupos se forman de manera distinta | Voluntarios más sanos; pérdidas de seguimiento desiguales |
| **Información** (medida) | Las variables se miden con error, o de forma distinta según el grupo | Recuerdo del consumo de café; resultado evaluado sin cegamiento |
| **Confusión** | Una tercera variable explica la asociación (Tema 270) | Nivel socioeconómico; confusión por indicación |

El azar se controla con el tamaño muestral y se cuantifica con el IC y el valor p. **Los sesgos no**: un estudio enorme y sesgado da una respuesta precisa y equivocada.
""")
c.titulo(3, "2.3 Diez preguntas para leer un resumen")
c.diagrama('Las diez preguntas de lectura crítica agrupadas en cuatro bloques: pregunta y diseño, resultados, sesgos y aplicación.', nombre="e2_3")
c.md("""
1. ¿Cuál es la pregunta PICO?
2. ¿Qué diseño es? ¿Permite conclusiones causales?
3. ¿Cuál es la variable principal? ¿Estaba registrada antes del estudio?
4. ¿Cuántos participantes y cuántos eventos hay?
5. ¿Se da el efecto con su IC, y en medidas absolutas (RAR, NNT) además de relativas?
6. ¿Es clínicamente relevante el efecto, además de estadísticamente significativo?
7. ¿Qué sesgos de selección, información o confusión son plausibles?
8. ¿Hay muchas comparaciones o análisis de subgrupos no previstos?
9. ¿A qué pacientes se pueden aplicar los resultados (validez externa)?
10. ¿Concuerdan las conclusiones con los resultados, o los exageran?
""")
c.titulo(3, "2.4 Evaluar la mejora recursiva")
c.md("""
En el Tema 090 vimos la **mejora recursiva**: generar, evaluar, corregir y volver a evaluar. La pregunta estadística es la misma tanto si mejora un modelo de IA como si mejora un estudiante: **¿la versión nueva acierta más que la anterior en las mismas tareas, más allá del azar?**

| Situación | Datos | Análisis |
| --- | --- | --- |
| Dos versiones de un *prompt* o de un modelo con los mismos casos | Acierto/fallo apareado | McNemar (Tema 240) |
| Tu acierto en el primer intento y tras la pista del asistente | Acierto/fallo apareado por misión | McNemar |
| Evolución de tu nota de una unidad a otra | Proporciones a lo largo del tiempo | IC de cada proporción, tendencia |

Y recuerda la advertencia de Goodhart. Si se mejora una y otra vez frente a **los mismos** casos de prueba, la mejora medida en ellos es optimista. La mejora real solo se mide con **pruebas reservadas** que no se han usado para decidir.
""")

c.titulo(2, "3. Demostración: leer un resumen y evaluar una mejora (20 min)")
c.titulo(3, "3.1 Del riesgo relativo al absoluto")
c.md("""
Supongamos que la mortalidad a 10 años en los que no toman café es del 8 %. Si el efecto fuera causal (gran «si»), ¿qué significaría un HR de 0,70?
""")
c.code("""
import numpy as np
import pandas as pd
from scipy import stats

riesgo_basal = 0.08
for hr in [0.70, 0.62, 0.79]:
    riesgo_cafe = 1 - (1 - riesgo_basal) ** hr   # aproximación con riesgos proporcionales
    rar = riesgo_basal - riesgo_cafe
    print(f"HR {hr:.2f}: mortalidad {riesgo_cafe:.1%} frente a {riesgo_basal:.0%} · RAR {rar:.1%} · «NNT» {1 / rar:.0f} a 10 años")
""")
c.md("""
Aun aceptando la causalidad, harían falta unas 40 personas tomando café 10 años para evitar una muerte. Y como es un estudio observacional, ese número no es un NNT: no se ha demostrado que cambiar el hábito cambie el riesgo.
""")

c.titulo(3, "3.2 Un modelo de lenguaje como ayudante de lectura crítica")
c.conexion_ia()
c.code("""
resumen = \"\"\"Estudio de cohortes prospectivo con 52.000 adultos seguidos 10 años. Los que tomaban 3 o más
cafés al día tuvieron una mortalidad menor que los que no tomaban café (HR ajustado 0,70; IC 95 %:
0,62 a 0,79). Los resultados se ajustaron por edad, sexo y tabaco. Conclusión: el café reduce la mortalidad.\"\"\"

prompt = f\"\"\"Eres un epidemiólogo. Analiza críticamente este resumen respondiendo, en una línea cada una,
a estas preguntas: 1) PICO; 2) diseño y si permite causalidad; 3) principales confusores no ajustados;
4) qué medida absoluta falta; 5) si la conclusión está justificada. No inventes datos que no estén en el resumen.

Resumen: {resumen}\"\"\"

respuesta = preguntar(prompt)
if respuesta is None:
    respuesta = \"\"\"1) P: 52.000 adultos; I: ≥ 3 cafés/día; C: no tomar café; O: mortalidad a 10 años.
2) Cohortes prospectivo, observacional: no permite afirmar causalidad.
3) Nivel socioeconómico, actividad física, dieta, alcohol, enfermedades previas (causalidad inversa).
4) Falta la mortalidad absoluta en cada grupo, la diferencia de riesgos y el número de muertes.
5) No: «reduce» es un lenguaje causal que el diseño no respalda; debería decir «se asoció con».
(Respuesta de ejemplo: configura tu clave para obtener la del modelo.)\"\"\"
print(respuesta)
""")
c.md("""
**Verifica cada punto** con las diez preguntas del apartado 2.3. Los modelos de lenguaje son útiles para no olvidar ninguna pregunta, pero pueden:

- **Inventar** datos o referencias que no están en el texto («según el estudio, el seguimiento fue del 95 %»).
- Dar por buena una conclusión si el *prompt* la presenta como cierta.
- Fallar en los cálculos (comprueba siempre con código, como en 3.1).

Y nunca se les deben dar datos de pacientes.
""")

c.titulo(3, "3.3 ¿Mejora la versión nueva del prompt? McNemar con pruebas reservadas")
c.md("""
Un equipo mejora un *prompt* que clasifica informes de radiografía de tórax como «neumonía sí/no». Prueban la versión 1 y la versión 2 con **los mismos 150 informes reservados**, nunca usados durante el desarrollo.
""")
c.code("""
from statsmodels.stats.contingency_tables import mcnemar

#               v2 acierta   v2 falla
tabla = np.array([[112,         5],      # v1 acierta
                  [17,          16]])    # v1 falla
n = tabla.sum()
print(f"Exactitud v1: {tabla[0].sum() / n:.1%} · v2: {tabla[:, 0].sum() / n:.1%}")
print(f"Discordantes: solo v2 acierta {tabla[1, 0]} · solo v1 acierta {tabla[0, 1]}")
print(f"McNemar exacta: p = {mcnemar(tabla, exact=True).pvalue:.3f}")
""")

c.md("""
La versión 2 acierta 8 puntos más, y entre los 22 informes en que discrepan, acierta en 17. Como los 150 informes estaban reservados, esta mejora sí es una estimación honesta.
""")

c.titulo(3, "3.4 Goodhart: mejorar contra la misma prueba")
c.md("""
Ahora simulamos un error frecuente. El equipo prueba 30 variantes de *prompt* que en realidad son **todas igual de buenas** (exactitud real del 80 %). Las evalúa con los mismos 40 casos y se queda con la mejor.
""")
c.code("""
rng = np.random.default_rng(seed=300)
exactitud_real = 0.80
casos_desarrollo, casos_reservados, variantes = 40, 400, 30

mejor_en_desarrollo, misma_en_reservados = [], []
for _ in range(2000):
    resultados = rng.binomial(casos_desarrollo, exactitud_real, size=variantes) / casos_desarrollo
    mejor_en_desarrollo.append(resultados.max())
    misma_en_reservados.append(rng.binomial(casos_reservados, exactitud_real) / casos_reservados)

print(f"Exactitud real de todas las variantes: {exactitud_real:.0%}")
print(f"Exactitud de la «mejor» en los 40 casos de desarrollo: {np.mean(mejor_en_desarrollo):.1%} de media")
print(f"Exactitud de esa misma variante en 400 casos reservados: {np.mean(misma_en_reservados):.1%}")
""")
c.md("""
Si se elige la mejor de 30 variantes con los mismos casos, aparece una «mejora» de unos 12 puntos que no existe. Es la selección del máximo del azar, la misma lógica de las comparaciones múltiples (Tema 260). La mejora recursiva necesita **dos** conjuntos de casos: uno para mejorar y otro, reservado, para medir.
""")

c.titulo(3, "3.5 Tu propia mejora recursiva: los informes de la app")
c.md("""
Cada informe de la app Bioestadística registra dos datos por misión. Si la resolviste en el **primer intento** y si la resolviste **tras la pista** del asistente. Con los informes de las 30 unidades se puede analizar tu aprendizaje igual que el de un modelo. Aquí, con datos simulados de un estudiante; en la misión reto lo harás con los tuyos.
""")
c.code("""
unidades = np.repeat(np.arange(10, 310, 10), 3)
mision = np.tile(["básica", "clínica", "reto"], 30)
dificultad = np.tile([0.5, 0.0, -0.7], 30)
progreso = (unidades - 150) / 150 * 0.8   # el estudiante mejora a lo largo del curso

p_primero = 1 / (1 + np.exp(-(0.6 + dificultad + progreso)))
primero = rng.random(90) < p_primero
tras_pista = primero | (rng.random(90) < 0.6)

informes = pd.DataFrame({"unidad": unidades, "mision": mision, "primer_intento": primero, "tras_pista": tras_pista})
informes.head(6)
""")
c.code("""
tabla_pista = pd.crosstab(informes["primer_intento"], informes["tras_pista"]).reindex(
    index=[True, False], columns=[True, False], fill_value=0)
print(tabla_pista, "\\n")
print(f"Acierto en el primer intento: {informes['primer_intento'].mean():.0%} · tras la pista: {informes['tras_pista'].mean():.0%}")
print(f"McNemar exacta: p = {mcnemar(tabla_pista.to_numpy(), exact=True).pvalue:.1e}")
""")
c.md("""
La pista ayuda: es lo esperable. La pregunta más interesante para tu aprendizaje es otra: ¿**dependes menos** de la pista a medida que avanza el curso?
""")
c.code("""
from statsmodels.stats.proportion import proportion_confint
import matplotlib.pyplot as plt

informes["modulo"] = pd.cut(informes["unidad"], [0, 40, 80, 130, 190, 300],
                            labels=["M1 Python", "M2 IA", "M3 Datos", "M4 Probabilidad", "M5 Inferencia"])
resumen = informes.groupby("modulo", observed=True)["primer_intento"].agg(["sum", "count"])
resumen["proporcion"] = resumen["sum"] / resumen["count"]
ic = [proportion_confint(s, n_, method="wilson") for s, n_ in zip(resumen["sum"], resumen["count"])]
resumen["li"], resumen["ls"] = zip(*ic)

plt.figure(figsize=(8, 4))
plt.errorbar(range(len(resumen)), resumen["proporcion"],
             yerr=[resumen["proporcion"] - resumen["li"], resumen["ls"] - resumen["proporcion"]],
             marker="o", capsize=4)
plt.xticks(range(len(resumen)), resumen.index)
plt.ylim(0, 1)
plt.ylabel("Acierto en el primer intento (IC 95 %)")
plt.title("Evolución del aprendizaje autónomo a lo largo del curso")
plt.show()
resumen.round(2)
""")
c.code("""
import statsmodels.formula.api as smf

informes["acierto"] = informes["primer_intento"].astype(int)
tendencia = smf.logit("acierto ~ unidad + C(mision)", data=informes).fit(disp=0)
b = tendencia.params["unidad"]
li, ls = tendencia.conf_int().loc["unidad"]
print(f"OR de acertar al primer intento por cada 100 temas de avance: {np.exp(100 * b):.2f} "
      f"(IC 95 %: {np.exp(100 * li):.2f} a {np.exp(100 * ls):.2f}), ajustada por el tipo de misión")
""")
c.md("""
Un modelo logístico (Tema 280) ajustado por la dificultad de la misión estima una tendencia: si resuelves más misiones sin ayuda a lo largo del curso. Con solo 90 misiones el IC es ancho: un estudiante es una muestra pequeña. Agregando los informes de toda la clase, el profesor puede ver qué unidades necesitan mejorarse: la asignatura también está sometida a mejora recursiva.
""")

c.titulo(3, "Ampliación: la pirámide no lo es todo")
c.md("""
Las revisiones sistemáticas de ensayos están en lo alto de la jerarquía de la evidencia, pero:

- Un metanálisis de ensayos sesgados es un resultado sesgado más preciso.
- Para muchas preguntas (efectos adversos raros, pronóstico, factores de riesgo que no se pueden asignar) los estudios observacionales son la mejor evidencia disponible.
- Los sistemas como **GRADE** valoran la certeza de la evidencia por más criterios que el diseño. Son el riesgo de sesgo, la imprecisión, la inconsistencia, la evidencia indirecta y el sesgo de publicación.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Leer solo las conclusiones del resumen.**

**Confundir precisión (IC estrecho) con validez (ausencia de sesgo).**

**Aceptar lenguaje causal en estudios observacionales.**

**Fiarse de las referencias o los datos que aporta un modelo de lenguaje** sin comprobarlos en la fuente.

**Medir la mejora de un sistema con los mismos casos usados para mejorarlo.**

**Juzgar tu progreso por una sola unidad:** usa todas las misiones y su IC.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 300 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** aplicar las diez preguntas de lectura crítica a tres resúmenes (un ensayo, una cohorte y un modelo de IA).
2. **Misión clínica (con pistas):** reescribir con medidas absolutas y lenguaje no causal la nota de prensa de un estudio observacional.
3. **Misión reto (con asistente):** cargar tus informes de las 30 unidades y comparar con McNemar tu acierto en el primer intento y tras la pista. Estimar tu tendencia a lo largo del curso y escribir un párrafo de autoevaluación.

Al terminar, exporta el **informe final** y súbelo junto con los anteriores: forman la evaluación continua (EC) de la asignatura.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("Un estudio de cohortes con 200.000 personas encuentra una asociación muy precisa (IC estrecho) entre un alimento y menor mortalidad. ¿Qué puede concluirse?", [
        ("Que la asociación probablemente no se debe al azar, pero puede deberse a sesgos o confusión", True, "Correcto: el tamaño controla el azar, no los sesgos."),
        ("Que el alimento reduce la mortalidad", False, "Un estudio observacional no demuestra causalidad."),
        ("Que el resultado es más fiable que el de un ensayo aleatorizado pequeño", False, "Precisión no es validez."),
        ("Nada, porque es observacional", False, "Aporta evidencia, con sus limitaciones."),
    ]),
    ("¿Qué guía de publicación usarías para valorar un artículo sobre un sistema de IA que predice la sepsis?", [
        ("TRIPOD+AI", True, "Correcto: es la guía para modelos predictivos, incluidos los de IA."),
        ("CONSORT", False, "CONSORT es para ensayos aleatorizados."),
        ("PRISMA", False, "PRISMA es para revisiones sistemáticas."),
        ("STARD", False, "STARD es para estudios de pruebas diagnósticas."),
    ]),
    ("Un modelo de lenguaje resume un artículo y cita «una tasa de seguimiento del 96 %» que no aparece en el texto. ¿Qué ha ocurrido?", [
        ("Ha inventado un dato (alucinación); hay que verificar todo en la fuente", True, "Correcto."),
        ("Ha encontrado el dato en otro sitio, así que es fiable", False, "No se puede saber sin comprobarlo."),
        ("Es un error de redondeo", False, "El dato no estaba en el texto."),
        ("Es normal y se puede usar", False, "Un dato no verificado no se usa."),
    ]),
    ("Dos versiones de un prompt se evalúan con los mismos 200 casos reservados. ¿Qué prueba compara su exactitud?", [
        ("McNemar", True, "Correcto: son datos apareados."),
        ("Prueba z de dos proporciones independientes", False, "Los casos son los mismos."),
        ("t de Student", False, "La variable es binaria."),
        ("Kappa de Cohen", False, "Kappa mide concordancia, no compara exactitud."),
    ]),
    ("Se prueban 25 variantes de un prompt con los mismos 30 casos y se elige la que más acierta. ¿Qué pasará al evaluarla con casos nuevos?", [
        ("Probablemente acertará menos que en los 30 casos de desarrollo", True, "Correcto: elegir el máximo con los mismos casos sobrestima el rendimiento (Goodhart)."),
        ("Acertará lo mismo", False, "Su ventaja era en parte azar."),
        ("Acertará más", False, "El rendimiento con los datos de selección es optimista."),
        ("No se puede evaluar", False, "Sí: con casos reservados."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Lee cada estudio con la pregunta PICO, el diseño, los sesgos y el efecto en medidas absolutas con su IC.
- El tamaño muestral controla el azar, no los sesgos: precisión no es validez.
- Las guías de publicación (CONSORT, STROBE, STARD, TRIPOD+AI, PRISMA) son también listas de lectura crítica.
- Un modelo de lenguaje ayuda a leer, pero todo lo que afirma se verifica.
- La mejora recursiva se mide con datos apareados y con pruebas reservadas; tu aprendizaje también.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Lectura crítica | Evaluación sistemática de la validez, los resultados y la aplicabilidad de un estudio |
| Pregunta PICO | Formulación de una pregunta clínica en población, intervención, comparación y resultado |
| Sesgo de selección | Error por la forma en que se eligen o se pierden los participantes |
| Sesgo de información | Error en la medida de la exposición o del resultado |
| Validez interna | Ausencia de sesgos en el estudio |
| Validez externa | Aplicabilidad de los resultados a otras poblaciones |
| CONSORT, STROBE, STARD, PRISMA | Guías de publicación de ensayos, estudios observacionales, pruebas diagnósticas y revisiones sistemáticas |
| GRADE | Sistema para valorar la certeza de la evidencia y la fuerza de las recomendaciones |
| Alucinación | Información falsa generada por un modelo de lenguaje con apariencia de verdadera |
| Mejora recursiva | Ciclo de generar, evaluar, corregir y volver a evaluar |
| Pruebas reservadas | Casos que no se usan para mejorar un sistema y sirven solo para medir su rendimiento |
""")

c.titulo(2, "Para saber más")
c.md("""
- Greenhalgh T. *How to Read a Paper: The Basics of Evidence-Based Healthcare*. 6.ª ed. Hoboken: Wiley-Blackwell; 2019.
- Red EQUATOR (*Enhancing the QUAlity and Transparency Of health Research*): guías de publicación en [equator-network.org](https://www.equator-network.org).
- Guyatt GH, *et al.* GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336(7650):924-926. doi:[10.1136/bmj.39489.470347.AD](https://doi.org/10.1136/bmj.39489.470347.AD)
- Ioannidis JPA. Why most published research findings are false. *PLoS Med*. 2005;2(8):e124. doi:[10.1371/journal.pmed.0020124](https://doi.org/10.1371/journal.pmed.0020124)
""")

c.pie(300)
print(c.guardar("../cuadernos"))
