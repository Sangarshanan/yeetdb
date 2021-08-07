import os 

def encode(value):
    return value.encode('unicode-escape').decode('ASCII')

def decode(value):
    return value.encode("ASCII").decode('unicode-escape')

class HashIndex:
    def __init__(self, dbname, tablename):
        self.name = f"{dbname}/{tablename}.kv" # Filename
        if not os.path.exists(self.name):
            with open(self.name, 'w'):
                pass
        self.index = {}
    
    # Special characters <EOK> end of key & <EOP> end of pair

    def insert(self, key, value):
        # Write to file and save offset
        with open(self.name, 'a') as f:
            f.seek(0, 2) # first line from the end
            end_offset = f.tell() # end offset
            f.write(encode(f"{key}<EOK>{value}<EOP>"))
        # create index using offset
        self.index[key] = {
            "offset": end_offset,
            "pk_size": len(f"{key}"), 
            "data_size": len(f"{value}"),
            "data": f"{value}"
        }
        
    def get(self, key):
        # Read from Offset and length
        try:
            return self.index[key]["data"]
        except:
            return "<NAN>"

    def iterate(self, keys):
        return list(map(lambda x : self.get(x), keys))

    def delete(self,key):
        key_index = self.index[key]
        with open(self.name, 'a') as f:
            char = f.seek(key_index["offset"])
            # Tombstone
            f.write(encode(f"{key}<EOK><NAN><EOP>"))
        self.index.pop(key, None)

def read_hash_index(dbname, tablename):
    with open(f"{dbname}/{tablename}.kv") as f:
        lines = f.readline()
    _index = {}
    offset_passed = 0
    for val in lines.split("<EOP>")[:-1]:
        key, value = val.split("<EOK>")
        _index[int(key)] = {
            "offset": offset_passed,
            "pk_size": len(key), 
            "data_size": len(value),
            "data": decode(f"{value}")
        }
        offset_passed += len(val) + 5
    hashin = HashIndex(dbname, tablename)
    hashin.index = _index
    return hashin
