import sys

def hextoreg(filename):
    str1 = ''
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
        for ln in lines:
            ln = ln.decode('hex')
            print(ln)
            str1 += ln
    return str1

strret = hextoreg(sys.argv[1])
print(strret)
