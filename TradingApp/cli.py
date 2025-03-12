#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import logging
from datetime import datetime

# Importações dos outros módulos do projeto
from config import load_config, save_config
from main import TradingBot
from performance_monitor import PerformanceMonitor
from src.backtest import Backtest

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/trading_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingBot-CLI")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Trading Bot CLI')
    
    # Subparsers para diferentes comandos
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Comando de iniciar
    start_parser = subparsers.add_parser('start', help='Start the trading bot')
    start_parser.add_argument('--config', '-c', type=str, default='config.json', 
                             help='Path to configuration file')
    start_parser.add_argument('--paper', '-p', action='store_true', 
                             help='Run in paper trading mode')
    
    # Comando de parar
    stop_parser = subparsers.add_parser('stop', help='Stop the trading bot')
    
    # Comando de status
    status_parser = subparsers.add_parser('status', help='Check bot status')
    
    # Comando de configuração
    config_parser = subparsers.add_parser('config', help='Configure the trading bot')
    config_parser.add_argument('--edit', '-e', action='store_true', 
                              help='Edit configuration file')
    config_parser.add_argument('--show', '-s', action='store_true',
                              help='Show current configuration')
    
    # Comando de relatório de desempenho
    report_parser = subparsers.add_parser('report', help='Generate performance report')
    report_parser.add_argument('--from', dest='from_date', type=str,
                              help='Start date (YYYY-MM-DD)')
    report_parser.add_argument('--to', dest='to_date', type=str,
                              help='End date (YYYY-MM-DD)')
    report_parser.add_argument('--output', '-o', type=str, default='report.html',
                              help='Output file for the report')
    
    # Comando de backtesting
    backtest_parser = subparsers.add_parser('backtest', help='Run backtest')
    backtest_parser.add_argument('--config', '-c', type=str, default='config.json',
                                help='Path to configuration file')
    backtest_parser.add_argument('--from', dest='from_date', type=str, required=True,
                                help='Start date (YYYY-MM-DD)')
    backtest_parser.add_argument('--to', dest='to_date', type=str, required=True,
                                help='End date (YYYY-MM-DD)')
    
    return parser.parse_args()

def start_bot(args):
    """Inicia o bot de trading."""
    logger.info("Starting trading bot...")
    try:
        config = load_config(args.config)
        bot = TradingBot(config, paper_trading=args.paper)
        bot.start()
        logger.info("Trading bot started successfully!")
    except Exception as e:
        logger.error(f"Failed to start trading bot: {str(e)}")
        sys.exit(1)

def stop_bot():
    """Para o bot de trading."""
    logger.info("Stopping trading bot...")
    # Aqui você implementaria a lógica para parar o bot
    # Por exemplo, escrevendo em um arquivo de controle ou enviando um sinal
    try:
        # Simples exemplo - na prática, você precisaria de um mecanismo mais robusto
        with open('.bot_control', 'w') as f:
            f.write('STOP')
        logger.info("Stop signal sent to trading bot.")
    except Exception as e:
        logger.error(f"Failed to stop trading bot: {str(e)}")
        sys.exit(1)

def check_status():
    """Verifica o status atual do bot."""
    logger.info("Checking trading bot status...")
    # Implementação da verificação de status
    # Isto poderia verificar processos, arquivos de status, etc.
    try:
        if os.path.exists('.bot_control'):
            with open('.bot_control', 'r') as f:
                status = f.read().strip()
            
            if status == 'RUNNING':
                print("Bot status: RUNNING")
            elif status == 'STOP':
                print("Bot status: STOPPED")
            else:
                print(f"Bot status: UNKNOWN ({status})")
        else:
            print("Bot status: NOT INITIALIZED")
    except Exception as e:
        logger.error(f"Failed to check bot status: {str(e)}")
        sys.exit(1)

def handle_config(args):
    """Manipula as operações de configuração."""
    if args.show:
        # Mostrar a configuração atual
        try:
            config = load_config('config/config.json')
            print("\nCurrent configuration:")
            for key, value in config.items():
                if isinstance(value, dict):
                    print(f"\n{key}:")
                    for subkey, subvalue in value.items():
                        print(f"  {subkey}: {subvalue}")
                else:
                    print(f"{key}: {value}")
        except Exception as e:
            logger.error(f"Failed to show configuration: {str(e)}")
            sys.exit(1)
    
    elif args.edit:
        # Editar a configuração
        # Esta é uma versão simplificada. Na prática, você pode querer um editor interativo
        try:
            config = load_config('config.json')
            print("\nEditing configuration. Enter new values (leave empty to keep current):")
            
            for key, value in config.items():
                if not isinstance(value, dict):
                    new_value = input(f"{key} [{value}]: ")
                    if new_value:
                        config[key] = type(value)(new_value) if not isinstance(value, bool) else (new_value.lower() == 'true')
                else:
                    print(f"\nEditing {key}:")
                    for subkey, subvalue in value.items():
                        new_value = input(f"  {subkey} [{subvalue}]: ")
                        if new_value:
                            config[key][subkey] = type(subvalue)(new_value) if not isinstance(subvalue, bool) else (new_value.lower() == 'true')
            
            save_config(config, 'config.json')
            print("Configuration saved successfully!")
        except Exception as e:
            logger.error(f"Failed to edit configuration: {str(e)}")
            sys.exit(1)

def generate_report(args):
    """Gera um relatório de desempenho."""
    logger.info(f"Generating performance report from {args.from_date} to {args.to_date}...")
    try:
        from_date = datetime.strptime(args.from_date, "%Y-%m-%d") if args.from_date else None
        to_date = datetime.strptime(args.to_date, "%Y-%m-%d") if args.to_date else datetime.now()
        
        monitor = PerformanceMonitor()
        report = monitor.generate_report(from_date=from_date, to_date=to_date)
        
        # Garantir que o diretório exista
        os.makedirs("reports/performance", exist_ok=True)
        
        # Salvar o relatório no caminho correto
        with open(f"reports/performance/{args.output}", 'w') as f:
            f.write(report)
        
        logger.info(f"Report generated successfully: reports/performance/{args.output}")
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        sys.exit(1)

def run_backtest(args):
    """Executa um backtest com os parâmetros definidos."""
    logger.info(f"Running backtest from {args.from_date} to {args.to_date}...")
    try:
        config = load_config(args.config)
        from_date = datetime.strptime(args.from_date, "%Y-%m-%d")
        to_date = datetime.strptime(args.to_date, "%Y-%m-%d")
        
        bot = TradingBot(config, paper_trading=True)
        results = bot.run_backtest(from_date=from_date, to_date=to_date)
        
        print("\nBacktest Results:")
        print(f"Total Trades: {results.get('total_trades', 0)}")
        print(f"Win Rate: {results.get('win_rate', 0):.2f}%")
        print(f"Profit/Loss: {results.get('profit_loss', 0):.2f}%")
        print(f"Max Drawdown: {results.get('max_drawdown', 0):.2f}%")
        print(f"Sharpe Ratio: {results.get('sharpe_ratio', 0):.2f}")
        
        # Salvar resultados em arquivo para análise posterior
        with open(f"backtest_{args.from_date}_to_{args.to_date}.json", 'w') as f:
            import json
            json.dump(results, f, indent=4)
        
        logger.info("Backtest completed successfully!")
    except Exception as e:
        logger.error(f"Failed to run backtest: {str(e)}")
        sys.exit(1)

def main():
    """Função principal do CLI."""
    args = parse_arguments()
    
    if args.command == 'start':
        start_bot(args)
    elif args.command == 'stop':
        stop_bot()
    elif args.command == 'status':
        check_status()
    elif args.command == 'config':
        handle_config(args)
    elif args.command == 'report':
        generate_report(args)
    elif args.command == 'backtest':
        run_backtest(args)
    else:
        print("Please specify a command. Use --help for more information.")
        sys.exit(1)

if __name__ == "__main__":
    main()