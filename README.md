# Blockchain POC - CS50 2022 Final Project

<!--
#### Video Demo:  <URL HERE>
<present your project to the world, as with slides, screenshots, voiceover, and/or live action. Your video should somehow include your project’s title, your name, your city and country, and any other details that you’d like to convey to viewers>

#### Description:
<several hundred words that describe things in detail>
<explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them>
<If it is too short, the system will reject it>
https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md
-->

<!--
##requirements:
- front: html, css and bootstrap
- back: python, flask, jinja
- sqlite3 (use amazon s3 for sqlite server https://www.sqlite.org/serverless.html)
## how to run
## concepts
Blockchain > _blockchain is a distributed database that allows direct transactions between two parties without the need of a central authority_
Hash > it's one side only algo. must popular is SHA256
Public Key Cryptography > authentication, where the public key verifies a holder of the paired. must popular RSA
Consensus > ""
## host
- https://pages.github.com/
- https://www.heroku.com/

-->
## entities

- Wallet
  - created_at
  - private_key PK*
  - public_key
  - email
  - balance*
- Transaction
  - created_at
  - sender_wallet_public_key
  - recipe_wallet_public_key
  - description
  - amount
  - sign PK
- Block
  - created_at
  - node_id PK
  - data ({ transactions: List[Transaction], ... })
  - hash PK
  - nonce
- Node*
  - transactions
  - id PK
  - url

*must not be save on db

## references

- http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/ https://github.com/adilmoujahid/blockchain-python-tutorial/
- https://arxiv.org/abs/1810.06130
- https://bitcoin.org/bitcoin.pdf
- https://github.com/khaosdoctor/typescript-blockchain
- https://mycoralhealth.medium.com/code-your-own-blockchain-in-less-than-200-lines-of-go-e296282bcffc
- https://medium.com/@vanflymen/learn-blockchains-by-building-one-117428612f46
