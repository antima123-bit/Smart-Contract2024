import json
import os
import hashlib
import requests
import base64
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from sawtooth_sdk.protobuf.batch_pb2 import Batch, BatchHeader, BatchList
import time
import pickle
import sys
import argparse
import subprocess


NAMESPACE = hashlib.sha512('Ecommerce'.encode('utf-8')).hexdigest()[0:6]
URL='http://rest-api:8008'

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

def _get_keyfile(customer_name):
    '''Get the private key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    key_file = '{}/{}.priv'.format(key_dir, customer_name)

    if not os.path.exists(key_file):
        return None
    return key_file


def create_product(reg_no, det, owner, private_key, url):
    # Prepare the transaction payload
    payload = {
        'operation':'create',
        'reg_no': reg_no,
        'det': det,
        'owner': owner,
        'price': -1,
        'private_key':_hash(private_key.encode('utf-8'))[0:64],
        'hash_value':None,
        'destination_owner':None,
        'time_limit':0,
        'lock_status':False
    }

    if get_product(reg_no,url) is not None:
            print(f"Registry no. {reg_no} already exists for owner {owner}")

    else:
        client_file=_get_keyfile(private_key)
        if client_file is None:
            print("User is not existed in the blockchain network,please generate private and public keys")
            return
        file_temp= open(_get_keyfile(private_key))
        privateKeyStr= file_temp.read().strip()
        privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
        signer = CryptoFactory(create_context('secp256k1')) \
                .new_signer(privateKey)
        publicKey = signer.get_public_key().as_hex()

        file_temp= open(_get_keyfile("client"))
        #file_temp= open(_get_keyfile(owner))
        privateKeyStr= file_temp.read().strip()
        private_temp = Secp256k1PrivateKey.from_hex(privateKeyStr)
        signer_temp = CryptoFactory(create_context('secp256k1')) \
                .new_signer(private_temp)
        publicKey_temp = signer_temp.get_public_key().as_hex()


        transaction_id=None
        transaction_header = create_transaction_header(publicKey, payload)
        signer_public_key=signer_public_key,
        family_name ='Ecommerce',
        family_version='1.0',
        inputs=[NAMESPACE],
        outputs=[NAMESPACE],
        dependencies=[],
        payload_sha512=hashlib.sha512(json.dumps(payload).encode()).hexdigest(),
        batcher_public_key=signer_public_key,
        nonce=''.SerializeToString()

        transaction = create_transaction(transaction_header, payload, signer)
        header=transaction_header,
        payload=json.dumps(payload).encode(),
        header_signature=signer.sign(transaction_header)

        batch = create_batch(transaction, signer_temp)
        header=batch_header,
        transactions=[transaction],
        header_signature=signer.sign(batch_header)


        batch_list = BatchList(batches=[batch])

        batch_list_bytes = batch_list.SerializeToString()
        #batch_signature = signer_temp.sign(batch_list_bytes)
        #batch.header_signature = batch_signature
        # Update the batch header signature

        # Submit the batch to the validator
        #print("batcher_publickey:",publicKey_temp)
        #print("transaction details:",transaction)
        print("Product Registered successfully in Ecommerce")
        print("Transaction_Header id:",transaction.header_signature)
        submit_batch(url, batch_list_bytes)


def buyPrice_product(reg_no, price,new_owner, private_key, url):
    # Prepare the transaction payload
    payload = {
        'operation':'buyPrice',
        'reg_no': reg_no,
        'new_owner': new_owner,
        'price':price,
        'private_key':private_key
    }
    product = get_product(reg_no, URL)
    print("product details:",product)
    if product['price']==-1:
         print("product price is not set by the owner")
         return
    if product['price']>price:
        print("Price not met")
        return
    print(f"product being transafered successfully to {new_owner}")
    reg_no=_hash(reg_no.encode('utf-8'))[0:64]
    file_temp= open(_get_keyfile(private_key))
    privateKeyStr= file_temp.read().strip()
    privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(privateKey)
    publicKey = signer.get_public_key().as_hex()

    file_temp= open(_get_keyfile("client"))
    #file_temp= open(_get_keyfile(new_owner))
    privateKeyStr= file_temp.read().strip()
    private_temp = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer_temp = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_temp)
    publicKey_temp = signer_temp.get_public_key().as_hex()

    # Create a transaction header
    transaction_header = TransactionHeader(
        signer_public_key=publicKey,
        family_name='product',
        family_version='1.0',
        inputs=[NAMESPACE + reg_no],
        outputs=[NAMESPACE + reg_no],
        dependencies=[],
        payload_sha512=hashlib.sha512(json.dumps(payload).encode()).hexdigest(),
        batcher_public_key=publicKey_temp,
        nonce='').SerializeToString()

    # Create a transaction
    transaction = Transaction(
        header=transaction_header,
        payload=json.dumps(payload).encode(),
        header_signature=signer.sign(transaction_header))

    # Create a batch header
    batch_header = BatchHeader(
        signer_public_key=publicKey_temp,
        transaction_ids=[transaction.header_signature]).SerializeToString()

    # Create a batch
    batch = Batch(
        header=batch_header,
        transactions=[transaction],
        header_signature=signer_temp.sign(batch_header))


    batch_list = BatchList(batches=[batch])


    batch_list_bytes = batch_list.SerializeToString()
    #batch_signature = signer_temp.sign(batch_list_bytes)
    #batch.header_signature = batch_signature
    # Update the batch header signature


    # Submit the batch to the validator
    #print(NAMESPACE + reg_no)
    submit_batch(url, batch_list_bytes)


def LockAsset_product(reg_no, owner, private_key,destination_owner, hash_value,time_limit,url):
    # Prepare the transaction payload
    payload = {
        'operation':'LockAsset',
        'reg_no': reg_no,
        'owner': owner,
        'private_key':_hash(private_key.encode('utf-8'))[0:64],
        'destination_owner':destination_owner,
        'hash_value':_hash(hash_value.encode('utf-8'))[0:64],
        'time_limit':time_limit,
    }
    product = get_product(reg_no, URL)
    #print("product details:",product)

    if product is None:
        print("product not found")
        return
    if product['private_key']!=_hash(private_key.encode('utf-8'))[0:64]:
         print("Unauthorized Access")
         return
    print(f"product being locked successfully by {owner}")
    reg_no=_hash(reg_no.encode('utf-8'))[0:64]
    file_temp= open(_get_keyfile(private_key))
    privateKeyStr= file_temp.read().strip()
    privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(privateKey)
    publicKey = signer.get_public_key().as_hex()

    file_temp= open(_get_keyfile("client"))
    #file_temp= open(_get_keyfile(new_owner))
    privateKeyStr= file_temp.read().strip()
    private_temp = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer_temp = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_temp)
    publicKey_temp = signer_temp.get_public_key().as_hex()

    # Create a transaction header
    transaction_header = TransactionHeader(
        signer_public_key=publicKey,
        family_name='product',
        family_version='1.0',
        inputs=[NAMESPACE + reg_no],
        outputs=[NAMESPACE + reg_no],
        dependencies=[],
        payload_sha512=hashlib.sha512(json.dumps(payload).encode()).hexdigest(),
        batcher_public_key=publicKey_temp,
        nonce='').SerializeToString()

    # Create a transaction
    transaction = Transaction(
        header=transaction_header,
        payload=json.dumps(payload).encode(),
        header_signature=signer.sign(transaction_header))

    # Create a batch header
    batch_header = BatchHeader(
        signer_public_key=publicKey_temp,
        transaction_ids=[transaction.header_signature]).SerializeToString()

    # Create a batch
    batch = Batch(
        header=batch_header,
        transactions=[transaction],
        header_signature=signer_temp.sign(batch_header))


    batch_list = BatchList(batches=[batch])


    batch_list_bytes = batch_list.SerializeToString()
    #batch_signature = signer_temp.sign(batch_list_bytes)
    #batch.header_signature = batch
    submit_batch(url, batch_list_bytes)


def ClaimAsset_product(reg_no, new_owner, private_key, secret_key,url):
    # Prepare the transaction payload
    payload = {
        'operation':'ClaimAsset',
        'reg_no': reg_no,
        'new_owner': new_owner,
        'private_key':_hash(private_key.encode('utf-8'))[0:64],
        'secret_key':_hash(secret_key.encode('utf-8'))[0:64],
    }
    product = get_product(reg_no, URL)
    if product is None:
         print("product not found")
         return
    print("Request sent to Validator for Claiming the Asset,check the status by getDetails function")
    reg_no=_hash(reg_no.encode('utf-8'))[0:64]
    file_temp= open(_get_keyfile(private_key))
    privateKeyStr= file_temp.read().strip()
    privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(privateKey)
    publicKey = signer.get_public_key().as_hex()

    file_temp= open(_get_keyfile("client"))
    #file_temp= open(_get_keyfile(new_owner))
    privateKeyStr= file_temp.read().strip()
    private_temp = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer_temp = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_temp)
    publicKey_temp = signer_temp.get_public_key().as_hex()

    # Create a transaction header
    transaction_header = TransactionHeader(
        signer_public_key=publicKey,
        family_name='product',
        family_version='1.0',
        inputs=[NAMESPACE + reg_no],
        outputs=[NAMESPACE + reg_no],
        dependencies=[],
        payload_sha512=hashlib.sha512(json.dumps(payload).encode()).hexdigest(),
        batcher_public_key=publicKey_temp,
        nonce='').SerializeToString()

    # Create a transaction
    transaction = Transaction(
        header=transaction_header,
        payload=json.dumps(payload).encode(),
        header_signature=signer.sign(transaction_header))

    # Create a batch header
    batch_header = BatchHeader(
        signer_public_key=publicKey_temp,
        transaction_ids=[transaction.header_signature]).SerializeToString()

    # Create a batch
    batch = Batch(
        header=batch_header,
        transactions=[transaction],
        header_signature=signer_temp.sign(batch_header))


    batch_list = BatchList(batches=[batch])


    batch_list_bytes = batch_list.SerializeToString()
    submit_batch(url, batch_list_bytes)


def RefundAsset_product(reg_no, new_owner, private_key,secret_key,url):
    # Prepare the transaction payload
    payload = {
        'operation':'RefundAsset',
        'reg_no': reg_no,
        'new_owner': new_owner,
        'private_key':_hash(private_key.encode('utf-8'))[0:64],
        'secret_key':_hash(secret_key.encode('utf-8'))[0:64],
    }
    product = get_product(reg_no, URL)
    if product is None:
         print("product not found")
         return
    print("Request sent to Validator for Refunding the Asset,check the status by getDetails function")
    reg_no=_hash(reg_no.encode('utf-8'))[0:64]
    file_temp= open(_get_keyfile(private_key))
    privateKeyStr= file_temp.read().strip()
    privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(privateKey)
    publicKey = signer.get_public_key().as_hex()

    file_temp= open(_get_keyfile("client"))
    #file_temp= open(_get_keyfile(new_owner))
    privateKeyStr= file_temp.read().strip()
    private_temp = Secp256k1PrivateKey.from_hex(privateKeyStr)
    signer_temp = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_temp)
    publicKey_temp = signer_temp.get_public_key().as_hex()

    # Create a transaction header
    transaction_header = TransactionHeader(
        signer_public_key=publicKey,
        family_name='product',
        family_version='1.0',
        inputs=[NAMESPACE + reg_no],
        outputs=[NAMESPACE + reg_no],
        dependencies=[],
        payload_sha512=hashlib.sha512(json.dumps(payload).encode()).hexdigest(),
        batcher_public_key=publicKey_temp,
        nonce='').SerializeToString()

    # Create a transaction
    transaction = Transaction(
        header=transaction_header,
        payload=json.dumps(payload).encode(),
        header_signature=signer.sign(transaction_header))

    # Create a batch header
    batch_header = BatchHeader(
        signer_public_key=publicKey_temp,
        transaction_ids=[transaction.header_signature]).SerializeToString()

    # Create a batch
    batch = Batch(
        header=batch_header,
        transactions=[transaction],
        header_signature=signer_temp.sign(batch_header))


    batch_list = BatchList(batches=[batch])


    batch_list_bytes = batch_list.SerializeToString()
    submit_batch(url, batch_list_bytes)





# Get transaction details
def get_transaction_details(transaction_id, url):
    response = requests.get(f'{url}/transactions/{transaction_id}')
    data = response.json()

    if 'data' in data:
        # Decode the base64 encoded payload
        payload = base64.b64decode(data['data']['payload']).decode('utf-8')
        # Load the payload as JSON
        payload = json.loads(payload)
        return payload
    else:
        return None



#########My code ends####################


def get_product(reg_no, url):
    reg_no=_hash(reg_no.encode('utf-8'))[0:64]
    response = requests.get(f'{url}/state/{NAMESPACE}{reg_no}')
    data = response.json()

    if 'data' in data:
        state_data = base64.b64decode(data['data']).decode()
        #print(json.loads(state_data))
        return json.loads(state_data)
    else:
        return None


def submit_batch(url, batch_list_bytes):
    headers = {'Content-Type': 'application/octet-stream'}
    data=batch_list_bytes
    url='http://rest-api:8008/batches'
    try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))
    except requests.ConnectionError as err:
            raise Exception('Failed to connect to {}: {}'.format(url, str(err)))
    except BaseException as err:
            raise Exception(err)

import argparse
def main():
    parser = argparse.ArgumentParser(description='product Client')
    parser.add_argument('action', choices=['register', 'setPrice','buyPrice', 'getDetails','LockAsset','ClaimAsset','RefundAsset','getByTxnId'], help='LandRegistry action')
    parser.add_argument('--reg-no', help='registry no.')
    parser.add_argument('--det', help='product details no.')
    parser.add_argument('--owner', help='Owner')
    parser.add_argument('--new-owner', help='New owner')
    parser.add_argument('--private-key', help='Private key')
    parser.add_argument('--destination-owner', help='Destination owner')
    parser.add_argument('--secret-key', help='Secret key')
    parser.add_argument('--hash-value', help='Hash value')
    parser.add_argument('--time-limit', help='Time limit for the transaction')
    parser.add_argument('--price',help='Buy/Sell at price')
    parser.add_argument('--transaction-id', help='Transaction ID')
    parser.add_argument('--url', default='http://rest-api:8008', help='Sawtooth REST API URL')

    args = parser.parse_args()
    if args.action == 'register':
        if args.owner == 'qwerty': # args.owner
            create_product(args.reg_no, args.det, args.owner, args.private_key, args.url)
        else:
            print("Need owner approval")
            print("Do not have access to register new products")
    elif args.action == 'setPrice':

        setPrice_product(args.reg_no, args.price,args.owner, args.private_key, args.url)
    elif args.action == 'buyPrice':
        buyPrice_product(args.reg_no, args.price,args.new_owner, args.private_key, args.url)
    elif args.action == 'getDetails':
        product = get_product(args.reg_no, args.url)
        if product:
            #print(f"comple details in json form: {product}")
            print("product num: ",product['reg_no'])
            print("Owner: ",product['owner'])
            print("Land Details: ",product['det'])
            print("Price: ",product['price'])
        else:
            print("product not found.")
            print("check registration num proporly")
    ### my functions starts

    elif args.action == 'LockAsset':

        LockAsset_product(args.reg_no, args.owner,args.private_key,args.destination_owner,args.hash_value,args.time_limit,args.url)

    elif args.action == 'ClaimAsset':

        ClaimAsset_product(args.reg_no, args.new_owner,args.private_key,args.secret_key,args.url)
    elif args.action == 'RefundAsset':

        RefundAsset_product(args.reg_no, args.new_owner, args.private_key,args.secret_key,args.url)


    elif args.action == 'getByTxnId':
        transaction = get_transaction_details(args.transaction_id, args.url)
        if transaction:
            print(transaction)
        else:
            print("No transaction found for the given transaction ID.")


    ### my functions ends





if __name__ == '__main__':
    #print("Hello")
    main()
