"""Diapositivas de los cuadernos: DIAPOS[tema] es una lista de diapositivas, cada una con su «ancla» (el principio
del título de sección tras el que se inserta), título, ideas y figura. Las figuras fijas se dibujan con figuras.py."""
from .estilo import FIGS
from . import m1, m2, m3, m4, m5, diagramas

DIAPOS = {}
for _m in (m1, m2, m3, m4, m5):
    DIAPOS.update(_m.DIAPOS)
