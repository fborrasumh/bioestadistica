from plantilla import Cuaderno

c = Cuaderno("Tema_070_Ficheros_y_formatos_de_datos_sanitarios_CSV_y_JSON.ipynb")

c.cabecera(
    70,
    "Gestión de ficheros y formatos de intercambio de datos sanitarios: CSV y JSON",
    "Módulo 2. Programando con IA",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Crear, leer y ampliar ficheros de texto desde Python.
2. Guardar y leer una tabla de pacientes en formato **CSV**.
3. Reconocer los problemas habituales de los CSV en español: separador, coma decimal y codificación.
4. Convertir datos de Python a **JSON** y viceversa, y extraer información de un JSON anidado.
5. Reconocer la estructura de un recurso del estándar sanitario **HL7 FHIR**.
6. Entender la respuesta de una API, que llega en formato JSON.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: ficheros, CSV y JSON | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un grupo de investigación de un hospital participa en un **registro multicéntrico** de insuficiencia cardiaca. Cada mes debe enviar los datos de sus pacientes (seudonimizados) en un fichero **CSV**. Al mismo tiempo, el laboratorio del hospital entrega los resultados analíticos al sistema de historia clínica en **JSON**, siguiendo el estándar internacional **HL7 FHIR**.

Una residente abre el CSV en una hoja de cálculo. Todas las columnas aparecen juntas en una sola. Los pesos han perdido los decimales. Las tildes se ven como símbolos extraños.

Los datos no se transmiten en el vacío: viajan en **formatos de fichero**. Conocerlos evita perder información por el camino. Además, son imprescindibles para el Tema 80, donde un modelo de IA responderá en JSON.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Ficheros de texto")
c.diagrama('Modos de open: "r" lee, "a" añade al final y "w" borra lo anterior. En Colab los ficheros se borran al cerrar la sesión.')
c.md("""
Un fichero se abre con `open(nombre, modo, encoding="utf-8")`:

| Modo | Significado | Cuidado |
| --- | --- | --- |
| `"r"` | Leer | Error si el fichero no existe |
| `"w"` | Escribir | **Borra** el contenido anterior |
| `"a"` | Añadir al final | Conserva lo que había |

Se usa siempre con `with`, que cierra el fichero automáticamente al terminar. La codificación **UTF-8** representa correctamente tildes, eñes y símbolos como «µ» o «°».

En Colab, los ficheros creados se guardan en una carpeta temporal visible en el panel **Archivos** y **se borran al cerrar la sesión**. Para conservarlos hay que descargarlos o guardarlos en Drive.
""")
c.titulo(3, "2.2 CSV")
c.md("""
**CSV** (*comma-separated values*) es una tabla en texto plano: una fila por línea y las columnas separadas por un carácter. Es el formato más usado para intercambiar datos tabulares.

```
codigo,edad,sexo,peso_kg,fevi_pct
IC-001,72,M,81.5,35
IC-002,68,F,64.0,
```

En España, muchas hojas de cálculo usan el **punto y coma** como separador y la **coma** como separador decimal. Por eso conviene saber siempre qué separador tiene un fichero antes de leerlo. Una celda vacía indica un **dato ausente**.
""")
c.titulo(3, "2.3 JSON")
c.md("""
**JSON** (*JavaScript Object Notation*) representa datos estructurados en texto. Su sintaxis es casi igual a la de los diccionarios y listas de Python. Admite datos **anidados**: diccionarios dentro de listas dentro de diccionarios.

| JSON | Python |
| --- | --- |
| objeto `{ }` | diccionario `dict` |
| array `[ ]` | lista `list` |
| `"texto"` | `str` |
| `12`, `12.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Es el formato de las **API** web y de los modelos de IA. También es el del estándar sanitario **HL7 FHIR**, que intercambia historias clínicas, resultados de laboratorio y prescripciones.
""")

c.titulo(2, "3. Demostración: ficheros, CSV y JSON (20 min)")
c.titulo(3, "3.1 Escribir y leer un fichero de texto")
c.code("""
informe = \"\"\"INFORME DE ALTA (paciente sintético IC-001)
Diagnóstico principal: insuficiencia cardiaca con fracción de eyección reducida.
Tratamiento al alta: sacubitrilo/valsartán, bisoprolol, dapagliflozina.
Revisión en consulta de Cardiología en 4 semanas.
\"\"\"

with open("informe_alta.txt", "w", encoding="utf-8") as fichero:
    fichero.write(informe)

with open("informe_alta.txt", "r", encoding="utf-8") as fichero:
    contenido = fichero.read()

print(contenido)
""")
c.md("""
Con el modo `"a"` se añade una línea sin borrar lo anterior. Leer con `.readlines()` devuelve una lista con una línea por elemento.
""")
c.code("""
with open("informe_alta.txt", "a", encoding="utf-8") as fichero:
    fichero.write("Alergias: no conocidas.\\n")

with open("informe_alta.txt", "r", encoding="utf-8") as fichero:
    lineas = fichero.readlines()

print("Número de líneas:", len(lineas))
print("Última línea:", lineas[-1].strip())
""")

c.titulo(3, "3.2 Buscar información en el texto")
c.code("""
texto = contenido.lower()
for farmaco in ["bisoprolol", "furosemida", "dapagliflozina"]:
    print(f"{farmaco}: {'sí' if farmaco in texto else 'no'} aparece en el informe")
""")

c.titulo(3, "3.3 Guardar una tabla en CSV")
c.md("""
El módulo `csv` escribe una lista de diccionarios como tabla. `DictWriter` usa las claves como nombres de columna.
""")
c.code("""
import csv

pacientes = [
    {"codigo": "IC-001", "edad": 72, "sexo": "M", "peso_kg": 81.5, "fevi_pct": 35},
    {"codigo": "IC-002", "edad": 68, "sexo": "F", "peso_kg": 64.0, "fevi_pct": None},
    {"codigo": "IC-003", "edad": 81, "sexo": "M", "peso_kg": 70.2, "fevi_pct": 28},
]

with open("registro_ic.csv", "w", encoding="utf-8", newline="") as fichero:
    escritor = csv.DictWriter(fichero, fieldnames=["codigo", "edad", "sexo", "peso_kg", "fevi_pct"])
    escritor.writeheader()
    escritor.writerows(pacientes)

print(open("registro_ic.csv", encoding="utf-8").read())
""")
c.md("""
Observa que el dato ausente de IC-002 queda como una celda vacía.
""")

c.titulo(3, "3.4 Leer un CSV")
c.md("""
`DictReader` lee cada fila como un diccionario. **Todo llega como texto**: hay que convertir los números y tratar las celdas vacías.
""")
c.code("""
with open("registro_ic.csv", encoding="utf-8") as fichero:
    lector = csv.DictReader(fichero)
    for fila in lector:
        edad = int(fila["edad"])
        fevi = float(fila["fevi_pct"]) if fila["fevi_pct"] != "" else None
        print(fila["codigo"], edad, "años · FEVI:", fevi)
""")

c.titulo(3, "3.5 El CSV «a la española»")
c.md("""
Este es el aspecto de un CSV exportado desde una hoja de cálculo configurada en español: punto y coma como separador y coma decimal.
""")
c.code("""
csv_espanol = \"\"\"codigo;edad;peso_kg
IC-004;77;68,4
IC-005;59;92,1
\"\"\"
with open("registro_es.csv", "w", encoding="utf-8") as fichero:
    fichero.write(csv_espanol)

with open("registro_es.csv", encoding="utf-8") as fichero:
    lector = csv.DictReader(fichero, delimiter=";")
    for fila in lector:
        peso = float(fila["peso_kg"].replace(",", "."))
        print(fila["codigo"], peso, "kg")
""")
c.md("""
Si se leyera con el separador por defecto (la coma), cada línea se partiría por la coma decimal y los datos quedarían desordenados. En el Tema 100, Pandas resolverá esto con dos parámetros: `sep=";"` y `decimal=","`.
""")

c.titulo(3, "3.6 JSON: de Python a texto y de vuelta")
c.code("""
import json

paciente = {"codigo": "IC-001", "edad": 72, "diabetes": True, "fevi_pct": None,
            "farmacos": ["bisoprolol", "dapagliflozina"]}

texto_json = json.dumps(paciente, ensure_ascii=False, indent=2)
print(texto_json)
""")
c.md("""
Observa la traducción: `True` pasa a `true` y `None` a `null`. Con `json.loads()` se recupera el diccionario.
""")
c.code("""
recuperado = json.loads(texto_json)
print(type(recuperado), recuperado["farmacos"][0])
""")
c.code("""
with open("paciente.json", "w", encoding="utf-8") as fichero:
    json.dump(paciente, fichero, ensure_ascii=False, indent=2)

with open("paciente.json", encoding="utf-8") as fichero:
    print(json.load(fichero)["edad"])
""")

c.titulo(3, "3.7 Un resultado de laboratorio en HL7 FHIR")
c.md("""
FHIR organiza la información clínica en **recursos** (Patient, Observation, MedicationRequest…). Este es un recurso *Observation* simplificado con una glucemia, codificada con el sistema internacional **LOINC**. Para llegar al valor hay que recorrer los niveles de anidamiento.
""")
c.code("""
observacion_fhir = \"\"\"
{
  "resourceType": "Observation",
  "status": "final",
  "code": {
    "coding": [{"system": "http://loinc.org", "code": "2339-0",
                "display": "Glucose [Mass/volume] in Blood"}]
  },
  "subject": {"reference": "Patient/IC-001"},
  "effectiveDateTime": "2027-10-04T08:15:00+02:00",
  "valueQuantity": {"value": 112, "unit": "mg/dL"}
}
\"\"\"

obs = json.loads(observacion_fhir)
codigo = obs["code"]["coding"][0]
print("Prueba:", codigo["display"], f"(LOINC {codigo['code']})")
print("Paciente:", obs["subject"]["reference"])
print("Resultado:", obs["valueQuantity"]["value"], obs["valueQuantity"]["unit"])
""")

c.titulo(3, "3.8 La respuesta de una API")
c.md("""
Cuando, en el Tema 80, enviemos una pregunta a un modelo de IA, la respuesta llegará como un JSON parecido a este (simplificado). Lo que interesa está en lo más profundo: el texto generado y el número de tokens consumidos, que determina el coste.
""")
c.code("""
respuesta_api = json.loads(\"\"\"
{
  "modelo": "modelo-ejemplo",
  "candidatos": [
    {"contenido": {"texto": "El IMC de 25,6 kg/m² corresponde a sobrepeso según la OMS."},
     "motivo_fin": "STOP"}
  ],
  "uso": {"tokens_entrada": 18, "tokens_salida": 16}
}
\"\"\")

print(respuesta_api["candidatos"][0]["contenido"]["texto"])
uso = respuesta_api["uso"]
print("Tokens totales:", uso["tokens_entrada"] + uso["tokens_salida"])
""")

c.titulo(3, "Ampliación: subir ficheros y usar Google Drive")
c.md("""
Para trabajar con un fichero de tu ordenador:

```python
from google.colab import files
subidos = files.upload()      # abre un diálogo para elegir el fichero
```

Para leer y guardar en tu Google Drive, de forma que los ficheros no se borren al cerrar la sesión:

```python
from google.colab import drive
drive.mount("/content/drive")
# Tus ficheros quedan en /content/drive/MyDrive/
```

Recuerda: **nunca** subas a Colab ficheros con datos de pacientes reales.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Abrir en modo `"w"` un fichero que se quería conservar:** se borra su contenido sin aviso.

**Olvidar `encoding="utf-8"`:** las tildes se leen como símbolos extraños (por ejemplo, «Ã³» en lugar de «ó»).

**No indicar el separador correcto** al leer un CSV con punto y coma.

**Usar los valores del CSV sin convertirlos:** `"72" + "5"` es `"725"`, no `77`.

**Confundir `json.dumps()` y `json.dump()`:** el primero devuelve un texto; el segundo escribe en un fichero.

**`FileNotFoundError`:** el fichero no existe en la carpeta actual, o la sesión se reinició y los ficheros temporales se borraron.
""")

c.titulo(3, "Ampliación: Gestionar carpetas y ficheros con os")
c.md("""
El módulo `os` crea carpetas, lista su contenido, comprueba si un fichero existe y lo borra. Es útil cuando hay muchos ficheros: por ejemplo, un informe por paciente.

Usa `os.path.join()` para construir las rutas. Así el código funciona igual en Windows, macOS y Linux.

**En tus materiales SIMUSTAT:** [Tema 100. Módulos para el tratamiento de ficheros](https://colab.research.google.com/drive/1q9hZcqKVktdQi5eDZGycieGFHDVABz2i), apartado 1.
""")
c.code("""
import os

os.makedirs("informes", exist_ok=True)        # no da error si ya existe
for codigo in ["P01", "P02", "P03"]:
    ruta = os.path.join("informes", f"{codigo}.txt")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"Paciente {codigo}: informe pendiente de revisar\\n")

print("Contenido:", sorted(os.listdir("informes")))
print("¿Existe P02?", os.path.exists(os.path.join("informes", "P02.txt")))

os.remove(os.path.join("informes", "P03.txt"))
print("Tras borrar P03:", sorted(os.listdir("informes")))
""")
c.md("""
`os.remove()` borra el fichero sin pasar por la papelera. Antes de borrar en un bucle, imprime la lista de ficheros y compruébala.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 70 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** identificar el separador, la coma decimal y los datos ausentes de varios CSV.
2. **Misión clínica (con pistas):** leer un CSV de un registro sintético. Calcular la edad media y el número de pacientes sin FEVI registrada.
3. **Misión reto (con asistente):** extraer el valor, la unidad y la fecha de un recurso FHIR *Observation*. Verificar el código que proponga el asistente con un segundo recurso distinto.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("Abres un fichero que ya contiene datos con open(\"datos.csv\", \"w\"). ¿Qué ocurre con el contenido anterior?", [
        ("Se borra", True, "Correcto: el modo \"w\" crea el fichero de nuevo. Para añadir se usa \"a\"."),
        ("Se conserva y lo nuevo se añade al final", False, "Eso hace el modo \"a\"."),
        ("Se produce un error", False, "No hay error; simplemente se sobrescribe."),
        ("Se crea una copia de seguridad", False, "Python no hace copias automáticas."),
    ]),
    ("Al leer un CSV con csv.DictReader, la edad aparece como \"72\". ¿De qué tipo es?", [
        ("str", True, "Correcto: todo lo que se lee de un CSV llega como texto y hay que convertirlo."),
        ("int", False, "Hay que convertirlo con int() para que sea un entero."),
        ("float", False, "csv no convierte los números automáticamente."),
        ("dict", False, "La fila completa es un diccionario; cada valor es texto."),
    ]),
    ("¿En qué se convierte el valor null de un JSON al leerlo con json.loads()?", [
        ("None", True, "Correcto: null es el valor nulo de JSON y equivale a None."),
        ("0", False, "null no es un cero."),
        ("\"null\"", False, "json.loads lo traduce a None, no a un texto."),
        ("False", False, "null y false son valores distintos en JSON."),
    ]),
    ("Un CSV exportado de una hoja de cálculo en español contiene la línea IC-004;77;68,4. ¿Qué parámetros necesitas al leerlo?", [
        ("Separador punto y coma y convertir la coma decimal en punto", True, "Correcto: el separador es ; y los decimales vienen con coma."),
        ("Ninguno: csv lo detecta automáticamente", False, "Por defecto csv usa la coma como separador."),
        ("Separador coma", False, "Partiría el peso 68,4 en dos columnas."),
        ("encoding=\"latin-1\"", False, "La codificación afecta a las tildes, no al separador."),
    ]),
    ("En el recurso FHIR del apartado 3.7, ¿qué expresión obtiene la unidad del resultado?", [
        ("obs[\"valueQuantity\"][\"unit\"]", True, "Correcto: la unidad está dentro de valueQuantity."),
        ("obs[\"unit\"]", False, "unit no está en el primer nivel del recurso."),
        ("obs[\"code\"][\"unit\"]", False, "code describe la prueba, no el resultado."),
        ("obs.unit", False, "A los diccionarios se accede con corchetes y la clave."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Los ficheros se abren con `with open(..., encoding="utf-8")`; el modo `"w"` sobrescribe.
- CSV es el formato de las tablas; todo se lee como texto y hay que comprobar separador y coma decimal.
- JSON es el formato de los datos estructurados y anidados, de las API y del estándar HL7 FHIR.
- Para llegar a un dato en un JSON anidado se encadenan claves e índices.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Codificación (UTF-8) | Forma de representar los caracteres, incluidas tildes y símbolos |
| CSV | Formato de tabla en texto plano con columnas separadas por un carácter |
| Separador | Carácter que separa las columnas de un CSV (coma, punto y coma, tabulador) |
| JSON | Formato de texto para datos estructurados y anidados |
| Serializar | Convertir datos de Python en texto (por ejemplo, JSON) para guardarlos o enviarlos |
| HL7 FHIR | Estándar internacional de intercambio de información sanitaria |
| LOINC | Sistema internacional de códigos para pruebas de laboratorio y observaciones clínicas |
| Seudonimizar | Sustituir los datos identificativos por un código, como IC-001 |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial de Python: lectura y escritura de archivos](https://docs.python.org/es/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Documentación del módulo csv](https://docs.python.org/es/3/library/csv.html)
- [Documentación del módulo json](https://docs.python.org/es/3/library/json.html)
- [Especificación de HL7 FHIR](https://hl7.org/fhir/)
""")

c.pie(70)
print(c.guardar("../cuadernos"))
