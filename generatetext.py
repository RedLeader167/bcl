sid = input("Shelf id: ")
txt = input("Text: ")
res = "\tDO MATERIALIZE $" + sid + " ^" + str(len(txt)) + "\n"
for i in range(len(txt)):
    res += "\tDO $" + sid + " ^" + str(i + 1) + ": " + str(ord(txt[i])) + "\n"
print(res)