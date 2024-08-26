import csv
from blockchain_parser.blockchain import Blockchain
import os
import ast

csv_file_path = "/Users/maverickchow/Downloads/2021_WitnessUnknownScript.csv"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=610691,
        # end=663913,
        start=690047,
        end=716599,
        )
p2trs=[]
others=[]
with open(csv_file_path, 'r', newline='') as csvfile:
    tx_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(tx_reader)
    target_row = next(tx_reader)
    target_tx_index = ast.literal_eval(target_row[1])
    print(target_tx_index)
    for block in blocks:
        for index, transaction in enumerate(block.transactions):
            if transaction.txid == target_row[0]:
                print(target_row[0])
                for i in target_tx_index:
                    if transaction.outputs[i].type == "p2tr":
                        p2trs.append((transaction.txid, i))
                        print(p2trs[-1])
                    else:
                        others.append((transaction.txid, i))
                target_row = next(tx_reader, "end")
                if target_row == "end":
                    with open("/Users/maverickchow/Desktop/out2021.txt", "w+") as f:
                        f.write("p2tr: ")
                        f.write(str(len(p2trs)))
                        f.write("\n")
                        f.write("not p2tr: ")
                        f.write(str(len(others)))
                        f.write("\n")
                        f.write("p2tr\n")
                        for i in p2trs:
                            f.write(str(i))
                            f.write("\n")
                        f.write("not p2tr\n")
                        for i in others:
                            f.write(str(i))
                            f.write("\n")
                    exit()
                target_tx_index = ast.literal_eval(target_row[1])

