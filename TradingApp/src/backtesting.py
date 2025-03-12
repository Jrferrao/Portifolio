#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import matplotlib.pyplot as plt
from pathlib import Path

logger = logging.getLogger("TradingBot-Backtest")

class Backtest:
    """Classe para realizar backtests da estratégia de trading."""
    
    def __init__(self, config, data_provider=None):
        """
        Inicializa o módulo de backtest.
        
        Args:
            config (dict): Configuração do backtest
            data_provider: Provedor de dados históricos
        """
        self.config = config
        self.data_provider = data_provider
        self.results = {
            'trades': [],
            'equity_curve': [],
            'metrics': {}
        }
        
    def load_historical_data(self, symbol, from_date, to_date):
        """
        Carrega dados históricos para o backtest.
        
        Args:
            symbol (str): Símbolo do ativo
            from_date (datetime): Data inicial
            to_date (datetime): Data final
            
        Returns:
            pandas.DataFrame: Dados históricos
        """
        if self.data_provider:
            return self.data_provider.get_historical_data(symbol, from_date, to_date)
        
        # Implementação alternativa (exemplo)
        # Na prática, você conectaria com uma API ou banco de dados
        try:
            # Verifica se temos dados em cache
            cache_file = Path(f"data_cache/{symbol}_{from_date.strftime('%Y%m%d')}_{to_date.strftime('%Y%m%d')}.csv")
            
            if cache_file.exists():
                logger.info(f"Loading cached data for {symbol} from {cache_file}")
                return pd.read_csv(cache_file, parse_dates=['timestamp'])
            
            # Se não, cria dados sintéticos para demonstração
            logger.warning(f"No data provider configured. Using synthetic data for {symbol}")
            
            # Cria uma série temporal com valores sintéticos
            days = (to_date - from_date).days + 1
            dates = [from_date + timedelta(days=i) for i in range(days)]
            
            # Preços sintéticos com alguma volatilidade
            base_price = 100.0
            prices = [base_price]
            
            for i in range(1, days):
                # Adiciona um movimento aleatório de até ±2%
                change = np.random.normal(0, 0.02)
                new_price = prices[-1] * (1 + change)
                prices.append(new_price)
            
            # Cria DataFrame
            data = pd.DataFrame({
                'timestamp': dates,
                'open': prices,
                'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'close': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
                'volume': [abs(np.random.normal(1000000, 200000)) for _ in prices]
            })
            
            # Assegura que os diretórios existam
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Salva para cache
            data.to_csv(cache_file, index=False)
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading historical data: {str(e)}")
            raise
    
    def apply_strategy(self, data, strategy):
        """
        Aplica a estratégia de trading aos dados históricos.
        
        Args:
            data (pandas.DataFrame): Dados históricos
            strategy: Estratégia de trading a ser aplicada
            
        Returns:
            list: Lista de trades gerados
        """
        trades = []
        position = None
        
        for i in range(len(data)):
            signal = strategy.generate_signal(data.iloc[:i+1])
            
            if signal == 'BUY' and position is None:
                entry_price = data.iloc[i]['close']
                entry_time = data.iloc[i]['timestamp']
                position = {'entry_price': entry_price, 'entry_time': entry_time}
                
            elif signal == 'SELL' and position is not None:
                exit_price = data.iloc[i]['close']
                exit_time = data.iloc[i]['timestamp']
                
                profit_pct = (exit_price - position['entry_price']) / position['entry_price'] * 100
                
                trade = {
                    'entry_time': position['entry_time'],
                    'entry_price': position['entry_price'],
                    'exit_time': exit_time,
                    'exit_price': exit_price,
                    'profit_pct': profit_pct
                }
                
                trades.append(trade)
                position = None
        
        return trades
    
    def calculate_metrics(self, trades, initial_capital=10000):
        """
        Calcula métricas de desempenho a partir dos trades.
        
        Args:
            trades (list): Lista de trades
            initial_capital (float): Capital inicial
            
        Returns:
            dict: Métricas de desempenho
        """
        if not trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_loss': 0,
                'max_drawdown': 0,
                'sharpe_ratio': 0
            }
        
        # Calcular curva de capital
        equity = [initial_capital]
        capital = initial_capital
        
        for trade in trades:
            profit = capital * (trade['profit_pct'] / 100)
            capital += profit
            equity.append(capital)
        
        # Calcular métricas
        wins = sum(1 for trade in trades if trade['profit_pct'] > 0)
        win_rate = (wins / len(trades)) * 100
        
        total_return = ((capital - initial_capital) / initial_capital) * 100
        
        # Calcular drawdown
        peak = equity[0]
        drawdowns = []
        
        for value in equity:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak * 100
            drawdowns.append(drawdown)
        
        max_drawdown = max(drawdowns)
        
        # Calcular retornos diários para Sharpe Ratio
        daily_returns = [(equity[i] / equity[i-1]) - 1 for i in range(1, len(equity))]
        
        if not daily_returns:
            sharpe_ratio = 0
        else:
            # Assumindo taxa livre de risco anual de 2%
            risk_free_daily = 0.02 / 252  # 252 dias de trading em um ano
            sharpe_ratio = (np.mean(daily_returns) - risk_free_daily) / np.std(daily_returns) * np.sqrt(252)
        
        return {
            'total_trades': len(trades),
            'win_rate': win_rate,
            'profit_loss': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'equity_curve': equity
        }
    
    def run(self, strategy, symbol, from_date, to_date, initial_capital=10000):
        """
        Executa o backtest completo.
        
        Args:
            strategy: Estratégia de trading
            symbol (str): Símbolo do ativo
            from_date (datetime): Data inicial
            to_date (datetime): Data final
            initial_capital (float): Capital inicial
            
        Returns:
            dict: Resultados do backtest
        """
        logger.info(f"Running backtest for {symbol} from {from_date} to {to_date}")
        
        # Carregar dados históricos
        data = self.load_historical_data(symbol, from_date, to_date)
        
        # Aplicar estratégia
        trades = self.apply_strategy(data, strategy)
        
        # Calcular métricas
        metrics = self.calculate_metrics(trades, initial_capital)
        
        self.results = {
            'trades': trades,
            'metrics': metrics,
            'equity_curve': metrics.pop('equity_curve', [])
        }
        
        return self.results
    
    def plot_results(self, output_file=None):
        """
        Plota os resultados do backtest.
        
        Args:
            output_file (str, optional): Caminho para salvar o gráfico
        """
        if not self.results['equity_curve']:
            logger.warning("No equity curve to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
        
        # Curva de capital
        ax1.plot(self.results['equity_curve'], label='Equity Curve')
        ax1.set_title('Backtest Results')
        ax1.set_ylabel('Capital')
        ax1.grid(True)
        ax1.legend()
        
        # Trades
        if self.results['trades']:
            trades_df = pd.DataFrame(self.results['trades'])
            
            # Converter para datetime se necessário
            if isinstance(trades_df['entry_time'].iloc[0], str):
                trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
                trades_df['exit_time'] = pd.to_datetime(trades_df['exit_time'])
            
            # Plotar lucros/perdas
            ax2.bar(range(len(trades_df)), trades_df['profit_pct'], 
                    color=[('green' if x > 0 else 'red') for x in trades_df['profit_pct']])
            ax2.set_xlabel('Trade Number')
            ax2.set_ylabel('Profit/Loss %')
            ax2.grid(True)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)
            logger.info(f"Plot saved to {output_file}")
        else:
            plt.show()

# Função auxiliar para uso direto
def run_quick_backtest(config, strategy, symbol, from_date, to_date, initial_capital=10000):
    """
    Função auxiliar para executar um backtest rápido.
    
    Args:
        config (dict): Configuração
        strategy: Estratégia de trading
        symbol (str): Símbolo do ativo
        from_date (str or datetime): Data inicial
        to_date (str or datetime): Data final
        initial_capital (float): Capital inicial
        
    Returns:
        dict: Resultados do backtest
    """
    # Converter datas se necessário
    if isinstance(from_date, str):
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    if isinstance(to_date, str):
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
    
    backtest = Backtest(config)
    results = backtest.run(strategy, symbol, from_date, to_date, initial_capital)
    backtest.plot_results(f"backtest_{symbol}_{from_date.strftime('%Y%m%d')}_{to_date.strftime('%Y%m%d')}.png")
    
    return results