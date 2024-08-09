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
        if transaction.txid == "69b3e5c18247e3e0cf25a5c0a85268d1b71111c23e7c00c9a545ada2f28033c1":
            print(transaction.txid)
            for inp in transaction.inputs:
                print(format_hash(inp.hex))
                print(len(inp.script.script))
                print(inp.script.script)
                print(inp.script.script[0])
                print(inp.script.script[1])
                print(inp.script.script[2])
                print(inp.script.is_p2sh())
