# main.py
# Script principal para execução do bot de trading

import os
import sys
import logging
import time
from datetime import datetime
import argparse

# Importar módulos do projeto
from crypto_trading_bot import CryptoTradingBot, demo_backtest
from performance_monitor import PerformanceMonitor
import config

def setup_logging():
    """Configura o sistema de logs"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger("main")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Bot de Trading de Criptomoedas com IA')
    parser.add_argument('--modo', choices=['real', 'simulacao', 'backtest'], default='simulacao',
                        help='Modo de execução: real, simulacao ou backtest')
    parser.add_argument('--capital', type=float, default=300,
                        help='Capital inicial (em USDT)')
    parser.add_argument('--intervalo', type=int, default=config.INTERVALO_VERIFICACAO,
                        help=f'Intervalo entre verificações (em segundos, padrão: {config.INTERVALO_VERIFICACAO})')
    parser.add_argument('--lucro', type=float, default=config.LIMITE_LUCRO_PERCENTUAL,
                        help=f'Limite de lucro percentual (padrão: {config.LIMITE_LUCRO_PERCENTUAL})')
    parser.add_argument('--stop', type=float, default=config.STOP_LOSS_PERCENTUAL,
                        help=f'Stop loss percentual (padrão: {config.STOP_LOSS_PERCENTUAL})')
    
    return parser.parse_args()

def main():
    """Função principal"""
    # Configurar logging
    logger = setup_logging()
    logger.info("Iniciando bot de trading de criptomoedas")
    
    # Parsear argumentos
    args = parse_arguments()
    logger.info(f"Modo de execução: {args.modo}")
    
    # Criar monitor de desempenho
    monitor = PerformanceMonitor()
    
    # Executar de acordo com o modo
    if args.modo == 'backtest':
        logger.info("Iniciando backtest...")
        demo_backtest()
        logger.info("Backtest concluído")
        return
    
    # Verificar credenciais da API
    if args.modo == 'real' and (not config.API_KEY or not config.API_SECRET):
        logger.error("Chaves da API não configuradas. Edite o arquivo config.py para usar o modo real.")
        logger.info("Alternando para modo de simulação.")
        args.modo = 'simulacao'
    
    # Configurar bot
    try:
        # Capital por cripto (dividir o capital pelo número de criptos)
        capital_por_cripto = args.capital / len(config.CRIPTOS)
        
        logger.info(f"Capital total: {args.capital} USDT, Capital por cripto: {capital_por_cripto:.2f} USDT")
        logger.info(f"Alvo de lucro: {args.lucro}%, Stop loss: {args.stop}%")
        
        # Criar bot
        bot = CryptoTradingBot(
            api_key=config.API_KEY if args.modo == 'real' else None,
            api_secret=config.API_SECRET if args.modo == 'real' else None,
            criptos=config.CRIPTOS,
            timeframe=config.TIMEFRAME,
            investimento_por_cripto=capital_por_cripto,
            limite_lucro_percentual=args.lucro,
            stop_loss_percentual=args.stop
        )
        
        # Registrar início de sessão
        monitor.record_trade({
            "type": "session_start",
            "mode": args.modo,
            "initial_capital": args.capital,
            "timestamp": datetime.now().isoformat(),
            "settings": {
                "criptos": config.CRIPTOS,
                "timeframe": config.TIMEFRAME,
                "limite_lucro": args.lucro,
                "stop_loss": args.stop,
                "intervalo": args.intervalo
            }
        })
        
        # Hook para registrar operações
        def on_trade_hook(trade_data):
            monitor.record_trade(trade_data)
        
        # Registrar hook no bot
        bot.set_trade_hook(on_trade_hook)
        
        # Iniciar bot
        if args.modo == 'real':
            logger.info("Iniciando bot em modo REAL - Operações serão executadas na exchange!")
            time.sleep(3)  # Pausa para o usuário ler o aviso
            logger.info("3...")
            time.sleep(1)
            logger.info("2...")
            time.sleep(1)
            logger.info("1...")
            time.sleep(1)
            logger.info("Bot iniciado!")
        else:
            logger.info("Iniciando bot em modo de SIMULAÇÃO - Sem operações reais na exchange")
        
        # Iniciar o bot
        bot.iniciar(intervalo_segundos=args.intervalo)
        
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
        
        # Gerar relatório final
        logger.info("Gerando relatório de desempenho...")
        monitor.generate_performance_report()
        monitor.print_summary()
        
    except Exception as e:
        logger.error(f"Erro crítico: {str(e)}", exc_info=True)
        # Tentar gerar relatório mesmo em caso de erro
        try:
            monitor.generate_performance_report()
            monitor.print_summary()
        except:
            pass

if __name__ == "__main__":
    main()