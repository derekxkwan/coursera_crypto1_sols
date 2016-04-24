a = [["9f970f4e932330e4", "6068f0b1b645c008"], ["7c2822ebfdc48bfb", "325032a9c5e2364b"],[ "4af532671351e2e1", "87a40cfa8dd39154"],["2d1cfa42c0b1d266", "eea6e3ddb2146dd0"]]

aord = []
for bigarr in a:
    newarr = []
    for smallarr in bigarr:
        newstr = smallarr.decode("hex")
        newarr2 = [ord(x) for x in newstr]
        newarr.append(newarr2)
    aord.append(newarr)

xord = []
for bigarr in aord:
    xorer = [chr(x^y) for (x,y) in zip(bigarr[0],bigarr[1])]
    print(xorer)
    xorstr = "".join(xorer)
    xord.append(xord)

print(xord)
