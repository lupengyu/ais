ASCII_TO_6BITS = {
    '0': "000000",
    '1': "000001",
    '2': "000010",
    '3': "000011",
    '4': "000100",
    '5': "000101",
    '6': "000110",
    '7': "000111",
    '8': "001000",
    '9': "001001",
    ':': "001010",
    ';': "001011",
    '<': "001100",
    '=': "001101",
    '>': "001110",
    '?': "001111",
    '@': "010000",
    'A': "010001",
    'B': "010010",
    'C': "010011",
    'D': "010100",
    'E': "010101",
    'F': "010110",
    'G': "010111",
    'H': "011000",
    'I': "011001",
    'J': "011010",
    'K': "011011",
    'L': "011100",
    'M': "011101",
    'N': "011110",
    'O': "011111",
    'P': "100000",
    'Q': "100001",
    'R': "100010",
    'S': "100011",
    'T': "100100",
    'U': "100101",
    'V': "100110",
    'W': "100111",
    "'": "101000",
    '`': "101000",
    'a': "101001",
    'b': "101010",
    'c': "101011",
    'd': "101100",
    'e': "101101",
    'f': "101110",
    'g': "101111",
    'h': "110000",
    'i': "110001",
    'j': "110010",
    'k': "110011",
    'l': "110100",
    'm': "110101",
    'n': "110110",
    'o': "110111",
    'p': "111000",
    'q': "111001",
    'r': "111010",
    's': "111011",
    't': "111100",
    'u': "111101",
    'v': "111110",
    'w': "111111"
}

BITS_TO_ASCII = {
    '000000': "@",
    '000001': "A",
    '000010': "B",
    '000011': "C",
    '000100': "D",
    '000101': "E",
    '000110': "F",
    '000111': "G",
    '001000': "H",
    '001001': "I",
    '001010': "J",
    '001011': "K",
    '001100': "L",
    '001101': "M",
    '001110': "N",
    '001111': "O",
    '010000': "P",
    '010001': "Q",
    '010010': "R",
    '010011': "S",
    '010100': "T",
    '010101': "U",
    '010110': "V",
    '010111': "W",
    '011000': "X",
    '011001': "Y",
    '011010': "Z",
    '011011': "[",
    '011100': "\\",
    '011101': "]",
    '011110': "^",
    '011111': "_",
    '100000': " ",
    '100001': "!",
    '100010': "\"",
    '100011': "#",
    '100100': "$",
    '100101': "%",
    '100110': "&",
    '100111': "`",
    "101000": "(",
    '101001': ")",
    '101010': "*",
    '101011': "+",
    '101100': ",",
    '101101': "-",
    '101110': ".",
    '101111': "/",
    '110000': "0",
    '110001': "1",
    '110010': "2",
    '110011': "3",
    '110100': "4",
    '110101': "5",
    '110110': "6",
    '110111': "7",
    '111000': "8",
    '111001': "9",
    '111010': ":",
    '111011': ";",
    '111100': "<",
    '111101': "=",
    '111110': ">",
    '111111': "?"
}


typeDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0,
                23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}
id = 1
infoid = 1
year = 0
month = 0
day = 0
hour = 0
minute = 0
sec = 0
tmpmessage = ""
tmpbit = []
waitSingle = 0

def getTypeDict():
    return typeDict

def bits_to_numbers(str):
    sum = 0
    length = len(str)
    for item in str:
        sum += int(item) * pow(2, length - 1)
        length -= 1
    return sum

def bits_to_Complementnumbers(str):
    sum = 0
    length = len(str)
    for i in range(1, length):
        sum += int(str[i]) * pow(2, length - 2)
        length -= 1
    if str[0] == "1":
        sum = (pow(2, len(str) - 1) - sum) * -1
    return sum

def XOR(str1, str2):
    if len(str1) != len(str2):
        return "error"
    str = ""
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            str += '0'
        else:
            str += '1'
    return str

def CRC_rightturn(CRC_low, CRC_hig):
    CRC = "0"
    for item in CRC_hig:
        CRC += item
    for i in range(len(CRC_low) - 1):
        CRC += CRC_low[i]
    return CRC

def CRC_check(CRC, item):
    CRC_low = XOR(item, CRC[6:12])
    CRC_hig = CRC[0:6]
    for i in range(6):
        judge = CRC_low[5]
        CRC = CRC_rightturn(CRC_low, CRC_hig)
        if judge == "1":
            CRC = XOR(CRC, "111100000001")# 翻转111100000001,不翻转100000001111
        CRC_low = CRC[6:12]
        CRC_hig = CRC[0:6]
    # print(CRC)
    return CRC

def AIS_Decoder(message, f, finfo, log):
    global id
    global year
    global month
    global day
    global hour
    global minute
    global sec
    global tmpbit
    global waitSingle
    global tmpmessage
    global infoid
    messages = message.split(",")
    # 判断是否具有主要内容
    if len(messages) < 6:
        return

    # 判断标识符定义是否正确
    if messages[0] != "!AIVDM" and messages[0] != "!AIVDO":
        return

    # 判断语句数是否正确
    sum = 0
    if messages[1].isdigit():
        sum = int(messages[1])
        #TODO: 目前只实现了单AIS编码
        # if sum != 1:
        #     return
        if sum <= 0 or sum > 9:
            return
    else:
        return

    # 判断序列牌号是否正确
    cnt = 0
    if messages[2].isdigit():
        cnt = int(messages[2])
        # if cnt != 1:
        #     return
        if cnt <= 0 or cnt > sum:
            return
    else:
        return
    
    # 判断统一标识是否合法
    if messages[3].isdigit():
        if int(messages[3]) < 0 or int(messages[3]) > 9:
            return
    else:
        if messages[3] != "":
            return

    # 判断接收频道是否正确
    if messages[4] != "A" and messages[4] != "B" and messages[4] != "":
        return
    
    # 封装数据处理
    bits = ""
    if len(messages) < 7:
        return

    check = messages[6].split("*")
    CRC = "111111111111"
    for item in messages[5]:
        try:
            bits += ASCII_TO_6BITS[item]
        except KeyError:
            return
        # if len(check) > 1:
        #     CRC = CRC_check(CRC, ASCII_TO_6BITS[item])

    # 校验码位处理
    if len(messages) == 7 and messages[6] != "":
        if len(check) > 0 and check[0] != "0":
            for item in check[0]:
                try:
                    bits += ASCII_TO_6BITS[item]
                except KeyError:
                    return
                # if len(check) > 1:
                #     # print("add:", item)
                #     CRC = CRC_check(CRC, ASCII_TO_6BITS[item])
        # TODO:校验码校验
        # 负责人：谷雨鸿
        # if(len(check) > 1):
        #     print("CRC:", CRC)
        #     print("crc: %s%s"%(ASCII_TO_6BITS[check[1][0]], ASCII_TO_6BITS[check[1][1]]))
    if waitSingle != 0:
        if waitSingle == 5:
            #348 84
            if sum != 2 or cnt != 2:
                return
            zhuanfa = tmpbit[6:8] #2
            MMSI = tmpbit[8:38] #30
            AIS = tmpbit[38:40] #2
            IMO = tmpbit[40:70] #30
            huhao = tmpbit[70:112] #42
            huhaostring = ""
            isum = 0
            for i in range(7):
                try:
                    huhaostring += BITS_TO_ASCII[huhao[isum:isum + 6]]
                    isum += 6
                except KeyError:
                    return
            name = tmpbit[112:232] #120
            namestring = ""
            isum = 0
            for i in range(20):
                try:
                    namestring += BITS_TO_ASCII[name[isum:isum + 6]]
                    isum += 6
                except KeyError:
                    return
            type = tmpbit[232:240] #8
            size = tmpbit[240:270]
            A = size[0:9]
            B = size[9:18]
            C = size[18:24]
            D = size[24:30]
            position = tmpbit[270:274]
            ETA = tmpbit[274:294]
            ETA_min = ETA[14:20]
            ETA_hour = ETA[9:14]
            ETA_day = ETA[4:9]
            ETA_month = ETA[0:4]
            chishui = tmpbit[294:302]
            des1 = tmpbit[302:348]
            des = (des1 + bits)[:120]
            desstring = ""
            isum = 0
            for i in range(20):
                try:
                    item = BITS_TO_ASCII[des[isum:isum + 6]]
                    if (item >= 'A' and item <= 'Z') or (item >= '0' and item <= '9') :
                        item = item
                    else:
                        item = ' '
                    desstring += item
                    isum += 6
                except KeyError:
                    return
            writeString = str(infoid) + "," + str(bits_to_numbers(zhuanfa)) + "," + str(bits_to_numbers(MMSI)) + "," + \
                        str(bits_to_numbers(AIS)) + "," + str(bits_to_numbers(IMO)) + "," + huhaostring + "," + \
                        namestring + "," + str(bits_to_numbers(type)) + "," + str(bits_to_numbers(A)) + "," + \
                        str(bits_to_numbers(B)) + "," + str(bits_to_numbers(C)) + "," + str(bits_to_numbers(D)) + "," + \
                        str(bits_to_numbers(A) + bits_to_numbers(B)) + "," + str(bits_to_numbers(C) + bits_to_numbers(D)) + "," + \
                        str(bits_to_numbers(position)) + "," + str(bits_to_numbers(ETA_month)) + "," + str(bits_to_numbers(ETA_day)) + "," + str(bits_to_numbers(ETA_hour)) + "," + \
                        str(bits_to_numbers(ETA_min)) + "," + str(bits_to_numbers(chishui) * 0.1) + "," + desstring + "," + \
                        str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(minute) + "," + str(sec) + \
                        "\r\n"
            finfo.write(writeString)
            log.write(tmpmessage)
            log.write(message + "decode: " + writeString)
            infoid += 1
        waitSingle = 0
        return
    Message_Type = bits[0:6]
    if bits_to_numbers(Message_Type) > 30 or bits_to_numbers(Message_Type) <= 0:
        return
    typeDict[bits_to_numbers(Message_Type)] += 1
    if(bits_to_numbers(Message_Type) == 1 or
        bits_to_numbers(Message_Type) == 2 or
            bits_to_numbers(Message_Type) == 3):
        if sum != 1 or cnt != 1:
            return
        if len(bits) < 168:
            return
        Repeat_Indicator = bits[6:8] #2
        MMSI = bits[8:38] #30
        Navigation_Status = bits[38:42] #4
        ROT = bits[42:50] #8
        # ROT = "01111111"
        SOG = bits[50:60] #10
        Position_Accuracy = bits[60] #1
        Longitude = bits[61:89] #28
        Latitude = bits[89:116] #27
        COG = bits[116:128] #12
        HDG = bits[128:137] #9
        Time_Stamp = bits[137:143] #6
        Reserved_for_regional = bits[143:145] #3
        #145-147位未使用
        RAIM_flag = bits[148]
        # Communication_State = bits[149:168]
        # Sync_state = Communication_State[0:2]
        # Slot_Timeout = Communication_State[2:5]
        # UTC_hour = Communication_State[5:10]
        # UTC_minute = Communication_State[10:19]

        writeString = str(id) + "," + str(bits_to_numbers(Message_Type)) + "," + \
                      str(bits_to_numbers(Repeat_Indicator)) + "," + \
                      str(bits_to_numbers(MMSI)) + "," + \
                      str(bits_to_numbers(Navigation_Status)) + "," + \
                      str(bits_to_Complementnumbers(ROT)) + "," + \
                      str(bits_to_numbers(SOG) * 0.1) + "," + \
                      str(bits_to_numbers(Position_Accuracy)) + ","
        if Longitude[0] == "0":
            writeString += str(int(bits_to_numbers(Longitude[1:]) / 600000)) + "." + str(int((bits_to_numbers(Longitude[1:]) % 600000) / 60)) + ","
        else:
            return
        if Latitude[0] == "0":
            writeString += str(int(bits_to_numbers(Latitude[1:]) / 600000)) + "." + str(int((bits_to_numbers(Latitude[1:]) % 600000) / 60)) + ","
        else:
            return
        writeString += str(bits_to_numbers(COG) * 0.1) + "," + str(bits_to_numbers(HDG)) + "," + str(bits_to_numbers(Time_Stamp)) + "," + str(bits_to_numbers(Reserved_for_regional)) + "," + str(RAIM_flag) + ","
        writeString += str(year) + "," + str(month) + "," + str(day) + "," + str(hour) + "," + str(minute) + "," + str(sec)
        writeString += "\r\n"
        f.write(writeString)
        log.write(message + "decode: " + writeString)
        id += 1
    else:
        if bits_to_numbers(Message_Type) == 4 or bits_to_numbers(Message_Type) == 11:
            if sum != 1 or cnt != 1:
                return
            if len(bits) < 168:
                return
            # zhuanfa = bits[6:8] #2
            # MMSI = bits[8:38] #30
            UTC_year = bits[38:52] #14
            UTC_month = bits[52:56] #4
            UTC_day = bits[56:61] #5
            UTC_hour = bits[61:66] #5
            UTC_min = bits[66:72] #6
            UTC_second = bits[72:78] #6
            # Position_Accuracy = bits[78]  # 1
            # Longitude = bits[79:107]  # 28
            # Latitude = bits[107:134]  # 27
            if bits_to_numbers(UTC_year) < 2018 or bits_to_numbers(UTC_year) > 2019:
                return
            year = bits_to_numbers(UTC_year)
            month = bits_to_numbers(UTC_month)
            day = bits_to_numbers(UTC_day)
            hour = bits_to_numbers(UTC_hour)
            minute = bits_to_numbers(UTC_min)
            sec = bits_to_numbers(UTC_second)
        if bits_to_numbers(Message_Type) == 5:
            if sum != 2 or cnt != 1:
                return
            tmpmessage = message
            tmpbit = bits[:]
            waitSingle = 5
        return
