# config.py
# Configurações para o bot de trading

# Credenciais da API (não compartilhe estas informações)
API_KEY = "SUA_API_KEY_DA_BINANCE"
API_SECRET = "SUA_API_SECRET_DA_BINANCE"

# Lista de criptomoedas para negociar
CRIPTOS = ["SOL/USDT", "MATIC/USDT", "AVAX/USDT"]

# Configurações de trading
INVESTIMENTO_POR_CRIPTO = 100  # Valor em USDT para cada criptomoeda
LIMITE_LUCRO_PERCENTUAL = 0.5  # Alvo de 0.5% de lucro
STOP_LOSS_PERCENTUAL = 0.3     # Stop loss de 0.3%
TIMEFRAME = "5m"               # Intervalo de tempo para análise (5 minutos)
INTERVALO_VERIFICACAO = 300    # Intervalo em segundos entre verificações (5 minutos)

# Configurações avançadas
MAX_OPERACOES_SIMULTANEAS = 3  # Número máximo de operações simultâneas
USAR_MACHINE_LEARNING = True   # Utilizar modelos de machine learning
RETRAIN_INTERVAL = 24          # Retreinar modelos a cada 24 horas