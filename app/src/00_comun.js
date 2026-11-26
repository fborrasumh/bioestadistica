/* ══ comun.js — Bioestadística: módulos, temas (generados desde los cuadernos), registro de misiones y utilidades de datos.
   Todos los datos son SINTÉTICOS y los nombres, inventados. ══ */
const REPO_URL = 'https://github.com/fborrasumh/bioestadistica';
const colabGH = f => `https://colab.research.google.com/github/fborrasumh/bioestadistica/blob/main/cuadernos/${f}`;
const UNIDADES = [
  {u: '1', t: L('Descubriendo Python'), url: REPO_URL},
  {u: '2', t: L('Programando con IA'), url: REPO_URL},
  {u: '3', t: L('Procesado inicial de datos'), url: REPO_URL},
  {u: '4', t: L('Probabilidad'), url: REPO_URL},
  {u: '5', t: L('Generalización de conclusiones'), url: REPO_URL}
];
/*@@TEMAS@@*/
const videoUrl = id => id;

/* ── registro de misiones ── */
const MIS = [];
const M = o => { o.ayuda = o.nivel === 1 ? 'ninguna' : o.nivel === 2 ? 'pistas' : 'ia'; MIS.push(o); return o; };
const misionPorId = id => MIS.find(m => m.id === id);
const misionesDeTema = n => MIS.filter(m => m.tema === n);

function instancia(m, seed) {
  const p = m.gen ? m.gen(Rng(seed)) : {};
  const nOcultos = m.k === 'code' ? (m.ocultos ?? 2) : 0;
  const ocultos = [];
  for (let j = 0; j < nOcultos; j++) { const q = m.gen(Rng(semillaOculta(seed, j)), j); ocultos.push({p: q, data: m.data ? m.data(q) : ''}); }
  return {p, seed, data: m.data ? m.data(p) : '', starter: m.starter ? m.starter(p) : '', ocultos};
}
function buildSpec(m, inst, student) {
  if (m.k === 'predict') return {mode: 'predict', code: m.predict(inst.p), answer: student};
  const spec = {mode: 'code', student, data: inst.data, sol: m.sol, out: m.out || [], stdout: !!m.stdout, req: m.req || [],
    mut: (m.mut || []).map(x => ({id: x.id, code: x.code})), ocultos: inst.ocultos.map(o => ({data: o.data}))};
  if (m.func) spec.func = {names: m.func.names, cases: m.func.cases(inst.p)};
  if (m.file) spec.file = m.file;
  if (m.plot) spec.plot = {n_axes: m.plot.n_axes, axes: m.plot.axes.map(a => { const o = {data: !!a.data}; if (a.marker) o.marker = a.marker; for (const f of ['title', 'xlabel', 'ylabel']) if (a[f]) o[f] = Object.values(a[f]); return o; })};
  return spec;
}
const nn = num;
const ARR = (nombre, v, n = 10) => pyLista(nombre, v, n);

/* ── atajos para escribir misiones en español (los otros idiomas caen al español) ── */
const E = s => L(s);
/* test de 4 preguntas: cada pregunta [enunciado, [correcta, distractor, distractor, distractor], explicación]; la app baraja las opciones */
function QZ(id, tema, nivel, titulo, preguntas, pistas = []) {
  return M({id, tema, k: 'quiz', nivel, t: E(titulo),
    quiz: preguntas.map(([q, o, exp]) => ({q: E(q), o: o.map(E), ok: 0, exp: E(exp)})), pistas: pistas.map(E)});
}
const mutE = (id, code, msg) => ({id, code, msg: E(msg)});

/* ── generación de datos sintéticos ── */
const gauss = (r, mu = 0, sd = 1) => { let u = 0, v = 0; while (u === 0) u = r.next(); v = r.next(); return mu + sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const red = (x, d = 1) => +(+x).toFixed(d);
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const ids = (pref, n, ini = 1) => Array.from({length: n}, (_, i) => `${pref}-${String(ini + i).padStart(3, '0')}`);
/* DataFrame de pandas como literal, una columna por línea */
function pyDF(nombre, cols, porLinea = 12) {
  const lin = Object.entries(cols).map(([k, v]) => {
    if (v.length <= porLinea) return `    ${py(k)}: ${py(v)},`;
    const trozos = chunk(v, porLinea).map(c => '        ' + c.map(py).join(', '));
    return `    ${py(k)}: [\n${trozos.join(',\n')}\n    ],`;
  });
  return `${nombre} = pd.DataFrame({\n${lin.join('\n')}\n})`;
}
/* cohorte cardiovascular sintética, parecida a la de los cuadernos */
function cohorteJS(r, n) {
  const c = {edad: [], sexo: [], imc: [], pas: [], diabetes: [], fumador: [], hdl: [], ldl: [], hba1c: [], evento: []};
  for (let i = 0; i < n; i++) {
    const edad = Math.round(clamp(gauss(r, 62, 12), 40, 88)), mujer = r.bool(.5), imc = red(clamp(gauss(r, 27.5, 4.4), 18, 45), 1);
    const dm = r.bool(clamp(0.05 + (edad - 40) * 0.004 + (imc - 25) * 0.01, 0.03, 0.6)), fum = r.bool(mujer ? 0.18 : 0.28);
    const pas = Math.round(112 + 0.55 * (edad - 40) + 0.9 * (imc - 25) + 4 * dm + gauss(r, 0, 13));
    const hdl = Math.round(clamp(gauss(r, mujer ? 58 : 49, mujer ? 12 : 10), 22, 110)), ldl = Math.round(clamp(gauss(r, 128, 32), 50, 260));
    const hba1c = red(dm ? clamp(gauss(r, 7.4, 1.1), 5.8, 12) : clamp(gauss(r, 5.5, 0.45), 4.3, 6.4), 1);
    const lg = -7.2 + 0.07 * edad + 0.6 * fum + 0.7 * dm + 0.018 * (pas - 120) - 0.02 * (hdl - 50) + 0.4 * !mujer;
    c.edad.push(edad); c.sexo.push(mujer ? 'Mujer' : 'Hombre'); c.imc.push(imc); c.pas.push(pas); c.diabetes.push(dm ? 1 : 0); c.fumador.push(fum ? 1 : 0);
    c.hdl.push(hdl); c.ldl.push(ldl); c.hba1c.push(hba1c); c.evento.push(r.bool(1 / (1 + Math.exp(-lg))) ? 1 : 0);
  }
  return c;
}
const sel = (c, campos) => Object.fromEntries(campos.map(k => [k, c[k]]));
const PK_PD = ['numpy', 'pandas'], PK_SC = ['numpy', 'scipy'], PK_PDSC = ['numpy', 'pandas', 'scipy'], PK_NP = ['numpy'], PK_MPL = ['numpy', 'matplotlib'];
const NOMBRES = ['Ana López', 'Luis Martín', 'Marta Gil', 'Pedro Ruiz', 'Lucía Soler', 'Jorge Vidal', 'Carmen Ortega', 'Raúl Peña', 'Elena Cano', 'Hugo Prieto'];
