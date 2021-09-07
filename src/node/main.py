from flask import Flask, request, jsonify

from common.initialize_blockchain import initialize_blockchain
from common.io_blockchain import get_blockchain_from_memory
from node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from node.transaction_validation.transaction_validation import Transaction, TransactionException

import time
import json


from datetime import datetime
from blockchain_users.albert import private_key as albert_private_key
from blockchain_users.bertrand import private_key as bertrand_private_key
from blockchain_users.camille import private_key as camille_private_key
from common.block import Block, BlockHeader
from common.io_blockchain import store_blockchain_in_memory
from common.merkle_tree import get_merkle_root
from common.transaction import Transaction
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from wallet.wallet import Owner


app = Flask(__name__)
initialize_blockchain()
##
albert_wallet = Owner(private_key=albert_private_key)
bertrand_wallet = Owner(private_key=bertrand_private_key)
camille_wallet = Owner(private_key=camille_private_key)

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

#####add block
@app.route("/add_block1", methods=['GET'])
def add_block1():
    print("MikkiTA add block camille start") 
    start = time.time()   
    block_1 = get_blockchain_from_memory()
    ##timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    ##now=datetime.now.strftime("%Y-%m-%d %H:%M:%S.%f")
    timestamp_2=datetime.now().isoformat()
    ##timestamp_2 = datetime.timestamp(datetime.fromisoformat(now))
    ##timestamp_2 = datetime.now
        
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"], output_index=0) 
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash, amount=1)
    transaction_2 = Transaction([input_0], [output_0])
    
    block_header_2 = BlockHeader(
        previous_block_hash=block_1.block_header.hash,
        timestamp=timestamp_2,
        noonce=block_1.block_header.noonce+1,
        merkle_root=get_merkle_root([transaction_2.transaction_data])
    )
    block_2 = Block(
        transactions=[transaction_2.transaction_data],
        block_header=block_header_2,
        previous_block=block_1,
    )
    store_blockchain_in_memory(block_2)
    print("MikkiTA add block camille end") 
    end = time.time()
    print("MikkiTA camille add end. time: ",end - start," seconds")  
    return jsonify(block_2.to_dict)
######################################################################    

@app.route("/add_block2", methods=['GET'])
def add_block2():
    print("MikkiTA add block bertrand start")  
    start = time.time()  
    block_1 = get_blockchain_from_memory()
    ##timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    ##now=datetime.now.strftime("%Y-%m-%d %H:%M:%S.%f")
    timestamp_2=datetime.now().isoformat()
    ##timestamp_2 = datetime.timestamp(datetime.fromisoformat(now))
    ##timestamp_2 = datetime.now
        
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"], output_index=0) 
    output_0 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash, amount=1)
    transaction_2 = Transaction([input_0], [output_0])
    
    block_header_2 = BlockHeader(
        previous_block_hash=block_1.block_header.hash,
        timestamp=timestamp_2,
        noonce=block_1.block_header.noonce+1,
        merkle_root=get_merkle_root([transaction_2.transaction_data])
    )
    block_2 = Block(
        transactions=[transaction_2.transaction_data],
        block_header=block_header_2,
        previous_block=block_1,
    )
    store_blockchain_in_memory(block_2)
    print("MikkiTA add block bertrand end") 
    end = time.time()
    print("MikkiTA bertrand add end. time: ",end - start," seconds")
    return jsonify(block_2.to_dict)

@app.route("/add_block3", methods=['GET'])
def add_block3():
    print("MikkiTA add block albert start")  
    start = time.time()   
    block_1 = get_blockchain_from_memory()
    ##timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    ##now=datetime.now.strftime("%Y-%m-%d %H:%M:%S.%f")
    timestamp_2=datetime.now().isoformat()
    ##timestamp_2 = datetime.timestamp(datetime.fromisoformat(now))
    ##timestamp_2 = datetime.now
        
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"], output_index=0) 
    output_0 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=1)
    transaction_2 = Transaction([input_0], [output_0])
    
    block_header_2 = BlockHeader(
        previous_block_hash=block_1.block_header.hash,
        timestamp=timestamp_2,
        noonce=block_1.block_header.noonce+1,
        merkle_root=get_merkle_root([transaction_2.transaction_data])
    )
    block_2 = Block(
        transactions=[transaction_2.transaction_data],
        block_header=block_header_2,
        previous_block=block_1,
    )
    store_blockchain_in_memory(block_2)
    print("MikkiTA add block albert end")
    end = time.time()
    print("MikkiTA albert add end. time: ",end - start," seconds") 
    return jsonify(block_2.to_dict)
