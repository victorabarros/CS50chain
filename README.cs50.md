# CS50chain
#### Video Demo:  https://youtu.be/ukvqLZFYixw
#### Description:

The CS50chain is my CS50 final project.
It was inspired by the bitcoin blockchain technology.
So here you'll find a simplified blockchain applying the most important concepts involved in this subject.

You can see details about [Blockchain here](https://www.investopedia.com/terms/b/blockchain.asp), but below has a brief introduction.

Blockchain is a decentralized way to save data. In our case, as bitcoin works, the data is financial transactions.

A blockchain is a collection of blocks of data. Details of my abstraction [here](./app/block.py).
The entity responsible for add new blocks to the blockchain is called node.
The API in itself is an abstraction of a node and it's a node from the blockchain network. Tt has its own blockchain data cloned that warranty the decentralized of the blockchain and it calls other nodes to make themselves sync every time is necessary add a new block.
In [my node class](./app/node.py) you can see the properties and methods.

The node aggregates transactions and after a few minutes it will start a process called mining where it'll calculate the nonce of the previous block based on the Proof of Work algorithm ([here](./app/block.py)).
Once nonce is calculated, this node is authorized to submit a new block to the blockchain.

For a user to be able to submit transactions to the node first is necessary to create their wallet. The wallet is defined basically as a pair of RSA256 keys, aka public and private keys.
The public key is the wallet address where other users can deposit money and the private key is used to sign withdrawals.
It's possible see the wallet class [here](./app/wallet.py) and the transaction class [here](./app/transaction.py).
Beyond these properties, the wallet class is responsible for processing transactions from the blockchain to calculate the wallet's balance and statement.

how to run:
First is necessary to install dependencies, so run pip3 install -r requirements.txt .
After that just run python3 app.py and open the browser on the localhost:5000.
At the Blockchain tab you can find the block table.
At Node tab you'll find current pending transactions, waiting to be mined and the address of other nodes to sync.
You can create a new wallet with public and private keys at the Create a Wallet tab.
After that, you can see a $1000 transaction pending to your wallet on the node tab. Is necessary to mine the current block to add this transaction to the blockchain.
At wallet tab you can see the transactions that you've made and the ones that you've received.
At the transaction tab you can create new transactions.

data persistance:
Is possible persist database on sqlite, just create the database.db file and execute the following commands.
CREATE TABLE blockchain ( id INTEGER PRIMARY KEY, data TEXT NULL, hash TEXT NOT NULL, nonce INTEGER NULL, created_at TIMESTAMP NOT NULL );
INSERT INTO blockchain ( id, data, hash, nonce, created_at ) VALUES ( 0, '{"transactions": []}', '8f829e9831c36d9e6c1140252048c749ff29bfff1ec7bb38bc3a18d356e504a2', null, '2022-06-12T04:49:16.425598' );

api:
- GET /api/node
  - get current node transactions and other node addresses
- POST /api/node/address
  - add new node address
- DELETE /api/node/transactions
  - clear node transactions
- POST /api/node/mine
  - mine block, aka sync transaction with other nodes, calculate nonce (proof of work), and create a new block to the blockchain
- GET /api/chain
  - get blockchain
- POST /api/chain
  - sync current node with other blockchain and transactions
- POST /api/wallet
  - create new wallet
- POST /api/search/wallet
  - wallet search
- POST /api/transaction
  - submit transaction to node

See more details, like data persistence, unit tests and more access https://github.com/victorabarros/CS50chain#this-is-cs50chain
