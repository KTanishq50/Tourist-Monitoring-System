// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TouristRegistry {
    struct Tourist {
        string touristId;
        string name;
        string aadhaarHash; // hashed
        uint256 validFrom;
        uint256 validTo;
        address registeredBy;
    }

    mapping(string => Tourist) private tourists;
    string[] private touristIds;

    event TouristAdded(string touristId, string name, address indexed registeredBy, uint256 validTo);

    function addTourist(
        string memory _touristId,
        string memory _name,
        string memory _aadhaarHash,
        uint256 _validFrom,
        uint256 _validTo
        
    ) public {
        // if overwriting is OK for your app omit check, else check existence
        tourists[_touristId] = Tourist(
            _touristId,
            _name,
            _aadhaarHash,
            _validFrom,
            _validTo,
            msg.sender
        );
        touristIds.push(_touristId);
        emit TouristAdded(_touristId, _name, msg.sender, _validTo);
    }

    function getTourist(string memory _touristId) public view returns (
        string memory,
        string memory,
        string memory,
        uint256,
        uint256,
        address
    ) {
        Tourist memory t = tourists[_touristId];
        return (
            t.touristId,
            t.name,
            t.aadhaarHash,
            t.validFrom,
            t.validTo,
            t.registeredBy
        );
    }

    function getAllTourists() public view returns (string[] memory) {
        return touristIds;
    }
}
