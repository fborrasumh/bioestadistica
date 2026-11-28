"""Genera videos/fabrica_videos.ipynb: voz con OpenAI en Colab y montaje con scripts/video.py."""
import os
import nbformat as nbf

REPO = "fborrasumh/bioestadistica"
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

celdas = [
    nbf.v4.new_markdown_cell(f"""<a href="https://colab.research.google.com/github/{REPO}/blob/main/videos/fabrica_videos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Abrir en Colab"/></a>

# Fábrica de vídeos locutados · Bioestadística (1964)

**Autor:** Fernando Borrás Rocher · Universidad Miguel Hernández de Elche · ORCID [0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573) · CC BY 4.0

Convierte el guion de cada tema (`videos/guiones/`, los 31 temas, del 0 al 300) y sus diapositivas (`videos/diapos/`) en un vídeo MP4 de unos 3 minutos con voz y subtítulos, y lo guarda en tu Google Drive.

**Antes de empezar**

1. Guarda tu clave de OpenAI en **Secrets** (icono de la llave, a la izquierda) con el nombre `OPENAI_API_KEY` y activa el acceso para este cuaderno. Nunca la escribas en una celda.
2. En **Parámetros**, deja `todos` o escribe los temas separados por comas (por ejemplo `10, 150`).
3. **Entorno de ejecución → Ejecutar todo.** Colab pedirá permiso para usar tu Drive.

**A tener en cuenta**

- La voz la genera el modelo `gpt-4o-mini-tts` de OpenAI. OpenAI ha anunciado que **deja de funcionar el 6 de enero de 2027**: genera los vídeos antes de esa fecha.
- Las normas de OpenAI piden indicar que la voz está generada por IA; las diapositivas ya lo dicen, y conviene repetirlo al compartir el vídeo.
- El audio de cada escena se guarda en Drive. Si vuelves a ejecutar el cuaderno, solo se paga la voz de las escenas cuyo texto haya cambiado.
"""),
    nbf.v4.new_code_cell("""#@title Parámetros
TEMAS = "todos"  #@param {type:"string"}
VOZ = "coral"  #@param ["coral", "marin", "cedar", "ash", "sage", "verse", "ballad", "alloy", "echo", "shimmer"]
CARPETA = "Bioestadistica_videos"  #@param {type:"string"}
INSTRUCCIONES = "Habla en español de España, como un profesor universitario cercano y claro que explica a estudiantes de Medicina. Ritmo pausado, entonación natural, pequeñas pausas tras cada idea."  #@param {type:"string"}
"""),
    nbf.v4.new_code_cell(f"""#@title Preparar: Drive, repositorio y clave
import os, sys, subprocess
from google.colab import drive, userdata
drive.mount("/content/drive")
if os.path.isdir("/content/bioestadistica"):
    subprocess.run(["git", "-C", "/content/bioestadistica", "pull", "-q"], check=True)
else:
    subprocess.run(["git", "clone", "-q", "--depth", "1", "https://github.com/{REPO}.git", "/content/bioestadistica"], check=True)
sys.path.insert(0, "/content/bioestadistica/scripts")
import video
from openai import OpenAI
cliente = OpenAI(api_key=userdata.get("OPENAI_API_KEY"))
SALIDA = f"/content/drive/MyDrive/{{CARPETA}}"
os.makedirs(f"{{SALIDA}}/audio", exist_ok=True)
temas = video.temas_con_guion() if TEMAS.strip() == "todos" else [int(t) for t in TEMAS.replace(",", " ").split()]
print("Temas:", temas, "· voz:", VOZ, "· carpeta:", SALIDA)
"""),
    nbf.v4.new_code_cell("""#@title Generar los vídeos
from IPython.display import display, Audio
for tema in temas:
    audios = video.locuta(tema, cliente, f"{SALIDA}/audio", VOZ, INSTRUCCIONES)
    if tema == temas[0]:
        display(Audio(audios[0]))                 # muestra de la primera escena
    mp4, srt = video.monta(tema, audios, f"{SALIDA}/Tema_{tema:03d}.mp4")
    print(f"Tema {tema}: {mp4} ({video._duracion(mp4):.0f} s) y sus subtítulos {os.path.basename(srt)}")
"""),
    nbf.v4.new_markdown_cell("""## Compartir los vídeos

Cada tema deja en tu carpeta de Drive `Tema_NNN.mp4` y `Tema_NNN.srt`. El MP4 ya lleva los subtítulos dentro, pero el reproductor de Drive no los muestra: para verlos en Drive, abre el vídeo, menú **⋮ → Administrar pistas de subtítulos** y sube el `.srt`.

Para compartir: botón derecho sobre el vídeo → **Compartir** → «Cualquier persona de la UMH con el enlace».
"""),
]

nb = nbf.v4.new_notebook()
nb["cells"] = celdas
nb["metadata"] = {"colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"}}
os.makedirs(os.path.join(RAIZ, "videos"), exist_ok=True)
nbf.write(nb, os.path.join(RAIZ, "videos", "fabrica_videos.ipynb"))
print("videos/fabrica_videos.ipynb")
