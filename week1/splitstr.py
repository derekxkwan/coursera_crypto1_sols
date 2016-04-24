import sys

def hexparse(ipt):
    with open(ipt, 'r'):
        str1 = ''
        for line in f.readlines():
            line = line.strip()
            t = iter(line)
            str1+=(a+b for a,b in zip(t,t)).decode('hex')
        return str1

str1 = hexparse(sys.argv[1])
print(str1)

