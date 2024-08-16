import os
import sys
print(sys.version)
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.script import CScriptOp
from blockchain_parser.utils import *


OP_HASH160 = CScriptOp(0xa9)
csv_path = "/Volumes/HKU_drive/HKU/2023_witnessunknown"
blocks_path = '/Volumes/HKU_drive/HKU/Bitcoin_core/blocks'
blockchain = Blockchain(os.path.expanduser(blocks_path))
blocks = blockchain.get_ordered_blocks(
        os.path.expanduser(blocks_path + '/index'),
        # start=783940,
        start=717015,
        end=717016
        # end=823785
        )

for block in blocks:
    for index, transaction in enumerate(block.transactions):
        if transaction.is_segwit:
            print(transaction.inputs[0].script.value)
