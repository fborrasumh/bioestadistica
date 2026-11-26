/* ══ Módulo 5 · Generalización de conclusiones (temas 200 a 300). El examen de este módulo es con Colab. ══ */

/* ───── Tema 200 · Estimación puntual e intervalos de confianza ───── */
QZ('m200-1', 200, 1, 'Interpretar intervalos de confianza', [
  ['«La HbA1c media fue 7,4 % (IC 95 %: 7,1 a 7,7)». ¿Qué afirmación es correcta?', ['Los valores de 7,1 a 7,7 son compatibles con los datos como media de la población', 'El 95 % de los pacientes tiene una HbA1c entre 7,1 y 7,7', 'La media de la muestra está entre 7,1 y 7,7 con un 95 % de probabilidad', 'Si se repitiera el estudio, la media sería 7,4 en el 95 % de las veces'], 'El IC describe la incertidumbre sobre la media de la población, no la variabilidad de los pacientes.'],
  ['Dos estudios estiman la misma prevalencia: IC 95 % de 18 % a 32 % y de 23 % a 27 %. ¿Qué indica la diferencia?', ['El segundo tiene una muestra mucho mayor y estima con más precisión', 'El segundo tiene más sesgo', 'El primero es más fiable', 'Las prevalencias son distintas'], 'La anchura del intervalo depende sobre todo del tamaño muestral.'],
  ['«Exactitud del modelo: 85 % (IC 95 %: 64 % a 95 %)». ¿Qué te dice el intervalo?', ['Que se evaluó con pocas preguntas y la exactitud real es muy incierta', 'Que el modelo acierta entre el 64 % y el 95 % de las veces en cada pregunta', 'Que el modelo es excelente', 'Que el IC está mal calculado'], 'Un intervalo tan ancho corresponde a unas 20 preguntas.'],
  ['¿Qué pasa con un IC 99 % frente a un IC 95 % con los mismos datos?', ['Es más ancho', 'Es más estrecho', 'Es igual', 'Está desplazado'], 'Para tener más confianza en contener el parámetro, el intervalo debe ser más ancho.']
]);

M({id: 'm200-2', tema: 200, k: 'code', nivel: 2, pk: PK_SC,
  t: E('Prevalencia de obesidad y LDL medio, con su IC 95 %'),
  gen: r => { const c = cohorteJS(r, r.int(60, 120)); return {imc: c.imc, ldl: c.ldl, e: r.pick([0.03, 0.04, 0.05])}; },
  data: p => `import math\nfrom scipy import stats\n${ARR('imc', p.imc, 15)}\n${ARR('ldl', p.ldl, 15)}   # mg/dL\nmargen = ${p.e}   # margen de error deseado para la prevalencia en el nuevo estudio`,
  enun: () => E(`<p>Calcula:</p><ul>
<li><code>prev</code>: proporción de obesos (IMC ≥ 30) y su IC 95 % de <b>Wilson</b>, <code>prev_li</code> y <code>prev_ls</code> (con z = 1,96). Todo redondeado a 3 decimales.</li>
<li><code>ldl_media</code> y su IC 95 % con la <i>t</i> de Student, <code>ldl_li</code> y <code>ldl_ls</code>, redondeados a 1 decimal.</li>
<li><code>n_necesario</code>: pacientes necesarios para estimar la prevalencia con el <code>margen</code> indicado, usando la prevalencia observada: ⌈1,96² · p(1 − p) / margen²⌉.</li></ul>
<p>IC de Wilson: centro = (p + z²/2n) / (1 + z²/n); semiamplitud = z · √(p(1 − p)/n + z²/4n²) / (1 + z²/n).</p>`),
  out: ['prev', 'prev_li', 'prev_ls', 'ldl_media', 'ldl_li', 'ldl_ls', 'n_necesario'],
  sol: String.raw`z = 1.96
n = len(imc)
p = sum(1 for x in imc if x >= 30) / n
centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
semi = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
prev, prev_li, prev_ls = round(p, 3), round(centro - semi, 3), round(centro + semi, 3)

m = len(ldl)
media = sum(ldl) / m
de = math.sqrt(sum((x - media) ** 2 for x in ldl) / (m - 1))
t = stats.t.ppf(0.975, df=m - 1)
ldl_media = round(media, 1)
ldl_li, ldl_ls = round(media - t * de / math.sqrt(m), 1), round(media + t * de / math.sqrt(m), 1)
n_necesario = math.ceil(z ** 2 * p * (1 - p) / margen ** 2)`,
  mut: [mutE('wald', String.raw`z = 1.96
n = len(imc)
p = sum(1 for x in imc if x >= 30) / n
semi = z * math.sqrt(p * (1 - p) / n)
prev, prev_li, prev_ls = round(p, 3), round(p - semi, 3), round(p + semi, 3)
m = len(ldl)
media = sum(ldl) / m
de = math.sqrt(sum((x - media) ** 2 for x in ldl) / (m - 1))
t = stats.t.ppf(0.975, df=m - 1)
ldl_media = round(media, 1)
ldl_li, ldl_ls = round(media - t * de / math.sqrt(m), 1), round(media + t * de / math.sqrt(m), 1)
n_necesario = math.ceil(z ** 2 * p * (1 - p) / margen ** 2)`, 'Has calculado el IC de Wald (p ± 1,96·EE). Se pide el de Wilson, que se comporta mejor con muestras pequeñas o proporciones extremas.'),
    mutE('de_en_ic', String.raw`z = 1.96
n = len(imc)
p = sum(1 for x in imc if x >= 30) / n
centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
semi = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
prev, prev_li, prev_ls = round(p, 3), round(centro - semi, 3), round(centro + semi, 3)
m = len(ldl)
media = sum(ldl) / m
de = math.sqrt(sum((x - media) ** 2 for x in ldl) / (m - 1))
t = stats.t.ppf(0.975, df=m - 1)
ldl_media = round(media, 1)
ldl_li, ldl_ls = round(media - t * de, 1), round(media + t * de, 1)
n_necesario = math.ceil(z ** 2 * p * (1 - p) / margen ** 2)`, 'El IC de la media usa el error estándar (DE / √n), no la DE: con la DE obtienes un intervalo para los pacientes, no para la media.')],
  pistas: [E('stats.t.ppf(0.975, df=n - 1) da el valor crítico de la t.'),
    E('math.ceil redondea hacia arriba: el tamaño muestral nunca se redondea hacia abajo.')]
});

M({id: 'm200-3', tema: 200, k: 'code', nivel: 3,
  t: E('Exactitud de un modelo de IA con 30 preguntas'),
  gen: r => ({x: r.int(18, 29)}),
  data: p => `import math\naciertos = ${p.x}\npreguntas = 30`,
  starter: () => `# Intervalo que ha propuesto el asistente.
p = aciertos / preguntas
ee = math.sqrt(p * (1 - p) / preguntas)
li, ls = round(p - 1.96 * ee, 3), round(p + 1.96 * ee, 3)
n_para_5 = math.ceil(1.96 ** 2 * p * (1 - p) / 0.05)
`,
  enun: () => E(`<p>Calcula el IC 95 % de <b>Wilson</b> de la exactitud, <code>li</code> y <code>ls</code> (3 decimales), y <code>n_para_5</code>: preguntas necesarias para estimar la exactitud con un margen de ±5 puntos (0,05) usando la exactitud observada. Revisa el código del asistente: tiene dos errores.</p>`),
  out: ['li', 'ls', 'n_para_5'],
  sol: String.raw`z = 1.96
n = preguntas
p = aciertos / n
centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
semi = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
li, ls = round(centro - semi, 3), round(centro + semi, 3)
n_para_5 = math.ceil(z ** 2 * p * (1 - p) / 0.05 ** 2)`,
  mut: [mutE('asistente', String.raw`p = aciertos / preguntas
ee = math.sqrt(p * (1 - p) / preguntas)
li, ls = round(p - 1.96 * ee, 3), round(p + 1.96 * ee, 3)
n_para_5 = math.ceil(1.96 ** 2 * p * (1 - p) / 0.05)`, 'El asistente usa Wald y olvida elevar el margen al cuadrado en el tamaño muestral.'),
    mutE('margen', String.raw`z = 1.96
n = preguntas
p = aciertos / n
centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
semi = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
li, ls = round(centro - semi, 3), round(centro + semi, 3)
n_para_5 = math.ceil(z ** 2 * p * (1 - p) / 0.05)`, 'El margen va al cuadrado en la fórmula del tamaño muestral: 0.05 ** 2.')],
  pistas: [E('Con 29 aciertos de 30, ¿llega el IC de Wald por encima de 1?'),
    E('n = z² · p(1 − p) / e²')]
});

/* ───── Tema 210 · Contraste de hipótesis ───── */
QZ('m210-1', 210, 1, 'Interpretaciones correctas e incorrectas del valor p', [
  ['«p = 0,03: hay un 3 % de probabilidad de que el tratamiento no funcione». ¿Es correcto?', ['No: p es la probabilidad de un resultado así o más extremo si no hubiera efecto', 'Sí', 'Solo si el estudio es aleatorizado', 'Sí, si la muestra es grande'], 'El valor p se calcula suponiendo que H₀ es cierta; no es la probabilidad de H₀.'],
  ['«p = 0,40: el tratamiento no tiene efecto». ¿Es correcto?', ['No: solo indica que no hay evidencia suficiente; puede faltar potencia', 'Sí', 'Sí, si p > 0,05', 'Solo si el IC es estrecho'], 'Ausencia de evidencia no es evidencia de ausencia.'],
  ['Con 20.000 pacientes, una diferencia de PAS de 0,8 mmHg da p < 0,001. ¿Qué concluyes?', ['Es estadísticamente significativa, pero clínicamente irrelevante', 'Es un efecto muy grande', 'El estudio está mal hecho', 'Hay que repetirlo'], 'Con muestras enormes, efectos mínimos alcanzan la significación.'],
  ['¿Qué es la potencia de un estudio?', ['La probabilidad de detectar un efecto que existe de verdad', 'La probabilidad de un falso positivo', 'El tamaño del efecto', '1 − p'], 'Potencia = 1 − β.']
]);

M({id: 'm210-2', tema: 210, k: 'code', nivel: 2, pk: PK_SC,
  t: E('Diferencia de HbA1c entre dos pautas: permutación y prueba t'),
  gen: r => { const n = r.int(15, 25), d = r.pick([0, 0.3, 0.6]); return {a: Array.from({length: n}, () => red(gauss(r, 7.6, 0.6), 1)), b: Array.from({length: n + r.int(6, 12)}, () => red(gauss(r, 7.6 - d, 1.1), 1)), sem: r.int(1, 99999)}; },
  data: p => `import numpy as np\nfrom scipy import stats\n${ARR('pauta_a', p.a, 15)}   # HbA1c (%) a los 6 meses\n${ARR('pauta_b', p.b, 15)}\nsemilla = ${p.sem}`,
  enun: () => E(`<p>Calcula:</p><ul>
<li><code>diferencia</code>: media de A − media de B, redondeada a 2 decimales.</li>
<li><code>p_t</code>: valor p bilateral de la prueba <i>t</i> de <b>Welch</b> (<code>stats.ttest_ind(..., equal_var=False)</code>), redondeado a 4 decimales; y su IC 95 % de la diferencia, <code>ic_li</code> e <code>ic_ls</code>, con <code>.confidence_interval()</code>, redondeados a 2 decimales.</li>
<li><code>p_perm</code>: valor p por permutación. Con <code>rng = np.random.default_rng(semilla)</code> y <code>todos = np.array(pauta_a + pauta_b)</code>, repite 2.000 veces: <code>x = rng.permutation(todos)</code>; diferencia de medias entre los primeros <code>len(pauta_a)</code> y el resto. <code>p_perm</code> es la proporción de diferencias con valor absoluto ≥ que la observada (sin redondear), redondeada a 3 decimales.</li></ul>`),
  out: ['diferencia', 'p_t', 'ic_li', 'ic_ls', 'p_perm'],
  sol: String.raw`obs = np.mean(pauta_a) - np.mean(pauta_b)
diferencia = round(float(obs), 2)
res = stats.ttest_ind(pauta_a, pauta_b, equal_var=False)
p_t = round(float(res.pvalue), 4)
ic = res.confidence_interval()
ic_li, ic_ls = round(float(ic.low), 2), round(float(ic.high), 2)
rng = np.random.default_rng(semilla)
todos = np.array(pauta_a + pauta_b)
na = len(pauta_a)
extremos = 0
for _ in range(2000):
    x = rng.permutation(todos)
    if abs(x[:na].mean() - x[na:].mean()) >= abs(obs):
        extremos += 1
p_perm = round(extremos / 2000, 3)`,
  mut: [mutE('student', String.raw`obs = np.mean(pauta_a) - np.mean(pauta_b)
diferencia = round(float(obs), 2)
res = stats.ttest_ind(pauta_a, pauta_b)
p_t = round(float(res.pvalue), 4)
ic = res.confidence_interval()
ic_li, ic_ls = round(float(ic.low), 2), round(float(ic.high), 2)
rng = np.random.default_rng(semilla)
todos = np.array(pauta_a + pauta_b)
na = len(pauta_a)
extremos = 0
for _ in range(2000):
    x = rng.permutation(todos)
    if abs(x[:na].mean() - x[na:].mean()) >= abs(obs):
        extremos += 1
p_perm = round(extremos / 2000, 3)`, 'Has usado la t clásica, que supone varianzas iguales. Se pide la de Welch: equal_var=False.'),
    mutE('unilateral', String.raw`obs = np.mean(pauta_a) - np.mean(pauta_b)
diferencia = round(float(obs), 2)
res = stats.ttest_ind(pauta_a, pauta_b, equal_var=False)
p_t = round(float(res.pvalue), 4)
ic = res.confidence_interval()
ic_li, ic_ls = round(float(ic.low), 2), round(float(ic.high), 2)
rng = np.random.default_rng(semilla)
todos = np.array(pauta_a + pauta_b)
na = len(pauta_a)
extremos = 0
for _ in range(2000):
    x = rng.permutation(todos)
    if x[:na].mean() - x[na:].mean() >= obs:
        extremos += 1
p_perm = round(extremos / 2000, 3)`, 'Tu permutación es unilateral: para un contraste bilateral compara los valores absolutos de las diferencias.')],
  pistas: [E('res = stats.ttest_ind(a, b, equal_var=False); res.pvalue y res.confidence_interval().'),
    E('Crea el generador una sola vez, antes del bucle.')]
});

M({id: 'm210-3', tema: 210, k: 'code', nivel: 3, pk: PK_SC,
  t: E('Tamaño muestral de un ensayo, comprobado por simulación'),
  gen: r => ({d: r.pick([4, 5, 6, 8]), sd: r.pick([10, 12, 14]), pot: r.pick([0.8, 0.9])}),
  data: p => `import math\nfrom scipy import stats\ndelta = ${p.d}       # diferencia mínima relevante de PAS (mmHg)\nsigma = ${p.sd}      # desviación típica esperada\nalfa = 0.05\npotencia = ${p.pot}`,
  starter: () => `# Cálculo que ha propuesto el asistente.
z_a = stats.norm.ppf(1 - alfa)
z_b = stats.norm.ppf(potencia)
n_por_grupo = math.ceil((z_a + z_b) ** 2 * sigma ** 2 / delta ** 2)
n_total = 2 * n_por_grupo
`,
  enun: () => E(`<p>Para comparar dos medias con un contraste <b>bilateral</b>, los pacientes por grupo son <i>n</i> = ⌈2 (z<sub>1−α/2</sub> + z<sub>1−β</sub>)² σ² / δ²⌉. Calcula <code>n_por_grupo</code> y <code>n_total</code>. Revisa el código del asistente: tiene dos errores.</p>`),
  out: ['n_por_grupo', 'n_total'],
  sol: String.raw`z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)
n_por_grupo = math.ceil(2 * (z_a + z_b) ** 2 * sigma ** 2 / delta ** 2)
n_total = 2 * n_por_grupo`,
  mut: [mutE('asistente', String.raw`z_a = stats.norm.ppf(1 - alfa)
z_b = stats.norm.ppf(potencia)
n_por_grupo = math.ceil((z_a + z_b) ** 2 * sigma ** 2 / delta ** 2)
n_total = 2 * n_por_grupo`, 'El asistente usa z de un contraste unilateral (1 − α en lugar de 1 − α/2) y olvida el factor 2 de la comparación de dos grupos.'),
    mutE('sin_2', String.raw`z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)
n_por_grupo = math.ceil((z_a + z_b) ** 2 * sigma ** 2 / delta ** 2)
n_total = 2 * n_por_grupo`, 'Falta el factor 2: la diferencia de dos medias tiene el doble de varianza que una media.')],
  pistas: [E('Con α = 0,05 bilateral, z = 1,96; con potencia del 80 %, z = 0,84.'),
    E('Comprueba con δ = 5, σ = 10, potencia 80 %: deben salir 63 por grupo.')]
});

/* ───── Tema 220 · Inferencia sobre proporciones ───── */
QZ('m220-1', 220, 1, 'Elegir la prueba para proporciones', [
  ['Comparar la proporción de fumadores de tu centro (52 de 200) con el 22 % de referencia.', ['Prueba binomial exacta frente a p₀', 'Prueba z de dos proporciones', 'McNemar', 't de Student'], 'Una proporción frente a un valor fijo.'],
  ['Comparar la mortalidad entre dos hospitales con 300 pacientes cada uno.', ['Prueba z de dos proporciones (o ji cuadrado)', 'McNemar', 'Binomial', 'Kappa'], 'Dos proporciones de grupos independientes con frecuencias grandes.'],
  ['Comparar complicaciones con dos técnicas en 12 y 14 pacientes, con 1 y 5 complicaciones.', ['Prueba exacta de Fisher', 'Ji cuadrado', 'z de dos proporciones', 't de Welch'], 'Con frecuencias esperadas pequeñas, la aproximación de la ji cuadrado falla.'],
  ['Comparar la sensibilidad de dos pruebas aplicadas a los mismos pacientes.', ['McNemar', 'Fisher', 'Ji cuadrado de independencia', 'z de dos proporciones'], 'Son datos apareados (Tema 240).']
]);

M({id: 'm220-2', tema: 220, k: 'code', nivel: 2,
  t: E('Prevalencia de diabetes: centro rural frente a urbanos'),
  gen: r => { const n1 = r.int(70, 110), n2 = r.int(200, 320), p1 = 0.14 + r.next() * 0.12, p2 = 0.12 + r.next() * 0.06; return {x1: Math.round(n1 * p1), n1, x2: Math.round(n2 * p2), n2}; },
  data: p => `from statistics import NormalDist\nx_rural, n_rural = ${p.x1}, ${p.n1}\nx_urb, n_urb = ${p.x2}, ${p.n2}`,
  enun: () => E(`<p>Calcula, redondeados a 3 decimales:</p><ul>
<li><code>dif</code>: prevalencia rural − urbana;</li>
<li><code>ic_li</code>, <code>ic_ls</code>: IC 95 % de la diferencia con el error estándar no combinado √(p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂);</li>
<li><code>p_valor</code> (4 decimales): prueba <i>z</i> bilateral con la proporción <b>conjunta</b> p̂ = (x₁ + x₂)/(n₁ + n₂) en el error estándar: z = dif / √(p̂(1 − p̂)(1/n₁ + 1/n₂)). Usa <code>NormalDist().cdf</code>.</li></ul>`),
  out: ['dif', 'ic_li', 'ic_ls', 'p_valor'],
  sol: String.raw`p1, p2 = x_rural / n_rural, x_urb / n_urb
d = p1 - p2
ee = (p1 * (1 - p1) / n_rural + p2 * (1 - p2) / n_urb) ** 0.5
dif, ic_li, ic_ls = round(d, 3), round(d - 1.96 * ee, 3), round(d + 1.96 * ee, 3)
pc = (x_rural + x_urb) / (n_rural + n_urb)
z = d / (pc * (1 - pc) * (1 / n_rural + 1 / n_urb)) ** 0.5
p_valor = round(2 * (1 - NormalDist().cdf(abs(z))), 4)`,
  mut: [mutE('unilateral', String.raw`p1, p2 = x_rural / n_rural, x_urb / n_urb
d = p1 - p2
ee = (p1 * (1 - p1) / n_rural + p2 * (1 - p2) / n_urb) ** 0.5
dif, ic_li, ic_ls = round(d, 3), round(d - 1.96 * ee, 3), round(d + 1.96 * ee, 3)
pc = (x_rural + x_urb) / (n_rural + n_urb)
z = d / (pc * (1 - pc) * (1 / n_rural + 1 / n_urb)) ** 0.5
p_valor = round(1 - NormalDist().cdf(abs(z)), 4)`, 'El contraste es bilateral: multiplica por 2 la probabilidad de la cola.')],
  pistas: [E('El IC y la prueba usan errores estándar distintos: el IC no supone H₀; la prueba sí.'),
    E('p bilateral = 2 · (1 − Φ(|z|)).')]
});

M({id: 'm220-3', tema: 220, k: 'code', nivel: 3, pk: PK_SC,
  t: E('Eventos en fumadores y no fumadores: ¿la prueba adecuada?'),
  gen: r => ({a: r.int(1, 5), n1: r.int(10, 16), c: r.int(0, 2), n2: r.int(14, 22)}),
  data: p => `from scipy import stats\neventos_fum, n_fum = ${p.a}, ${p.n1}\neventos_nofum, n_nofum = ${p.c}, ${p.n2}`,
  starter: () => `# Código que ha propuesto el asistente.
tabla = [[eventos_fum, n_fum - eventos_fum], [eventos_nofum, n_nofum - eventos_nofum]]
chi2, p_valor, gl, esperadas = stats.chi2_contingency(tabla)
min_esperada = 0
prueba = 'ji cuadrado'
p_valor = round(p_valor, 4)
`,
  enun: () => E(`<p>Construye la tabla 2 × 2 y calcula <code>min_esperada</code>, la menor frecuencia esperada bajo independencia (redondeada a 2 decimales). Si es menor de 5, la prueba adecuada es la exacta de Fisher. Guarda en <code>prueba</code> el nombre (<code>'Fisher'</code> o <code>'ji cuadrado'</code>) y en <code>p_valor</code> su valor p bilateral, redondeado a 4 decimales.</p>`),
  out: ['min_esperada', 'prueba', 'p_valor'],
  sol: String.raw`tabla = [[eventos_fum, n_fum - eventos_fum], [eventos_nofum, n_nofum - eventos_nofum]]
chi2, p_chi, gl, esperadas = stats.chi2_contingency(tabla)
min_esperada = round(float(esperadas.min()), 2)
if min_esperada < 5:
    prueba = 'Fisher'
    p_valor = round(float(stats.fisher_exact(tabla)[1]), 4)
else:
    prueba = 'ji cuadrado'
    p_valor = round(float(p_chi), 4)`,
  mut: [mutE('asistente', String.raw`tabla = [[eventos_fum, n_fum - eventos_fum], [eventos_nofum, n_nofum - eventos_nofum]]
chi2, p_valor, gl, esperadas = stats.chi2_contingency(tabla)
min_esperada = round(float(esperadas.min()), 2)
prueba = 'ji cuadrado'
p_valor = round(float(p_valor), 4)`, 'Con frecuencias esperadas menores de 5, la ji cuadrado no es fiable: el asistente debía haber usado la prueba exacta de Fisher.')],
  pistas: [E('stats.chi2_contingency devuelve también la tabla de frecuencias esperadas.'),
    E('stats.fisher_exact(tabla) devuelve la odds ratio y el valor p.')]
});

/* ───── Tema 230 · RR, OR y NNT ───── */
M({id: 'm230-1', tema: 230, k: 'code', nivel: 1,
  t: E('RR, OR, RAR y NNT de un ensayo'),
  gen: r => { const n = r.pick([200, 500, 1000, 2000]); const pc = 0.08 + r.next() * 0.15; const pt = pc * (0.5 + r.next() * 0.35); return {a: Math.round(n * pt), n, c: Math.round(n * pc)}; },
  data: p => `import math\nev_trat, n_trat = ${p.a}, ${p.n}\nev_ctrl, n_ctrl = ${p.c}, ${p.n}`,
  enun: () => E('<p>Calcula: <code>rr</code> (riesgo en tratados / riesgo en control) y <code>or_</code>, redondeados a 2 decimales; <code>rar</code> (riesgo control − riesgo tratados), redondeada a 3 decimales; y <code>nnt</code>, ⌈1 / RAR⌉ con la RAR sin redondear.</p>'),
  out: ['rr', 'or_', 'rar', 'nnt'],
  sol: String.raw`rt, rc = ev_trat / n_trat, ev_ctrl / n_ctrl
rr = round(rt / rc, 2)
or_ = round((ev_trat / (n_trat - ev_trat)) / (ev_ctrl / (n_ctrl - ev_ctrl)), 2)
r = rc - rt
rar = round(r, 3)
nnt = math.ceil(1 / r)`,
  mut: [mutE('or_riesgos', String.raw`rt, rc = ev_trat / n_trat, ev_ctrl / n_ctrl
rr = round(rt / rc, 2)
or_ = round(rt / rc, 2)
r = rc - rt
rar = round(r, 3)
nnt = math.ceil(1 / r)`, 'La OR es el cociente de odds (eventos / no eventos), no de riesgos (eventos / total).'),
    mutE('nnt_rrr', String.raw`rt, rc = ev_trat / n_trat, ev_ctrl / n_ctrl
rr = round(rt / rc, 2)
or_ = round((ev_trat / (n_trat - ev_trat)) / (ev_ctrl / (n_ctrl - ev_ctrl)), 2)
r = rc - rt
rar = round(r, 3)
nnt = math.ceil(1 / (1 - rt / rc))`, 'El NNT es el inverso de la reducción absoluta, no de la relativa.')],
  pistas: []
});

M({id: 'm230-2', tema: 230, k: 'code', nivel: 2,
  t: E('Riesgo relativo de evento cardiovascular con su IC'),
  gen: r => { const c = cohorteJS(r, r.int(250, 400)); let a = 0, b = 0, cc = 0, d = 0; c.fumador.forEach((f, i) => { if (f) c.evento[i] ? a++ : b++; else c.evento[i] ? cc++ : d++; }); if (!a) a = 1; if (!cc) cc = 1; return {a, b, c: cc, d}; },
  data: p => `import math\n# fumadores: con evento, sin evento\na, b = ${p.a}, ${p.b}\n# no fumadores: con evento, sin evento\nc, d = ${p.c}, ${p.d}`,
  enun: () => E(`<p>Calcula el riesgo relativo de evento de los fumadores, <code>rr</code>, y su IC 95 % en escala logarítmica: EE(ln RR) = √(1/a − 1/(a+b) + 1/c − 1/(c+d)); límites exp(ln RR ± 1,96 · EE). Redondea <code>rr</code>, <code>rr_li</code> y <code>rr_ls</code> a 2 decimales. <code>significativo</code>: <code>True</code> si el IC no contiene el 1.</p>`),
  out: ['rr', 'rr_li', 'rr_ls', 'significativo'],
  sol: String.raw`r = (a / (a + b)) / (c / (c + d))
ee = math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
li, ls = math.exp(math.log(r) - 1.96 * ee), math.exp(math.log(r) + 1.96 * ee)
rr, rr_li, rr_ls = round(r, 2), round(li, 2), round(ls, 2)
significativo = li > 1 or ls < 1`,
  mut: [mutE('simetrico', String.raw`r = (a / (a + b)) / (c / (c + d))
ee = math.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
li, ls = r - 1.96 * ee, r + 1.96 * ee
rr, rr_li, rr_ls = round(r, 2), round(li, 2), round(ls, 2)
significativo = li > 1 or ls < 1`, 'El IC del RR se calcula en escala logarítmica y se exponencia: por eso es asimétrico.')],
  pistas: [E('Calcula ln(RR) con math.log, suma y resta 1,96·EE, y vuelve con math.exp.'),
    E('El IC contiene el 1 si li <= 1 <= ls.')]
});

M({id: 'm230-3', tema: 230, k: 'code', nivel: 3,
  t: E('De la reducción relativa a la absoluta y el NNT'),
  gen: r => ({rc: red(0.02 + r.next() * 0.1, 3), rrr: r.pick([0.2, 0.25, 0.3, 0.35, 0.4]), anos: r.pick([3, 5])}),
  data: p => `import math\nriesgo_control = ${p.rc}   # riesgo de infarto a ${p.anos} años sin tratamiento\nrrr = ${p.rrr}              # «el fármaco reduce el riesgo un ${Math.round(p.rrr * 100)} %»`,
  starter: () => `# Cifras que ha propuesto el asistente para la nota de prensa.
riesgo_trat = round(riesgo_control - rrr, 4)
rar = round(rrr, 4)
nnt = math.ceil(1 / rrr)
`,
  enun: () => E(`<p>La nota de prensa solo da la reducción relativa del riesgo. Calcula las cifras que necesita un paciente: <code>riesgo_trat</code> (riesgo con el fármaco) y <code>rar</code> (reducción absoluta), redondeados a 4 decimales, y <code>nnt</code>, ⌈1 / RAR⌉ con la RAR sin redondear.</p>`),
  out: ['riesgo_trat', 'rar', 'nnt'],
  sol: String.raw`rt = riesgo_control * (1 - rrr)
r = riesgo_control - rt
riesgo_trat, rar = round(rt, 4), round(r, 4)
nnt = math.ceil(1 / r)`,
  mut: [mutE('asistente', String.raw`riesgo_trat = round(riesgo_control - rrr, 4)
rar = round(rrr, 4)
nnt = math.ceil(1 / rrr)`, 'El asistente resta la reducción relativa como si fuera absoluta: un 30 % menos de un riesgo del 5 % es un 3,5 %, no un −25 %.')],
  pistas: [E('Riesgo con tratamiento = riesgo control × (1 − RRR).'),
    E('Con un riesgo basal bajo, el NNT es grande aunque la RRR sea llamativa.')]
});

/* ───── Tema 240 · Datos apareados y concordancia ───── */
M({id: 'm240-1', tema: 240, k: 'code', nivel: 1,
  t: E('Kappa de Cohen a mano'),
  gen: r => ({a: r.int(20, 60), b: r.int(2, 15), c: r.int(2, 15), d: r.int(30, 90)}),
  data: p => `# Radiólogo 1 en filas, radiólogo 2 en columnas: neumonía sí / no\nss, sn = ${p.a}, ${p.b}\nns, nn = ${p.c}, ${p.d}`,
  enun: () => E('<p>Calcula, redondeados a 3 decimales: <code>po</code> (acuerdo observado), <code>pe</code> (acuerdo esperado por azar, con las frecuencias marginales de cada radiólogo) y <code>kappa</code> = (Po − Pe) / (1 − Pe), con Po y Pe sin redondear.</p>'),
  out: ['po', 'pe', 'kappa'],
  sol: String.raw`n = ss + sn + ns + nn
p_o = (ss + nn) / n
p_e = ((ss + sn) / n) * ((ss + ns) / n) + ((ns + nn) / n) * ((sn + nn) / n)
po, pe = round(p_o, 3), round(p_e, 3)
kappa = round((p_o - p_e) / (1 - p_e), 3)`,
  mut: [mutE('sin_azar', String.raw`n = ss + sn + ns + nn
p_o = (ss + nn) / n
p_e = 0.5
po, pe = round(p_o, 3), round(p_e, 3)
kappa = round((p_o - p_e) / (1 - p_e), 3)`, 'El acuerdo esperado no es 0,5: se calcula con las proporciones marginales de cada radiólogo.')],
  pistas: []
});

M({id: 'm240-2', tema: 240, k: 'code', nivel: 2,
  t: E('Dos pruebas de cribado en los mismos pacientes: McNemar y kappa'),
  gen: r => ({a: r.int(30, 70), b: r.int(3, 18), c: r.int(1, 10), d: r.int(40, 100)}),
  data: p => `import math\n# Prueba A en filas, prueba B en columnas (positivo / negativo), mismos pacientes\npp, pn = ${p.a}, ${p.b}\nnp_, nn = ${p.c}, ${p.d}`,
  enun: () => E(`<p>Calcula:</p><ul>
<li><code>p_mcnemar</code>: valor p de la prueba <b>exacta</b> de McNemar, 2 · P(X ≤ min(b, c)) con X ~ Binomial(b + c, 0,5), sin pasar de 1, redondeado a 4 decimales (b = pn, c = np_);</li>
<li><code>kappa</code>: concordancia entre las dos pruebas, redondeada a 3 decimales.</li></ul>`),
  out: ['p_mcnemar', 'kappa'],
  sol: String.raw`b, c = pn, np_
m = b + c
cola = sum(math.comb(m, k) for k in range(min(b, c) + 1)) / 2 ** m
p_mcnemar = round(min(1.0, 2 * cola), 4)
n = pp + pn + np_ + nn
po = (pp + nn) / n
pe = ((pp + pn) / n) * ((pp + np_) / n) + ((np_ + nn) / n) * ((pn + nn) / n)
kappa = round((po - pe) / (1 - pe), 3)`,
  mut: [mutE('concordantes', String.raw`m = pp + nn
cola = sum(math.comb(m, k) for k in range(min(pp, nn) + 1)) / 2 ** m
p_mcnemar = round(min(1.0, 2 * cola), 4)
n = pp + pn + np_ + nn
po = (pp + nn) / n
pe = ((pp + pn) / n) * ((pp + np_) / n) + ((np_ + nn) / n) * ((pn + nn) / n)
kappa = round((po - pe) / (1 - pe), 3)`, 'McNemar usa los pares discordantes (positivo en una prueba y negativo en la otra), no los concordantes.')],
  pistas: [E('Solo informan sobre la diferencia los pacientes en los que las pruebas discrepan.'),
    E('math.comb(m, k) / 2 ** m es la probabilidad binomial con p = 0,5.')]
});

M({id: 'm240-3', tema: 240, k: 'code', nivel: 3, pk: PK_SC,
  t: E('¿Ayuda la pista? Primer intento frente a tras la pista'),
  gen: r => { const n = r.int(30, 60), primero = [], tras = []; for (let i = 0; i < n; i++) { const p = r.bool(.55); primero.push(p ? 1 : 0); tras.push(p || r.bool(.5) ? 1 : 0); } return {primero, tras}; },
  data: p => `from scipy import stats\n${ARR('primer_intento', p.primero, 20)}\n${ARR('tras_pista', p.tras, 20)}   # 1 = misión resuelta; mismas misiones`,
  starter: () => `# Análisis que ha propuesto el asistente.
tabla = [[sum(primer_intento), len(primer_intento) - sum(primer_intento)],
         [sum(tras_pista), len(tras_pista) - sum(tras_pista)]]
p_valor = round(float(stats.chi2_contingency(tabla)[1]), 4)
b = c = 0
`,
  enun: () => E(`<p>Cada posición es una misión de un estudiante: si la resolvió al primer intento y si la resolvió tras la pista. Son datos <b>apareados</b>. Calcula <code>b</code> (no resuelta al primer intento pero sí tras la pista), <code>c</code> (resuelta al primer intento pero no tras la pista) y <code>p_valor</code>: McNemar exacta con <code>stats.binomtest(b, b + c, 0.5).pvalue</code>, redondeado a 4 decimales.</p>`),
  out: ['b', 'c', 'p_valor'],
  sol: String.raw`b = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 0 and y == 1)
c = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 1 and y == 0)
p_valor = round(float(stats.binomtest(b, b + c, 0.5).pvalue), 4)`,
  mut: [mutE('asistente', String.raw`tabla = [[sum(primer_intento), len(primer_intento) - sum(primer_intento)], [sum(tras_pista), len(tras_pista) - sum(tras_pista)]]
p_valor = round(float(stats.chi2_contingency(tabla)[1]), 4)
b = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 0 and y == 1)
c = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 1 and y == 0)`, 'El asistente trata las dos columnas como grupos independientes con una ji cuadrado. Son las mismas misiones: McNemar.')],
  pistas: [E('zip(primer_intento, tras_pista) da el par de cada misión.'),
    E('Si c = 0, la prueba solo depende de b.')]
});

/* ───── Tema 250 · Pruebas t ───── */
QZ('m250-1', 250, 1, 'Elegir la prueba t', [
  ['Glucemia de 25 pacientes antes y después de un tratamiento.', ['t para muestras relacionadas', 't de Welch para muestras independientes', 't para una muestra frente a 100', 'Ji cuadrado'], 'Los mismos pacientes medidos dos veces.'],
  ['PAS de 40 fumadores frente a 60 no fumadores.', ['t de Welch para muestras independientes', 't para muestras relacionadas', 'McNemar', 'Kappa'], 'Dos grupos distintos de pacientes.'],
  ['¿Es la HbA1c media de tus diabéticos distinta del objetivo del 7 %?', ['t para una muestra frente a 7', 't de Welch', 't relacionada', 'Fisher'], 'Una media frente a un valor de referencia.'],
  ['Con medias 130 y 124, DE de las diferencias 10 y n = 25 pares, ¿cuánto vale t?', ['3,0', '0,6', '6,0', '15'], 't = 6 / (10 / √25) = 6 / 2 = 3.']
]);

M({id: 'm250-2', tema: 250, k: 'code', nivel: 2, pk: PK_SC,
  t: E('IMC de diabéticos y no diabéticos'),
  gen: r => { const c = cohorteJS(r, r.int(80, 140)); return {dm: c.imc.filter((_, i) => c.diabetes[i]), no: c.imc.filter((_, i) => !c.diabetes[i])}; },
  data: p => `import numpy as np\nfrom scipy import stats\n${ARR('imc_dm', p.dm, 15)}\n${ARR('imc_no', p.no, 15)}`,
  enun: () => E(`<p>Calcula: <code>diferencia</code> (media diabéticos − no diabéticos, 2 decimales); <code>p_valor</code> de la <i>t</i> de Welch (4 decimales); su IC 95 %, <code>ic_li</code> e <code>ic_ls</code> (2 decimales); y <code>d_cohen</code> = diferencia / DE conjunta, con DE conjunta = √(((n₁ − 1)s₁² + (n₂ − 1)s₂²) / (n₁ + n₂ − 2)), redondeada a 2 decimales.</p>`),
  out: ['diferencia', 'p_valor', 'ic_li', 'ic_ls', 'd_cohen'],
  sol: String.raw`a, b = np.array(imc_dm), np.array(imc_no)
dif = a.mean() - b.mean()
res = stats.ttest_ind(a, b, equal_var=False)
ic = res.confidence_interval()
n1, n2 = len(a), len(b)
s = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
diferencia, p_valor = round(float(dif), 2), round(float(res.pvalue), 4)
ic_li, ic_ls = round(float(ic.low), 2), round(float(ic.high), 2)
d_cohen = round(float(dif / s), 2)`,
  mut: [mutE('d_media', String.raw`a, b = np.array(imc_dm), np.array(imc_no)
dif = a.mean() - b.mean()
res = stats.ttest_ind(a, b, equal_var=False)
ic = res.confidence_interval()
s = (a.std(ddof=1) + b.std(ddof=1)) / 2
diferencia, p_valor = round(float(dif), 2), round(float(res.pvalue), 4)
ic_li, ic_ls = round(float(ic.low), 2), round(float(ic.high), 2)
d_cohen = round(float(dif / s), 2)`, 'La DE conjunta pondera las varianzas por sus grados de libertad; no es la media de las dos DE.')],
  pistas: [E('a.var(ddof=1) es la varianza muestral.'),
    E('Una d de 0,5 es un efecto «mediano»: compáralo con la diferencia en kg/m².')]
});

M({id: 'm250-3', tema: 250, k: 'code', nivel: 3, pk: PK_SC,
  t: E('Un ensayo antes-después: ¿la prueba equivocada?'),
  gen: r => { const n = r.int(14, 24), antes = Array.from({length: n}, () => Math.round(gauss(r, 150, 14))); return {antes, despues: antes.map(x => Math.round(x - gauss(r, 4, 6)))}; },
  data: p => `from scipy import stats\n${ARR('antes', p.antes, 12)}\n${ARR('despues', p.despues, 12)}   # PAS de los mismos pacientes tras 8 semanas`,
  starter: () => `# Análisis que ha propuesto el asistente.
res = stats.ttest_ind(despues, antes)
p_valor = round(float(res.pvalue), 4)
cambio_medio = round(sum(despues) / len(despues) - sum(antes) / len(antes), 2)
`,
  enun: () => E('<p>Calcula <code>cambio_medio</code> (media de las diferencias después − antes, 2 decimales) y <code>p_valor</code> de la prueba adecuada para estos datos (4 decimales). Revisa el análisis del asistente.</p>'),
  out: ['cambio_medio', 'p_valor'],
  sol: String.raw`dif = [d - a for a, d in zip(antes, despues)]
cambio_medio = round(sum(dif) / len(dif), 2)
p_valor = round(float(stats.ttest_rel(despues, antes).pvalue), 4)`,
  mut: [mutE('asistente', String.raw`res = stats.ttest_ind(despues, antes)
p_valor = round(float(res.pvalue), 4)
cambio_medio = round(sum(despues) / len(despues) - sum(antes) / len(antes), 2)`, 'Son los mismos pacientes medidos dos veces: la prueba t para muestras independientes ignora el apareamiento. Usa stats.ttest_rel.')],
  pistas: [E('¿Son los dos grupos de pacientes distintos o los mismos?'),
    E('La prueba apareada es la t para una muestra aplicada a las diferencias.')]
});

/* ───── Tema 260 · ANOVA y no paramétricas ───── */
M({id: 'm260-1', tema: 260, k: 'code', nivel: 1,
  t: E('Falsos positivos con k comparaciones'),
  gen: r => ({ks: r.sample([2, 3, 5, 6, 8, 10, 15, 20], 3).sort((a, b) => a - b)}),
  data: p => `alfa = 0.05\n${ARR('comparaciones', p.ks)}`,
  enun: () => E('<p>Para cada número de comparaciones independientes <i>k</i>, calcula la probabilidad de al menos un falso positivo, 1 − (1 − α)<sup>k</sup>, redondeada a 3 decimales, en <code>p_algun_fp</code>, y el umbral de Bonferroni α / <i>k</i>, redondeado a 4 decimales, en <code>umbral_bonf</code> (diccionarios con clave <i>k</i>).</p>'),
  out: ['p_algun_fp', 'umbral_bonf'],
  sol: String.raw`p_algun_fp = {k: round(1 - (1 - alfa) ** k, 3) for k in comparaciones}
umbral_bonf = {k: round(alfa / k, 4) for k in comparaciones}`,
  mut: [mutE('suma', String.raw`p_algun_fp = {k: round(k * alfa, 3) for k in comparaciones}
umbral_bonf = {k: round(alfa / k, 4) for k in comparaciones}`, 'Las probabilidades no se suman: con 20 comparaciones, k·α daría 1. Usa el complementario: 1 − 0,95^k.')],
  pistas: []
});

M({id: 'm260-2', tema: 260, k: 'code', nivel: 2, pk: PK_SC,
  t: E('PAS en cuatro grupos de edad: ANOVA'),
  gen: r => { const c = cohorteJS(r, r.int(80, 140)); const g = {'<50': [], '50-59': [], '60-69': [], '≥70': []}; c.edad.forEach((e, i) => g[e < 50 ? '<50' : e < 60 ? '50-59' : e < 70 ? '60-69' : '≥70'].push(c.pas[i])); return {g}; },
  data: p => `from scipy import stats\npas_por_edad = {\n${Object.entries(p.g).map(([k, v]) => `    ${py(k)}: ${py(v)},`).join('\n')}\n}`,
  enun: () => E(`<p>Calcula: <code>f</code> y <code>p_valor</code> del ANOVA de un factor (<code>stats.f_oneway</code>), redondeados a 2 y 6 decimales; <code>eta2</code>, SC entre grupos / SC total, redondeado a 3 decimales; y <code>p_kruskal</code>, el valor p de Kruskal-Wallis, redondeado a 6 decimales.</p>`),
  out: ['f', 'p_valor', 'eta2', 'p_kruskal'],
  sol: String.raw`grupos = list(pas_por_edad.values())
res = stats.f_oneway(*grupos)
f, p_valor = round(float(res.statistic), 2), round(float(res.pvalue), 6)
todos = [x for g in grupos for x in g]
media = sum(todos) / len(todos)
sc_total = sum((x - media) ** 2 for x in todos)
sc_entre = sum(len(g) * (sum(g) / len(g) - media) ** 2 for g in grupos)
eta2 = round(sc_entre / sc_total, 3)
p_kruskal = round(float(stats.kruskal(*grupos).pvalue), 6)`,
  mut: [mutE('sc_sin_n', String.raw`grupos = list(pas_por_edad.values())
res = stats.f_oneway(*grupos)
f, p_valor = round(float(res.statistic), 2), round(float(res.pvalue), 6)
todos = [x for g in grupos for x in g]
media = sum(todos) / len(todos)
sc_total = sum((x - media) ** 2 for x in todos)
sc_entre = sum((sum(g) / len(g) - media) ** 2 for g in grupos)
eta2 = round(sc_entre / sc_total, 3)
p_kruskal = round(float(stats.kruskal(*grupos).pvalue), 6)`, 'La suma de cuadrados entre grupos pondera cada desviación por el tamaño del grupo: len(g) · (media_g − media)².')],
  pistas: [E('stats.f_oneway(*grupos) recibe cada grupo como un argumento.'),
    E('η² indica qué parte de la variabilidad de la PAS explica la edad agrupada.')]
});

M({id: 'm260-3', tema: 260, k: 'code', nivel: 3,
  t: E('«Encuentra algo significativo»: la corrección de Holm'),
  gen: r => ({p: Array.from({length: r.int(6, 10)}, () => red(r.bool(.3) ? r.next() * 0.02 : r.next(), 4))}),
  data: p => `alfa = 0.05\n${ARR('valores_p', p.p)}   # todos los contrastes que ha probado el asistente`,
  starter: () => `# Corrección que ha propuesto el asistente.
k = len(valores_p)
ajustados = [round(p * k, 4) for p in valores_p]
significativos = [i for i, p in enumerate(valores_p) if p < alfa]
`,
  enun: () => E(`<p>Aplica la corrección de <b>Holm</b>: ordena los valores p de menor a mayor; el de posición <i>i</i> (empezando en 0) se multiplica por (k − i); cada ajustado debe ser al menos igual que el anterior (máximo acumulado) y como mucho 1. Devuelve <code>ajustados</code> en el <b>orden original</b>, redondeados a 4 decimales al final, y <code>significativos</code>: posiciones originales con ajustado &lt; α, en orden creciente.</p>`),
  out: ['ajustados', 'significativos'],
  sol: String.raw`k = len(valores_p)
orden = sorted(range(k), key=lambda i: valores_p[i])
aj = [0.0] * k
maximo = 0.0
for pos, i in enumerate(orden):
    maximo = max(maximo, min(1.0, valores_p[i] * (k - pos)))
    aj[i] = maximo
ajustados = [round(x, 4) for x in aj]
significativos = [i for i in range(k) if aj[i] < alfa]`,
  mut: [mutE('asistente', String.raw`k = len(valores_p)
ajustados = [round(min(1.0, p * k), 4) for p in valores_p]
significativos = [i for i, p in enumerate(valores_p) if p < alfa]`, 'El asistente aplica Bonferroni a medias y luego decide con los valores p sin ajustar: los «hallazgos» siguen siendo los mismos.'),
    mutE('sin_maximo', String.raw`k = len(valores_p)
orden = sorted(range(k), key=lambda i: valores_p[i])
aj = [0.0] * k
for pos, i in enumerate(orden):
    aj[i] = min(1.0, valores_p[i] * (k - pos))
ajustados = [round(x, 4) for x in aj]
significativos = [i for i in range(k) if aj[i] < alfa]`, 'Falta el máximo acumulado: un valor p mayor no puede quedar con un ajustado menor que uno anterior.')],
  pistas: [E('sorted(range(k), key=lambda i: valores_p[i]) da las posiciones ordenadas por su valor p.'),
    E('Recorre las posiciones ordenadas llevando el máximo de los ajustados vistos.')]
});

/* ───── Tema 270 · Regresión lineal ───── */
QZ('m270-1', 270, 1, 'Interpretar coeficientes de regresión', [
  ['«PAS = 92 + 0,56 · edad». ¿Qué significa 0,56?', ['La PAS media aumenta 0,56 mmHg por cada año de edad', 'La correlación es 0,56', 'La edad explica el 56 % de la PAS', 'La PAS de un recién nacido'], 'Es la pendiente.'],
  ['En un modelo con edad, IMC y sexo, el coeficiente del IMC es 0,85. ¿Cómo se interpreta?', ['Por cada kg/m² más, la PAS media es 0,85 mmHg mayor a igualdad de edad y sexo', 'Bajar 1 kg/m² baja la PAS 0,85 mmHg en cualquier paciente', 'Es el efecto sin ajustar', 'El IMC explica el 85 % de la PAS'], 'Es un efecto ajustado y observacional.'],
  ['Al añadir la edad, el coeficiente de la PAS sobre la creatinina pasa de 0,11 a 0,03. ¿Qué indica?', ['Que la edad confundía la asociación', 'Que el modelo está mal', 'Que la PAS protege el riñón', 'Nada relevante'], 'Un cambio grande del coeficiente al ajustar es la señal de confusión.'],
  ['¿Cuál de estos coeficientes procede de un modelo ajustado?', ['«OR de diabetes 1,48, ajustada por edad y sexo»', '«Diferencia de medias cruda 9,6 mg/dL»', '«r = 0,48»', '«RR 1,64 (tabla 2 × 2)»'], 'Solo un modelo con varias variables da efectos ajustados.']
]);

M({id: 'm270-2', tema: 270, k: 'code', nivel: 2, pk: PK_NP,
  t: E('IMC y HDL: asociación cruda y ajustada por sexo'),
  gen: r => { const n = r.int(60, 100), mujer = [], imc = [], hdl = []; for (let i = 0; i < n; i++) { const m = r.bool(.5) ? 1 : 0; const im = red(gauss(r, m ? 26 : 28.5, 4), 1); mujer.push(m); imc.push(im); hdl.push(Math.round(gauss(r, 60 + 10 * m - 0.6 * (im - 27), 9))); } return {mujer, imc, hdl}; },
  data: p => `import numpy as np\n${ARR('imc', p.imc, 15)}\n${ARR('mujer', p.mujer, 20)}   # 1 = mujer\n${ARR('hdl', p.hdl, 15)}   # mg/dL`,
  enun: () => E(`<p>Calcula, redondeadas a 3 decimales:</p><ul>
<li><code>pendiente_cruda</code>: pendiente de HDL sobre IMC (<code>np.polyfit(imc, hdl, 1)[0]</code>);</li>
<li><code>pendiente_ajustada</code>: coeficiente del IMC en el modelo HDL ~ 1 + IMC + mujer, con <code>np.linalg.lstsq</code> sobre la matriz de diseño de columnas [1, imc, mujer];</li>
<li><code>cambio_pct</code>: cambio relativo de la pendiente al ajustar, |ajustada − cruda| / |cruda| · 100, con los valores sin redondear y redondeado a 1 decimal;</li>
<li><code>confusion</code>: <code>True</code> si el cambio es mayor del 10 %.</li></ul>`),
  out: ['pendiente_cruda', 'pendiente_ajustada', 'cambio_pct', 'confusion'],
  sol: String.raw`x, y, s = np.array(imc), np.array(hdl), np.array(mujer)
b_cruda = np.polyfit(x, y, 1)[0]
X = np.column_stack([np.ones(len(x)), x, s])
b_aj = np.linalg.lstsq(X, y, rcond=None)[0][1]
cambio = abs(b_aj - b_cruda) / abs(b_cruda) * 100
pendiente_cruda, pendiente_ajustada = round(float(b_cruda), 3), round(float(b_aj), 3)
cambio_pct = round(float(cambio), 1)
confusion = bool(cambio > 10)`,
  mut: [mutE('sin_constante', String.raw`x, y, s = np.array(imc), np.array(hdl), np.array(mujer)
b_cruda = np.polyfit(x, y, 1)[0]
X = np.column_stack([x, s])
b_aj = np.linalg.lstsq(X, y, rcond=None)[0][0]
cambio = abs(b_aj - b_cruda) / abs(b_cruda) * 100
pendiente_cruda, pendiente_ajustada = round(float(b_cruda), 3), round(float(b_aj), 3)
cambio_pct = round(float(cambio), 1)
confusion = bool(cambio > 10)`, 'Falta la columna de unos (la ordenada en el origen): sin ella el modelo obliga a la recta a pasar por 0.')],
  pistas: [E('np.column_stack([np.ones(n), imc, mujer]) construye la matriz de diseño.'),
    E('lstsq devuelve los coeficientes en el orden de las columnas: [ordenada, imc, mujer].')]
});

QZ('m270-3', 270, 3, 'El «efecto» del tratamiento antihipertensivo', [
  ['El asistente ajusta PAS ~ edad + IMC + tratamiento y obtiene: «el tratamiento aumenta la PAS 17 mmHg». ¿Qué ocurre?', ['Confusión por indicación: se trata a los que tienen la PAS alta', 'Los antihipertensivos suben la presión', 'Falta ajustar por sexo', 'Hay pocos pacientes'], 'El tratamiento es consecuencia de la PAS elevada, no su causa.'],
  ['¿Qué diseño permitiría estimar el efecto del fármaco?', ['Un ensayo aleatorizado', 'El mismo modelo con más variables', 'Una correlación', 'Un modelo logístico'], 'La aleatorización rompe la relación entre el pronóstico y el tratamiento.'],
  ['¿Qué frase es correcta para el informe?', ['«Los tratados tenían una PAS mayor; el diseño no permite estimar el efecto del tratamiento»', '«El tratamiento aumenta la PAS»', '«El tratamiento no funciona»', '«El efecto del tratamiento es de 17 mmHg ajustado»'], 'Describe la asociación y la limitación del diseño.'],
  ['Si los médicos usan más un asistente de IA en los casos difíciles, ¿qué se observará en la historia clínica?', ['Peor evolución en los casos con asistente, aunque no haga daño', 'Mejor evolución con asistente', 'Ninguna diferencia', 'Siempre un efecto causal'], 'Es la misma confusión por indicación aplicada a evaluar herramientas de IA.']
]);

/* ───── Tema 280 · Regresión logística ───── */
M({id: 'm280-1', tema: 280, k: 'code', nivel: 1,
  t: E('Coeficientes, odds ratios y probabilidades'),
  gen: r => ({b_edad: red(0.04 + r.next() * 0.06, 3), b_fum: red(0.3 + r.next() * 0.6, 2), logit: red(-3 + r.next() * 2.5, 2)}),
  data: p => `import math\nb_edad = ${p.b_edad}      # coeficiente de la edad (por año)\nb_fumador = ${p.b_fum}    # coeficiente del tabaco\nlogit = ${p.logit}        # β0 + β1·x1 + … de un paciente`,
  enun: () => E('<p>Calcula, redondeados a 3 decimales: <code>or_edad</code> (por año), <code>or_edad_10</code> (por 10 años), <code>or_fumador</code> y <code>prob</code>, la probabilidad de evento del paciente, 1 / (1 + e<sup>−logit</sup>).</p>'),
  out: ['or_edad', 'or_edad_10', 'or_fumador', 'prob'],
  sol: String.raw`or_edad = round(math.exp(b_edad), 3)
or_edad_10 = round(math.exp(10 * b_edad), 3)
or_fumador = round(math.exp(b_fumador), 3)
prob = round(1 / (1 + math.exp(-logit)), 3)`,
  mut: [mutE('por10', String.raw`or_edad = round(math.exp(b_edad), 3)
or_edad_10 = round(10 * math.exp(b_edad), 3)
or_fumador = round(math.exp(b_fumador), 3)
prob = round(1 / (1 + math.exp(-logit)), 3)`, 'La OR por 10 años es e^(10·β), no 10 veces la OR por año: las OR se multiplican.')],
  pistas: []
});

M({id: 'm280-2', tema: 280, k: 'code', nivel: 2,
  t: E('OR del tabaco: cruda y ajustada por sexo (Mantel-Haenszel)'),
  gen: r => { const c = cohorteJS(r, r.int(300, 450)); const t = {Hombre: [0, 0, 0, 0], Mujer: [0, 0, 0, 0]}; c.sexo.forEach((s, i) => { t[s][(c.fumador[i] ? 0 : 2) + (c.evento[i] ? 0 : 1)]++; }); for (const s of Object.keys(t)) t[s] = t[s].map(x => x || 1); return {t}; },
  data: p => `# Por sexo: [fumadores con evento, fumadores sin evento, no fumadores con evento, no fumadores sin evento]\nestratos = ${py(p.t)}`,
  enun: () => E(`<p>Calcula, redondeadas a 2 decimales:</p><ul>
<li><code>or_cruda</code>: OR del tabaco sumando los dos estratos en una sola tabla;</li>
<li><code>or_por_sexo</code>: diccionario con la OR de cada estrato;</li>
<li><code>or_mh</code>: OR ajustada por sexo de Mantel-Haenszel, Σ(a·d/n) / Σ(b·c/n), con n el total de cada estrato.</li></ul>`),
  out: ['or_cruda', 'or_por_sexo', 'or_mh'],
  sol: String.raw`A = sum(e[0] for e in estratos.values())
B = sum(e[1] for e in estratos.values())
C = sum(e[2] for e in estratos.values())
D = sum(e[3] for e in estratos.values())
or_cruda = round(A * D / (B * C), 2)
or_por_sexo = {s: round(a * d / (b * c), 2) for s, (a, b, c, d) in estratos.items()}
num = sum(a * d / (a + b + c + d) for a, b, c, d in estratos.values())
den = sum(b * c / (a + b + c + d) for a, b, c, d in estratos.values())
or_mh = round(num / den, 2)`,
  mut: [mutE('media_or', String.raw`A = sum(e[0] for e in estratos.values())
B = sum(e[1] for e in estratos.values())
C = sum(e[2] for e in estratos.values())
D = sum(e[3] for e in estratos.values())
or_cruda = round(A * D / (B * C), 2)
or_por_sexo = {s: round(a * d / (b * c), 2) for s, (a, b, c, d) in estratos.items()}
or_mh = round(sum(a * d / (b * c) for a, b, c, d in estratos.values()) / 2, 2)`, 'La OR de Mantel-Haenszel no es la media de las OR de los estratos: pondera cada estrato por su tamaño.')],
  pistas: [E('for s, (a, b, c, d) in estratos.items() desempaqueta cada tabla.'),
    E('Si la OR ajustada difiere mucho de la cruda, el sexo confunde la asociación.')]
});

M({id: 'm280-3', tema: 280, k: 'code', nivel: 3,
  t: E('¿Caben tantas variables? Eventos por variable'),
  gen: r => ({ev: r.int(30, 140), vars: r.sample(['edad', 'sexo', 'fumador', 'diabetes', 'pas', 'hdl', 'ldl', 'imc', 'centro', 'hba1c', 'creatinina', 'hta_tratada'], r.int(8, 12)), n: r.int(400, 1500)}),
  data: p => `pacientes = ${p.n}\neventos = ${p.ev}\n${ARR('variables', p.vars, 6)}   # las que ha metido el asistente en el modelo`,
  starter: () => `# Valoración que ha propuesto el asistente.
epv = round(pacientes / len(variables), 1)
suficiente = epv >= 10
max_variables = pacientes // 10
`,
  enun: () => E('<p>Calcula <code>epv</code> (eventos por variable, redondeado a 1 decimal), <code>suficiente</code> (<code>True</code> si EPV ≥ 10, con el valor sin redondear) y <code>max_variables</code>: número máximo de variables con al menos 10 eventos por variable.</p>'),
  out: ['epv', 'suficiente', 'max_variables'],
  sol: String.raw`e = eventos / len(variables)
epv = round(e, 1)
suficiente = e >= 10
max_variables = eventos // 10`,
  mut: [mutE('asistente', String.raw`epv = round(pacientes / len(variables), 1)
suficiente = epv >= 10
max_variables = pacientes // 10`, 'Lo que limita una regresión logística es el número de eventos, no el de pacientes.')],
  pistas: [E('Con 1.000 pacientes y 40 eventos, ¿cuántas variables caben?')]
});

/* ───── Tema 290 · Modelos predictivos e IA ───── */
QZ('m290-1', 290, 1, 'Discriminación, calibración y rendimiento aparente', [
  ['«El modelo asigna más riesgo a los que tienen el evento: AUC 0,82».', ['Discriminación', 'Calibración', 'Rendimiento aparente', 'Exactitud'], 'El AUC mide la capacidad de ordenar a los pacientes.'],
  ['«De los pacientes con riesgo predicho del 20 %, tuvo el evento el 21 %».', ['Calibración', 'Discriminación', 'Sobreajuste', 'Sensibilidad'], 'Concordancia entre probabilidades predichas y observadas.'],
  ['«AUC de 0,97 en los 600 pacientes con los que se entrenó el modelo».', ['Rendimiento aparente, optimista', 'Validación externa', 'Calibración perfecta', 'Validación interna'], 'Medido con los mismos datos del ajuste.'],
  ['«En 2.000 pacientes de otro hospital, el modelo predijo 420 eventos y hubo 480».', ['Validación externa con mala calibración (infraestima el riesgo)', 'Rendimiento aparente', 'Buena discriminación', 'Sobreajuste demostrado'], 'O/E = 1,14: el modelo infraestima el riesgo en esa población.']
]);

M({id: 'm290-2', tema: 290, k: 'code', nivel: 2,
  t: E('Validar un modelo con pacientes reservados'),
  gen: r => { const n = r.int(60, 100), p = [], y = []; for (let i = 0; i < n; i++) { const lg = gauss(r, -1.8, 1.1); const pr = 1 / (1 + Math.exp(-lg)); p.push(red(pr, 3)); y.push(r.bool(clamp(pr * 1.25, 0, 1)) ? 1 : 0); } if (!y.includes(1)) y[0] = 1; return {p, y}; },
  data: p => `${ARR('prob', p.p, 12)}   # probabilidad predicha en los pacientes reservados\n${ARR('evento', p.y, 20)}`,
  enun: () => E(`<p>Evalúa el modelo en los pacientes reservados. Calcula:</p><ul>
<li><code>auc</code>: por pares evento/no evento (empates = 0,5), redondeado a 3 decimales;</li>
<li><code>o_e</code>: eventos observados / eventos esperados (suma de las probabilidades), redondeado a 2 decimales;</li>
<li><code>brier</code>: media de (probabilidad − evento)², redondeada a 4 decimales;</li>
<li><code>infraestima</code>: <code>True</code> si O/E (sin redondear) es mayor que 1.</li></ul>`),
  out: ['auc', 'o_e', 'brier', 'infraestima'],
  sol: String.raw`pos = [p for p, y in zip(prob, evento) if y == 1]
neg = [p for p, y in zip(prob, evento) if y == 0]
puntos = sum(1 if a > b else 0.5 if a == b else 0 for a in pos for b in neg)
auc = round(puntos / (len(pos) * len(neg)), 3)
oe = sum(evento) / sum(prob)
o_e = round(oe, 2)
brier = round(sum((p - y) ** 2 for p, y in zip(prob, evento)) / len(prob), 4)
infraestima = oe > 1`,
  mut: [mutE('oe_invertido', String.raw`pos = [p for p, y in zip(prob, evento) if y == 1]
neg = [p for p, y in zip(prob, evento) if y == 0]
puntos = sum(1 if a > b else 0.5 if a == b else 0 for a in pos for b in neg)
auc = round(puntos / (len(pos) * len(neg)), 3)
oe = sum(prob) / sum(evento)
o_e = round(oe, 2)
brier = round(sum((p - y) ** 2 for p, y in zip(prob, evento)) / len(prob), 4)
infraestima = oe > 1`, 'Has calculado esperados / observados: el cociente es observados (eventos reales) entre esperados (suma de probabilidades).')],
  pistas: [E('Los eventos esperados son la suma de las probabilidades predichas.'),
    E('Un O/E mayor que 1 significa que ocurren más eventos de los que predice el modelo.')]
});

QZ('m290-3', 290, 3, 'Las preguntas TRIPOD+AI para la empresa', [
  ['El folleto dice «exactitud del 89 %» y el evento ocurre en el 11 % de los pacientes. ¿Qué preguntas?', ['¿Cuál es el AUC y la calibración? Decir siempre «no» ya da un 89 %', '¿Qué lenguaje de programación usa?', '¿Cuántos parámetros tiene?', '¿Es de código abierto?'], 'Con eventos poco frecuentes, la exactitud no informa.'],
  ['«AUC de 0,90». ¿Qué falta saber?', ['Si se midió con pacientes no usados para entrenarlo', 'El color de la interfaz', 'El precio', 'Si usa redes neuronales'], 'El rendimiento aparente es optimista.'],
  ['Nuestra población es mayor que la del hospital de desarrollo. ¿Qué pides?', ['Validación externa y, si hace falta, recalibración con nuestros datos', 'Nada, el modelo es el mismo', 'Más variables', 'Una versión más compleja'], 'La calibración suele deteriorarse al cambiar de población.'],
  ['¿Qué pide TRIPOD+AI sobre la equidad?', ['El rendimiento por subgrupos (sexo, edad, nivel socioeconómico…)', 'Que el modelo no use la edad', 'Que la exactitud supere el 90 %', 'Nada'], 'Un modelo puede funcionar bien en conjunto y mal en un grupo.']
]);

/* ───── Tema 300 · Lectura crítica y evaluación de la mejora recursiva ───── */
QZ('m300-1', 300, 1, 'Las diez preguntas de lectura crítica', [
  ['Ensayo aleatorizado: «el fármaco redujo la mortalidad (HR 0,80; IC 95 %: 0,62 a 1,03)». ¿Qué concluyes?', ['No hay evidencia suficiente: el IC incluye el 1', 'El fármaco reduce la mortalidad un 20 %', 'El fármaco aumenta la mortalidad', 'El estudio está mal hecho'], 'La estimación es compatible con un beneficio importante y con ningún efecto.'],
  ['Cohorte: «el café reduce la mortalidad (HR ajustado 0,70)». ¿Qué falla en la conclusión?', ['El lenguaje causal en un estudio observacional', 'El HR', 'El tamaño muestral', 'Nada'], 'Debería decir «se asoció con»; pueden quedar confusores no medidos.'],
  ['Modelo de IA: «AUC 0,95 en la muestra de desarrollo». ¿Qué pregunta de lectura crítica es la clave?', ['¿Se validó en pacientes no usados para desarrollarlo?', '¿Cuál es el PICO?', '¿Se registró el ensayo?', '¿Cuál es el NNT?'], 'Es la pregunta de la validación.'],
  ['Un estudio de 200.000 personas da un IC muy estrecho. ¿Qué no controla el tamaño?', ['Los sesgos de selección, información y confusión', 'El azar', 'La precisión', 'El error estándar'], 'Precisión no es validez.']
]);

M({id: 'm300-2', tema: 300, k: 'code', nivel: 2,
  t: E('Reescribir una nota de prensa con medidas absolutas'),
  gen: r => { const n1 = r.int(4000, 20000), n0 = r.int(4000, 20000), p0 = 0.02 + r.next() * 0.06, rr = 0.6 + r.next() * 0.3; return {e1: Math.round(n1 * p0 * rr), n1, e0: Math.round(n0 * p0), n0}; },
  data: p => `# Cohorte: «Los que hacen ejercicio a diario reducen su mortalidad»\nmuertes_ejercicio, n_ejercicio = ${p.e1}, ${p.n1}\nmuertes_sedentarios, n_sedentarios = ${p.e0}, ${p.n0}`,
  enun: () => E(`<p>Calcula las cifras para una nota de prensa honesta: <code>riesgo_ej</code> y <code>riesgo_sed</code> (en %, 2 decimales), <code>rr</code> (2 decimales), <code>reduccion_relativa</code> (en %, 1 decimal), <code>diferencia_absoluta</code> (puntos porcentuales, 2 decimales) y <code>por_cada_1000</code>: muertes menos por cada 1.000 personas (redondeado a entero). Todo con los valores sin redondear.</p><p>La frase correcta será: «se asoció con», no «reduce», porque es un estudio observacional.</p>`),
  out: ['riesgo_ej', 'riesgo_sed', 'rr', 'reduccion_relativa', 'diferencia_absoluta', 'por_cada_1000'],
  sol: String.raw`r1 = muertes_ejercicio / n_ejercicio
r0 = muertes_sedentarios / n_sedentarios
riesgo_ej, riesgo_sed = round(r1 * 100, 2), round(r0 * 100, 2)
rr = round(r1 / r0, 2)
reduccion_relativa = round((1 - r1 / r0) * 100, 1)
diferencia_absoluta = round((r0 - r1) * 100, 2)
por_cada_1000 = round((r0 - r1) * 1000)`,
  mut: [mutE('absoluta_relativa', String.raw`r1 = muertes_ejercicio / n_ejercicio
r0 = muertes_sedentarios / n_sedentarios
riesgo_ej, riesgo_sed = round(r1 * 100, 2), round(r0 * 100, 2)
rr = round(r1 / r0, 2)
reduccion_relativa = round((1 - r1 / r0) * 100, 1)
diferencia_absoluta = round((1 - r1 / r0) * 100, 2)
por_cada_1000 = round((r0 - r1) * 1000)`, 'La diferencia absoluta es riesgo sedentarios − riesgo ejercicio, en puntos porcentuales; lo que has calculado es la reducción relativa.')],
  pistas: [E('Primero los dos riesgos; todo lo demás sale de ellos.'),
    E('Una reducción relativa del 30 % puede ser una diferencia absoluta de menos de 1 punto.')]
});

/* el reto final usa los informes del propio estudiante si ya ha hecho al menos 15 misiones */
function datosPropios() {
  const filas = MIS.map(m => ({m, p: (typeof S !== 'undefined' && S.prog) ? S.prog[m.id] : null})).filter(x => x.p && x.p.prim !== undefined);
  if (filas.length < 15) return null;
  return {primero: filas.map(x => x.p.prim ? 1 : 0), tras: filas.map(x => x.p.done ? 1 : 0), modulo: filas.map(x => +temaDe(x.m).u)};
}
M({id: 'm300-3', tema: 300, k: 'code', nivel: 3,
  t: E('Tu propia mejora recursiva: análisis de tus informes'),
  gen: (r, j) => {
    const propios = j === undefined ? datosPropios() : null;
    if (propios) return {...propios, propios: true};
    const n = r.int(40, 90), primero = [], tras = [], modulo = [];
    for (let i = 0; i < n; i++) { const md = 1 + Math.floor(i * 5 / n); const p = r.bool(0.35 + 0.1 * md); primero.push(p ? 1 : 0); tras.push(p || r.bool(.6) ? 1 : 0); modulo.push(md); }
    return {primero, tras, modulo, propios: false};
  },
  data: p => `import math\n# ${p.propios ? 'Tus informes de la app: una posición por misión intentada' : 'Informes simulados de un estudiante (cuando hayas intentado 15 misiones, aquí aparecerán los tuyos)'}\n${ARR('primer_intento', p.primero, 20)}\n${ARR('tras_pista', p.tras, 20)}\n${ARR('modulo', p.modulo, 20)}`,
  starter: () => `# Análisis que ha propuesto el asistente.
b = tras_pista.count(1)
c = primer_intento.count(1)
p_mcnemar = 0.05
acierto_por_modulo = {}
`,
  enun: () => E(`<p>Analiza tu aprendizaje igual que se analiza un modelo de IA. Calcula:</p><ul>
<li><code>b</code>: misiones no resueltas al primer intento pero sí después; <code>c</code>: resueltas al primer intento y no después;</li>
<li><code>p_mcnemar</code>: McNemar exacta, 2 · P(X ≤ min(b, c)) con X ~ Bin(b + c; 0,5), sin pasar de 1, redondeada a 4 decimales (si b + c = 0, vale 1);</li>
<li><code>acierto_por_modulo</code>: diccionario módulo → proporción de misiones resueltas al primer intento, redondeada a 2 decimales, solo con los módulos que aparecen, en orden creciente.</li></ul>
<p>Después, escribe en tu cuaderno un párrafo de autoevaluación: ¿dependes menos de la pista a lo largo del curso?</p>`),
  out: ['b', 'c', 'p_mcnemar', 'acierto_por_modulo'],
  sol: String.raw`b = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 0 and y == 1)
c = sum(1 for x, y in zip(primer_intento, tras_pista) if x == 1 and y == 0)
m = b + c
if m == 0:
    p_mcnemar = 1.0
else:
    p_mcnemar = round(min(1.0, 2 * sum(math.comb(m, k) for k in range(min(b, c) + 1)) / 2 ** m), 4)
acierto_por_modulo = {}
for md in sorted(set(modulo)):
    valores = [x for x, mm in zip(primer_intento, modulo) if mm == md]
    acierto_por_modulo[md] = round(sum(valores) / len(valores), 2)`,
  mut: [mutE('asistente', String.raw`b = tras_pista.count(1)
c = primer_intento.count(1)
p_mcnemar = 0.05
acierto_por_modulo = {}`, 'El asistente cuenta totales, no pares discordantes, e inventa el valor p.')],
  pistas: [E('Los pares discordantes se cuentan recorriendo a la vez las dos listas con zip.'),
    E('sorted(set(modulo)) da los módulos presentes en orden.')]
});
