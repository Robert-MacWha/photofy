// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import {ByteHasher} from "./helper/ByteHasher.sol";
import {IWorldID} from "./interfaces/IWorldID.sol";

contract ImageRepository {
    using ByteHasher for bytes;

    /// @notice Thrown when attempting to reuse a nullifier
    error InvalidNullifier();

    /// @dev The World ID instance that will be used for verifying proofs
    IWorldID internal immutable worldId;

    /// @dev The contract's external nullifier hash
    uint256 internal immutable externalNullifier;

    /// @dev The World ID group ID (always 1)
    uint256 internal immutable groupId = 1;

    /// @dev Whether a nullifier hash has been used already. Used to guarantee an action is only performed once by a single person
    mapping(uint256 => bool) internal nullifierHashes;

    struct Image {
        uint256 creator;
        bytes32 previousVersion;
        bytes32 representation;
        int8 modificationSummary;
    }

    mapping(address => bool) public admins;
    mapping(bytes32 => Image) public images;
    mapping(uint256 => int) public untrustworthy;

    modifier onlyAdmin() {
        require(admins[msg.sender], "Caller is not an admin");
        _;
    }

    constructor(
        IWorldID _worldId,
        string memory _appId,
        string memory _actionId
    ) {
        worldId = _worldId;
        externalNullifier = abi
            .encodePacked(abi.encodePacked(_appId).hashToField(), _actionId)
            .hashToField();

        admins[msg.sender] = true;
    }

    function uploadImage(
        address signal,
        uint256 root,
        uint256 nullifierHash,
        uint256[8] calldata proof,
        bytes32 previousVersion,
        bytes32 representation,
        int8 modificationSummary
    ) public {
        // Verify the provided proof is valid and the user is verified by World ID
        worldId.verifyProof(
            root,
            groupId,
            abi.encodePacked(signal).hashToField(),
            nullifierHash,
            externalNullifier,
            proof
        );

        // We now record the user has done this, so they can't do it again (proof of uniqueness)
        nullifierHashes[nullifierHash] = true;

        images[representation] = Image(
            nullifierHash,
            previousVersion,
            representation,
            modificationSummary
        );
    }

    function getImage(
        bytes32 representation
    ) public view returns (uint256, bytes32, int8) {
        uint256 a = images[representation].creator;
        bytes32 b = images[representation].previousVersion;
        int8 m = images[representation].modificationSummary;

        return (a, b, m);
    }

    function flagUntrustworthy(uint256 userID, int score) public onlyAdmin {
        untrustworthy[userID] = score;
    }

    function addAdmin(address user) public onlyAdmin {
        admins[user] = true;
    }

    function removeAdmin(address user) public onlyAdmin {
        require(user != msg.sender, "Admin cannot remove themselves");
        admins[user] = false;
    }
}
