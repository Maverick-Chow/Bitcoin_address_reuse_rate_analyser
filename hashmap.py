from tree import Tree


class HashTable:

    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [Tree() for _ in range(self.size)]

    def add(self, address):

        hashed_address = hash(address) % self.size

        bucket = self.hash_table[hashed_address]

        bucket.add(address)

    def list(self):
        result = []
        for i in self.hash_table:
            result += i.list_tree()
        return result

    def analyse(self):
        total_address_count = 0
        reused_address_count = 0
        for i in self.hash_table:
            total_address_count += i.size
            reused_address_count += i._count_reused(i.root)
        reuse_percentage = reused_address_count*100/total_address_count
        return f"""
 ==========================================
 || Total address count: {total_address_count}
 || Reused address count: {reused_address_count}
 || Reuse percentage: {reuse_percentage}%
 ==========================================
        """
