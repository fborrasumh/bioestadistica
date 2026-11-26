/* ══ lotes.js — corrección por lotes de los informes JSON (panel del profesorado).
   EC propuesta = misiones completadas válidas / total de misiones × 10. La confirma el profesorado. ══ */
const LT = {filas: [], trabajando: false, parar: false};
const MIN_COPIA = 8;   // misiones con código idéntico (no trivial) compartidas por dos estudiantes para avisar

/* lector mínimo de ZIP (sin librerías): ficheros guardados o comprimidos con deflate */
async function leeZip(buf) {
  const d = new DataView(buf), u8 = new Uint8Array(buf), dec = new TextDecoder();
  let fin = -1;
  for (let i = buf.byteLength - 22; i >= Math.max(0, buf.byteLength - 66000); i--) if (d.getUint32(i, true) === 0x06054b50) { fin = i; break; }
  if (fin < 0) throw new Error('zip');
  const total = d.getUint16(fin + 10, true); let off = d.getUint32(fin + 16, true); const out = [];
  for (let k = 0; k < total; k++) {
    if (d.getUint32(off, true) !== 0x02014b50) break;
    const metodo = d.getUint16(off + 10, true), tam = d.getUint32(off + 20, true), nl = d.getUint16(off + 28, true), el = d.getUint16(off + 30, true), cl = d.getUint16(off + 32, true), loc = d.getUint32(off + 42, true);
    const nombre = dec.decode(u8.subarray(off + 46, off + 46 + nl)); off += 46 + nl + el + cl;
    if (!/\.json$/i.test(nombre) || /(^|\/)__MACOSX\//.test(nombre)) continue;
    const ini = loc + 30 + d.getUint16(loc + 26, true) + d.getUint16(loc + 28, true), datos = u8.subarray(ini, ini + tam);
    let texto;
    if (metodo === 0) texto = dec.decode(datos);
    else if (metodo === 8) {
      if (typeof DecompressionStream === 'undefined') throw new Error('deflate');
      texto = await new Response(new Blob([datos]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).text();
    } else continue;
    out.push({nombre: nombre.split('/').pop(), texto});
  }
  return out;
}

const normCodigo = s => String(s || '').split('\n').map(l => l.replace(/#.*$/, '').trim()).filter(Boolean).join('\n');
async function analizaInforme(j, fichero) {
  const f = {fichero, alumno: String(j.alumno || '').trim(), sem: j.sem || '', creado: j.creado || '', v: j.v || '', j,
    rota: await verificaCadena(j.cadena || []), eventos: (j.cadena || []).length,
    validas: 0, completadas: 0, porMod: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, prim: 0, intentadas: 0, quizOk: 0, codigos: {}, alertas: [], rec: null};
  /* el progreso no está dentro de la cadena: se contrasta con ella (evento «ok» y huella del código que aprobó) */
  const okIds = new Set(), hcs = {}, sinRegistro = [], otroCodigo = [];
  for (const e of j.cadena || []) { if (e.tipo === 'ok') okIds.add(e.id); if (e.tipo === 'intento' && e.ok && e.hc) (hcs[e.id] = hcs[e.id] || new Set()).add(e.hc); }
  for (const m of MIS) {
    const p = j.prog?.[m.id]; if (!p) continue;
    if (p.prim !== undefined) { f.intentadas++; if (p.prim) f.prim++; }
    if (!p.done) continue;
    f.completadas++;
    let ok;
    if (m.k === 'quiz') { ok = Array.isArray(p.respOk) && p.respOk.length === m.quiz.length && m.quiz.every((q, i) => p.respOk[i] === q.ok); if (ok) f.quizOk++; }
    else if (m.k === 'predict') ok = typeof p.resp === 'string' && p.resp.trim() !== '';
    else { ok = typeof p.codeOk === 'string' && p.codeOk.trim() !== ''; const c = normCodigo(p.codeOk); if (c.length >= 60) f.codigos[m.id] = await sha256(c); }
    if (ok && !okIds.has(m.id)) { ok = false; sinRegistro.push(m.id); }
    if (ok && m.k !== 'quiz' && !(hcs[m.id] && hcs[m.id].has((await sha256(m.k === 'predict' ? p.resp : p.codeOk)).slice(0, 16)))) { ok = false; otroCodigo.push(m.id); }
    if (ok) { f.validas++; f.porMod[temaDe(m).u]++; }
  }
  if (sinRegistro.length) f.alertas.push(t('{0} misiones completadas sin registro en la cadena: {1}', sinRegistro.length, sinRegistro.join(', ')));
  if (otroCodigo.length) f.alertas.push(t('{0} misiones cuyo código no es el que aprobó: {1}', otroCodigo.length, otroCodigo.join(', ')));
  f.ec = Math.round(1000 * f.validas / MIS.length) / 100;
  if (f.rota) f.alertas.push(t('Registro roto en el evento {0}: el fichero pudo editarse', f.rota));
  if (!f.alumno) f.alertas.push(t('Sin nombre de alumno'));
  const sinResp = f.completadas - f.validas - sinRegistro.length - otroCodigo.length;
  if (sinResp > 0) f.alertas.push(t('{0} misiones marcadas como completadas sin respuesta válida', sinResp));
  return f;
}

function alertasCruzadas(filas) {
  const porNombre = {};
  for (const f of filas) { const k = norm(f.alumno); if (k) (porNombre[k] = porNombre[k] || []).push(f); }
  for (const grupo of Object.values(porNombre)) if (grupo.length > 1) {
    grupo.sort((a, b) => String(b.creado).localeCompare(String(a.creado)));
    grupo.slice(1).forEach(f => { f.sustituido = true; f.alertas.push(t('Hay un informe más reciente de este alumno')); });
  }
  const vigentes = filas.filter(f => !f.sustituido), porSem = {};
  for (const f of vigentes) if (f.sem) (porSem[f.sem] = porSem[f.sem] || []).push(f);
  for (const g of Object.values(porSem)) if (g.length > 1) g.forEach(f => f.alertas.push(t('Misma semilla que: {0}', g.filter(x => x !== f).map(x => x.alumno || x.fichero).join(', '))));
  const porCodigo = {};
  for (const f of vigentes) for (const [id, h] of Object.entries(f.codigos)) (porCodigo[id + h] = porCodigo[id + h] || []).push(f);
  const pares = new Map();
  for (const g of Object.values(porCodigo)) {
    if (g.length < 2 || g.length > 4) continue;   // si muchos coinciden, es la solución natural
    for (let a = 0; a < g.length; a++) for (let b = a + 1; b < g.length; b++) { const k = [g[a], g[b]]; const c = pares.get(k[0]) || new Map(); c.set(k[1], (c.get(k[1]) || 0) + 1); pares.set(k[0], c); }
  }
  for (const [fa, m] of pares) for (const [fb, n] of m) if (n >= MIN_COPIA) {
    fa.alertas.push(t('Código idéntico a {0} en {1} misiones', fb.alumno || fb.fichero, n));
    fb.alertas.push(t('Código idéntico a {0} en {1} misiones', fa.alumno || fa.fichero, n));
  }
}

async function cargaLote(files) {
  const est = $('loteEstado'); LT.filas = []; let malos = 0;
  est.innerHTML = `<span class="spin"></span> ${esc(t('Leyendo…'))}`;
  const docs = [];
  for (const f of files) {
    if (/\.zip$/i.test(f.name)) {
      try { docs.push(...await leeZip(await f.arrayBuffer())); }
      catch (e) { toast(e.message === 'deflate' ? t('Este navegador no descomprime ZIP: descomprímelo y carga los JSON') : t('No se pudo leer el ZIP {0}', f.name)); }
    } else docs.push({nombre: f.name, texto: await f.text()});
  }
  for (const d of docs) {
    let j; try { j = JSON.parse(d.texto); } catch { malos++; continue; }
    if (j.fmt !== FMT) { malos++; continue; }
    LT.filas.push(await analizaInforme(j, d.nombre));
  }
  alertasCruzadas(LT.filas);
  LT.filas.sort((a, b) => norm(a.alumno || a.fichero).localeCompare(norm(b.alumno || b.fichero)));
  est.textContent = t('{0} informes leídos.', LT.filas.length) + (malos ? ' ' + t('{0} ficheros ignorados (no son informes de esta app).', malos) : '');
  pintaLoteTabla();
}

/* recálculo completo: vuelve a ejecutar el código de cada misión con la semilla del alumno */
async function recalculaFila(f) {
  let ok = 0, n = 0; f.fallan = [];
  for (const m of MIS) {
    const p = f.j.prog?.[m.id]; if (!p?.done || m.k === 'quiz') continue;
    n++;
    const inst = instancia(m, semillaDe(p.semOk ?? f.j.sem, m.id, p.kOk ?? p.k));
    const res = await pyRun(buildSpec(m, inst, m.k === 'predict' ? (p.resp || '') : (p.codeOk || '')), m.pk || [], 15000);
    if (res.fatal) throw new Error('py');
    if (res.ok) ok++; else f.fallan.push(m.id);
  }
  f.rec = {ok, n};
  f.ecRec = Math.round(1000 * (f.quizOk + ok) / MIS.length) / 100;
  if (f.fallan.length) f.alertas.push(t('{0} misiones no se recalculan: {1}', f.fallan.length, f.fallan.join(', ')));
}
async function recalculaLote(soloAlertas) {
  if (LT.trabajando) { LT.parar = true; return; }
  const filas = LT.filas.filter(f => !f.sustituido && !f.rec && (!soloAlertas || f.alertas.length));
  if (!filas.length) return toast(t('No hay informes pendientes de recalcular'));
  LT.trabajando = true; LT.parar = false; pintaLoteBotones();
  const est = $('loteEstado'), t0 = Date.now();
  try {
    for (let i = 0; i < filas.length && !LT.parar; i++) {
      const resto = i ? Math.round((Date.now() - t0) / i * (filas.length - i) / 60000) : null;
      est.innerHTML = `<span class="spin"></span> ${esc(t('Recalculando {0} de {1}: {2}', i + 1, filas.length, filas[i].alumno || filas[i].fichero))}${resto !== null ? ' · ' + esc(t('quedan unos {0} min', resto)) : ''}`;
      await recalculaFila(filas[i]); pintaLoteTabla();
    }
    est.textContent = LT.parar ? t('Recálculo detenido.') : t('Recálculo terminado.');
  } catch { est.textContent = t('No se pudo ejecutar Python para verificar. Comprueba la conexión.'); }
  LT.trabajando = false; LT.parar = false; pintaLoteBotones();
}

const filaCsv = f => [f.alumno, f.fichero, f.creado.slice(0, 16).replace('T', ' '), f.sem, f.rota ? t('roto') : t('íntegro'), f.completadas, f.validas,
  f.porMod[1], f.porMod[2], f.porMod[3], f.porMod[4], f.porMod[5], f.intentadas ? Math.round(100 * f.prim / f.intentadas) : '',
  f.ec.toFixed(2).replace('.', ','), f.rec ? `${f.rec.ok}/${f.rec.n}` : '', f.rec ? f.ecRec.toFixed(2).replace('.', ',') : '', f.sustituido ? t('sí') : '', f.alertas.join(' | ')];
function exportaLote() {
  if (!LT.filas.length) return toast(t('Carga primero los informes'));
  dl(`1964_EC_${HOY()}.csv`, csvDe([t('alumno'), t('fichero'), t('fecha_informe'), t('semilla'), t('registro'), t('completadas'), t('validas'), 'M1', 'M2', 'M3', 'M4', 'M5',
    t('pct_primer_intento'), t('EC_propuesta'), t('recalculo'), t('EC_tras_recalculo'), t('sustituido'), t('alertas')], LT.filas.map(filaCsv)), 'text/csv;charset=utf-8');
}

function pintaLoteBotones() {
  if (!$('loteRec')) return;
  $('loteRec').textContent = LT.trabajando ? t('Detener') : t('Recalcular todos');
  $('loteRecA').disabled = LT.trabajando;
}
function pintaLoteTabla() {
  const caja = $('loteRes'); if (!caja) return;
  if (!LT.filas.length) { caja.innerHTML = ''; return; }
  const vig = LT.filas.filter(f => !f.sustituido), conAl = vig.filter(f => f.alertas.length).length;
  const media = vig.length ? (vig.reduce((a, f) => a + f.ec, 0) / vig.length).toFixed(2) : '—';
  caja.innerHTML = `<p style="margin:12px 0 6px"><b>${esc(t('{0} estudiantes', vig.length))}</b> · ${esc(t('EC propuesta media: {0}', media.replace('.', ',')))} · ${esc(t('{0} con alertas', conAl))}</p>
  <div class="pm-tbl"><table><thead><tr><th>${esc(t('Alumno/a'))}</th><th>${esc(t('Registro'))}</th><th>${esc(t('Completadas'))}</th><th>M1</th><th>M2</th><th>M3</th><th>M4</th><th>M5</th><th>${esc(t('1.er intento'))}</th><th>${esc(t('EC propuesta'))}</th><th>${esc(t('Recálculo'))}</th><th>${esc(t('Alertas'))}</th></tr></thead><tbody>${
    LT.filas.map(f => `<tr${f.sustituido ? ' style="opacity:.5"' : ''}><td>${esc(f.alumno || '—')}<br><span class="help">${esc(f.fichero)}</span></td><td>${f.rota ? '✗' : '✓'}</td><td>${f.validas} / ${MIS.length}</td>${[1, 2, 3, 4, 5].map(k => `<td>${f.porMod[k]}</td>`).join('')}<td>${f.intentadas ? Math.round(100 * f.prim / f.intentadas) + ' %' : '—'}</td><td><b>${f.ec.toFixed(2).replace('.', ',')}</b>${f.rec ? `<br><span class="help">${esc(t('tras recálculo'))}: ${f.ecRec.toFixed(2).replace('.', ',')}</span>` : ''}</td><td>${f.rec ? `${f.rec.ok}/${f.rec.n}` : '—'}</td><td>${f.alertas.map(a => `<div class="help" style="color:#B42318">${esc(a)}</div>`).join('')}</td></tr>`).join('')
  }</tbody></table></div>`;
}
function pintaLote() {
  $('profLote').innerHTML = `<h3>${esc(t('Corregir la evaluación continua de toda la clase'))}</h3>
  <p class="help">${esc(t('Carga a la vez todos los informes JSON, o el ZIP descargado de la tarea del Campus Virtual. Todo se procesa en este navegador; no se envía nada.'))}</p>
  <p class="help">${esc(t('EC propuesta = misiones completadas válidas / {0} × 10 (con respuesta correcta, registradas en la cadena y con el mismo código que aprobó). Es una propuesta: la nota la decides tú.', MIS.length))}</p>
  <div class="actions" style="margin-top:0"><input type="file" id="loteFile" accept=".json,.zip,application/json,application/zip" multiple></div>
  <div class="actions"><button class="btn btn-ghost" id="loteRecA" type="button">${esc(t('Recalcular los que tienen alertas'))}</button><button class="btn btn-ghost" id="loteRec" type="button">${esc(t('Recalcular todos'))}</button><button class="btn btn-primary" id="loteCsv" type="button"><svg class="i"><use href="#i-download"/></svg>${esc(t('Descargar tabla (CSV)'))}</button></div>
  <p class="help">${esc(t('El recálculo vuelve a ejecutar el código de cada misión con la semilla del alumno. Es lento (varios segundos por alumno); puedes detenerlo y seguir después.'))}</p>
  <p class="help" id="loteEstado" aria-live="polite"></p><div id="loteRes"></div>`;
  $('loteFile').onchange = e => { if (e.target.files.length) cargaLote([...e.target.files]); };
  $('loteRec').onclick = () => recalculaLote(false); $('loteRecA').onclick = () => recalculaLote(true); $('loteCsv').onclick = exportaLote;
  pintaLoteBotones(); pintaLoteTabla();
}
