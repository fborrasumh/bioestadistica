"""Genera los conjuntos de datos sintéticos de la asignatura (semilla fija).

Autor: Fernando Borrás Rocher. Ningún dato corresponde a personas reales.

- cohorte_cardiovascular.csv: 400 pacientes de Atención Primaria de tres centros,
  con errores de registro deliberados para practicar la limpieza (Tema 100).
- analiticas.csv: resultados de laboratorio de la misma cohorte (Tema 110).
- centros.csv: características de los centros de salud (Tema 110).
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(1964)
n = 400

centro = rng.choice(["CS Norte", "CS Sur", "CS Centro"], size=n, p=[0.4, 0.35, 0.25])
mujer = rng.random(n) < 0.52
edad = rng.integers(40, 86, size=n)
talla_cm = np.where(mujer, rng.normal(160, 6.5, n), rng.normal(173, 7, n)).round(0)
imc = rng.normal(27.5, 4.5, n).clip(17, 45)
peso_kg = (imc * (talla_cm / 100) ** 2).round(1)
fumador = rng.random(n) < np.where(mujer, 0.18, 0.26)
diabetes = rng.random(n) < (0.06 + 0.003 * (edad - 40) + 0.01 * (imc - 25)).clip(0.02, 0.5)
pas = (112 + 0.55 * (edad - 40) + 0.9 * (imc - 25) + 4 * diabetes + rng.normal(0, 13, n)).round(0)
pad = (72 + 0.12 * (edad - 40) + 0.5 * (imc - 25) + rng.normal(0, 8, n)).round(0)
hta_tratada = (pas >= 140) & (rng.random(n) < 0.7)
colesterol = rng.normal(205, 38, n).round(0)
hdl = np.where(mujer, rng.normal(58, 12, n), rng.normal(48, 10, n)).round(0)
glucemia = np.where(diabetes, rng.normal(148, 30, n), rng.normal(94, 10, n)).round(0)

logit = -7.2 + 0.07 * edad + 0.6 * fumador + 0.7 * diabetes + 0.018 * (pas - 120) - 0.02 * (hdl - 50) + 0.4 * (~mujer)
evento = rng.random(n) < 1 / (1 + np.exp(-logit))

ids = [f"CV-{i:04d}" for i in range(1, n + 1)]
cohorte = pd.DataFrame({
    "id": ids,
    "centro": centro,
    "sexo": np.where(mujer, "Mujer", "Hombre"),
    "edad": edad,
    "peso_kg": peso_kg,
    "talla_cm": talla_cm,
    "pas_mmHg": pas,
    "pad_mmHg": pad,
    "colesterol_mg_dl": colesterol,
    "hdl_mg_dl": hdl,
    "glucemia_mg_dl": glucemia,
    "fumador": np.where(fumador, "Sí", "No"),
    "diabetes": np.where(diabetes, "Sí", "No"),
    "hta_tratada": np.where(hta_tratada, "Sí", "No"),
    "evento_cv_5a": evento.astype(int),
})

# Errores de registro deliberados
cohorte = cohorte.astype({"peso_kg": "object", "talla_cm": "object", "sexo": "object", "fumador": "object"})
idx = rng.permutation(n)
for i in idx[:6]:
    cohorte.loc[i, "sexo"] = rng.choice(["mujer", "M", "hombre", "H"])
for i in idx[6:10]:
    cohorte.loc[i, "fumador"] = rng.choice(["si", "SI", "no"])
cohorte.loc[idx[10], "peso_kg"] = 680.0            # coma desplazada (68,0)
cohorte.loc[idx[11], "peso_kg"] = 7.4              # coma desplazada (74)
for i in idx[12:16]:                               # talla registrada en metros
    cohorte.loc[i, "talla_cm"] = round(float(cohorte.loc[i, "talla_cm"]) / 100, 2)
a, b = cohorte.loc[idx[16], "pas_mmHg"], cohorte.loc[idx[16], "pad_mmHg"]
cohorte.loc[idx[16], ["pas_mmHg", "pad_mmHg"]] = [b, a]   # sistólica y diastólica invertidas
cohorte.loc[idx[17], "glucemia_mg_dl"] = 1120      # cero de más
for col, k in [("peso_kg", 18), ("colesterol_mg_dl", 30), ("hdl_mg_dl", 34), ("glucemia_mg_dl", 12)]:
    filas = rng.choice(n, size=k, replace=False)
    cohorte.loc[filas, col] = np.nan
filas = rng.choice(n, size=9, replace=False)
cohorte.loc[filas, "fumador"] = np.nan
cohorte = pd.concat([cohorte, cohorte.iloc[[idx[20], idx[21]]]], ignore_index=True)  # duplicados

cohorte.to_csv("cohorte_cardiovascular.csv", index=False)

# Analíticas (Tema 110): no todos los pacientes tienen analítica y hay alguno que no está en la cohorte
con_analitica = rng.choice(ids, size=360, replace=False)
analiticas = pd.DataFrame({
    "id": con_analitica,
    "hba1c_pct": np.where(
        pd.Series(con_analitica).map(dict(zip(ids, diabetes))).to_numpy(),
        rng.normal(7.4, 1.2, 360), rng.normal(5.4, 0.35, 360)).round(1).clip(4.5, 12),
    "creatinina_mg_dl": (rng.lognormal(np.log(0.92), 0.22, 360)
                         * np.where(rng.random(360) < 0.1, rng.uniform(1.6, 3.2, 360), 1)).round(2),
    "ldl_mg_dl": rng.normal(125, 33, 360).round(0),
})
extra = pd.DataFrame({"id": ["CV-9001", "CV-9002"], "hba1c_pct": [6.1, 7.4],
                      "creatinina_mg_dl": [0.9, 1.4], "ldl_mg_dl": [130, 98]})
pd.concat([analiticas, extra]).to_csv("analiticas.csv", index=False)

pd.DataFrame({
    "centro": ["CS Norte", "CS Sur", "CS Centro"],
    "tipo": ["urbano", "urbano", "rural"],
    "poblacion_asignada": [21500, 18200, 9400],
}).to_csv("centros.csv", index=False)

print(cohorte.shape, analiticas.shape)
