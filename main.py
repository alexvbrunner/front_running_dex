from UTILS.config_utils import load_config
from UTILS.web3_utils import init_web3, load_contract_abi
from UTILS.transaction_utils import track_mempool, handle_event
from UTILS.attack import execute_sandwich_attack
import os
import time

def main():
    config = load_config()
    web3 = init_web3(config)
    uniswap_v2_router_abi = load_contract_abi('UniswapV2Router02.json')
    uniswap_v2_router = web3.eth.contract(address=config['UNISWAP_ROUTER_ADDRESS'], abi=uniswap_v2_router_abi)
    
    tx_filter = track_mempool(web3)
    poll_interval = config.get('POLL_INTERVAL', 2)
    while True:
        for event in tx_filter.get_new_entries():
            target_tx = handle_event(web3, event, config, uniswap_v2_router)
            if target_tx:
                execute_sandwich_attack(web3, target_tx, uniswap_v2_router, config, os.getenv('ACCOUNT_ADDRESS'), os.getenv('PRIVATE_KEY'))
        time.sleep(poll_interval)  # Use the poll_interval

if __name__ == "__main__":
    main()