# CS50chain
#### Video Demo:  https://youtu.be/hocXsAqws4o
#### Description:

The CS50chain is my CS50 final project.
It was inspired by the bitcoin blockchain technology, that's not a topic that I domain 100%, but this was a chance to be more familiar with it.
So here you'll find a simplified blockchain applying the most important concepts involved in this subject.

You can see details about [Blockchain here](https://www.investopedia.com/terms/b/blockchain.asp), but below has a brief introduction.

Blockchain is a decentralized way to save data. In our case, as bitcoin works, the data is financial transactions.

A blockchain is a collection of blocks of data. Details of my abstraction [here](./app/block.py).
How responsible to add new blocks to the blockchain is the node.
The API in itself is an abstraction to a node, it has its own blockchain data cloned that warranty the decentralized of the blockchain and it calls other nodes to make themselves updates. In [my node class](./app/node.py) you can see the properties and methods.

The node aggregates transactions and after a few minutes it will start a process called mining where it'll calculate the nonce of the previous block based on the Proof of Work algorithm ([here](./app/block.py)). Once nonce is calculated, this node is authorized to submit a new block to the blockchain.

For a user to be able to submit transactions to the node first is necessary to create their wallet. The wallet is defined basically as a pair of RSA256 keys, aka public and private keys. The public key is the wallet address where other users can deposit money and the private key is used to sign withdrawals. It's possible see the wallet class [here](./app/wallet.py) and the transaction class [here](./app/transaction.py). Beyond these properties, the wallet class is responsible for processing transactions from the blockchain to calculate the wallet's balance and statement.

See more details, like data persistence, unit tests and more access https://github.com/victorabarros/CS50chain#this-is-cs50chain
