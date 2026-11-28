from plantilla import Cuaderno

c = Cuaderno("Tema_240_Datos_apareados_y_concordancia_McNemar_y_kappa_de_Cohen.ipynb")

c.cabecera(
    240,
    "Análisis de datos apareados y de concordancia: prueba de McNemar e índice kappa de Cohen",
    "Módulo 5. Generalización de conclusiones",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Evaluación:** el examen del Módulo 5 se hace **con Colab**. Practica ejecutando e interpretando cada análisis.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Reconocer cuándo dos proporciones proceden de datos **apareados** (los mismos pacientes, las mismas preguntas o pares emparejados).
2. Aplicar e interpretar la **prueba de McNemar** para comparar dos proporciones apareadas.
3. Distinguir **asociación**, **acuerdo** y **concordancia más allá del azar**.
4. Calcular e interpretar el **índice kappa de Cohen** y su versión ponderada para escalas ordinales.
5. Reconocer las limitaciones de kappa cuando la prevalencia es extrema.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: McNemar y kappa | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
El servicio de Urgencias evalúa un asistente de IA que propone el nivel de triaje a partir del motivo de consulta y las constantes. Se plantean dos preguntas:

1. **¿Es mejor el modelo nuevo que el anterior?** Los dos se prueban con **los mismos 200 casos** clínicos, de los que se conoce el triaje correcto establecido por un panel de expertos. El nuevo acierta el 81 % y el anterior el 74 %.
2. **¿Coincide el asistente con la enfermera de triaje?** En 150 pacientes reales, los dos asignan un nivel de prioridad. Coinciden en el 78 % de los casos.

La primera pregunta no se responde con la prueba *z* de dos proporciones independientes (Tema 220). **Los casos son los mismos**: hay que usar la prueba de McNemar. La segunda no es una comparación, sino una medida de **concordancia**. Un 78 % de coincidencia puede ser menos de lo que parece si gran parte se debe al azar. Para eso existe el índice kappa.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Datos apareados")
c.diagrama('Dos gráficos de puntos: grupos independientes frente a datos apareados, donde una línea une a cada paciente consigo mismo.', nombre="e2_1")
c.md("""
Los datos son apareados cuando cada observación de un grupo tiene una pareja natural en el otro:

- El mismo paciente **antes y después** de una intervención.
- Dos pruebas diagnósticas aplicadas a los **mismos** pacientes.
- Dos modelos de IA evaluados con las **mismas** preguntas.
- Casos y controles **emparejados** por edad y sexo.

Analizarlos como independientes desperdicia información y da resultados incorrectos.
""")
c.titulo(3, "2.2 La prueba de McNemar")
c.diagrama('Tabla de pares: a y d no informan; McNemar usa solo b y c.')
c.md("""
Con dos resultados binarios apareados, la tabla se construye con los **pares**:

| | Modelo B acierta | Modelo B falla |
| --- | --- | --- |
| **Modelo A acierta** | *a* (ambos aciertan) | ***b*** (solo A acierta) |
| **Modelo A falla** | ***c*** (solo B acierta) | *d* (ambos fallan) |

Los pares concordantes (*a* y *d*) no dicen nada sobre cuál es mejor. La prueba solo usa los **pares discordantes** *b* y *c*. Si $H_0$ es cierta (las dos proporciones son iguales), *b* y *c* deberían ser parecidos:

$$\\chi^2_{McNemar} = \\frac{(b - c)^2}{b + c}$$

Con pocos pares discordantes (*b* + *c* < 25), usa la versión **exacta**. Es una prueba binomial de *b* frente a *b* + *c* con *p* = 0,5.
""")
c.titulo(3, "2.3 Acuerdo y concordancia: el índice kappa")
c.md("""
Dos observadores pueden coincidir por azar. Si los dos clasifican al 90 % de los pacientes como «no urgente», coincidirán muy a menudo aunque elijan al azar. El **índice kappa de Cohen** corrige el acuerdo observado por el esperado por azar:

$$\\kappa = \\frac{P_o - P_e}{1 - P_e}$$

donde $P_o$ es la proporción de acuerdo observado y $P_e$ la esperada por azar, calculada con las frecuencias marginales de cada observador.

| κ | Grado de concordancia (Landis y Koch) |
| --- | --- |
| < 0 | Peor que el azar |
| 0,00 a 0,20 | Insignificante |
| 0,21 a 0,40 | Discreta |
| 0,41 a 0,60 | Moderada |
| 0,61 a 0,80 | Sustancial |
| 0,81 a 1,00 | Casi perfecta |

Para escalas **ordinales**, como los cinco niveles de triaje, usa la **kappa ponderada**. Penaliza menos un desacuerdo de un nivel que uno de cuatro.
""")
c.titulo(3, "2.4 Asociación no es concordancia")
c.md("""
Supón que la enfermera asigna siempre un nivel más grave que el asistente. Las dos clasificaciones estarán perfectamente **asociadas** (la ji cuadrado será muy significativa). Pero **no coincidirán nunca**. La ji cuadrado mide asociación; kappa mide concordancia.
""")

c.titulo(2, "3. Demostración: McNemar y kappa (20 min)")
c.titulo(3, "3.1 Dos modelos con los mismos 200 casos")
c.code("""
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(seed=240)
n = 200
# Resultado de cada caso (True = acierto). Pares: 140 aciertan ambos, 22 solo el nuevo,
# 8 solo el anterior y 30 fallan ambos
nuevo = np.array([True] * 140 + [True] * 22 + [False] * 8 + [False] * 30)
anterior = np.array([True] * 140 + [False] * 22 + [True] * 8 + [False] * 30)

etiqueta = {True: "Sí", False: "No"}
tabla = pd.crosstab(pd.Series(nuevo, name="Nuevo acierta").map(etiqueta),
                    pd.Series(anterior, name="Anterior acierta").map(etiqueta))
tabla = tabla.loc[["Sí", "No"], ["Sí", "No"]]
print(tabla, "\\n")
print(f"Exactitud: nuevo {nuevo.mean():.1%} · anterior {anterior.mean():.1%}")
""")
c.code("""
from statsmodels.stats.contingency_tables import mcnemar

b = tabla.loc["Sí", "No"]   # solo acierta el nuevo
c_ = tabla.loc["No", "Sí"]  # solo acierta el anterior
print(f"Pares discordantes: solo el nuevo acierta {b} · solo el anterior acierta {c_}")

exacta = mcnemar(tabla.to_numpy(), exact=True)
asintotica = mcnemar(tabla.to_numpy(), exact=False, correction=True)
print(f"McNemar exacta: p = {exacta.pvalue:.4f}")
print(f"McNemar ji cuadrado (con corrección de continuidad): χ² = {asintotica.statistic:.2f}, p = {asintotica.pvalue:.4f}")
""")

c.titulo(3, "3.2 El error de ignorar el apareamiento")
c.code("""
from statsmodels.stats.proportion import proportions_ztest

z, p_indep = proportions_ztest([nuevo.sum(), anterior.sum()], [n, n])
print(f"Prueba z como si fueran independientes: p = {p_indep:.4f}")
print(f"Prueba de McNemar (correcta):           p = {exacta.pvalue:.4f}")
""")
c.md("""
Si se tratan los datos como independientes, el valor p sale mucho mayor. La prueba *z* trata como «ruido» la variabilidad entre casos fáciles y difíciles. En el diseño apareado esa variabilidad se anula, porque **cada caso se compara consigo mismo**. El diseño apareado es más potente, siempre que se analice como tal.

**Cómo se comunica:** «El modelo nuevo acertó en el 81 % de los casos y el anterior en el 74 % (*n* = 200 casos comunes). De los 30 casos en que discreparon, el nuevo acertó en 22 y el anterior en 8 (McNemar exacta, *p* = 0,016)».
""")

c.titulo(3, "3.3 Acuerdo entre la enfermera y el asistente")
c.md("""
Simulamos 150 pacientes con dos clasificaciones: «urgente» o «no urgente».
""")
c.code("""
from sklearn.metrics import cohen_kappa_score

urgente_real = rng.random(150) < 0.25
enfermera = np.where(rng.random(150) < 0.88, urgente_real, ~urgente_real)
asistente = np.where(rng.random(150) < 0.86, urgente_real, ~urgente_real)

tabla_acuerdo = pd.crosstab(pd.Series(enfermera, name="Enfermera: urgente"),
                            pd.Series(asistente, name="Asistente: urgente"))
print(tabla_acuerdo, "\\n")

po = (enfermera == asistente).mean()
pe = enfermera.mean() * asistente.mean() + (1 - enfermera.mean()) * (1 - asistente.mean())
kappa_manual = (po - pe) / (1 - pe)

print(f"Acuerdo observado Po = {po:.3f}")
print(f"Acuerdo esperado por azar Pe = {pe:.3f}")
print(f"Kappa a mano = {kappa_manual:.3f} · con scikit-learn = {cohen_kappa_score(enfermera, asistente):.3f}")
""")
c.md("""
Con las prevalencias de cada clasificador, el azar explicaría por sí solo un 59 % de coincidencias. El 78 % de acuerdo se convierte en κ = 0,47: concordancia solo **moderada**. En 33 de 150 pacientes, el asistente y la enfermera discrepan sobre si el caso es urgente.
""")

c.titulo(3, "3.4 Kappa con su intervalo de confianza")
c.code("""
from statsmodels.stats.inter_rater import cohens_kappa

resultado = cohens_kappa(tabla_acuerdo.to_numpy())
print(f"κ = {resultado.kappa:.3f} (IC 95 %: {resultado.kappa_low:.3f} a {resultado.kappa_upp:.3f})")
""")

c.titulo(3, "3.5 Kappa ponderada: los cinco niveles de triaje")
c.md("""
El Sistema Español de Triaje y el Manchester usan cinco niveles (1 = resucitación, 5 = no urgente). Un desacuerdo entre los niveles 2 y 3 es menos grave que uno entre 1 y 5.
""")
c.code("""
nivel_real = rng.choice([1, 2, 3, 4, 5], size=150, p=[0.03, 0.12, 0.35, 0.35, 0.15])

def clasificar(nivel, error):
    salto = rng.choice([-1, 0, 1], size=len(nivel), p=[error / 2, 1 - error, error / 2])
    return np.clip(nivel + salto, 1, 5)

enfermera_n = clasificar(nivel_real, 0.30)
asistente_n = clasificar(nivel_real, 0.35)

print(pd.crosstab(pd.Series(enfermera_n, name="Enfermera"), pd.Series(asistente_n, name="Asistente")), "\\n")
print(f"Acuerdo exacto: {(enfermera_n == asistente_n).mean():.1%}")
print(f"Kappa sin ponderar:          {cohen_kappa_score(enfermera_n, asistente_n):.3f}")
print(f"Kappa ponderada lineal:      {cohen_kappa_score(enfermera_n, asistente_n, weights='linear'):.3f}")
print(f"Kappa ponderada cuadrática:  {cohen_kappa_score(enfermera_n, asistente_n, weights='quadratic'):.3f}")
""")
c.md("""
Casi todos los desacuerdos son de un solo nivel, así que la kappa ponderada es mucho mayor que la simple. En escalas ordinales se debe dar la **ponderada** e indicar el tipo de ponderación.
""")

c.titulo(3, "Ampliación: la paradoja de kappa")
c.md("""
Con una prevalencia muy extrema, kappa puede ser baja aunque el acuerdo sea altísimo:
""")
c.code("""
# 200 radiografías; casi todas normales
paradoja = np.array([[2, 4],
                     [5, 189]])
acuerdo = np.trace(paradoja) / paradoja.sum()
print(f"Acuerdo observado: {acuerdo:.1%}")
print(f"κ = {cohens_kappa(paradoja).kappa:.3f}")
""")
c.md("""
Con un 95,5 % de acuerdo, kappa es solo discreta, porque casi todo el acuerdo se esperaba por azar al ser casi todas normales. Por eso conviene publicar la **tabla completa** y el acuerdo observado, además de kappa. Valora también el acuerdo por separado en positivos y en negativos.
""")

c.titulo(3, "Ampliación: McNemar antes y después")
c.md("""
En 120 hipertensos se registra si tienen la **presión arterial controlada** (sí/no) antes y 6 meses después de una intervención educativa de enfermería.
""")
c.code("""
#                    Después: controlado   Después: no controlado
antes_despues = np.array([[48, 6],      # Antes: controlado
                          [23, 43]])    # Antes: no controlado
r = mcnemar(antes_despues, exact=True)
print(f"Controlados antes: {antes_despues[0].sum() / 120:.1%} · después: {antes_despues[:, 0].sum() / 120:.1%}")
print(f"Mejoran: {antes_despues[1, 0]} · empeoran: {antes_despues[0, 1]} · McNemar exacta: p = {r.pvalue:.4f}")
""")
c.md("""
Ojo: sin grupo control, la mejora puede tener tres causas. La intervención, la **regresión a la media** (Tema 130) u otros cambios del período. McNemar dice que el cambio no es atribuible al azar, no que lo cause la intervención.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Comparar proporciones apareadas con la ji cuadrado o la *z* de independientes.**

**Medir la concordancia con el porcentaje de acuerdo o con la ji cuadrado.** Usa kappa.

**Usar kappa simple en escalas ordinales.** Usa la ponderada.

**Dar kappa sin la tabla**, cuando la prevalencia es extrema.

**Confundir concordancia con validez:** dos observadores pueden coincidir mucho y equivocarse los dos. La validez se mide frente a un patrón de referencia (Tema 160).
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 240 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** decidir si seis diseños producen datos apareados o independientes, y calcular a mano una kappa.
2. **Misión clínica (con pistas):** comparar con McNemar dos pruebas de cribado aplicadas a los mismos pacientes y medir su concordancia.
3. **Misión reto (con asistente):** usar los informes de las unidades anteriores. Comparar con McNemar tu acierto en el primer intento y tras la pista del asistente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente.")
c.quiz([
    ("Dos pruebas de cribado se aplican a los mismos 300 pacientes. ¿Cómo comparas su sensibilidad?", [
        ("Con la prueba de McNemar", True, "Correcto: son proporciones apareadas."),
        ("Con la prueba z de dos proporciones independientes", False, "Los pacientes son los mismos."),
        ("Con el índice kappa", False, "Kappa mide concordancia, no compara proporciones."),
        ("Con la prueba exacta de Fisher", False, "Fisher es para muestras independientes."),
    ]),
    ("En una tabla de McNemar, a = 60, b = 15, c = 5, d = 20. ¿Qué casillas usa la prueba?", [
        ("Solo b y c, los pares discordantes", True, "Correcto: χ² = (15 − 5)² / (15 + 5) = 5."),
        ("Solo a y d", False, "Los pares concordantes no informan sobre la diferencia."),
        ("Las cuatro", False, "La prueba solo usa los discordantes."),
        ("a y b", False, "Revisa qué pares indican diferencia entre las pruebas."),
    ]),
    ("Dos radiólogos coinciden en el 85 % de las radiografías; el acuerdo esperado por azar es del 70 %. ¿Cuánto vale kappa?", [
        ("0,50", True, "Correcto: (0,85 − 0,70) / (1 − 0,70) = 0,15 / 0,30 = 0,50."),
        ("0,85", False, "Ese es el acuerdo observado."),
        ("0,15", False, "Esa es la diferencia, sin dividir por 1 − Pe."),
        ("0,21", False, "Revisa la fórmula."),
    ]),
    ("Un médico clasifica siempre un nivel por encima de otro en una escala de 1 a 5. ¿Qué ocurre?", [
        ("Hay asociación perfecta pero concordancia nula", True, "Correcto: no coinciden nunca, aunque uno predice perfectamente al otro."),
        ("Kappa es 1", False, "Kappa sería 1 si coincidieran siempre."),
        ("La ji cuadrado no será significativa", False, "La asociación es perfecta."),
        ("Hay concordancia perfecta", False, "No coinciden en ningún caso."),
    ]),
    ("Para medir la concordancia entre dos observadores en una escala de gravedad de cinco niveles, ¿qué usas?", [
        ("Kappa ponderada", True, "Correcto: tiene en cuenta que los desacuerdos de un nivel son menos graves."),
        ("Kappa simple", False, "Trata igual un desacuerdo de un nivel que uno de cuatro."),
        ("Porcentaje de acuerdo", False, "No descuenta el azar."),
        ("Prueba de McNemar", False, "McNemar compara proporciones apareadas."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Mismos pacientes o mismas preguntas: datos apareados.
- McNemar compara dos proporciones apareadas usando solo los pares discordantes.
- El apareamiento aumenta la potencia, pero solo si se analiza como tal.
- Kappa mide la concordancia corregida por el azar; en escalas ordinales, kappa ponderada.
- Asociación no es concordancia, y concordancia no es validez.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Datos apareados | Observaciones en las que cada valor de un grupo tiene una pareja en el otro |
| Pares discordantes | Pares en los que los dos resultados difieren |
| Prueba de McNemar | Contraste de dos proporciones apareadas basado en los pares discordantes |
| Acuerdo observado ($P_o$) | Proporción de casos en que coinciden dos clasificaciones |
| Acuerdo esperado ($P_e$) | Proporción de coincidencias que se esperaría por azar |
| Índice kappa de Cohen | Medida de concordancia entre dos observadores corregida por el azar |
| Kappa ponderada | Versión de kappa que pondera los desacuerdos según su distancia en una escala ordinal |
| Paradoja de kappa | Valor bajo de kappa con acuerdo alto, cuando la prevalencia es extrema |
""")

c.titulo(2, "Para saber más")
c.md("""
- McNemar Q. Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika*. 1947;12(2):153-157. doi:[10.1007/BF02295996](https://doi.org/10.1007/BF02295996)
- Landis JR, Koch GG. The measurement of observer agreement for categorical data. *Biometrics*. 1977;33(1):159-174. doi:[10.2307/2529310](https://doi.org/10.2307/2529310)
- Feinstein AR, Cicchetti DV. High agreement but low kappa: I. The problems of two paradoxes. *J Clin Epidemiol*. 1990;43(6):543-549. doi:[10.1016/0895-4356(90)90158-L](https://doi.org/10.1016/0895-4356%2890%2990158-L)
""")

c.pie(240)
print(c.guardar("../cuadernos"))
