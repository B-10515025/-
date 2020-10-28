pragma solidity >=0.7.0;

contract Private {
    string private flag;

    constructor (string memory _flag) {
        flag = _flag;
    }
}