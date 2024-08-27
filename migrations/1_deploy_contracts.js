const RewardContract = artifacts.require("RewardContract");

module.exports = function (deployer) {
  deployer.deploy(RewardContract);
};
