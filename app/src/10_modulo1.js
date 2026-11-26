/* ══ Módulo 1 · Descubriendo Python (temas 10 a 40) ══ */
const NOM_NIVEL = {1: 'básica', 2: 'clínica', 3: 'reto'};

/* ───── Tema 10 · Introducción a la bioestadística computacional ───── */
QZ('m10-1', 10, 1, 'Tipos de variables de una historia clínica', [
  ['En una historia clínica sintética, ¿qué tipo de variable es el «grupo sanguíneo» (A, B, AB, 0)?',
    ['Cualitativa nominal', 'Cualitativa ordinal', 'Cuantitativa discreta', 'Cuantitativa continua'],
    'Las categorías del grupo sanguíneo no tienen un orden natural: es una variable cualitativa nominal.'],
  ['¿Y el estadio de la insuficiencia cardíaca según la NYHA (I, II, III, IV)?',
    ['Cualitativa ordinal', 'Cualitativa nominal', 'Cuantitativa continua', 'Cuantitativa de razón'],
    'Las clases NYHA tienen un orden de gravedad, pero la distancia entre ellas no es una cantidad medible.'],
  ['¿Qué tipo de variable es el número de ingresos hospitalarios en el último año?',
    ['Cuantitativa discreta', 'Cuantitativa continua', 'Cualitativa ordinal', 'Cualitativa nominal'],
    'Es un recuento: solo toma valores enteros (0, 1, 2…).'],
  ['La temperatura en grados Celsius es una variable cuantitativa de intervalo, no de razón. ¿Por qué?',
    ['Porque su cero es arbitrario: 40 °C no es «el doble de calor» que 20 °C', 'Porque solo toma valores enteros', 'Porque tiene pocas categorías', 'Porque se mide con un termómetro'],
    'En una escala de razón el cero significa ausencia de la magnitud (como en el peso). En grados Celsius el cero es un convenio.']
]);

M({id: 'm10-2', tema: 10, k: 'code', nivel: 2,
  t: E('IMC, presión arterial media y superficie corporal'),
  gen: r => ({peso: red(45 + r.next() * 70, 1), talla: r.int(150, 195), pas: r.int(95, 175), pad: r.int(55, 105)}),
  data: p => `peso = ${p.peso}       # kg\ntalla_cm = ${p.talla}    # cm\npas = ${p.pas}          # mmHg\npad = ${p.pad}          # mmHg`,
  enun: () => E(`<p>Calcula con las variables de arriba:</p><ul>
<li><code>imc</code>: índice de masa corporal = peso / talla², con la talla <b>en metros</b>, redondeado a 1 decimal.</li>
<li><code>pam</code>: presión arterial media = (PAS + 2·PAD) / 3, redondeada a 1 decimal.</li>
<li><code>sc</code>: superficie corporal de Mosteller = √(talla en cm · peso / 3600), en m², redondeada a 2 decimales.</li>
<li><code>obesidad</code>: <code>True</code> si el IMC (ya redondeado) es 30 o más.</li></ul>`),
  out: ['imc', 'pam', 'sc', 'obesidad'],
  sol: String.raw`imc = round(peso / (talla_cm / 100) ** 2, 1)
pam = round((pas + 2 * pad) / 3, 1)
sc = round((talla_cm * peso / 3600) ** 0.5, 2)
obesidad = imc >= 30`,
  mut: [
    mutE('talla_cm', String.raw`imc = round(peso / talla_cm ** 2, 1)
pam = round((pas + 2 * pad) / 3, 1)
sc = round((talla_cm * peso / 3600) ** 0.5, 2)
obesidad = imc >= 30`, 'El IMC usa la talla en metros: divide los centímetros entre 100 antes de elevar al cuadrado.'),
    mutE('por2', String.raw`imc = round(peso / (talla_cm / 100) * 2, 1)
pam = round((pas + 2 * pad) / 3, 1)
sc = round((talla_cm * peso / 3600) ** 0.5, 2)
obesidad = imc >= 30`, 'En Python el cuadrado se escribe ** 2; * 2 multiplica por dos.'),
    mutE('pam_media', String.raw`imc = round(peso / (talla_cm / 100) ** 2, 1)
pam = round((pas + pad) / 2, 1)
sc = round((talla_cm * peso / 3600) ** 0.5, 2)
obesidad = imc >= 30`, 'La PAM no es la media de PAS y PAD: la diástole dura más que la sístole, por eso la PAD cuenta dos veces.'),
    mutE('sc_metros', String.raw`imc = round(peso / (talla_cm / 100) ** 2, 1)
pam = round((pas + 2 * pad) / 3, 1)
sc = round((talla_cm / 100 * peso / 3600) ** 0.5, 2)
obesidad = imc >= 30`, 'La fórmula de Mosteller usa la talla en centímetros, no en metros.')
  ],
  pistas: [E('Los paréntesis importan: (talla_cm / 100) ** 2 primero convierte a metros y luego eleva al cuadrado.'),
    E('La raíz cuadrada de x se puede escribir x ** 0.5 (o math.sqrt(x) tras import math).'),
    E('round(valor, 1) redondea a 1 decimal; una comparación como imc >= 30 ya da True o False.')]
});

QZ('m10-3', 10, 3, 'Trabajar con un asistente de IA y una clave de API', [
  ['¿Dónde debe guardarse tu clave de API para usarla en un cuaderno de Colab?',
    ['En los Secretos de Colab, y leerla con userdata.get', 'Escrita en una celda de código, para no perderla', 'En una celda de texto del cuaderno', 'En el nombre del cuaderno'],
    'Una clave escrita en el cuaderno viaja con él si lo compartes o lo subes a GitHub. Los Secretos de Colab no se copian con el cuaderno.'],
  ['Vas a pedir al asistente ayuda con un análisis de tu servicio. ¿Qué no debes enviarle nunca?',
    ['Datos de pacientes reales, aunque quites el nombre', 'El enunciado del ejercicio', 'Tu propio código con datos sintéticos', 'El mensaje de error de Python'],
    'Los datos clínicos reales son datos de salud protegidos: no se envían a un proveedor externo sin una base legal y un acuerdo de tratamiento.'],
  ['El asistente te propone un código que calcula el IMC y da 2.45 para un paciente de 70 kg y 169 cm. ¿Qué haces?',
    ['Compruebo el resultado con un caso que sé calcular a mano: debería dar unos 24,5', 'Lo acepto: el asistente no se equivoca en cuentas', 'Le pido que lo repita hasta que dé otro número', 'Cambio de modelo de IA'],
    'Verificar con un caso conocido es la base de la programación asistida: 70 / 1,69² ≈ 24,5. El código tiene un error de unidades o de orden de operaciones.'],
  ['Has pegado por error tu clave en un chat público. ¿Qué es lo correcto?',
    ['Revocarla en la web del proveedor y crear una nueva', 'Borrar el mensaje y seguir usándola', 'Esperar a ver si alguien la usa', 'Cambiar la contraseña de tu correo'],
    'Una clave expuesta debe considerarse comprometida: se revoca y se genera otra.']
]);

/* ───── Tema 20 · Representación de datos clínicos en Python ───── */
QZ('m20-1', 20, 1, 'El tipo de dato de cada campo', [
  ['¿Qué tipo de Python es más adecuado para la frecuencia cardíaca en latidos por minuto (72)?',
    ['int', 'str', 'float', 'bool'], 'Es un recuento entero de latidos: int.'],
  ['¿Y para la lista de diagnósticos de un paciente, que puede tener varios y cambiar?',
    ['list', 'str', 'int', 'tuple de un elemento'], 'Una lista guarda varios valores en orden y se puede ampliar.'],
  ['¿Qué tipo usarías para «¿es alérgico a la penicilina?»?',
    ['bool', 'str', 'float', 'list'], 'Es una pregunta de sí o no: True o False.'],
  ['Falta la determinación de la creatinina. ¿Cómo la representas en Python?',
    ['None', '0', "''", 'False'], 'None indica «sin dato». Un 0 sería un valor (imposible) de creatinina y falsearía los cálculos.']
]);

const SEXOS_TXT = ['mujer', 'hombre'];
const DX_TXT = ['hta', 'dm2', 'epoc', 'fa', 'asma', 'icc', 'erc'];
const mezcla = (r, s) => s.split('').map(ch => r.bool() ? ch.toUpperCase() : ch.toLowerCase()).join('');
M({id: 'm20-2', tema: 20, k: 'code', nivel: 2,
  t: E('Limpiar un texto exportado de la historia clínica'),
  gen: r => {
    const n = r.pick(NOMBRES).split(' '), dx = r.sample(DX_TXT, r.int(1, 3));
    const sp = () => ' '.repeat(r.int(0, 2));
    return {texto: `${sp()}${mezcla(r, n[1])}${sp()};${sp()}${mezcla(r, n[0])}${sp()};${sp()}${r.int(18, 95)}${sp()};${sp()}${dx.map(d => mezcla(r, d)).join(sp() + ',' + sp())}${sp()}`};
  },
  data: p => `texto = ${py(p.texto)}   # apellido ; nombre ; edad ; diagnósticos separados por comas`,
  enun: () => E(`<p>El sistema exporta cada paciente como una línea de texto con los campos separados por <code>;</code>, con espacios sobrantes y mayúsculas al azar. Construye el diccionario <code>paciente</code> con las claves:</p><ul>
<li><code>'apellido'</code> y <code>'nombre'</code>: sin espacios sobrantes y con la inicial en mayúscula (<code>.strip().title()</code>).</li>
<li><code>'edad'</code>: como número entero.</li>
<li><code>'diagnosticos'</code>: lista de los diagnósticos, sin espacios y en mayúsculas, en el orden del texto.</li></ul>`),
  out: ['paciente'],
  sol: String.raw`campos = texto.split(';')
paciente = {
    'apellido': campos[0].strip().title(),
    'nombre': campos[1].strip().title(),
    'edad': int(campos[2]),
    'diagnosticos': [d.strip().upper() for d in campos[3].split(',')],
}`,
  mut: [
    mutE('edad_txt', String.raw`campos = texto.split(';')
paciente = {'apellido': campos[0].strip().title(), 'nombre': campos[1].strip().title(), 'edad': campos[2].strip(), 'diagnosticos': [d.strip().upper() for d in campos[3].split(',')]}`, 'La edad sigue siendo un texto: conviértela con int(...) para poder calcular con ella.'),
    mutE('dx_sin_strip', String.raw`campos = texto.split(';')
paciente = {'apellido': campos[0].strip().title(), 'nombre': campos[1].strip().title(), 'edad': int(campos[2]), 'diagnosticos': [d.upper() for d in campos[3].split(',')]}`, 'Cada diagnóstico conserva los espacios de alrededor: aplica .strip() a cada uno.'),
    mutE('sin_title', String.raw`campos = texto.split(';')
paciente = {'apellido': campos[0].strip(), 'nombre': campos[1].strip(), 'edad': int(campos[2]), 'diagnosticos': [d.strip().upper() for d in campos[3].split(',')]}`, 'Faltan las mayúsculas iniciales del nombre y del apellido: .title().')
  ],
  pistas: [E('texto.split(";") devuelve una lista con los cuatro campos.'),
    E('int(" 67 ") funciona aunque haya espacios alrededor.'),
    E('Para los diagnósticos: separa el cuarto campo por comas y recorre la lista con una comprensión: [d.strip().upper() for d in ...].')]
});

M({id: 'm20-3', tema: 20, k: 'code', nivel: 3,
  t: E('Media de una serie con valores ausentes'),
  gen: (r, j) => {
    const n = r.int(8, 12), v = Array.from({length: n}, () => r.int(70, 240));
    const k = j === 1 ? 1 : r.int(2, 4); r.sample([...v.keys()], k).forEach(i => { v[i] = null; });
    return {v};
  },
  data: p => ARR('glucemias', p.v) + '   # mg/dL; None = no se pudo medir',
  starter: () => `# Código que ha propuesto el asistente. Compruébalo y corrígelo.
media = round(sum(g if g is not None else 0 for g in glucemias) / len(glucemias), 1)
n_validos = len(glucemias)
`,
  enun: () => E(`<p>El asistente ha escrito el código de abajo para calcular la glucemia media de la serie. Verifícalo con un caso que sepas calcular y corrígelo. Debes obtener:</p><ul>
<li><code>n_validos</code>: número de determinaciones que no son <code>None</code>.</li>
<li><code>media</code>: media de las determinaciones válidas, redondeada a 1 decimal. Un valor ausente <b>no</b> es un cero.</li></ul>`),
  out: ['media', 'n_validos'],
  sol: String.raw`validos = [g for g in glucemias if g is not None]
n_validos = len(validos)
media = round(sum(validos) / n_validos, 1)`,
  mut: [mutE('ceros', String.raw`media = round(sum(g if g is not None else 0 for g in glucemias) / len(glucemias), 1)
n_validos = len(glucemias)`, 'Es el error del asistente: tratar los ausentes como ceros baja la media y cuenta pacientes sin dato.')],
  pistas: [E('Prueba el código del asistente con [100, None, 200]: ¿cuánto debería dar la media?'),
    E('Una comprensión con condición filtra la lista: [g for g in glucemias if g is not None].'),
    E('La media es la suma de los válidos dividida entre el número de válidos.')]
});

/* ───── Tema 30 · Lógica booleana y estructuras condicionales ───── */
QZ('m30-1', 30, 1, 'Predecir comparaciones y condiciones', [
  ['Con pas = 140 y pad = 85, ¿qué vale pas >= 140 or pad >= 90?', ['True', 'False', '140', 'Da error'], 'Basta con que una de las dos condiciones sea cierta: 140 >= 140 es True.'],
  ['Con glucemia = 126, ¿qué vale 100 <= glucemia < 126?', ['False', 'True', '126', 'Da error'], 'El límite superior es estricto: 126 < 126 es False.'],
  ['Con fiebre = True y tos = False, ¿qué vale fiebre and not tos?', ['True', 'False', 'None', 'Da error'], 'not tos es True, y True and True es True.'],
  ['¿Qué imprime este código con edad = 65? if edad > 65: print("A") elif edad >= 18: print("B") else: print("C")', ['B', 'A', 'C', 'A y B'], '65 > 65 es False, así que pasa al elif: 65 >= 18 es True y se imprime B. Solo se ejecuta una rama.']
]);

M({id: 'm30-2', tema: 30, k: 'code', nivel: 2,
  t: E('Clasificar la glucemia en ayunas y la presión arterial'),
  gen: (r, j) => {
    if (j !== undefined) return j === 0 ? {glu: 126, pas: 140, pad: 70} : {glu: 100, pas: 128, pad: 85};
    return {glu: r.int(70, 160), pas: r.int(100, 175), pad: r.int(60, 105)};
  },
  data: p => `glucemia = ${p.glu}   # mg/dL en ayunas\npas = ${p.pas}\npad = ${p.pad}`,
  enun: () => E(`<p>Crea dos variables de texto con <code>if</code>/<code>elif</code>/<code>else</code>:</p><ul>
<li><code>cat_glucemia</code>: <code>'normal'</code> si es menor de 100; <code>'prediabetes'</code> de 100 a 125; <code>'diabetes'</code> si es 126 o más.</li>
<li><code>cat_pa</code>: <code>'hipertensión'</code> si PAS ≥ 140 <b>o</b> PAD ≥ 90; si no, <code>'normal-alta'</code> si PAS ≥ 130 o PAD ≥ 85; si no, <code>'normal'</code>.</li></ul><p>Las pruebas ocultas usan los valores frontera.</p>`),
  out: ['cat_glucemia', 'cat_pa'],
  req: ['if'],
  sol: String.raw`if glucemia < 100:
    cat_glucemia = 'normal'
elif glucemia <= 125:
    cat_glucemia = 'prediabetes'
else:
    cat_glucemia = 'diabetes'

if pas >= 140 or pad >= 90:
    cat_pa = 'hipertensión'
elif pas >= 130 or pad >= 85:
    cat_pa = 'normal-alta'
else:
    cat_pa = 'normal'`,
  mut: [
    mutE('frontera_126', String.raw`if glucemia < 100:
    cat_glucemia = 'normal'
elif glucemia <= 126:
    cat_glucemia = 'prediabetes'
else:
    cat_glucemia = 'diabetes'
if pas >= 140 or pad >= 90:
    cat_pa = 'hipertensión'
elif pas >= 130 or pad >= 85:
    cat_pa = 'normal-alta'
else:
    cat_pa = 'normal'`, 'Una glucemia de 126 mg/dL ya es diagnóstica de diabetes: el tramo de prediabetes acaba en 125.'),
    mutE('and', String.raw`if glucemia < 100:
    cat_glucemia = 'normal'
elif glucemia <= 125:
    cat_glucemia = 'prediabetes'
else:
    cat_glucemia = 'diabetes'
if pas >= 140 and pad >= 90:
    cat_pa = 'hipertensión'
elif pas >= 130 and pad >= 85:
    cat_pa = 'normal-alta'
else:
    cat_pa = 'normal'`, 'Basta con que la PAS o la PAD superen el umbral: usa or, no and.'),
    mutE('estricto', String.raw`if glucemia < 100:
    cat_glucemia = 'normal'
elif glucemia <= 125:
    cat_glucemia = 'prediabetes'
else:
    cat_glucemia = 'diabetes'
if pas > 140 or pad > 90:
    cat_pa = 'hipertensión'
elif pas > 130 or pad > 85:
    cat_pa = 'normal-alta'
else:
    cat_pa = 'normal'`, 'Los umbrales están incluidos: una PAS de 140 ya es hipertensión. Usa >=.')
  ],
  pistas: [E('Ordena las condiciones de mayor a menor gravedad: el primer if que se cumple gana.'),
    E('«De 100 a 125» incluye los dos extremos.'),
    E('«PAS ≥ 140 o PAD ≥ 90» se escribe pas >= 140 or pad >= 90.')]
});

M({id: 'm30-3', tema: 30, k: 'code', nivel: 3,
  t: E('Escala CURB-65 de gravedad de la neumonía'),
  gen: (r, j) => j === undefined ? {conf: r.bool(.3), bun: r.int(8, 40), fr: r.int(14, 36), pas: r.int(80, 150), pad: r.int(50, 95), edad: r.int(30, 92)}
    : j === 0 ? {conf: false, bun: 19, fr: 30, pas: 95, pad: 60, edad: 65} : {conf: true, bun: 20, fr: 29, pas: 89, pad: 61, edad: 64},
  data: p => `confusion = ${py(p.conf)}\nbun = ${p.bun}         # nitrógeno ureico en mg/dL\nfr = ${p.fr}          # respiraciones por minuto\npas = ${p.pas}\npad = ${p.pad}\nedad = ${p.edad}`,
  starter: () => `# Código que ha propuesto el asistente. Verifícalo con casos frontera y corrígelo.
curb = 0
if confusion:
    curb += 1
if bun > 19:
    curb += 1
if fr > 30:
    curb += 1
if pas < 90 or pad < 60:
    curb += 1
if edad > 65:
    curb += 1
if curb <= 1:
    riesgo = 'bajo'
elif curb == 2:
    riesgo = 'intermedio'
else:
    riesgo = 'alto'
`,
  enun: () => E(`<p>CURB-65 suma un punto por cada criterio: <b>C</b>onfusión; <b>U</b>rea elevada (BUN &gt; 19 mg/dL); frecuencia <b>R</b>espiratoria ≥ 30; presión arterial (<b>B</b>lood pressure) sistólica &lt; 90 o diastólica ≤ 60; edad ≥ <b>65</b>.</p><p>Revisa el código del asistente frente a esta definición y obtén <code>curb</code> (0 a 5) y <code>riesgo</code>: <code>'bajo'</code> (0-1), <code>'intermedio'</code> (2) o <code>'alto'</code> (3 o más).</p>`),
  out: ['curb', 'riesgo'],
  sol: String.raw`curb = 0
if confusion:
    curb += 1
if bun > 19:
    curb += 1
if fr >= 30:
    curb += 1
if pas < 90 or pad <= 60:
    curb += 1
if edad >= 65:
    curb += 1
if curb <= 1:
    riesgo = 'bajo'
elif curb == 2:
    riesgo = 'intermedio'
else:
    riesgo = 'alto'`,
  mut: [mutE('asistente', String.raw`curb = 0
if confusion:
    curb += 1
if bun > 19:
    curb += 1
if fr > 30:
    curb += 1
if pas < 90 or pad < 60:
    curb += 1
if edad > 65:
    curb += 1
if curb <= 1:
    riesgo = 'bajo'
elif curb == 2:
    riesgo = 'intermedio'
else:
    riesgo = 'alto'`, 'Siguen los fallos del asistente en las fronteras: FR ≥ 30, PAD ≤ 60 y edad ≥ 65 incluyen el valor límite.')],
  pistas: [E('Prueba mentalmente un paciente de 65 años con FR 30 y PAD 60: ¿cuántos puntos debería tener?'),
    E('Compara cada desigualdad del código con la definición: ¿«≥» o «>»? ¿«≤» o «<»?'),
    E('Hay tres criterios mal escritos en el código del asistente.')]
});

/* ───── Tema 40 · Estructuras iterativas: series de pacientes ───── */
M({id: 'm40-1', tema: 40, k: 'predict', nivel: 1,
  t: E('¿Cuántas vueltas da el bucle?'),
  gen: r => { const umbral = r.pick([90, 100, 110]); return {fc: r.shuffle([umbral, ...Array.from({length: r.int(4, 7)}, () => r.int(48, 130))]), umbral}; },
  predict: p => `taquicardias = 0
vueltas = 0
for fc in ${py(p.fc)}:
    vueltas += 1
    if fc > ${p.umbral}:
        taquicardias += 1
print(vueltas)
print(taquicardias)`,
  enun: p => E(`<p>Lee el programa y escribe lo que imprimirá, una línea por cada <code>print</code>. El umbral de taquicardia es <b>mayor que</b> ${p.umbral} lpm.</p>`),
  mut: [{id: 'mayor_igual', alt: p => `${p.fc.length}\n${p.fc.filter(x => x >= p.umbral).length}`, msg: E('Fíjate en que la condición es «>»: una FC igual al umbral no cuenta.')},
    {id: 'indice', alt: p => `${p.fc.length - 1}\n${p.fc.filter(x => x > p.umbral).length}`, msg: E('El contador empieza en 0 y suma 1 en cada vuelta: al final vale el número de elementos de la lista.')}],
  pistas: []
});

M({id: 'm40-2', tema: 40, k: 'code', nivel: 2,
  t: E('Prevalencia de hipertensión e IMC de una serie de pacientes'),
  gen: r => { const n = r.int(10, 16); return {pas: r.ints(n, 105, 175), pad: r.ints(n, 60, 105), peso: Array.from({length: n}, () => red(48 + r.next() * 60, 1)), talla: Array.from({length: n}, () => red(1.5 + r.next() * 0.42, 2))}; },
  data: p => [ARR('pas', p.pas), ARR('pad', p.pad), ARR('peso', p.peso), ARR('talla', p.talla) + '   # m'].join('\n'),
  enun: () => E(`<p>Cada posición de las listas es un paciente. Recorre las listas con un bucle <code>for</code> y calcula:</p><ul>
<li><code>n_hta</code>: número de pacientes con PAS ≥ 140 o PAD ≥ 90.</li>
<li><code>prevalencia</code>: porcentaje de pacientes con hipertensión, redondeado a 1 decimal.</li>
<li><code>imcs</code>: lista con el IMC de cada paciente (peso / talla²), redondeado a 1 decimal, en el mismo orden.</li></ul>`),
  out: ['n_hta', 'prevalencia', 'imcs'],
  req: ['for'],
  sol: String.raw`n_hta = 0
imcs = []
for i in range(len(pas)):
    if pas[i] >= 140 or pad[i] >= 90:
        n_hta += 1
    imcs.append(round(peso[i] / talla[i] ** 2, 1))
prevalencia = round(n_hta / len(pas) * 100, 1)`,
  mut: [mutE('and', String.raw`n_hta = 0
imcs = []
for i in range(len(pas)):
    if pas[i] >= 140 and pad[i] >= 90:
        n_hta += 1
    imcs.append(round(peso[i] / talla[i] ** 2, 1))
prevalencia = round(n_hta / len(pas) * 100, 1)`, 'Un paciente es hipertenso si cumple cualquiera de los dos criterios: or.'),
    mutE('proporcion', String.raw`n_hta = 0
imcs = []
for i in range(len(pas)):
    if pas[i] >= 140 or pad[i] >= 90:
        n_hta += 1
    imcs.append(round(peso[i] / talla[i] ** 2, 1))
prevalencia = round(n_hta / len(pas), 1)`, 'Se pide un porcentaje: multiplica la proporción por 100.')],
  pistas: [E('for i in range(len(pas)) recorre las posiciones 0, 1, 2… y te deja usar pas[i], pad[i], peso[i]…'),
    E('Empieza con n_hta = 0 e imcs = [] antes del bucle; dentro, suma 1 o añade con .append(...).'),
    E('La prevalencia se calcula después del bucle, cuando ya conoces n_hta.')]
});

M({id: 'm40-3', tema: 40, k: 'code', nivel: 3,
  t: E('Dosis hasta el estado estacionario con while'),
  gen: r => ({dosis: r.pick([100, 250, 500, 1000]), f: red(0.3 + r.next() * 0.55, 2)}),
  data: p => `dosis = ${p.dosis}    # mg por dosis\nf = ${p.f}       # fracción del fármaco que queda en el cuerpo al llegar la dosis siguiente`,
  starter: () => `# Código que ha propuesto el asistente. Verifícalo y corrígelo.
css = dosis / (1 - f)
c = dosis
n_dosis = 0
while c < 0.9 * css:
    c = c * f + dosis
    n_dosis += 1
c_final = round(c, 2)
`,
  enun: () => E(`<p>Justo después de cada dosis, la cantidad en el cuerpo es la que quedaba (<code>c · f</code>) más la nueva dosis. Antes de la primera dosis no hay fármaco (<code>c = 0</code>). La cantidad tiende a <code>css = dosis / (1 − f)</code>.</p>
<p>Con un bucle <code>while</code>, calcula <code>n_dosis</code>: cuántas dosis hacen falta para que, justo después de una dosis, la cantidad alcance al menos el 90 % de <code>css</code>; y <code>c_final</code>: esa cantidad, redondeada a 2 decimales. Revisa el código del asistente.</p>`),
  out: ['n_dosis', 'c_final'],
  req: ['while'],
  sol: String.raw`css = dosis / (1 - f)
c = 0
n_dosis = 0
while c < 0.9 * css:
    c = c * f + dosis
    n_dosis += 1
c_final = round(c, 2)`,
  mut: [mutE('asistente', String.raw`css = dosis / (1 - f)
c = dosis
n_dosis = 0
while c < 0.9 * css:
    c = c * f + dosis
    n_dosis += 1
c_final = round(c, 2)`, 'El asistente empieza con c = dosis pero n_dosis = 0: cuenta una dosis de menos. Antes de la primera dosis, c = 0.')],
  pistas: [E('Simula a mano con dosis = 100 y f = 0,5: tras la 1.ª dosis hay 100; tras la 2.ª, 150; tras la 3.ª, 175… y css = 200.'),
    E('El estado inicial debe ser coherente: si todavía no hay ninguna dosis, la cantidad es 0.')]
});
