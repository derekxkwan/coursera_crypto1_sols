from Crypto.Cipher import AES as aes
from Crypto import Random as crnd

#16 bit IV chosen at random and prepended to the ciphertext
#pkcs5 padding
q = [{"key": "36f18357be4dbd77f050515c73fcf9f2", "ct": "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"},{"key": "36f18357be4dbd77f050515c73fcf9f2", "ct": "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"}]
def inciv(iv):
    ivord = [ord(x) for x in iv]
    curinc = True #if we are currently incrementing
    diginc = -1 #digit being incremented
    while curinc:
        curdiv = (ivord[diginc]+1)/255
        if curdiv >= 1: #if adding one will make a carry
            ivord[diginc] = (ivord[diginc] + 1) % 255 #go ahead and add
            diginc += -1 #move one digit to the left
        else:
            #if adding one will not make a carry
            ivord[diginc] += 1 #increment
            curinc = False #stop incrementing
        if abs(diginc) >= len(ivord):
            #if overflow
            curinc = False #just stop
    retstr = "".join([chr(x) for x in ivord])
    return retstr

def encrypt(key, pt):
    bs = aes.block_size
    iv = crnd.new().read(aes.block_size)
    ptlen = len(pt)
    padnum = bs - ptlen % bs
    if ptlen % bs != 0:
        pt += chr(padnum)*padnum #padding
    ptlen = len(pt)
    ptrange = int(ptlen/float(bs) + 0.9999999999)
    ptarr = map(lambda i: pt[i*bs:(i+1)*bs], range(ptlen/bs))
    cipher = aes.new(key.decode("hex"), aes.MODE_ECB)
    retstr = iv
    for ptelt in ptarr:
        randval = cipher.encrypt(iv)
        randord = [ord(x) for x in randval]
        ptord = [ord(x) for x in ptelt]
        xorlen = min(len(randord),len(ptord))
        ctord = [chr(x^y) for (x,y) in zip(randord[:xorlen],ptord[:xorlen])]
        ctstr = "".join(ctord)
        retstr += ctstr
        iv = inciv(iv)
    return retstr.encode('hex')

def decrypt(key, ct):
    bs = aes.block_size
    ct = ct.decode('hex')
    iv = ct[:16]
    ct = ct[16:]
    ctlen = len(ct)
    ctrange = int(ctlen/float(bs) + 0.9999999999)
    ctarr = map(lambda i: ct[i*bs:(i+1)*bs], range(ctrange))
    cipher = aes.new(key.decode('hex'), aes.MODE_ECB)
    retstr = ""
    for ctelt in ctarr:
        randval = cipher.encrypt(iv)
        randord = [ord(x) for x in randval]
        ctord = [ord(x) for x in ctelt]
        xorlen = min(len(randord),len(ctord))
        ptord = [chr(x^y) for (x,y) in zip(randord[:xorlen],ctord[:xorlen])]
        ptstr = "".join(ptord)
        retstr += ptstr
        iv = inciv(iv)
    return retstr
testkey = q[0]["key"]
teststr = "this string is sixteen bytes log"
retstr = encrypt(testkey, teststr)
retstr2 = decrypt(testkey, retstr)
for pair in q:
    key = pair["key"]
    ct = pair["ct"]
    retstr = decrypt(key, ct)
    print(retstr)
