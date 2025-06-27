import pandas as pd
import matplotlib.pyplot as plt

# Carregar os arquivos fornecidos
file_shopee = '/mnt/data/Meganium_Sales_Data_-_Shopee.csv'
file_etsy = '/mnt/data/Meganium_Sales_Data_-_Etsy.csv'
file_aliexpress = '/mnt/data/Meganium_Sales_Data_-_AliExpress.csv'

df_shopee = pd.read_csv(file_shopee)
df_etsy = pd.read_csv(file_etsy)
df_aliexpress = pd.read_csv(file_aliexpress)

# Adicionando coluna de marketplace para cada dataframe
df_shopee['Marketplace'] = 'Shopee'
df_etsy['Marketplace'] = 'Etsy'
df_aliexpress['Marketplace'] = 'AliExpress'

# Unificando os dataframes
df_total = pd.concat([df_shopee, df_etsy, df_aliexpress], ignore_index=True)

# Analisar as colunas relevantes para faturamento e moeda
# Verificando nomes das colunas para definir quais usar
df_total.columns

# Faturamento por moeda
faturamento_moeda = df_total.groupby('currency')['total_price'].sum().reset_index()

# Faturamento por marketplace
faturamento_marketplace = df_total.groupby('Marketplace')['total_price'].sum().reset_index()

# Exibir tabelas para o usuário
import ace_tools as tools; tools.display_dataframe_to_user(name="Faturamento por Moeda", dataframe=faturamento_moeda)
tools.display_dataframe_to_user(name="Faturamento por Marketplace", dataframe=faturamento_marketplace)

# Gráficos de pizza
plt.figure(figsize=(6, 6))
plt.pie(faturamento_moeda['total_price'], labels=faturamento_moeda['currency'], autopct='%1.1f%%', startangle=140)
plt.title('Distribuição do Faturamento por Moeda')
plt.show()

plt.figure(figsize=(6, 6))
plt.pie(faturamento_marketplace['total_price'], labels=faturamento_marketplace['Marketplace'], autopct='%1.1f%%', startangle=140)
plt.title('Distribuição do Faturamento por Marketplace')
plt.show()
