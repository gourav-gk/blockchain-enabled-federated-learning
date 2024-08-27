from typing import List, Tuple

from flwr.server import ServerApp, ServerConfig
from flwr.common import Metrics
from web3 import Web3
import json
from custom_strategy import CustomFedAvg  # Import the custom strategy

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verify connection
if not web3.is_connected():
    raise Exception("Failed to connect to Ganache")

# Get the deployed contract address and ABI
with open("build/contracts/RewardContract.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json["abi"]
    network_id = list(contract_json["networks"].keys())[0]
    contract_address = contract_json["networks"][network_id]["address"]

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set up the account that will be used to send transactions
owner_account = web3.eth.accounts[
    0
]  # Replace with the actual owner account if different
web3.eth.default_account = owner_account


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


# Define custom strategy with reward logic
strategy = CustomFedAvg(
    web3, contract, evaluate_metrics_aggregation_fn=weighted_average
)

# Define config
config = ServerConfig(num_rounds=3)

# Flower ServerApp
app = ServerApp(
    config=config,
    strategy=strategy,
)

# Legacy mode
if __name__ == "__main__":
    from flwr.server import start_server

    start_server(
        server_address="0.0.0.0:8080",
        config=config,
        strategy=strategy,
    )
