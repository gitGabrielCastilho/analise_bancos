import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


tickers = {
    'Itaú': 'ITUB4.SA',
    'Santander': 'SANB11.SA',
    'Bradesco': 'BBDC4.SA',
    'Banco do Brasil': 'BBAS3.SA'
}

def get_stock_data(ticker):
    data = yf.download(ticker, start='2020-01-01', end='2024-01-01')
    return data


dataframes = {name: get_stock_data(ticker) for name, ticker in tickers.items()}


for bank, df in dataframes.items():
    filename = f"{bank.replace(' ', '_')}_data.csv"  
    df.to_csv(filename)

files = {
    'Itaú': 'Itaú_data.csv',
    'Santander': 'Santander_data.csv',
    'Bradesco': 'Bradesco_data.csv',
    'Banco do Brasil': 'Banco_do_Brasil_data.csv'
}

dataframes = {bank: pd.read_csv(file, index_col='Date', parse_dates=True) for bank, file in files.items()}

for bank, df in dataframes.items():
    print(f"Estatísticas descritivas para {bank}:\n", df.describe(), "\n")

######################################################################################
#Análise Exploratória com Seaborn

#Preço Fechamento
plt.figure(figsize=(14, 7))

for bank, df in dataframes.items():
    plt.plot(df.index, df['Close'], label=bank)

plt.title('Preços de Fechamento dos Bancos')
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento (R$)')
plt.legend()
plt.show()

#Retorno Diário
plt.figure(figsize=(14, 7))

for bank, df in dataframes.items():
    df['Daily Return'] = df['Close'].pct_change()
    plt.plot(df.index, df['Daily Return'], label=bank)

plt.title('Retornos Diários dos Bancos')
plt.xlabel('Data')
plt.ylabel('Retorno Diário (%)')
plt.legend()
plt.show()


plt.figure(figsize=(14, 7))

for bank, df in dataframes.items():
    sns.histplot(df['Daily Return'].dropna(), bins=50, kde=True, label=bank, alpha=0.5)

plt.title('Histogramas dos Retornos Diários')
plt.xlabel('Retorno Diário (%)')
plt.ylabel('Frequência')
plt.legend()
plt.show()


# Matriz de correlação
returns = pd.concat([df['Daily Return'] for df in dataframes.values()], axis=1)
returns.columns = dataframes.keys()


corr_matrix = returns.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriz de Correlação dos Retornos Diários')
plt.show()

#Análise Comparativa
mean_returns = returns.mean()
std_returns = returns.std()

print("Média dos Retornos Diários:\n", mean_returns)
print("\nDesvio Padrão dos Retornos Diários:\n", std_returns)







