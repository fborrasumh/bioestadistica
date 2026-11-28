from plantilla import Cuaderno

c = Cuaderno("Tema_060_Modulos_aleatoriedad_y_visualizacion_con_Matplotlib.ipynb")

c.cabecera(
    60,
    "Módulos científicos, generación de números aleatorios y visualización básica con Matplotlib",
    "Módulo 2. Programando con IA",
    "50 minutos de clase, más el estudio de los apartados de ampliación",
)

c.configuracion()

c.titulo(2, "Objetivos de aprendizaje")
c.md("""
Al terminar esta sesión serás capaz de:

1. Importar módulos de Python y usar sus funciones (`math`, `statistics`, `random`, `numpy`).
2. Generar números aleatorios de forma **reproducible** con una semilla.
3. Aleatorizar la asignación de pacientes a los brazos de un ensayo clínico.
4. Simular mediciones clínicas con una distribución normal.
5. Construir con Matplotlib gráficos de líneas, barras, histogramas y dispersión correctamente rotulados.
6. Reconocer los errores más frecuentes que hacen que un gráfico engañe.
""")

c.titulo(2, "Plan de la sesión")
c.md("""
| Bloque | Minutos |
| --- | --- |
| 1. Caso clínico de partida | 5 |
| 2. Conceptos clave | 10 |
| 3. Demostración: azar y gráficos | 20 |
| 4. Práctica en la app Bioestadística | 10 |
| 5. Autoevaluación | 5 |
""")

c.titulo(2, "1. Caso clínico de partida (5 min)")
c.md("""
Un servicio de Neumología diseña un **ensayo clínico** para comparar dos pautas de fisioterapia respiratoria en pacientes con EPOC. Van a participar 20 pacientes. El comité de ética exige que la asignación a cada pauta sea **aleatoria**: ni el investigador ni el paciente la eligen.

¿Por qué? Si el investigador eligiera, tendería sin querer a dar la pauta nueva a quien cree que responderá mejor. Entonces la comparación quedaría **sesgada**. El azar reparte por igual, en promedio, todas las características de los pacientes, también las que no se han medido.

Además, cuando terminen el estudio querrán ver la evolución de cada paciente de un vistazo. Hoy aprenderemos a usar el azar de forma controlada y reproducible, y a representar datos clínicos con gráficos.
""")

c.titulo(2, "2. Conceptos clave (10 min)")
c.titulo(3, "2.1 Módulos")
c.diagrama('Módulos que se importan: math, statistics y random vienen con Python; numpy y matplotlib son externos y Colab ya los trae.')
c.md("""
Un **módulo** es un archivo con funciones listas para usar. Python incluye muchos de serie y se pueden instalar otros. Para usarlos hay que **importarlos**:

| Forma | Ejemplo | Uso posterior |
| --- | --- | --- |
| Importar el módulo | `import math` | `math.sqrt(16)` |
| Importar con un alias | `import numpy as np` | `np.mean(datos)` |
| Importar una función | `from statistics import median` | `median(datos)` |

| Módulo | Para qué lo usaremos |
| --- | --- |
| `math` | Funciones matemáticas: raíces, logaritmos, exponenciales |
| `statistics` | Estadísticos básicos: media, mediana, desviación típica |
| `random` | Números aleatorios sencillos |
| `numpy` | Cálculo numérico con muchos datos y generación aleatoria avanzada |
| `matplotlib` | Gráficos |

Colab ya trae instalados todos estos. Un módulo externo que no esté instalado se instala con `%pip install nombre`.
""")
c.titulo(3, "2.2 Aleatoriedad y semilla")
c.md("""
Los ordenadores generan números **pseudoaleatorios**: parecen aleatorios, pero salen de un cálculo que parte de un valor inicial, la **semilla**. Con la misma semilla se obtiene siempre la misma secuencia.

En ciencia, esto es una ventaja. Con la semilla fija, una simulación o una aleatorización son **reproducibles**: otra persona puede comprobarlas.
""")
c.titulo(3, "2.3 Un buen gráfico clínico")
c.md("""
- Título que diga qué se muestra.
- Ejes rotulados **con sus unidades**.
- Leyenda si hay más de una serie.
- En los gráficos de barras, el eje vertical empieza en **cero**.
- El tipo de gráfico adecuado al tipo de variable:

| Gráfico | Cuándo se usa | Ejemplo |
| --- | --- | --- |
| Líneas | Evolución en el tiempo | Curva de temperatura |
| Barras | Comparar frecuencias de categorías | Ingresos por servicio |
| Histograma | Distribución de una variable cuantitativa | Presión arterial de una muestra |
| Dispersión | Relación entre dos variables cuantitativas | Peso frente a talla |
""")

c.titulo(2, "3. Demostración: azar y gráficos (20 min)")
c.titulo(3, "3.1 El módulo math")
c.code("""
import math

print("Raíz cuadrada de 3,08:", math.sqrt(3.08))
print("Logaritmo neperiano de 10:", math.log(10))
print("Número e:", math.e)
""")
c.md("""
Aplicación: la fracción de fármaco que queda tras un tiempo *t* con una constante de eliminación *k* es $e^{-kt}$.
""")
c.code("""
k_por_hora = 0.1155          # corresponde a una vida media de unas 6 horas
horas = 12
fraccion_restante = math.exp(-k_por_hora * horas)
print(f"Queda el {fraccion_restante:.0%} del fármaco a las {horas} h")
""")

c.titulo(3, "3.2 El módulo statistics")
c.code("""
from statistics import mean, median, stdev

estancias_dias = [3, 5, 4, 2, 21, 6, 4, 3, 5]
print("Media:", round(mean(estancias_dias), 1), "días")
print("Mediana:", median(estancias_dias), "días")
print("Desviación típica:", round(stdev(estancias_dias), 1), "días")
""")
c.md("""
La media (5,9 días) está muy por encima de la mediana (4 días) por un solo paciente con 21 días de estancia. En el Tema 120 veremos cuándo conviene cada medida.
""")

c.titulo(3, "3.3 Aleatorizar un ensayo clínico")
c.md("""
Para asignar 10 pacientes a cada pauta, crea una lista con 10 etiquetas «A» y 10 «B». Después, **barájala** con `random.shuffle()`. La semilla hace que la asignación se pueda reproducir y auditar.
""")
c.code("""
import random

random.seed(1964)

asignaciones = ["A"] * 10 + ["B"] * 10
random.shuffle(asignaciones)

for numero, pauta in enumerate(asignaciones, start=1):
    print(f"Paciente {numero:02d}: pauta {pauta}")
""")
c.md("""
Vuelve a ejecutar la celda: sale la misma asignación, porque la semilla es la misma. Cambia la semilla y obtendrás otra distinta.

Otras funciones útiles del módulo `random`:
""")
c.code("""
random.seed(2027)
print("Número decimal entre 0 y 1:", random.random())
print("Entero entre 1 y 6:", random.randint(1, 6))
print("Elección al azar:", random.choice(["Cardiología", "Neumología", "Digestivo"]))
print("Muestra de 3 sin repetición:", random.sample(range(1, 101), 3))
""")

c.titulo(3, "3.4 Simular mediciones con numpy")
c.md("""
Para simular muchas mediciones se usa el generador de `numpy`. La presión arterial sistólica de una población adulta se puede aproximar por una **distribución normal** con una media y una desviación típica dadas. La estudiaremos en el Tema 180.
""")
c.code("""
import numpy as np

rng = np.random.default_rng(seed=1964)
pas_mmHg = rng.normal(loc=130, scale=15, size=500)

print("Primeras cinco:", pas_mmHg[:5].round())
print(f"Media simulada: {pas_mmHg.mean():.1f} mmHg")
print(f"Pacientes con PAS ≥ 140: {(pas_mmHg >= 140).sum()} de {len(pas_mmHg)}")
""")

c.titulo(3, "3.5 Gráfico de líneas: la curva de temperatura")
c.code("""
import matplotlib.pyplot as plt

horas = [0, 4, 8, 12, 16, 20, 24, 28, 32]
temperatura_c = [38.9, 39.2, 38.6, 38.1, 37.8, 37.4, 37.1, 36.9, 36.8]

plt.figure(figsize=(7, 4))
plt.plot(horas, temperatura_c, marker="o", label="Temperatura")
plt.axhline(38, color="red", linestyle="--", label="Umbral de fiebre (38 °C)")
plt.xlabel("Horas desde el inicio del antibiótico")
plt.ylabel("Temperatura (°C)")
plt.title("Paciente sintético 017: respuesta al tratamiento antibiótico")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
""")

c.titulo(3, "3.6 Gráfico de barras: ingresos por servicio")
c.code("""
servicios = ["Medicina Interna", "Cardiología", "Neumología", "Digestivo", "Neurología"]
ingresos = [142, 98, 87, 64, 51]

plt.figure(figsize=(7, 4))
plt.bar(servicios, ingresos, color="steelblue")
plt.ylabel("Número de ingresos")
plt.title("Ingresos por servicio en enero (datos sintéticos)")
plt.xticks(rotation=30, ha="right")
plt.show()
""")

c.titulo(3, "3.7 Histograma: distribución de la presión arterial")
c.code("""
plt.figure(figsize=(7, 4))
plt.hist(pas_mmHg, bins=25, color="steelblue", edgecolor="white")
plt.axvline(140, color="red", linestyle="--", label="140 mmHg")
plt.xlabel("Presión arterial sistólica (mmHg)")
plt.ylabel("Número de pacientes")
plt.title("Distribución de la PAS en 500 pacientes sintéticos")
plt.legend()
plt.show()
""")

c.titulo(3, "3.8 Gráfico de dispersión: peso y talla")
c.code("""
talla_m = rng.normal(1.70, 0.09, size=200)
peso_kg = 22 * talla_m ** 2 + rng.normal(0, 8, size=200)

plt.figure(figsize=(6, 5))
plt.scatter(talla_m, peso_kg, alpha=0.6)
plt.xlabel("Talla (m)")
plt.ylabel("Peso (kg)")
plt.title("Relación entre talla y peso (200 adultos sintéticos)")
plt.show()
""")

c.titulo(3, "Ampliación: guardar un gráfico")
c.md("""
Un gráfico se guarda como imagen con `plt.savefig()` antes de `plt.show()`. El archivo aparece en el panel **Archivos** de la barra lateral, desde donde se descarga. Los archivos de esa carpeta se borran al cerrar la sesión.
""")
c.code("""
plt.figure(figsize=(6, 4))
plt.bar(servicios, ingresos)
plt.ylabel("Número de ingresos")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("ingresos_por_servicio.png", dpi=200)
plt.show()
""")

c.titulo(3, "Ampliación: cómo engaña un gráfico")
c.md("""
Los mismos datos pueden contar historias muy distintas según se dibujen. Si el eje vertical de un gráfico de barras no empieza en cero, una diferencia pequeña parece enorme.
""")
c.code("""
tratamientos = ["Fármaco A", "Fármaco B"]
curacion_pct = [78, 81]

fig, ejes = plt.subplots(1, 2, figsize=(9, 3.5))
ejes[0].bar(tratamientos, curacion_pct)
ejes[0].set_ylim(76, 82)
ejes[0].set_title("Eje recortado: parece una gran diferencia")
ejes[0].set_ylabel("Curación (%)")
ejes[1].bar(tratamientos, curacion_pct)
ejes[1].set_ylim(0, 100)
ejes[1].set_title("Eje desde cero: diferencia de 3 puntos")
plt.tight_layout()
plt.show()
""")

c.titulo(3, "Ampliación: errores frecuentes")
c.md("""
**Olvidar importar el módulo.** Usar `math.sqrt()` sin `import math` produce `NameError`.

**No fijar la semilla.** Sin semilla, cada ejecución da resultados distintos y no se pueden reproducir ni revisar.

**Ejes sin unidades.** «Temperatura» no es suficiente: ¿grados Celsius o Fahrenheit?

**Elegir mal el gráfico.** Unir con líneas categorías sin orden (servicios hospitalarios) sugiere una evolución que no existe.

**Recortar el eje** de un gráfico de barras, como en el ejemplo anterior.
""")

c.titulo(3, "Ampliación: Una imagen médica es una matriz de NumPy")
c.md("""
Una imagen en escala de grises es una **matriz 2D**: cada elemento es un píxel. En una tomografía computarizada (TAC), cada valor está en **unidades Hounsfield** (UH). El aire vale −1000, el agua 0 y el hueso cortical unos 700 o más.

Un TAC completo es una **matriz 3D**: una pila de cortes. Su forma es `(cortes, filas, columnas)`.

La **ventana** decide qué valores se ven. Los valores por debajo de la ventana salen negros y los de encima salen blancos. Con `np.clip()` se aplica una ventana a toda la matriz en una sola operación.

**En tus materiales SIMUSTAT:** [Tema 140. Procesado de imágenes 2D con NumPy](https://colab.research.google.com/drive/1quCl69jOeY89qRlmjrMjFC-k-8s-8NMT), apartado 2. **En tus materiales SIMUSTAT:** [Tema 150. Procesado de imágenes 3D con NumPy](https://colab.research.google.com/drive/1eyZmZuo3DvMjGsdQ7m6W947P-v25a0z0), apartado 2 (los TAC).
""")
c.code("""
import numpy as np
import matplotlib.pyplot as plt

# Corte sintético de tórax: aire, tejido blando, dos pulmones y una costilla
filas, columnas = np.mgrid[0:200, 0:200]
corte = np.full((200, 200), -1000.0)                                     # aire
cuerpo = ((filas - 100) / 80) ** 2 + ((columnas - 100) / 95) ** 2 < 1
corte[cuerpo] = 40                                                       # tejido blando
for centro in (60, 140):
    pulmon = ((filas - 95) / 50) ** 2 + ((columnas - centro) / 28) ** 2 < 1
    corte[pulmon] = -800                                                 # pulmón
anillo = np.abs(np.sqrt((filas - 100) ** 2 + (columnas - 100) ** 2) - 76) < 3
corte[anillo & cuerpo] = 700                                             # costilla
for f, col in [(70, 50), (90, 70), (115, 55), (75, 150), (100, 130), (120, 148)]:
    corte[(filas - f) ** 2 + (columnas - col) ** 2 < 12] = -600          # vasos pulmonares
corte[(filas - 105) ** 2 + (columnas - 140) ** 2 < 30] = 40              # nódulo

print("Forma del corte:", corte.shape, "| mínimo:", corte.min(), "UH | máximo:", corte.max(), "UH")

def ventana(imagen, centro, anchura):
    return np.clip(imagen, centro - anchura / 2, centro + anchura / 2)

fig, ejes = plt.subplots(1, 2, figsize=(9, 4.5))
for eje, (nombre, c_v, a_v) in zip(ejes, [("Ventana pulmonar", -600, 1500), ("Ventana de mediastino", 40, 400)]):
    eje.imshow(ventana(corte, c_v, a_v), cmap="gray")
    eje.set_title(f"{nombre} (C {c_v}, A {a_v})")
    eje.axis("off")
plt.tight_layout()
plt.show()

tac = np.stack([corte] * 30)          # 30 cortes iguales: un volumen 3D
print("Forma del volumen:", tac.shape)
""")
c.md("""
La misma matriz da dos imágenes distintas. La ventana pulmonar distingue los vasos dentro del pulmón. La de mediastino deja el pulmón en negro, pero el nódulo y el tejido blando se ven en gris. Los datos no cambian: cambia cómo se presentan.
""")

c.titulo(2, "4. Práctica en la app Bioestadística (10 min)")
c.md("""
Abre la **[unidad 60 de la app Bioestadística](https://fborrasumh.github.io/bioestadistica/)** y completa sus misiones:

1. **Misión básica (sin asistente):** elegir el gráfico adecuado para cada pregunta clínica.
2. **Misión clínica (con pistas):** aleatorizar 30 pacientes en tres brazos con una semilla y comprobar que cada brazo tiene 10.
3. **Misión reto (con asistente):** pedir al asistente el gráfico de evolución de la glucemia de un paciente. Revisar que cumple todas las normas de un buen gráfico clínico.

Al terminar, exporta el **informe de la unidad**.
""")

c.titulo(2, "5. Autoevaluación (5 min)")
c.md("Responde sin asistente y sin ejecutar código.")
c.quiz([
    ("¿Para qué se fija una semilla al aleatorizar los pacientes de un ensayo?", [
        ("Para que la asignación sea reproducible y se pueda auditar", True, "Correcto: con la misma semilla se obtiene la misma secuencia."),
        ("Para que la asignación deje de ser aleatoria", False, "Sigue siendo aleatoria respecto a las características de los pacientes."),
        ("Para que salgan más pacientes en el brazo del tratamiento nuevo", False, "La semilla no cambia las proporciones."),
        ("Porque Python no genera números aleatorios sin semilla", False, "Sin semilla también los genera, pero distintos en cada ejecución."),
    ]),
    ("¿Qué gráfico es el más adecuado para mostrar la distribución de la glucemia en 300 pacientes?", [
        ("Histograma", True, "Correcto: muestra cómo se distribuye una variable cuantitativa."),
        ("Gráfico de líneas", False, "Las líneas muestran evolución en el tiempo."),
        ("Gráfico de barras de cada paciente", False, "300 barras no permiten ver la distribución."),
        ("Gráfico de sectores", False, "Los sectores representan proporciones de categorías."),
    ]),
    ("Tras import numpy as np, ¿cómo se llama a la función mean?", [
        ("np.mean(datos)", True, "Correcto: el alias np sustituye al nombre del módulo."),
        ("mean(datos)", False, "Sin importar la función directamente, hay que anteponer el módulo."),
        ("numpy.mean(datos)", False, "Al usar un alias, el nombre que queda disponible es np."),
        ("np(mean, datos)", False, "La sintaxis es módulo.función(argumentos)."),
    ]),
    ("Las estancias de 9 pacientes son 3, 5, 4, 2, 21, 6, 4, 3 y 5 días. ¿Qué medida representa mejor la estancia típica?", [
        ("La mediana, porque no la desplaza el valor extremo de 21 días", True, "Correcto: la mediana (4 días) no se ve afectada por un valor atípico."),
        ("La media, porque usa todos los datos", False, "Precisamente por usar todos los datos, el valor de 21 la desplaza."),
        ("La desviación típica", False, "Mide la dispersión, no el valor típico."),
        ("El valor máximo", False, "El máximo es el caso extremo, no el típico."),
    ]),
    ("Un gráfico de barras compara curaciones del 78 % y del 81 % con el eje vertical entre 76 y 82. ¿Qué problema tiene?", [
        ("Exagera visualmente una diferencia de 3 puntos", True, "Correcto: en barras, el eje debe empezar en cero."),
        ("Ninguno: así se ve mejor la diferencia", False, "Se ve mejor a costa de distorsionar su magnitud."),
        ("Debería ser un gráfico de líneas", False, "Las barras son adecuadas; el problema es el eje."),
        ("Le falta la semilla", False, "La semilla no tiene que ver con los gráficos."),
    ]),
])

c.titulo(2, "Ideas clave")
c.md("""
- Los módulos amplían Python: se importan con `import` y se usan con `módulo.función()`.
- Los números aleatorios del ordenador dependen de una semilla: fijarla hace los resultados reproducibles.
- La aleatorización evita el sesgo de asignación en los ensayos clínicos.
- Cada tipo de variable tiene su gráfico; los ejes llevan siempre unidades y las barras empiezan en cero.
""")

c.titulo(2, "Glosario")
c.md("""
| Término | Definición |
| --- | --- |
| Módulo | Archivo de Python con funciones que se pueden importar |
| Alias | Nombre corto con el que se importa un módulo (`np`, `plt`) |
| Número pseudoaleatorio | Número generado por un cálculo que imita el azar |
| Semilla | Valor inicial que determina la secuencia de números pseudoaleatorios |
| Aleatorización | Asignación al azar de los participantes a los grupos de un estudio |
| Sesgo de asignación | Distorsión de los resultados por elegir quién recibe cada tratamiento |
| Histograma | Gráfico de la distribución de una variable cuantitativa |
""")

c.titulo(2, "Para saber más")
c.md("""
- [Documentación del módulo random](https://docs.python.org/es/3/library/random.html)
- [Documentación del módulo statistics](https://docs.python.org/es/3/library/statistics.html)
- [Galería de ejemplos de Matplotlib](https://matplotlib.org/stable/gallery/index.html)
""")

c.pie(60)
print(c.guardar("../cuadernos"))
