import csv
from blockchain_parser.blockchain import Blockchain
import os

csv_folder_path = "/Volumes/HKU_drive/zip_files/2012/"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=164467,
        # end=164468,
        start=160037,
        end=214563,
        # end=769788,
        )


class error_ob:
    def __init__(self, message, expected, actual):
        self.message = message
        self.expected = expected
        self.actual = actual

    def show(self):
        print(self.message)
        print("expected: " + str(self.expected))
        print("actual: " + str(self.actual))


error_log = []
for block in blocks:
    csv_path = csv_folder_path + "block" + str(block.height) + "addr.csv"
    csv_address_for_curr_block = []
    with open(csv_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            if row[0] == "Block Height":
                continue
            if row[2] == '':
                csv_address_for_curr_block.append([])
                continue
            csv_address_for_curr_block.append(row[2].split(','))
    for index, transaction in enumerate(block.transactions):
        output = []
        for i in transaction.outputs:
            if len(i.addresses) == 1:
                output.append(i.addresses[0].address)
            elif len(i.addresses) > 1:
                output.append(
                        "multisig("+(", ".join(list(map(lambda x: x.address, i.addresses))))+")"
                        )
        if output != csv_address_for_curr_block[index]:
            message = "FAILED at block: " + str(block.height) + ", with transaction index: " + str(index) + ", and transaction hash: " + str(transaction.txid)
            error_log.append(error_ob(message, csv_address_for_curr_block[index], output))
            print(message)
        else:
            print(str(block.height) + " " + str(index) + " PASSED")

for i in error_log:
    i.show()
