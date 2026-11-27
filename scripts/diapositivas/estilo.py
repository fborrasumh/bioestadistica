"""Estilo común y utilidades de dibujo de las figuras fijas (PNG) de las diapositivas."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

AZUL, AZUL_CLARO, ROJO, VERDE, NARANJA, GRIS, TINTA = "#4682B4", "#DCE8F3", "#C0392B", "#2E8B57", "#D98200", "#8A97A6", "#1F3B57"
FIGS = {}

plt.rcParams.update({
    "font.size": 15, "axes.titlesize": 18, "axes.labelsize": 15, "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 100, "savefig.dpi": 150, "savefig.bbox": "tight", "axes.titleweight": "bold", "axes.titlecolor": TINTA,
})


def figura(tema, nombre):
    """Registra una función que dibuja la figura tema_XXX_nombre.png."""
    def deco(f):
        FIGS[(tema, nombre)] = f
        return f
    return deco


def lienzo(ancho=12, alto=5.5):
    fig, ax = plt.subplots(figsize=(ancho, alto))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def caja(ax, x, y, w, h, texto, color=AZUL, relleno=None, tam=15, negrita=False, txt=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=2", linewidth=2,
                                edgecolor=color, facecolor=relleno or AZUL_CLARO))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=tam, color=txt or TINTA,
            fontweight="bold" if negrita else "normal", wrap=True)


def flecha(ax, x1, y1, x2, y2, color=GRIS, texto=None, tam=13, curva=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=22, linewidth=2.2, color=color,
                                 connectionstyle=f"arc3,rad={curva}"))
    if texto:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 2.5, texto, ha="center", fontsize=tam, color=color)


def titulo(ax, texto, y=96, tam=19):
    ax.text(50, y, texto, ha="center", va="top", fontsize=tam, fontweight="bold", color=TINTA)
