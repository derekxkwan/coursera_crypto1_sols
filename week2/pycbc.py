from Crypto.Cipher import AES as aes
from Crypto import Random as crnd

#16 bit IV chosen at random and prepended to the ciphertext
#pkcs5 padding
q = [{"key": "140b41b22a29beb4061bda66b6747e14", "ct": "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"}, {"key": "140b41b22a29beb4061bda66b6747e14", "ct": "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"}]


qord = []
for i in range(len(q)):
    newdict = {}
    newdict["key"] = [ord(x) for x in q[i]["key"].decode("hex")]
    newdict["ct"] = [ord(x) for x in q[i]["ct"].decode("hex")]
    newdict["iv"] = newdict["ct"][:16]
    newdict["ct"] = newdict["ct"][16:]
    qord.append(newdict)

def encrypt(key, pt):
    bs = aes.block_size
    iv = crnd.new().read(aes.block_size)
    ptlen = len(pt)
    padnum = bs - ptlen % bs
    pt += chr(padnum)*padnum #padding
    ptlen = len(pt)
    ptrange = int(ptlen/float(bs) + 0.999999999999999)
    ptarr = map(lambda i: pt[i*bs:(i+1)*bs], range(ptrange))
    cipher = aes.new(key.decode("hex"), aes.MODE_ECB)
    retstr = iv
    prev = iv
    for ptelt in ptarr:
        ptord = [ord(x) for x in ptelt]
        prevord = [ord(x) for x in prev]
        iptord = [chr(x^y) for (x,y) in zip(ptord,prevord)]
        ipt = "".join(iptord)
        ciphered = cipher.encrypt(ipt)
        retstr += ciphered
        prev = ciphered
    return retstr.encode("hex")

def decrypt(key, ct):
    ct = ct.decode("hex")
    iv = ct[:16]
    ct = ct[16:]
    bs = aes.block_size
    ctlen = len(ct)
    ctrange = int(ctlen/float(bs) + 0.99999999999999)
    ctarr = map(lambda i: ct[i*bs:(i+1)*bs], range(ctrange))
    cipher = aes.new(key.decode("hex"), aes.MODE_ECB)
    prev = iv
    retstr = ""
    for ctelt in ctarr:
        decrypted = cipher.decrypt(ctelt)
        prevord = [ord(x) for x in prev]
        decord = [ord(x) for x in decrypted]
        optord = [chr(x^y) for (x,y) in zip(prevord, decord)]
        decstr = "".join(optord)
        retstr += decstr
        prev = ctelt
    retstr = retstr[:-ord(retstr[len(retstr)-1:])]
    return retstr



'''
testkey = q[0]["key"]
teststr = "this is a test encryption"
retstr = encrypt(testkey, teststr)
print(retstr) 
retstr2 = decrypt(testkey, retstr)
print(retstr2)
'''

for pair in q:
    key = pair["key"]
    ct = pair["ct"]
    retstr = decrypt(key, ct)
    print(retstr)
