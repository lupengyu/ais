import Decoder

f = open("data/11.25 20.56.txt")
fwirt = open("main.csv", "w+")
flog = open("decodelog.txt", "w+")
line = f.readline()
sum = 0
while line:
    Decoder.AIS_Decoder(line, fwirt, flog)
    line = f.readline()
    sum += 1
    if sum % 100 == 0:
        print(sum)

f.close()
fwirt.close()
flog.close()
print(sum, Decoder.getTypeDict())