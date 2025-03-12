# Tutorial do Sistema de Trading Bot

Este tutorial irá guiá-lo através da configuração e uso do sistema de Trading Bot.

## Índice
1. [Estrutura do Sistema](#estrutura-do-sistema)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso Básico](#uso-básico)
5. [Comandos Avançados](#comandos-avançados)
6. [Monitoramento de Performance](#monitoramento-de-performance)
7. [Backtesting](#backtesting)
8. [Solução de Problemas](#solução-de-problemas)

## Estrutura do Sistema

O sistema é composto pelos seguintes arquivos:
- `config.py`: Gerencia as configurações do bot
- `main.py`: Contém a implementação principal do bot de trading
- `performance_monitor.py`: Monitora e avalia o desempenho do bot
- `cli.py`: Interface de linha de comando para interagir com o bot
- `backtest.py`: Módulo para realizar backtests das estratégias

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone ou baixe os arquivos do sistema para um diretório local.

2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Certifique-se de que os arquivos Python tenham permissão de execução:
   ```bash
   chmod +x cli.py main.py
   ```

## Configuração

Antes de executar o bot, você precisa configurar os parâmetros de trading:

1. Crie um arquivo de configuração inicial:
   ```bash
   python cli.py config --edit
   ```

2. Defina os parâmetros necessários quando solicitado:
   - **API Keys**: Chaves de API para o serviço de trading
   - **Trading Pairs**: Pares de trading (ex: BTC/USDT)
   - **Risk Parameters**: Parâmetros de gestão de risco
   - **Strategy Settings**: Configurações da estratégia de trading

Alternativamente, você pode criar manualmente um arquivo `config.json` seguindo o formato:

```json
{
  "api": {
    "key": "sua_api_key",
    "secret": "sua_api_secret",
    "exchange": "binance"
  },
  "trading": {
    "pairs": ["BTC/USDT", "ETH/USDT"],
    "timeframe": "1h"
  },
  "risk": {
    "max_position_size": 0.1,
    "stop_loss_pct": 2.0,
    "take_profit_pct": 4.0
  },
  "strategy": {
    "type": "moving_average_crossover",
    "fast_period": 9,
    "slow_period": 21
  }
}
```

## Uso Básico

### Iniciando o Bot

Para iniciar o bot em modo de trading real:
```bash
python cli.py start
```

Para iniciar o bot em modo de paper trading (simulação):
```bash
python cli.py start --paper
```

### Verificando o Status

Para verificar o status atual do bot:
```bash
python cli.py status
```

### Parando o Bot

Para parar o bot:
```bash
python cli.py stop
```

## Comandos Avançados

### Visualizando a Configuração Atual

```bash
python cli.py config --show
```

### Editando a Configuração

```bash
python cli.py config --edit
```

### Gerando Relatório de Desempenho

Para gerar um relatório de desempenho para um período específico:
```bash
python cli.py report --from 2023-01-01 --to 2023-02-01 --output performance_report.html
```

## Monitoramento de Performance

O sistema inclui um módulo de monitoramento de performance que acompanha:
- Taxa de sucesso das operações
- Retorno sobre investimento (ROI)
- Drawdown máximo
- Sharpe ratio

Para visualizar as métricas de performance em tempo real:
```bash
python performance_monitor.py --live
```

## Backtesting

O backtesting permite testar suas estratégias em dados históricos antes de usá-las em trading real.

### Executando um Backtest

```bash
python cli.py backtest --from 2023-01-01 --to 2023-03-01
```

### Visualizando Resultados do Backtest

Os resultados do backtest são salvos como:
- Arquivo JSON com todas as métricas (`backtest_YYYYMMDD_to_YYYYMMDD.json`)
- Gráfico PNG mostrando a curva de capital e trades

## Solução de Problemas

### Logs do Sistema

Os logs do sistema são armazenados em `trading_bot.log`. Consulte este arquivo para informações de depuração.

### Problemas Comuns

1. **Erro de conexão com a exchange**:
   - Verifique suas credenciais de API
   - Confirme se a exchange está online
   - Verifique sua conexão com a internet

2. **Bot não executa trades**:
   - Verifique os parâmetros da estratégia
   - Confirme se há saldo suficiente na conta
   - Verifique os limites de preço e quantidade

3. **Desempenho abaixo do esperado**:
   - Ajuste os parâmetros da estratégia
   - Considere mudar para um timeframe diferente
   - Execute backtests adicionais para otimização

Para suporte adicional, consulte a documentação completa ou abra um issue no repositório do projeto.