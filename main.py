from web3 import Web3
import time

# Ethereum RPC endpoint
rpc_url = "https://base.llamarpc.com"
# Chain ID
chain_id = 8453
# Smart contract address
contract_address = "0x597774837debe9f074453c04cea46b532759b28a" #dont touch
# Hex data template
hex_data_template = "0x70e6c1e3000000000000000000000000(tut paste address tega which you want to send but without 0x (if you wan to send your own tags just paste your address and delete 0x))000000000000000000000000{address}0000000000000000000000000000000000000000000000000000000000000001"

# Read addresses 
with open("wallets.txt", "r") as file:
    addresses = [line.strip() for line in file]

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider(rpc_url))
web3.eth.chainId = chain_id

# Your private key to sign the transaction
private_key = "your private key 123 5 aaaaaaaaaaa "

# Maximum number of retries
max_retries = 3

# Iterate through addresses and make function call
for address in addresses:
    for attempt in range(max_retries):
        try:
            # Construct hex data with the current address
            hex_data = hex_data_template.format(address=address)
            nonce = web3.eth.get_transaction_count("SENDER ADDRESS", 'pending')  # replace "SENDER_ADDRESS" with your sender's address
            checksum_contract_address = web3.to_checksum_address(contract_address)

            # Build the transaction
            transaction = {
                'to': checksum_contract_address,
                'data': hex_data,
                'gas': 200000,  # Adjust the gas limit accordingly#dont touch
                'gasPrice': 222,  # Adjust the gas price accordingly #dont touch
                'nonce': nonce,
                'chainId': 8453,
            }

            # Sign the transaction
            signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

            # Send the transaction
            transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

            print(f"Transaction sent: {transaction_hash.hex()}")
            break  # Break out of the retry loop if successful

        except ValueError as ve:
            # Handle specific exception (e.g., underpriced, nonce too low)
            print(f"Error: {ve}")
            time.sleep(5)  # Wait for a moment before retrying

        except Exception as e:
            # Handle other exceptions
            print(f"Unexpected error: {e}")
            break  # Break out of the retry loop

    else:
        print(f"Failed to send transaction after {max_retries} attempts for address: {address}")
