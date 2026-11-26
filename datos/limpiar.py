"""Aplica la limpieza del Tema 100 y guarda cohorte_limpia.csv (base de los temas siguientes)."""
import numpy as np
import pandas as pd

c = pd.read_csv("cohorte_cardiovascular.csv").drop_duplicates()
c["sexo"] = c["sexo"].str.strip().str.lower().map({"mujer": "Mujer", "m": "Mujer", "hombre": "Hombre", "h": "Hombre"})
c["fumador"] = c["fumador"].str.lower().map({"sí": "Sí", "si": "Sí", "no": "No"})
m = c["talla_cm"] < 3
c.loc[m, "talla_cm"] = c.loc[m, "talla_cm"] * 100
c.loc[(c["peso_kg"] < 30) | (c["peso_kg"] > 250), "peso_kg"] = np.nan
c.loc[c["glucemia_mg_dl"] > 600, "glucemia_mg_dl"] = np.nan
inv = c["pad_mmHg"] >= c["pas_mmHg"]
c.loc[inv, ["pas_mmHg", "pad_mmHg"]] = c.loc[inv, ["pad_mmHg", "pas_mmHg"]].values
c["imc"] = (c["peso_kg"] / (c["talla_cm"] / 100) ** 2).round(1)
c.to_csv("cohorte_limpia.csv", index=False)
print(c.shape)
