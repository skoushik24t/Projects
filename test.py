def stringtobinary(txt):
    out = ""
    for c in list(txt):
        tmp = bin(ord(c))[2:]
        out += "0"*(8-len(tmp))+tmp+" "
    return out

f = open("Airplanes.mp3", "r+b")
for i in range(100):
    print stringtobinary(f.read(32))