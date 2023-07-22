// SPDX-License-Identifier: MIT
pragma solidity ^0.8.6;

contract ImageRepository {
    struct Image {
        address creator;
        bytes32 previousVersion;
        bytes32 representation;
        int8 modificationSummary;
    }

    mapping (address => bool) public admins;
    mapping (bytes32 => Image) public images;
    mapping (address => int) public untrustworthy;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Caller is not an admin");
        _;
    }

    constructor() {
        admins[msg.sender] = true;
    }

    function uploadImage(bytes32 previousVersion, bytes32 representation, int8 modificationSummary) public {
        require(images[representation].creator == address(0));
        images[representation] = Image(msg.sender, previousVersion, representation, modificationSummary);
    }

    function getImage(bytes32 representation) public view returns (address, bytes32, int8) {
        address a = images[representation].creator;
        bytes32 b = images[representation].previousVersion;
        int8 m = images[representation].modificationSummary;

        return (a, b, m);
    }

    function flagUntrustworthy(address user, int score) public onlyAdmin {
        untrustworthy[user] = score;
    }

    function addAdmin(address user) public onlyAdmin {
        admins[user] = true;
    }

    function removeAdmin(address user) public onlyAdmin {
        require(user != msg.sender, "Admin cannot remove themselves");
        admins[user] = false;
    }
}
