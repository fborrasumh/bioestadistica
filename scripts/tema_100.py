from plantilla import Cuaderno

c = Cuaderno("Tema_100_Pandas_valores_perdidos_y_atipicos_en_registros_clinicos.ipynb")

c.cabecera(
    100,
    "Estructuras de datos con Pandas: tratamiento de valores perdidos y atípicos en registros clínicos",
    "Módulo 3. Procesado inicial de datos",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Cargar un registro clínico en un **DataFrame** de Pandas y explorar su estructura.
2. Seleccionar columnas, filtrar filas y crear variables nuevas.
3. Detectar y corregir registros duplicados y categorías escritas de formas distintas.
4. Cuantificar los **valores perdidos** y decidir cómo tratarlos sin sesgar el análisis.
5. Distinguir un **error de registro** de un **valor atípico** real, con reglas de plausibilidad fisiológica y con el criterio del rango intercuartílico.
6. Documentar cada decisión de limpieza en un registro auditable.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: limpieza de un registro clínico | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Tres centros de salud han reunido un **registro de riesgo cardiovascular** con 400 pacientes seguidos durante cinco años (datos sintéticos). Antes de analizarlo, una enfermera de investigación calcula el peso medio y obtiene 78,1 kg. Parece razonable.

Pero al revisar los datos aparecen problemas. Un paciente pesa **680 kg** y otro **7,4 kg**. Hay cuatro tallas de «1,6 cm» y una presión diastólica mayor que la sistólica. Hay una glucemia de **1.120 mg/dL** y el sexo aparece como «Mujer» y como «mujer». Faltan 18 pesos y hay dos pacientes registrados dos veces.

Ninguno de estos problemas impide calcular una media: Python la calcula sin protestar. Por eso son peligrosos. La preparación de los datos ocupa la mayor parte del tiempo de cualquier análisis. Y es la parte que más condiciona sus conclusiones.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Pandas y el DataFrame")
c.md("""
**Pandas** es la biblioteca de Python para trabajar con datos en forma de tabla. Su estructura central es el **DataFrame**: una tabla. Cada **fila** es una unidad de observación (un paciente) y cada **columna** es una variable. Cada columna individual es una **Series**.

| Instrucción | Qué hace |
| --- | --- |
| `pd.read_csv(ruta)` | Carga un CSV en un DataFrame |
| `df.head()` | Muestra las primeras filas |
| `df.shape` | Número de filas y columnas |
| `df.dtypes` / `df.info()` | Tipo de cada columna y valores no nulos |
| `df.describe()` | Resumen numérico de cada columna |
| `df["col"]` | Selecciona una columna |
| `df[df["edad"] >= 65]` | Filtra filas que cumplen una condición |
| `df["col"].value_counts()` | Frecuencias de cada valor |
""")
c.titulo(3, "2.2 Valores perdidos")
c.diagrama('Árbol: dato ausente según su mecanismo (completamente al azar, al azar condicionado, no al azar) y la consecuencia de cada uno.')
c.md("""
Pandas representa los datos ausentes como `NaN` (*not a number*). Antes de decidir qué hacer con ellos hay que preguntarse **por qué faltan**:

| Mecanismo | Significado | Ejemplo clínico | Consecuencia |
| --- | --- | --- | --- |
| Completamente al azar | La ausencia no depende de nada | Se perdió un tubo de la muestra | Eliminar los casos no sesga, solo reduce la muestra |
| Al azar condicionado | Depende de otras variables registradas | A los más jóvenes se les pide menos colesterol | Hay que tener en cuenta esas variables |
| No al azar | Depende del propio valor ausente | Los pacientes más obesos evitan pesarse | Cualquier tratamiento simple sesga el resultado |

**Rellenar con cero nunca es correcto** para una variable clínica. Rellenar con la media (imputación simple) mantiene el tamaño de la muestra, pero reduce artificialmente la variabilidad.
""")
c.titulo(3, "2.3 Errores de registro y valores atípicos")
c.md("""
| | Error de registro | Valor atípico real |
| --- | --- | --- |
| Qué es | Un valor **imposible** o incompatible | Un valor **extremo pero posible** |
| Ejemplo | Peso de 680 kg, PAD mayor que PAS | Colesterol total de 340 mg/dL |
| Cómo se detecta | Rangos de plausibilidad fisiológica y reglas de coherencia | Criterios estadísticos, como el rango intercuartílico |
| Qué hacer | Corregir si la causa es evidente; si no, marcar como perdido | **Conservar**: es información clínica |

El **rango intercuartílico** (RIC) es la distancia entre el percentil 25 (Q1) y el 75 (Q3). El criterio de Tukey considera atípicos los valores por debajo de Q1 − 1,5 × RIC o por encima de Q3 + 1,5 × RIC. Lo estudiaremos con detalle en el Tema 120.

**Toda decisión de limpieza se documenta.** Un análisis que no explica qué datos cambió no es reproducible.
""")

c.titulo(2, "3. Demostración: limpieza de un registro clínico (20 min)")
c.titulo(3, "3.1 Cargar y explorar")
c.code("""
import pandas as pd
import numpy as np

URL = "https://raw.githubusercontent.com/fborrasumh/bioestadistica/main/datos/cohorte_cardiovascular.csv"
cohorte = pd.read_csv(URL)

print("Filas y columnas:", cohorte.shape)
cohorte.head()
""")
c.code("""
cohorte.info()
""")
c.md("""
Observa en `info()` que algunas columnas tienen menos valores no nulos que filas: son los **valores perdidos**.
""")
c.code("""
cohorte.describe().round(1)
""")
c.md("""
`describe()` ya muestra los problemas: un peso máximo de 680 kg y una talla mínima de 1,6 cm. También una PAD máxima de 163 mmHg y una glucemia máxima de 1.120 mg/dL.
""")

c.titulo(3, "3.2 Seleccionar, filtrar y crear variables")
c.code("""
# Una columna
print(cohorte["edad"].head(3))

# Varias columnas
print(cohorte[["id", "edad", "pas_mmHg"]].head(3))

# Filtrar: pacientes de 75 años o más del CS Centro
mayores = cohorte[(cohorte["edad"] >= 75) & (cohorte["centro"] == "CS Centro")]
print("Pacientes de 75 años o más en CS Centro:", len(mayores))
""")
c.md("""
Al combinar condiciones en Pandas se usan `&` (y), `|` (o) y `~` (no), con **cada condición entre paréntesis**.
""")

c.titulo(3, "3.3 Registro de limpieza")
c.md("""
Antes de cambiar nada, creamos una lista donde anotar cada decisión.
""")
c.code("""
registro_limpieza = []

def anotar(problema, decision, filas_afectadas):
    registro_limpieza.append({"problema": problema, "decisión": decision, "filas": filas_afectadas})
""")

c.titulo(3, "3.4 Duplicados")
c.code("""
duplicados = cohorte.duplicated().sum()
print("Filas duplicadas:", duplicados)

cohorte = cohorte.drop_duplicates()
anotar("Filas duplicadas", "Eliminadas", int(duplicados))
print("Pacientes únicos:", len(cohorte), "·", cohorte["id"].is_unique)
""")

c.titulo(3, "3.5 Categorías escritas de formas distintas")
c.code("""
print(cohorte["sexo"].value_counts())
print(cohorte["fumador"].value_counts(dropna=False))
""")
c.code("""
cambiados = (~cohorte["sexo"].isin(["Mujer", "Hombre"])).sum()
cohorte["sexo"] = cohorte["sexo"].str.strip().str.lower().map(
    {"mujer": "Mujer", "m": "Mujer", "hombre": "Hombre", "h": "Hombre"}
)
anotar("Sexo con distintas grafías", "Unificado a Mujer/Hombre", int(cambiados))

cambiados = (cohorte["fumador"].notna() & ~cohorte["fumador"].isin(["Sí", "No"])).sum()
cohorte["fumador"] = cohorte["fumador"].str.lower().map({"sí": "Sí", "si": "Sí", "no": "No"})
anotar("Fumador con distintas grafías", "Unificado a Sí/No", int(cambiados))

print(cohorte["sexo"].value_counts(), cohorte["fumador"].value_counts(dropna=False), sep="\\n\\n")
""")
c.md("""
`.map()` sustituye cada valor según un diccionario. Un valor que no esté en el diccionario se convertiría en `NaN`; por eso conviene comprobar con `value_counts()` antes y después.
""")

c.titulo(3, "3.6 Valores perdidos")
c.code("""
perdidos = pd.DataFrame({
    "n_perdidos": cohorte.isna().sum(),
    "porcentaje": (cohorte.isna().mean() * 100).round(1),
})
perdidos[perdidos["n_perdidos"] > 0]
""")
c.md("""
Veamos cómo cambia el peso medio según la decisión que tomemos. Primero corregiremos los errores de peso (apartado 3.7); aquí solo mostramos el efecto de **rellenar con cero**:
""")
c.code("""
peso = cohorte["peso_kg"]
print(f"Media ignorando los perdidos: {peso.mean():.1f} kg (n = {peso.notna().sum()})")
print(f"Media rellenando con cero:    {peso.fillna(0).mean():.1f} kg (n = {len(peso)})  ← sesgada")
""")
c.md("""
Pandas **ignora los `NaN`** por defecto al calcular medias y otros estadísticos. Es lo correcto si los datos faltan al azar; en otro caso, hay que estudiar el patrón de ausencias. Lo que nunca se hace es sustituirlos por cero.
""")

c.titulo(3, "3.7 Errores de registro: reglas de plausibilidad")
c.md("""
Definimos rangos fisiológicamente plausibles para un adulto y revisamos los valores que quedan fuera.
""")
c.code("""
rangos = {
    "peso_kg": (30, 250),
    "talla_cm": (120, 220),
    "pas_mmHg": (70, 260),
    "pad_mmHg": (30, 150),
    "glucemia_mg_dl": (40, 600),
}

for variable, (minimo, maximo) in rangos.items():
    fuera = cohorte[(cohorte[variable] < minimo) | (cohorte[variable] > maximo)]
    print(f"{variable}: {len(fuera)} valores fuera de [{minimo}, {maximo}]")
    if len(fuera) > 0:
        print("   ", fuera[variable].tolist())
""")
c.md("""
Cada error requiere una decisión razonada:

- **Tallas entre 1 y 2:** se registraron en metros. La corrección es evidente: multiplicar por 100.
- **Pesos de 680 y 7,4 kg:** probablemente una coma desplazada (68,0 y 74), pero no podemos estar seguros. Los marcamos como perdidos.
- **Glucemia de 1.120 mg/dL:** probablemente un cero de más, pero sin certeza. La marcamos como perdida.
""")
c.code("""
en_metros = cohorte["talla_cm"] < 3
cohorte.loc[en_metros, "talla_cm"] = cohorte.loc[en_metros, "talla_cm"] * 100
anotar("Talla registrada en metros", "Multiplicada por 100", int(en_metros.sum()))

imposible = (cohorte["peso_kg"] < 30) | (cohorte["peso_kg"] > 250)
cohorte.loc[imposible, "peso_kg"] = np.nan
anotar("Peso fisiológicamente imposible", "Marcado como perdido", int(imposible.sum()))

imposible = cohorte["glucemia_mg_dl"] > 600
cohorte.loc[imposible, "glucemia_mg_dl"] = np.nan
anotar("Glucemia > 600 mg/dL", "Marcada como perdida", int(imposible.sum()))
""")
c.md("""
**Regla de coherencia:** la presión diastólica no puede ser mayor que la sistólica. Si lo es, lo más probable es que se hayan intercambiado.
""")
c.code("""
invertidas = cohorte["pad_mmHg"] >= cohorte["pas_mmHg"]
print(cohorte.loc[invertidas, ["id", "pas_mmHg", "pad_mmHg"]])

cohorte.loc[invertidas, ["pas_mmHg", "pad_mmHg"]] = cohorte.loc[invertidas, ["pad_mmHg", "pas_mmHg"]].values
anotar("PAD mayor que PAS", "Valores intercambiados", int(invertidas.sum()))
""")
c.md("""
`.loc[filas, columnas]` selecciona y modifica a la vez filas y columnas concretas. Es la forma segura de cambiar valores en un DataFrame.
""")

c.titulo(3, "3.8 Valores atípicos reales: el criterio del RIC")
c.code("""
q1, q3 = cohorte["colesterol_mg_dl"].quantile([0.25, 0.75])
ric = q3 - q1
limite_inferior, limite_superior = q1 - 1.5 * ric, q3 + 1.5 * ric

atipicos = cohorte[(cohorte["colesterol_mg_dl"] < limite_inferior) | (cohorte["colesterol_mg_dl"] > limite_superior)]
print(f"Límites de Tukey: {limite_inferior:.0f} a {limite_superior:.0f} mg/dL")
print("Valores atípicos:", sorted(atipicos["colesterol_mg_dl"].tolist()))
""")
c.md("""
Un colesterol total de 84 mg/dL es inusual, pero **posible**. Es un valor atípico estadístico, no un error, y se **conserva**: eliminarlos ocultaría precisamente a los pacientes de mayor interés clínico.
""")

c.titulo(3, "3.9 Variables derivadas y resultado final")
c.code("""
cohorte["imc"] = (cohorte["peso_kg"] / (cohorte["talla_cm"] / 100) ** 2).round(1)
cohorte.describe().round(1)
""")
c.code("""
pd.DataFrame(registro_limpieza)
""")
c.code("""
cohorte.to_csv("cohorte_limpia.csv", index=False)
print("Guardado cohorte_limpia.csv con", len(cohorte), "pacientes")
""")

c.titulo(3, "Ampliación: auditar una limpieza hecha por IA")
c.md("""
Si pides al asistente «limpia este conjunto de datos», probablemente propondrá eliminar filas. Por ejemplo, todas las filas con valores perdidos (`dropna()`) o los atípicos según algún criterio. Antes de aceptarlo:

1. Pide que **explique cada paso** y la razón clínica o estadística.
2. Comprueba **cuántas filas** se pierden: `dropna()` sobre toda la tabla puede eliminar un tercio de los pacientes.
3. Comprueba que no se eliminan **valores atípicos reales**.
4. Compara cinco valores antes y después, a mano.
5. Exige un **registro de limpieza** como el del apartado 3.3.
""")
c.code("""
original = pd.read_csv(URL)
print("Pacientes originales:", len(original))
print("Pacientes tras dropna() sobre toda la tabla:", len(original.dropna()))
""")

c.titulo(3, "Ampliación: imputación por la media")
c.code("""
hdl = cohorte["hdl_mg_dl"]
hdl_imputado = hdl.fillna(hdl.mean())
print(f"Desviación típica original:  {hdl.std():.2f} mg/dL")
print(f"Desviación típica imputada:  {hdl_imputado.std():.2f} mg/dL  ← subestimada")
""")
c.md("""
Rellenar con la media no cambia la media, pero **reduce la variabilidad**. Entonces los intervalos de confianza y las pruebas estadísticas parecen más precisos de lo que son. Existen métodos mejores, como la imputación múltiple, que quedan fuera de este curso.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Rellenar con cero** los valores perdidos de una variable clínica.

**Eliminar todos los valores atípicos** sin distinguir errores de valores extremos reales.

**Usar `and`/`or` en lugar de `&`/`|`** al filtrar con Pandas: produce `ValueError`.

**Olvidar los paréntesis** en las condiciones combinadas: `cohorte["edad"] >= 65 & cohorte["diabetes"] == "Sí"` no hace lo que parece.

**Modificar una copia en lugar del original:** para cambiar valores, usar siempre `.loc[filas, columna]`.

**No documentar** los cambios: el análisis deja de ser reproducible.
""")

c.titulo(3, "Ampliación: Fechas clínicas con pandas")
c.md("""
Las fechas suelen llegar como **texto** ("03/02/2026"). Con texto no se pueden restar fechas ni agrupar por mes. `pd.to_datetime()` las convierte en fechas reales.

Indica siempre el formato (`format="%d/%m/%Y"`). Si no, pandas puede leer el 03/02 como 2 de marzo. Con `errors="coerce"`, una fecha imposible pasa a ser un valor perdido (`NaT`) y no detiene el análisis.

**En tus materiales SIMUSTAT:** [Tema 70. Módulos math, random, time e instalación de módulos externos](https://colab.research.google.com/drive/1s8vuaHhH94JDhDjfMf2DbsdpK7d29usU), apartado 4. **En tus materiales SIMUSTAT:** [Tema 170. Gestión de datos con Pandas y tratamiento de valores anómalos](https://colab.research.google.com/drive/1f_m55KKTYuHCMu2ZrnnoDyw5lCkCgXhd), apartado 4 (series temporales).
""")
c.code("""
ingresos = pd.DataFrame({
    "id": ["H1", "H2", "H3", "H4"],
    "ingreso": ["03/02/2026", "15/02/2026", "28/02/2026", "02/03/2026"],
    "alta": ["10/02/2026", "16/02/2026", "31/02/2026", "09/03/2026"],   # 31/02 no existe
})
for col in ["ingreso", "alta"]:
    ingresos[col] = pd.to_datetime(ingresos[col], format="%d/%m/%Y", errors="coerce")

ingresos["estancia_dias"] = (ingresos["alta"] - ingresos["ingreso"]).dt.days
ingresos["mes_ingreso"] = ingresos["ingreso"].dt.month
print(ingresos)
print("\\nFechas no válidas:", ingresos["alta"].isna().sum())
print("Estancia media:", ingresos["estancia_dias"].mean().round(1), "días")
""")
c.md("""
La fecha de alta de H3 no existe; queda como `NaT` y su estancia como valor perdido. Igual que con cualquier valor perdido, **regístralo y revísalo en la fuente**: no lo rellenes.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 100 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** clasificar valores como error de registro, valor atípico real o dato plausible.
2. **Misión clínica (con pistas):** limpiar un registro sintético de pacientes con EPOC y presentar su registro de limpieza.
3. **Misión reto (con asistente):** pedir al asistente que limpie el registro. Auditar su propuesta con los cinco pasos de la ampliación y corregir lo que no sea aceptable.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("En un registro, un paciente pesa 680 kg. ¿Qué es lo más adecuado?", [
        ("Marcarlo como perdido y anotarlo en el registro de limpieza", True, "Correcto: es imposible y no sabemos con certeza el valor real."),
        ("Conservarlo, porque es un valor atípico", False, "No es un valor extremo posible: es un error de registro."),
        ("Sustituirlo por 68 kg", False, "Es probable, pero no seguro; corregir sin certeza introduce un dato inventado."),
        ("Eliminar al paciente del estudio", False, "Se perderían todos sus demás datos, que son válidos."),
    ]),
    ("Un paciente tiene un colesterol total de 340 mg/dL, por encima del límite de Tukey. ¿Qué haces?", [
        ("Conservarlo: es un valor extremo pero clínicamente posible", True, "Correcto: es un valor atípico real con interés clínico."),
        ("Eliminarlo porque es un valor atípico", False, "Eliminarlo ocultaría a los pacientes de mayor riesgo."),
        ("Sustituirlo por la mediana", False, "Se perdería información real."),
        ("Marcarlo como perdido", False, "No es un error de registro."),
    ]),
    ("¿Qué expresión selecciona a los pacientes de 65 años o más que son fumadores?", [
        ("cohorte[(cohorte[\"edad\"] >= 65) & (cohorte[\"fumador\"] == \"Sí\")]", True, "Correcto: & y cada condición entre paréntesis."),
        ("cohorte[cohorte[\"edad\"] >= 65 and cohorte[\"fumador\"] == \"Sí\"]", False, "En Pandas se usa & en lugar de and."),
        ("cohorte[(cohorte[\"edad\"] >= 65) | (cohorte[\"fumador\"] == \"Sí\")]", False, "| selecciona a quienes cumplen al menos una condición."),
        ("cohorte[\"edad\" >= 65 & \"fumador\" == \"Sí\"]", False, "Hay que comparar las columnas, no sus nombres."),
    ]),
    ("Faltan 18 pesos de 400. ¿Qué efecto tiene rellenarlos con 0 antes de calcular el peso medio?", [
        ("Infraestima el peso medio", True, "Correcto: se introducen 18 pesos falsos de 0 kg."),
        ("Ninguno, porque Pandas ignora los ceros", False, "Pandas ignora los NaN, no los ceros."),
        ("Sobreestima el peso medio", False, "Los ceros arrastran la media hacia abajo."),
        ("Aumenta la precisión del resultado", False, "Introduce un sesgo."),
    ]),
    ("¿Por qué no conviene eliminar todas las filas con algún valor perdido (dropna sobre toda la tabla)?", [
        ("Porque se pierden muchos pacientes con datos válidos en otras variables", True, "Correcto: en el ejemplo se pierde casi una cuarta parte de la cohorte."),
        ("Porque dropna produce un error con datos clínicos", False, "dropna funciona; el problema es lo que elimina."),
        ("Porque dropna convierte los NaN en ceros", False, "dropna elimina filas, no las rellena."),
        ("Porque Pandas no permite eliminar filas", False, "Sí lo permite."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Un DataFrame es una tabla: una fila por paciente, una columna por variable.
- `info()`, `describe()` y `value_counts()` son la primera revisión obligatoria de cualquier conjunto de datos.
- Los valores perdidos se cuantifican y se tratan según por qué faltan; nunca se rellenan con cero.
- Un error de registro se corrige o se marca como perdido; un valor atípico real se conserva.
- Cada decisión de limpieza se anota en un registro.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| DataFrame | Tabla de datos de Pandas, con filas y columnas |
| Series | Columna de un DataFrame |
| `NaN` | Valor perdido en Pandas |
| Imputación | Sustitución de un valor perdido por un valor estimado |
| Error de registro | Valor imposible o incoherente, debido a un fallo al registrar el dato |
| Valor atípico | Valor extremo, alejado del resto, pero posible |
| Rango intercuartílico | Diferencia entre los percentiles 75 y 25 |
| Registro de limpieza | Documento que recoge cada cambio realizado en los datos y su motivo |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Guía de inicio de Pandas](https://pandas.pydata.org/docs/getting_started/index.html)
- [Pandas: trabajar con datos perdidos](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- Sterne JAC, *et al.* Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. *BMJ*. 2009;338:b2393.
- SIMUSTAT Unidigital UMH. [Tema 70. Módulos math, random, time e instalación de módulos externos](https://colab.research.google.com/drive/1s8vuaHhH94JDhDjfMf2DbsdpK7d29usU). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
- SIMUSTAT Unidigital UMH. [Tema 170. Gestión de datos con Pandas y tratamiento de valores anómalos](https://colab.research.google.com/drive/1f_m55KKTYuHCMu2ZrnnoDyw5lCkCgXhd). Cuaderno de Google Colab. Elche: Universidad Miguel Hernández; 2023.
""")

c.pie(100)
print(c.guardar("../cuadernos"))
