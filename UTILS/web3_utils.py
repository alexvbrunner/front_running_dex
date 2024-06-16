import json
import requests
from web3 import Web3
import logging

def init_web3(config):
    # Initialize a Web3 instance using a WebSocket provider from the given configuration
    return Web3(Web3.WebsocketProvider(config['WEB3_PROVIDER_URL']))

def load_contract_abi(path):
    # Load and return the ABI (Application Binary Interface) from a JSON file at the specified path
    with open(path) as f:
        return json.load(f)

def get_current_gas_price(web3, config):
    # Fetch the current gas price from a specified URL and convert it to Wei
    try:
        response = requests.get(config['GAS_TRACKER_URL'])  # Make an HTTP GET request to the gas tracker URL
        response.raise_for_status()  # Raise an exception for HTTP errors
        gas_data = response.json()  # Parse the JSON response
        return web3.toWei(gas_data['result']['FastGasPrice'], 'gwei')  # Convert the gas price from Gwei to Wei
    except requests.RequestException as e:
        logging.error(f"Failed to fetch gas price: {e}")  # Log an error if the request fails
        return None  # Return None if there is an exception