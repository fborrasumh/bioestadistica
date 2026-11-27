"""Vídeos locutados por tema: diapositivas 1920×1080 a partir del guion y montaje con ffmpeg.

Aquí se dibujan las diapositivas (python3 video.py diapos 150) y se ensaya el montaje con
audio de relleno (python3 video.py ensayo 150). La voz real se genera en Colab
(videos/fabrica_videos.ipynb), que usa monta() de este mismo fichero.
"""
import json
import os
import re
import subprocess
import sys
import wave

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GUIONES = os.path.join(RAIZ, "videos", "guiones")
DIAPOS = os.path.join(RAIZ, "videos", "diapos")
FIGURAS = os.path.join(RAIZ, "figuras")
APP = "fborrasumh.github.io/bioestadistica"
W, H, FPS, PAUSA = 1920, 1080, 30, 0.6

NAVY, NARANJA, FONDO, TINTA, SUAVE = "#0F2237", "#E4572E", "#F4F6FA", "#0F2237", "#5D7691"


def guion(tema):
    return json.load(open(os.path.join(GUIONES, f"tema_{tema:03d}.json"), encoding="utf-8"))


# ── diapositivas ──────────────────────────────────────────────────────────
def _fuente(peso, tam):
    from PIL import ImageFont
    return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/Inter-{peso}.otf", tam)


def _parrafo(d, texto, x, y, ancho, fuente, color, interlinea=1.25):
    """Escribe texto ajustado a un ancho; devuelve la y final."""
    lineas, actual = [], ""
    for p in texto.split():
        prueba = (actual + " " + p).strip()
        if d.textlength(prueba, font=fuente) <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
    lineas.append(actual)
    alto = int(fuente.size * interlinea)
    for l in lineas:
        d.text((x, y), l, font=fuente, fill=color)
        y += alto
    return y


def _figura_de_codigo(tema, nombre, ancla):
    """Ejecuta el código de la diapositiva del cuaderno y guarda la figura."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from diapositivas import DIAPOS as D
    codigo = next(x["codigo"] for x in D[tema] if x["ancla"].startswith(ancla))
    ruta = os.path.join(DIAPOS, nombre)
    plt.rcParams.update({"font.size": 15})
    exec(codigo.replace("plt.show()", f"plt.savefig({ruta!r}, dpi=150, bbox_inches='tight'); plt.close('all')"), {})
    return ruta


def dibuja(tema):
    from PIL import Image, ImageDraw
    g = guion(tema)
    os.makedirs(DIAPOS, exist_ok=True)
    rutas = []
    for i, e in enumerate(g["escenas"], 1):
        tipo = e.get("tipo", "normal")
        img = Image.new("RGB", (W, H), NAVY if tipo == "portada" else FONDO)
        d = ImageDraw.Draw(img)
        if tipo == "portada":
            d.text((140, 150), f"BIOESTADÍSTICA (1964) · TEMA {tema}", font=_fuente("SemiBold", 34), fill="#9FB0C3")
            y = _parrafo(d, e["titulo"], 140, 250, 1640, _fuente("ExtraBold", 110), "#FFFFFF", 1.1)
            d.rectangle((140, y + 30, 340, y + 42), fill=NARANJA)
            y = _parrafo(d, e["subtitulo"], 140, y + 90, 1500, _fuente("Regular", 46), "#D5DEE8")
            d.text((140, 880), "Fernando Borrás Rocher · Universidad Miguel Hernández de Elche", font=_fuente("SemiBold", 34), fill="#FFFFFF")
            d.text((140, 935), "Voz generada con inteligencia artificial · CC BY 4.0", font=_fuente("Regular", 30), fill="#9FB0C3")
        else:
            d.rectangle((0, 0, W, 96), fill=NAVY)
            d.text((80, 26), "Bio", font=_fuente("ExtraBold", 38), fill="#FFFFFF")
            d.text((80 + d.textlength("Bio", font=_fuente("ExtraBold", 38)), 26), "estadística", font=_fuente("ExtraBold", 38), fill=NARANJA)
            d.text((W - 80, 34), f"Tema {tema}", font=_fuente("SemiBold", 30), fill="#D5DEE8", anchor="ra")
            d.rectangle((80, 150, 92, 230), fill=NARANJA)
            fig, f = e.get("fig"), None
            if fig:
                ruta = os.path.join(FIGURAS, fig)
                if not os.path.exists(ruta):
                    ruta = _figura_de_codigo(tema, fig, e["codigo_de"])
                f = Image.open(ruta).convert("RGB")
            abajo = f is not None and f.width / f.height > 1.7      # figura apaisada: debajo del texto
            lado = f is not None and not abajo
            ancho_txt = 700 if lado else 1600
            y = _parrafo(d, e["titulo"], 120, 148, (720 if lado else 1680), _fuente("Bold", 62 if lado else 68), TINTA, 1.15) + 40
            fb = _fuente("Regular", 44 if f else 54)
            y_ideas = y
            for idea in e.get("ideas", []):
                d.ellipse((124, y + 18, 140, y + 34), fill=NARANJA)
                y = _parrafo(d, idea, 170, y, ancho_txt - 50, fb, TINTA, 1.3) + 26
            if e.get("pregunta"):
                fq = _fuente("SemiBold", 40)
                if abajo:                                       # a la derecha de las viñetas
                    qx, qy, qw = 1080, y_ideas, 720
                else:
                    qx, qy, qw = 120, y, ancho_txt
                fin = _parrafo(d, e["pregunta"], qx + 30, -1000, qw - 60, fq, "#B23A15", 1.3) + 1000
                d.rounded_rectangle((qx, qy, qx + qw, qy + fin + 44), 18, fill="#FDECE6")
                _parrafo(d, e["pregunta"], qx + 30, qy + 22, qw - 60, fq, "#B23A15", 1.3)
                if not abajo:
                    y = qy + fin + 70
            if tipo == "cierre":
                d.text((170, 900), f"{APP}/#tema-{tema}", font=_fuente("Bold", 44), fill=NARANJA)
            if f is not None:
                if abajo:
                    cx, cy, caja_w, caja_h = 120, y + 30, 1680, 1000 - (y + 30)
                else:
                    cx, cy, caja_w, caja_h = 880, 150, 960, 840
                esc = min(caja_w / f.width, caja_h / f.height)
                f = f.resize((int(f.width * esc), int(f.height * esc)), Image.LANCZOS)
                x0, y0 = cx + (caja_w - f.width) // 2, cy + (caja_h - f.height) // 2
                d.rounded_rectangle((x0 - 20, y0 - 20, x0 + f.width + 20, y0 + f.height + 20), 20, fill="#FFFFFF", outline="#D9E2EC", width=2)
                img.paste(f, (x0, y0))
            d.text((W - 80, H - 50), "Voz generada con IA · CC BY 4.0", font=_fuente("Regular", 24), fill=SUAVE, anchor="ra")
        ruta = os.path.join(DIAPOS, f"tema_{tema:03d}_{i:02d}.png")
        img.save(ruta, optimize=True)
        rutas.append(ruta)
    return rutas


# ── montaje ───────────────────────────────────────────────────────────────
def _ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def _duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)


def _trozos(texto, maximo=80, minimo=25):
    """Frases cortadas en trozos legibles: hasta `maximo` caracteres, cortando en comas y dos puntos."""
    trozos = []
    for frase in re.split(r"(?<=[.?!])\s+", texto.strip()):
        actual = ""
        for parte in re.split(r"(?<=[,:;])\s+", frase):
            if actual and len(actual) + 1 + len(parte) > maximo:
                trozos.append(actual)
                actual = parte
            else:
                actual = (actual + " " + parte).strip()
        trozos.append(actual)
    unidos = []                                   # un trozo muy corto se une al siguiente
    for t in trozos:
        if unidos and len(unidos[-1]) < minimo:
            unidos[-1] += " " + t
        else:
            unidos.append(t)
    final = []                                    # lo que aún es largo se parte por palabras en mitades
    pendientes = unidos[::-1]
    while pendientes:
        t = pendientes.pop()
        if len(t) <= maximo:
            final.append(t)
            continue
        pal = t.split()
        corte = min(range(1, len(pal)), key=lambda k: abs(len(" ".join(pal[:k])) - len(t) / 2))
        pendientes += [" ".join(pal[corte:]), " ".join(pal[:corte])]
    return final


def _srt(escenas, duraciones):
    """Subtítulos por frase; dentro de cada escena, el tiempo se reparte según la longitud."""
    def hms(t):
        ms = int(round(t * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    out, n, t0 = [], 1, 0.0
    for e, dur in zip(escenas, duraciones):
        frases = _trozos(e["texto"])
        hablado = dur - PAUSA
        total = sum(len(f) for f in frases)
        t = t0
        for f in frases:
            dt = hablado * len(f) / total
            out.append(f"{n}\n{hms(t)} --> {hms(t + dt)}\n{f}\n")
            n, t = n + 1, t + dt
        t0 += dur
    return "\n".join(out)


def monta(tema, audios, salida, tmp="/tmp/video_tmp"):
    """audios: un fichero de voz por escena (cualquier formato que lea ffmpeg). Crea salida.mp4 y salida.srt."""
    g = guion(tema)
    os.makedirs(tmp, exist_ok=True)
    escenas_v, escenas_a, duraciones = [], [], []
    for i, a in enumerate(audios, 1):
        dur = round((_duracion(a) + PAUSA) * FPS) / FPS          # duración exacta en fotogramas
        png = os.path.join(DIAPOS, f"tema_{tema:03d}_{i:02d}.png")
        v, wv = os.path.join(tmp, f"v{i:02d}.mp4"), os.path.join(tmp, f"a{i:02d}.wav")
        _ff("-framerate", str(FPS), "-i", png, "-vf", f"format=yuv420p,loop=-1:1,trim=duration={dur}",
            "-r", str(FPS), "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-tune", "stillimage",
            "-pix_fmt", "yuv420p", v + ".tmp.mp4")
        os.replace(v + ".tmp.mp4", v)
        _ff("-i", a, "-af", f"aresample=48000,apad=whole_dur={dur}", "-t", str(dur), "-ac", "1", wv)
        escenas_v.append(v); escenas_a.append(wv); duraciones.append(dur)
    lista = os.path.join(tmp, "lista.txt")
    open(lista, "w").write("".join(f"file '{v}'\n" for v in escenas_v))
    voz = os.path.join(tmp, "voz.wav")
    lista_a = os.path.join(tmp, "lista_a.txt")
    open(lista_a, "w").write("".join(f"file '{a}'\n" for a in escenas_a))
    _ff("-f", "concat", "-safe", "0", "-i", lista_a, "-c", "copy", voz)
    srt = salida.rsplit(".", 1)[0] + ".srt"
    open(srt, "w", encoding="utf-8").write(_srt(g["escenas"], duraciones))
    _ff("-f", "concat", "-safe", "0", "-i", lista, "-i", voz, "-i", srt,
        "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=spa", "-movflags", "+faststart", salida + ".tmp.mp4")
    os.replace(salida + ".tmp.mp4", salida)
    return salida, srt


INSTRUCCIONES = ("Habla en español de España, como un profesor universitario cercano y claro que explica a "
                 "estudiantes de Medicina. Ritmo pausado, entonación natural, pequeñas pausas tras cada idea.")


def locuta(tema, cliente, carpeta_audio, voz="coral", instrucciones=INSTRUCCIONES):
    """Voz de cada escena con OpenAI. Reutiliza el audio ya generado si el texto, la voz y las instrucciones no cambian."""
    import hashlib
    os.makedirs(carpeta_audio, exist_ok=True)
    audios = []
    for i, e in enumerate(guion(tema)["escenas"], 1):
        huella = hashlib.sha256((voz + instrucciones + e["texto"]).encode()).hexdigest()[:10]
        ruta = os.path.join(carpeta_audio, f"tema_{tema:03d}_{i:02d}_{huella}.mp3")
        if not os.path.exists(ruta):
            with cliente.audio.speech.with_streaming_response.create(
                    model="gpt-4o-mini-tts", voice=voz, input=e["texto"], instructions=instrucciones,
                    response_format="mp3") as r:
                r.stream_to_file(ruta + ".tmp")
            os.replace(ruta + ".tmp", ruta)
            print(f"Tema {tema}, escena {i}: voz generada", flush=True)
        audios.append(ruta)
    return audios


def temas_con_guion():
    return sorted(int(f[5:8]) for f in os.listdir(GUIONES) if re.fullmatch(r"tema_\d{3}\.json", f))


def ensayo(tema):
    """Montaje con silencio de la duración estimada (2,6 palabras por segundo) en lugar de voz."""
    g = guion(tema)
    audios = []
    for i, e in enumerate(g["escenas"], 1):
        ruta = f"/tmp/video_tmp/relleno_{i:02d}.wav"
        os.makedirs("/tmp/video_tmp", exist_ok=True)
        n = int(48000 * len(e["texto"].split()) / 2.6)
        with wave.open(ruta, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b"\0\0" * n)
        audios.append(ruta)
    return monta(tema, audios, f"/tmp/ensayo_tema_{tema:03d}.mp4")


if __name__ == "__main__" and sys.argv[1] == "locutar":
    from openai import OpenAI
    pedidos, voz, salida = sys.argv[2], sys.argv[3], sys.argv[4]
    temas = temas_con_guion() if pedidos.strip() == "todos" else [int(t) for t in pedidos.replace(",", " ").split()]
    faltan = [t for t in temas if t not in temas_con_guion()]
    if faltan:
        sys.exit(f"Sin guion en videos/guiones: {faltan}")
    cliente = OpenAI()                                   # lee OPENAI_API_KEY del entorno
    os.makedirs(salida, exist_ok=True)
    for t in temas:
        mp4, _ = monta(t, locuta(t, cliente, os.path.join(salida, "..", "audio_cache"), voz), os.path.join(salida, f"Tema_{t:03d}.mp4"))
        print(f"Tema {t}: {mp4} ({_duracion(mp4):.0f} s)", flush=True)
elif __name__ == "__main__":
    accion, tema = sys.argv[1], int(sys.argv[2])
    if accion == "diapos":
        print("\n".join(dibuja(tema)))
    elif accion == "ensayo":
        print(ensayo(tema))
