from plantilla import Cuaderno

c = Cuaderno("Tema_030_Logica_booleana_y_estructuras_condicionales.ipynb")

c.cabecera(
    30,
    "Lógica booleana y estructuras condicionales aplicadas a la clasificación clínica",
    "Módulo 1. Descubriendo Python",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Escribir comparaciones entre valores clínicos y obtener un resultado lógico (`True` o `False`).
2. Combinar varias condiciones con los operadores `and`, `or` y `not`.
3. Construir estructuras `if`, `elif` y `else` para clasificar a un paciente según criterios clínicos.
4. Ordenar correctamente las condiciones y tratar los límites de cada categoría.
5. Manejar datos ausentes antes de aplicar una regla de decisión.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: reglas clínicas en Python | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En el servicio de Urgencias llega **Antonio**, de 77 años (paciente sintético), con fiebre y sospecha de infección respiratoria. En el triaje se registran:

| Dato | Valor |
| --- | --- |
| Frecuencia respiratoria | 24 rpm |
| Presión arterial sistólica | 96 mmHg |
| Estado mental | Desorientado (Glasgow 14) |

La escala **qSOFA** (*quick Sequential Organ Failure Assessment*) suma un punto por cada criterio que se cumple. Los criterios son: frecuencia respiratoria ≥ 22 rpm, presión sistólica ≤ 100 mmHg y alteración del estado mental. Una puntuación de 2 o más identifica a pacientes con infección y mayor riesgo de mala evolución.

Antonio cumple los tres criterios. Para un clínico, la decisión es inmediata. Pero un **sistema de alerta** de la historia clínica la toma con todos los pacientes que llegan. Por eso la regla tiene que estar escrita sin ambigüedad: **si** se cumple esto **y** aquello, **entonces** se activa la alerta. Eso es la lógica condicional.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Comparaciones")
c.diagrama('Recta numérica en 22 rpm: fr_rpm >= 22 incluye el 22; fr_rpm > 22 lo excluye.')
c.md("""
Una comparación devuelve un valor lógico (`bool`): `True` o `False`.

| Operador | Significado | Ejemplo clínico | Resultado con FR = 24 |
| --- | --- | --- | --- |
| `==` | Igual a | `fr_rpm == 22` | `False` |
| `!=` | Distinto de | `fr_rpm != 22` | `True` |
| `<` / `>` | Menor / mayor que | `fr_rpm > 22` | `True` |
| `<=` / `>=` | Menor o igual / mayor o igual | `fr_rpm >= 22` | `True` |
| `in` | Pertenece a | `"tos" in sintomas` | Depende de la lista |

**No confundas `=` con `==`.** Un solo signo **asigna** un valor; dos signos **comparan**.
""")
c.titulo(3, "2.2 Operadores lógicos")
c.md("""
| Operador | Verdadero cuando… | Ejemplo clínico |
| --- | --- | --- |
| `and` | Se cumplen **todas** las condiciones | Fiebre **y** tos |
| `or` | Se cumple **al menos una** | Dolor torácico **o** disnea |
| `not` | La condición **no** se cumple | **No** alérgico a penicilina |

Tabla de verdad:

| A | B | A `and` B | A `or` B | `not` A |
| --- | --- | --- | --- | --- |
| True | True | True | True | False |
| True | False | False | True | False |
| False | True | False | True | True |
| False | False | False | False | True |
""")
c.titulo(3, "2.3 Estructuras condicionales")
c.md("""
```python
if condición_1:
    acciones si se cumple la condición 1
elif condición_2:
    acciones si no se cumple la 1 pero sí la 2
else:
    acciones si no se cumple ninguna
```

- Las acciones de cada rama van **sangradas** con 4 espacios: así sabe Python qué pertenece a cada rama.
- Cada línea `if`, `elif` y `else` termina en **dos puntos**.
- Python evalúa las condiciones **de arriba abajo** y ejecuta **solo la primera rama que se cumple**. Por eso el orden importa.
""")

c.titulo(2, "3. Demostración: reglas clínicas en Python (20 min)")
c.titulo(3, "3.1 Comparaciones y operadores lógicos")
c.code("""
fr_rpm = 24
pas_mmHg = 96
estado_mental_alterado = True

print("FR ≥ 22:", fr_rpm >= 22)
print("PAS ≤ 100:", pas_mmHg <= 100)
print("FR alta y PAS baja:", fr_rpm >= 22 and pas_mmHg <= 100)
print("Alguno de los tres:", fr_rpm >= 22 or pas_mmHg <= 100 or estado_mental_alterado)
""")

c.titulo(3, "3.2 La escala qSOFA")
c.md("""
En Python, `True` vale 1 y `False` vale 0 al sumar. Así, la puntuación qSOFA es la suma de los tres criterios.
""")
c.code("""
qsofa = (fr_rpm >= 22) + (pas_mmHg <= 100) + estado_mental_alterado
print("qSOFA:", qsofa)

if qsofa >= 2:
    print("qSOFA positivo: paciente con mayor riesgo. Valorar disfunción orgánica.")
else:
    print("qSOFA negativo. Mantener la vigilancia clínica.")
""")

c.titulo(3, "3.3 Varias categorías: el índice de masa corporal")
c.md("""
Con `elif` se encadenan tantas categorías como haga falta. Clasificación de la OMS para adultos:

| IMC (kg/m²) | Categoría |
| --- | --- |
| < 18,5 | Bajo peso |
| 18,5 a 24,9 | Normal |
| 25,0 a 29,9 | Sobrepeso |
| ≥ 30,0 | Obesidad |
""")
c.code("""
peso_kg = 68
talla_m = 1.63
imc = peso_kg / talla_m ** 2

if imc < 18.5:
    categoria = "bajo peso"
elif imc < 25:
    categoria = "normal"
elif imc < 30:
    categoria = "sobrepeso"
else:
    categoria = "obesidad"

print(f"IMC {imc:.1f} kg/m²: {categoria}")
""")
c.md("""
Observa que la segunda condición es solo `imc < 25`. No hace falta escribir `imc >= 18.5 and imc < 25`: si el IMC fuera menor de 18,5, ya se habría ejecutado la primera rama.
""")

c.titulo(3, "3.4 Dos variables a la vez: la presión arterial")
c.md("""
La guía de la Sociedad Europea de Hipertensión (2023) clasifica la presión arterial en consulta así:

| Categoría | PAS (mmHg) | | PAD (mmHg) |
| --- | --- | --- | --- |
| Óptima | < 120 | y | < 80 |
| Normal | 120 a 129 | y/o | 80 a 84 |
| Normal-alta | 130 a 139 | y/o | 85 a 89 |
| Hipertensión grado 1 | 140 a 159 | y/o | 90 a 99 |
| Hipertensión grado 2 | 160 a 179 | y/o | 100 a 109 |
| Hipertensión grado 3 | ≥ 180 | y/o | ≥ 110 |

Si la sistólica y la diastólica caen en categorías distintas, se asigna **la más alta**. Por eso conviene empezar comprobando la categoría más grave y usar `or`.
""")
c.code("""
pas_mmHg = 148
pad_mmHg = 92

if pas_mmHg >= 180 or pad_mmHg >= 110:
    categoria_pa = "hipertensión grado 3"
elif pas_mmHg >= 160 or pad_mmHg >= 100:
    categoria_pa = "hipertensión grado 2"
elif pas_mmHg >= 140 or pad_mmHg >= 90:
    categoria_pa = "hipertensión grado 1"
elif pas_mmHg >= 130 or pad_mmHg >= 85:
    categoria_pa = "normal-alta"
elif pas_mmHg >= 120 or pad_mmHg >= 80:
    categoria_pa = "normal"
else:
    categoria_pa = "óptima"

print(f"{pas_mmHg}/{pad_mmHg} mmHg: {categoria_pa}")
""")
c.md("""
Prueba con 132/101 mmHg: la sistólica sería normal-alta, pero la diastólica lo lleva a hipertensión grado 2.
""")

c.titulo(3, "3.5 Pertenencia a una lista: síntomas de alarma")
c.code("""
sintomas = ["fiebre", "tos", "disnea"]
sintomas_alarma = ["disnea", "dolor torácico", "hemoptisis"]

if "disnea" in sintomas:
    print("Presenta disnea: valorar saturación de oxígeno.")

alarma = any(s in sintomas_alarma for s in sintomas)
print("¿Algún síntoma de alarma?", alarma)
""")
c.md("""
La función `any()` devuelve `True` si **alguno** de los elementos cumple la condición; `all()` devuelve `True` si los cumplen **todos**. La sintaxis `for s in sintomas` se explica en el Tema 40.
""")

c.titulo(3, "3.6 Comprobar primero que el dato existe")
c.md("""
Una regla clínica no se puede aplicar si falta un dato. Comparar `None` con un número da error, así que primero se comprueba que el valor existe con `is None`.
""")
c.code("""
glucemia_ayunas_mg_dl = None     # pendiente de resultado

if glucemia_ayunas_mg_dl is None:
    print("Glucemia no disponible: no se puede clasificar.")
elif glucemia_ayunas_mg_dl >= 126:
    print("Compatible con diabetes (confirmar con una segunda determinación).")
elif glucemia_ayunas_mg_dl >= 100:
    print("Glucemia basal alterada.")
else:
    print("Glucemia en ayunas normal.")
""")

c.titulo(3, "Ampliación: la expresión condicional de una línea")
c.code("""
temperatura_c = 38.4
estado = "febril" if temperatura_c >= 38 else "afebril"
print(estado)
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Ordenar mal las condiciones.** Si se comprueba `imc >= 25` antes que `imc >= 30`, un paciente con IMC 34 sale como sobrepeso. Se ejecuta siempre la primera rama que se cumple.
""")
c.code("""
imc = 34
if imc >= 25:
    print("Clasificación errónea: sobrepeso")
elif imc >= 30:
    print("Nunca se llega aquí")
""")
c.md("""
**Equivocar los límites.** «PAS ≤ 100» no es lo mismo que «PAS < 100». Un paciente con 100 mmHg exactos cumple el primer criterio, pero no el segundo. Comprueba siempre los valores frontera.

**Usar `=` en lugar de `==`** dentro de un `if`: produce `SyntaxError`.

**Olvidar los dos puntos o la sangría.** Producen `SyntaxError` e `IndentationError`.

**Comparar texto sin normalizarlo.** `"Disnea" == "disnea"` es `False`. Normaliza con `.lower()` antes de comparar.

**Escribir mal una condición compuesta.** `fr_rpm >= 22 or 30` es siempre verdadera, porque `30` por sí solo se considera verdadero. Lo correcto es repetir la variable: `fr_rpm >= 22 or fr_rpm >= 30`.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 30 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** predecir el resultado de comparaciones y condiciones compuestas con datos clínicos.
2. **Misión clínica (con pistas):** programar la clasificación de la glucemia en ayunas y la de la presión arterial, comprobando los valores frontera.
3. **Misión reto (con asistente):** programar la escala CURB-65 de gravedad de la neumonía. Verificar con casos conocidos el código que proponga el asistente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("Con fr = 22 y pas = 100, ¿cuánto vale (fr >= 22) + (pas < 100)?", [
        ("1", True, "Correcto: fr >= 22 es True (1) y pas < 100 es False (0), porque 100 no es menor que 100."),
        ("2", False, "Revisa el segundo criterio: 100 < 100 es falso."),
        ("0", False, "El primer criterio sí se cumple: 22 >= 22."),
        ("True", False, "Al sumar valores lógicos se obtiene un número."),
    ]),
    ("Un paciente tiene 130/112 mmHg. Según el código del apartado 3.4, ¿cómo se clasifica?", [
        ("Hipertensión grado 3", True, "Correcto: la diastólica ≥ 110 basta, porque la condición usa or."),
        ("Normal-alta", False, "Esa sería la categoría de la sistólica, pero se asigna la más alta."),
        ("Hipertensión grado 1", False, "La diastólica de 112 supera el umbral de grado 3."),
        ("No se puede clasificar", False, "Con las dos cifras disponibles, la regla da una categoría."),
    ]),
    ("¿Qué expresión es verdadera solo si el paciente tiene fiebre y no es alérgico a la penicilina?", [
        ("fiebre and not alergia_penicilina", True, "Correcto: and exige las dos condiciones y not invierte la segunda."),
        ("fiebre or not alergia_penicilina", False, "Con or bastaría con una de las dos."),
        ("not fiebre and alergia_penicilina", False, "Invierte las dos condiciones respecto a lo pedido."),
        ("fiebre and alergia_penicilina", False, "Seleccionaría justo a los alérgicos."),
    ]),
    ("En una cadena if/elif para el IMC, ¿por qué se comprueba imc < 18.5 antes que imc < 25?", [
        ("Porque solo se ejecuta la primera rama que se cumple", True, "Correcto: si se comprobara antes imc < 25, el bajo peso nunca se detectaría."),
        ("Porque Python ordena las condiciones automáticamente", False, "Python respeta el orden en que se escriben."),
        ("Por estilo: el orden no influye en el resultado", False, "El orden sí cambia el resultado."),
        ("Porque elif solo admite comparaciones con <", False, "elif admite cualquier condición."),
    ]),
    ("La glucemia de un paciente vale None. ¿Qué ocurre al ejecutar if glucemia >= 126:?", [
        ("Se produce un TypeError", True, "Correcto: no se puede comparar None con un número. Hay que comprobar antes si es None."),
        ("La condición es False y se pasa a la siguiente rama", False, "Python no compara None con números: da error."),
        ("La condición es True", False, "La comparación ni siquiera se puede evaluar."),
        ("Python sustituye None por 0", False, "Python nunca sustituye automáticamente un dato ausente."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Una comparación produce `True` o `False`; `and`, `or` y `not` las combinan.
- `if`, `elif` y `else` traducen una regla clínica a código; solo se ejecuta la primera rama que se cumple.
- Con categorías ordenadas, empieza por un extremo y respeta los límites exactos de la guía.
- Comprueba que el dato existe (`is None`) antes de aplicar una regla.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Valor lógico (`bool`) | `True` o `False` |
| Operador de comparación | Símbolo que compara dos valores: `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Operador lógico | `and`, `or`, `not`: combinan o invierten condiciones |
| Estructura condicional | Bloque `if`/`elif`/`else` que ejecuta código según se cumplan condiciones |
| Sangría | Espacios al inicio de la línea que indican qué código pertenece a cada bloque |
| Valor frontera | Valor exacto del límite entre dos categorías |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial de Python: la sentencia if](https://docs.python.org/es/3/tutorial/controlflow.html#if-statements)
- Singer M, *et al.* The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). *JAMA*. 2016;315(8):801-810. doi:[10.1001/jama.2016.0287](https://doi.org/10.1001/jama.2016.0287)
- Mancia G, *et al.* 2023 ESH Guidelines for the management of arterial hypertension. *J Hypertens*. 2023;41(12):1874-2071. doi:[10.1097/HJH.0000000000003480](https://doi.org/10.1097/HJH.0000000000003480)
""")

c.pie(30)
print(c.guardar("../cuadernos"))
