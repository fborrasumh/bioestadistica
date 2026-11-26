import asyncio, json, zipfile, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1300,'height':1000})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(600)
        informes = await pg.evaluate("""async () => {
          const hacer = async (alumno, sem, nq, nc, codigo, creado) => {
            S.prog = {}; S.cadena = []; S.alumno = alumno; S.sem = sem;
            const qs = MIS.filter(m => m.k === 'quiz').slice(0, nq), cs = MIS.filter(m => m.k === 'code').slice(0, nc);
            for (const m of qs) { const pp = P(m.id); pp.intentos = 1; pp.prim = true; await addEv({tipo: 'intento', id: m.id, k: 0, ok: true, bien: 4}); await completa(m, undefined, {respOk: m.quiz.map(q => q.ok)}); await addEv({tipo: 'ok', id: m.id, k: 0, est: 3}); }
            for (const m of cs) { const pp = P(m.id); pp.intentos = 2; pp.prim = false; await addEv({tipo: 'intento', id: m.id, k: 0, ok: true, hc: (await sha256(codigo(m))).slice(0, 16)}); await completa(m, codigo(m)); await addEv({tipo: 'ok', id: m.id, k: 0, est: 2}); }
            const j = JSON.parse(JSON.stringify(informeJSON())); j.creado = creado; return j;
          };
          const A = await hacer('García López, Ana', 's-ana', 20, 15, m => m.sol, '2027-12-10T10:00:00Z');
          const A0 = await hacer('García López, Ana', 's-ana', 5, 0, m => m.sol, '2027-11-01T10:00:00Z');
          const B = await hacer('Pérez Ruiz, Luis', 's-luis', 10, 15, m => m.sol, '2027-12-11T10:00:00Z');
          const C = await hacer('Soler Gil, Marta', 's-ana', 23, 0, m => m.sol, '2027-12-11T11:00:00Z');
          const D = await hacer('Vidal Cano, Jorge', 's-jorge', 12, 3, m => m.sol + '\\nx_extra = 1', '2027-12-12T09:00:00Z');
          D.cadena[2].m = 'm999-1';
          const E = await hacer('Ortega Prieto, Elena', 's-elena', 23, 5, m => m.sol + '\\nfin = 0', '2027-12-12T09:30:00Z');
          E.prog['m40-2'] = {done: true, stars: 3, codeOk: 'x = 1'}; E.prog[MIS.filter(m => m.k === 'code')[0].id].codeOk = 'imc = 0';
          return {A, A0, B, C, D, E};
        }""")
        os.makedirs('/tmp/lote_bio', exist_ok=True)
        for k,v in informes.items(): json.dump(v, open(f'/tmp/lote_bio/{k}.json','w'))
        with zipfile.ZipFile('/tmp/lote_bio/entregas.zip','w',zipfile.ZIP_DEFLATED) as z:
            for k in informes: z.write(f'/tmp/lote_bio/{k}.json', f'Entrega_{k}/bioestadistica_{k}.json')
            z.writestr('__MACOSX/Entrega_A/._x.json','basura'); z.writestr('leeme.txt','hola')
        await pg.evaluate("go(4)"); await pg.wait_for_timeout(300)
        await pg.set_input_files('#loteFile', '/tmp/lote_bio/entregas.zip'); await pg.wait_for_timeout(2500)
        estado = await pg.inner_text('#loteEstado'); tabla = await pg.inner_text('#loteRes')
        await pg.locator('#profLote').screenshot(path='/tmp/lote_bio.png')
        csv = await pg.evaluate("""() => { let out=''; const o=window.dl; window.dl=(n,c)=>{out=n+'\\n'+c}; exportaLote(); window.dl=o; return out; }""")
        print(json.dumps({'errores':errs,'estado':estado,'csv':csv.splitlines()}, ensure_ascii=False, indent=1)); print(tabla[:1500])
        await b.close()
asyncio.run(main())
