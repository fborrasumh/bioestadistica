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
