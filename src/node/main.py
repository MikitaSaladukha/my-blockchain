from flask import Flask, request

from common.initialize_blockchain import blockchain
from node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from node.transaction_validation.transaction_validation import Transaction, TransactionException

app = Flask(__name__)

blockchain_base = blockchain()


@app.route("/block", methods=['POST'])
def validate_block():
    content = request.json
    try:
        new_block = NewBlock(blockchain_base)
        new_block.receive(new_block=content["block"])
        new_block.validate()
        new_block.add()
    except (NewBlockException, TransactionException) as new_block_exception:
        return f'{new_block_exception}', 400
    return "Transaction success", 200


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    try:
        transaction_validation = Transaction(blockchain_base)
        transaction_validation.receive(transaction=content["transaction"])
        transaction_validation.validate()
        transaction_validation.validate_funds()
        transaction_validation.broadcast()
        transaction_validation.store()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200