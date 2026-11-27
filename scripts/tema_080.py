from plantilla import Cuaderno

c = Cuaderno("Tema_080_Modelos_de_lenguaje_funcionamiento_limitaciones_y_API.ipynb")

c.cabecera(
    80,
    "Fundamentos de los modelos de lenguaje de gran tamaño: funcionamiento, limitaciones y uso seguro mediante API",
    "Módulo 2. Programando con IA",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Requisito:** tener una clave de acceso guardada en Secretos (Tema 10, ampliación). Sin clave, el cuaderno funciona con respuestas de ejemplo.\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Explicar cómo genera texto un modelo de lenguaje de gran tamaño (LLM): tokens y predicción probabilística de la siguiente palabra.
2. Describir el efecto de la **temperatura** sobre las respuestas.
3. Identificar las principales limitaciones de los LLM: alucinaciones, fecha de corte, variabilidad y sesgos.
4. Enviar una petición a un modelo mediante su **API** desde Python, con la clave guardada en Secretos.
5. Pedir una respuesta en formato JSON y comprobarla antes de usarla.
6. Calcular el consumo de tokens de una petición.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: de la probabilidad a la API | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un estudiante de sexto curso prepara una sesión clínica sobre el tratamiento de la hiponatremia. Pide a un asistente de IA «las cinco referencias más importantes, con su DOI». El asistente responde al instante con cinco artículos bien formateados: autores, revista, año, volumen y DOI.

Al buscarlos, dos no existen. Los autores son reales, las revistas también, pero esos artículos nunca se publicaron. Un tercero existe, pero no dice lo que el asistente afirma.

El asistente no ha «mentido». Ha hecho exactamente aquello para lo que está construido: **generar el texto más probable** después de la pregunta. Una referencia bibliográfica plausible es un texto muy probable, exista o no. Entender cómo funciona un modelo de lenguaje es la mejor protección frente a sus errores.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Cómo genera texto un LLM")
c.md("""
Un **modelo de lenguaje de gran tamaño** (LLM, *large language model*) es una red neuronal entrenada con enormes cantidades de texto. Su tarea parece simple: **predecir el siguiente fragmento de texto**.

1. El texto se divide en **tokens**: palabras, partes de palabras o signos. En español, una palabra equivale de media a algo más de un token.
2. Para cada posición, el modelo calcula una **distribución de probabilidad** sobre todos los tokens posibles.
3. Se **elige** un token según esas probabilidades, se añade al texto y se repite el proceso.

Así, tras «El paciente refiere dolor torácico de características…», el token «opresivas» tendrá una probabilidad alta, y «azules», una muy baja. El modelo no consulta una base de datos ni comprueba hechos: **genera lo probable**.
""")
c.titulo(3, "2.2 La temperatura")
c.md("""
La **temperatura** controla cómo se elige el siguiente token:

| Temperatura | Efecto | Uso |
| --- | --- | --- |
| Baja (cercana a 0) | Casi siempre elige el token más probable: respuestas estables y repetitivas | Extraer datos, clasificar, generar código |
| Media (alrededor de 1) | Respeta las probabilidades del modelo | Uso general |
| Alta (mayor de 1) | Da más oportunidades a tokens poco probables: más variedad y más errores | Generar ideas |

Por eso **la misma pregunta puede recibir respuestas distintas**. En el Tema 190 mediremos esa variabilidad con métodos estadísticos.
""")
c.titulo(3, "2.3 Limitaciones")
c.diagrama('Seis limitaciones (alucinación, fecha de corte, variabilidad, sesgos, complacencia, cálculo poco fiable) llevan a una regla: toda respuesta se verifica.')
c.md("""
| Limitación | Qué significa | Ejemplo clínico |
| --- | --- | --- |
| **Alucinación** | Genera información falsa con aspecto convincente | Referencias, dosis o estudios inexistentes |
| **Fecha de corte** | Solo conoce lo que había en sus datos de entrenamiento | Desconoce una guía clínica publicada después |
| **Variabilidad** | La misma pregunta da respuestas distintas | Dos explicaciones contradictorias de una prueba |
| **Sesgos** | Reproduce los sesgos de los textos con que se entrenó | Peor rendimiento en poblaciones infrarrepresentadas |
| **Complacencia** | Tiende a dar la razón a quien pregunta | Confirma un diagnóstico erróneo sugerido en la pregunta |
| **Cálculo poco fiable** | Predice texto, no calcula | Errores en operaciones con varios pasos |

La regla de la asignatura se deriva de todo esto: **toda respuesta se verifica**.
""")
c.titulo(3, "2.4 Qué es una API")
c.md("""
Una **API** (*application programming interface*) permite que un programa use un servicio de otro. Usar un LLM por su API consiste en:

1. Enviar una **petición** con la pregunta (*prompt*), el modelo elegido y parámetros como la temperatura.
2. Identificarse con la **clave de acceso** (API key).
3. Recibir una **respuesta** en JSON (Tema 70) con el texto generado y el número de tokens consumidos.

El coste se mide en **tokens** de entrada (la pregunta) y de salida (la respuesta). En el nivel gratuito no se paga, pero hay un límite de peticiones por minuto y por día.
""")

c.titulo(2, "3. Demostración: de la probabilidad a la API (20 min)")
c.titulo(3, "3.1 Un modelo de juguete: elegir la siguiente palabra")
c.md("""
Simulamos las puntuaciones que un modelo podría asignar a cinco continuaciones posibles de «El paciente refiere dolor torácico de características…». La función **softmax** convierte las puntuaciones en probabilidades, y la temperatura las divide antes.
""")
c.code("""
import numpy as np
import matplotlib.pyplot as plt

candidatos = ["opresivas", "punzantes", "pleuríticas", "mecánicas", "azules"]
puntuaciones = np.array([4.0, 2.5, 2.0, 1.5, -2.0])


def probabilidades(puntuaciones, temperatura):
    \"\"\"Softmax con temperatura: convierte puntuaciones en probabilidades.\"\"\"
    z = puntuaciones / temperatura
    exp_z = np.exp(z - z.max())
    return exp_z / exp_z.sum()


fig, ejes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
for eje, t in zip(ejes, [0.2, 1.0, 2.0]):
    eje.bar(candidatos, probabilidades(puntuaciones, t), color="steelblue")
    eje.set_title(f"Temperatura {t}")
    eje.tick_params(axis="x", rotation=45)
ejes[0].set_ylabel("Probabilidad")
plt.tight_layout()
plt.show()
""")
c.md("""
Con temperatura 0,2, «opresivas» acapara casi toda la probabilidad. Con temperatura 2, incluso «azules» tiene alguna posibilidad. Generamos 10 continuaciones con cada temperatura:
""")
c.code("""
rng = np.random.default_rng(seed=80)
for t in [0.2, 1.0, 2.0]:
    elegidas = rng.choice(candidatos, size=10, p=probabilidades(puntuaciones, t))
    print(f"T = {t}: {', '.join(elegidas)}")
""")

c.titulo(3, "3.2 Preparar la conexión con la API")
c.md("""
Usaremos la API de **Google Gemini** con la biblioteca oficial `google-genai`. La celda lee la clave de Secretos **sin mostrarla**. Si no hay clave, el resto del cuaderno usará respuestas de ejemplo.

El nombre del modelo cambia con el tiempo. Si la petición falla porque el modelo no existe, ejecuta la celda de ampliación «Ver los modelos disponibles». Después, cambia la variable `MODELO`.
""")
c.code("""
%pip install -q google-genai

MODELO = "gemini-2.5-flash"

try:
    from google.colab import userdata
    from google import genai
    from google.genai import types
    cliente = genai.Client(api_key=userdata.get("GEMINI_API_KEY"))
    print("Conexión preparada con el modelo", MODELO)
except Exception as error:
    cliente = None
    print("Sin clave o fuera de Colab: se usarán respuestas de ejemplo.", type(error).__name__)
""")

c.titulo(3, "3.3 Una función para preguntar")
c.md("""
Encapsulamos la petición en una función (Tema 50). Devuelve el texto y el número de tokens consumidos.
""")
c.code('''
def preguntar(prompt, temperatura=0.2):
    """Envía un prompt al modelo y devuelve (texto, tokens_entrada, tokens_salida)."""
    if cliente is None:
        return ("[Sin clave configurada: aquí aparecería la respuesta del modelo]",
                len(prompt.split()), 0)
    respuesta = cliente.models.generate_content(
        model=MODELO,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperatura),
    )
    uso = respuesta.usage_metadata
    return respuesta.text, uso.prompt_token_count, uso.candidates_token_count


texto, entrada, salida = preguntar(
    "Explica en dos frases cómo se calcula la presión arterial media a partir de la "
    "presión sistólica y la diastólica."
)
print(texto)
print(f"\\nTokens: {entrada} de entrada y {salida} de salida")
''')
c.md("""
**Verifica:** ¿coincide la fórmula que da el modelo con la del Tema 10? Compruébalo siempre.
""")

c.titulo(3, "3.4 Pedir una respuesta en JSON y comprobarla")
c.md("""
Para usar la respuesta en un programa, se pide en un formato estructurado. Después se **comprueba** con un caso de resultado conocido, como en el Tema 50. Aquí pedimos una clasificación cuyo resultado sabemos de antemano.
""")
c.code("""
import json

prompt = (
    "Clasifica la presión arterial 148/92 mmHg según la guía ESH 2023. "
    'Responde solo con un JSON con las claves "categoria" y "motivo", sin texto adicional.'
)

if cliente is None:
    texto = '{"categoria": "hipertensión grado 1", "motivo": "PAS 140-159 o PAD 90-99"}'
else:
    texto, _, _ = preguntar(prompt, temperatura=0)

texto = texto.strip().removeprefix("```json").removesuffix("```").strip()
datos = json.loads(texto)
print(datos)

assert "grado 1" in datos["categoria"].lower(), "La clasificación no coincide con la guía"
print("Respuesta comprobada")
""")
c.md("""
Las dos líneas `removeprefix`/`removesuffix` limpian una costumbre de muchos modelos: envolver el JSON en marcas de código.
""")

c.titulo(3, "3.5 La misma pregunta, varias respuestas")
c.md("""
Con temperatura alta, repetimos cinco veces la misma pregunta. Si no hay clave, se simulan respuestas para mostrar el efecto.
""")
c.code("""
pregunta = "En una sola palabra, ¿cuál es el síntoma más frecuente de la insuficiencia cardiaca?"

for intento in range(1, 6):
    if cliente is None:
        texto = rng.choice(["Disnea", "Disnea", "Disnea", "Fatiga", "Edemas"])
    else:
        texto, _, _ = preguntar(pregunta, temperatura=1.5)
    print(f"Intento {intento}: {texto.strip()}")
""")

c.titulo(3, "3.6 Detectar una alucinación")
c.md("""
Pide al modelo referencias bibliográficas y **comprueba cada una**: busca el DOI en [doi.org](https://doi.org) o el título en PubMed. Anota cuántas existen y dicen lo que el modelo afirma.
""")
c.code("""
texto, _, _ = preguntar(
    "Dame tres referencias bibliográficas, con su DOI, sobre la ecuación CKD-EPI 2021 "
    "para estimar el filtrado glomerular.",
    temperatura=0.7,
)
print(texto)
print("\\n→ Verifica cada DOI en https://doi.org antes de usar ninguna referencia.")
""")

c.titulo(3, "Ampliación: ver los modelos disponibles")
c.code("""
if cliente is not None:
    for modelo in cliente.models.list():
        if "gemini" in modelo.name:
            print(modelo.name)
else:
    print("Necesitas una clave configurada para listar los modelos.")
""")

c.titulo(3, "Ampliación: la misma petición con OpenAI")
c.md("""
Si tienes una clave de OpenAI guardada como `OPENAI_API_KEY`, la petición equivalente es esta. Comprueba en la documentación de OpenAI el nombre de los modelos disponibles.
""")
c.code("""
%pip install -q openai

try:
    from openai import OpenAI
    cliente_openai = OpenAI(api_key=userdata.get("OPENAI_API_KEY"))
    respuesta = cliente_openai.responses.create(
        model="gpt-4.1-mini",
        input="Explica en una frase qué es la presión arterial media.",
    )
    print(respuesta.output_text)
except Exception as error:
    print("No se ha podido usar OpenAI:", type(error).__name__)
""")

c.titulo(3, "Ampliación: buenas prácticas para escribir un prompt")
c.md("""
| Práctica | Ejemplo |
| --- | --- |
| Dar contexto y rol | «Eres profesor de bioestadística de un grado de Medicina…» |
| Ser específico | «En tres frases», «para estudiantes de segundo curso» |
| Pedir el formato | «Responde en JSON con las claves…» |
| Pedir el razonamiento | «Explica cada paso del cálculo» |
| Pedir que reconozca sus límites | «Si no estás seguro, dilo» |
| No sugerir la respuesta | Evitar «¿Verdad que es una neumonía?» |
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Escribir la clave en el código** en lugar de leerla de Secretos.

**Confiar en la respuesta sin verificarla**, sobre todo en cifras, dosis y referencias.

**Enviar datos de pacientes**, aunque parezcan anónimos: edad, fecha y diagnóstico raro pueden bastar para identificar a una persona.

**Ignorar los límites del nivel gratuito:** si se superan, la API devuelve un error de cuota (código 429). Basta con esperar.

**Usar un modelo retirado:** los nombres de los modelos cambian; consulta la lista de modelos disponibles.

**Analizar el JSON sin limpiarlo** cuando el modelo lo envuelve en marcas de código.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 80 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** predecir el efecto de la temperatura sobre distribuciones de probabilidad de juguete.
2. **Misión clínica (con pistas):** pedir al modelo que clasifique cinco valores de IMC en JSON. Comprobar cada clasificación con la función del Tema 50.
3. **Misión reto (con asistente):** pedir tres referencias sobre un tema clínico, verificar cada DOI y calcular la proporción de referencias correctas.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Qué hace un modelo de lenguaje al generar una respuesta?", [
        ("Elige, token a token, una continuación según su probabilidad", True, "Correcto: genera el texto más probable dado lo anterior."),
        ("Busca la respuesta en una base de datos médica", False, "No consulta bases de datos: genera texto a partir de lo aprendido."),
        ("Razona como un médico y comprueba los hechos", False, "No comprueba hechos; por eso puede alucinar."),
        ("Copia literalmente textos de su entrenamiento", False, "Genera texto nuevo a partir de patrones aprendidos."),
    ]),
    ("Quieres que el modelo extraiga datos de un texto siempre de la misma forma. ¿Qué temperatura conviene?", [
        ("Baja, cercana a 0", True, "Correcto: favorece la opción más probable y da respuestas estables."),
        ("Alta, mayor de 1", False, "Una temperatura alta aumenta la variedad y los errores."),
        ("Da igual: la temperatura no afecta a la respuesta", False, "La temperatura cambia cómo se elige cada token."),
        ("Temperatura negativa", False, "La temperatura es un valor positivo."),
    ]),
    ("Un modelo te da una referencia con un DOI que no existe. ¿Cómo se llama este fenómeno?", [
        ("Alucinación", True, "Correcto: información falsa con aspecto convincente."),
        ("Fecha de corte", False, "La fecha de corte explica que desconozca lo reciente, no que invente."),
        ("Sesgo de asignación", False, "Es un concepto de los ensayos clínicos (Tema 60)."),
        ("Error de cuota", False, "Es un error de la API por exceso de peticiones."),
    ]),
    ("¿Dónde debe estar la clave de acceso al usar la API desde Colab?", [
        ("En el panel Secretos, leída con userdata.get()", True, "Correcto: así no aparece nunca en el código ni en pantalla."),
        ("En una variable al principio del cuaderno", False, "Cualquiera que vea el cuaderno vería la clave."),
        ("Dentro del prompt", False, "La clave nunca se envía como texto de la pregunta."),
        ("En un fichero CSV junto a los datos", False, "Quedaría expuesta al compartir el fichero."),
    ]),
    ("Una petición consume 120 tokens de entrada y 380 de salida. ¿Cuántos tokens consume en total?", [
        ("500", True, "Correcto: el consumo es la suma de entrada y salida."),
        ("380", False, "También cuentan los tokens de entrada."),
        ("260", False, "No se restan: se suman."),
        ("120", False, "También cuentan los tokens de salida."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Un LLM genera texto prediciendo, token a token, la continuación más probable; no comprueba hechos.
- La temperatura regula la variabilidad: baja para tareas que exigen estabilidad.
- Alucinaciones, fecha de corte, variabilidad, sesgos y complacencia obligan a verificar toda respuesta.
- La API se usa con la clave guardada en Secretos; la respuesta llega en JSON con el texto y los tokens consumidos.
- Una respuesta en JSON se comprueba con casos conocidos antes de usarla.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| LLM | Modelo de lenguaje de gran tamaño, entrenado para predecir texto |
| Token | Fragmento de texto con el que trabaja el modelo |
| *Prompt* | Instrucción o pregunta que se envía al modelo |
| Temperatura | Parámetro que regula la aleatoriedad en la elección de tokens |
| Softmax | Función que convierte puntuaciones en probabilidades que suman 1 |
| Alucinación | Información falsa generada con apariencia verosímil |
| Fecha de corte | Fecha hasta la que llegan los datos de entrenamiento del modelo |
| API | Interfaz que permite a un programa usar un servicio externo |
| Cuota | Límite de peticiones o tokens permitidos en un periodo |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Documentación de la API de Gemini](https://ai.google.dev/gemini-api/docs)
- [Documentación de la API de OpenAI](https://platform.openai.com/docs)
- Thirunavukarasu AJ, *et al.* Large language models in medicine. *Nat Med*. 2023;29(8):1930-1940.
""")

c.pie(80)
print(c.guardar("../cuadernos"))
