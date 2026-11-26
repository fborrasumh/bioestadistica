// Genera, para cada misión y semilla, las especificaciones que la app enviaría al arnés de Python:
// la solución de referencia (debe aprobar) y cada error típico (debe suspender).
// Uso: node specs.js ../../index.html 20 > /tmp/specs.json
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const N = +(process.argv[3] || 10);
const js = html.slice(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
const trozo = (a, b) => js.slice(js.indexOf(a), js.indexOf(b));
const codigo = [
  "const esc = s => String(s ?? '').replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));",
  'const chunk = (a, n) => { const o = []; for (let i = 0; i < a.length; i += n) o.push(a.slice(i, i + n)); return o; };',
  'let S = {prog: {}};',
  trozo('const L = (es, en, pt)', '/* ══ runner.js'),
  'module.exports = {MIS, instancia, buildSpec, semillaDe};'
].join('\n');
fs.writeFileSync('/tmp/_mis.js', codigo);
const {MIS, instancia, buildSpec, semillaDe} = require('/tmp/_mis.js');
const harness = trozo('const PY_HARNESS = String.raw`', '`;\n\nconst PY_WORKER_SRC').replace('const PY_HARNESS = String.raw`', '');
const casos = [];
for (const m of MIS) {
  for (let s = 0; s < N; s++) {
    const inst = instancia(m, semillaDe('prueba' + s, m.id, 0));
    if (m.k === 'code') {
      casos.push({id: m.id, s, tipo: 'sol', pk: m.pk || [], spec: buildSpec(m, inst, m.sol)});
      for (const mu of m.mut || []) casos.push({id: m.id, s, tipo: 'mut', mut: mu.id, pk: m.pk || [], spec: buildSpec(m, inst, mu.code)});
      if (inst.starter && s === 0) casos.push({id: m.id, s, tipo: 'starter', pk: m.pk || [], spec: buildSpec(m, inst, inst.starter)});
    } else if (m.k === 'predict') {
      const code = m.predict(inst.p);
      casos.push({id: m.id, s, tipo: 'ref', pk: m.pk || [], spec: {mode: 'ref', sol: code, data: '', out: []}});
      for (const mu of m.mut || []) casos.push({id: m.id, s, tipo: 'alt', mut: mu.id, alt: mu.alt(inst.p), pk: [], spec: {mode: 'predict', code, answer: mu.alt(inst.p)}});
    }
  }
}
const resumen = {misiones: MIS.length, porTipo: {}, porTema: {}};
for (const m of MIS) { resumen.porTipo[m.k] = (resumen.porTipo[m.k] || 0) + 1; resumen.porTema[m.tema] = (resumen.porTema[m.tema] || 0) + 1; }
process.stdout.write(JSON.stringify({harness, casos, resumen, quiz: MIS.filter(m => m.k === 'quiz').map(m => ({id: m.id, n: m.quiz.length, malas: m.quiz.filter(q => q.o.length !== 4 || q.ok !== 0).length}))}));
