import logging
import time

def is_interesting_transaction(web3, transaction, config, uniswap_v2_router):
    """
    Determines if a transaction is "interesting" based on specific criteria.
    
    Args:
    - web3: An instance of a Web3 connection.
    - transaction: The transaction object to analyze.
    - config: A dictionary containing configuration parameters like TOKEN1, TOKEN2, and THRESHOLD_AMOUNT.
    - uniswap_v2_router: An instance of the UniswapV2Router contract to decode transaction inputs.
    
    Returns:
    - True if the transaction meets the criteria of swapping a specified amount of TOKEN1 for TOKEN2.
    - False otherwise.
    """
    try:
        input_data = transaction.input
        if input_data.startswith("0x38ed1739"):  # Check if the transaction is a swap function call
            decoded_input = uniswap_v2_router.decode_function_input(input_data)
            if decoded_input[0].fn_name == "swapExactTokensForTokens":
                amount_in = decoded_input[1]['amountIn']
                path = decoded_input[1]['path']
                if path[0] == config['TOKEN1'] and path[-1] == config['TOKEN2']:
                    if amount_in > web3.toWei(config['THRESHOLD_AMOUNT'], 'ether'):
                        return True
    except Exception as e:
        logging.error(f"Error decoding transaction: {e}")
    return False

def handle_event(web3, event, config, uniswap_v2_router):
    """
    Processes an event to check if it contains an interesting transaction.
    
    Args:
    - web3: An instance of a Web3 connection.
    - event: The event object to process.
    - config: A dictionary containing configuration parameters.
    - uniswap_v2_router: An instance of the UniswapV2Router contract.
    
    Returns:
    - The transaction object if it is interesting.
    - None otherwise.
    """
    transaction = web3.eth.getTransaction(event)
    if transaction and is_interesting_transaction(web3, transaction, config, uniswap_v2_router):
        logging.info(f"Found interesting transaction: {transaction.hash.hex()}")
        return transaction
    return None

def track_mempool(web3):
    """
    Creates a filter to track pending transactions in the mempool.
    
    Args:
    - web3: An instance of a Web3 connection.
    
    Returns:
    - A filter object for pending transactions.
    """
    return web3.eth.filter('pending')

