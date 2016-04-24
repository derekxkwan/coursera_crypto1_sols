import gmpy2
from gmpy2 import mpz

def rptsq(base, toraise):
    #repeated squaring algo
    #base = value to raise, toraise = exponent
    binstr = bin(toraise)[2:] #string in binary of toraise
    curmult = base
    curval = mpz('1')
    for digit in reversed(xrange(len(binstr))):
            if binstr[digit] == '1':
                curval = gmpy2.mul(curval, curmult)
            curmult = gmpy2.mul(curmult, base)
    return curval

p=mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')

g=mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')

h=mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')

B = 2**20

gB = gmpy2.powmod(g, B, p)

#val of h/g^x1
hgx1val = {}

#make hashtable by with keys being the values of hgx1

for x1 in xrange(2**20 + 1):
    gx1 = gmpy2.powmod(g, x1,p) #calculate g^x1
    hgx1 = str(gmpy2.divm(h,gx1,p)) #calculating h/g^x1 in Z_p and make str
    hgx1val[hgx1] = x1 #adding val as key and gpow as value to hash

for x0 in xrange(2**20 + 1):
    gBx0 = str(gmpy2.powmod(gB,x0, p)) #calculate (g^B)^x0 and make str
    if gBx0 in hgx1val:
        xret = gmpy2.mul(x0,B)
        xret = gmpy2.add(hgx1val[gBx0], xret)
        xret = gmpy2.f_mod(xret, p)
        print(xret)
        break
