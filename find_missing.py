import os
import csv
from blockchain_parser.blockchain import Blockchain


csv_path = "/Volumes/HKU_drive/HKU/2023_win_process_1"
csv_out_path = "/Volumes/HKU_drive/HKU/2023_win_process_1_out"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=783940,
        start=780939,
        end=783903
        # end=823785
        )

for block in blocks:
    cur_height = block.height
    print(f"Processing block {cur_height}")
    print("======================\n")
    print(f"BLOCK: {cur_height}\n")
    print("======================\n")
    try:
        with open(csv_path+f"/{cur_height}.csv", newline='') as csvfile:
            tx_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            target_hashes = []
            for tx_hash in tx_reader:
                if tx_hash[0] == "Txid":
                    continue
                target_hashes.append([tx_hash[0]])
                # Target hashes contains all txhash to look for in the current csv

        # Find all output address of target hashes
        counter = 0
        for index, transaction in enumerate(block.transactions):
            if len(target_hashes) == counter:
                break
            if target_hashes[counter][0] == str(transaction.txid):
                counter += 1
                # Append outputs to target_hashes
                for output in transaction.outputs:
                    if len(output.addresses) == 0:
                        target_hashes[counter-1].append("NOT_FOUND")
                    elif len(output.addresses) == 1:
                        target_hashes[counter-1].append(output.addresses[0].address)
                    else:
                        # Multisig address
                        multisig = "multisig("
                        for ad in output.addresses:
                            multisig += ad.address
                        multisig += ")"

        with open(csv_out_path+f"/{cur_height}_out.csv", 'w+', newline='') as csvfile:
            tx_writer = csv.writer(csvfile, delimiter=',', quotechar='|')
            for i in target_hashes:
                tx_writer.writerow(i)

    except FileNotFoundError:
        print(f"WARNING: {cur_height}.csv not found\n")
