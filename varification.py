import os
from hashmap import HashTable
from blockchain_parser.blockchain import Blockchain


csv_path = "/Volumes/HKU_drive/HKU/2023_witnessunknown"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
log_path = "/Volumes/HKU_drive/2023_reuse_project/2023log.txt"
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        start=100410,
        end=160037,
        # end=769788,
        )

print("initialising hashtable")
t = HashTable(5000000)
reuse_no = 0
total_added = 0
total_seen = 0
total_multisig = 0

for block_i, block in enumerate(blocks):
    print("================================")
    print(f"Processing block {block.height}")
    no_txs = len(block.transactions)
    print("enumerating block transactions")
    for index, transaction in enumerate(block.transactions):

        # Show progress per 500 transaction
        if index % 500 == 0:
            print(f"{index} / {no_txs}")

        print("processing transaction")
        # Produce a set of output addresses use per transaction
        cur_tx_output_set = []
        for output in transaction.outputs:
            if len(output.addresses) == 1:
                cur_tx_output_set.append(output.addresses[0].address)
            elif len(output.addresses) > 1:
                total_multisig += 1
                cur_tx_output_set.append(
                        "multisig("+(", ".join(list(map(lambda x: x.address, output.addresses))))+")"
                        )
                print("================================================================")
        cur_tx_output_set = set(cur_tx_output_set)

        # Add each transaction to the BST, if already exsit, BST will increment it's occurence
        for out_str in cur_tx_output_set:
            print("================================")
            print(f"Processing block {block.height}")
            print(f"{index} / {no_txs}")
            print(total_multisig)
            print(out_str)
            t.add(out_str)

    # Produce outputs
    if block_i % 15000 == 0:
        datas = t.analyse()
        print(datas)


print(t.analyse())
# t.store_tree('/Volumes/HKU_drive/2023_reuse_project/2023_reuse_final.csv')
