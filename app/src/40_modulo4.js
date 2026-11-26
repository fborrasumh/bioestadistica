/* ══ Módulo 4 · Probabilidad (temas 140 a 190). El examen de este módulo es a mano: las misiones básicas piden razonar sin ayuda. ══ */

/* ───── Tema 140 · Fundamentos de probabilidad y técnicas de recuento ───── */
QZ('m140-1', 140, 1, 'Probabilidades de cruces genéticos', [
  ['Un padre con una enfermedad autosómica dominante (heterocigoto, Aa) y una madre sana (aa). ¿Probabilidad de que un hijo esté afectado?', ['1/2', '1/4', '3/4', '1'], 'Cada hijo recibe A o a del padre con probabilidad 1/2; de la madre siempre a.'],
  ['Dos portadores sanos de una enfermedad autosómica recesiva (Aa × Aa). ¿Probabilidad de un hijo afectado (aa)?', ['1/4', '1/2', '3/4', '0'], 'Hace falta recibir a de los dos: 1/2 · 1/2 = 1/4.'],
  ['En ese mismo cruce, un hijo está sano. ¿Probabilidad de que sea portador?', ['2/3', '1/2', '1/4', '3/4'], 'Entre los sanos (AA, Aa, aA), dos de cada tres son portadores: es una probabilidad condicionada.'],
  ['Dos portadores tienen tres hijos. ¿Probabilidad de que ninguno esté afectado?', ['27/64', '3/4', '1/64', '9/16'], 'Los hijos son independientes: (3/4)³ = 27/64.']
]);

M({id: 'm140-2', tema: 140, k: 'code', nivel: 2,
  t: E('Unión, intersección, complementario e independencia en una cohorte'),
  gen: (r, j) => {
    const n = r.int(60, 120), pa = 0.2 + r.next() * 0.3, pb = 0.15 + r.next() * 0.35, dep = j === 0 ? 0 : j === 1 ? 0.35 : r.pick([0, 0.3]);
    const a = [], b = [];
    for (let i = 0; i < n; i++) { const x = r.bool(pa); a.push(x ? 1 : 0); b.push(r.bool(clamp(pb + (x ? dep : 0), 0, 1)) ? 1 : 0); }
    return {a, b};
  },
  data: p => `${ARR('fumador', p.a, 20)}\n${ARR('epoc', p.b, 20)}   # 1 = sí, 0 = no; cada posición es un paciente`,
  enun: () => E(`<p>Con las frecuencias de la cohorte, calcula y redondea a 3 decimales:</p><ul>
<li><code>p_f</code> = P(fumador), <code>p_e</code> = P(EPOC), <code>p_f_y_e</code> = P(fumador y EPOC), <code>p_f_o_e</code> = P(fumador o EPOC) y <code>p_no_f</code> = P(no fumador).</li>
<li><code>p_e_dado_f</code> = P(EPOC | fumador).</li>
<li><code>independientes</code>: <code>True</code> si |P(EPOC | fumador) − P(EPOC)| &lt; 0,05, con los valores sin redondear.</li></ul>`),
  out: ['p_f', 'p_e', 'p_f_y_e', 'p_f_o_e', 'p_no_f', 'p_e_dado_f', 'independientes'],
  sol: String.raw`n = len(fumador)
pf = sum(fumador) / n
pe = sum(epoc) / n
pfe = sum(1 for f, e in zip(fumador, epoc) if f and e) / n
p_e_f = pfe / pf
p_f, p_e, p_f_y_e = round(pf, 3), round(pe, 3), round(pfe, 3)
p_f_o_e = round(pf + pe - pfe, 3)
p_no_f = round(1 - pf, 3)
p_e_dado_f = round(p_e_f, 3)
independientes = abs(p_e_f - pe) < 0.05`,
  mut: [mutE('union_suma', String.raw`n = len(fumador)
pf = sum(fumador) / n
pe = sum(epoc) / n
pfe = sum(1 for f, e in zip(fumador, epoc) if f and e) / n
p_e_f = pfe / pf
p_f, p_e, p_f_y_e = round(pf, 3), round(pe, 3), round(pfe, 3)
p_f_o_e = round(pf + pe, 3)
p_no_f = round(1 - pf, 3)
p_e_dado_f = round(p_e_f, 3)
independientes = abs(p_e_f - pe) < 0.05`, 'P(A o B) = P(A) + P(B) − P(A y B): si no restas la intersección, cuentas dos veces a los fumadores con EPOC.'),
    mutE('condicionada', String.raw`n = len(fumador)
pf = sum(fumador) / n
pe = sum(epoc) / n
pfe = sum(1 for f, e in zip(fumador, epoc) if f and e) / n
p_e_f = pfe / pe
p_f, p_e, p_f_y_e = round(pf, 3), round(pe, 3), round(pfe, 3)
p_f_o_e = round(pf + pe - pfe, 3)
p_no_f = round(1 - pf, 3)
p_e_dado_f = round(p_e_f, 3)
independientes = abs(p_e_f - pe) < 0.05`, 'Has calculado P(fumador | EPOC). P(EPOC | fumador) divide la intersección entre P(fumador).')],
  pistas: [E('Las probabilidades se estiman con frecuencias relativas: casos / n.'),
    E('zip(fumador, epoc) recorre los dos valores de cada paciente a la vez.'),
    E('P(B | A) = P(A y B) / P(A).')]
});

M({id: 'm140-3', tema: 140, k: 'code', nivel: 3,
  t: E('Combinaciones en un ensayo clínico'),
  gen: r => { const n = r.pick([10, 12, 14, 16, 20]); return {n, k: n / 2, g: r.int(3, 4)}; },
  data: p => `import math\nn = ${p.n}            # pacientes del ensayo\nk = ${p.k}             # se asignan al tratamiento; el resto, al control\ngraves = ${p.g}        # pacientes con enfermedad grave entre los n`,
  starter: () => `# Razonamiento que ha propuesto el asistente. Revísalo paso a paso.
formas = math.perm(n, k)
p_todos_graves_tratados = math.perm(n - graves, k - graves) / math.perm(n, k)
`,
  enun: () => E(`<p>En un ensayo se eligen al azar <code>k</code> de los <code>n</code> pacientes para el tratamiento. Calcula:</p><ul>
<li><code>formas</code>: número de grupos de tratamiento distintos que pueden formarse (el orden de elección no importa).</li>
<li><code>p_todos_graves_tratados</code>: probabilidad de que <b>todos</b> los pacientes graves caigan en el grupo de tratamiento, redondeada a 4 decimales.</li></ul>`),
  out: ['formas', 'p_todos_graves_tratados'],
  sol: String.raw`formas = math.comb(n, k)
p_todos_graves_tratados = round(math.comb(n - graves, k - graves) / math.comb(n, k), 4)`,
  mut: [mutE('asistente', String.raw`formas = math.perm(n, k)
p_todos_graves_tratados = round(math.perm(n - graves, k - graves) / math.perm(n, k), 4)`, 'El asistente usa variaciones (math.perm), que tienen en cuenta el orden. Un grupo de pacientes es el mismo en cualquier orden: combinaciones, math.comb.')],
  pistas: [E('Si los graves ya están en el tratamiento, ¿cuántos huecos quedan y entre cuántos pacientes se eligen?'),
    E('Comprueba con un caso pequeño: 4 pacientes, 2 al tratamiento, 1 grave → la probabilidad es 1/2.')]
});

/* ───── Tema 150 · Probabilidad condicionada y teorema de Bayes ───── */
QZ('m150-1', 150, 1, 'Bayes con frecuencias naturales', [
  ['Prevalencia 1 %, sensibilidad 90 %, especificidad 90 %. De 1.000 personas, ¿cuántos positivos hay y cuántos están enfermos?', ['108 positivos, de los que 9 están enfermos', '90 positivos, todos enfermos', '100 positivos, 90 enfermos', '10 positivos, 9 enfermos'], 'Enfermos: 10, de los que 9 dan positivo. Sanos: 990, de los que 99 dan falso positivo. 9 / 108 ≈ 8 %.'],
  ['Con esos datos, ¿cuál es el valor predictivo positivo?', ['Alrededor del 8 %', 'El 90 %', 'El 1 %', 'El 50 %'], 'Con una prevalencia baja, la mayoría de los positivos son falsos positivos.'],
  ['Si la misma prueba se aplica en una consulta especializada con una prevalencia del 30 %, ¿qué ocurre con el VPP?', ['Aumenta mucho', 'No cambia', 'Disminuye', 'Se iguala a la sensibilidad'], 'El VPP depende de la probabilidad previa: 270 / (270 + 70) ≈ 79 %.'],
  ['Confundir la sensibilidad, P(positivo | enfermo), con el VPP, P(enfermo | positivo), se llama…', ['Falacia de la tasa base (o de la condicional transpuesta)', 'Sesgo de selección', 'Regresión a la media', 'Error de tipo II'], 'Es el error más frecuente al interpretar una prueba positiva.']
]);

const postprueba = (pre, s, e) => (s * pre) / (s * pre + (1 - e) * (1 - pre));
M({id: 'm150-2', tema: 150, k: 'code', nivel: 2,
  t: E('Probabilidad posprueba de TVP con un dímero D positivo'),
  gen: r => ({s: red(0.93 + r.next() * 0.05, 2), e: red(0.4 + r.next() * 0.2, 2), pb: red(0.03 + r.next() * 0.04, 2), pa: red(0.4 + r.next() * 0.25, 2)}),
  data: p => `sensibilidad = ${p.s}\nespecificidad = ${p.e}\npre_baja = ${p.pb}    # Wells improbable\npre_alta = ${p.pa}    # Wells probable`,
  enun: () => E(`<p>Calcula, redondeadas a 3 decimales:</p><ul>
<li><code>post_baja</code> y <code>post_alta</code>: probabilidad de TVP tras un dímero D <b>positivo</b> con probabilidad previa baja y alta (teorema de Bayes).</li>
<li><code>post_neg_baja</code>: probabilidad de TVP tras un dímero D <b>negativo</b> con probabilidad previa baja.</li>
<li><code>rv_pos</code>: razón de verosimilitud positiva, sensibilidad / (1 − especificidad), redondeada a 2 decimales.</li></ul>`),
  out: ['post_baja', 'post_alta', 'post_neg_baja', 'rv_pos'],
  sol: String.raw`def posprueba_positiva(pre):
    return sensibilidad * pre / (sensibilidad * pre + (1 - especificidad) * (1 - pre))

post_baja = round(posprueba_positiva(pre_baja), 3)
post_alta = round(posprueba_positiva(pre_alta), 3)
fn = (1 - sensibilidad) * pre_baja
vn = especificidad * (1 - pre_baja)
post_neg_baja = round(fn / (fn + vn), 3)
rv_pos = round(sensibilidad / (1 - especificidad), 2)`,
  mut: [mutE('sensibilidad', String.raw`post_baja = round(sensibilidad, 3)
post_alta = round(sensibilidad, 3)
post_neg_baja = round(1 - especificidad, 3)
rv_pos = round(sensibilidad / (1 - especificidad), 2)`, 'Es la falacia de la tasa base: la sensibilidad no es la probabilidad de enfermedad tras un positivo, que depende de la probabilidad previa.')],
  pistas: [E('Imagina 1.000 pacientes: ¿cuántos tienen TVP? ¿cuántos de ellos dan positivo? ¿cuántos sanos dan positivo?'),
    E('P(TVP | +) = verdaderos positivos / todos los positivos.'),
    E('Tras un negativo: falsos negativos / todos los negativos.')]
});

M({id: 'm150-3', tema: 150, k: 'code', nivel: 3,
  t: E('El caso de Lucía: ¿comete el asistente la falacia de la tasa base?'),
  gen: r => ({prev: red(0.005 + r.next() * 0.015, 3), s: red(0.85 + r.next() * 0.1, 2), e: red(0.9 + r.next() * 0.07, 2), sem: r.int(1, 9999)}),
  data: p => `import random\nprevalencia = ${p.prev}   # cáncer de mama en el grupo de edad de Lucía\nsensibilidad = ${p.s}\nespecificidad = ${p.e}\nsemilla = ${p.sem}`,
  starter: () => `# Respuesta del asistente: «Si la mamografía tiene una sensibilidad del 90 %,
# la probabilidad de que Lucía tenga cáncer es del 90 %».
vpp = sensibilidad
`,
  enun: () => E(`<p>Lucía, sin síntomas, tiene una mamografía de cribado positiva. Calcula:</p><ul>
<li><code>vpp</code>: probabilidad de que tenga cáncer dado el positivo, por el teorema de Bayes, redondeada a 3 decimales.</li>
<li><code>vpp_simulado</code>: la misma probabilidad por simulación: fija <code>random.seed(semilla)</code> y simula 100.000 mujeres; para cada una, primero <code>random.random() &lt; prevalencia</code> decide si tiene cáncer y después <code>random.random()</code> decide el resultado (positivo si es menor que la sensibilidad, en las enfermas, o menor que 1 − especificidad, en las sanas). Redondea a 3 decimales.</li></ul>`),
  out: ['vpp', 'vpp_simulado'],
  sol: String.raw`vpp = round(sensibilidad * prevalencia / (sensibilidad * prevalencia + (1 - especificidad) * (1 - prevalencia)), 3)
random.seed(semilla)
positivas = enfermas_positivas = 0
for _ in range(100000):
    cancer = random.random() < prevalencia
    u = random.random()
    positiva = u < sensibilidad if cancer else u < 1 - especificidad
    if positiva:
        positivas += 1
        enfermas_positivas += cancer
vpp_simulado = round(enfermas_positivas / positivas, 3)`,
  mut: [mutE('asistente', String.raw`vpp = sensibilidad
random.seed(semilla)
positivas = enfermas_positivas = 0
for _ in range(100000):
    cancer = random.random() < prevalencia
    u = random.random()
    positiva = u < sensibilidad if cancer else u < 1 - especificidad
    if positiva:
        positivas += 1
        enfermas_positivas += cancer
vpp_simulado = round(enfermas_positivas / positivas, 3)`, 'El asistente confunde P(positivo | cáncer) con P(cáncer | positivo): la simulación le lleva la contraria.')],
  ocultos: 1,
  pistas: [E('Con una prevalencia tan baja, la mayoría de las mamografías positivas son falsos positivos.'),
    E('En la simulación, cuenta solo las mujeres con resultado positivo y, entre ellas, las que tienen cáncer.')]
});

/* ───── Tema 160 · Evaluación de pruebas diagnósticas ───── */
M({id: 'm160-1', tema: 160, k: 'code', nivel: 1,
  t: E('Índices de una tabla 2 × 2'),
  gen: r => ({vp: r.int(20, 90), fn: r.int(2, 25), fp: r.int(5, 60), vn: r.int(80, 400)}),
  data: p => `vp, fn = ${p.vp}, ${p.fn}     # enfermos: prueba positiva, prueba negativa\nfp, vn = ${p.fp}, ${p.vn}     # sanos: prueba positiva, prueba negativa`,
  enun: () => E('<p>Calcula, redondeados a 3 decimales: <code>sensibilidad</code>, <code>especificidad</code>, <code>vpp</code>, <code>vpn</code> y <code>prevalencia</code>.</p>'),
  out: ['sensibilidad', 'especificidad', 'vpp', 'vpn', 'prevalencia'],
  sol: String.raw`sensibilidad = round(vp / (vp + fn), 3)
especificidad = round(vn / (vn + fp), 3)
vpp = round(vp / (vp + fp), 3)
vpn = round(vn / (vn + fn), 3)
prevalencia = round((vp + fn) / (vp + fn + fp + vn), 3)`,
  mut: [mutE('cruzados', String.raw`sensibilidad = round(vp / (vp + fp), 3)
especificidad = round(vn / (vn + fn), 3)
vpp = round(vp / (vp + fn), 3)
vpn = round(vn / (vn + fp), 3)
prevalencia = round((vp + fn) / (vp + fn + fp + vn), 3)`, 'Has intercambiado los denominadores: la sensibilidad se calcula entre los enfermos (vp + fn); el VPP, entre los positivos (vp + fp).')],
  pistas: []
});

M({id: 'm160-2', tema: 160, k: 'code', nivel: 2,
  t: E('Troponina de alta sensibilidad: un punto de corte para descartar infarto'),
  gen: r => {
    const n = r.int(40, 60), v = [], y = [];
    for (let i = 0; i < n; i++) { const iam = r.bool(.2); y.push(iam ? 1 : 0); v.push(Math.round(iam ? Math.exp(gauss(r, Math.log(90), 0.8)) : Math.exp(gauss(r, Math.log(8), 0.7)))); }
    if (!y.includes(1)) { y[0] = 1; v[0] = 120; }
    const minIam = Math.min(...v.filter((_, i) => y[i]));
    return {v, y, cortes: [...new Set([3, 5, Math.max(2, minIam - 1), minIam, 14, 30, 52])].sort((a, b) => a - b)};
  },
  data: p => `${ARR('troponina', p.v, 15)}   # ng/L\n${ARR('infarto', p.y, 20)}   # 1 = infarto confirmado\n${ARR('cortes', p.cortes)}   # positivo si troponina >= corte`,
  enun: () => E(`<p>Para cada punto de corte (positivo si troponina ≥ corte), calcula la sensibilidad y la especificidad, redondeadas a 3 decimales, en los diccionarios <code>sens</code> y <code>esp</code> (clave: el corte).</p><p>Para <b>descartar</b> el infarto se quiere una sensibilidad del 100 %. <code>corte_descarte</code>: el <b>mayor</b> corte con sensibilidad igual a 1, que es el que más especificidad conserva.</p>`),
  out: ['sens', 'esp', 'corte_descarte'],
  sol: String.raw`sens, esp = {}, {}
for c in cortes:
    vp = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t >= c)
    fn = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t < c)
    vn = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t < c)
    fp = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t >= c)
    sens[c] = round(vp / (vp + fn), 3)
    esp[c] = round(vn / (vn + fp), 3)
corte_descarte = max(c for c in cortes if sens[c] == 1)`,
  mut: [mutE('mayor_estricto', String.raw`sens, esp = {}, {}
for c in cortes:
    vp = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t > c)
    fn = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t <= c)
    vn = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t <= c)
    fp = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t > c)
    sens[c] = round(vp / (vp + fn), 3)
    esp[c] = round(vn / (vn + fp), 3)
corte_descarte = max(c for c in cortes if sens[c] == 1)`, 'Un valor igual al corte es positivo: troponina >= corte.'),
    mutE('menor', String.raw`sens, esp = {}, {}
for c in cortes:
    vp = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t >= c)
    fn = sum(1 for t, y in zip(troponina, infarto) if y == 1 and t < c)
    vn = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t < c)
    fp = sum(1 for t, y in zip(troponina, infarto) if y == 0 and t >= c)
    sens[c] = round(vp / (vp + fn), 3)
    esp[c] = round(vn / (vn + fp), 3)
corte_descarte = min(c for c in cortes if sens[c] == 1)`, 'El menor corte también tiene sensibilidad 1, pero pierde especificidad: se busca el mayor.')],
  pistas: [E('Recorre los cortes y, dentro, cuenta VP, FN, VN y FP con zip(troponina, infarto).'),
    E('Al subir el corte, la sensibilidad baja y la especificidad sube.')]
});

M({id: 'm160-3', tema: 160, k: 'code', nivel: 3,
  t: E('El área bajo la curva ROC, comprobada a mano'),
  gen: r => { const n = r.int(12, 20), v = [], y = []; for (let i = 0; i < n; i++) { const e = r.bool(.4); y.push(e ? 1 : 0); v.push(Math.round(gauss(r, e ? 60 : 40, 14))); } if (!y.includes(1)) y[0] = 1; if (!y.includes(0)) y[1] = 0; return {v, y}; },
  data: p => `${ARR('marcador', p.v, 15)}\n${ARR('enfermo', p.y, 20)}`,
  starter: () => `# Código que ha propuesto el asistente para el AUC. Verifícalo.
enf = [m for m, e in zip(marcador, enfermo) if e == 1]
sanos = [m for m, e in zip(marcador, enfermo) if e == 0]
ganados = sum(1 for a in enf for b in sanos if a >= b)
auc = round(ganados / (len(enf) + len(sanos)), 3)
`,
  enun: () => E(`<p>El AUC es la probabilidad de que un enfermo elegido al azar tenga un valor del marcador mayor que un sano elegido al azar; los empates cuentan <b>medio</b>. Calcula <code>auc</code> comparando todos los pares enfermo-sano, redondeado a 3 decimales, y <code>n_pares</code>, el número de pares comparados. Revisa el código del asistente.</p>`),
  out: ['auc', 'n_pares'],
  sol: String.raw`enf = [m for m, e in zip(marcador, enfermo) if e == 1]
sanos = [m for m, e in zip(marcador, enfermo) if e == 0]
puntos = 0
for a in enf:
    for b in sanos:
        if a > b:
            puntos += 1
        elif a == b:
            puntos += 0.5
n_pares = len(enf) * len(sanos)
auc = round(puntos / n_pares, 3)`,
  mut: [mutE('asistente', String.raw`enf = [m for m, e in zip(marcador, enfermo) if e == 1]
sanos = [m for m, e in zip(marcador, enfermo) if e == 0]
ganados = sum(1 for a in enf for b in sanos if a >= b)
n_pares = len(enf) + len(sanos)
auc = round(ganados / (len(enf) + len(sanos)), 3)`, 'El número de pares es enfermos × sanos, no su suma; y los empates valen 0,5, no 1.')],
  pistas: [E('Con 3 enfermos y 4 sanos hay 3 × 4 = 12 pares.'),
    E('Un AUC mayor que 1 indica que el denominador está mal.')]
});

/* ───── Tema 170 · Variables aleatorias discretas ───── */
QZ('m170-1', 170, 1, '¿Binomial, Poisson o ninguna?', [
  ['Número de pacientes, de 20 tratados, que responden a un antibiótico con probabilidad 0,7 cada uno, de forma independiente.', ['Binomial (n = 20, p = 0,7)', 'Poisson', 'Ninguna', 'Normal'], 'Número fijo de ensayos independientes con la misma probabilidad de éxito.'],
  ['Número de ingresos en la UCI en una noche, con una media estable de 1,8 por noche.', ['Poisson (λ = 1,8)', 'Binomial', 'Ninguna', 'Uniforme'], 'Recuento de sucesos raros e independientes en un intervalo, sin un máximo fijo.'],
  ['Número de casos de gripe en un colegio durante un brote, en el que unos niños contagian a otros.', ['Ninguna: los casos no son independientes', 'Poisson', 'Binomial', 'Normal'], 'El contagio rompe la independencia: hay sobredispersión.'],
  ['En una distribución de Poisson, la varianza es…', ['Igual a la media (λ)', 'El doble de la media', 'Igual a n · p', 'Siempre 1'], 'Si la varianza observada es mucho mayor que la media, el modelo de Poisson no se ajusta (sobredispersión).']
]);

M({id: 'm170-2', tema: 170, k: 'code', nivel: 2, pk: PK_SC,
  t: E('Probabilidad de 4 o más ingresos en la UCI en una noche'),
  gen: r => ({lam: red(0.8 + r.next() * 2.4, 1), k: r.pick([3, 4, 5])}),
  data: p => `import math\nlam = ${p.lam}   # ingresos medios por noche\nk = ${p.k}`,
  enun: () => E(`<p>Si los ingresos siguen una distribución de Poisson con media <code>lam</code>, calcula a mano (con <code>math</code>) y redondea a 4 decimales:</p><ul>
<li><code>p0</code>: probabilidad de ningún ingreso;</li>
<li><code>p_k_o_mas</code>: probabilidad de <code>k</code> o más ingresos.</li></ul><p>Después compruébalo con <code>scipy.stats.poisson</code> (por ejemplo, <code>poisson.sf(k - 1, lam)</code>).</p>`),
  out: ['p0', 'p_k_o_mas'],
  sol: String.raw`def poisson_pmf(x, lam):
    return math.exp(-lam) * lam ** x / math.factorial(x)

p0 = round(poisson_pmf(0, lam), 4)
p_k_o_mas = round(1 - sum(poisson_pmf(x, lam) for x in range(k)), 4)`,
  mut: [mutE('incluye_k', String.raw`def poisson_pmf(x, lam):
    return math.exp(-lam) * lam ** x / math.factorial(x)

p0 = round(poisson_pmf(0, lam), 4)
p_k_o_mas = round(1 - sum(poisson_pmf(x, lam) for x in range(k + 1)), 4)`, '«k o más» incluye k: al complementario solo se le restan 0, 1, …, k − 1, es decir, range(k).'),
    mutE('sf_k', String.raw`from scipy.stats import poisson
p0 = round(poisson.pmf(0, lam), 4)
p_k_o_mas = round(poisson.sf(k, lam), 4)`, 'poisson.sf(k) es P(X > k), que no incluye k. Para P(X ≥ k) usa poisson.sf(k - 1, lam).')],
  pistas: [E('P(X = x) = e^−λ · λ^x / x!'),
    E('P(X ≥ k) = 1 − P(X ≤ k − 1).')]
});

M({id: 'm170-3', tema: 170, k: 'code', nivel: 3, pk: PK_NP,
  t: E('Simular los aciertos de un modelo de IA en 40 preguntas'),
  gen: r => ({p: red(0.6 + r.next() * 0.3, 2), sem: r.int(1, 99999)}),
  data: p => `import numpy as np\np = ${p.p}        # probabilidad de acierto en cada pregunta\nsemilla = ${p.sem}`,
  starter: () => `# Código que ha propuesto el asistente. ¿Simula lo que se pide?
rng = np.random.default_rng(semilla)
aciertos = rng.binomial(1, p, size=5000)
media_sim = round(float(aciertos.mean()), 2)
var_sim = round(float(aciertos.var()), 2)
media_teo = round(40 * p, 2)
var_teo = round(40 * p * (1 - p), 2)
`,
  enun: () => E(`<p>Con <code>rng = np.random.default_rng(semilla)</code>, simula <b>5.000 exámenes</b> de 40 preguntas: <code>aciertos = rng.binomial(40, p, size=5000)</code>. Calcula, redondeados a 2 decimales:</p><ul>
<li><code>media_sim</code> y <code>var_sim</code> (varianza con <code>.var()</code>) de los aciertos simulados;</li>
<li><code>media_teo</code> = 40·p y <code>var_teo</code> = 40·p·(1 − p);</li>
<li><code>p_menos_30</code>: proporción de exámenes simulados con menos de 30 aciertos, redondeada a 3 decimales.</li></ul>`),
  out: ['media_sim', 'var_sim', 'media_teo', 'var_teo', 'p_menos_30'],
  sol: String.raw`rng = np.random.default_rng(semilla)
aciertos = rng.binomial(40, p, size=5000)
media_sim = round(float(aciertos.mean()), 2)
var_sim = round(float(aciertos.var()), 2)
media_teo = round(40 * p, 2)
var_teo = round(40 * p * (1 - p), 2)
p_menos_30 = round(float((aciertos < 30).mean()), 3)`,
  mut: [mutE('asistente', String.raw`rng = np.random.default_rng(semilla)
aciertos = rng.binomial(1, p, size=5000)
media_sim = round(float(aciertos.mean()), 2)
var_sim = round(float(aciertos.var()), 2)
media_teo = round(40 * p, 2)
var_teo = round(40 * p * (1 - p), 2)
p_menos_30 = round(float((aciertos < 30).mean()), 3)`, 'El asistente simula 5.000 preguntas sueltas (binomial con n = 1), no 5.000 exámenes de 40 preguntas: su media no se parece a 40·p.')],
  pistas: [E('rng.binomial(n, p, size) da size recuentos de aciertos en n ensayos.'),
    E('Compara la media simulada con la teórica: si no se parecen, la simulación no es la pedida.')]
});

/* ───── Tema 180 · Distribución normal e intervalos de referencia ───── */
M({id: 'm180-1', tema: 180, k: 'code', nivel: 1,
  t: E('Probabilidades y percentiles de la hemoglobina en mujeres sanas'),
  gen: r => ({mu: red(13.2 + r.next() * 0.8, 1), sd: red(0.8 + r.next() * 0.5, 1), a: r.pick([11, 11.5, 12])}),
  data: p => `from statistics import NormalDist\nmu, sd = ${p.mu}, ${p.sd}   # g/dL\numbral = ${p.a}`,
  enun: () => E(`<p>Si la hemoglobina de las mujeres sanas sigue una normal con media <code>mu</code> y desviación <code>sd</code>, calcula con <code>NormalDist(mu, sd)</code>:</p><ul>
<li><code>p_menos</code>: P(Hb &lt; umbral), redondeada a 4 decimales;</li>
<li><code>p_entre</code>: P(mu − 2·sd &lt; Hb &lt; mu + 2·sd), redondeada a 4 decimales;</li>
<li><code>p2_5</code> y <code>p97_5</code>: percentiles 2,5 y 97,5, redondeados a 1 decimal.</li></ul><p>En el examen lo harás con la tabla de la normal: comprueba aquí tus cálculos.</p>`),
  out: ['p_menos', 'p_entre', 'p2_5', 'p97_5'],
  sol: String.raw`hb = NormalDist(mu, sd)
p_menos = round(hb.cdf(umbral), 4)
p_entre = round(hb.cdf(mu + 2 * sd) - hb.cdf(mu - 2 * sd), 4)
p2_5 = round(hb.inv_cdf(0.025), 1)
p97_5 = round(hb.inv_cdf(0.975), 1)`,
  mut: [mutE('complementario', String.raw`hb = NormalDist(mu, sd)
p_menos = round(1 - hb.cdf(umbral), 4)
p_entre = round(hb.cdf(mu + 2 * sd) - hb.cdf(mu - 2 * sd), 4)
p2_5 = round(hb.inv_cdf(0.025), 1)
p97_5 = round(hb.inv_cdf(0.975), 1)`, 'cdf(x) ya es P(X < x); 1 − cdf(x) es la probabilidad de estar por encima.')],
  pistas: []
});

M({id: 'm180-2', tema: 180, k: 'code', nivel: 2, pk: PK_NP,
  t: E('Intervalo de referencia de la TSH'),
  gen: r => ({tsh: Array.from({length: r.int(120, 160)}, () => red(Math.exp(gauss(r, Math.log(1.6), 0.45)), 2))}),
  data: p => `import numpy as np\n${ARR('tsh', p.tsh, 15)}   # mU/L en voluntarios sanos`,
  enun: () => E(`<p>La TSH de los sanos es asimétrica. Calcula, redondeados a 2 decimales:</p><ul>
<li><code>param_li</code> y <code>param_ls</code>: media ± 1,96 · DE (con <i>n</i> − 1);</li>
<li><code>noparam_li</code> y <code>noparam_ls</code>: percentiles 2,5 y 97,5 con <code>np.percentile</code>.</li>
<li><code>metodo</code>: <code>'paramétrico'</code> o <code>'no paramétrico'</code>, el adecuado para esta variable (CLSI recomienda el no paramétrico con al menos 120 sanos).</li></ul>`),
  out: ['param_li', 'param_ls', 'noparam_li', 'noparam_ls', 'metodo'],
  sol: String.raw`x = np.array(tsh)
m, s = x.mean(), x.std(ddof=1)
param_li, param_ls = round(m - 1.96 * s, 2), round(m + 1.96 * s, 2)
noparam_li = round(float(np.percentile(x, 2.5)), 2)
noparam_ls = round(float(np.percentile(x, 97.5)), 2)
metodo = 'no paramétrico'`,
  mut: [mutE('percentil_5', String.raw`x = np.array(tsh)
m, s = x.mean(), x.std(ddof=1)
param_li, param_ls = round(m - 1.96 * s, 2), round(m + 1.96 * s, 2)
noparam_li = round(float(np.percentile(x, 5)), 2)
noparam_ls = round(float(np.percentile(x, 95)), 2)
metodo = 'no paramétrico'`, 'El intervalo de referencia del 95 % deja un 2,5 % a cada lado: percentiles 2,5 y 97,5.'),
    mutE('param', String.raw`x = np.array(tsh)
m, s = x.mean(), x.std(ddof=1)
param_li, param_ls = round(m - 1.96 * s, 2), round(m + 1.96 * s, 2)
noparam_li = round(float(np.percentile(x, 2.5)), 2)
noparam_ls = round(float(np.percentile(x, 97.5)), 2)
metodo = 'paramétrico'`, 'Con una variable asimétrica, media ± 1,96 DE da un límite inferior demasiado bajo y uno superior que deja fuera a demasiados sanos.')],
  pistas: [E('np.percentile(x, 2.5) da el percentil 2,5.'),
    E('Compara los dos intervalos: ¿cuál se ajusta a la forma de los datos?')]
});

M({id: 'm180-3', tema: 180, k: 'code', nivel: 3, pk: PK_NP,
  t: E('Intervalo de referencia de los triglicéridos, teniendo en cuenta la asimetría'),
  gen: r => ({tg: Array.from({length: r.int(80, 110)}, () => Math.round(Math.exp(gauss(r, Math.log(105), 0.55))))}),
  data: p => `import numpy as np\n${ARR('trigliceridos', p.tg, 15)}   # mg/dL en sanos`,
  starter: () => `# Intervalo que ha propuesto el asistente.
x = np.array(trigliceridos)
li = round(float(x.mean() - 1.96 * x.std(ddof=1)), 1)
ls = round(float(x.mean() + 1.96 * x.std(ddof=1)), 1)
`,
  enun: () => E(`<p>El asistente ha calculado el intervalo con media ± 1,96 DE sobre los valores originales, pero los triglicéridos son muy asimétricos. Calcúlalo en la escala <b>logarítmica</b>: media y DE (<i>n</i> − 1) de <code>np.log(x)</code>, límites media ± 1,96 DE, y vuelta a mg/dL con <code>np.exp</code>. Guarda <code>li</code> y <code>ls</code> redondeados a 1 decimal, y <code>pct_fuera</code>: porcentaje de los sanos de la muestra que quedan fuera de tu intervalo, redondeado a 1 decimal.</p>`),
  out: ['li', 'ls', 'pct_fuera'],
  sol: String.raw`x = np.array(trigliceridos)
lx = np.log(x)
m, s = lx.mean(), lx.std(ddof=1)
li = round(float(np.exp(m - 1.96 * s)), 1)
ls = round(float(np.exp(m + 1.96 * s)), 1)
pct_fuera = round(float(((x < li) | (x > ls)).mean() * 100), 1)`,
  mut: [mutE('asistente', String.raw`x = np.array(trigliceridos)
li = round(float(x.mean() - 1.96 * x.std(ddof=1)), 1)
ls = round(float(x.mean() + 1.96 * x.std(ddof=1)), 1)
pct_fuera = round(float(((x < li) | (x > ls)).mean() * 100), 1)`, 'En la escala original, el intervalo simétrico no respeta la asimetría: el límite inferior queda muy bajo (a veces negativo).'),
    mutE('exp_de', String.raw`x = np.array(trigliceridos)
lx = np.log(x)
m, s = lx.mean(), lx.std(ddof=1)
li = round(float(np.exp(m) - 1.96 * np.exp(s)), 1)
ls = round(float(np.exp(m) + 1.96 * np.exp(s)), 1)
pct_fuera = round(float(((x < li) | (x > ls)).mean() * 100), 1)`, 'Los límites se calculan en la escala logarítmica y después se exponencian: exp(m ± 1,96 s), no exp(m) ± 1,96 exp(s).')],
  pistas: [E('np.log(x) transforma toda la lista; np.exp deshace la transformación.'),
    E('El intervalo resultante es asimétrico alrededor de la mediana: es lo esperable.')]
});

/* ───── Tema 190 · Simulación de Monte Carlo y distribuciones muestrales ───── */
M({id: 'm190-1', tema: 190, k: 'code', nivel: 1,
  t: E('Error estándar de medias y proporciones'),
  gen: r => ({sd: r.int(8, 20), p: red(0.1 + r.next() * 0.4, 2), ns: r.sample([25, 50, 100, 200, 400, 800], 3).sort((a, b) => a - b)}),
  data: p => `import math\nde = ${p.sd}      # desviación típica de la PAS (mmHg)\np = ${p.p}      # prevalencia\n${ARR('tamanos', p.ns)}`,
  enun: () => E(`<p>Para cada tamaño muestral de <code>tamanos</code>, calcula el error estándar de la media (DE / √n) y de la proporción (√(p(1 − p)/n)), redondeados a 3 decimales, en los diccionarios <code>ee_media</code> y <code>ee_prop</code> (clave: el tamaño).</p><p>Fíjate en cuánto hay que multiplicar <i>n</i> para dividir el error estándar entre dos.</p>`),
  out: ['ee_media', 'ee_prop'],
  sol: String.raw`ee_media = {n: round(de / math.sqrt(n), 3) for n in tamanos}
ee_prop = {n: round(math.sqrt(p * (1 - p) / n), 3) for n in tamanos}`,
  mut: [mutE('sin_raiz', String.raw`ee_media = {n: round(de / n, 3) for n in tamanos}
ee_prop = {n: round(p * (1 - p) / n, 3) for n in tamanos}`, 'El error estándar disminuye con la raíz de n, no con n.')],
  pistas: []
});

M({id: 'm190-2', tema: 190, k: 'code', nivel: 2, pk: PK_NP,
  t: E('Distribución muestral de la prevalencia de hipertensión'),
  gen: r => ({p: red(0.25 + r.next() * 0.2, 2), sem: r.int(1, 99999)}),
  data: p => `import numpy as np\np = ${p.p}           # prevalencia real en la población\nsemilla = ${p.sem}`,
  enun: () => E(`<p>Con <code>rng = np.random.default_rng(semilla)</code> y <b>en este orden</b>, para n = 50, 200 y 800 simula 2.000 estudios con <code>rng.binomial(n, p, size=2000) / n</code>. Guarda en diccionarios con clave n, redondeados a 4 decimales:</p><ul>
<li><code>de_sim</code>: desviación típica de las prevalencias simuladas (<code>.std()</code>);</li>
<li><code>ee_teo</code>: error estándar teórico √(p(1 − p)/n).</li></ul>`),
  out: ['de_sim', 'ee_teo'],
  sol: String.raw`rng = np.random.default_rng(semilla)
de_sim, ee_teo = {}, {}
for n in [50, 200, 800]:
    prev = rng.binomial(n, p, size=2000) / n
    de_sim[n] = round(float(prev.std()), 4)
    ee_teo[n] = round(float(np.sqrt(p * (1 - p) / n)), 4)`,
  mut: [mutE('rng_dentro', String.raw`de_sim, ee_teo = {}, {}
for n in [50, 200, 800]:
    rng = np.random.default_rng(semilla)
    prev = rng.binomial(n, p, size=2000) / n
    de_sim[n] = round(float(prev.std()), 4)
    ee_teo[n] = round(float(np.sqrt(p * (1 - p) / n)), 4)`, 'Has creado el generador dentro del bucle: cada tamaño reutiliza la misma secuencia de números. Créalo una sola vez, antes del bucle.'),
    mutE('recuento', String.raw`rng = np.random.default_rng(semilla)
de_sim, ee_teo = {}, {}
for n in [50, 200, 800]:
    prev = rng.binomial(n, p, size=2000)
    de_sim[n] = round(float(prev.std()), 4)
    ee_teo[n] = round(float(np.sqrt(p * (1 - p) / n)), 4)`, 'rng.binomial devuelve el número de hipertensos; para la prevalencia hay que dividir entre n.')],
  pistas: [E('Crea el generador una sola vez; cada llamada a rng.binomial continúa la secuencia.'),
    E('La desviación típica de la distribución muestral es el error estándar.')]
});

M({id: 'm190-3', tema: 190, k: 'code', nivel: 3,
  t: E('Veinte respuestas de un modelo de IA a la misma pregunta'),
  gen: r => { const p = 0.5 + r.next() * 0.4; return {resp: Array.from({length: 20}, () => r.bool(p) ? 'sí' : 'no')}; },
  data: p => `import math\n${ARR('respuestas', p.resp)}   # «¿Está indicada la anticoagulación en este paciente?», repetida 20 veces`,
  starter: () => `# Análisis que ha propuesto el asistente.
p_si = respuestas.count('sí') / len(respuestas)
ee = math.sqrt(p_si * (1 - p_si))
cambios = 0
`,
  enun: () => E(`<p>Has repetido 20 veces la misma pregunta a un modelo con temperatura alta. Calcula:</p><ul>
<li><code>p_si</code>: proporción de respuestas «sí», redondeada a 2 decimales;</li>
<li><code>ee</code>: su error estándar binomial con n = 20, √(p(1 − p)/n), con <i>p</i> sin redondear, redondeado a 3 decimales;</li>
<li><code>cambios</code>: número de veces que la respuesta cambia respecto a la anterior.</li></ul>`),
  out: ['p_si', 'ee', 'cambios'],
  sol: String.raw`n = len(respuestas)
p = respuestas.count('sí') / n
p_si = round(p, 2)
ee = round(math.sqrt(p * (1 - p) / n), 3)
cambios = sum(1 for a, b in zip(respuestas, respuestas[1:]) if a != b)`,
  mut: [mutE('asistente', String.raw`p = respuestas.count('sí') / len(respuestas)
p_si = round(p, 2)
ee = round(math.sqrt(p * (1 - p)), 3)
cambios = sum(1 for a, b in zip(respuestas, respuestas[1:]) if a != b)`, 'Falta dividir entre n dentro de la raíz: √(p(1 − p)) es la desviación de una sola respuesta, no el error estándar de la proporción.')],
  pistas: [E('zip(respuestas, respuestas[1:]) empareja cada respuesta con la siguiente.'),
    E('Si un modelo cambia de respuesta clínica al repetir la pregunta, ¿qué implica para usarlo en la consulta?')]
});
