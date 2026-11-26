/* ══ Módulo 2 · Programando con IA (temas 50 a 80) ══ */

/* ───── Tema 50 · Funciones, índices y escalas clínicas ───── */
M({id: 'm50-1', tema: 50, k: 'code', nivel: 1,
  t: E('Función de superficie corporal de Mosteller'),
  gen: r => ({casos: Array.from({length: 3}, () => [red(40 + r.next() * 80, 1), r.int(145, 200)])}),
  data: () => '',
  enun: () => E(`<p>Define la función <code>mosteller(peso, talla_cm)</code> que devuelva (con <code>return</code>) la superficie corporal en m², √(talla en cm · peso / 3600), redondeada a 2 decimales.</p><p>Se probará con varios pacientes.</p>`),
  func: {names: ['mosteller'], cases: p => p.casos.map(([w, h]) => ({e: `mosteller(${w}, ${h})`, vis: true})).concat([{e: 'mosteller(70, 170)', vis: false}])},
  req: ['def'],
  sol: String.raw`def mosteller(peso, talla_cm):
    return round((talla_cm * peso / 3600) ** 0.5, 2)`,
  mut: [mutE('print', String.raw`def mosteller(peso, talla_cm):
    print(round((talla_cm * peso / 3600) ** 0.5, 2))`, 'La función imprime el valor pero no lo devuelve: sin return, quien la llama recibe None.'),
    mutE('sin_raiz', String.raw`def mosteller(peso, talla_cm):
    return round(talla_cm * peso / 3600, 2)`, 'Falta la raíz cuadrada: ** 0.5.')],
  pistas: []
});

M({id: 'm50-2', tema: 50, k: 'code', nivel: 2,
  t: E('CURB-65 como función, con sus valores frontera'),
  gen: r => ({c: [r.bool(), r.int(10, 35), r.int(16, 34), r.int(85, 140), r.int(50, 90), r.int(40, 90)]}),
  data: () => '',
  enun: () => E(`<p>Define <code>curb65(confusion, bun, fr, pas, pad, edad)</code> que devuelva la puntuación (0 a 5): un punto por confusión, BUN &gt; 19 mg/dL, FR ≥ 30, PAS &lt; 90 o PAD ≤ 60, y edad ≥ 65.</p><p>Se prueba con casos visibles y con casos frontera ocultos.</p>`),
  func: {names: ['curb65'], cases: p => [
    {e: `curb65(${py(p.c[0])}, ${p.c.slice(1).join(', ')})`, vis: true},
    {e: 'curb65(False, 19, 29, 90, 61, 64)', vis: true},
    {e: 'curb65(True, 20, 30, 89, 60, 65)', vis: true},
    {e: 'curb65(False, 20, 30, 120, 80, 50)', vis: false},
    {e: 'curb65(False, 10, 18, 120, 60, 65)', vis: false}]},
  req: ['def'],
  sol: String.raw`def curb65(confusion, bun, fr, pas, pad, edad):
    puntos = 0
    if confusion:
        puntos += 1
    if bun > 19:
        puntos += 1
    if fr >= 30:
        puntos += 1
    if pas < 90 or pad <= 60:
        puntos += 1
    if edad >= 65:
        puntos += 1
    return puntos`,
  mut: [mutE('fronteras', String.raw`def curb65(confusion, bun, fr, pas, pad, edad):
    return int(confusion) + int(bun > 19) + int(fr > 30) + int(pas < 90 or pad < 60) + int(edad > 65)`, 'Fallas en los valores frontera: FR ≥ 30, PAD ≤ 60 y edad ≥ 65 incluyen el límite.'),
    mutE('tension_and', String.raw`def curb65(confusion, bun, fr, pas, pad, edad):
    return int(confusion) + int(bun > 19) + int(fr >= 30) + int(pas < 90 and pad <= 60) + int(edad >= 65)`, 'El criterio de presión se cumple con la PAS baja o con la PAD baja: or.')],
  pistas: [E('Un True sumado a un número vale 1: int(fr >= 30) da 1 o 0.'),
    E('Escribe la función con un if por criterio y un acumulador, y termina con return.'),
    E('Prueba tú los casos límite: FR = 30, PAD = 60, edad = 65.')]
});

M({id: 'm50-3', tema: 50, k: 'code', nivel: 3,
  t: E('Escala de coma de Glasgow: corrige la función del asistente'),
  gen: r => ({o: r.int(1, 4), v: r.int(1, 5), m: r.int(1, 6)}),
  data: () => '',
  starter: () => `# Función que ha propuesto el asistente. Pruébala con casos frontera y corrígela.
def glasgow(ocular, verbal, motora):
    total = ocular + verbal + motora
    if total > 13:
        gravedad = 'leve'
    elif total > 9:
        gravedad = 'moderado'
    else:
        gravedad = 'grave'
    return total, gravedad
`,
  enun: () => E(`<p>La escala de Glasgow suma la respuesta ocular (1-4), verbal (1-5) y motora (1-6). El traumatismo craneoencefálico se clasifica como <b>leve</b> (13-15), <b>moderado</b> (9-12) o <b>grave</b> (3-8).</p><p>Corrige <code>glasgow(ocular, verbal, motora)</code> para que devuelva la tupla <code>(total, gravedad)</code> y, si algún componente está fuera de su rango, devuelva <code>None</code>.</p>`),
  func: {names: ['glasgow'], cases: p => [{e: `glasgow(${p.o}, ${p.v}, ${p.m})`, vis: true}, {e: 'glasgow(4, 4, 5)', vis: true},
    {e: 'glasgow(3, 3, 3)', vis: false}, {e: 'glasgow(2, 2, 4)', vis: false}, {e: 'glasgow(5, 5, 6)', vis: false}, {e: 'glasgow(1, 1, 0)', vis: false}]},
  req: ['def'],
  sol: String.raw`def glasgow(ocular, verbal, motora):
    if not (1 <= ocular <= 4 and 1 <= verbal <= 5 and 1 <= motora <= 6):
        return None
    total = ocular + verbal + motora
    if total >= 13:
        gravedad = 'leve'
    elif total >= 9:
        gravedad = 'moderado'
    else:
        gravedad = 'grave'
    return total, gravedad`,
  mut: [mutE('asistente', String.raw`def glasgow(ocular, verbal, motora):
    total = ocular + verbal + motora
    if total > 13:
        gravedad = 'leve'
    elif total > 9:
        gravedad = 'moderado'
    else:
        gravedad = 'grave'
    return total, gravedad`, 'Es la versión del asistente: con 13 puntos debe ser leve y con 9, moderado; y no comprueba los rangos de cada componente.'),
    mutE('sin_rango', String.raw`def glasgow(ocular, verbal, motora):
    total = ocular + verbal + motora
    if total >= 13:
        gravedad = 'leve'
    elif total >= 9:
        gravedad = 'moderado'
    else:
        gravedad = 'grave'
    return total, gravedad`, 'Las fronteras ya están bien, pero un componente fuera de rango (por ejemplo, ocular = 5) debe devolver None.')],
  pistas: [E('Prueba glasgow(4, 4, 5): suma 13, que es un traumatismo leve.'),
    E('Comprueba los rangos al principio de la función con una condición encadenada: 1 <= ocular <= 4 and …'),
    E('return None termina la función sin seguir calculando.')]
});

/* ───── Tema 60 · Módulos, aleatoriedad y visualización con Matplotlib ───── */
QZ('m60-1', 60, 1, 'El gráfico adecuado para cada pregunta clínica', [
  ['¿Qué gráfico usarías para ver la distribución de la glucemia en 400 pacientes?', ['Histograma', 'Gráfico de sectores', 'Gráfico de líneas', 'Diagrama de barras de cada paciente'], 'El histograma muestra la forma de la distribución de una variable cuantitativa.'],
  ['¿Y para la evolución de la temperatura de un paciente ingresado cada 6 horas?', ['Gráfico de líneas con el tiempo en el eje X', 'Histograma', 'Gráfico de sectores', 'Diagrama de caja'], 'Una serie temporal se representa con líneas que unen las medidas en orden.'],
  ['¿Qué gráfico compara la PAS entre fumadores y no fumadores mostrando mediana, cuartiles y atípicos?', ['Diagrama de caja', 'Gráfico de sectores', 'Gráfico de líneas', 'Mapa de calor'], 'El diagrama de caja resume la distribución de cada grupo y permite compararlos.'],
  ['¿Qué gráfico muestra la relación entre el IMC y la PAS de cada paciente?', ['Gráfico de dispersión', 'Histograma', 'Diagrama de barras', 'Gráfico de sectores'], 'Cada punto es un paciente con sus dos valores: se ve la forma y la intensidad de la relación.']
]);

M({id: 'm60-2', tema: 60, k: 'code', nivel: 2,
  t: E('Aleatorizar 30 pacientes en tres brazos'),
  gen: r => ({sem: r.int(1, 9999)}),
  data: p => `import random\npacientes = [f"P{i:02d}" for i in range(1, 31)]\nsemilla = ${p.sem}`,
  enun: () => E(`<p>Aleatoriza los 30 pacientes en tres brazos (A, B y C) de 10 pacientes cada uno, de forma reproducible:</p><ol>
<li>Fija la semilla con <code>random.seed(semilla)</code>.</li>
<li>Crea la lista <code>brazos</code> con 10 <code>'A'</code>, 10 <code>'B'</code> y 10 <code>'C'</code>, en ese orden, y barájala con <code>random.shuffle(brazos)</code>.</li>
<li>Crea el diccionario <code>asignacion</code> que asocie cada paciente (en el orden de la lista) con su brazo.</li>
<li>Crea <code>conteo</code>: diccionario con el número de pacientes de cada brazo.</li></ol>`),
  out: ['brazos', 'asignacion', 'conteo'],
  sol: String.raw`random.seed(semilla)
brazos = ['A'] * 10 + ['B'] * 10 + ['C'] * 10
random.shuffle(brazos)
asignacion = dict(zip(pacientes, brazos))
conteo = {b: brazos.count(b) for b in 'ABC'}`,
  mut: [mutE('sin_semilla', String.raw`brazos = ['A'] * 10 + ['B'] * 10 + ['C'] * 10
random.shuffle(brazos)
asignacion = dict(zip(pacientes, brazos))
conteo = {b: brazos.count(b) for b in 'ABC'}`, 'Sin random.seed(semilla), cada ejecución da una aleatorización distinta: no es reproducible ni verificable.'),
    mutE('choice', String.raw`random.seed(semilla)
brazos = [random.choice('ABC') for _ in range(30)]
asignacion = dict(zip(pacientes, brazos))
conteo = {b: brazos.count(b) for b in 'ABC'}`, 'Elegir el brazo al azar paciente a paciente no garantiza 10 por brazo: baraja una lista que ya tiene 10 de cada.')],
  pistas: [E('La semilla debe fijarse justo antes de barajar.'),
    E('[\'A\'] * 10 crea una lista con diez A; las listas se suman con +.'),
    E('dict(zip(lista1, lista2)) empareja elemento a elemento.')]
});

M({id: 'm60-3', tema: 60, k: 'code', nivel: 3, pk: PK_MPL,
  t: E('Gráfico de evolución de la glucemia'),
  gen: r => { const n = r.int(6, 10); return {dias: Array.from({length: n}, (_, i) => i + 1), g: Array.from({length: n}, () => r.int(85, 260))}; },
  data: p => `import matplotlib.pyplot as plt\n${ARR('dias', p.dias)}\n${ARR('glucemia', p.g)}   # mg/dL en ayunas`,
  starter: () => `# Código que ha propuesto el asistente. Revisa que cumple las normas de un buen gráfico clínico.
plt.plot(glucemia)
plt.show()
`,
  enun: () => E(`<p>El asistente ha dibujado la glucemia, pero el gráfico no se puede interpretar. Corrígelo para que:</p><ul>
<li>dibuje la glucemia frente a los <b>días</b> (eje X) con puntos unidos por líneas (<code>'o-'</code>);</li>
<li>tenga el título <code>Evolución de la glucemia</code>, el eje X <code>Día de ingreso</code> y el eje Y <code>Glucemia (mg/dL)</code>.</li></ul>`),
  plot: {n_axes: 1, axes: [{data: true, marker: 'o', title: E('Evolución de la glucemia'), xlabel: E('Día de ingreso'), ylabel: E('Glucemia (mg/dL)')}]},
  sol: String.raw`plt.plot(dias, glucemia, 'o-')
plt.title('Evolución de la glucemia')
plt.xlabel('Día de ingreso')
plt.ylabel('Glucemia (mg/dL)')
plt.show()`,
  mut: [mutE('asistente', String.raw`plt.plot(glucemia)
plt.show()`, 'El gráfico del asistente usa las posiciones 0, 1, 2… como eje X y no tiene título, unidades ni marcadores.')],
  pistas: [E('plt.plot(x, y, \'o-\') dibuja puntos unidos por líneas.'),
    E('plt.title, plt.xlabel y plt.ylabel añaden los textos; las unidades van en la etiqueta del eje.')]
});

/* ───── Tema 70 · Ficheros y formatos de datos sanitarios: CSV y JSON ───── */
QZ('m70-1', 70, 1, 'Separadores, coma decimal y datos ausentes en un CSV', [
  ['Un CSV exportado de un hospital español tiene la línea «CV-001;67;5,8;». ¿Cuál es el separador de campos?', ['El punto y coma', 'La coma', 'El espacio', 'El guion'], 'En España se suele usar «;» como separador porque la coma es el separador decimal.'],
  ['En esa línea, ¿qué es «5,8»?', ['Un número decimal con coma: 5.8 para Python', 'Dos campos, 5 y 8', 'Un texto que no se puede convertir', 'Una fecha'], 'Al leerlo hay que cambiar la coma por un punto antes de float(), o indicar decimal="," a pandas.'],
  ['El último campo de «CV-001;67;5,8;» está vacío. ¿Qué significa?', ['Un dato ausente', 'Un cero', 'Un error del separador', 'El final del fichero'], 'Un campo vacío es un dato ausente y debe convertirse en None o NaN, no en 0.'],
  ['¿Por qué conviene abrir los ficheros con encoding="utf-8"?', ['Para leer bien las tildes y la ñ de los nombres y diagnósticos', 'Para que el fichero ocupe menos', 'Para cifrarlo', 'Para que se lea más rápido'], 'Si se usa otra codificación, «Gómez» puede aparecer como «GÃ³mez».']
]);

M({id: 'm70-2', tema: 70, k: 'code', nivel: 2,
  t: E('Leer un registro CSV de insuficiencia cardíaca'),
  gen: r => {
    const n = r.int(8, 12), filas = [];
    for (let i = 0; i < n; i++) filas.push([`IC-${String(i + 1).padStart(3, '0')}`, r.int(48, 92), r.bool(.25) ? '' : String(red(20 + r.next() * 45, 1)).replace('.', ',')]);
    if (!filas.some(f => f[2] === '')) filas[0][2] = '';
    return {filas};
  },
  data: p => `contenido = """id;edad;fevi\n${p.filas.map(f => f.join(';')).join('\n')}\n"""\nwith open('registro.csv', 'w', encoding='utf-8') as f:\n    f.write(contenido)`,
  enun: () => E(`<p>Los datos de arriba crean el fichero <code>registro.csv</code> (separador <code>;</code>, coma decimal y campos vacíos si falta la fracción de eyección). Léelo con el módulo <code>csv</code> y calcula:</p><ul>
<li><code>n_pacientes</code>: número de pacientes (sin contar la cabecera).</li>
<li><code>edad_media</code>: edad media, redondeada a 1 decimal.</li>
<li><code>sin_fevi</code>: número de pacientes sin FEVI registrada.</li>
<li><code>fevi_media</code>: FEVI media de los que la tienen, redondeada a 1 decimal.</li></ul>`),
  out: ['n_pacientes', 'edad_media', 'sin_fevi', 'fevi_media'],
  req: ['with'],
  sol: String.raw`import csv
with open('registro.csv', encoding='utf-8') as f:
    filas = list(csv.DictReader(f, delimiter=';'))
n_pacientes = len(filas)
edad_media = round(sum(int(x['edad']) for x in filas) / n_pacientes, 1)
fevis = [float(x['fevi'].replace(',', '.')) for x in filas if x['fevi'] != '']
sin_fevi = n_pacientes - len(fevis)
fevi_media = round(sum(fevis) / len(fevis), 1)`,
  mut: [mutE('ceros', String.raw`import csv
with open('registro.csv', encoding='utf-8') as f:
    filas = list(csv.DictReader(f, delimiter=';'))
n_pacientes = len(filas)
edad_media = round(sum(int(x['edad']) for x in filas) / n_pacientes, 1)
fevis = [float(x['fevi'].replace(',', '.')) if x['fevi'] else 0.0 for x in filas]
sin_fevi = sum(1 for x in filas if x['fevi'] == '')
fevi_media = round(sum(fevis) / len(fevis), 1)`, 'Un campo vacío es un dato ausente: si lo cuentas como 0, la FEVI media baja de forma artificial.'),
    mutE('cabecera', String.raw`with open('registro.csv', encoding='utf-8') as f:
    lineas = f.read().strip().split('\n')
n_pacientes = len(lineas)
filas = [l.split(';') for l in lineas[1:]]
edad_media = round(sum(int(x[1]) for x in filas) / len(filas), 1)
fevis = [float(x[2].replace(',', '.')) for x in filas if x[2] != '']
sin_fevi = len(filas) - len(fevis)
fevi_media = round(sum(fevis) / len(fevis), 1)`, 'n_pacientes incluye la línea de cabecera.')],
  pistas: [E('csv.DictReader(f, delimiter=";") da un diccionario por fila con las claves de la cabecera.'),
    E('Los valores leídos son textos: int(x["edad"]) y float(x["fevi"].replace(",", ".")).'),
    E('Filtra los vacíos con una condición en la comprensión: if x["fevi"] != "".')]
});

const LOINC = [['2339-0', 'Glucose [Mass/volume] in Blood', 'mg/dL', [70, 250]], ['718-7', 'Hemoglobin [Mass/volume] in Blood', 'g/dL', [8, 17]], ['2823-3', 'Potassium [Moles/volume] in Serum or Plasma', 'mmol/L', [3, 6]], ['2160-0', 'Creatinine [Mass/volume] in Serum or Plasma', 'mg/dL', [0.5, 3]]];
M({id: 'm70-3', tema: 70, k: 'code', nivel: 3,
  t: E('Extraer los datos de un recurso FHIR Observation'),
  gen: (r, j) => {
    const [cod, nom, ud, [a, b]] = j === undefined ? LOINC[0] : LOINC[1 + j];
    const d1 = `2026-${String(r.int(1, 12)).padStart(2, '0')}-${String(r.int(1, 28)).padStart(2, '0')}`;
    return {cod, nom, ud, v: red(a + r.next() * (b - a), 1), d1, d2: d1.slice(0, 8) + String(Math.min(28, +d1.slice(8) + 1)).padStart(2, '0'), id: `obs-${r.int(1000, 9999)}`};
  },
  data: p => `import json\nrecurso = '''${JSON.stringify({resourceType: 'Observation', id: p.id, status: 'final', code: {coding: [{system: 'http://loinc.org', code: p.cod, display: p.nom}]}, subject: {reference: 'Patient/ejemplo'}, effectiveDateTime: `${p.d1}T08:30:00+01:00`, issued: `${p.d2}T10:05:00+01:00`, valueQuantity: {value: p.v, unit: p.ud, system: 'http://unitsofmeasure.org'}}, null, 2)}'''`,
  starter: () => `# Código que ha propuesto el asistente. Pruébalo y corrígelo.
obs = json.loads(recurso)
valor = obs['valueQuantity']['value']
unidad = obs['valueQuantity']['unit']
fecha = obs['issued'][:10]
loinc = obs['code']['coding'][0]['display']
`,
  enun: () => E(`<p>El texto <code>recurso</code> es un recurso FHIR <i>Observation</i> en JSON. Obtén:</p><ul>
<li><code>valor</code> (número) y <code>unidad</code> (texto) del resultado;</li>
<li><code>fecha</code>: la fecha en que se <b>tomó</b> la muestra (<code>effectiveDateTime</code>), solo <code>AAAA-MM-DD</code>;</li>
<li><code>loinc</code>: el <b>código</b> LOINC de la prueba (por ejemplo, <code>'2339-0'</code>).</li></ul><p>Las pruebas ocultas usan otros recursos (hemoglobina, potasio, creatinina).</p>`),
  out: ['valor', 'unidad', 'fecha', 'loinc'],
  sol: String.raw`obs = json.loads(recurso)
valor = obs['valueQuantity']['value']
unidad = obs['valueQuantity']['unit']
fecha = obs['effectiveDateTime'][:10]
loinc = obs['code']['coding'][0]['code']`,
  mut: [mutE('asistente', String.raw`obs = json.loads(recurso)
valor = obs['valueQuantity']['value']
unidad = obs['valueQuantity']['unit']
fecha = obs['issued'][:10]
loinc = obs['code']['coding'][0]['display']`, 'El asistente toma «issued» (cuándo se emitió el informe) en lugar de «effectiveDateTime» (cuándo se tomó la muestra), y el nombre de la prueba en lugar de su código.')],
  pistas: [E('json.loads convierte el texto en diccionarios y listas de Python.'),
    E('Imprime obs.keys() para ver todos los campos del recurso.'),
    E('coding es una lista: su primer elemento es coding[0], con las claves system, code y display.')]
});

/* ───── Tema 80 · Modelos de lenguaje ───── */
QZ('m80-1', 80, 1, 'La temperatura y las distribuciones de probabilidad', [
  ['Un modelo asigna a la siguiente palabra las probabilidades «neumonía» 0,6, «bronquitis» 0,3, «asma» 0,1. Si baja la temperatura, ¿qué ocurre?', ['«Neumonía» se vuelve aún más probable', 'Las tres se igualan', '«Asma» se vuelve la más probable', 'Las probabilidades no cambian'], 'Una temperatura baja concentra la probabilidad en la opción más probable; una alta la reparte.'],
  ['Con temperatura muy alta, ¿cómo serán las respuestas del modelo?', ['Más variadas y con más riesgo de incoherencias', 'Siempre idénticas', 'Más cortas', 'Más precisas'], 'Al repartir la probabilidad, el modelo elige con más frecuencia palabras poco probables.'],
  ['¿Qué temperatura conviene para extraer datos estructurados de un informe clínico?', ['Baja (0 a 0,2)', 'Alta (1,5 a 2)', 'Da igual', 'La máxima permitida'], 'Para extracción y clasificación interesa una respuesta estable y reproducible.'],
  ['Con temperatura 0, ¿garantiza el modelo que la respuesta sea correcta?', ['No: será la más probable, no necesariamente la verdadera', 'Sí, siempre', 'Sí, si la pregunta es médica', 'Solo si se pide en inglés'], 'La temperatura controla la variabilidad, no la veracidad: un modelo puede dar siempre la misma respuesta equivocada.']
]);

const CAT_IMC = imc => imc < 18.5 ? 'bajo peso' : imc < 25 ? 'normal' : imc < 30 ? 'sobrepeso' : 'obesidad';
M({id: 'm80-2', tema: 80, k: 'code', nivel: 2,
  t: E('Verificar las clasificaciones de IMC que devuelve un modelo'),
  gen: r => {
    const imcs = Array.from({length: 5}, () => r.pick([18.5, 24.9, 25, 29.9, 30, red(16 + r.next() * 22, 1)]));
    const malas = new Set(r.sample([0, 1, 2, 3, 4], r.int(1, 2)));
    const cats = ['bajo peso', 'normal', 'sobrepeso', 'obesidad'];
    return {res: imcs.map((v, i) => ({paciente: i + 1, imc: v, categoria: malas.has(i) ? r.pick(cats.filter(c => c !== CAT_IMC(v))) : CAT_IMC(v)}))};
  },
  data: p => `import json\nrespuesta_modelo = '${JSON.stringify(p.res)}'`,
  enun: () => E(`<p>Has pedido al modelo que clasifique cinco IMC y que responda en JSON. Comprueba su respuesta con tu propio código:</p><ul>
<li>Define <code>clasifica_imc(imc)</code>: <code>'bajo peso'</code> (&lt; 18,5), <code>'normal'</code> (18,5 a &lt; 25), <code>'sobrepeso'</code> (25 a &lt; 30), <code>'obesidad'</code> (≥ 30).</li>
<li><code>errores</code>: lista con el número de <code>paciente</code> de las clasificaciones del modelo que no coinciden con la tuya, en orden.</li>
<li><code>exactitud</code>: proporción de clasificaciones correctas del modelo, redondeada a 2 decimales.</li></ul>`),
  out: ['errores', 'exactitud'],
  func: {names: ['clasifica_imc'], cases: () => [{e: 'clasifica_imc(18.5)', vis: true}, {e: 'clasifica_imc(30)', vis: true}, {e: 'clasifica_imc(24.99)', vis: false}]},
  sol: String.raw`def clasifica_imc(imc):
    if imc < 18.5:
        return 'bajo peso'
    elif imc < 25:
        return 'normal'
    elif imc < 30:
        return 'sobrepeso'
    return 'obesidad'

datos = json.loads(respuesta_modelo)
errores = [d['paciente'] for d in datos if d['categoria'] != clasifica_imc(d['imc'])]
exactitud = round(1 - len(errores) / len(datos), 2)`,
  mut: [mutE('frontera', String.raw`def clasifica_imc(imc):
    if imc <= 18.5:
        return 'bajo peso'
    elif imc <= 25:
        return 'normal'
    elif imc <= 30:
        return 'sobrepeso'
    return 'obesidad'

datos = json.loads(respuesta_modelo)
errores = [d['paciente'] for d in datos if d['categoria'] != clasifica_imc(d['imc'])]
exactitud = round(1 - len(errores) / len(datos), 2)`, 'Los límites de la OMS pertenecen a la categoría superior: un IMC de 25 ya es sobrepeso. Usa «<».')],
  pistas: [E('json.loads(respuesta_modelo) da una lista de diccionarios con las claves paciente, imc y categoria.'),
    E('Si tu función se equivoca en las fronteras, culparás al modelo de errores que son tuyos.')]
});

M({id: 'm80-3', tema: 80, k: 'code', nivel: 3,
  t: E('Verificar las referencias que propone un modelo'),
  gen: r => {
    const base = [['Glycated haemoglobin and cardiovascular risk', '10.1056/NEJMoa0802987'], ['Interpreting diagnostic accuracy studies', '10.1136/bmj.39489.470347.AD'], ['Statistics notes: Absence of evidence is not evidence of absence', '10.1136/bmj.311.7003.485'], ['Calibration: the Achilles heel of predictive analytics', '10.1186/s12916-019-1466-7'], ['TRIPOD+AI statement', '10.1136/bmj-2023-078378']];
    const reg = Object.fromEntries(base.map(([tit, doi]) => [doi, tit]));
    const refs = r.sample(base, 3).map(([tit, doi]) => {
      const k = r.int(0, 3);
      return k === 0 ? {titulo: tit, doi: '10.1000/' + r.int(10000, 99999)} : k === 1 ? {titulo: 'Machine learning ' + tit.toLowerCase(), doi} : {titulo: tit, doi};
    });
    return {reg, refs};
  },
  data: p => `registro_doi = ${py(p.reg)}   # lo que devuelve el registro de DOI (simulado)\nreferencias = ${py(p.refs)}   # lo que ha propuesto el modelo`,
  enun: () => E(`<p>Has pedido al modelo tres referencias y te ha dado las de <code>referencias</code>. El diccionario <code>registro_doi</code> simula la consulta al registro de DOI: asocia cada DOI existente con su título real.</p><p>Una referencia es <b>correcta</b> si su DOI existe en el registro <b>y</b> el título coincide (sin distinguir mayúsculas ni espacios de los extremos). Calcula:</p><ul>
<li><code>correctas</code>: lista de las posiciones (0, 1, 2) de las referencias correctas.</li>
<li><code>proporcion</code>: proporción de referencias correctas, redondeada a 2 decimales.</li></ul>`),
  out: ['correctas', 'proporcion'],
  sol: String.raw`def normaliza(texto):
    return texto.strip().lower()

correctas = []
for i, ref in enumerate(referencias):
    titulo_real = registro_doi.get(ref['doi'])
    if titulo_real is not None and normaliza(titulo_real) == normaliza(ref['titulo']):
        correctas.append(i)
proporcion = round(len(correctas) / len(referencias), 2)`,
  mut: [mutE('solo_doi', String.raw`correctas = [i for i, ref in enumerate(referencias) if ref['doi'] in registro_doi]
proporcion = round(len(correctas) / len(referencias), 2)`, 'Que el DOI exista no basta: el modelo puede pegar un DOI real a un título que no le corresponde.')],
  pistas: [E('registro_doi.get(doi) devuelve None si el DOI no existe, en lugar de dar error.'),
    E('enumerate(referencias) da a la vez la posición y la referencia.')]
});
