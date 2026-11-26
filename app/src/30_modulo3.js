/* ══ Módulo 3 · Procesado inicial de datos (temas 90 a 130) ══ */

/* ───── Tema 90 · Programación asistida por IA y mejora recursiva ───── */
QZ('m90-1', 90, 1, '¿Qué valores frontera faltan en las pruebas?', [
  ['Pruebas de una función que clasifica la glucemia en ayunas (normal < 100, prediabetes 100-125, diabetes ≥ 126) con los valores 85, 110 y 150. ¿Qué falta sobre todo?', ['Los valores frontera 99, 100, 125 y 126', 'Más valores entre 85 y 99', 'Un valor de 300', 'Un valor negativo'], 'Los errores típicos (< frente a <=) solo aparecen en las fronteras.'],
  ['Una función de CURB-65 se ha probado con pacientes de 40 y 80 años. ¿Qué edades deberían añadirse?', ['64 y 65', '50 y 70', '0 y 120', '18 y 100'], 'El criterio de edad cambia en 65: hay que probar justo a cada lado.'],
  ['Las pruebas de una función de IMC pasan todas, pero se escribieron mirando el código que generó la IA. ¿Cuál es el problema?', ['Pueden reproducir los mismos errores del código: deben salir de la definición clínica', 'Ninguno, si pasan', 'Que son demasiadas', 'Que no usan pandas'], 'Las pruebas se derivan de la especificación (la guía clínica), no de la implementación.'],
  ['En la mejora recursiva, ¿para qué sirven las pruebas reservadas?', ['Para medir el resultado final con casos que no se usaron para corregir el código', 'Para corregir el código en cada iteración', 'Para que el asistente aprenda', 'Para ahorrar tiempo'], 'Si se mejora mirando siempre las mismas pruebas, el código acaba ajustado a ellas (ley de Goodhart).']
]);

const WELLS = ['cancer_activo', 'paralisis_o_inmovilizacion', 'encamamiento_o_cirugia', 'dolor_trayecto_venoso', 'edema_toda_la_pierna', 'diferencia_perimetro_3cm', 'edema_con_fovea', 'venas_colaterales', 'tvp_previa'];
const wellsDe = cs => [...cs].reduce((a, c) => a + (c === 'diagnostico_alternativo' ? -2 : 1), 0);
const casoWells = (r, objetivo) => { for (let k = 0; k < 200; k++) { const c = r.sample([...WELLS, 'diagnostico_alternativo'], r.int(0, 5)); if (objetivo === undefined || wellsDe(c) === objetivo) return c; } return objetivo === 2 ? WELLS.slice(0, 2) : WELLS.slice(0, 1); };
const pySet = a => a.length ? '{' + a.map(py).join(', ') + '}' : 'set()';
M({id: 'm90-2', tema: 90, k: 'code', nivel: 2,
  t: E('Especificación y pruebas de la escala de Wells para la TVP'),
  gen: r => ({c: [casoWells(r), casoWells(r, 1), casoWells(r, 2), casoWells(r, -1)]}),
  data: () => `CRITERIOS = ${py(WELLS)}\n# además existe 'diagnostico_alternativo' (tan o más probable que la TVP)`,
  enun: () => E(`<p>La escala de Wells para la trombosis venosa profunda suma <b>1 punto</b> por cada criterio de <code>CRITERIOS</code> presente y <b>resta 2</b> si hay un <code>'diagnostico_alternativo'</code>. Con la versión de dos niveles, la TVP es <code>'probable'</code> si la puntuación es 2 o más e <code>'improbable'</code> si es menor.</p><p>Define <code>wells(criterios)</code>, que recibe un conjunto de textos y devuelve la puntuación, y <code>categoria_wells(puntos)</code>.</p>`),
  func: {names: ['wells', 'categoria_wells'], cases: p => [...p.c.map(c => ({e: `wells(${pySet(c)})`, vis: true})), {e: 'categoria_wells(2)', vis: true}, {e: 'categoria_wells(1)', vis: false}, {e: `wells(${pySet(['diagnostico_alternativo', 'tvp_previa'])})`, vis: false}]},
  req: ['def'],
  sol: String.raw`def wells(criterios):
    puntos = 0
    for c in criterios:
        if c == 'diagnostico_alternativo':
            puntos -= 2
        elif c in CRITERIOS:
            puntos += 1
    return puntos

def categoria_wells(puntos):
    return 'probable' if puntos >= 2 else 'improbable'`,
  mut: [mutE('suma_alternativo', String.raw`def wells(criterios):
    return len(criterios)

def categoria_wells(puntos):
    return 'probable' if puntos >= 2 else 'improbable'`, 'El diagnóstico alternativo no suma: resta 2 puntos.'),
    mutE('umbral', String.raw`def wells(criterios):
    return sum(-2 if c == 'diagnostico_alternativo' else 1 for c in criterios)

def categoria_wells(puntos):
    return 'probable' if puntos > 2 else 'improbable'`, 'Con 2 puntos la TVP ya es probable: el umbral es «≥ 2».')],
  pistas: [E('Recorre el conjunto con for c in criterios y acumula los puntos.'),
    E('Un if/elif dentro del bucle distingue el diagnóstico alternativo del resto.'),
    E('Prueba wells({"diagnostico_alternativo", "tvp_previa"}): debe dar −1.')]
});

M({id: 'm90-3', tema: 90, k: 'code', nivel: 3,
  t: E('Ciclo de mejora con pruebas reservadas'),
  gen: r => ({c: [casoWells(r, 0), casoWells(r, 2), casoWells(r, 3)]}),
  data: () => `CRITERIOS = ${py(WELLS)}`,
  starter: () => `# Versión 1 que ha propuesto el asistente. Escribe tus pruebas, ejecútalas y corrige la función.
def wells(criterios):
    puntos = 0
    for c in criterios:
        if c == 'diagnostico_alternativo':
            puntos += 2
        else:
            puntos += 1
    return puntos

def categoria_wells(puntos):
    return 'probable' if puntos > 2 else 'improbable'

# Tus pruebas: lista de pares (conjunto de criterios, puntuación esperada)
pruebas = []
`,
  enun: () => E(`<p>Aplica el ciclo de mejora recursiva a la versión del asistente de la escala de Wells (1 punto por criterio, −2 por diagnóstico alternativo; probable si ≥ 2):</p><ol>
<li>Escribe en <code>pruebas</code> al menos <b>6</b> pares <code>(criterios, puntuación_esperada)</code> calculados por ti a partir de la definición, que incluyan las puntuaciones frontera <b>1 y 2</b> y algún caso con diagnóstico alternativo.</li>
<li>Corrige <code>wells</code> y <code>categoria_wells</code> hasta que pasen tus pruebas.</li></ol><p>La app comprobará tus pruebas y, además, probará tu función con <b>pruebas reservadas</b> que no ves.</p>`),
  func: {names: ['wells', 'categoria_wells'], cases: p => [
    {e: 'len(pruebas) >= 6', vis: true}, {e: 'all(wells(c) == e for c, e in pruebas)', vis: true}, {e: '{1, 2} <= {e for _, e in pruebas}', vis: true},
    {e: "any('diagnostico_alternativo' in c for c, _ in pruebas)", vis: true},
    ...p.c.map(c => ({e: `wells(${pySet(c)})`, vis: false})), {e: 'categoria_wells(2)', vis: false}]},
  req: ['def'],
  sol: String.raw`def wells(criterios):
    puntos = 0
    for c in criterios:
        if c == 'diagnostico_alternativo':
            puntos -= 2
        elif c in CRITERIOS:
            puntos += 1
    return puntos

def categoria_wells(puntos):
    return 'probable' if puntos >= 2 else 'improbable'

pruebas = [
    (set(), 0),
    ({'tvp_previa'}, 1),
    ({'tvp_previa', 'cancer_activo'}, 2),
    ({'edema_toda_la_pierna', 'edema_con_fovea', 'venas_colaterales'}, 3),
    ({'diagnostico_alternativo'}, -2),
    ({'diagnostico_alternativo', 'tvp_previa', 'cancer_activo'}, 0),
]`,
  mut: [mutE('sin_pruebas', String.raw`def wells(criterios):
    return sum(-2 if c == 'diagnostico_alternativo' else 1 for c in criterios)

def categoria_wells(puntos):
    return 'probable' if puntos >= 2 else 'improbable'

pruebas = [({'tvp_previa'}, 1), ({'tvp_previa', 'cancer_activo'}, 2)]`, 'La función ya está bien, pero tus pruebas son demasiado pocas: escribe al menos 6, con las fronteras 1 y 2 y algún diagnóstico alternativo.')],
  pistas: [E('Calcula tú cada puntuación esperada a partir de la definición, no ejecutando la función.'),
    E('Un par de prueba se escribe así: ({"tvp_previa", "cancer_activo"}, 2).'),
    E('El asistente suma el diagnóstico alternativo y usa «> 2» como umbral: dos errores.')]
});

/* ───── Tema 100 · Pandas: valores perdidos y atípicos ───── */
QZ('m100-1', 100, 1, '¿Error de registro, atípico real o dato plausible?', [
  ['Un adulto con un peso registrado de 680 kg.', ['Error de registro', 'Valor atípico real', 'Dato plausible', 'Dato ausente'], 'Es fisiológicamente imposible: probablemente 68,0 kg con la coma desplazada.'],
  ['Una glucemia de 520 mg/dL en un paciente atendido en Urgencias por cetoacidosis diabética.', ['Valor atípico real', 'Error de registro', 'Dato ausente', 'Dato plausible en cualquier paciente'], 'Es extremo pero coherente con el contexto clínico: no se elimina.'],
  ['Una talla de 1,72 en una columna en la que el resto de valores están en centímetros (165, 180…).', ['Error de registro (unidades): se convierte a 172 cm', 'Valor atípico real', 'Dato plausible', 'Se elimina el paciente'], 'Es un error de unidades que se puede corregir de forma justificada y documentada.'],
  ['Una PAS de 185 mmHg en un paciente con hipertensión mal controlada.', ['Dato plausible', 'Error de registro', 'Dato ausente', 'Debe eliminarse por ser atípico'], 'Es alto pero clínicamente posible: eliminarlo sesgaría el análisis.']
]);

M({id: 'm100-2', tema: 100, k: 'code', nivel: 2, pk: PK_PD,
  t: E('Limpiar un registro de pacientes con EPOC'),
  gen: r => {
    const n = r.int(10, 14), f = {id: ids('EPOC', n), sexo: [], edad: [], fev1_l: []};
    const graf = {Hombre: ['Hombre', 'hombre', 'H', ' h', 'HOMBRE'], Mujer: ['Mujer', 'mujer', 'M', 'm ', 'MUJER']};
    for (let i = 0; i < n; i++) { const s = r.pick(['Hombre', 'Mujer']); f.sexo.push(r.pick(graf[s])); f.edad.push(r.int(45, 88)); f.fev1_l.push(red(0.7 + r.next() * 1.9, 2)); }
    r.sample([...Array(n).keys()], r.int(1, 3)).forEach(i => { f.fev1_l[i] = Math.round(f.fev1_l[i] * 1000); });
    const d = r.sample([...Array(n).keys()], r.int(1, 2)); d.forEach(i => { for (const k of Object.keys(f)) f[k].push(f[k][i]); });
    return {f};
  },
  data: p => `import pandas as pd\n${pyDF('registro', p.f)}`,
  enun: () => E(`<p>El registro tiene filas duplicadas, el sexo escrito de varias formas y algunos FEV1 en mililitros en lugar de litros. Crea <code>limpio</code> y calcula:</p><ol>
<li><code>n_duplicados</code>: filas eliminadas al quitar los pacientes repetidos (mismo <code>id</code>, se conserva la primera).</li>
<li>Unifica <code>sexo</code> en <code>'Hombre'</code> y <code>'Mujer'</code>. <code>sexos</code>: lista ordenada de los valores distintos que quedan.</li>
<li><code>n_fev1_corregidos</code>: número de FEV1 mayores de 20 (están en mL), que debes pasar a litros.</li>
<li><code>n_final</code>: número de pacientes; <code>fev1_medio</code>: FEV1 medio en litros, redondeado a 2 decimales.</li></ol>`),
  out: ['n_duplicados', 'sexos', 'n_fev1_corregidos', 'n_final', 'fev1_medio'],
  sol: String.raw`limpio = registro.drop_duplicates(subset='id').copy()
n_duplicados = len(registro) - len(limpio)
limpio['sexo'] = limpio['sexo'].str.strip().str.lower().str[0].map({'h': 'Hombre', 'm': 'Mujer'})
sexos = sorted(limpio['sexo'].unique().tolist())
en_ml = limpio['fev1_l'] > 20
n_fev1_corregidos = int(en_ml.sum())
limpio.loc[en_ml, 'fev1_l'] = limpio.loc[en_ml, 'fev1_l'] / 1000
n_final = len(limpio)
fev1_medio = round(limpio['fev1_l'].mean(), 2)`,
  mut: [mutE('sin_ml', String.raw`limpio = registro.drop_duplicates(subset='id').copy()
n_duplicados = len(registro) - len(limpio)
limpio['sexo'] = limpio['sexo'].str.strip().str.lower().str[0].map({'h': 'Hombre', 'm': 'Mujer'})
sexos = sorted(limpio['sexo'].unique().tolist())
n_fev1_corregidos = int((limpio['fev1_l'] > 20).sum())
n_final = len(limpio)
fev1_medio = round(limpio['fev1_l'].mean(), 2)`, 'Has contado los FEV1 en mililitros pero no los has convertido: la media queda multiplicada por cientos.'),
    mutE('con_duplicados', String.raw`limpio = registro.copy()
n_duplicados = int(registro.duplicated(subset='id').sum())
limpio['sexo'] = limpio['sexo'].str.strip().str.lower().str[0].map({'h': 'Hombre', 'm': 'Mujer'})
sexos = sorted(limpio['sexo'].unique().tolist())
en_ml = limpio['fev1_l'] > 20
n_fev1_corregidos = int(en_ml.sum())
limpio.loc[en_ml, 'fev1_l'] = limpio.loc[en_ml, 'fev1_l'] / 1000
n_final = len(limpio)
fev1_medio = round(limpio['fev1_l'].mean(), 2)`, 'Has contado los duplicados pero no los has eliminado: hay pacientes que cuentan dos veces.')],
  pistas: [E('drop_duplicates(subset="id") elimina las filas repetidas por identificador; añade .copy() para modificar después.'),
    E('.str.strip().str.lower().str[0] deja solo la inicial en minúscula; .map({...}) la traduce.'),
    E('Con una máscara booleana: limpio.loc[mascara, "fev1_l"] = limpio.loc[mascara, "fev1_l"] / 1000.')]
});

M({id: 'm100-3', tema: 100, k: 'code', nivel: 3, pk: PK_PD,
  t: E('Auditar la limpieza que propone el asistente'),
  gen: r => {
    const n = r.int(12, 16), f = {id: ids('CV', n), pas_mmHg: r.ints(n, 105, 178), colesterol: Array.from({length: n}, () => r.int(150, 290))};
    r.sample([...Array(n).keys()], r.int(2, 4)).forEach(i => { f.colesterol[i] = null; });
    r.sample([...Array(n).keys()], r.int(1, 2)).forEach(i => { f.pas_mmHg[i] = r.pick([0, 1300, 14]); });
    return {f};
  },
  data: p => `import pandas as pd\n${pyDF('registro', p.f)}`,
  starter: () => `# Limpieza que ha propuesto el asistente. Audítala y corrígela.
limpio = registro.dropna()
limpio = limpio[(limpio['pas_mmHg'] > 50) & (limpio['pas_mmHg'] < 300)]
n_final = len(limpio)
n_pas_imposibles = len(registro) - n_final
n_colesterol_ausentes = 0
pas_media = round(limpio['pas_mmHg'].mean(), 1)
`,
  enun: () => E(`<p>El asistente elimina cualquier paciente con algún dato ausente y también los que tienen una PAS imposible. Así se pierden pacientes con datos válidos. Corrige la limpieza para que:</p><ul>
<li>no se elimine <b>ningún</b> paciente: <code>n_final</code> es el número de filas de <code>limpio</code>;</li>
<li>las PAS imposibles (≤ 50 o ≥ 300 mmHg) se conviertan en dato ausente (<code>NaN</code>); <code>n_pas_imposibles</code> es cuántas había;</li>
<li><code>n_colesterol_ausentes</code>: número de colesteroles ausentes;</li>
<li><code>pas_media</code>: PAS media de los valores válidos, redondeada a 1 decimal.</li></ul>`),
  out: ['n_final', 'n_pas_imposibles', 'n_colesterol_ausentes', 'pas_media'],
  sol: String.raw`limpio = registro.copy()
imposible = (limpio['pas_mmHg'] <= 50) | (limpio['pas_mmHg'] >= 300)
n_pas_imposibles = int(imposible.sum())
limpio['pas_mmHg'] = limpio['pas_mmHg'].mask(imposible)
n_final = len(limpio)
n_colesterol_ausentes = int(limpio['colesterol'].isna().sum())
pas_media = round(limpio['pas_mmHg'].mean(), 1)`,
  mut: [mutE('asistente', String.raw`limpio = registro.dropna()
limpio = limpio[(limpio['pas_mmHg'] > 50) & (limpio['pas_mmHg'] < 300)]
n_final = len(limpio)
n_pas_imposibles = len(registro) - n_final
n_colesterol_ausentes = 0
pas_media = round(limpio['pas_mmHg'].mean(), 1)`, 'Es la limpieza del asistente: dropna() elimina pacientes cuya PAS es válida solo porque les falta el colesterol.'),
    mutE('pas_cero', String.raw`limpio = registro.copy()
imposible = (limpio['pas_mmHg'] <= 50) | (limpio['pas_mmHg'] >= 300)
n_pas_imposibles = int(imposible.sum())
limpio.loc[imposible, 'pas_mmHg'] = 0
n_final = len(limpio)
n_colesterol_ausentes = int(limpio['colesterol'].isna().sum())
pas_media = round(limpio['pas_mmHg'].mean(), 1)`, 'Un valor imposible no se convierte en 0 sino en ausente (NaN): un 0 entra en la media.')],
  pistas: [E('.isna().sum() cuenta los valores ausentes de una columna.'),
    E('serie.mask(condicion) pone NaN donde la condición es True.'),
    E('pandas ignora los NaN al calcular la media.')]
});

/* ───── Tema 110 · Integración de datos clínicos y tablas de frecuencias ───── */
M({id: 'm110-1', tema: 110, k: 'predict', nivel: 1, pk: PK_PD,
  t: E('¿Cuántas filas da cada unión?'),
  gen: r => { const a = r.sample(['P1', 'P2', 'P3', 'P4', 'P5', 'P6'], r.int(3, 5)).sort(), b = r.sample(['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'], r.int(3, 5)).sort(); return {a, b}; },
  predict: p => `import pandas as pd
pacientes = pd.DataFrame({'id': ${py(p.a)}})
analiticas = pd.DataFrame({'id': ${py(p.b)}})
print(len(pacientes.merge(analiticas, on='id', how='inner')))
print(len(pacientes.merge(analiticas, on='id', how='left')))
print(len(pacientes.merge(analiticas, on='id', how='outer')))`,
  enun: () => E('<p>Sin ejecutarlo, escribe los tres números que imprimirá el programa: las filas de la unión interna, por la izquierda y completa.</p>'),
  mut: [{id: 'izq_derecha', alt: p => { const i = p.a.filter(x => p.b.includes(x)).length; return `${i}\n${p.b.length}\n${new Set([...p.a, ...p.b]).size}`; }, msg: E('how="left" conserva todas las filas de la tabla de la izquierda (pacientes), no de la derecha.')}],
  pistas: []
});

M({id: 'm110-2', tema: 110, k: 'code', nivel: 2, pk: PK_PD,
  t: E('Unir la cohorte con las analíticas y tabular el filtrado glomerular'),
  gen: r => {
    const n = r.int(14, 20), idc = ids('CV', n), edad = r.ints(n, 40, 88);
    const idx = r.sample([...Array(n).keys()], n - r.int(1, 3)).sort((a, b) => a - b);
    return {c: {id: idc, edad}, a: {id: idx.map(i => idc[i]), fge: idx.map(() => r.pick([r.int(8, 14), r.int(15, 29), r.int(30, 44), r.int(45, 59), r.int(60, 89), r.int(60, 89), r.int(90, 120), 90, 60, 30]))}};
  },
  data: p => `import pandas as pd\n${pyDF('cohorte', p.c)}\n${pyDF('analiticas', p.a)}   # FG estimado en mL/min/1,73 m²`,
  enun: () => E(`<p>Une la cohorte con las analíticas conservando solo los pacientes que tienen analítica, y clasifica el filtrado glomerular estimado según KDIGO: <b>G1</b> ≥ 90, <b>G2</b> 60-89, <b>G3a</b> 45-59, <b>G3b</b> 30-44, <b>G4</b> 15-29, <b>G5</b> &lt; 15.</p><ul>
<li><code>n_unidos</code>: número de pacientes tras la unión.</li>
<li><code>frecuencias</code>: diccionario con el número de pacientes de cada categoría, con <b>las seis</b> claves en el orden G1 a G5 (también las que tengan 0).</li>
<li><code>pct_g3_o_peor</code>: porcentaje de pacientes con FG &lt; 60, redondeado a 1 decimal.</li></ul>`),
  out: ['n_unidos', 'frecuencias', 'pct_g3_o_peor'],
  sol: String.raw`unidos = cohorte.merge(analiticas, on='id', how='inner')
n_unidos = len(unidos)
categorias = ['G5', 'G4', 'G3b', 'G3a', 'G2', 'G1']
unidos['kdigo'] = pd.cut(unidos['fge'], bins=[0, 15, 30, 45, 60, 90, 1000], labels=categorias, right=False)
conteo = unidos['kdigo'].value_counts()
frecuencias = {c: int(conteo[c]) for c in ['G1', 'G2', 'G3a', 'G3b', 'G4', 'G5']}
pct_g3_o_peor = round((unidos['fge'] < 60).mean() * 100, 1)`,
  mut: [mutE('right', String.raw`unidos = cohorte.merge(analiticas, on='id', how='inner')
n_unidos = len(unidos)
categorias = ['G5', 'G4', 'G3b', 'G3a', 'G2', 'G1']
unidos['kdigo'] = pd.cut(unidos['fge'], bins=[0, 15, 30, 45, 60, 90, 1000], labels=categorias)
conteo = unidos['kdigo'].value_counts()
frecuencias = {c: int(conteo[c]) for c in ['G1', 'G2', 'G3a', 'G3b', 'G4', 'G5']}
pct_g3_o_peor = round((unidos['fge'] < 60).mean() * 100, 1)`, 'Por defecto pd.cut incluye el extremo derecho: un FG de 60 caería en G3a. Usa right=False para que 60 sea G2.'),
    mutE('left', String.raw`unidos = cohorte.merge(analiticas, on='id', how='left')
n_unidos = len(unidos)
categorias = ['G5', 'G4', 'G3b', 'G3a', 'G2', 'G1']
unidos['kdigo'] = pd.cut(unidos['fge'], bins=[0, 15, 30, 45, 60, 90, 1000], labels=categorias, right=False)
conteo = unidos['kdigo'].value_counts()
frecuencias = {c: int(conteo[c]) for c in ['G1', 'G2', 'G3a', 'G3b', 'G4', 'G5']}
pct_g3_o_peor = round((unidos['fge'] < 60).mean() * 100, 1)`, 'Con how="left" entran pacientes sin analítica y cuentan en el denominador del porcentaje.')],
  pistas: [E('merge(..., on="id", how="inner") conserva solo los identificadores presentes en las dos tablas.'),
    E('pd.cut(serie, bins=[...], labels=[...], right=False) crea los intervalos [a, b).'),
    E('value_counts() no incluye el orden que quieres: construye el diccionario recorriendo la lista de categorías.')]
});

M({id: 'm110-3', tema: 110, k: 'code', nivel: 3, pk: PK_PD,
  t: E('La «Tabla 1» de la cohorte por sexo'),
  gen: r => { const c = cohorteJS(r, r.int(20, 30)); return {c: sel(c, ['sexo', 'edad', 'diabetes'])}; },
  data: p => `import pandas as pd\n${pyDF('cohorte', p.c)}`,
  starter: () => `# Código que ha propuesto el asistente. Verifica tres cifras a mano y corrígelo.
edad_media = {}
pct_diabetes = {}
for s in ['Hombre', 'Mujer']:
    grupo = cohorte[cohorte['sexo'] == s]
    edad_media[s] = round(grupo['edad'].mean(), 1)
    pct_diabetes[s] = round(grupo['diabetes'].sum() / len(cohorte) * 100, 1)
n = cohorte['sexo'].value_counts().to_dict()
`,
  enun: () => E(`<p>La «Tabla 1» de un artículo describe a los pacientes de cada grupo. Corrige el código del asistente para obtener, con las claves <code>'Hombre'</code> y <code>'Mujer'</code>:</p><ul>
<li><code>n</code>: número de pacientes de cada sexo;</li>
<li><code>edad_media</code>: edad media de cada sexo, redondeada a 1 decimal;</li>
<li><code>pct_diabetes</code>: porcentaje de diabéticos <b>dentro de cada sexo</b>, redondeado a 1 decimal.</li></ul>`),
  out: ['n', 'edad_media', 'pct_diabetes'],
  sol: String.raw`n = cohorte['sexo'].value_counts().to_dict()
edad_media = {s: round(g['edad'].mean(), 1) for s, g in cohorte.groupby('sexo')}
pct_diabetes = {s: round(g['diabetes'].mean() * 100, 1) for s, g in cohorte.groupby('sexo')}`,
  mut: [mutE('asistente', String.raw`edad_media = {}
pct_diabetes = {}
for s in ['Hombre', 'Mujer']:
    grupo = cohorte[cohorte['sexo'] == s]
    edad_media[s] = round(grupo['edad'].mean(), 1)
    pct_diabetes[s] = round(grupo['diabetes'].sum() / len(cohorte) * 100, 1)
n = cohorte['sexo'].value_counts().to_dict()`, 'El asistente divide los diabéticos de cada sexo entre el total de la cohorte: el denominador debe ser el número de pacientes de ese sexo.')],
  pistas: [E('Verifica a mano: cuenta los hombres diabéticos y divídelos entre el número de hombres.'),
    E('La media de una columna 0/1 es la proporción de unos.')]
});

/* ───── Tema 120 · Estadística descriptiva univariante ───── */
M({id: 'm120-1', tema: 120, k: 'code', nivel: 1,
  t: E('Media, mediana y desviación típica de 7 hemoglobinas'),
  gen: r => ({hb: Array.from({length: 7}, () => red(9 + r.next() * 8, 1))}),
  data: p => `import statistics\n${ARR('hb', p.hb)}   # g/dL`,
  enun: () => E(`<p>Calcula, redondeadas a 2 decimales: <code>media</code>, <code>mediana</code> y <code>de</code> (desviación típica <b>muestral</b>, con <i>n</i> − 1).</p><p>Hazlo primero a mano y después compruébalo con el módulo <code>statistics</code>.</p>`),
  out: ['media', 'mediana', 'de'],
  sol: String.raw`media = round(statistics.mean(hb), 2)
mediana = round(statistics.median(hb), 2)
de = round(statistics.stdev(hb), 2)`,
  mut: [mutE('poblacional', String.raw`media = round(statistics.mean(hb), 2)
mediana = round(statistics.median(hb), 2)
de = round(statistics.pstdev(hb), 2)`, 'pstdev divide entre n (desviación poblacional). Con una muestra se usa n − 1: statistics.stdev.')],
  pistas: []
});

M({id: 'm120-2', tema: 120, k: 'code', nivel: 2, pk: PK_NP,
  t: E('Describir el LDL y la HbA1c de la cohorte'),
  gen: r => { const c = cohorteJS(r, r.int(30, 45)); return {ldl: c.ldl, hba1c: c.hba1c}; },
  data: p => `import numpy as np\n${ARR('ldl', p.ldl)}   # mg/dL\n${ARR('hba1c', p.hba1c)}   # %`,
  enun: () => E(`<p>El LDL tiene una distribución aproximadamente simétrica; la HbA1c es asimétrica, porque mezcla diabéticos y no diabéticos. Elige y calcula el resumen adecuado de cada una:</p><ul>
<li><code>ldl_media</code> y <code>ldl_de</code> (con <i>n</i> − 1), redondeadas a 1 decimal;</li>
<li><code>hba1c_mediana</code>, <code>hba1c_q1</code> y <code>hba1c_q3</code> (percentiles 25 y 75 con <code>np.percentile</code>), redondeados a 2 decimales;</li>
<li><code>resumen_hba1c</code>: <code>'media y DE'</code> o <code>'mediana y RIC'</code>, según el adecuado.</li></ul>`),
  out: ['ldl_media', 'ldl_de', 'hba1c_mediana', 'hba1c_q1', 'hba1c_q3', 'resumen_hba1c'],
  sol: String.raw`ldl_media = round(np.mean(ldl), 1)
ldl_de = round(np.std(ldl, ddof=1), 1)
hba1c_mediana = round(np.median(hba1c), 2)
hba1c_q1 = round(np.percentile(hba1c, 25), 2)
hba1c_q3 = round(np.percentile(hba1c, 75), 2)
resumen_hba1c = 'mediana y RIC'`,
  mut: [mutE('ddof', String.raw`ldl_media = round(np.mean(ldl), 1)
ldl_de = round(np.std(ldl), 1)
hba1c_mediana = round(np.median(hba1c), 2)
hba1c_q1 = round(np.percentile(hba1c, 25), 2)
hba1c_q3 = round(np.percentile(hba1c, 75), 2)
resumen_hba1c = 'mediana y RIC'`, 'np.std divide entre n por defecto: para la desviación muestral usa ddof=1.'),
    mutE('media_asim', String.raw`ldl_media = round(np.mean(ldl), 1)
ldl_de = round(np.std(ldl, ddof=1), 1)
hba1c_mediana = round(np.median(hba1c), 2)
hba1c_q1 = round(np.percentile(hba1c, 25), 2)
hba1c_q3 = round(np.percentile(hba1c, 75), 2)
resumen_hba1c = 'media y DE'`, 'Con una distribución asimétrica, la media y la DE describen mal a los pacientes: usa la mediana y el rango intercuartílico.')],
  pistas: [E('np.std(x, ddof=1) da la desviación típica muestral.'),
    E('np.percentile(x, 25) y np.percentile(x, 75) dan los cuartiles.')]
});

M({id: 'm120-3', tema: 120, k: 'code', nivel: 3, pk: PK_PD,
  t: E('¿n o n − 1? Corrige los resúmenes del asistente'),
  gen: r => { const c = cohorteJS(r, r.int(25, 35)); return {c: sel(c, ['edad', 'imc', 'pas', 'hdl'])}; },
  data: p => `import pandas as pd\nimport numpy as np\n${pyDF('cohorte', p.c)}`,
  starter: () => `# Código que ha propuesto el asistente. ¿Usa n o n - 1?
de = {}
for v in ['edad', 'imc', 'pas', 'hdl']:
    de[v] = round(float(np.std(cohorte[v])), 2)
cv = {v: round(de[v] / cohorte[v].mean() * 100, 1) for v in de}
`,
  enun: () => E(`<p>Corrige el código para que <code>de</code> contenga la desviación típica <b>muestral</b> (<i>n</i> − 1) de cada variable, redondeada a 2 decimales, y <code>cv</code> el coeficiente de variación (DE / media · 100) calculado con esa DE <b>sin redondear</b> y redondeado a 1 decimal.</p>`),
  out: ['de', 'cv'],
  sol: String.raw`de, cv = {}, {}
for v in ['edad', 'imc', 'pas', 'hdl']:
    s = cohorte[v].std()
    de[v] = round(float(s), 2)
    cv[v] = round(float(s / cohorte[v].mean() * 100), 1)`,
  mut: [mutE('asistente', String.raw`de = {}
for v in ['edad', 'imc', 'pas', 'hdl']:
    de[v] = round(float(np.std(cohorte[v])), 2)
cv = {v: round(de[v] / cohorte[v].mean() * 100, 1) for v in de}`, 'np.std usa n; la desviación muestral (la de pandas, .std()) usa n − 1. Además el CV se calcula con la DE redondeada.')],
  pistas: [E('Compara np.std(cohorte["edad"]) con cohorte["edad"].std(): ¿por qué difieren?'),
    E('Guarda la DE sin redondear en una variable y redondea solo al final.')]
});

/* ───── Tema 130 · Análisis bivariante ───── */
QZ('m130-1', 130, 1, 'Emparejar gráficos de dispersión con su correlación', [
  ['Los puntos de PAS frente a edad forman una nube alargada que sube, con bastante dispersión. ¿Qué r es más probable?', ['0,5', '−0,5', '0,98', '0'], 'Una relación positiva moderada.'],
  ['Los puntos de FEV1 frente a años de tabaquismo bajan casi en línea recta. ¿Qué r es más probable?', ['−0,9', '0,9', '0', '−0,1'], 'Relación negativa fuerte.'],
  ['Los puntos forman una U perfecta (riesgo alto con IMC muy bajo y muy alto). ¿Qué r es más probable?', ['Cercano a 0, aunque la relación es fuerte', '1', '−1', '0,7'], 'El coeficiente de Pearson solo mide la relación lineal: no detecta una U.'],
  ['Una nube sin relación, más un único paciente muy alejado en la esquina superior derecha. ¿Qué ocurre con r?', ['Puede salir alto por ese único punto', 'Sigue siendo 0', 'Se vuelve negativo', 'No se puede calcular'], 'Pearson es sensible a los atípicos: por eso hay que mirar siempre el gráfico o usar Spearman.']
]);

M({id: 'm130-2', tema: 130, k: 'code', nivel: 2, pk: PK_PD,
  t: E('IMC y presión arterial, por separado en hombres y mujeres'),
  gen: r => { const c = cohorteJS(r, r.int(30, 50)); return {c: sel(c, ['sexo', 'imc', 'pas'])}; },
  data: p => `import pandas as pd\n${pyDF('cohorte', p.c)}`,
  enun: () => E(`<p>Calcula el coeficiente de correlación de Pearson entre el IMC y la PAS, redondeado a 2 decimales:</p><ul>
<li><code>r_global</code>: en toda la cohorte;</li>
<li><code>r_por_sexo</code>: diccionario con las claves <code>'Hombre'</code> y <code>'Mujer'</code>;</li>
<li><code>r2_global</code>: proporción de la variabilidad de la PAS explicada linealmente por el IMC (<i>r</i>² con <i>r</i> sin redondear), redondeada a 3 decimales.</li></ul>`),
  out: ['r_global', 'r_por_sexo', 'r2_global'],
  sol: String.raw`r = cohorte['imc'].corr(cohorte['pas'])
r_global = round(r, 2)
r2_global = round(r ** 2, 3)
r_por_sexo = {s: round(g['imc'].corr(g['pas']), 2) for s, g in cohorte.groupby('sexo')}`,
  mut: [mutE('r2_redondeado', String.raw`r_global = round(cohorte['imc'].corr(cohorte['pas']), 2)
r2_global = round(r_global ** 2, 3)
r_por_sexo = {s: round(g['imc'].corr(g['pas']), 2) for s, g in cohorte.groupby('sexo')}`, 'Has elevado al cuadrado el r ya redondeado: calcula r² con el valor completo.')],
  pistas: [E('serie1.corr(serie2) calcula Pearson.'),
    E('groupby("sexo") permite repetir el cálculo en cada grupo.')]
});

QZ('m130-3', 130, 3, 'Conclusiones causales injustificadas de un análisis exploratorio', [
  ['El asistente concluye: «Los pacientes con más IMC tienen más PAS (r = 0,3): adelgazar baja la tensión». ¿Cómo se reescribe correctamente?', ['«En esta cohorte, un IMC mayor se asoció con una PAS mayor (r = 0,3)»', '«El IMC causa hipertensión»', '«El IMC explica el 30 % de la PAS»', '«Adelgazar 1 kg/m² baja la PAS 0,3 mmHg»'], 'Un estudio transversal muestra asociación, no efecto. r = 0,3 tampoco es un porcentaje explicado (r² = 0,09).'],
  ['«Los diabéticos de la cohorte tienen más eventos: la diabetes es la causa». ¿Qué variable puede confundir esa asociación?', ['La edad', 'El número de identificación', 'El centro de salud del investigador', 'El orden de las filas'], 'La diabetes es más frecuente en los mayores, que tienen más eventos por su edad (Temas 130 y 270).'],
  ['«La creatinina y la PAS están correlacionadas: la hipertensión daña el riñón de estos pacientes». ¿Qué falta antes de decirlo?', ['Considerar la edad, que eleva las dos, y la causalidad inversa', 'Un gráfico de sectores', 'Calcular la media de la creatinina', 'Nada: la correlación lo demuestra'], 'La enfermedad renal también eleva la presión: la dirección causal no se deduce de una correlación.'],
  ['¿Qué diseño permitiría estimar el efecto causal de un fármaco sobre la PAS?', ['Un ensayo clínico aleatorizado', 'Una correlación en la cohorte', 'Un gráfico de dispersión', 'Una tabla de frecuencias'], 'La aleatorización reparte por igual los factores conocidos y desconocidos.']
]);
