import csv
from blockchain_parser.blockchain import Blockchain
import os

csv_folder_path = "/Volumes/HKU_drive/output_address/2023/"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=164467,
        # end=164468,
        start=716599,
        end=769787,
        # end=769788,
        )
for block in blocks:
    print(f"processing block {block.height}")
    csv_path = csv_folder_path + "block" + str(block.height) + "addr.csv"
    with open(csv_path, 'w+', newline='') as csvfile:
        tx_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        tx_writer.writerow(["Block Height", "Txid", "Output Addresses"])
        for index, transaction in enumerate(block.transactions):
            output = []
            for i in transaction.outputs:
                if len(i.addresses) == 1:
                    output.append(i.addresses[0].address)
                elif len(i.addresses) > 1:
                    output.append(
                            "multisig("+(", ".join(list(map(lambda x: x.address, i.addresses))))+")"
                            )

            tx_writer.writerow([block.height, transaction.txid, ",".join(set(output))])
