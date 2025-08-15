from pathlib import Path
from core.broker_client import BrokerClient
from core.execution import sell_puts, sell_calls
from core.state_manager import update_state, calculate_risk
from config.credentials import ALPACA_API_KEY, ALPACA_SECRET_KEY, IS_PAPER
from config.params import MAX_RISK
from logging.strategy_logger import StrategyLogger
from logging.logger_setup import setup_logger
from core.cli_args import parse_args
import logging
import sys

def main():
    args = parse_args()

    # ✅ Initialize general logger early to ensure log file is created
    logger = setup_logger(level=args.log_level, to_file=args.log_to_file)
    logger.addHandler(logging.StreamHandler(sys.stdout))  # Log to console too
    logger.info("🚀 Strategy execution started.")

    # ✅ Initialize strategy-specific logger
    strat_logger = StrategyLogger(enabled=args.strat_log)
    strat_logger.set_fresh_start(args.fresh_start)

    # ✅ Load symbols
    SYMBOLS_FILE = Path(__file__).parent.parent / "config" / "symbol_list.txt"
    if not SYMBOLS_FILE.exists():
        logger.error(f"Symbol list file not found at {SYMBOLS_FILE}")
        return

    with open(SYMBOLS_FILE, 'r') as file:
        SYMBOLS = [line.strip() for line in file.readlines() if line.strip()]
    if not SYMBOLS:
        logger.warning("No symbols found in symbol_list.txt.")
        return

    # ✅ Initialize broker client
    client = BrokerClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, paper=IS_PAPER)

    if args.fresh_start:
        logger.info("Running in fresh start mode — liquidating all positions.")
        client.liquidate_all_positions()
        allowed_symbols = SYMBOLS
        buying_power = MAX_RISK
    else:
        positions = client.get_positions()
        strat_logger.add_current_positions(positions)

        current_risk = calculate_risk(positions)
        states = update_state(positions)
        strat_logger.add_state_dict(states)

        for symbol, state in states.items():
            if state["type"] == "long_shares":
                sell_calls(client, symbol, state["price"], state["qty"], strat_logger)

        allowed_symbols = list(set(SYMBOLS).difference(states.keys()))
        buying_power = MAX_RISK - current_risk

    strat_logger.set_buying_power(buying_power)
    strat_logger.set_allowed_symbols(allowed_symbols)

    logger.info(f"📊 Current buying power: ${buying_power}")
    logger.info(f"📈 Allowed symbols: {allowed_symbols}")

    sell_puts(client, allowed_symbols, buying_power, strat_logger)

    strat_logger.save()
    logger.info("✅ Strategy execution completed.")

if __name__ == "__main__":
    main()