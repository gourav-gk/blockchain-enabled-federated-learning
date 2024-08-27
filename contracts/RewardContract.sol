pragma solidity ^0.8.0;

contract RewardContract {
    address public owner;

    event RewardSent(address indexed client, uint256 amount);
    event OwnerOnly(address caller);

    constructor() {
        owner = msg.sender;
    }

    function rewardClient(address payable client, uint256 amount) public {
        if (msg.sender != owner) {
            emit OwnerOnly(msg.sender);
            revert("Only the owner can reward clients");
        }
        client.transfer(amount);
        emit RewardSent(client, amount);
    }

    // Fallback function to receive Ether
    receive() external payable {}
}
