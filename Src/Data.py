import configparser
from collections.abc import Mapping, Sequence
from enum import Enum
from Province import Province
from Officer import Officer

class GameStatus():
    ShowLogo = 1
    DisplayMenu = 2
    ShowOthers =3
    WaitNumber = 4
    ShowMap = 5
    ShowCommands = 6
    ShowGenerals = 7
    ShowGenerals2 = 8

class InputMode():
    Alpha_OK = 1
    Number_Only = 2
    Number_YN_Only = 4

class ShowOfficerFlag():
    Empty = 0
    Int = 1
    War = 2
    Chm = 3
    Soldiers = 4
    Loyalty = 5
    Weapons = 6

class DelegateMode():
    No = 0
    Directly = 1
    Full = 4
    Internal = 5
    Military = 6
    Person = 7

class Data(object):
    GamePath = "../Resources/"
    SaveData = None
    KAODATA = None
    PACKDATA = None
    MONTAGE = None
    HEXDATA = None
    GRPDATA = None
    TAIKI = None
    SCENARIO = None
    OPENING = None
    MSG16P = None
    NAME16P = None
    CHARACTER = None
    LOGOTEXT = None
    CNINDEX = {}
    MaxNumberOfGenerals = 255
    BUF = None
    Status = None
    InputMode = InputMode.Alpha_OK
    DSBUF = []

    SettingsFileName = "settings.txt"
    DATA_OFFSET = 0x38
    PROVINCE_START = 0x2D8C+DATA_OFFSET
    PROVINCE_SIZE = 0x23
    RULER_START = 0x2AFC+DATA_OFFSET
    RULER_SIZE = 0x29

    OFFSET = 0x38
    OFFICER_OFFSET = 0x20+OFFSET
    OFFICER_SIZE = 0x2B
    PROVINCE_OFFSET = 0X2D8C+OFFSET
    PROVINCE_SIZE = 0x23
    RULER_OFFSET = 0x2AFC+OFFSET
    RULER_SIZE = 0x29
    CURRENT_RULER_OFFSET = 0x335c+OFFSET
    CURRENT_RULER_OFFICER_OFFSET = 0x335e + OFFSET
    CURRENT_PROVINCE_OFFSET = 0x3362+OFFSET
    GAME_DIFFCULTY_OFFSET = 0x337B + OFFSET
    GAME_DIFFCULTY = 1
    NUMBER_OF_RULERS = 0
    NUMBER_OF_RULERS_OFFSET = 0x47 + OFFSET
    OfficerList = Sequence[Province]
    ProvinceList = Sequence[Province]
    RULER_AS_OFFICER_OFFSET = 0x2ACA + OFFSET
    FOLLOWER_OFFSET = 0x2A9F + OFFSET
    PROVINCE_DESC = None

    RulerPalette = []

    with open(GamePath + "kaodata.dat", "rb") as f:
        KAODATA = bytearray(f.read(210240))

    with open(GamePath + "montage.dat", "rb") as f:
        MONTAGE = bytearray(f.read(50688))

    with open(GamePath + "scenario.dat", "rb") as f:
        SCENARIO = bytearray(f.read(79386))

    with open(GamePath + "taiki.dat", "rb") as f:
        TAIKI = bytearray(f.read(79386))

    with open(GamePath + "hexdata.dat", "rb") as f:
        HEXDATA = bytearray(f.read(15108))

    with open(GamePath + "grpdata.dat", "rb") as f:
        GRPDATA = bytearray(f.read(46715))

    with open(GamePath + "packdata.dat", "rb") as f:
        PACKDATA = bytearray(f.read(65661))

    with open(GamePath + "opening.dat", "rb") as f:
        OPENING = bytearray(f.read(113514))

    with open(GamePath + "msg.16p", "rb") as f:
        MSG16P = bytearray(f.read(34500))

    with open(GamePath + "name.16p", "rb") as f:
        NAME16P = bytearray(f.read(358820))

    with open(GamePath + "character.8p", "rb") as f:
        CHARACTER = bytearray(f.read(6384))

    with open(GamePath + "cnindex.dat", "rb") as f:
        buf = bytearray(f.read(2312))
        for i in range(0, len(buf), 2):
            CNINDEX[(buf[i + 1] << 8) + (buf[i + 0])] = int(i / 2)

    with open(GamePath+"dsbuf.dat","rb") as f:
        #DSBUF = list(f.read())[0x3FD0:0x9f92]
        DSBUF = list(f.read())
        for i in range(0,6):
            DSBUF[0xAFF6+i] = i

    with open(GamePath + "province.des", "rb") as f:
        tmp = bytearray(f.read(833))
        i = 0

        buf=[]
        buf2=[]
        buf3 = []
        while True:
            if i>=len(tmp):
                break

            b = tmp[i]
            if b==0:
                buf2.append("".join(buf3))
                buf.append(buf2)
                buf2=[]
                buf3=[]
                i+=1
            elif b==0x0A:
                buf2.append("".join(buf3))
                buf3=[]
                i+=1
            elif b<0x80:
                buf3.append(chr(b))
                i+=1
            else:
                b2 = tmp[i+1]
                zh_cn = CNINDEX.get(b*256+b2)
                if zh_cn is not None:
                    buf3.append("$")
                    buf3.append(str(zh_cn))
                    i += 2
                    buf3.append("$")

        PROVINCE_DESC = buf.copy()

    with open(GamePath + "logotext.dat", "rb") as f:
        buf = bytearray(f.read(198))
        page = 0
        LOGOTEXT = {}

        i = 0
        tmp = []
        while True:
            if i>=len(buf):
                break
            if buf[i]>=0x80:
                tmp.append(CNINDEX[buf[i+0]*256+buf[i+1]])
                i+=2
            elif buf[i]==0:
                LOGOTEXT[page] = tmp
                tmp = []
                page += 1
                i+=1
            else:
                i+=1

            with open(GamePath + "h.bin", "rb") as f:
                tmp_buf = f.read(0x58)

            with open(GamePath + "s1", "rb") as f:
                tmp_buf2 = f.read(30752)

            BUF = bytearray(tmp_buf) + bytearray(tmp_buf2)[0x20:]
            RulerPalette = bytearray(tmp_buf2)[0x10:0x20]

    MapIndex = [[0, 0, 0, 0, 0, 2, 1, 0],
                      [0, 0, 0, 4, 3, 6, 0, 0],
                      [0, 0, 0, 5, 7, 9, 8, 0],
                      [15, 0, 0, 11, 10, 17, 16, 24],
                      [14, 13, 12, 20, 19, 28, 18, 25],
                      [0, 30, 29, 31, 21, 22, 27, 26],
                      [0, 33, 32, 40, 23, 38, 37, 0],
                      [0, 35, 34, 41, 39, 0, 0, 0],
                      [0, 0, 36, 0, 0, 0, 0, 0]]

    # Text={}
    # conf = configparser.ConfigParser()
    # conf.read(GamePath + "text_zhtw.txt", encoding="utf-8")
    # for o in conf.options("text"):
    #     Text[o] = conf.get("text",o)

    Status = GameStatus.ShowLogo

    GrpdataMappings = {
        # all width is (top 2 bytes+3)/4, 80 02 means:(0x280+3)/4=0xa0
        "MainMenu": [0x00, 0x00,0x00],
        "Map": [0x37ae, 0x00,0x00],
        "MapTop": [0x62B2, 0x128,0x00],
        "MapBottom": [0x6951,0x128, 0x3d],
        "MapHead": [0x696a,0x200, 0x04],
        "jiemeng": [0x6a18,0x138, 0x48],
        "Transit": [0x731f,0x138, 0x48],
        "SendFood": [0x7bec,0x138, 0x48],
        "Letter": [0x85f0,0x1c0, 0x44],
        "SomeWeather": [0x881f,0x1f0, 0x28],
        "Sunny": [0x8990, 0x1f0, 0x28],
        "Cloud": [0x8b44, 0x1f0, 0x28],
        "Rain": [0x8d2a, 0x1f0, 0x28],
        "WarMenu": [0x8f52,0x1a0, 0x0],
    }


