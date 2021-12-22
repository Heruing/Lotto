dd = {1:12, 2:1, 3:76, 4:15}
ki= dd.items()
ss = sorted(ki, key= lambda ki: ki[1], reverse=True)
sortedNumbers = map(lambda x: x[0],sorted(dd.items(), key= lambda item: item[1]))
print(list(sortedNumbers))