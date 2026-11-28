from plantilla import Cuaderno

c = Cuaderno("Tema_040_Estructuras_iterativas_series_de_pacientes.ipynb")

c.cabecera(
    40,
    "Estructuras iterativas para el procesamiento de series de pacientes",
    "Módulo 1. Descubriendo Python",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Recorrer una serie de mediciones o una cohorte de pacientes con un bucle `for`.
2. Usar acumuladores y contadores para calcular totales, medias y proporciones.
3. Combinar bucles y condiciones para detectar valores de alarma.
4. Recorrer varias listas a la vez con `zip()` y numerar los elementos con `enumerate()`.
5. Repetir un cálculo mientras se cumpla una condición con un bucle `while`.
6. Calcular la prevalencia de una condición en una cohorte sintética.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: bucles con datos clínicos | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
La supervisora de una planta de Endocrinología pide un informe al final del turno. Hay 8 pacientes con diabetes ingresados. ¿Cuántos han tenido alguna **hipoglucemia** (glucemia < 70 mg/dL) en las últimas 24 horas? ¿Cuál ha sido la glucemia media de cada uno?

Cada paciente tiene entre 4 y 6 glucemias capilares. Revisarlas una a una es lento y propenso a errores, y mañana habrá que repetirlo. Lo que se necesita es una instrucción que diga: **para cada paciente**, y **para cada glucemia** de ese paciente, comprueba si es menor de 70.

Un **bucle** repite la misma operación sobre todos los elementos de una serie. Es la base de cualquier análisis de datos.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 El bucle for")
c.md("""
```python
for elemento in serie:
    acciones con elemento
```

- `serie` puede ser una lista, una cadena, un `range()` o cualquier colección.
- En cada vuelta (**iteración**), `elemento` toma el siguiente valor de la serie.
- Las acciones van sangradas, como en un `if`.
""")
c.titulo(3, "2.2 Acumuladores y contadores")
c.diagrama('Acumulador y contador con las glucemias 110, 65 y 140: total llega a 315, n_hipo a 1 y la media es 105.')
c.md("""
Para resumir una serie se usa una variable que se inicializa **antes** del bucle y se actualiza **dentro** de él:

| Patrón | Inicialización | Dentro del bucle | Ejemplo clínico |
| --- | --- | --- | --- |
| Acumulador | `total = 0` | `total = total + valor` | Suma de glucemias para la media |
| Contador | `n = 0` | `n = n + 1` si se cumple una condición | Número de hipoglucemias |
| Lista de resultados | `resultados = []` | `resultados.append(...)` | IMC de cada paciente |

`total = total + valor` puede abreviarse como `total += valor`.
""")
c.titulo(3, "2.3 El bucle while")
c.diagrama('Diagrama de flujo de un while que divide la concentración entre 2 mientras sea al menos 10 mg/L: 100, 50, 25, 12,5 y 6,25; 4 vidas medias.', nombre="e2_3")
c.md("""
```python
while condición:
    acciones
```

Repite las acciones **mientras** la condición sea verdadera. Se usa cuando no se sabe de antemano cuántas repeticiones hacen falta. Por ejemplo, cuántas vidas medias tarda un fármaco en bajar de un nivel. Dentro del bucle algo tiene que cambiar para que la condición acabe siendo falsa; si no, el bucle no termina nunca.
""")
c.titulo(3, "2.4 Prevalencia")
c.md("""
La **prevalencia** es la proporción de individuos de una población que presentan una condición en un momento dado:

$$\\text{Prevalencia} = \\frac{\\text{número de casos}}{\\text{número total de individuos}}$$

Es el primer indicador que calcularemos con un bucle: un contador de casos dividido entre el total.
""")

c.titulo(2, "3. Demostración: bucles con datos clínicos (20 min)")
c.titulo(3, "3.1 Recorrer una serie de mediciones")
c.code("""
glucemias_mg_dl = [182, 165, 64, 148, 139, 92]

for glucemia in glucemias_mg_dl:
    print(glucemia, "mg/dL")
""")
c.titulo(3, "3.2 Acumulador: la media")
c.code("""
total = 0
for glucemia in glucemias_mg_dl:
    total += glucemia

media = total / len(glucemias_mg_dl)
print(f"Glucemia media: {media:.1f} mg/dL")
""")
c.md("""
Python tiene la función `sum()`, que hace lo mismo en una línea. Escribir el bucle sirve para entender qué hace `sum()` por dentro y para cuando el cálculo es más complejo que una suma.
""")
c.code("""
print(sum(glucemias_mg_dl) / len(glucemias_mg_dl))
""")

c.titulo(3, "3.3 Bucle con condición: detectar hipoglucemias")
c.code("""
hipoglucemias = 0
for glucemia in glucemias_mg_dl:
    if glucemia < 70:
        hipoglucemias += 1
        print(f"Hipoglucemia detectada: {glucemia} mg/dL")

print("Total de hipoglucemias:", hipoglucemias)
""")

c.titulo(3, "3.4 Numerar con enumerate() y emparejar con zip()")
c.md("""
`enumerate()` da a la vez la posición y el valor. Aquí se suma 1 a la posición para numerar las tomas desde 1, como se haría en la gráfica de enfermería.
""")
c.code("""
for posicion, glucemia in enumerate(glucemias_mg_dl):
    print(f"Toma {posicion + 1}: {glucemia} mg/dL")
""")
c.md("""
`zip()` recorre varias listas a la vez, emparejando sus elementos. Útil cuando sistólica y diastólica se guardan en listas separadas.
""")
c.code("""
horas = ["08:00", "14:00", "20:00"]
pas_mmHg = [152, 138, 145]
pad_mmHg = [94, 86, 91]

for hora, pas, pad in zip(horas, pas_mmHg, pad_mmHg):
    pam = pad + (pas - pad) / 3
    print(f"{hora}  PA {pas}/{pad} mmHg  PAM {pam:.0f} mmHg")
""")

c.titulo(3, "3.5 Repetir un número de veces: range()")
c.md("""
`range(n)` genera los números de 0 a n − 1. `range(inicio, fin, paso)` permite elegir el inicio, el final (no incluido) y el salto.
""")
c.code("""
# Horas de administración de un antibiótico cada 8 horas durante un día
for hora in range(0, 24, 8):
    print(f"Dosis a las {hora:02d}:00")
""")

c.titulo(3, "3.6 Recorrer una cohorte")
c.md("""
La cohorte del caso: cada paciente es un diccionario con su código y sus glucemias. Un bucle **dentro de otro** (bucles anidados) recorre primero los pacientes y, para cada uno, sus glucemias.
""")
c.code("""
cohorte = [
    {"codigo": "E-01", "glucemias": [182, 165, 148, 139]},
    {"codigo": "E-02", "glucemias": [96, 64, 110, 128, 105]},
    {"codigo": "E-03", "glucemias": [210, 198, 176, 160, 155, 149]},
    {"codigo": "E-04", "glucemias": [88, 72, 69, 91]},
    {"codigo": "E-05", "glucemias": [140, 132, 151, 147]},
    {"codigo": "E-06", "glucemias": [120, 115, 98, 101, 110]},
    {"codigo": "E-07", "glucemias": [65, 58, 92, 140]},
    {"codigo": "E-08", "glucemias": [170, 162, 158, 149, 152]},
]

pacientes_con_hipoglucemia = 0

for paciente in cohorte:
    glucemias = paciente["glucemias"]
    media = sum(glucemias) / len(glucemias)

    tuvo_hipoglucemia = False
    for glucemia in glucemias:
        if glucemia < 70:
            tuvo_hipoglucemia = True

    if tuvo_hipoglucemia:
        pacientes_con_hipoglucemia += 1

    marca = "  ← hipoglucemia" if tuvo_hipoglucemia else ""
    print(f"{paciente['codigo']}: media {media:.0f} mg/dL{marca}")

proporcion = pacientes_con_hipoglucemia / len(cohorte)
print(f"\\nPacientes con alguna hipoglucemia: {pacientes_con_hipoglucemia} de {len(cohorte)} ({proporcion:.0%})")
""")
c.md("""
El formato `{proporcion:.0%}` multiplica por 100 y añade el signo de porcentaje.
""")

c.titulo(3, "3.7 El bucle while: eliminación de un fármaco")
c.md("""
Un fármaco con una **vida media** de 6 horas reduce su concentración plasmática a la mitad cada 6 horas. Si la concentración inicial es 40 mg/L, ¿cuántas horas tardará en bajar a 5 mg/L o menos? No sabemos de antemano cuántas vueltas hará falta dar: es un caso típico de `while`.
""")
c.code("""
concentracion_mg_l = 40
vida_media_h = 6
umbral_mg_l = 5
horas = 0

while concentracion_mg_l > umbral_mg_l:
    concentracion_mg_l = concentracion_mg_l / 2
    horas += vida_media_h
    print(f"A las {horas} h: {concentracion_mg_l:.1f} mg/L")

print(f"Tarda {horas} horas ({horas // vida_media_h} vidas medias) en llegar a {umbral_mg_l} mg/L")
""")

c.titulo(3, "Ampliación: break y continue")
c.md("""
`break` sale del bucle en cuanto se cumple algo; `continue` salta a la siguiente vuelta. Útil para detenerse en la **primera** alarma o para ignorar datos ausentes.
""")
c.code("""
saturaciones = [97, 96, None, 94, 89, 95]

for toma, sat in enumerate(saturaciones, start=1):
    if sat is None:
        print(f"Toma {toma}: sin dato, se omite")
        continue
    if sat < 90:
        print(f"Toma {toma}: saturación {sat} %. Avisar al médico de guardia.")
        break
    print(f"Toma {toma}: {sat} %")
""")

c.titulo(3, "Ampliación: listas por comprensión")
c.md("""
Una **lista por comprensión** construye una lista nueva en una sola línea a partir de otra. Es una forma compacta de escribir un bucle con `append()`.
""")
c.code("""
glucemias_mg_dl = [182, 165, 64, 148, 139, 92]

glucemias_mmol_l = [round(g / 18, 1) for g in glucemias_mg_dl]
hipoglucemias = [g for g in glucemias_mg_dl if g < 70]

print(glucemias_mmol_l)
print(hipoglucemias)
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Inicializar el acumulador dentro del bucle.** Si `total = 0` se escribe dentro del `for`, se pone a cero en cada vuelta y al final solo contiene el último valor.

**Olvidar la sangría.** Lo que no está sangrado no forma parte del bucle y se ejecuta una sola vez al final.

**Bucles while infinitos.** Si dentro del bucle no cambia nada que afecte a la condición, el bucle no termina. En Colab se detiene con el botón ■ de la celda.

**Modificar la lista que se recorre.** Añadir o quitar elementos de una lista mientras se recorre con `for` produce resultados imprevisibles; es mejor construir una lista nueva.

**Dividir entre cero.** Al calcular una media o una proporción, comprueba que la serie no está vacía: `len(lista) == 0` produce `ZeroDivisionError`.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 40 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** predecir cuántas veces se ejecuta un bucle y qué valor final tiene un acumulador.
2. **Misión clínica (con pistas):** calcular la prevalencia de hipertensión en una cohorte sintética y el IMC de cada paciente.
3. **Misión reto (con asistente):** programar con `while` cuántas dosis de mantenimiento hacen falta para llegar al estado estacionario de un fármaco. Verificar el código que proponga el asistente.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Cuántas veces se ejecuta print en: for h in range(0, 24, 6): print(h)?", [
        ("4", True, "Correcto: range(0, 24, 6) genera 0, 6, 12 y 18; el 24 no se incluye."),
        ("5", False, "El final de range no se incluye: 24 no aparece."),
        ("24", False, "El paso es 6, no 1."),
        ("6", False, "Revisa qué números genera range con paso 6."),
    ]),
    ("Se quiere contar las glucemias menores de 70 mg/dL. ¿Dónde debe ir contador = 0?", [
        ("Antes del bucle", True, "Correcto: si se pone dentro, el contador vuelve a cero en cada vuelta."),
        ("Dentro del bucle, antes del if", False, "Se reiniciaría en cada vuelta y solo contaría la última glucemia."),
        ("Dentro del if", False, "Se pondría a cero cada vez que se detectara un caso."),
        ("Después del bucle", False, "El bucle intentaría usar una variable que todavía no existe."),
    ]),
    ("En una cohorte de 250 pacientes, 45 tienen diabetes. ¿Cuál es la prevalencia de diabetes?", [
        ("18 %", True, "Correcto: 45 / 250 = 0,18."),
        ("45 %", False, "45 es el número de casos, no la proporción."),
        ("5,6 %", False, "Sale de dividir 250 entre 45: el orden de la división está invertido."),
        ("82 %", False, "Esa es la proporción de pacientes sin diabetes."),
    ]),
    ("¿Cuándo es preferible un bucle while a un bucle for?", [
        ("Cuando no se sabe de antemano cuántas repeticiones hacen falta", True, "Correcto: while repite mientras se cumpla una condición."),
        ("Cuando se recorre una lista de pacientes", False, "Para recorrer una lista conocida es más claro un for."),
        ("Siempre, porque es más rápido", False, "No es más rápido; cada uno tiene su uso."),
        ("Nunca: while está desaconsejado en Python", False, "while es una estructura básica y útil."),
    ]),
    ("Un fármaco tiene una vida media de 4 horas y una concentración inicial de 80 mg/L. ¿Qué concentración tiene a las 12 horas?", [
        ("10 mg/L", True, "Correcto: 12 horas son 3 vidas medias: 80 → 40 → 20 → 10."),
        ("20 mg/L", False, "Eso son solo 2 vidas medias (8 horas)."),
        ("26,7 mg/L", False, "La concentración no baja en proporción lineal: se reduce a la mitad en cada vida media."),
        ("0 mg/L", False, "La concentración se reduce a la mitad en cada vida media, pero nunca llega exactamente a cero."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Un bucle `for` aplica la misma operación a cada elemento de una serie.
- Los acumuladores y contadores se inicializan antes del bucle y se actualizan dentro.
- Un bucle con un `if` dentro detecta valores de alarma y calcula proporciones como la prevalencia.
- `while` repite mientras se cumpla una condición; dentro, algo debe cambiar para que termine.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Bucle | Estructura que repite un bloque de instrucciones |
| Iteración | Cada una de las vueltas de un bucle |
| Acumulador | Variable que va sumando valores en cada iteración |
| Contador | Variable que cuenta cuántas veces se cumple una condición |
| Bucles anidados | Un bucle dentro de otro |
| Prevalencia | Proporción de individuos con una condición en un momento dado |
| Vida media | Tiempo que tarda la concentración de un fármaco en reducirse a la mitad |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial de Python: la sentencia for y la función range()](https://docs.python.org/es/3/tutorial/controlflow.html#for-statements)
- [Tutorial de Python: listas por comprensión](https://docs.python.org/es/3/tutorial/datastructures.html#list-comprehensions)
""")

c.pie(40)
print(c.guardar("../cuadernos"))
