import sys

result = {}
lines = sys.stdin.readlines()
key = ''
value = []



class Chain:
    def __init__(self, name):
        self.name = name
        self.tables = {}
    def getName(self):
        return name
    def addCommand(self, tableName, command):
        self.tables.setdefault(tableName, []).append(command)
    def show(self):
        tableOrder = [
            "raw",
            "mangle",
            "nat",
            "filter"
        ]
        print("=== {} ===".format(self.name))
        for tableName in tableOrder:
            print("--- {} ---".format(tableName))
            commands = self.tables.get(tableName, [])
            if len(commands) == 0:
                continue
            for command in commands:
                print("{}".format(command))

chains = {}

currentTableName = ""
for l in lines:
    line = l.strip('\n').strip('\r')
    if line.startswith('*'):
        currentTableName = line[1:len(line)]
    elif line.strip() == 'COMMIT':
        continue
    elif line.startswith('-A'):
        chainName = line.split(" ")[1]
        chains.setdefault(chainName, Chain(chainName)).addCommand(currentTableName, line.rstrip("\n"))
        #print("add command to {}/{}: {}\n".format(chainName, currentTableName, line))
    elif line.startswith('#') or line.startswith(":"):
        continue
    else:
        print("unrecognized line:" + line + "\n")

for key, chain in chains.items():
    chain.show()
