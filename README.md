# Bioestadística (1964) · Grado en Medicina · UMH

Materiales de la asignatura Bioestadística (código 1964) del Grado en Medicina de la Universidad Miguel Hernández de Elche, curso 2027-2028.

**Autor:** Fernando Borrás Rocher · Universidad Miguel Hernández de Elche · ORCID [0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573)

## Contenido del repositorio

- `cuadernos/`: el Tema 0 (guía de Colab, lectura previa) y los 30 cuadernos de Google Colab, uno por tema (Tema 10 a Tema 300), cada uno para una sesión de 50 minutos.
- `scripts/`: los scripts que generan cada cuaderno a partir de una plantilla común.
- `cuadernos.html`: página con los 31 cuadernos (abrir en Colab, ver en GitHub, practicar en la app), con buscador; se enlaza desde la barra superior y la portada de la app; su botón «Practicar en la app» abre la ruta en las misiones del tema con el enlace directo `index.html#tema-150` (sirve para cualquier tema: `#tema-10` … `#tema-300`) y se regenera con `scripts/pagina_cuadernos.py`.
- `index.html`: la app **Bioestadística** (se publica en https://fborrasumh.github.io/bioestadistica/ al activar GitHub Pages).
- `app/`: fuentes de la app (`src/` con las misiones de cada módulo), el script que la monta (`build.py`) y sus pruebas (`tests/`).
- `datos/`: los ficheros de datos sintéticos que usan los cuadernos.

## Temario

| Módulo | Temas |
| --- | --- |
| Módulo 1. Descubriendo Python | 10-40 |
| Módulo 2. Programando con IA | 50-80 |
| Módulo 3. Procesado inicial de datos | 90-130 |
| Módulo 4. Probabilidad | 140-190 |
| Módulo 5. Generalización de conclusiones | 200-300 |

## Dar la clase con el cuaderno

Cada cuaderno se puede proyectar en lugar de una presentación. Al principio de cada bloque hay una **diapositiva** (celda con borde azul): título, una figura y dos o tres ideas, a veces con una pregunta para la clase. Debajo, en la sección «Desarrollo para el estudio», está el detalle, que se puede plegar con la flecha de su título.

- Antes de empezar: **Entorno de ejecución → Ejecutar todo**, para que se dibujen los gráficos de las celdas ocultas.
- Hay 94 diapositivas en los 30 temas. Los esquemas fijos están en `figuras/` (PNG) y se generan con `python3 scripts/figuras.py`; las diapositivas se definen en `scripts/diapositivas/` (una por módulo) y se insertan solas al generar cada cuaderno.
- Las figuras son propias, salvo el diagrama de Florence Nightingale (1858, dominio público, Wikimedia Commons) del Tema 60.

## App Bioestadística

Práctica de los 30 temas, con **tres misiones por tema** (90 en total), como se anuncia en el apartado «Práctica en la app» de cada cuaderno:

| Misión | Ayuda | Tipo |
| --- | --- | --- |
| Básica | Ninguna, como en el examen | Test o código |
| Clínica | Pistas fijas | Código con datos clínicos sintéticos |
| Reto | Pistas y tutor de IA opcional (con la clave de cada estudiante) | Casi siempre: verificar y corregir un código que «ha propuesto el asistente» |

- **Python real en el navegador** (Pyodide 0.27.7 en un Web Worker): pandas, NumPy, SciPy y matplotlib se descargan solo en las misiones que los usan. No hay servidor.
- **El código corrige; la IA no.** Cada misión ejecuta una solución de referencia con los mismos datos, prueba casos ocultos y reconoce los errores típicos (umbrales con `<` en vez de `<=`, *n* en lugar de *n* − 1, Wald en lugar de Wilson, prueba *t* independiente con datos apareados, OR por 10 años mal calculada…).
- **Datos por semilla:** cada estudiante recibe datos distintos y el profesorado puede reproducirlos.
- **Informe de evaluación continua (EC)** en Word, JSON y CSV, con el nombre `1964_apellidos_nombre_AAAAMMDD-HHMM` (minúsculas, sin tildes; la app exige apellidos y nombre antes de descargarlo). Cada informe es acumulativo: vale el más reciente. El CSV incluye, por misión, `primer_intento` (resuelta en el primer intento, sin ayudas) y `tras_pista` (resuelta al final), los datos que se analizan en el Tema 300. El reto del Tema 300 usa los informes del propio estudiante cuando ha intentado al menos 15 misiones.
- **Corrección de la EC de toda la clase:** el panel del profesorado carga de golpe todos los JSON (o el ZIP de la tarea del Campus Virtual) y da una tabla descargable con, por estudiante, las misiones completadas válidas (total y por módulo), el porcentaje resuelto al primer intento y la **EC propuesta = misiones completadas válidas / 90 × 10**, que confirma el profesorado. Una misión solo cuenta si su respuesta es correcta, tiene su evento en el registro encadenado y su código coincide con la huella del que aprobó. Avisa de registros editados, informes repetidos (se queda el más reciente), semillas compartidas y código idéntico entre estudiantes. Opcionalmente vuelve a ejecutar el código de cada misión con la semilla del estudiante (lento: varios segundos por estudiante).
- **Profesorado:** verificación del JSON de un estudiante (registro encadenado SHA-256 y recálculo de cada solución con su semilla) y exámenes individualizados.

El motor (ejecución, corrección, informes y panel del profesorado) es el de [PyMedIA](https://github.com/fborrasumh/pymedia) 1.0.1, del mismo autor; `app/build.py` cambia la marca, los temas y las misiones, y añade los niveles de ayuda y los campos del informe.

**Descargas sin conexión:** el Word, el JSON, el CSV y el ZIP se escriben en el propio navegador, sin librerías de internet.

**Límites:** la interfaz y las misiones están solo en español en esta versión. La primera carga necesita internet (Pyodide unos 14 MB; SciPy y pandas, varios MB más). Las soluciones de referencia viajan dentro del fichero: la app no es un sistema de examen vigilado. Las fórmulas y umbrales clínicos son didácticos. Las misiones se han probado con CPython y las versiones de pandas, NumPy y SciPy de Pyodide 0.27.7 (90 misiones × 8 semillas); no se han probado dentro de Pyodide en el navegador ni con una clave real de IA.

```bash
cd app
python3 build.py              # monta ../index.html
python3 tests/logic_test.py 8 # 90 misiones × 8 semillas: la solución aprueba, cada error típico suspende y se reconoce
```

## Cuadernos disponibles

| Tema | Título | Abrir |
| --- | --- | --- |
| 0 | Guía del entorno de trabajo: cuadernos Jupyter y Google Colab (lectura previa obligatoria) | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_000_Guia_del_entorno_Google_Colab.ipynb) |
| 10 | Introducción a la bioestadística computacional en ciencias de la salud: entorno Google Colab y asistentes de inteligencia artificial | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_010_Introduccion_bioestadistica_computacional.ipynb) |
| 20 | Representación de datos clínicos en Python: tipos numéricos, cadenas de texto y estructuras de datos | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_020_Representacion_de_datos_clinicos_en_Python.ipynb) |
| 30 | Lógica booleana y estructuras condicionales aplicadas a la clasificación clínica | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_030_Logica_booleana_y_estructuras_condicionales.ipynb) |
| 40 | Estructuras iterativas para el procesamiento de series de pacientes | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_040_Estructuras_iterativas_series_de_pacientes.ipynb) |
| 50 | Funciones en Python para la implementación de índices y escalas clínicas | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_050_Funciones_indices_y_escalas_clinicas.ipynb) |
| 60 | Módulos científicos, generación de números aleatorios y visualización básica con Matplotlib | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_060_Modulos_aleatoriedad_y_visualizacion_con_Matplotlib.ipynb) |
| 70 | Gestión de ficheros y formatos de intercambio de datos sanitarios: CSV y JSON | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_070_Ficheros_y_formatos_de_datos_sanitarios_CSV_y_JSON.ipynb) |
| 80 | Fundamentos de los modelos de lenguaje de gran tamaño: funcionamiento, limitaciones y uso seguro mediante API | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_080_Modelos_de_lenguaje_funcionamiento_limitaciones_y_API.ipynb) |
| 90 | Programación asistida por inteligencia artificial: ciclo de mejora recursiva de generación, verificación y corrección | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_090_Programacion_asistida_por_IA_y_mejora_recursiva.ipynb) |
| 100 | Estructuras de datos con Pandas: tratamiento de valores perdidos y atípicos en registros clínicos | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_100_Pandas_valores_perdidos_y_atipicos_en_registros_clinicos.ipynb) |
| 110 | Integración de fuentes de datos clínicos y elaboración de tablas de frecuencias | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_110_Integracion_de_datos_clinicos_y_tablas_de_frecuencias.ipynb) |
| 120 | Estadística descriptiva univariante: medidas de tendencia central, dispersión y forma | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_120_Estadistica_descriptiva_univariante.ipynb) |
| 130 | Análisis bivariante y representación gráfica de datos clínicos: asociación y correlación | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_130_Analisis_bivariante_asociacion_y_correlacion.ipynb) |
| 140 | Fundamentos de la teoría de la probabilidad y técnicas de recuento | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_140_Fundamentos_de_probabilidad_y_tecnicas_de_recuento.ipynb) |
| 150 | Probabilidad condicionada, independencia y teorema de Bayes en el razonamiento clínico | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_150_Probabilidad_condicionada_y_teorema_de_Bayes.ipynb) |
| 160 | Evaluación de pruebas diagnósticas y de cribado: sensibilidad, especificidad y valores predictivos | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_160_Evaluacion_de_pruebas_diagnosticas_y_de_cribado.ipynb) |
| 170 | Variables aleatorias discretas: distribuciones binomial y de Poisson | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_170_Variables_aleatorias_discretas_binomial_y_Poisson.ipynb) |
| 180 | Variables aleatorias continuas y distribución normal: intervalos de referencia clínicos | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_180_Variables_continuas_distribucion_normal_e_intervalos_de_referencia.ipynb) |
| 190 | Simulación de Monte Carlo y distribuciones muestrales | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_190_Simulacion_de_Monte_Carlo_y_distribuciones_muestrales.ipynb) |
| 200 | Estimación puntual e intervalos de confianza | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_200_Estimacion_puntual_e_intervalos_de_confianza.ipynb) |
| 210 | Fundamentos del contraste de hipótesis: significación estadística, errores y potencia | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_210_Contraste_de_hipotesis_significacion_errores_y_potencia.ipynb) |
| 220 | Inferencia sobre proporciones en una y dos poblaciones | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_220_Inferencia_sobre_proporciones_en_una_y_dos_poblaciones.ipynb) |
| 230 | Análisis de tablas de contingencia y medidas de asociación epidemiológica: riesgo relativo, odds ratio y número necesario a tratar | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_230_Tablas_de_contingencia_y_medidas_de_asociacion_RR_OR_y_NNT.ipynb) |
| 240 | Análisis de datos apareados y de concordancia: prueba de McNemar e índice kappa de Cohen | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_240_Datos_apareados_y_concordancia_McNemar_y_kappa_de_Cohen.ipynb) |
| 250 | Inferencia sobre medias: pruebas t para muestras independientes y relacionadas | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_250_Inferencia_sobre_medias_pruebas_t_independientes_y_relacionadas.ipynb) |
| 260 | Comparación de más de dos grupos: análisis de la varianza y pruebas no paramétricas | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_260_Comparacion_de_mas_de_dos_grupos_ANOVA_y_pruebas_no_parametricas.ipynb) |
| 270 | Modelos de regresión lineal simple y múltiple | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_270_Modelos_de_regresion_lineal_simple_y_multiple.ipynb) |
| 280 | Modelo de regresión logística | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_280_Modelo_de_regresion_logistica.ipynb) |
| 290 | Modelos predictivos e inteligencia artificial en la práctica clínica: desarrollo, validación y comunicación | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_290_Modelos_predictivos_e_IA_en_la_practica_clinica_desarrollo_validacion_y_comunicacion.ipynb) |
| 300 | Lectura crítica de la evidencia científica y evaluación de la mejora recursiva | [Colab](https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/Tema_300_Lectura_critica_de_la_evidencia_y_evaluacion_de_la_mejora_recursiva.ipynb) |

## Licencia

Cuadernos: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Todos los pacientes y datos son sintéticos.
