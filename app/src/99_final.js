/* ══ final.js — refuerzos, ejemplo de la portada y registro del primer intento ══ */
/* refuerzo tras dos fallos: el reto remite a la clínica del tema, la clínica a la básica, y la básica a la clínica del tema anterior */
function refuerzos() {
  const o = {};
  for (const m of MIS) {
    const [tema, n] = [m.tema, +m.id.split('-')[1]];
    const destino = n > 1 ? `m${tema}-${n - 1}` : `m${tema - 10}-2`;
    if (misionPorId(destino)) o[m.id] = destino;
  }
  return o;
}
/* el ejemplo de la portada abre una misión con un fallo típico a propósito */
const EJEMPLO = {id: 'm10-2', code: 'imc = round(peso / (talla_cm / 100) * 2, 1)\npam = round((pas + 2 * pad) / 3, 1)\nsc = round((talla_cm * peso / 3600) ** 0.5, 2)\nobesidad = imc >= 30\n'};
/* primer intento: la primera vez que se comprueba una misión, ¿se resuelve sin pistas, sin IA y sin ver el resultado? */
function marcaPrimero(p, ok) { if (p.prim === undefined && !p.k) p.prim = !!ok && !p.pistas && !p.ia && !p.vista; }
/* nombre de los informes: 1964_apellidos_nombre_AAAAMMDD-HHMM.ext (minúsculas, sin tildes, con guiones bajos) */
function partesAlumno() {
  if (S.apellidos !== undefined || S.nombre !== undefined) return {ape: S.apellidos || '', nom: S.nombre || ''};
  const [a, n] = String(S.alumno || '').split(',').map(x => x.trim());
  return n !== undefined ? {ape: a, nom: n} : {ape: '', nom: ''};
}
function nombreInforme(ext) {
  const {ape, nom} = partesAlumno(), d = new Date(), p = n => String(n).padStart(2, '0');
  return `1964_${slug(ape)}_${slug(nom)}_${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}.${ext}`;
}
function exigeNombre() {
  const {ape, nom} = partesAlumno();
  if (ape.trim() && nom.trim()) return true;
  toast(t('Escribe tus apellidos y tu nombre antes de descargar el informe'));
  const c = document.getElementById(ape.trim() ? 'inNom' : 'inApe'); if (c) c.focus();
  return false;
}
