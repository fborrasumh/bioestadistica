from plantilla import Cuaderno

c = Cuaderno("Tema_090_Programacion_asistida_por_IA_y_mejora_recursiva.ipynb")

c.cabecera(
    90,
    "Programación asistida por inteligencia artificial: ciclo de mejora recursiva de generación, verificación y corrección",
    "Módulo 3. Procesado inicial de datos",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Requisito:** Temas 50 (funciones y casos de prueba) y 80 (API). Sin clave, el cuaderno funciona con respuestas simuladas.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Describir el ciclo de **mejora recursiva**: generar, ejecutar, verificar y corregir.
2. Escribir una **especificación** y sus **casos de prueba** antes de pedir código a un modelo de IA.
3. Programar un bucle que pide código al modelo, lo prueba y le devuelve los fallos. El bucle para cuando se superan las pruebas o se agotan los intentos.
4. Registrar cada iteración del ciclo para poder analizarla después.
5. Explicar por qué superar las pruebas no garantiza que el código sea correcto (ley de Goodhart).
6. Aplicar las medidas de seguridad necesarias antes de ejecutar código generado por IA.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: un ciclo de mejora recursiva | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
El servicio de Urgencias quiere que la historia clínica calcule automáticamente la escala **CURB-65** de gravedad de la neumonía adquirida en la comunidad. La escala suma un punto por cada criterio:

| Criterio | Punto si… |
| --- | --- |
| **C**onfusión | Desorientación de nueva aparición |
| **U**rea | Urea > 7 mmol/L |
| Frecuencia **R**espiratoria | ≥ 30 rpm |
| Presión arterial (**B**lood pressure) | PAS < 90 mmHg **o** PAD ≤ 60 mmHg |
| Edad **65** | ≥ 65 años |

Un residente pide al asistente de IA la función. El código se ejecuta sin errores. Pero con una paciente de 65 años y PAD de 60 mmHg, la función da 0 puntos en lugar de 2. El asistente escribió `edad > 65` y `pad < 60`.

En el Tema 50 aprendimos a descubrir estos errores con casos de prueba. Hoy damos el paso siguiente: **devolver los fallos al modelo** para que corrija su propio código, y repetirlo hasta que todo funcione. Es el **ciclo de mejora recursiva**, la forma en que hoy se programa con IA.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 El ciclo de mejora recursiva")
c.md("""
```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ 1. GENERAR   │ ──▶ │ 2. EJECUTAR  │ ──▶ │ 3. VERIFICAR │
  │ el modelo    │     │ el código    │     │ con pruebas  │
  │ escribe      │     │              │     │              │
  └──────────────┘     └──────────────┘     └──────┬───────┘
         ▲                                         │
         │        ¿fallos? → 4. CORREGIR           │
         └──────── se devuelven los fallos ◀───────┘
                   al modelo

  Se detiene cuando se superan todas las pruebas o se agotan los intentos.
```

Lo que hace que el ciclo funcione no es el modelo, sino la **calidad del criterio de verificación**. Un modelo excelente con pruebas pobres produce código que parece correcto y no lo es.
""")
c.titulo(3, "2.2 Primero la especificación y las pruebas")
c.md("""
El orden correcto, que en ingeniería del software se llama **desarrollo guiado por pruebas**:

1. Escribir la **especificación**: qué recibe la función, qué devuelve y con qué reglas.
2. Escribir los **casos de prueba** a partir de fuentes fiables, antes de ver ningún código.
3. Solo entonces pedir el código.

Si las pruebas se escriben después de ver el código, se tiende a escribir pruebas que ese código ya supera.
""")
c.titulo(3, "2.3 Criterios de parada")
c.diagrama('Flujo del ciclo: generar, probar; si todo pasa, fin; si se agotan los intentos o se repite el código, revisar a mano; si no, devolver los fallos.')
c.md("""
| Criterio | Para qué sirve |
| --- | --- |
| Todas las pruebas superadas | Objetivo del ciclo |
| Número máximo de intentos | Evita bucles infinitos y gasto de cuota |
| El modelo repite el mismo código | Señal de que no sabe corregirlo con la información dada |
""")
c.titulo(3, "2.4 La ley de Goodhart")
c.md("""
*«Cuando una medida se convierte en objetivo, deja de ser una buena medida.»* Supón que el único objetivo del ciclo es superar las pruebas. Entonces el código las superará. Pero puede fallar en los casos que las pruebas no cubren. Por eso:

- Las pruebas deben cubrir los **valores frontera** de cada criterio.
- Conviene guardar algunas pruebas **reservadas** que el modelo no ve, para comprobar al final. Volveremos sobre esta idea en el Módulo 5.
""")
c.titulo(3, "2.5 Seguridad")
c.md("""
Ejecutar código generado por IA es ejecutar código de un desconocido:

- **Leer el código antes de ejecutarlo**, aunque sea por encima.
- Ejecutarlo en un entorno aislado, como Colab, nunca en un ordenador con datos sensibles.
- No pedir código que acceda a ficheros, a internet o a Drive si la tarea no lo necesita.
- Nunca incluir datos de pacientes en la especificación ni en las pruebas.
""")

c.titulo(2, "3. Demostración: un ciclo de mejora recursiva (20 min)")
c.titulo(3, "3.1 Conexión con el modelo")
c.conexion_ia()

c.titulo(3, "3.2 La especificación")
c.code('''
ESPECIFICACION = """
Escribe en Python una función llamada curb65 con estos parámetros:
- confusion (bool): desorientación de nueva aparición
- urea_mmol_l (float): urea sérica en mmol/L
- fr_rpm (int): frecuencia respiratoria en respiraciones por minuto
- pas_mmHg (int): presión arterial sistólica
- pad_mmHg (int): presión arterial diastólica
- edad (int): edad en años

Devuelve un entero de 0 a 5 sumando un punto por cada criterio:
- confusión presente
- urea > 7 mmol/L
- frecuencia respiratoria >= 30
- presión sistólica < 90 o presión diastólica <= 60
- edad >= 65

Devuelve solo el código de la función, dentro de un bloque ```python```, sin ejemplos de uso.
"""
''')

c.titulo(3, "3.3 Los casos de prueba, escritos antes que el código")
c.md("""
Cada caso indica los datos de entrada y el resultado esperado, calculado a mano. Hay casos para **cada criterio** y para **cada valor frontera**: 7 frente a 7,1 mmol/L, 29 frente a 30 rpm, 90 mmHg de PAS, 60 mmHg de PAD y 64 frente a 65 años.
""")
c.code("""
base = dict(confusion=False, urea_mmol_l=5.0, fr_rpm=18, pas_mmHg=130, pad_mmHg=80, edad=50)

PRUEBAS = [
    (base, 0),
    ({**base, "confusion": True}, 1),
    ({**base, "urea_mmol_l": 7.0}, 0),
    ({**base, "urea_mmol_l": 7.1}, 1),
    ({**base, "fr_rpm": 29}, 0),
    ({**base, "fr_rpm": 30}, 1),
    ({**base, "pas_mmHg": 90}, 0),
    ({**base, "pas_mmHg": 89}, 1),
    ({**base, "pad_mmHg": 61}, 0),
    ({**base, "pad_mmHg": 60}, 1),
    ({**base, "edad": 64}, 0),
    ({**base, "edad": 65}, 1),
    ({**base, "edad": 65, "pad_mmHg": 60}, 2),
    (dict(confusion=True, urea_mmol_l=9.0, fr_rpm=32, pas_mmHg=85, pad_mmHg=50, edad=80), 5),
]
print(len(PRUEBAS), "casos de prueba")
""")
c.md("""
La sintaxis `{**base, "edad": 65}` crea una copia del diccionario `base` cambiando solo la edad.
""")

c.titulo(3, "3.4 Ejecutar y verificar el código generado")
c.code('''
def verificar(codigo):
    """Ejecuta el código en un espacio aislado y devuelve la lista de fallos."""
    espacio = {}
    try:
        exec(codigo, espacio)
        funcion = espacio["curb65"]
    except Exception as error:
        return [f"El código no se puede ejecutar: {type(error).__name__}: {error}"]

    fallos = []
    for entrada, esperado in PRUEBAS:
        try:
            obtenido = funcion(**entrada)
        except Exception as error:
            fallos.append(f"Con {entrada} se produce {type(error).__name__}")
            continue
        if obtenido != esperado:
            fallos.append(f"Con {entrada} se esperaba {esperado} y se obtuvo {obtenido}")
    return fallos
''')

c.titulo(3, "3.5 Generar código: con el modelo o simulado")
c.md("""
Si hay conexión, se pide el código al modelo, añadiendo el código anterior y sus fallos cuando los hay. Sin conexión, se usan tres versiones simuladas que reproducen errores habituales de los asistentes.
""")
c.code('''
import re

VERSIONES_SIMULADAS = [
    """def curb65(confusion, urea_mmol_l, fr_rpm, pas_mmHg, pad_mmHg, edad):
    puntos = confusion + (urea_mmol_l > 7) + (fr_rpm >= 30)
    puntos += (pas_mmHg < 90 or pad_mmHg < 60) + (edad > 65)
    return puntos""",
    """def curb65(confusion, urea_mmol_l, fr_rpm, pas_mmHg, pad_mmHg, edad):
    puntos = confusion + (urea_mmol_l > 7) + (fr_rpm >= 30)
    puntos += (pas_mmHg < 90 or pad_mmHg < 60) + (edad >= 65)
    return puntos""",
    """def curb65(confusion, urea_mmol_l, fr_rpm, pas_mmHg, pad_mmHg, edad):
    puntos = int(confusion) + (urea_mmol_l > 7) + (fr_rpm >= 30)
    puntos += (pas_mmHg < 90 or pad_mmHg <= 60) + (edad >= 65)
    return int(puntos)""",
]


def generar(codigo_anterior, fallos, intento):
    """Devuelve el código de la función: del modelo o de las versiones simuladas."""
    if cliente is None:
        return VERSIONES_SIMULADAS[min(intento - 1, len(VERSIONES_SIMULADAS) - 1)]
    prompt = ESPECIFICACION
    if codigo_anterior:
        prompt += (
            "\\nTu versión anterior era:\\n```python\\n" + codigo_anterior + "\\n```\\n"
            "Falla en estos casos de prueba:\\n- " + "\\n- ".join(fallos)
            + "\\nCorrige la función."
        )
    texto = preguntar(prompt, temperatura=0.2)
    bloque = re.search(r"```(?:python)?\\n(.*?)```", texto, re.DOTALL)
    return bloque.group(1).strip() if bloque else texto.strip()
''')

c.titulo(3, "3.6 El ciclo completo")
c.code("""
MAX_INTENTOS = 5
registro = []
codigo, fallos = None, []

for intento in range(1, MAX_INTENTOS + 1):
    codigo = generar(codigo, fallos, intento)
    fallos = verificar(codigo)
    registro.append({"intento": intento, "pruebas_falladas": len(fallos),
                     "pruebas_superadas": len(PRUEBAS) - len(fallos)})
    print(f"Intento {intento}: {len(PRUEBAS) - len(fallos)} de {len(PRUEBAS)} pruebas superadas")
    for fallo in fallos[:3]:
        print("   ·", fallo)
    if not fallos:
        print("\\nTodas las pruebas superadas. Código final:\\n")
        print(codigo)
        break
else:
    print("\\nSe agotaron los intentos sin superar todas las pruebas: revisar a mano.")
""")
c.md("""
La construcción `for … else` ejecuta el bloque `else` solo si el bucle termina **sin** pasar por `break`, es decir, si se agotan los intentos.
""")

c.titulo(3, "3.7 El registro del ciclo")
c.md("""
Registrar cada iteración permite analizar el ciclo: cuántos intentos hicieron falta y cómo evolucionaron los fallos. En el Módulo 5 compararemos así, con métodos estadísticos, distintas formas de pedir código al modelo.
""")
c.code("""
import pandas as pd
import matplotlib.pyplot as plt

tabla = pd.DataFrame(registro)
print(tabla.to_string(index=False))

plt.figure(figsize=(6, 3.5))
plt.plot(tabla["intento"], tabla["pruebas_superadas"], marker="o")
plt.axhline(len(PRUEBAS), linestyle="--", color="gray", label="Total de pruebas")
plt.xlabel("Intento")
plt.ylabel("Pruebas superadas")
plt.xticks(tabla["intento"])
plt.ylim(0, len(PRUEBAS) + 1)
plt.title("Evolución del ciclo de mejora recursiva")
plt.legend()
plt.show()
""")

c.titulo(3, "3.8 Goodhart en acción: pruebas insuficientes")
c.md("""
¿Qué habría pasado con pruebas pobres, sin valores frontera? La primera versión simulada, con dos errores, las habría superado todas:
""")
c.code("""
PRUEBAS_COMPLETAS = PRUEBAS
PRUEBAS = [
    (base, 0),
    ({**base, "confusion": True}, 1),
    (dict(confusion=True, urea_mmol_l=9.0, fr_rpm=32, pas_mmHg=85, pad_mmHg=50, edad=80), 5),
]
print("Fallos con pruebas pobres:", len(verificar(VERSIONES_SIMULADAS[0])))

PRUEBAS = PRUEBAS_COMPLETAS
print("Fallos con pruebas completas:", len(verificar(VERSIONES_SIMULADAS[0])))
""")
c.md("""
**Con pruebas pobres, el ciclo habría terminado en el primer intento con un código erróneo.** Una paciente de 65 años con PAD de 60 mmHg habría recibido 0 puntos en lugar de 2. La calidad del ciclo es la calidad de sus pruebas.
""")

c.titulo(3, "Ampliación: pruebas reservadas")
c.md("""
Para protegerte frente a Goodhart, separa las pruebas en dos grupos. El primero se devuelve al modelo durante el ciclo. El segundo son **pruebas reservadas**, que solo se usan al final. Si el código supera las primeras pero falla en las reservadas, el ciclo ha aprendido a aprobar el examen. No ha aprendido a resolver el problema.
""")
c.code("""
PRUEBAS_RESERVADAS = [
    (dict(confusion=False, urea_mmol_l=7.5, fr_rpm=30, pas_mmHg=88, pad_mmHg=58, edad=70), 4),
    (dict(confusion=True, urea_mmol_l=6.9, fr_rpm=22, pas_mmHg=95, pad_mmHg=62, edad=40), 1),
]

espacio = {}
exec(codigo, espacio)
for entrada, esperado in PRUEBAS_RESERVADAS:
    obtenido = espacio["curb65"](**entrada)
    print("correcto" if obtenido == esperado else "FALLO", "·", entrada, "→", obtenido)
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Escribir las pruebas después de ver el código:** se acaban escribiendo pruebas que ese código ya supera.

**No poner límite de intentos:** el ciclo puede gastar toda la cuota de la API.

**Ejecutar el código generado sin leerlo.**

**Devolver al modelo solo «está mal»:** sin indicar qué casos fallan y por qué, el modelo no tiene información para corregir.

**Dar por correcta una función porque supera las pruebas:** solo es correcta en lo que las pruebas comprueban.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 90 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** identificar qué valores frontera faltan en un conjunto de casos de prueba.
2. **Misión clínica (con pistas):** escribir la especificación y las pruebas de la escala de Wells para trombosis venosa profunda.
3. **Misión reto (con asistente):** ejecutar el ciclo de mejora recursiva para esa escala. Registrar las iteraciones y comprobar el resultado con pruebas reservadas.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Cuál es el orden correcto para programar con un asistente de IA?", [
        ("Especificación, casos de prueba, generación del código y verificación", True, "Correcto: las pruebas se escriben antes de ver el código."),
        ("Generación del código, casos de prueba y verificación", False, "Si las pruebas se escriben después, se adaptan al código que ya existe."),
        ("Generación del código y uso directo si no da errores", False, "Ejecutarse sin errores no significa ser correcto."),
        ("Casos de prueba, uso directo y especificación", False, "La especificación es lo primero: define qué se quiere."),
    ]),
    ("Una función CURB-65 usa edad > 65. ¿Qué caso de prueba descubre el error?", [
        ("Un paciente de exactamente 65 años", True, "Correcto: el valor frontera es el que distingue > de >=."),
        ("Un paciente de 80 años", False, "Con 80 años, > 65 y >= 65 dan el mismo resultado."),
        ("Un paciente de 40 años", False, "Con 40 años, ninguna de las dos versiones suma el punto."),
        ("Ningún caso puede descubrirlo", False, "El caso frontera lo descubre."),
    ]),
    ("¿Qué información conviene devolver al modelo cuando su código falla?", [
        ("Los casos concretos que fallan, con el resultado esperado y el obtenido", True, "Correcto: es la información que permite corregir."),
        ("Solo «está mal, inténtalo otra vez»", False, "Sin saber qué falla, el modelo no tiene en qué basarse."),
        ("Las pruebas reservadas", False, "Las reservadas no se enseñan al modelo: sirven para la comprobación final."),
        ("Los datos de un paciente real con el que falló", False, "Nunca se envían datos de pacientes."),
    ]),
    ("Un ciclo de mejora recursiva supera todas sus pruebas en el primer intento. ¿Qué puedes concluir?", [
        ("Que el código es correcto en lo que comprueban las pruebas, y nada más", True, "Correcto: la garantía depende de la calidad de las pruebas."),
        ("Que el código es correcto en cualquier caso", False, "Las pruebas pobres del apartado 3.8 dejaban pasar dos errores."),
        ("Que el modelo no necesitaba pruebas", False, "Sin pruebas no habría forma de saberlo."),
        ("Que hay que aumentar la temperatura", False, "La temperatura no tiene que ver con la validez de las pruebas."),
    ]),
    ("¿Por qué se fija un número máximo de intentos?", [
        ("Para que el ciclo termine aunque el modelo no consiga corregir el código", True, "Correcto: evita bucles infinitos y gasto de cuota."),
        ("Porque el modelo empeora a partir del tercer intento", False, "No hay una regla fija; depende del problema."),
        ("Porque Python no permite más de cinco iteraciones", False, "Python no impone ese límite."),
        ("Para que el código sea más rápido", False, "El límite no afecta a la velocidad del código final."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- El ciclo de mejora recursiva genera código, lo ejecuta y lo verifica con pruebas. Devuelve los fallos al modelo hasta que se superan las pruebas o se agotan los intentos.
- La especificación y las pruebas se escriben **antes** del código, con atención a los valores frontera.
- Superar las pruebas solo garantiza lo que las pruebas comprueban (ley de Goodhart); las pruebas reservadas ayudan a detectarlo.
- El código generado por IA se lee antes de ejecutarlo, en un entorno aislado y sin datos de pacientes.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Mejora recursiva | Ciclo en el que un modelo corrige su propia salida a partir de una verificación externa |
| Especificación | Descripción precisa de lo que debe hacer una función |
| Desarrollo guiado por pruebas | Forma de programar en la que las pruebas se escriben antes que el código |
| Criterio de parada | Condición que detiene un ciclo iterativo |
| Ley de Goodhart | Cuando una medida se convierte en objetivo, deja de ser una buena medida |
| Pruebas reservadas | Casos que no se usan durante el ciclo y sirven para la comprobación final |
| `exec()` | Función de Python que ejecuta código contenido en una cadena de texto |
""")

c.titulo(2, "Para saber más")
c.md("""
- Lim WS, *et al.* Defining community acquired pneumonia severity on presentation to hospital: an international derivation and validation study. *Thorax*. 2003;58(5):377-382. doi:[10.1136/thorax.58.5.377](https://doi.org/10.1136/thorax.58.5.377)
- [Tutorial de Python: errores y excepciones](https://docs.python.org/es/3/tutorial/errors.html)
""")

c.pie(90)
print(c.guardar("../cuadernos"))
