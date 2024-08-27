from flwr.server.strategy import FedAvg
from typing import List, Tuple, Optional
from flwr.common import Parameters, FitRes
from web3 import Web3
import json


class CustomFedAvg(FedAvg):
    def __init__(self, web3, contract, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.web3 = web3
        self.contract = contract

    def aggregate_fit(
        self,
        rnd: int,
        results: List[Tuple[Optional[int], FitRes]],
        failures: List[BaseException],
    ) -> Tuple[Optional[Parameters], dict]:
        # Call the original aggregate_fit method to get the aggregated parameters
        aggregated_parameters, metrics = super().aggregate_fit(rnd, results, failures)

        # Example: Reward the first client (simplified example)
        if results:
            client_address = self.web3.to_checksum_address(
                "0x3fBc87403fBFA7A83f74aC9114c1582E73bc10D9"
            )  # Replace with actual client address
            reward_amount = self.web3.to_wei(0.1, "ether")  # Set the reward amount
            self.reward_client(self.web3)

        return aggregated_parameters, metrics

    """def reward_client(self, client_address, amount):
        tx_hash = self.contract.functions.rewardClient(
            client_address, amount
        ).transact()
        self.web3.eth.wait_for_transaction_receipt(tx_hash)"""

    def reward_client(self, w3):
        x_hash = w3.eth.send_transaction(
            {
                "from": w3.eth.accounts[0],
                "to": w3.eth.accounts[1],
                "value": w3.to_wei(3, "ether"),
            }
        )
