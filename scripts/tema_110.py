from plantilla import Cuaderno

c = Cuaderno("Tema_110_Integracion_de_datos_clinicos_y_tablas_de_frecuencias.ipynb")

c.cabecera(
    110,
    "Integración de fuentes de datos clínicos y elaboración de tablas de frecuencias",
    "Módulo 3. Procesado inicial de datos",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Unir tablas de distintas fuentes por un identificador común y comprobar el resultado de la unión.
2. Elegir el tipo de unión adecuado (interna, por la izquierda o completa) según la pregunta clínica.
3. Resumir datos por grupos con `groupby`.
4. Construir tablas de frecuencias absolutas, relativas y acumuladas.
5. Agrupar una variable cuantitativa en categorías clínicas.
6. Construir e interpretar tablas de contingencia con porcentajes por filas o por columnas.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: unir y contar | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
El registro cardiovascular del Tema 100 está limpio. Ahora la coordinadora quiere saber qué proporción de pacientes con diabetes tiene **mal control glucémico** (HbA1c ≥ 8 %) en cada centro. También quiere saber si los centros rurales difieren de los urbanos.

El problema es que la información está repartida en tres sitios:

- La **cohorte**, con los datos clínicos de cada paciente.
- Las **analíticas**, que envía el laboratorio, con la HbA1c, la creatinina y el LDL. No todos los pacientes tienen analítica, y el laboratorio ha enviado dos resultados de pacientes que no están en la cohorte.
- La tabla de **centros**, con el tipo de centro (urbano o rural) y su población.

Hay que **integrar** las tres fuentes sin perder ni duplicar pacientes, y después **contar**. Las tablas de frecuencias son el primer resultado de cualquier estudio clínico: la «Tabla 1» de los artículos.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Unir tablas")
c.md("""
Dos tablas se unen por una **clave**: una columna que identifica a cada paciente en ambas, como el código `id`. Con `pd.merge()` se elige qué filas conservar:

| Tipo (`how=`) | Conserva | Cuándo usarlo |
| --- | --- | --- |
| `"inner"` | Solo los pacientes presentes en las **dos** tablas | Análisis que necesita datos de ambas fuentes |
| `"left"` | **Todos** los de la tabla izquierda; los que faltan en la derecha quedan con `NaN` | Conservar la cohorte completa |
| `"outer"` | Todos los de **cualquiera** de las dos | Revisar discrepancias entre fuentes |

**Después de cada unión, comprueba el número de filas.** Si la clave está repetida en una de las tablas, la unión multiplica filas sin avisar.
""")
c.titulo(3, "2.2 Frecuencias")
c.diagrama('Barras de frecuencia absoluta y relativa de las categorías de IMC de la cohorte, con la frecuencia acumulada en una línea.', nombre="e2_2")
c.md("""
| Frecuencia | Definición | Ejemplo con 400 pacientes |
| --- | --- | --- |
| Absoluta (*n*) | Número de casos en cada categoría | 74 diabéticos |
| Relativa (*f*) | Proporción: *n* / total | 74 / 400 = 0,185 |
| Porcentual | Relativa × 100 | 18,5 % |
| Acumulada | Suma de las anteriores en variables **ordinales** | Pacientes con IMC hasta «sobrepeso» |

Las frecuencias acumuladas solo tienen sentido si las categorías tienen un orden.
""")
c.titulo(3, "2.3 Tablas de contingencia")
c.md("""
Una **tabla de contingencia** cruza dos variables categóricas. Los porcentajes se pueden calcular sobre el total de cada **fila** o de cada **columna**, y responden a preguntas distintas:

- Porcentaje **por filas** (fila = tabaco): «De los fumadores, ¿qué porcentaje tuvo un evento?»
- Porcentaje **por columnas** (columna = evento): «De los que tuvieron un evento, ¿qué porcentaje fumaba?»

Confundirlos es uno de los errores más frecuentes al leer artículos.
""")

c.titulo(2, "3. Demostración: unir y contar (20 min)")
c.titulo(3, "3.1 Cargar las tres fuentes")
c.code("""
import pandas as pd

DATOS = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/"
cohorte = pd.read_csv(DATOS + "cohorte_limpia.csv")
analiticas = pd.read_csv(DATOS + "analiticas.csv")
centros = pd.read_csv(DATOS + "centros.csv")

print("Cohorte:", cohorte.shape, "· Analíticas:", analiticas.shape, "· Centros:", centros.shape)
analiticas.head()
""")

c.titulo(3, "3.2 Comprobar las claves antes de unir")
c.diagrama('Diagrama de Venn de los id: sin analítica, en las dos tablas y fuera de cohorte.')
c.code("""
print("¿id único en la cohorte?", cohorte["id"].is_unique)
print("¿id único en analíticas?", analiticas["id"].is_unique)

sin_analitica = set(cohorte["id"]) - set(analiticas["id"])
fuera_de_cohorte = set(analiticas["id"]) - set(cohorte["id"])
print("Pacientes de la cohorte sin analítica:", len(sin_analitica))
print("Analíticas de pacientes que no están en la cohorte:", sorted(fuera_de_cohorte))
""")
c.md("""
Los conjuntos de Python (Tema 20) permiten restar listas de identificadores para encontrar las discrepancias.
""")

c.titulo(3, "3.3 Tres tipos de unión")
c.code("""
for tipo in ["inner", "left", "outer"]:
    unida = pd.merge(cohorte, analiticas, on="id", how=tipo)
    print(f"{tipo:>5}: {len(unida)} filas")
""")
c.md("""
- `inner` conserva solo los 360 pacientes que están en ambas tablas.
- `left` conserva los 400 de la cohorte; los 40 sin analítica tendrán `NaN` en HbA1c.
- `outer` añade además las 2 analíticas huérfanas: útil para avisar al laboratorio, no para el análisis.

Para el estudio queremos la cohorte completa, así que usamos `left`. El parámetro `indicator=True` añade una columna que dice de dónde viene cada fila. `validate="one_to_one"` detiene la unión si la clave está repetida.
""")
c.code("""
datos = pd.merge(cohorte, analiticas, on="id", how="left", indicator=True, validate="one_to_one")
print(datos["_merge"].value_counts())
datos = datos.drop(columns="_merge")

datos = pd.merge(datos, centros, on="centro", how="left", validate="many_to_one")
print("Filas finales:", len(datos))
datos[["id", "centro", "tipo", "diabetes", "hba1c_pct"]].head()
""")

c.titulo(3, "3.4 Resumir por grupos")
c.code("""
datos.groupby("centro").agg(
    pacientes=("id", "count"),
    edad_media=("edad", "mean"),
    pas_media=("pas_mmHg", "mean"),
    eventos=("evento_cv_5a", "sum"),
).round(1)
""")

c.titulo(3, "3.5 Tabla de frecuencias de una variable")
c.code("""
n = datos["diabetes"].value_counts()
f = datos["diabetes"].value_counts(normalize=True)

pd.DataFrame({"n": n, "%": (f * 100).round(1)})
""")

c.titulo(3, "3.6 De cuantitativa a categórica: la HbA1c")
c.md("""
`pd.cut()` agrupa una variable cuantitativa en intervalos. Con `right=False`, cada intervalo incluye su límite inferior y excluye el superior: [7, 8) significa «7 o más y menos de 8».
""")
c.code("""
diabeticos = datos[datos["diabetes"] == "Sí"].copy()

diabeticos["control"] = pd.cut(
    diabeticos["hba1c_pct"],
    bins=[0, 7, 8, 20],
    labels=["< 7 %", "7 a 7,9 %", "≥ 8 %"],
    right=False,
)

tabla = diabeticos["control"].value_counts().sort_index().to_frame("n")
tabla["%"] = (tabla["n"] / tabla["n"].sum() * 100).round(1)
tabla["% acumulado"] = tabla["%"].cumsum().round(1)
tabla
""")
c.md("""
Los porcentajes se calculan sobre los diabéticos **con HbA1c disponible**. Siempre hay que indicar el denominador:
""")
c.code("""
print("Diabéticos:", len(diabeticos), "· con HbA1c:", diabeticos["hba1c_pct"].notna().sum())
""")

c.titulo(3, "3.7 Tabla de contingencia")
c.code("""
pd.crosstab(datos["fumador"], datos["evento_cv_5a"], margins=True, margins_name="Total")
""")
c.md("""
Porcentajes **por filas**: de los fumadores y de los no fumadores, qué porcentaje tuvo un evento cardiovascular en cinco años.
""")
c.code("""
(pd.crosstab(datos["fumador"], datos["evento_cv_5a"], normalize="index") * 100).round(1)
""")
c.md("""
Porcentajes **por columnas**: de los que tuvieron un evento y de los que no, qué porcentaje fumaba.
""")
c.code("""
(pd.crosstab(datos["fumador"], datos["evento_cv_5a"], normalize="columns") * 100).round(1)
""")
c.md("""
Las dos tablas son correctas, pero responden a preguntas distintas. Para estudiar si el tabaco se asocia a más eventos, la pregunta natural es la primera. Compara el **riesgo** de evento entre fumadores y no fumadores. En el Tema 230 la cuantificaremos con el riesgo relativo.
""")

c.titulo(3, "3.8 La pregunta del caso")
c.code("""
diabeticos["mal_control"] = diabeticos["hba1c_pct"] >= 8

resumen = diabeticos.dropna(subset=["hba1c_pct"]).groupby("tipo")["mal_control"].agg(["sum", "count", "mean"])
resumen.columns = ["mal control (n)", "diabéticos con HbA1c (n)", "proporción"]
resumen["proporción"] = (resumen["proporción"] * 100).round(1).astype(str) + " %"
resumen
""")

c.titulo(3, "Ampliación: unir filas de varios centros")
c.md("""
Si cada centro enviara su propio fichero con las mismas columnas, se apilarían con `pd.concat()`:
""")
c.code("""
norte = cohorte[cohorte["centro"] == "CS Norte"]
sur = cohorte[cohorte["centro"] == "CS Sur"]
apilado = pd.concat([norte, sur], ignore_index=True)
print(len(norte), "+", len(sur), "=", len(apilado))
""")

c.titulo(3, "Ampliación: formato ancho y formato largo")
c.md("""
Las mediciones repetidas pueden guardarse en **formato ancho** (una columna por visita) o en **formato largo** (una fila por paciente y visita). Muchos análisis y gráficos necesitan el formato largo; `melt()` y `pivot()` convierten entre ambos.
""")
c.code("""
ancho = pd.DataFrame({"id": ["CV-0001", "CV-0002"], "pas_basal": [148, 136], "pas_6m": [138, 131], "pas_12m": [132, 128]})
largo = ancho.melt(id_vars="id", var_name="visita", value_name="pas_mmHg")
print(largo)
print(largo.pivot(index="id", columns="visita", values="pas_mmHg"))
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**No comprobar el número de filas tras una unión.** Una clave repetida multiplica las filas; una clave mal escrita las pierde.

**Usar `inner` sin darse cuenta:** es el valor por defecto de `merge()`. Elimina sin aviso a los pacientes sin datos en la segunda tabla.

**Claves con formatos distintos:** `"CV-0001"` y `"cv-0001"`, o el número 1 y el texto `"0001"`, no coinciden.

**No indicar el denominador** de un porcentaje.

**Confundir porcentajes por filas y por columnas.**

**Calcular frecuencias acumuladas en variables nominales**, que no tienen orden.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 110 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** predecir el número de filas que dará cada tipo de unión entre dos tablas pequeñas.
2. **Misión clínica (con pistas):** unir la cohorte con las analíticas y construir la tabla de frecuencias del filtrado glomerular por categorías.
3. **Misión reto (con asistente):** construir con el asistente la «Tabla 1» de la cohorte por sexo. Verificar tres de sus cifras a mano.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("Una cohorte tiene 400 pacientes y la tabla de analíticas, 360 de ellos más 2 que no están en la cohorte. ¿Cuántas filas da merge(cohorte, analiticas, on=\"id\", how=\"left\")?", [
        ("400", True, "Correcto: se conservan todos los de la cohorte; los 40 sin analítica quedan con NaN."),
        ("360", False, "Eso daría how=\"inner\"."),
        ("402", False, "Eso daría how=\"outer\"."),
        ("362", False, "Esas son las filas de la tabla de analíticas."),
    ]),
    ("Tras unir dos tablas, el resultado tiene más filas que ambas. ¿Cuál es la causa más probable?", [
        ("La clave está repetida en alguna de las tablas", True, "Correcto: cada repetición multiplica filas. validate=\"one_to_one\" lo detecta."),
        ("Se ha usado how=\"left\"", False, "left nunca da más filas que la tabla izquierda si la clave es única."),
        ("Hay valores perdidos", False, "Los NaN no multiplican filas."),
        ("La unión ha fallado", False, "La unión ha funcionado, pero con una clave no única."),
    ]),
    ("En una tabla de contingencia de tabaco (filas) por evento (columnas), ¿qué porcentaje responde a «de los fumadores, cuántos tuvieron un evento»?", [
        ("El porcentaje por filas", True, "Correcto: el denominador es el total de cada fila, es decir, de fumadores."),
        ("El porcentaje por columnas", False, "Ese responde a «de los que tuvieron un evento, cuántos fumaban»."),
        ("El porcentaje sobre el total de la tabla", False, "Ese da la proporción de fumadores con evento entre todos los pacientes."),
        ("Ninguno: hace falta una prueba estadística", False, "La proporción se lee directamente de la tabla."),
    ]),
    ("¿En qué variable tiene sentido calcular frecuencias acumuladas?", [
        ("Categoría de control glucémico (< 7 %, 7 a 7,9 %, ≥ 8 %)", True, "Correcto: es ordinal, sus categorías tienen orden."),
        ("Centro de salud", False, "Es nominal: no tiene orden."),
        ("Grupo sanguíneo", False, "Es nominal: no tiene orden."),
        ("Sexo", False, "Es nominal y dicotómica."),
    ]),
    ("pd.cut(hba1c, bins=[0, 7, 8, 20], right=False). ¿En qué intervalo queda una HbA1c de 7,0 %?", [
        ("[7, 8)", True, "Correcto: con right=False, cada intervalo incluye su límite inferior."),
        ("[0, 7)", False, "7 no pertenece a [0, 7), que excluye el 7."),
        ("[8, 20)", False, "7 es menor que 8."),
        ("En ninguno", False, "Los intervalos cubren de 0 a 20."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Las tablas se unen por una clave; se comprueba su unicidad antes y el número de filas después.
- El tipo de unión depende de la pregunta: `left` para conservar toda la cohorte.
- `groupby` resume por grupos; `value_counts` y `crosstab` construyen tablas de frecuencias y de contingencia.
- Todo porcentaje necesita su denominador; por filas y por columnas responden a preguntas distintas.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Clave | Columna que identifica de forma única a cada unidad en una tabla |
| Unión (*merge*) | Combinación de dos tablas por una clave común |
| Frecuencia absoluta | Número de casos en una categoría |
| Frecuencia relativa | Proporción de casos en una categoría |
| Frecuencia acumulada | Suma de las frecuencias hasta una categoría, en variables ordinales |
| Tabla de contingencia | Tabla que cruza dos variables categóricas |
| Denominador | Total sobre el que se calcula una proporción |
| HbA1c | Hemoglobina glicosilada; refleja el control glucémico de los últimos meses |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Pandas: unir, combinar y concatenar](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Pandas: agrupar datos con groupby](https://pandas.pydata.org/docs/user_guide/groupby.html)
- American Diabetes Association. Standards of Care in Diabetes. *Diabetes Care* (edición anual): objetivos de HbA1c. Edición 2026 disponible en: [Diabetes Care, suplemento 1](https://diabetesjournals.org/care/issue/49/Supplement_1).
""")

c.pie(110)
print(c.guardar("../cuadernos"))
