import os
import csv
from blockchain_parser.blockchain import Blockchain
import requests
import json


csv_path = "/Volumes/HKU_drive/HKU/2023_witnessunknown"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=783940,
        start=367319,
        end=367320
        # end=823785
        )
out_file = "out2.txt"


def get_outs_api(hash):

    x = requests.get(f'https://blockchain.info/rawtx/{hash}')
    x = x.text
    y = json.loads(x)

    result = []
    for out in y["out"]:
        if "addr" in out:
            result.append(out["addr"])
        else:
            result.append(None)
    return result


def test_txs(target_hashes, block, f):
    counter = 0
    for index, transaction in enumerate(block.transactions):
        if len(target_hashes) == counter:
            break
        if target_hashes[counter] == str(transaction.txid):
            counter += 1
            result = "PASSED"
            f.write(f"tx_hash: {transaction.txid}\n")
            f.write("output addresses:\n")

            outputs = []
            # Test for address found and build output list
            for output in transaction.outputs:
                if len(output.addresses) == 0:
                    result = "FAILED"
                    f.write("    - Address not found\n")
                    outputs.append(None)
                else:
                    if len(output.addresses)>1:
                        f.write("    - multisig(")
                        f.write(", ".join(list(map(lambda x: x.address, output.addresses))))
                        f.write(")\n")
                    else:
                        f.write(f"    - {output.addresses[0].address}\n")
                    outputs.append(output.addresses[0].address)
            f.write(f"test all address found: {result}\n")

            # # Test if address is correct against api
            # api_outs = get_outs_api(str(transaction.txid))
            # # f.write(f"{api_outs}\n")
            # # f.write(f"{outputs}\n")
            # if api_outs == outputs:
            #     f.write("test correct output: PASSED\n\n")
            # else:
            #     f.write("test correct output: FAILED\n\n")


f = open(out_file, "a")
for block in blocks:
    cur_height = block.height
    print(f"Processing block {cur_height}")
    f.write("======================\n")
    f.write(f"BLOCK: {cur_height}\n")
    f.write("======================\n")
    try:
        with open(csv_path+f"/{cur_height}.csv", newline='') as csvfile:
            tx_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            target_hashes = []
            for tx_hash in tx_reader:
                if tx_hash[0] == "Txid":
                    continue
                target_hashes.append(tx_hash[0])
            test_txs(target_hashes, block, f)
    except FileNotFoundError:
        f.write(f"WARNING: {cur_height}.csv not found\n")
f.close()
