import Decoder
import time

starttime = time.time()
fwirt = open("main.csv", "w+")
flog = open("decodelog.txt", "w+")
finfo = open("info.csv", "w+")
filecnt = 0
for i in range(10000):
    try:
        f = open("data/f" + str(i) + ".txt")
    except FileNotFoundError:
        continue
    print(str(i) + ".txt")
    filecnt += 1
    line = f.readline()
    sum = 0
    while line:
        Decoder.AIS_Decoder(line, fwirt, finfo, flog)
        line = f.readline()
        sum += 1
        if sum % 10000 == 0:
            print(sum)
    f.close()
fwirt.close()
flog.close()
endtime = time.time()
print("File cnt:", filecnt)
print("Spend time:", endtime-starttime)
print(sum, Decoder.getTypeDict())