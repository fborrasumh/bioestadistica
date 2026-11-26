from plantilla import Cuaderno

c = Cuaderno("Tema_020_Representacion_de_datos_clinicos_en_Python.ipynb")

c.cabecera(
    20,
    "Representación de datos clínicos en Python: tipos numéricos, cadenas de texto y estructuras de datos",
    "Módulo 1. Descubriendo Python",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Distinguir los tipos de datos básicos de Python: enteros, decimales, texto, lógicos y valor nulo.
2. Relacionar cada tipo de dato de Python con el tipo de variable clínica que representa.
3. Convertir datos de un tipo a otro, en particular texto que contiene números.
4. Manipular cadenas de texto clínico: limpiar, normalizar y extraer partes.
5. Guardar series de mediciones en **listas** y la ficha de un paciente en un **diccionario**.
6. Reconocer los errores más frecuentes al mezclar tipos de datos.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: tipos y estructuras en Python | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un residente exporta desde la historia clínica electrónica los datos de un paciente ingresado en Medicina Interna (paciente sintético):

```
Paciente: P-0457 | Edad: 72 | Sexo: varón | Diabetes: sí
Glucemias capilares (mg/dL): 182, 165, 210, 148, 139
Diagnóstico: "  Insuficiencia cardiaca DESCOMPENSADA "
Peso al ingreso: "81,5"
Fracción de eyección: (no registrada)
```

Para un ordenador, cada uno de estos datos es de una naturaleza distinta. La edad es un número entero; el peso aparece como **texto** con coma decimal; el diagnóstico tiene espacios sobrantes y mayúsculas irregulares; las glucemias son una **serie** de valores; y la fracción de eyección **falta**.

Antes de calcular nada hay que **representar cada dato con el tipo adecuado**. Si no, la media de las glucemias, la comparación de diagnósticos o el cálculo del IMC darán errores o, peor, resultados falsos sin aviso.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Tipos de datos básicos")
c.md("""
| Tipo en Python | Nombre | Ejemplo | Variable clínica que suele representar |
| --- | --- | --- | --- |
| `int` | Entero | `72` | Cuantitativa discreta: edad en años, número de ingresos |
| `float` | Decimal (coma flotante) | `81.5` | Cuantitativa continua: peso, glucemia, creatinina |
| `str` | Cadena de texto | `"varón"` | Cualitativa: sexo, diagnóstico, servicio |
| `bool` | Lógico | `True`, `False` | Dicotómica: diabetes sí/no, éxitus sí/no |
| `NoneType` | Valor nulo | `None` | Dato **ausente**: no medido o no registrado |

La función `type()` indica el tipo de cualquier valor.

**El dato ausente no es un cero.** Una fracción de eyección no registrada no es una fracción de eyección del 0 %. Confundirlos es uno de los errores más graves al analizar datos clínicos; por eso Python tiene un valor específico, `None`.
""")
c.titulo(3, "2.2 Estructuras de datos")
c.md("""
| Estructura | Sintaxis | Para qué sirve | Ejemplo clínico |
| --- | --- | --- | --- |
| Lista | `[182, 165, 210]` | Serie ordenada de valores, modificable | Glucemias de un ingreso |
| Tupla | `(148, 92)` | Grupo fijo de valores que van juntos | Presión arterial sistólica y diastólica |
| Diccionario | `{"edad": 72, "sexo": "varón"}` | Pares **clave → valor** | Ficha de un paciente |
| Conjunto | `{"HTA", "DM2"}` | Elementos únicos, sin orden | Diagnósticos distintos de un servicio |

**Los índices empiezan en 0.** En una lista, el primer elemento es el `[0]`, el segundo el `[1]` y el último el `[-1]`.
""")

c.titulo(2, "3. Demostración: tipos y estructuras en Python (20 min)")
c.titulo(3, "3.1 Números y tipos")
c.code("""
edad_anios = 72
glucemia_mg_dl = 182.0
diabetes = True
fraccion_eyeccion = None

print(type(edad_anios), type(glucemia_mg_dl), type(diabetes), type(fraccion_eyeccion))
""")
c.md("""
Operaciones aritméticas básicas: `+`, `-`, `*`, `/` (división con decimales), `//` (división entera), `%` (resto) y `**` (potencia).
""")
c.code("""
dias_ingreso = 17
print("Semanas completas:", dias_ingreso // 7)
print("Días sobrantes:", dias_ingreso % 7)
print("Estancia en semanas:", round(dias_ingreso / 7, 1))
""")

c.titulo(3, "3.2 Convertir texto en números")
c.md("""
Los datos exportados llegan a menudo como **texto**. El peso `"81,5"` no se puede usar en un cálculo hasta convertirlo: primero se cambia la coma por un punto y después se convierte en `float`.
""")
c.code("""
peso_texto = "81,5"
peso_kg = float(peso_texto.replace(",", "."))
print(peso_kg, type(peso_kg))
""")
c.md("""
Las funciones `int()`, `float()` y `str()` convierten entre tipos. `int()` **trunca** (quita los decimales); para redondear se usa `round()`.
""")
c.code("""
print(int(81.9), round(81.9))
print("Peso: " + str(peso_kg) + " kg")
""")

c.titulo(3, "3.3 Cadenas de texto clínico")
c.md("""
Las cadenas tienen **métodos**, funciones que se aplican con un punto detrás del texto. Los más útiles para limpiar texto clínico:

| Método | Qué hace |
| --- | --- |
| `.strip()` | Quita los espacios del principio y del final |
| `.lower()` / `.upper()` | Pasa a minúsculas / mayúsculas |
| `.capitalize()` | Primera letra en mayúscula y el resto en minúscula |
| `.replace(a, b)` | Sustituye `a` por `b` |
| `.split(separador)` | Divide el texto en una lista |
| `.startswith(x)` | Comprueba si empieza por `x` |
""")
c.code("""
diagnostico = "  Insuficiencia cardiaca DESCOMPENSADA "
diagnostico_limpio = diagnostico.strip().capitalize()
print(f"[{diagnostico}]")
print(f"[{diagnostico_limpio}]")
""")
c.md("""
Normalizar el texto es imprescindible para contar casos: para Python, `"Insuficiencia cardiaca"` e `"insuficiencia cardiaca "` son textos **distintos**.
""")
c.code("""
print("Insuficiencia cardiaca" == "insuficiencia cardiaca ")
print("Insuficiencia cardiaca".lower() == "insuficiencia cardiaca ".strip().lower())
""")
c.md("""
Los caracteres de una cadena también se numeran desde 0, y se pueden extraer **porciones** con `[inicio:fin]` (el final no se incluye).
""")
c.code("""
codigo = "P-0457"
print("Prefijo:", codigo[0])
print("Número:", codigo[2:])
print("Longitud:", len(codigo))
""")
c.code("""
linea = "Paciente: P-0457 | Edad: 72 | Sexo: varón | Diabetes: sí"
campos = linea.split(" | ")
print(campos)
print("Edad como texto:", campos[1].split(": ")[1])
""")

c.titulo(3, "3.4 Listas: series de mediciones")
c.code("""
glucemias_mg_dl = [182, 165, 210, 148, 139]

print("Primera:", glucemias_mg_dl[0])
print("Última:", glucemias_mg_dl[-1])
print("Número de mediciones:", len(glucemias_mg_dl))
print("Máxima:", max(glucemias_mg_dl), "· Mínima:", min(glucemias_mg_dl))
print(f"Media: {sum(glucemias_mg_dl) / len(glucemias_mg_dl):.1f} mg/dL")
""")
c.md("""
Las listas se pueden ampliar con `.append()`, ordenar con `sorted()` y recortar con porciones.
""")
c.code("""
glucemias_mg_dl.append(126)        # nueva glucemia del día siguiente
print("Serie actualizada:", glucemias_mg_dl)
print("Ordenada:", sorted(glucemias_mg_dl))
print("Primeras tres:", glucemias_mg_dl[:3])
""")

c.titulo(3, "3.5 Tuplas: valores que van juntos")
c.code("""
presion_arterial = (148, 92)       # (sistólica, diastólica)
pas, pad = presion_arterial        # desempaquetado
print(f"PAS {pas} mmHg · PAD {pad} mmHg")
""")
c.md("""
Una tupla no se puede modificar. Es útil para datos que no deben cambiar por error, como una medición ya registrada.
""")

c.titulo(3, "3.6 Diccionarios: la ficha del paciente")
c.code("""
paciente = {
    "codigo": "P-0457",
    "edad": 72,
    "sexo": "varón",
    "diabetes": True,
    "peso_kg": 81.5,
    "glucemias_mg_dl": [182, 165, 210, 148, 139],
    "fraccion_eyeccion": None,
}

print("Edad:", paciente["edad"])
print("Glucemia máxima:", max(paciente["glucemias_mg_dl"]))
print("¿Tiene registrada la fracción de eyección?", paciente["fraccion_eyeccion"] is not None)
""")
c.md("""
Se añaden o modifican datos asignando un valor a una clave. El método `.get()` devuelve un valor por defecto si la clave no existe, en lugar de dar error.
""")
c.code("""
paciente["fraccion_eyeccion"] = 35       # el ecocardiograma ya está informado
paciente["servicio"] = "Medicina Interna"

print(paciente["fraccion_eyeccion"])
print(paciente.get("alergias", "sin registrar"))
print(list(paciente.keys()))
""")

c.titulo(3, "3.7 Una cohorte: lista de diccionarios")
c.md("""
Varios pacientes se representan como una **lista de diccionarios**: cada elemento de la lista es la ficha de un paciente. Esta es la estructura que, en el Tema 100, se convertirá en una tabla de datos con Pandas.
""")
c.code("""
cohorte = [
    {"codigo": "P-0457", "edad": 72, "diabetes": True},
    {"codigo": "P-0458", "edad": 65, "diabetes": False},
    {"codigo": "P-0459", "edad": 81, "diabetes": True},
]

print("Pacientes:", len(cohorte))
print("Edad del segundo paciente:", cohorte[1]["edad"])
""")

c.titulo(3, "Ampliación: conjuntos para valores únicos")
c.code("""
diagnosticos_servicio = ["HTA", "DM2", "HTA", "EPOC", "DM2", "HTA"]
distintos = set(diagnosticos_servicio)
print("Diagnósticos distintos:", distintos)
print("Número de diagnósticos distintos:", len(distintos))
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Sumar texto y números.** `"Peso: " + 81.5` produce `TypeError`. Hay que convertir el número con `str()` o, mejor, usar una cadena formateada (*f-string*).
""")
c.code("""
peso_kg = 81.5
print(f"Peso: {peso_kg} kg")
""")
c.md("""
**Convertir texto con coma.** `float("81,5")` produce `ValueError`: primero hay que reemplazar la coma por un punto.

**Salirse de la lista.** En una lista de 5 elementos, el índice `[5]` no existe (los válidos van de 0 a 4) y produce `IndexError`.

**Pedir una clave inexistente.** `paciente["alergias"]` produce `KeyError` si la clave no existe; `paciente.get("alergias")` devuelve `None`.

**Tratar el dato ausente como cero.** Sustituir un `None` por `0` antes de calcular una media la sesga hacia abajo. En el Tema 100 veremos cómo tratar correctamente los valores perdidos.

Quita el `#` de cada línea, una a una, para ver los mensajes de error:
""")
c.code("""
# print("Peso: " + 81.5)
# float("81,5")
# [182, 165, 210, 148, 139][5]
# paciente["alergias"]
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 20 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** asignar el tipo de dato de Python adecuado a cada campo de una historia clínica sintética.
2. **Misión clínica (con pistas):** limpiar un texto exportado de la historia clínica y construir el diccionario del paciente.
3. **Misión reto (con asistente):** calcular la media de una serie de constantes con valores ausentes sin tratarlos como ceros, y verificar el código que proponga el asistente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Qué tipo de dato de Python es el más adecuado para registrar si un paciente es fumador?", [
        ("bool", True, "Correcto: es una variable dicotómica, con dos valores posibles."),
        ("float", False, "float representa cantidades continuas, no categorías."),
        ("list", False, "Una lista guarda varios valores; aquí solo hay uno."),
        ("None", False, "None representa un dato ausente, no una respuesta sí/no."),
    ]),
    ("La lista glucemias = [182, 165, 210, 148, 139]. ¿Qué devuelve glucemias[1]?", [
        ("165", True, "Correcto: los índices empiezan en 0, así que [1] es el segundo elemento."),
        ("182", False, "182 es glucemias[0]."),
        ("139", False, "139 es glucemias[-1]."),
        ("Un error", False, "El índice 1 existe en una lista de cinco elementos."),
    ]),
    ("¿Cuál es la forma correcta de convertir el texto \"81,5\" en el número 81.5?", [
        ("float(\"81,5\".replace(\",\", \".\"))", True, "Correcto: primero se cambia la coma por el punto y después se convierte."),
        ("float(\"81,5\")", False, "Produce ValueError: Python no acepta la coma decimal."),
        ("int(\"81,5\")", False, "int no acepta decimales ni coma."),
        ("str(81,5)", False, "str convierte en texto, que es justo lo contrario de lo que se busca."),
    ]),
    ("La fracción de eyección de un paciente no se ha medido. ¿Cómo debe registrarse?", [
        ("None", True, "Correcto: indica que el dato falta, sin confundirlo con un valor real."),
        ("0", False, "Un 0 % es un valor clínico (incompatible con la vida), no un dato ausente."),
        ("\"\"", False, "Una cadena vacía es texto, no un valor nulo, y dificulta los cálculos."),
        ("False", False, "False es un valor lógico, no un dato ausente."),
    ]),
    ("paciente = {\"edad\": 72, \"sexo\": \"varón\"}. ¿Qué devuelve paciente.get(\"alergias\")?", [
        ("None", True, "Correcto: .get() devuelve None si la clave no existe."),
        ("KeyError", False, "Eso ocurre con paciente[\"alergias\"], no con .get()."),
        ("\"alergias\"", False, ".get() devuelve el valor asociado, no el nombre de la clave."),
        ("False", False, ".get() no devuelve valores lógicos por defecto."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Cada dato clínico se representa con un tipo: `int`, `float`, `str`, `bool` o `None`.
- El dato ausente se registra como `None`, nunca como cero.
- El texto exportado se limpia y se convierte antes de calcular.
- Las listas guardan series de mediciones; los diccionarios, la ficha de un paciente; una lista de diccionarios, una cohorte.
- Los índices empiezan en 0.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Tipo de dato | Naturaleza de un valor, que determina qué operaciones admite |
| Cadena (`str`) | Secuencia de caracteres de texto |
| Método | Función propia de un tipo de dato que se aplica con un punto, como `.strip()` |
| Índice | Posición de un elemento en una lista o una cadena, empezando por 0 |
| Lista | Serie ordenada y modificable de valores |
| Tupla | Serie ordenada que no se puede modificar |
| Diccionario | Colección de pares clave → valor |
| `None` | Valor nulo de Python; representa un dato ausente |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial de Python: introducción informal (números, texto y listas)](https://docs.python.org/es/3/tutorial/introduction.html)
- [Tutorial de Python: estructuras de datos](https://docs.python.org/es/3/tutorial/datastructures.html)
""")

c.pie(20)
print(c.guardar("../cuadernos"))
