# Consolidar dados usando as colunas corretas
shopee['country'] = shopee['delivery_country']
etsy['country'] = etsy['delivery_country']
aliexpress['country'] = aliexpress['delivery_country']

df_all = pd.concat([
    shopee[['country', 'quantity']],
    etsy[['country', 'quantity']],
    aliexpress[['country', 'quantity']]
])

# Agrupar por país e somar as quantidades
country_sales = df_all.groupby('country', as_index=False)['quantity'].sum().sort_values('quantity', ascending=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Compras por País", dataframe=country_sales)

country_sales.head(10)
