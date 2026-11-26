from plantilla import Cuaderno

c = Cuaderno("Tema_010_Introduccion_bioestadistica_computacional.ipynb")

c.cabecera(
    10,
    "Introducción a la bioestadística computacional en ciencias de la salud: entorno Google Colab y asistentes de inteligencia artificial",
    "Módulo 1. Descubriendo Python",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
    nota="**Requisito previo:** haber trabajado el [Tema 0. Guía del entorno de trabajo](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_000_Guia_del_entorno_Google_Colab.ipynb).\n\n",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Explicar qué aporta la bioestadística a la práctica clínica y a la medicina basada en la evidencia.
2. Distinguir población, muestra, parámetro y estadístico en un problema clínico.
3. Clasificar las variables clínicas según su tipo y su escala de medida.
4. Identificar las principales fuentes de datos en ciencias de la salud.
5. Ejecutar y documentar cálculos clínicos sencillos en un cuaderno de Colab.
6. Usar un asistente de inteligencia artificial con seguridad: sin datos de pacientes, sin exponer la clave de acceso y verificando siempre su respuesta.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Recorrido por el cuaderno | 5 |
| 4. Demostración: cálculos clínicos en Python | 15 |
| 5. Práctica en la app Bioestadística | 10 |
| 6. Autoevaluación | 5 |

Los apartados marcados como **ampliación** no se explican en clase: son material de estudio.
""")

# 1
c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
En una consulta de Atención Primaria se atiende a **Carmen**, de 58 años (paciente sintética). La enfermera registra:

| Dato | Valor |
| --- | --- |
| Peso | 68 kg |
| Talla | 1,63 m |
| Presión arterial | 148/92 mmHg |
| Glucemia en ayunas | 112 mg/dL |
| Fumadora | Sí |
| Grado de disnea (escala mMRC, de 0 a 4) | 1 |
| Ingresos hospitalarios en el último año | 0 |

Con estos datos, el médico decide con su juicio clínico: la presión arterial está en rango de hipertensión (≥ 140/90 mmHg) y la glucemia en ayunas, entre 100 y 125 mg/dL, indica glucemia basal alterada.

Pero el centro de salud atiende a **3.000 personas con hipertensión**, y las preguntas cambian de escala:

- ¿Qué proporción tiene la presión arterial controlada?
- ¿Es peor el control en fumadores que en no fumadores, o la diferencia es fruto del azar?
- ¿Ha mejorado el control desde que se cambió el protocolo?

Responder exige **convertir los registros clínicos en datos**, **resumirlos** y **cuantificar la incertidumbre**. Ese es el objeto de la bioestadística, y en esta asignatura lo haremos con código.
""")

# 2
c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Bioestadística y medicina basada en la evidencia")
c.md("""
La **bioestadística** es la aplicación de los métodos estadísticos a las ciencias de la vida y de la salud. Proporciona las herramientas para:

- **Describir** lo observado en un grupo de pacientes.
- **Medir la incertidumbre** de cualquier conclusión que se extraiga de datos.
- **Generalizar** lo observado en un grupo a la población de la que procede.

La **medicina basada en la evidencia** integra la mejor evidencia científica disponible con la experiencia clínica y los valores del paciente. Casi toda esa evidencia (la eficacia de un fármaco, la fiabilidad de una prueba diagnóstica, los valores de referencia de un análisis) se apoya en métodos bioestadísticos. Sin bioestadística no se puede leer críticamente un artículo científico.
""")
c.titulo(3, "2.2 Población, muestra, parámetro y estadístico")
c.md("""
| Concepto | Definición | En el caso de Carmen |
| --- | --- | --- |
| **Población** | Conjunto completo de individuos sobre el que se quiere concluir | Todas las personas con hipertensión del departamento de salud |
| **Muestra** | Subconjunto de la población que se estudia realmente | 300 pacientes con hipertensión del centro, elegidos al azar |
| **Parámetro** | Valor numérico que describe a la población (casi siempre desconocido) | Proporción real de pacientes con la presión controlada |
| **Estadístico** | Valor numérico calculado en la muestra | Proporción de pacientes controlados entre los 300 estudiados |

La estadística inferencial, que veremos en el Módulo 5, permite pasar del estadístico al parámetro con un margen de error conocido.
""")
c.titulo(3, "2.3 Tipos de variables")
c.md("""
Cada característica registrada de un paciente es una **variable**. Su tipo determina cómo se resume, cómo se representa y qué prueba estadística se usa.

| Tipo | Subtipo | Característica | Ejemplos |
| --- | --- | --- | --- |
| Cuantitativa | Continua | Puede tomar cualquier valor en un intervalo | Peso, talla, glucemia, presión arterial |
| Cuantitativa | Discreta | Toma valores enteros, normalmente recuentos | Ingresos en el último año, número de hijos |
| Cualitativa | Nominal | Categorías sin orden | Grupo sanguíneo, sexo, fumador (sí/no) |
| Cualitativa | Ordinal | Categorías con un orden natural | Disnea mMRC, estadio tumoral, escala de Glasgow por tramos |

Una variable cualitativa con solo dos categorías (fumador sí/no, curado sí/no) se llama **dicotómica** o **binaria**. Es la más frecuente en los ensayos clínicos.

Una **variable derivada** se calcula a partir de otras: el IMC se obtiene del peso y la talla.
""")
c.titulo(3, "2.4 Por qué programar")
c.md("""
Una hoja de cálculo es suficiente para 30 pacientes. Para 3.000, o para repetir el mismo análisis cada mes con datos nuevos, el código ofrece tres ventajas:

- **Reproducibilidad:** cualquier persona puede repetir el análisis y obtener el mismo resultado.
- **Escalabilidad:** el mismo código sirve para 30 o para 300.000 pacientes.
- **Trazabilidad:** cada paso queda escrito y se puede revisar, como un protocolo.
""")
c.titulo(3, "2.5 Inteligencia artificial: tres normas")
c.md("""
Colab y la app Bioestadística incluyen asistentes basados en **modelos de lenguaje de gran tamaño** (LLM). Escriben y explican código con rapidez, pero **pueden equivocarse con total seguridad**, también en estadística. En el Tema 80 estudiaremos por qué.

1. **Nunca** introduzcas datos reales de pacientes (Reglamento (UE) 2016/679, de protección de datos, y secreto profesional).
2. La **clave de acceso** es personal, como una contraseña: se guarda en Secretos, nunca en el código.
3. **Toda respuesta se verifica**: se ejecuta, se comprueba con un caso conocido y se entiende línea a línea.
""")

c.titulo(3, "Ampliación: fuentes de datos en ciencias de la salud")
c.md("""
| Fuente | Ejemplo | Ventaja | Limitación |
| --- | --- | --- | --- |
| Historia clínica electrónica | Registros de Atención Primaria | Gran volumen y datos reales de la práctica | Datos incompletos o registrados con distintos criterios |
| Registros poblacionales | Registros de cáncer, de mortalidad | Cobertura de toda una población | Pocas variables por paciente |
| Encuestas de salud | Encuesta Nacional de Salud de España | Información de la población general | Datos declarados, no medidos |
| Ensayos clínicos | Comparación de dos tratamientos | Máximo control del sesgo | Pacientes seleccionados, no siempre representativos |
| Datos abiertos | Portales de datos de organismos sanitarios | Acceso libre y reutilizable | Hay que comprobar su calidad y su licencia |

En esta asignatura trabajaremos con **datos sintéticos** (generados por ordenador con características realistas) y con **datos abiertos**. Nunca con datos de pacientes identificables.
""")

# 3
c.titulo(2, "3. Recorrido por el cuaderno (5 min)")
c.md("""
Repaso rápido de lo trabajado en el Tema 0:

1. Comprueba que estás en **tu copia** (el nombre del cuaderno no debe empezar por *Copia de* si ya lo has renombrado, y debe estar en tu Drive).
2. Abre el **índice** en la barra lateral y localiza el apartado 4.
3. Ejecuta la celda siguiente y observa el número que aparece a su izquierda.
4. Vuelve a ejecutarla: el número aumenta, porque indica el orden de ejecución.
""")
c.code("""
print("Mi cuaderno de Bioestadística está listo")
""")

# 4
c.titulo(2, "4. Demostración: cálculos clínicos en Python (15 min)")
c.titulo(3, "4.1 Índice de masa corporal")
c.md("""
$$\\text{IMC} = \\frac{\\text{peso (kg)}}{\\text{talla (m)}^2}$$

Cada dato se guarda en una **variable** con un nombre que indica qué es y en qué unidad está. En Python la potencia se escribe `**` y el separador decimal es el **punto**.
""")
c.code("""
# Datos de la paciente Carmen (sintéticos)
peso_kg = 68
talla_m = 1.63

imc = peso_kg / talla_m ** 2
imc
""")
c.md("""
Para presentar el resultado con su unidad y redondeado se usa una **cadena formateada** (*f-string*): `{imc:.1f}` inserta el valor con un decimal.
""")
c.code("""
print(f"IMC de Carmen: {imc:.1f} kg/m²")
""")
c.md("""
**Interpretación:** según la Organización Mundial de la Salud, un IMC entre 25,0 y 29,9 kg/m² corresponde a sobrepeso.
""")

c.titulo(3, "4.2 Presión arterial media")
c.md("""
La presión arterial media (PAM) estima la presión de perfusión de los órganos:

$$\\text{PAM} \\approx \\text{PAD} + \\frac{\\text{PAS} - \\text{PAD}}{3}$$

Los paréntesis fijan el orden de las operaciones, igual que en matemáticas.
""")
c.code("""
pas_mmHg = 148   # presión arterial sistólica
pad_mmHg = 92    # presión arterial diastólica

pam_mmHg = pad_mmHg + (pas_mmHg - pad_mmHg) / 3
print(f"Presión arterial media: {pam_mmHg:.0f} mmHg")
""")

c.titulo(3, "4.3 Superficie corporal")
c.md("""
La superficie corporal se usa para ajustar la dosis de muchos fármacos, como los quimioterápicos. La fórmula de Mosteller es:

$$\\text{SC (m}^2) = \\sqrt{\\frac{\\text{talla (cm)} \\times \\text{peso (kg)}}{3600}}$$

La raíz cuadrada se obtiene elevando a 0,5. Observa que esta fórmula usa la talla **en centímetros**: por eso la variable lleva la unidad en el nombre.
""")
c.code("""
talla_cm = talla_m * 100
superficie_corporal_m2 = (talla_cm * peso_kg / 3600) ** 0.5
print(f"Superficie corporal: {superficie_corporal_m2:.2f} m²")
""")

c.titulo(3, "4.4 Cambio de unidades")
c.md("""
La glucemia se expresa en mg/dL en España y en mmol/L en otros países y en muchos artículos. Para pasar de mg/dL a mmol/L se divide entre 18 (aproximadamente, la masa molar de la glucosa dividida entre 10).
""")
c.code("""
glucemia_mg_dl = 112
glucemia_mmol_l = glucemia_mg_dl / 18
print(f"Glucemia: {glucemia_mg_dl} mg/dL = {glucemia_mmol_l:.1f} mmol/L")
""")

c.titulo(3, "4.5 Comprobar un resultado")
c.md("""
Antes de fiarte de un cálculo, propio o del asistente, compruébalo con un valor que conozcas. La comparación `==` devuelve `True` (verdadero) o `False` (falso).

Hemos calculado a mano que el IMC de Carmen es 25,6 kg/m². Comprobémoslo:
""")
c.code("""
round(imc, 1) == 25.6
""")

c.titulo(3, "4.6 Una mirada al destino del curso")
c.md("""
La celda siguiente genera **200 pacientes sintéticos** y compara la presión arterial sistólica de fumadores y no fumadores. **No hace falta entender este código todavía**: al final del Módulo 3 sabrás escribirlo, y en el Módulo 5 sabrás decidir si la diferencia es real o fruto del azar.
""")
c.code("""
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=1964)
pacientes = pd.DataFrame({
    "edad": rng.integers(40, 80, size=200),
    "fumador": rng.choice(["sí", "no"], size=200, p=[0.3, 0.7]),
    "pas_mmHg": rng.normal(135, 15, size=200).round(),
})

pacientes.groupby("fumador")["pas_mmHg"].describe().round(1)
""")

c.titulo(3, "4.7 La clave de acceso, sin exponerla")
c.md("""
Si ya guardaste tu clave en **Secretos** (apartado siguiente), esta celda comprueba si existe sin mostrarla. Busca los dos nombres que usaremos en el curso: `GEMINI_API_KEY` y `OPENAI_API_KEY`.
""")
c.code("""
for nombre in ["GEMINI_API_KEY", "OPENAI_API_KEY"]:
    try:
        from google.colab import userdata
        clave = userdata.get(nombre)
        print(f"{nombre}: configurada")
    except Exception as error:
        print(f"{nombre}: no configurada ({type(error).__name__})")
""")

c.titulo(3, "Ampliación: cómo obtener una clave de acceso (API key)")
c.md("""
Para la asignatura basta con **una** clave. Recomendamos la de **Google Gemini**, que tiene un nivel gratuito sin tarjeta de crédito. La de **OpenAI** es de pago y es opcional.

| | Google Gemini | OpenAI |
| --- | --- | --- |
| Coste | Nivel gratuito con límites de uso; no pide tarjeta | De pago: se compran créditos por adelantado (mínimo 5 dólares) |
| Dónde se obtiene | Google AI Studio (aistudio.google.com) | Plataforma de OpenAI (platform.openai.com) |
| Nombre del secreto en Colab | `GEMINI_API_KEY` | `OPENAI_API_KEY` |
| Requisito de edad | 18 años | Según sus condiciones de uso |

#### Opción A. Clave gratuita de Google Gemini

1. Entra en [Google AI Studio](https://aistudio.google.com/) con tu cuenta de Google y acepta las condiciones de uso.
2. Pulsa **Get API key** (Obtener clave de API) en el menú lateral.
3. Pulsa **Create API key** (Crear clave de API). Si te lo pide, elige crearla en un proyecto nuevo: AI Studio lo prepara solo.
4. Copia la clave y guárdala en el panel **Secretos** de Colab con el nombre `GEMINI_API_KEY` (pasos al final de este apartado).
5. Comprueba en la lista de claves que el proyecto aparece como gratuito (*Free*). No actives la facturación: no es necesaria para la asignatura.

Si aparece un aviso de que el nivel gratuito no está disponible para tu proyecto, crea la clave en otro proyecto nuevo o consulta al profesor. No actives la facturación para resolverlo.

#### Opción B. Clave de pago de OpenAI

1. Entra en la [plataforma de OpenAI](https://platform.openai.com/) con tu cuenta. La cuenta de ChatGPT sirve para entrar, pero la API se paga aparte: una suscripción a ChatGPT no incluye uso de la API.
2. En la sección de facturación (**Billing**), añade un método de pago y compra el mínimo de créditos.
3. **Desactiva la recarga automática** (*auto-reload*), que viene activada por defecto, para no hacer cargos sin darte cuenta. Los créditos caducan al año y no se devuelven.
4. En **API keys**, pulsa **Create new secret key**, ponle un nombre y cópiala en ese momento: después no se vuelve a mostrar.
5. Guárdala en **Secretos** de Colab con el nombre `OPENAI_API_KEY`.

#### Guardar la clave en Colab

1. Abre el panel **Secretos** (icono de la llave en la barra lateral izquierda).
2. Pulsa **Añadir nuevo secreto**.
3. Escribe el nombre exacto (`GEMINI_API_KEY` o `OPENAI_API_KEY`) y pega la clave en el valor.
4. Activa el interruptor de acceso del cuaderno.
5. Ejecuta la celda del apartado 4.7 para comprobarlo.

#### Normas de seguridad

- La clave es personal: no se comparte, no se escribe en el código y no se envía por correo ni por mensajería.
- Si crees que alguien ha visto tu clave, **bórrala** en AI Studio o en la plataforma de OpenAI y crea otra.
- Las condiciones de estos servicios prohíben usarlos en la práctica clínica real o para dar consejo médico. En la asignatura los usamos solo para aprender, con datos sintéticos.
- Ni el nivel gratuito ni el de pago autorizan a enviar datos de pacientes.
""")

c.titulo(3, "4.8 Pedir ayuda al asistente con seguridad")
c.md("""
| Petición inadecuada | Petición adecuada |
| --- | --- |
| «Calcula el IMC de Carmen López, NHC 123456, que pesa 68 kg y mide 1,63 m» | «Escribe en Python el cálculo del IMC a partir de dos variables, peso_kg y talla_m, y explica cada línea» |
| Identifica a una persona y pide solo un número | No identifica a nadie, pide código y explicación, y el resultado se puede verificar |

**Prueba:** abre el asistente de Colab, pídele el cálculo de la superficie corporal con la fórmula de Mosteller y compara su resultado con el del apartado 4.3. Si no coinciden, averigua por qué antes de dar por buena ninguna de las dos versiones.
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Usar la coma decimal.** En Python, `1,63` no es un número: es una pareja de valores (1 y 63). Ejecuta la celda y observa el resultado.
""")
c.code("""
talla_con_coma = 1,63
print(talla_con_coma, type(talla_con_coma))
""")
c.md("""
**Mezclar unidades.** Si se escribe la talla en centímetros (163) en la fórmula del IMC, el resultado es 10.000 veces menor. Poner la unidad en el nombre (`talla_m`, `talla_cm`) previene el error.

**Olvidar los paréntesis.** `92 + 148 - 92 / 3` no es la presión arterial media: Python divide antes de sumar.
""")
c.code("""
print("Sin paréntesis:", 92 + 148 - 92 / 3)
print("Con paréntesis:", 92 + (148 - 92) / 3)
""")
c.md("""
**Ejecutar las celdas fuera de orden.** Si una celda usa una variable antes de que se ejecute la celda que la define, Python responde con `NameError`.

**Confundir mayúsculas y minúsculas.** `Peso_kg` y `peso_kg` son variables distintas.

**Exponer la clave de acceso** escribiéndola en una celda y compartiendo después el cuaderno.
""")

# 5
c.titulo(2, "5. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 10 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** clasificar las variables de una historia clínica sintética según su tipo y su escala de medida.
2. **Misión clínica (con pistas):** calcular el IMC, la presión arterial media y la superficie corporal de un paciente y redactar su interpretación.
3. **Misión reto (con asistente):** configurar el asistente con tu clave, revisar qué datos se envían y verificar el código que te proponga.

Al terminar, exporta el **informe de la unidad**: forma parte del caso práctico integrador (25 % de la nota).
""")

# 6
c.titulo(2, "6. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código. Si no has ejecutado la configuración del cuaderno, hazlo antes.")
c.quiz([
    ("El grado de disnea según la escala mMRC (0 a 4) es una variable:", [
        ("Cualitativa ordinal", True, "Correcto: sus categorías tienen un orden natural, pero la distancia entre ellas no es necesariamente igual."),
        ("Cuantitativa continua", False, "Solo toma cinco valores que expresan categorías, no una medida continua."),
        ("Cuantitativa discreta", False, "Los números son etiquetas de categorías ordenadas, no recuentos."),
        ("Cualitativa nominal", False, "Sus categorías sí tienen un orden."),
    ]),
    ("En un estudio sobre 300 pacientes hipertensos de un centro, el 62 % tiene la presión controlada. Ese 62 % es:", [
        ("Un estadístico", True, "Correcto: se calcula en la muestra estudiada."),
        ("Un parámetro", False, "El parámetro sería la proporción en toda la población, que no conocemos."),
        ("Una población", False, "La población es el conjunto de individuos, no un valor numérico."),
        ("Una variable", False, "La variable es «presión controlada (sí/no)»; el 62 % es un resumen de ella."),
    ]),
    ("¿Qué muestra la celda talla = 1,80 seguida de print(talla)?", [
        ("(1, 80)", True, "Correcto: la coma separa dos valores y Python crea una pareja (tupla)."),
        ("1.8", False, "El separador decimal en Python es el punto, no la coma."),
        ("1,80", False, "Python no interpreta la coma como separador decimal."),
        ("Un error", False, "No hay error: la expresión es válida, aunque no hace lo que se pretendía."),
    ]),
    ("¿Cuál de estas expresiones calcula correctamente la presión arterial media con PAS = 148 y PAD = 92?", [
        ("92 + (148 - 92) / 3", True, "Correcto: los paréntesis obligan a restar antes de dividir."),
        ("92 + 148 - 92 / 3", False, "Python divide 92 entre 3 antes de sumar y restar."),
        ("(92 + 148 - 92) / 3", False, "Divide entre 3 toda la suma, no solo la diferencia."),
        ("92 + 148 / 3", False, "No resta la diastólica antes de dividir."),
    ]),
    ("¿Cuál de estas peticiones a un asistente de IA cumple las normas de la asignatura?", [
        ("Pedir una función que calcule el IMC y que explique cada línea", True, "Correcto: no contiene datos identificativos y produce código verificable."),
        ("Pegar el informe de alta de un paciente real para que lo resuma", False, "Nunca se introducen datos reales de pacientes."),
        ("Escribir la API key en el mensaje para que el asistente la configure", False, "La clave nunca se comparte."),
        ("Copiar su respuesta en un informe sin ejecutarla", False, "Toda respuesta se verifica antes de usarla."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- La bioestadística convierte observaciones clínicas en conclusiones fundadas y cuantifica su incertidumbre.
- Se estudia una **muestra** para conocer una **población**; el **estadístico** estima el **parámetro**.
- El tipo de variable decide cómo se resume y se analiza.
- En Python, el separador decimal es el punto y las variables deben llevar la unidad en el nombre.
- El asistente de IA ayuda, pero no sustituye la verificación ni el juicio propio, y nunca recibe datos de pacientes ni la clave de acceso.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Bioestadística | Aplicación de los métodos estadísticos a las ciencias de la vida y de la salud |
| Población | Conjunto completo de individuos sobre el que se quiere concluir |
| Muestra | Subconjunto de la población que se estudia |
| Parámetro | Valor que describe a la población |
| Estadístico | Valor calculado en la muestra |
| Variable | Característica que se registra en cada individuo |
| Variable dicotómica | Variable cualitativa con dos categorías |
| Datos sintéticos | Datos generados por ordenador que imitan las características de datos reales |
| LLM | Modelo de lenguaje de gran tamaño, base de los asistentes de IA |
| API key | Clave personal que autoriza el uso de un servicio de IA desde el código |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Tutorial oficial de Python en español](https://docs.python.org/es/3/tutorial/)
- [Preguntas frecuentes de Google Colab](https://research.google.com/colaboratory/faq.html)
- [Clasificación del IMC de la Organización Mundial de la Salud](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
""")

c.pie(10)
print(c.guardar("../cuadernos"))
