# performance_monitor.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime, timedelta
import numpy as np

class PerformanceMonitor:
    def __init__(self, results_dir="./results"):
        """
        Inicializa o monitor de desempenho
        
        Args:
            results_dir: Diretório para salvar os resultados
        """
        self.results_dir = results_dir
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        self.trades_file = os.path.join(results_dir, "trades.json")
        self.performance_file = os.path.join(results_dir, "performance.json")
        
        # Inicializar arquivos se não existirem
        if not os.path.exists(self.trades_file):
            with open(self.trades_file, "w") as f:
                json.dump([], f)
        
        if not os.path.exists(self.performance_file):
            with open(self.performance_file, "w") as f:
                json.dump({
                    "start_capital": 0,
                    "current_capital": 0,
                    "total_profit": 0,
                    "win_rate": 0,
                    "total_trades": 0,
                    "winning_trades": 0,
                    "losing_trades": 0,
                    "daily_returns": []
                }, f)
    
    def record_trade(self, trade_data):
        """
        Registra uma operação de trading
        
        Args:
            trade_data: Dicionário com informações da operação
        """
        # Carregar operações existentes
        with open(self.trades_file, "r") as f:
            trades = json.load(f)
        
        # Adicionar timestamp
        if "timestamp" not in trade_data:
            trade_data["timestamp"] = datetime.now().isoformat()
        
        # Adicionar nova operação
        trades.append(trade_data)
        
        # Salvar operações
        with open(self.trades_file, "w") as f:
            json.dump(trades, f, indent=2)
        
        # Atualizar métricas de desempenho
        self.update_performance_metrics()
    
    def update_performance_metrics(self):
        """
        Atualiza as métricas de desempenho com base nas operações registradas
        """
        # Carregar operações
        with open(self.trades_file, "r") as f:
            trades = json.load(f)
        
        # Carregar métricas atuais
        with open(self.performance_file, "r") as f:
            performance = json.load(f)
        
        # Calcular métricas
        completed_trades = [t for t in trades if t.get("type") == "sell"]
        
        if completed_trades:
            winning_trades = [t for t in completed_trades if t.get("profit", 0) > 0]
            losing_trades = [t for t in completed_trades if t.get("profit", 0) <= 0]
            
            performance["total_trades"] = len(completed_trades)
            performance["winning_trades"] = len(winning_trades)
            performance["losing_trades"] = len(losing_trades)
            performance["win_rate"] = len(winning_trades) / len(completed_trades) * 100 if completed_trades else 0
            
            # Calcular capital atual e lucro total
            if "start_capital" not in performance or performance["start_capital"] == 0:
                # Inferir capital inicial da primeira operação
                first_trade = min(trades, key=lambda x: x.get("timestamp", ""))
                if "initial_capital" in first_trade:
                    performance["start_capital"] = first_trade["initial_capital"]
                else:
                    performance["start_capital"] = 1000  # Valor padrão
            
            total_profit = sum([t.get("profit", 0) for t in completed_trades])
            performance["total_profit"] = total_profit
            performance["current_capital"] = performance["start_capital"] + total_profit
            
            # Calcular retornos diários
            daily_returns = {}
            for trade in completed_trades:
                if "timestamp" in trade:
                    date = trade["timestamp"].split("T")[0]
                    if date not in daily_returns:
                        daily_returns[date] = 0
                    daily_returns[date] += trade.get("profit", 0)
            
            performance["daily_returns"] = [{"date": date, "return": value} for date, value in daily_returns.items()]
        
        # Salvar métricas atualizadas
        with open(self.performance_file, "w") as f:
            json.dump(performance, f, indent=2)
    
    def generate_performance_report(self):
        """
        Gera um relatório de desempenho e gráficos
        
        Returns:
            dict: Relatório de desempenho
        """
        # Carregar métricas
        with open(self.performance_file, "r") as f:
            performance = json.load(f)
        
        # Carregar operações
        with open(self.trades_file, "r") as f:
            trades = json.load(f)
        
        completed_trades = [t for t in trades if t.get("type") == "sell"]
        
        # Criar DataFrame para análise
        if completed_trades:
            df_trades = pd.DataFrame(completed_trades)
            if "timestamp" in df_trades.columns:
                df_trades["timestamp"] = pd.to_datetime(df_trades["timestamp"])
                df_trades.sort_values("timestamp", inplace=True)
            
            # Adicionar capital acumulado
            if "profit" in df_trades.columns:
                df_trades["cumulative_profit"] = df_trades["profit"].cumsum()
                df_trades["cumulative_capital"] = performance["start_capital"] + df_trades["cumulative_profit"]
            
            # Gerar gráficos
            self._generate_equity_curve(df_trades, performance)
            self._generate_win_loss_chart(performance)
            self._generate_crypto_performance(df_trades)
        
        # Preparar relatório
        report = {
            "summary": {
                "start_capital": performance["start_capital"],
                "current_capital": performance["current_capital"],
                "total_profit": performance["total_profit"],
                "total_profit_percentage": (performance["total_profit"] / performance["start_capital"]) * 100 if performance["start_capital"] > 0 else 0,
                "win_rate": performance["win_rate"],
                "total_trades": performance["total_trades"]
            },
            "trading_period": {
                "start_date": min([t.get("timestamp", "") for t in trades]).split("T")[0] if trades else "N/A",
                "end_date": max([t.get("timestamp", "") for t in trades]).split("T")[0] if trades else "N/A"
            },
            "per_crypto": self._get_per_crypto_stats(completed_trades)
        }
        
        # Salvar relatório
        with open(os.path.join(self.results_dir, "report.json"), "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _get_per_crypto_stats(self, completed_trades):
        """
        Calcula estatísticas por criptomoeda
        """
        stats = {}
        
        for crypto in set([t.get("symbol", "unknown") for t in completed_trades]):
            crypto_trades = [t for t in completed_trades if t.get("symbol") == crypto]
            winning = [t for t in crypto_trades if t.get("profit", 0) > 0]
            
            stats[crypto] = {
                "total_trades": len(crypto_trades),
                "winning_trades": len(winning),
                "win_rate": len(winning) / len(crypto_trades) * 100 if crypto_trades else 0,
                "total_profit": sum([t.get("profit", 0) for t in crypto_trades]),
                "average_profit": sum([t.get("profit", 0) for t in crypto_trades]) / len(crypto_trades) if crypto_trades else 0,
                "best_trade": max([t.get("profit", 0) for t in crypto_trades]) if crypto_trades else 0,
                "worst_trade": min([t.get("profit", 0) for t in crypto_trades]) if crypto_trades else 0
            }
        
        return stats
    
    def _generate_equity_curve(self, df_trades, performance):
        """
        Gera gráfico de curva de capital
        """
        if "cumulative_capital" in df_trades.columns and "timestamp" in df_trades.columns:
            plt.figure(figsize=(12, 6))
            plt.plot(df_trades["timestamp"], df_trades["cumulative_capital"])
            plt.axhline(y=performance["start_capital"], color='r', linestyle='--', label='Capital Inicial')
            plt.title("Curva de Capital")
            plt.xlabel("Data")
            plt.ylabel("Capital (USDT)")
            plt.grid(True)
            plt.legend()
            plt.savefig(os.path.join(self.results_dir, "equity_curve.png"))
            plt.close()
    
    def _generate_win_loss_chart(self, performance):
        """
        Gera gráfico de vitórias e derrotas
        """
        labels = ['Vitórias', 'Derrotas']
        sizes = [performance["winning_trades"], performance["losing_trades"]]
        colors = ['#4CAF50', '#F44336']
        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title("Proporção de Operações Vencedoras vs. Perdedoras")
        plt.savefig(os.path.join(self.results_dir, "win_loss_chart.png"))
        plt.close()
    
    def _generate_crypto_performance(self, df_trades):
        """
        Gera gráfico de desempenho por criptomoeda
        """
        if "symbol" in df_trades.columns and "profit" in df_trades.columns:
            crypto_profit = df_trades.groupby("symbol")["profit"].sum()
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(crypto_profit.index, crypto_profit.values)
            
            # Colorir barras (verde para lucro, vermelho para prejuízo)
            for i, bar in enumerate(bars):
                bar.set_color('#4CAF50' if crypto_profit.values[i] > 0 else '#F44336')
            
            plt.title("Lucro/Prejuízo por Criptomoeda")
            plt.xlabel("Criptomoeda")
            plt.ylabel("Lucro/Prejuízo (USDT)")
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.savefig(os.path.join(self.results_dir, "crypto_performance.png"))
            plt.close()
    
    def print_summary(self):
        """
        Imprime um resumo do desempenho no console
        """
        # Carregar métricas
        with open(self.performance_file, "r") as f:
            performance = json.load(f)
        
        print("\n" + "="*50)
        print("RESUMO DE DESEMPENHO DO BOT DE TRADING")
        print("="*50)
        
        print(f"\nCapital inicial: {performance['start_capital']:.2f} USDT")
        print(f"Capital atual: {performance['current_capital']:.2f} USDT")
        print(f"Lucro total: {performance['total_profit']:.2f} USDT ({(performance['total_profit']/performance['start_capital']*100 if performance['start_capital'] > 0 else 0):.2f}%)")
        print(f"Total de operações: {performance['total_trades']}")
        print(f"Operações vencedoras: {performance['winning_trades']} ({performance['win_rate']:.2f}%)")
        print(f"Operações perdedoras: {performance['losing_trades']} ({(100-performance['win_rate']):.2f}%)")
        
        # Carregar operações
        with open(self.trades_file, "r") as f:
            trades = json.load(f)
        
        if trades:
            completed_trades = [t for t in trades if t.get("type") == "sell"]
            if completed_trades:
                best_trade = max(completed_trades, key=lambda x: x.get("profit", 0))
                worst_trade = min(completed_trades, key=lambda x: x.get("profit", 0))
                
                print(f"\nMelhor operação: {best_trade.get('symbol', 'N/A')} - Lucro: {best_trade.get('profit', 0):.2f} USDT")
                print(f"Pior operação: {worst_trade.get('symbol', 'N/A')} - Lucro: {worst_trade.get('profit', 0):.2f} USDT")
        
        print("\nRelatório completo salvo em:", os.path.join(self.results_dir, "report.json"))
        print("="*50)


# Exemplo de uso
if __name__ == "__main__":
    # Criar monitor de desempenho
    monitor = PerformanceMonitor()
    
    # Exemplo de registro de operações (para testes)
    for i in range(10):
        profit = np.random.normal(0.5, 1)
        monitor.record_trade({
            "symbol": np.random.choice(["SOL/USDT", "MATIC/USDT", "AVAX/USDT"]),
            "type": "sell",
            "entry_price": 100,
            "exit_price": 100 + profit,
            "quantity": 1,
            "profit": profit,
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
        })
    
    # Gerar relatório
    report = monitor.generate_performance_report()
    
    # Imprimir resumo
    monitor.print_summary()