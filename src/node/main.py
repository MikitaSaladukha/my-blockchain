from flask import Flask, request, jsonify

from common.initialize_blockchain import initialize_blockchain
from common.io_blockchain import get_blockchain_from_memory
from node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from node.transaction_validation.transaction_validation import Transaction, TransactionException
from common.block import Block
import time

app = Flask(__name__)
initialize_blockchain()
##x=0

@app.route("/block", methods=['POST'])
def validate_block():
    content = request.json
    blockchain_base = get_blockchain_from_memory()
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
    blockchain_base = get_blockchain_from_memory()
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


@app.route("/block", methods=['GET'])
def get_blocks():
    print("Mikkita")
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/utxo/<user>", methods=['GET'])
def get_user_utxos(user):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_user_utxos(user))


@app.route("/transactions/<transaction_hash>", methods=['GET'])
def get_transaction(transaction_hash):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(transaction_hash))

###########################################################################


@app.route("/first_block", methods=['GET'])
def get_first_block():
    print("MikkiTA start")    
    blockchain_base = get_blockchain_from_memory()
    start = time.time()
    first=first_from_last(blockchain_base)
    end = time.time()
    print("MikkiTA end. time: ",end - start," seconds")   

    return jsonify(first.to_dict)

def first_from_last(block_object)-> Block:
    if block_object is None:
        print("error - None block")
        return None
    elif block_object.previous_block is None:
        print("first good")
        return block_object
    else:
        ##x=x+1
        ##print(x)
        print("iteration")
        return first_from_last(block_object.previous_block)
    
