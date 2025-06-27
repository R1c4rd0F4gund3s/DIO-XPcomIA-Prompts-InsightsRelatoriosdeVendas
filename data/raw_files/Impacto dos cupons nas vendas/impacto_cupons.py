import pandas as pd
from datetime import datetime

# Carregar os arquivos
file_shopee = "/mnt/data/Meganium_Sales_Data_-_Shopee.csv"
file_etsy = "/mnt/data/Meganium_Sales_Data_-_Etsy.csv"
file_aliexpress = "/mnt/data/Meganium_Sales_Data_-_AliExpress.csv"

df_shopee = pd.read_csv(file_shopee)
df_etsy = pd.read_csv(file_etsy)
df_aliexpress = pd.read_csv(file_aliexpress)

# Adicionar coluna de origem
df_shopee["marketplace"] = "Shopee"
df_etsy["marketplace"] = "Etsy"
df_aliexpress["marketplace"] = "AliExpress"

# Padronizar nomes das colunas que identificam uso de cupom
cupon_cols = [col for col in df_shopee.columns if "cupon" in col.lower() or "coupon" in col.lower() or "cupom" in col.lower()]
if cupon_cols:
    cupon_col_shopee = cupon_cols[0]
else:
    cupon_col_shopee = None

cupon_cols = [col for col in df_etsy.columns if "cupon" in col.lower() or "coupon" in col.lower() or "cupom" in col.lower()]
if cupon_cols:
    cupon_col_etsy = cupon_cols[0]
else:
    cupon_col_etsy = None

cupon_cols = [col for col in df_aliexpress.columns if "cupon" in col.lower() or "coupon" in col.lower() or "cupom" in col.lower()]
if cupon_cols:
    cupon_col_aliexpress = cupon_cols[0]
else:
    cupon_col_aliexpress = None

# Padronizar coluna de cupom para todos os dataframes
df_shopee["coupon_used"] = df_shopee[cupon_col_shopee] if cupon_col_shopee else False
df_etsy["coupon_used"] = df_etsy[cupon_col_etsy] if cupon_col_etsy else False
df_aliexpress["coupon_used"] = df_aliexpress[cupon_col_aliexpress] if cupon_col_aliexpress else False

# Padronizar nomes de colunas principais
def get_colname(cols, name):
    for col in cols:
        if name in col.lower():
            return col
    return None

q_col_shopee = get_colname(df_shopee.columns, 'quant')
v_col_shopee = get_colname(df_shopee.columns, 'total')
currency_col_shopee = get_colname(df_shopee.columns, 'curren')

q_col_etsy = get_colname(df_etsy.columns, 'quant')
v_col_etsy = get_colname(df_etsy.columns, 'total')
currency_col_etsy = get_colname(df_etsy.columns, 'curren')

q_col_aliexpress = get_colname(df_aliexpress.columns, 'quant')
v_col_aliexpress = get_colname(df_aliexpress.columns, 'total')
currency_col_aliexpress = get_colname(df_aliexpress.columns, 'curren')

# Selecionar e renomear colunas para padronizar
df_shopee = df_shopee.rename(columns={q_col_shopee: "quantity", v_col_shopee: "total_value", currency_col_shopee: "currency"})
df_etsy = df_etsy.rename(columns={q_col_etsy: "quantity", v_col_etsy: "total_value", currency_col_etsy: "currency"})
df_aliexpress = df_aliexpress.rename(columns={q_col_aliexpress: "quantity", v_col_aliexpress: "total_value", currency_col_aliexpress: "currency"})

# Concatenar tudo
df = pd.concat([df_shopee, df_etsy, df_aliexpress], ignore_index=True)

# Ajustar valores para análise
df["coupon_used"] = df["coupon_used"].astype(bool)
df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce').fillna(0)
df["total_value"] = pd.to_numeric(df["total_value"], errors='coerce').fillna(0)

# Agrupar dados
summary = (
    df.groupby(["marketplace", "currency", "coupon_used"])
    .agg(
        volume_vendas = ("quantity", "sum"),
        valor_vendas = ("total_value", "sum"),
        pedidos = ("quantity", "count")
    )
    .reset_index()
)

import ace_tools as tools; tools.display_dataframe_to_user(name="Impacto dos Cupons nas Vendas", dataframe=summary)

summary
