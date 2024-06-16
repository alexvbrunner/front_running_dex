import logging
import time
from UTILS.web3_utils import *

# Function to execute a sandwich attack using Uniswap V2 router
def execute_sandwich_attack(web3, target_tx, uniswap_v2_router, config, account, private_key):
    amount_in = web3.toWei(1, 'ether')
    gas_price = get_current_gas_price(web3, config)
    increased_gas_price = int(gas_price * 1.2)

    # Execute a buy transaction at a slightly increased gas price
    buy_tx = execute_trade(web3, uniswap_v2_router, config['TOKEN1'], config['TOKEN2'], amount_in, account, private_key, increased_gas_price)
    logging.info(f"Buy Transaction Hash: {buy_tx.hex()}")

    # Wait for the target transaction to be mined
    while web3.eth.getTransactionReceipt(target_tx.hash) is None:
        time.sleep(1)

    # Execute a sell transaction at the same increased gas price
    sell_tx = execute_trade(web3, uniswap_v2_router, config['TOKEN1'], config['TOKEN2'], amount_in, account, private_key, increased_gas_price)
    logging.info(f"Sell Transaction Hash: {sell_tx.hex()}")

# Function to execute a trade on Uniswap V2
def execute_trade(web3, router, token1, token2, amount, account, private_key, gas_price, config):
    nonce = web3.eth.getTransactionCount(account)
    # Build a transaction for swapping tokens
    tx = router.functions.swapExactTokensForTokens(
        amount,
        0,
        [token1, token2],
        account,
        int(time.time()) + 60
    ).buildTransaction({
        'chainId': config['CHAIN_ID'],
        'gas': config['GAS_LIMIT'],
        'gasPrice': gas_price,
        'nonce': nonce,
    })

    # Sign and send the transaction
    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash