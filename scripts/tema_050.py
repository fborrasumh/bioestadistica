from plantilla import Cuaderno

c = Cuaderno("Tema_050_Funciones_indices_y_escalas_clinicas.ipynb")

c.cabecera(
    50,
    "Funciones en Python para la implementación de índices y escalas clínicas",
    "Módulo 2. Programando con IA",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Definir funciones con `def`, parámetros y valor de retorno.
2. Documentar una función para que otra persona sepa qué hace, qué recibe y qué devuelve.
3. Implementar índices y escalas clínicas como funciones reutilizables.
4. Usar parámetros con valor por defecto y llamadas por nombre.
5. Comprobar una función con **casos de prueba** (`assert`) antes de confiar en ella, sea tuya o del asistente de IA.
6. Rechazar valores de entrada imposibles en lugar de devolver un resultado absurdo.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: escalas clínicas como funciones | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
**Rosa**, de 78 años (paciente sintética), acude a Urgencias con palpitaciones. El electrocardiograma muestra una **fibrilación auricular** no conocida. Es hipertensa y diabética, sin ictus previos ni enfermedad vascular. Pesa 58 kg y su creatinina sérica es de 1,3 mg/dL.

El médico necesita dos cálculos para decidir el tratamiento:

1. La escala **CHA₂DS₂-VASc**, que estima el riesgo de ictus y orienta la anticoagulación.
2. El **aclaramiento de creatinina**, porque la dosis de varios anticoagulantes depende de la función renal.

Estos cálculos se repiten cada día con cientos de pacientes. Escribirlos una sola vez, comprobarlos bien y reutilizarlos es justo lo que permite una **función**. Y si el asistente de IA escribe la función por nosotros, necesitamos una manera de **comprobar** que la ha escrito bien.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Qué es una función")
c.md("""
Una **función** es un bloque de código con nombre que recibe datos (**parámetros**), hace un cálculo y devuelve un resultado (**valor de retorno**). Ya has usado funciones de Python: `print()`, `len()`, `round()`, `max()`. Ahora escribirás las tuyas.

```python
def nombre_de_la_funcion(parametro_1, parametro_2):
    \"\"\"Explicación de lo que hace la función.\"\"\"
    resultado = ...
    return resultado
```

| Parte | Para qué sirve |
| --- | --- |
| `def` | Indica que se define una función |
| Parámetros | Los datos que necesita, entre paréntesis |
| *Docstring* (entre triples comillas) | Documenta qué hace, qué recibe y qué devuelve |
| `return` | Devuelve el resultado a quien llamó a la función |

Definir una función **no la ejecuta**: solo la guarda. Se ejecuta al **llamarla**: `imc(68, 1.63)`.
""")
c.titulo(3, "2.2 Por qué usar funciones")
c.md("""
- **Una sola fuente de verdad:** si la fórmula cambia, se corrige en un único sitio.
- **Legibilidad:** `cha2ds2_vasc(...)` se entiende mejor que diez líneas de sumas.
- **Verificación:** una función se puede probar con casos de resultado conocido.
""")
c.titulo(3, "2.3 Casos de prueba")
c.md("""
Un **caso de prueba** compara el resultado de la función con un valor que conocemos de antemano, calculado a mano o tomado de una fuente fiable. La instrucción `assert condición` no hace nada si la condición es verdadera y detiene el programa con `AssertionError` si es falsa.

```python
assert round(imc(68, 1.63), 1) == 25.6
```

Es la herramienta central de este módulo: **ninguna función, propia o generada por IA, se da por buena sin pasar sus casos de prueba**.
""")

c.titulo(2, "3. Demostración: escalas clínicas como funciones (20 min)")
c.titulo(3, "3.1 Una primera función: el IMC")
c.code('''
def imc(peso_kg, talla_m):
    """Calcula el índice de masa corporal.

    Parámetros:
        peso_kg: peso en kilogramos.
        talla_m: talla en metros.
    Devuelve:
        IMC en kg/m².
    """
    return peso_kg / talla_m ** 2


print(f"{imc(68, 1.63):.1f} kg/m²")
print(f"{imc(92, 1.80):.1f} kg/m²")
''')
c.md("""
La documentación de una función se consulta con `help()`:
""")
c.code("""
help(imc)
""")

c.titulo(3, "3.2 Funciones que usan otras funciones")
c.code('''
def categoria_imc(valor_imc):
    """Devuelve la categoría de la OMS para un IMC de adulto."""
    if valor_imc < 18.5:
        return "bajo peso"
    elif valor_imc < 25:
        return "normal"
    elif valor_imc < 30:
        return "sobrepeso"
    else:
        return "obesidad"


def informe_peso(peso_kg, talla_m):
    """Devuelve un texto con el IMC y su categoría."""
    valor = imc(peso_kg, talla_m)
    return f"IMC {valor:.1f} kg/m² ({categoria_imc(valor)})"


print(informe_peso(58, 1.55))
''')

c.titulo(3, "3.3 Casos de prueba")
c.md("""
Los casos de prueba se eligen para comprobar **el cálculo** y **los límites entre categorías**. Si la celda no muestra nada salvo el mensaje final, todas las pruebas se han superado.
""")
c.code("""
assert round(imc(68, 1.63), 1) == 25.6
assert categoria_imc(18.4) == "bajo peso"
assert categoria_imc(18.5) == "normal"
assert categoria_imc(24.9) == "normal"
assert categoria_imc(25.0) == "sobrepeso"
assert categoria_imc(30.0) == "obesidad"
print("Todas las pruebas superadas")
""")

c.titulo(3, "3.4 La escala CHA₂DS₂-VASc")
c.md("""
| Criterio | Puntos |
| --- | --- |
| **C**: insuficiencia cardiaca congestiva | 1 |
| **H**: hipertensión arterial | 1 |
| **A₂**: edad ≥ 75 años | 2 |
| **D**: diabetes mellitus | 1 |
| **S₂**: ictus o accidente isquémico transitorio previo | 2 |
| **V**: enfermedad vascular (infarto previo, arteriopatía periférica, placa aórtica) | 1 |
| **A**: edad de 65 a 74 años | 1 |
| **Sc**: sexo femenino | 1 |

La guía europea de fibrilación auricular de 2024 propone una versión sin el criterio de sexo (CHA₂DS₂-VA). Aquí programamos la clásica, todavía muy citada, y en la práctica se adapta en una línea.

Los criterios ausentes tienen valor por defecto `False`, así que al llamar a la función solo hace falta indicar los presentes, **por su nombre**.
""")
c.code('''
def cha2ds2_vasc(edad, mujer, insuficiencia_cardiaca=False, hipertension=False,
                 diabetes=False, ictus_previo=False, enfermedad_vascular=False):
    """Calcula la escala CHA2DS2-VASc de riesgo de ictus en fibrilación auricular."""
    puntos = 0
    puntos += insuficiencia_cardiaca
    puntos += hipertension
    puntos += diabetes
    puntos += 2 * ictus_previo
    puntos += enfermedad_vascular
    puntos += mujer
    if edad >= 75:
        puntos += 2
    elif edad >= 65:
        puntos += 1
    return puntos


# Rosa: 78 años, mujer, hipertensa y diabética
print("CHA2DS2-VASc de Rosa:", cha2ds2_vasc(78, mujer=True, hipertension=True, diabetes=True))
''')
c.md("""
Rosa suma 5 puntos: 2 por la edad, 1 por la hipertensión, 1 por la diabetes y 1 por ser mujer. Comprobamos la función con casos calculados a mano, incluidos los límites de edad:
""")
c.code("""
assert cha2ds2_vasc(50, mujer=False) == 0
assert cha2ds2_vasc(64, mujer=False) == 0
assert cha2ds2_vasc(65, mujer=False) == 1
assert cha2ds2_vasc(75, mujer=False) == 2
assert cha2ds2_vasc(78, mujer=True, hipertension=True, diabetes=True) == 5
assert cha2ds2_vasc(80, mujer=True, insuficiencia_cardiaca=True, hipertension=True,
                    diabetes=True, ictus_previo=True, enfermedad_vascular=True) == 9
print("Todas las pruebas superadas")
""")

c.titulo(3, "3.5 Aclaramiento de creatinina y validación de los datos")
c.md("""
La fórmula de **Cockcroft-Gault** estima el aclaramiento de creatinina:

$$\\text{ClCr (mL/min)} = \\frac{(140 - \\text{edad}) \\times \\text{peso (kg)}}{72 \\times \\text{creatinina (mg/dL)}} \\times 0{,}85 \\text{ si es mujer}$$

Una función clínica no debe devolver un resultado absurdo si recibe un dato imposible. Con `raise ValueError(...)` la función **se niega a calcular** y explica por qué.
""")
c.code('''
def cockcroft_gault(edad, peso_kg, creatinina_mg_dl, mujer):
    """Aclaramiento de creatinina (mL/min) según Cockcroft-Gault."""
    if creatinina_mg_dl <= 0:
        raise ValueError("La creatinina debe ser mayor que 0 mg/dL")
    if not 18 <= edad <= 120:
        raise ValueError("La fórmula está validada en adultos")
    aclaramiento = (140 - edad) * peso_kg / (72 * creatinina_mg_dl)
    if mujer:
        aclaramiento *= 0.85
    return aclaramiento


print(f"Aclaramiento de Rosa: {cockcroft_gault(78, 58, 1.3, mujer=True):.0f} mL/min")
''')
c.code("""
assert round(cockcroft_gault(60, 72, 1.0, mujer=False)) == 80
assert round(cockcroft_gault(60, 72, 1.0, mujer=True)) == 68

try:
    cockcroft_gault(70, 70, 0, mujer=False)
except ValueError as error:
    print("Dato rechazado:", error)
""")
c.md("""
**Comprobación a mano del primer caso:** (140 − 60) × 72 / (72 × 1,0) = 80 mL/min; en una mujer, 80 × 0,85 = 68 mL/min.
""")

c.titulo(3, "3.6 Verificar una función escrita por el asistente")
c.md("""
Supón que pides al asistente de IA: *«Escribe en Python una función que calcule la presión arterial media a partir de la sistólica y la diastólica»* y te devuelve esto:
""")
c.code('''
def presion_arterial_media(pas, pad):
    """Presión arterial media (versión propuesta por un asistente)."""
    return (pas + pad) / 2
''')
c.md("""
El código funciona sin errores, pero ¿es correcto? Lo comprobamos con un caso conocido: con 120/80 mmHg, la PAM aproximada es 80 + (120 − 80) / 3 = 93,3 mmHg. Quita el `#` de la última línea para ejecutar la prueba.
""")
c.code("""
resultado = presion_arterial_media(120, 80)
print(f"Resultado de la función: {resultado:.1f} mmHg")
# assert round(resultado, 1) == 93.3
""")
c.md("""
La función devuelve 100 mmHg: calcula la **media aritmética** de las dos cifras, no la presión arterial media fisiológica, que pondera más la diastólica porque el corazón pasa más tiempo en diástole. **El código se ejecutaba sin error y el resultado era clínicamente incorrecto.** Solo el caso de prueba lo ha descubierto. La versión correcta:
""")
c.code('''
def presion_arterial_media(pas, pad):
    """Presión arterial media aproximada: PAD + (PAS - PAD) / 3."""
    return pad + (pas - pad) / 3


assert round(presion_arterial_media(120, 80), 1) == 93.3
print("Prueba superada")
''')

c.titulo(3, "Ampliación: filtrado glomerular estimado (CKD-EPI 2021)")
c.md("""
La ecuación CKD-EPI de 2021, sin coeficiente racial, es la recomendada actualmente para estimar el filtrado glomerular:

$$\\text{FGe} = 142 \\times \\min\\left(\\frac{Cr}{\\kappa}, 1\\right)^{\\alpha} \\times \\max\\left(\\frac{Cr}{\\kappa}, 1\\right)^{-1{,}200} \\times 0{,}9938^{\\text{edad}} \\times 1{,}012 \\text{ si es mujer}$$

con κ = 0,7 y α = −0,241 en mujeres, y κ = 0,9 y α = −0,302 en varones. La creatinina (Cr) se expresa en mg/dL y el resultado en mL/min/1,73 m².
""")
c.code('''
def fge_ckd_epi_2021(creatinina_mg_dl, edad, mujer):
    """Filtrado glomerular estimado (mL/min/1,73 m²), ecuación CKD-EPI 2021."""
    kappa = 0.7 if mujer else 0.9
    alfa = -0.241 if mujer else -0.302
    cociente = creatinina_mg_dl / kappa
    fge = 142 * min(cociente, 1) ** alfa * max(cociente, 1) ** -1.200 * 0.9938 ** edad
    if mujer:
        fge *= 1.012
    return fge


print(f"FGe de Rosa: {fge_ckd_epi_2021(1.3, 78, mujer=True):.0f} mL/min/1,73 m²")
''')
c.md("""
Cuando no se dispone de valores de referencia publicados, se pueden comprobar **propiedades** que la función debe cumplir: a más creatinina, menos filtrado; a más edad, menos filtrado.
""")
c.code("""
assert fge_ckd_epi_2021(2.0, 60, mujer=False) < fge_ckd_epi_2021(1.0, 60, mujer=False)
assert fge_ckd_epi_2021(1.0, 80, mujer=False) < fge_ckd_epi_2021(1.0, 40, mujer=False)
print("Propiedades comprobadas")
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Olvidar `return`.** Una función sin `return` devuelve `None`; el error aparece después, al usar ese `None` en un cálculo.

**Confundir `print` con `return`.** `print` muestra un valor en pantalla; `return` lo entrega para usarlo en otros cálculos.

**Cambiar el orden de los parámetros.** `imc(1.63, 68)` da 0,0004 kg/m² sin ningún error. Llamar por nombre (`imc(peso_kg=68, talla_m=1.63)`) lo evita.

**Variables locales.** Las variables creadas dentro de una función no existen fuera de ella.

**Confiar en código que «funciona».** Que una función se ejecute sin errores no significa que sea correcta, como se ha visto con la presión arterial media.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 50 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** completar la función de superficie corporal de Mosteller y escribir sus casos de prueba.
2. **Misión clínica (con pistas):** programar la escala CURB-65 como función y comprobar sus valores frontera.
3. **Misión reto (con asistente):** pedir al asistente la escala de Glasgow como función, escribir tú los casos de prueba y corregir lo que falle.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Qué devuelve una función que calcula un resultado y lo muestra con print, pero no tiene return?", [
        ("None", True, "Correcto: sin return, una función devuelve None aunque haya mostrado algo en pantalla."),
        ("El último valor calculado", False, "Python no devuelve automáticamente el último cálculo."),
        ("El texto mostrado por print", False, "print solo muestra; no entrega el valor."),
        ("Un error", False, "No hay error al llamarla; el problema aparece al usar el resultado."),
    ]),
    ("Un varón de 70 años es hipertenso y tuvo un ictus hace dos años. ¿Cuál es su CHA₂DS₂-VASc?", [
        ("4", True, "Correcto: 1 por la edad (65 a 74), 1 por la hipertensión y 2 por el ictus previo."),
        ("3", False, "El ictus previo suma 2 puntos, no 1."),
        ("5", False, "Con 70 años la edad suma 1 punto, no 2."),
        ("2", False, "Revisa cuántos criterios cumple."),
    ]),
    ("¿Qué ocurre al ejecutar assert round(imc(68, 1.63), 1) == 25.6 si la función es correcta?", [
        ("Nada: la ejecución continúa sin mensajes", True, "Correcto: assert solo interrumpe cuando la condición es falsa."),
        ("Se muestra True", False, "assert no muestra nada si la condición se cumple."),
        ("Se muestra el IMC", False, "assert no imprime el valor comprobado."),
        ("Se produce AssertionError", False, "Eso ocurre solo si la condición es falsa."),
    ]),
    ("El asistente propone una función que se ejecuta sin errores. ¿Qué debes hacer antes de usarla?", [
        ("Comprobarla con casos de prueba de resultado conocido", True, "Correcto: que se ejecute no significa que el cálculo sea correcto."),
        ("Nada, si no hay errores es correcta", False, "La función de presión arterial media del apartado 3.6 se ejecutaba sin error y era incorrecta."),
        ("Pedir al asistente que confirme que es correcta", False, "El asistente puede confirmar con seguridad un error."),
        ("Ejecutarla dos veces", False, "Repetir la ejecución da el mismo resultado, correcto o no."),
    ]),
    ("¿Por qué conviene que cockcroft_gault() lance un ValueError si la creatinina es 0?", [
        ("Para no devolver un resultado absurdo con un dato imposible", True, "Correcto: es mejor detenerse y explicar el problema que calcular algo sin sentido."),
        ("Porque Python no permite dividir entre números pequeños", False, "El problema es dividir entre cero, y además el dato es clínicamente imposible."),
        ("Para que la función sea más rápida", False, "La validación no tiene que ver con la velocidad."),
        ("Porque assert no funciona con ceros", False, "assert y raise son herramientas distintas."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Una función encapsula un cálculo clínico: se escribe una vez, se documenta y se reutiliza.
- `return` entrega el resultado; `print` solo lo muestra.
- Los parámetros con valor por defecto y las llamadas por nombre hacen las escalas más legibles y seguras.
- **Ninguna función se usa sin pasar sus casos de prueba**, y menos si la ha escrito un asistente de IA.
- Ante datos imposibles, la función debe negarse a calcular.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Función | Bloque de código con nombre que recibe parámetros y devuelve un resultado |
| Parámetro | Dato que recibe una función |
| Valor de retorno | Resultado que entrega una función con `return` |
| *Docstring* | Texto de documentación al inicio de una función |
| Valor por defecto | Valor que toma un parámetro si no se indica al llamar a la función |
| Caso de prueba | Comprobación de que una función da el resultado esperado en un caso conocido |
| `assert` | Instrucción que detiene el programa si una condición es falsa |
| `raise` | Instrucción que lanza un error de forma deliberada |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial de Python: definir funciones](https://docs.python.org/es/3/tutorial/controlflow.html#defining-functions)
- Cockcroft DW, Gault MH. Prediction of creatinine clearance from serum creatinine. *Nephron*. 1976;16(1):31-41.
- Inker LA, *et al.* New creatinine- and cystatin C-based equations to estimate GFR without race. *N Engl J Med*. 2021;385(19):1737-1749.
- Lip GY, *et al.* Refining clinical risk stratification for predicting stroke and thromboembolism in atrial fibrillation using a novel risk factor-based approach: the Euro Heart Survey on Atrial Fibrillation. *Chest*. 2010;137(2):263-272.
""")

c.pie(50)
print(c.guardar("../cuadernos"))
