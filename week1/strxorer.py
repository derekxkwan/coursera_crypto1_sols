import sys
import binascii

seltext = int(sys.argv[1])
MSGS = ['ct1.txt', 'ct2.txt', 'ct3.txt', 'ct4.txt', 'ct5.txt', 'ct6.txt', 'ct7.txt', 'ct8.txt', 'ct9.txt', 'ct10.txt', 'cttarg.txt']

if seltext <0:
    seltext = 0
elif seltext > len(MSGS)-1:
    seltext = len(MSGS) - 1

TARG = 'cttarg.txt'

def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)]),
    else:
       return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def strxornums(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
       return [ord(x) ^ ord(y) for (x, y) in zip(a[:len(b)], b)]
    else:
       return [ord(x) ^ ord(y) for (x, y) in zip(a, b[:len(a)])]


def filetostr(filename):
    strret = ''
    with open(filename, 'r') as f:
        strret = [line.strip().decode('hex') for line in f]
        return strret[0]

def filetoarr(filename):
    arrret = []
    with open(filename, 'r') as f:
        strret = [line.strip().decode('hex') for line in f]
        arrret = [ord(x) for x in strret[0]]
    return arrret

def xorrestore(key, msg):
    curlen = len(msg)
    targarr = [chr(x^y) for (x,y) in zip(msg, key[:curlen])]
    targstr = "".join(targarr)
    for y in range(curlen):
        print(y, msg[y], targstr[y])
    print(targstr)
    return targstr
xorarrs = []
xorstrs = []
longest = ""
xortarg = filetoarr(TARG)
keylen = 0
for fname in MSGS:
    retstr = filetostr(fname)
    retarr = filetoarr(fname)
    curlen = len(retstr)
    keylen = max(curlen, keylen)
    if curlen == keylen:
        longest = fname
    xorstrs.append(retstr)
    xorarrs.append(retarr)
'''
spacearrs = []
for arridx in range(len(targxor)):
    spacearr = [i for i in range(len(targxor[arridx])) if targxor[arridx][i] >= 65 or targxor[arridx][i] == 0]
    spacearrs.append(spacearr)


commonspaces = spacearrs[0]
maxlen = len(spacearrs[0])
for i in range(len(spacearrs)):
    if i > 0:
        newarr = []
        for elt in spacearrs[i]:
            if elt in commonspaces:
                newarr.append(elt)
        commonspaces = newarr
'''

key = [0 for i in range(keylen)]
for i in range(len(xorarrs)):
    spacearrs = []
    targxor = []
    curlen = len(xorarrs[i])
    for j in range(len(xorarrs)):
        if j != i:
            nowlen = min(curlen, len(xorarrs[j]))
            newarr = [x^y for (x,y) in zip(xorarrs[i][:nowlen], xorarrs[j][:nowlen])]
            targxor.append(newarr)
    #print(targxor)
    for arridx in range(len(targxor)):
        spacearr = [j for j in range(len(targxor[arridx])) if targxor[arridx][j] >= 65 or targxor[arridx][j] == 0]
        spacearrs.append(spacearr)


    commonspaces = spacearrs[0]
    maxlen = len(spacearrs[0])
    for j in range(len(spacearrs)):
        if j > 0:
            newarr = []
            for elt in spacearrs[j]:
                if elt in commonspaces:
                    newarr.append(elt)
            commonspaces = newarr
    for idx in commonspaces:
        if key[idx] == 0:
            key[idx] = xorarrs[i][idx] ^ 32
#print(key)
key[2] = 110
key[82] = 97
key[81] = 154
key[14] = 149
key[7] = 204
key[10] = 53
key[42] = 109
key[21] = 127
key[49] = 99
key[50] = 254
key[54] = 72
key[25] = 127
key[26] = 107
key[36] = 25
key[30] = 197
key[31] = 11
key[32] = 105
key[33] = 176
key[34] = 51
key[35] = 154
#key[30] = 197
newstr = xorrestore(key,xorarrs[seltext])
#print(targxor[6])
#print(targxor[1])
#print(targstr)
