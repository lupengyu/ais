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

typeDict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0,
                23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}

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

def AIS_Decoder(message, f, log):
    # print("Decoded message:")
    # print(message)
    messages = message.split(",")
    # 判断是否具有主要内容
    if len(messages) < 6:
        # print("Unable to decode message")
        return

    # 判断标识符定义是否正确
    if messages[0] != "!AIVDM" and messages[0] != "!AIVDO":
        # print("Invalid data packet ID")
        return

    # 判断语句数是否正确
    sum = 0
    if messages[1].isdigit():
        sum = int(messages[1])
        if sum <= 0 or sum > 9:
            # print("Need more data for parsing")
            return
    else:
        # print("Invalid number of fragments")
        return

    # 判断序列牌号是否正确
    cnt = 0
    if messages[2].isdigit():
        cnt = int(messages[2])
        if cnt <= 0 or cnt > sum:
            # print("Need more data for parsing")
            return
    else:
        # print("Invalid number of fragments")
        return
    
    # 判断统一标识是否合法
    if messages[3].isdigit():
        if int(messages[3]) < 0 or int(messages[3]) > 9:
            # print("Need more data for parsing")
            return
    else:
        if messages[3] != "":
            # print("Invalid number of fragments")
            return

    # 判断接收频道是否正确
    if messages[4] != "A" and messages[4] != "B" and messages[4] != "":
        # print("Invalid radio channel code")
        return
    
    # 封装数据处理
    bits = ""
    if len(messages) < 7:
        return
    # print()
    check = messages[6].split("*")
    CRC = "111111111111"
    for item in messages[5]:
        if item == '!':
            return
        bits += ASCII_TO_6BITS[item]
        # if len(check) > 1:
        #     CRC = CRC_check(CRC, ASCII_TO_6BITS[item])

    # 校验码位处理
    if len(messages) == 7 and messages[6] != "":
        if len(check) > 0 and check[0] != "0":
            for item in check[0]:
                bits += ASCII_TO_6BITS[item]
                # if len(check) > 1:
                #     # print("add:", item)
                #     CRC = CRC_check(CRC, ASCII_TO_6BITS[item])
        # TODO:校验码校验
        # 负责人：谷雨鸿
        # if(len(check) > 1):
        #     print("CRC:", CRC)
        #     print("crc: %s%s"%(ASCII_TO_6BITS[check[1][0]], ASCII_TO_6BITS[check[1][1]]))
    Message_Type = bits[0:6]
    if bits_to_numbers(Message_Type) > 30 or bits_to_numbers(Message_Type) <= 0:
        return
    typeDict[bits_to_numbers(Message_Type)] += 1
    if(bits_to_numbers(Message_Type) == 1 or
        bits_to_numbers(Message_Type) == 2 or
            bits_to_numbers(Message_Type) == 3):
        if len(bits) < 168:
            return
        Repeat_Indicator = bits[6:8]
        MMSI = bits[8:38]
        Navigation_Status = bits[38:42]
        ROT = bits[42:50]
        # ROT = "01111111"
        SOG = bits[50:60]
        Position_Accuracy = bits[60]
        Longitude = bits[61:89]
        Latitude = bits[89:116]
        COG = bits[116:128]
        HDG = bits[128:137]
        Time_Stamp = bits[137:143]
        Reserved_for_regional = bits[143:147]
        #147位未使用
        RAIM_flag = bits[148]
        Communication_State = bits[149:168]
        Sync_state = Communication_State[0:2]
        Slot_Timeout = Communication_State[2:5]
        UTC_hour = Communication_State[5:10]
        UTC_minute = Communication_State[10:17]

        writeString = str(bits_to_numbers(Message_Type)) + "," + \
                      str(bits_to_numbers(Repeat_Indicator)) + "," + \
                      str(bits_to_numbers(MMSI)) + "," + \
                      str(bits_to_numbers(Navigation_Status)) + "," + \
                      str(bits_to_Complementnumbers(ROT)) + "," + \
                      str(bits_to_numbers(SOG) * 0.1) + ","
        if Longitude[0] == "0":
            writeString += str(int(bits_to_numbers(Longitude[1:]) / 600000)) + "." + str(int((bits_to_numbers(Longitude[1:]) % 600000) / 60))
            # print("Longitude: \t\t %d°.%d E"%(int(bits_to_numbers(Longitude[1:]) / 600000), int((bits_to_numbers(Longitude[1:]) % 600000) / 60)))
        else:
            return
            # print("Longitude: \t\t %d°.%d W"%(int(bits_to_numbers(Longitude[1:]) / 600000), int((bits_to_numbers(Longitude[1:]) % 600000) / 60)))
        writeString += ","
        if Latitude[0] == "0":
            writeString += str(int(bits_to_numbers(Latitude[1:]) / 600000)) + "." + str(
                int((bits_to_numbers(Latitude[1:]) % 600000) / 60))
            # print("Latitude: \t\t %d°.%d N"%(int(bits_to_numbers(Latitude[1:]) / 600000), int((bits_to_numbers(Latitude[1:]) % 600000) / 60)))
        else:
            return
            # print("Latitude: \t\t %d°.%d S"%(int(bits_to_numbers(Latitude[1:]) / 600000), int((bits_to_numbers(Latitude[1:]) % 600000) / 60)))
        writeString += ","
        writeString +=  str(bits_to_numbers(COG) * 0.1) + "," + \
                        str(bits_to_numbers(HDG)) + "," + \
                        str(bits_to_numbers(Time_Stamp)) + "," + \
                        str(bits_to_numbers(Reserved_for_regional)) + "," + \
                        str(RAIM_flag) + "," + \
                        str(bits_to_numbers(Sync_state)) + "," + \
                        str(bits_to_numbers(Slot_Timeout)) + "," + \
                        str(bits_to_numbers(UTC_hour)) + "," + \
                        str(bits_to_numbers(UTC_minute))
        writeString += "\r\n"
        f.write(writeString)
        log.write(message + "decode: " + writeString)
        # print(message)
        # print(writeString)
        # print("Message Type: \t\t", bits_to_numbers(Message_Type))
        # print("Repeat Indicator: \t", bits_to_numbers(Repeat_Indicator))
        # print("MMSI: \t\t\t", bits_to_numbers(MMSI))
        # print("Navigation Status: \t", bits_to_numbers(Navigation_Status))
        # # TODO:ROT计算未完成，如下只输出其补码
        # print("ROT: \t\t\t", bits_to_Complementnumbers(ROT))
        # print("SOG: \t\t\t", bits_to_numbers(SOG) * 0.1, "kn")
        # print("Position Accuracy: \t", Position_Accuracy)
        # if Longitude[0] == "0":
        #     print("Longitude: \t\t %d°.%d E"%(int(bits_to_numbers(Longitude[1:]) / 600000), int((bits_to_numbers(Longitude[1:]) % 600000) / 60)))
        # else:
        #     print("Longitude: \t\t %d°.%d W"%(int(bits_to_numbers(Longitude[1:]) / 600000), int((bits_to_numbers(Longitude[1:]) % 600000) / 60)))
        # if Latitude[0] == "0":
        #     print("Latitude: \t\t %d°.%d N"%(int(bits_to_numbers(Latitude[1:]) / 600000), int((bits_to_numbers(Latitude[1:]) % 600000) / 60)))
        # else:
        #     print("Latitude: \t\t %d°.%d S"%(int(bits_to_numbers(Latitude[1:]) / 600000), int((bits_to_numbers(Latitude[1:]) % 600000) / 60)))
        # print("COG: \t\t\t", bits_to_numbers(COG) * 0.1)
        # print("HDG: \t\t\t", bits_to_numbers(HDG))
        # print("Time Stamp: \t\t", bits_to_numbers(Time_Stamp))
        # print("Reserved for regional: \t", Reserved_for_regional)
        # print("RAIM flag: \t\t", RAIM_flag)
        # # print("Communication State", Communication_State)
        # print("Sync state: \t\t", bits_to_numbers(Sync_state))
        # print("Slot Timeout: \t\t", bits_to_numbers(Slot_Timeout))
        # print("UTC hour: \t\t", bits_to_numbers(UTC_hour))
        # print("UTC minute: \t\t", bits_to_numbers(UTC_minute))
    else:
        # TODO:27种编码剩余完成
        # print("Message Type: \t\t", bits_to_numbers(Message_Type))
        return

# !AIVDM,1,1,0,B,16:b4BiP007WveP@taA000IN1P00,0*64
# !AIVDM,1,1,,A,169FsD001o8ewMhF8Bb997A@05K8,0*26
# !AIVDM,1,1,0,A,H6:VA;A0DpN1PT4pN3S3>222222,2*25