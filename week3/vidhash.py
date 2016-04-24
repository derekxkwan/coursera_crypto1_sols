from Crypto.Hash import SHA256 as sha256

#1 KB = 1024 bytes = 1024 * 8 bits
#one char is 1 byte

testh0 =  "03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8"
testfile = "testhash.mp4"
assnfile = "assnhash.mp4"
testfile = "6 - 2 - Generic birthday attack (16 min).mp4"
assnfile = "6 - 1 - Introduction (11 min).mp4"

def parsevid(filename):
    str1 = ''
    with open(filename, 'r') as f:
        str1 = f.read()
        vidarray = [str1[i*1024:(i+1)*1024] for i in range(int(len(str1)/1024 +0.99999999999999999))]
    return vidarray

testarr = parsevid(assnfile)
def geth0(arr):
    i = len(arr)-2
    prevstr = arr[i+1]
    while i >= 0:
        h = sha256.new()
        h.update(prevstr)
        hstr = h.digest()
        prevstr = arr[i]
        prevstr += hstr
        i += -1
    h = sha256.new()
    h.update(prevstr)
    return h.hexdigest()

testh0 = geth0(testarr)
print(testh0)
