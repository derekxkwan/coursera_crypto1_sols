import urllib2
import sys

BLOCKSIZE = 16
TARGET = 'http://crypto-class.appspot.com/po?er='
qry = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------

def guessblock(istr, lastblk):
    loc = [ord(x) for x in istr[-(BLOCKSIZE*2):-BLOCKSIZE]]
    if lastblk:
        guess = [0] * BLOCKSIZE 
    else:
        guess = [32] * BLOCKSIZE #assume that the string consists of non-control chars
    padnum = 1
    while padnum <= BLOCKSIZE:
        curpad = [0]*(BLOCKSIZE-padnum) + [padnum]*padnum
        inqstr = (istr[:-(BLOCKSIZE*2)]+''.join([chr(x^y^z) for (x,y,z) in zip(loc,curpad, guess)]) + istr[-BLOCKSIZE:]).encode('hex')
        retval = po.query(inqstr)
        if retval == 1:
            #correct guess
            print("This is my current guess: " + ''.join([chr(ch) for ch in guess]))
            curguess = guess[-padnum]
            if curguess <= BLOCKSIZE:
                guess = [32]*(BLOCKSIZE-curguess) + [curguess]*curguess
                padnum = curguess + 1
            else:
                padnum += 1
        else:
            #incorrect guess
            guess[-padnum] += 1
    print("DONE!!!")
    return ''.join([chr(ch) for ch in guess if ch >= 32])
        
        


class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
            return 2 #all correct
        except urllib2.HTTPError, e:          
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return 1 # good padding = right guess
            return 0 #wrong padding = wrong guess

if __name__ == "__main__":
    po = PaddingOracle()
    #po.query(sys.argv[1])       # Issue HTTP query with the given argument
    qryreg = qry.decode('hex')
    #print(len(qryreg))
    correct = ''
    curlen = BLOCKSIZE*2
    while curlen <= len(qryreg):
        if curlen == len(qryreg):
            lastbl = 1
        else:
            lastbl = 0
        cuript = qryreg[:curlen]
        curout = guessblock(cuript, lastbl)
        correct += curout
        curlen += BLOCKSIZE
        print(correct)
    print correct
