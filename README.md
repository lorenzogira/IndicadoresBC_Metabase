# IndicadoresBC_Metabase
 
Extração de indicadores econômicos via API pública do Banco Central (SGS).
Documentação da API: https://dadosabertos.bcb.gov.br/dataset/22707-taxa-selic---definida-pelo-copom

Séries escolhidas (códigos SGS conhecidos e estáveis):
  11   -> Taxa Selic (% a.a., diária)
  433  -> IPCA - variação mensal (%)
  1    -> Dólar americano (venda) - PTAX, diária
  189  -> IGP-M - variação mensal (%)

Uso:
    python extrair_indicadores.py

Saída:
    indicadores.db   (SQLite, tabela "indicadores" em formato longo: data | indicador | valor)
    indicadores.csv  (mesma coisa, em CSV, útil como backup ou pra importar direto no Metabase)

