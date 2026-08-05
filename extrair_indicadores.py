import sqlite3
from datetime import date

import pandas as pd
import requests

SERIES = {
    "selic": 11,
    "ipca": 433,
    "dolar_ptax_venda": 1,
    "igpm": 189,
}

# Ajuste o período conforme quiser (formato dd/mm/aaaa)
DATA_INICIAL = "01/01/2015"
DATA_FINAL = date.today().strftime("%d/%m/%Y")

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"


def buscar_serie(nome: str, codigo: int) -> pd.DataFrame:
    """Busca uma série do SGS e devolve um DataFrame (data, indicador, valor)."""
    url = BASE_URL.format(codigo=codigo)
    params = {
        "formato": "json",
        "dataInicial": DATA_INICIAL,
        "dataFinal": DATA_FINAL,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    dados = resp.json()

    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["indicador"] = nome
    return df[["data", "indicador", "valor"]]


def main():
    frames = []
    for nome, codigo in SERIES.items():
        print(f"Buscando {nome} (série {codigo})...")
        try:
            frames.append(buscar_serie(nome, codigo))
        except requests.RequestException as e:
            print(f"  Falhou ao buscar {nome}: {e}")

    if not frames:
        print("Nenhuma série foi extraída. Verifique sua conexão e tente de novo.")
        return

    df_final = pd.concat(frames, ignore_index=True).sort_values(["indicador", "data"])

    # CSV (fácil de importar direto no Metabase/Excel se quiser começar simples)
    df_final.to_csv("indicadores.csv", index=False)

    # SQLite (recomendado para conectar o Metabase de verdade)
    conn = sqlite3.connect("indicadores.db")
    df_final.to_sql("indicadores", conn, if_exists="replace", index=False)
    conn.close()

    print(f"\nOK: {len(df_final)} linhas salvas em indicadores.csv e indicadores.db")
    print(df_final.groupby("indicador")["data"].agg(["min", "max", "count"]))


if __name__ == "__main__":
    main()