from collections.abc import Mapping, Sequence
from Province import Province
from Officer import Officer
from Ruler import Ruler
from Data import Data,ShowOfficerFlag,DelegateMode

class RoTK2(object):


    ProvinceList = Sequence[Province]

    @staticmethod
    def Init():
        Data.OfficerList = RoTK2.GetOfficerList()
        Data.ProvinceList = RoTK2.GetProvinceList()

        Data.GAME_DIFFCULTY = int(Data.BUF[Data.GAME_DIFFCULTY_OFFSET])
        Data.NUMBER_OF_RULERS = int(Data.BUF[Data.NUMBER_OF_RULERS_OFFSET])
    @staticmethod
    def GetProvinceList()->Sequence[Province]:
        start = Data.PROVINCE_OFFSET
        size = Data.PROVINCE_SIZE

        city_names = ["幽州", "幷州", "冀州", "青州", "兗州", "司州", "雍州", "涼州", "徐州", "予州", "荊州", "揚州", "益州", "交州"]

        plist = []
        for i in range(0, 41):
            p = Province()

            city_data = Data.BUF[start + i * size:start + i * size + size]

            x = city_data[0x20]
            y = city_data[0x21]
            p.X = x
            p.Y = y
            name_index = city_data[0x22]
            p.NameIndex = name_index
            p.No = Data.MapIndex[y][x]
            p.Name = city_names[name_index] + "-" + str(p.No)
            p.Offset = start + i * size
            p.NextProvince = (city_data[0x01]<<8)+city_data[0x00]
            p.RulerNo = city_data[0x10]

            p.WarRulerNo = city_data[0x11]
            daili = city_data[0x12]
            zhanzhengjun = city_data[0x14]
            yunshujun = city_data[0x15]

            p.Governor = (city_data[0x03]<<8)+city_data[0x02]
            p.FirstUnClaimedOfficerOffset = (city_data[0x05] << 8) + city_data[0x04]
            p.FreeOfficerOffset = (city_data[0x07] << 8) + city_data[0x06]

            daili_mappings = {0: "",3:"未知", 4: "全权", 5: "内政", 6: "军事", 7: "人事"}
            if daili < 8:
                p.DelegateControl = daili_mappings[daili]

            if yunshujun < 41:
                name_index = Data.BUF[start + size * yunshujun + size - 1]
                p.ProvinceSendGoods = city_names[name_index] + "-" + str(yunshujun + 1)
            if zhanzhengjun < 41:
                name_index = Data.BUF[start + size * zhanzhengjun + size - 1]
                p.ProvinceInvade = city_names[name_index] + "-" + str(name_index + 1)

            p.Gold = (city_data[0x09]<<8)+city_data[0x08]
            p.Food = (city_data[0x0D] << 24) + (city_data[0x0C] << 16) + (city_data[0x0B] << 8) + city_data[0x0A]
            p.Population = ((city_data[0x0F]<<8)+city_data[0x0E]) * 100
            p.Land = city_data[0x16]
            p.Loyalty = city_data[0x17]
            p.Flood = city_data[0x18]
            p.Horses = city_data[0x19]
            p.Castle = city_data[0x1A]
            p.RicePrice = city_data[0x1B]

            s = 0
            next = (city_data[0x03]<<8)+city_data[0x02]
            olist = []
            while next > 0:
                gen = RoTK2.GetOfficerByOffset(next)
                s += gen.Soldiers
                olist.append(gen)
                next = gen.NextOfficerOffset

            p.ClaimedOfficerNumber = len(olist)
            p.Soldiers = s

            p.UnClaimedOfficerNumber = 0
            p.UnclaimedOfficerList = []
            if p.FirstUnClaimedOfficerOffset>0:
                p.UnClaimedOfficerNumber = 1
                gen = RoTK2.GetOfficerByOffset(p.FirstUnClaimedOfficerOffset)
                gen.IsUnClaimed = True
                p.UnclaimedOfficerList.append(gen)
                #olist.append(gen)
                next = gen.NextOfficerOffset
                while next>0:
                    gen = RoTK2.GetOfficerByOffset(next)
                    gen.IsUnClaimed = True
                    #olist.append(gen)
                    next = gen.NextOfficerOffset
                    p.UnClaimedOfficerNumber += 1
                    p.UnclaimedOfficerList.append(gen)

            p.FreeOfficerNumber = 0
            if p.FreeOfficerOffset>0:
                gen = RoTK2.GetOfficerByOffset(p.FreeOfficerOffset)
                gen.IsFree = True
                p.FreeOfficerNumber += 1
                #olist.append(gen)

                next = gen.NextOfficerOffset
                while next > 0:
                    gen = RoTK2.GetOfficerByOffset(next)
                    gen.IsFree = True
                    #olist.append(gen)
                    next = gen.NextOfficerOffset
                    p.FreeOfficerNumber += 1

            p.OfficerList = olist

            plist.append(p)

        return plist

    @staticmethod
    def GetOfficerName(gen_offset):
        if gen_offset=="":
            return ""
        ruler_name_data = ""
        index = 0
        while True:
            if index>12:
                break
            if Data.BUF[gen_offset+0x1c+index]==0:
                break

            if Data.BUF[gen_offset+0x1c+index+0]<0x80:
                ruler_name_data += chr(Data.BUF[gen_offset+0x1c+index+0])
                index += 1
                continue

            s = Data.BUF[gen_offset+0x1c+index+0]*256+Data.BUF[gen_offset+0x1c+index+1]

            if s not in [0xD8F0,0xD8F1,0xD8F2,0xD8F3,0xD8F4,0xD8F5]:
                ruler_name_data+="$"+str(Data.CNINDEX[s])+"$"
            else:
                ruler_name_data+="$"+str(s)+"$"
            index+=2

        return ruler_name_data
    @staticmethod
    def GetOfficerList()->Sequence[Officer]:
        pos = Data.OFFICER_OFFSET
        size = Data.OFFICER_SIZE

        gen_no = 0
        olist  = []

        while True:
            tmp = RoTK2.GetOfficerFromBuffer(Data.BUF[pos + size * gen_no:pos + size * gen_no + size], gen_no, Data.BUF[0x45] * 256 + Data.BUF[0x44])
            olist.append(tmp)

            gen_no += 1
            if gen_no > Data.MaxNumberOfGenerals:
                break

        empty_officer = Officer()
        empty_officer.Offset = 0
        empty_officer.name = ""

        empty_king = Officer()
        empty_king.Offset = 255
        empty_king.name = ""

        olist.append(empty_officer)
        olist.append(empty_king)

        return olist

    @staticmethod
    def GetProvinceByOffset(offset)->Province:
        ret = None

        for c in RoTK2.GetProvinceList():
            if c.Offset == offset:
                ret = c
                break

        return ret

    @staticmethod
    def GetProvinceBySequence(sequence)->Province:
        return RoTK2.GetProvinceList()[sequence-1]

    @staticmethod
    def GetCurrentProvinceNo():
        return RoTK2.GetProvinceByOffset((Data.BUF[Data.CURRENT_PROVINCE_OFFSET+1] << 8) + Data.BUF[Data.CURRENT_PROVINCE_OFFSET]).No

    @staticmethod
    def GetProvincesByRulerNo(ruler_no)->Sequence[Province]:
        plist = []
        for p in RoTK2.GetProvinceList():
            if p.RulerNo==ruler_no:
                plist.append(p)

        return plist
    @staticmethod
    def FlushData():
        for p in Province.Init():
            off = RoTK2.PROVINCE_OFFSET+(p.No-1)*RoTK2.PROVINCE_SIZE
            Data.BUF[off+0x00] = p.NextProvince%256
            Data.BUF[off + 0x01] = p.NextProvince >>8
            Data.BUF[off + 0x10] = p.RulerNo
            Data.BUF[off + 0x11] = p.WarRulerNo

            Data.BUF[off + 0x02] = (p.Governor+0x38) % 256
            Data.BUF[off + 0x03] = (p.Governor+0x38) >>8
            Data.BUF[off + 0x08] = p.Gold%256
            Data.BUF[off + 0x09] = p.Gold>>8
            Data.BUF[off + 0x0A] = p.Food % 256
            Data.BUF[off + 0x0B] = (p.Food >> 8) % 256
            Data.BUF[off + 0x0C] = (p.Food >> 16) % 256
            Data.BUF[off + 0x0D] = p.Food >> 24
            Data.BUF[off + 0x0E] = int((p.Population/100)) % 256
            Data.BUF[off + 0x0F] = int((p.Population/100)) >>8

            Data.BUF[off + 0x16] = p.Land
            Data.BUF[off + 0x17] = p.Loyalty

            Data.BUF[off + 0x18] = p.Flood
            Data.BUF[off + 0x19] = p.Horses
            Data.BUF[off + 0x1A] = p.Castle
            Data.BUF[off + 0x1B] = p.RicePrice

    @staticmethod
    def ReOrderOfficers(prov_no, flag:ShowOfficerFlag):
        officer_list = RoTK2.GetProvinceBySequence(prov_no).OfficerList
        if len(officer_list)<1:
            return

        governor = officer_list[0]
        if len(officer_list)>1:
            new_list = []
            for o in officer_list[1:]:
                if o.IsUnClaimed or o.IsFree:
                    continue
                new_list.append(o)

            if flag==ShowOfficerFlag.Int:
                olist = sorted(new_list,key=lambda x:x.Int,reverse=True)
            elif flag==ShowOfficerFlag.War:
                olist = sorted(new_list,key=lambda x:x.War,reverse=True)
            elif flag==ShowOfficerFlag.Chm:
                olist = sorted(new_list,key=lambda x:x.Chm,reverse=True)
            elif flag==ShowOfficerFlag.Soldiers:
                olist = sorted(new_list,key=lambda x:x.Soldiers,reverse=True)
            elif flag==ShowOfficerFlag.Loyalty:
                olist = sorted(new_list,key=lambda x:x.Loyalty,reverse=True)
            else:
                raise Exception("Invalid sorted flag.")

            governor.NextOfficerOffset = olist[0].Offset
            RoTK2.FlushOfficer(governor)

            for i in range(0,len(olist)):
                if i==len(olist)-1:
                    olist[i].NextOfficerOffset = 0
                else:
                    olist[i].NextOfficerOffset = olist[i+1].Offset

                RoTK2.FlushOfficer(olist[i])

            Data.OfficerList = RoTK2.GetOfficerList()
            Data.ProvinceList = RoTK2.GetProvinceList()

    @staticmethod
    def FlushOfficer(officer:Officer):
        Data.BUF[officer.Offset + 0x00] = officer.NextOfficerOffset % 256
        Data.BUF[officer.Offset + 0x01] = officer.NextOfficerOffset >> 8

        Data.BUF[officer.Offset + 0x04] = officer.Int
        Data.BUF[officer.Offset + 0x05] = officer.War
        Data.BUF[officer.Offset + 0x06] = officer.Chm
        Data.BUF[officer.Offset + 0x07] = officer.yili
        Data.BUF[officer.Offset + 0x08] = officer.rende
        Data.BUF[officer.Offset + 0x09] = officer.yewang
        Data.BUF[officer.Offset + 0x0A] = officer.RulerNo
        Data.BUF[officer.Offset + 0x0B] = officer.Loyalty
        Data.BUF[officer.Offset + 0x12] = officer.Soldiers % 256
        Data.BUF[officer.Offset + 0x13] = officer.Soldiers >> 8
        Data.BUF[officer.Offset + 0x14] = officer.Weapons % 256
        Data.BUF[officer.Offset + 0x15] = officer.Weapons >> 8
        Data.BUF[officer.Offset + 0x16] = officer.TrainingLevel

        Data.BUF[officer.Offset + 0x0C] = officer.shiwei
        Data.BUF[officer.Offset + 0x0D] = officer.SpyBlongedToRuler

        Data.BUF[officer.Offset + 0x0E] = officer.SpyInCityNo
        Data.BUF[officer.Offset + 0x0F] = officer.xiangxing

        Data.OfficerList = RoTK2.GetOfficerList()

    def FlushProvince(province:Province):
        Data.BUF[province.Offset + 0x00] = province.NextProvince % 256
        Data.BUF[province.Offset + 0x01] = province.NextProvince >> 8
        Data.BUF[province.Offset + 0x02] = province.Governor % 256
        Data.BUF[province.Offset + 0x03] = province.Governor >> 8
        Data.BUF[province.Offset + 0x04] = province.FirstUnClaimedOfficerOffset % 256
        Data.BUF[province.Offset + 0x05] = province.FirstUnClaimedOfficerOffset >> 8
        Data.BUF[province.Offset + 0x06] = province.FreeOfficerOffset % 256
        Data.BUF[province.Offset + 0x07] = province.FreeOfficerOffset >> 8
        Data.BUF[province.Offset + 0x08] = province.Gold % 256
        Data.BUF[province.Offset + 0x09] = province.Gold >> 8
        Data.BUF[province.Offset + 0x0A] = province.Food % 256
        Data.BUF[province.Offset + 0x0B] = (province.Food >> 8) % 256
        Data.BUF[province.Offset + 0x0C] = (province.Food >> 16) % 256
        Data.BUF[province.Offset + 0x0D] = province.Food >> 24
        Data.BUF[province.Offset + 0x0E] = int((province.Population / 100)) % 256
        Data.BUF[province.Offset + 0x0F] = int((province.Population / 100)) >> 8
        Data.BUF[province.Offset + 0x10] = province.RulerNo
        Data.BUF[province.Offset + 0x11] = province.WarRulerNo
        # TODO: 12~15
        Data.BUF[province.Offset + 0x16] = province.Land
        Data.BUF[province.Offset + 0x17] = province.Loyalty
        Data.BUF[province.Offset + 0x18] = province.Flood
        Data.BUF[province.Offset + 0x19] = province.Horses
        Data.BUF[province.Offset + 0x1A] = province.Castle
        Data.BUF[province.Offset + 0x1B] = province.RicePrice

        Data.ProvinceList = RoTK2.GetProvinceList()

    @staticmethod
    def GetOfficeName(name1, name2, name3, name4, name5, name6):
        name_list = {0xaba6: "劉", 0xab9f: "備", 0xFB92: "公", 0x309B: "孫", 0xBBAE: "瓚", 0xBCA1: "越", 0xEA9C: "馬",
                     0xD5AD: "騰",0xD0A4:"廖",0x46A8:"賢",0x669E:"淳",0xCDAC:"瓊",0x4A94:"仲",0xD7A5:"興",0xD998:"姜",0xC3A5:"維",0xF7A7:"誕",0x949E:"爽",
                     0x8D98: "候", 0xD8A9: "選", 0x32A1: "程", 0x6DA6: "銀",0xD2AA:"禅",0x509B:"師",
                     0x59AD: "關", 0xD094: "羽", 0xAE9D: "張", 0x9A9A: "飛",0x8B98:"信",
                     0X989F: "陶", 0X65AB: "謙", 0XF09C: "乾",
                     0X949F: "陳", 0XF3A0: "登", 0XDCAA: "糜", 0X3998: "竺",
                     0X5398: "芳",
                     0XF0D8: "马",0XF1D8: "述",0XF2D8: "杰",0XF3D8: "屈",0XF4D8: "世",0XF5D8: "宏",
                     0XAF9C: "袁", 0X4A9F: "術", 0X479A: "胤", 0XF899: "紀",
                     0XF0AE: "靈", 0X56A7: "樂", 0XF29F: "就", 0XB9A8: "動",
                     0X949F: "陳", 0X31AE: "蘭", 0XD695: "李", 0X58AC: "豐",
                     0X74A4: "雷", 0X41AB: "薄", 0X6E9D: "堅",
                     0X77A0: "普", 0X42A1: "策", 0X36A2: "黃", 0XE3A5: "蓋",

                     0XA6AB: "韓", 0X4BA3: "當", 0XD2D4: "闞", 0X41A9: "澤",
                     0XB694: "朱", 0XD897: "治", 0X399E: "曹", 0XE6A8: "操",
                     0X369B: "宮", 0X42A1: "策", 0XED9A: "夏", 0X8D98: "侯",
                     0X789E: "淵", 0XCF9D: "惇", 0X9C99: "洪", 0X9C97: "昂",
                     0XED92: "仁", 0XCFA1: "進", 0X619C: "純", 0X6C98: "表",

                     0X6AC6: "蒯", 0X5696: "良", 0X8AA2: "嵩",
                     0X36A2: "黃", 0X439C: "祖", 0XDAA7: "蔡", 0XA298: "冒",
                     0X9B95: "宋", 0X5697: "忠", 0X6EA8: "鄧", 0X99A3: "義",
                     0X6293: "文", 0X9DA3: "聘", 0XA3A7: "磐", 0X6495: "呂",
                     0XFB92: "公", 0X909E: "焉", 0X85AD: "嚴", 0X8EAC: "顏",
                     0X6295: "吳", 0X81AE: "懿", 0X4C94: "任", 0XB9A3: "董",
                     0XCE96: "和", 0XB7A1: "貴", 0X74A4: "雷", 0X6D94: "同",
                     0X88A7: "璋", 0X4695: "冷", 0X629A: "苞", 0XEC9C: "高", 0XEB95: "沛", 0XCDA2: "楊", 0XB4AC: "懷",
                     0XD49E: "紹", 0XEF93: "田", 0X76A5: "熙", 0XFDAC: "譚", 0XFD96: "尚", 0X879F: "郭", 0XB6A4: "圖",
                     0X8DA2: "幹",
                     0X39AE: "覽", 0XCFA0: "焦", 0XBCAD: "觸",
                     0XCFA6: "審", 0XD89C: "配", 0XE5CD: "嶷", 0XD397: "沮", 0XE59D: "受", 0X89A8: "震", 0X4D97: "延",
                     0X8CAB: "醜",
                     0X829F: "逢", 0XB696: "卓", 0XF1A3: "賈",
                     0X6AC3: "詡", 0XCB93: "布", 0X7AA1: "華", 0XF3A1: "雄", 0XAFA8: "儒", 0X64A1: "肅", 0X54A7: "樊",
                     0X81A3: "稠",
                     0X439A: "胡", 0XECBF: "軫",
                     0X579B: "徐", 0X39A5: "榮", 0XDAB0: "汜", 0X39B3: "旻", 0XA3AA: "濟", 0X33AC: "繍", 0XB5BC: "傕",
                     0XF0A3: "資",
                     0X4DA6: "趙", 0XA395: "岑", 0X7A93: "王",
                     0X979B: "朗", 0XBDA3: "虞", 0X38AC: "翻", 0XC5CE: "繇", 0X4A93: "太", 0XB793: "史", 0X96A2: "慈",
                     0X579A: "英",
                     0XBC97: "武",
                     0X97AC: "馥", 0X75A7: "潘", 0X9BA6: "鳳", 0X6C96: "辛", 0XA2A1: "評", 0X8A9A: "郃", 0XC09C: "豹",
                     0X4C93: "孔",
                     0XADA9: "融", 0X9994: "安", 0X6B9D: "國",
                     0X439E: "梁", 0XCA9A: "剛", 0XF7A1: "雲", 0XDF96: "奉", 0X8F9B: "晃", 0XF5AA: "翼", 0XDAA9: "遼",
                     0XC7A2: "楷",
                     0XD59C: "郝", 0X85A1: "萌", 0X589F: "許",
                     0X9CAC: "魏", 0XFCAD: "續", 0XA894: "成", 0XD3A8: "憲", 0X6BAC: "邈", 0XFAA1: "順", 0XA09C: "荀",
                     0XFCB6: "彧",
                     0XD295: "攸", 0XACA4: "嘉", 0X649B: "恩", 0X7199: "昱",
                     0XA796: "典", 0X959A: "韋", 0X81AA: "懋", 0XCBAA: "矯", 0XC7A6: "嬉", 0X95AB: "鐘", 0XAEA9: "衡",
                     0XBDA1: "超", 0X4DAE: "鐵", 0XA894: "成", 0XFA96: "宜", 0XF6A8: "橫", 0X3897: "岱", 0XB1AC: "龐",
                     0XE0A6: "德",
                     0X9CA9: "興", 0XF197: "玩", 0XF099: "秋", 0XB5A0: "湛",
                     0XF792: "允", 0XD196: "周", 0X4AA3: "瑜", 0XDFA5: "蒙", 0XD196: "周", 0XB89B: "泰", 0XA292: "丁",
                     0XDF96: "奉",
                     0XA6A8: "魯", 0XEEA9: "閻", 0XE69A: "圃", 0XEBA7: "衛",
                     0XCC93: "平", 0XB397: "松", 0X8A99: "柏", 0XB5A1: "費", 0XDCA3: "詩", 0X83AE: "權", 0XDA9E: "累",
                     0X5694: "全",
                     0X9FBE: "琮", 0XD2A0: "然", 0XAEA7: "範", 0X57AE: "顧",
                     0X70A4: "雍", 0X959F: "陸", 0XE3AA: "績", 0XAB9E: "巽", 0XE295: "步", 0XEDD6: "騭？", 0X9C9B: "桓",
                     0X959F: "陸", 0X57A6: "遜", 0XBABB: "翊", 0X97B8: "纮", 0X6B99: "昭",
                     0X92AE: "襲", 0XF898: "度", 0XE09B: "珪", 0XE6A0: "琦", 0XD29E: "統", 0XBE9A: "倉", 0XFBAB: "簡",
                     0XC49A: "淩",
                     0XD498: "奕", 0X64A5: "滿",
                     0XFCA5: "褚", 0XB293: "司", 0X4894: "休", 0X96D3: "顗", 0XB198: "南", 0XB9AC: "曠", 0X5AA1: "翔",
                     0X77C1: "楙",
                     0X53AE: "霸", 0X7893: "牛", 0X7698: "金", 0XB99A: "修", 0X4E9D: "商", 0XDA95: "杜", 0XA59D: "常",
                     0XF79B: "真", 0X739F: "通", 0XF998: "建", 0XAA9F: "傅", 0XBF92: "于", 0X77A3: "禁", 0XA49C: "虔",
                     0XD9A7: "蔣",
                     0XB1A0: "渠", 0X309E: "旋", 0X8EA8: "鞏", 0XB495: "志", 0X4C9A: "範", 0X78AA: "應",
                     0X4BAA: "鮑", 0X54AA: "龍", 0X7496: "刑", 0X42A4: "道", 0XE793: "玄", 0XE0AD: "齡", 0X7799: "柔",
                     0XF9A7: "諸",
                     0XB5A3: "葛", 0X8A98: "亮", 0XEB98: "封", 0XDCA6: "廣", 0X5A9C: "索", 0X36A0: "循", 0XA0BE: "琬",
                     0X6F9B: "拳", 0X8AA7: "瑾", 0XEB93: "甘", 0XCEA4: "寧", 0X3598: "秉", 0XF796: "宗", 0X7197: "承",
                     0XEAA2: "溫",
                     0X47AB: "薛", 0XB6A5: "綜", 0XEBD5: "騭", 0XE3A4: "彰", 0X8293: "丕", 0X99A0: "植", 0X9BA3: "群",
                     0X6F93: "毛", 0XACB3: "玠", 0XE398: "威", 0XEFA8: "曄", 0XC79B: "浩", 0XAB9D: "庶", 0X6794: "匡",
                     0X67B5: "毘",
                     0X9CC1: "歆", 0XF496: "孟", 0XBCAA: "獲", 0XB8D1: "闿", 0X56AA: "優",
                     0XB794: "朵", 0X3799: "思", 0X8098: "阿", 0XC3A2: "會", 0XBEAA: "環", 0X4EA1: "結", 0XF896: "定",
                     0X3695: "余",
                     0XC293: "奴", 0XB0BE: "畯", 0X69AB: "謝", 0X319E: "旌",
                     0XA5CA: "鲂", 0XB59E: "盛", 0X4294: "伉", 0XB29F: "凱", 0XDC9B: "班", 0X5498: "芝", 0XCD97: "法",
                     0XDE93: "正",
                     0XC3C5: "祎", 0XF6A9: "霍", 0X479B: "峻", 0X44A4: "達",
                     0XD0AC: "疆", 0XE0A4: "廖", 0X3693: "化", 0X879E: "淮", 0X43A0: "惠", 0X6ACF: "謖", 0XB0AC: "寵",
                     0XA194: "式",
                     0X37AF: "觀", 0X4494: "伊", 0XA5AD: "籍",
                     0XC892: "士", 0XAAAA: "濬", 0X6998: "虎", 0XA2A0: "欽", 0X9AC2: "粲", 0XCCA1: "逵", 0XF0AB: "禮",
                     0XAE95: "彤",
                     0XE592: "之", 0X78A4: "靖", 0X4B99: "恪",
                     0XDF93: "母", 0X8493: "丘", 0XA6A6: "儉", 0XE394: "艾", 0XC5CA: "叡", 0x4699: "恢", 0xE692: "尹", 0x52AA: "默",
                     0x5193: "巴",0xA0A6: "儀", 0x85AC: "双", 0x82A1: "著",0xE695:"沙",0xF6A6:"摩",0xAA93:"可",0xEFA7:"褒",0x43A4:"遂",0xEEA8:"暹"
                     }

        name1_1 = name1>>8
        name1_2 = name1 & 0xff
        name2_1 = name2>>8
        name2_2 = name2 & 0xff
        name3_1 = name3>>8
        name3_2 = name3 & 0xff
        name4_1 = name4 >> 8
        name4_2 = name4 & 0xff
        name5_1 = name5 >> 8
        name5_2 = name5 & 0xff
        name6_1 = name6 >> 8
        name6_2 = name6 & 0xff


        if name1+name2+name3+name4+name5+name6==0:
            return ""

        if  name1_1<0x80 and name1_2<0x80 and name2_1<0x80 and name2_2<0x80 and name3_1<0x80 and name3_2<0x80 and name4_1<0x80 and name4_2<0x80 and name5_1<0x80 and name5_2<0x80 and name6_1<0x80 and name6_2<0x80:
            name = chr(name1_2)+chr(name1_1)+chr(name2_2)+chr(name2_1)+chr(name3_2)+chr(name3_1)+chr(name4_2)+chr(name4_1)+chr(name5_2)+chr(name5_1)+chr(name6_2)+chr(name6_1)
            return name.replace("\0","")

        name = ""
        if name_list.__contains__(name1):
            name += name_list[name1]
        else:
            name += "0X{0:X}".format(name1)

        if name2 > 0:
            if name_list.__contains__(name2):
                name += name_list[name2]
            else:
                name += "0X{0:X}".format(name2)

        if name3 > 0:
            if name_list.__contains__(name3):
                name += name_list[name3]
            else:
                name += "0X{0:X}".format(name3)

        if name4 > 0:
            if name_list.__contains__(name4):
                name += name_list[name4]
            else:
                name += "0X{0:X}".format(name4)
        if name5 > 0:
            if name_list.__contains__(name5):
                name += name_list[name5]
            else:
                name += "0X{0:X}".format(name5)
        if name6 > 0:
            if name_list.__contains__(name6):
                name += name_list[name6]
            else:
                name += "0X{0:X}".format(name6)

        return name

    @staticmethod
    def IsRuler(officer:Officer):
        for i in range(0, 16):
            if officer.Offset == Data.BUF[Data.RULER_START + Data.RULER_SIZE * i + 1] * 256 +Data.BUF[Data.RULER_START + Data.RULER_SIZE * i]:
                return True
        return False

    @staticmethod
    def IsAdvisor(officer:Officer):
        for i in range(0, 16):
            if officer.Offset == Data.BUF[Data.RULER_START + Data.RULER_SIZE * i + 5] * 256 +Data.BUF[Data.RULER_START + Data.RULER_SIZE * i + 4]:
                return True

        return False

    @staticmethod
    def GetAdvisor():
        current_ruler_offset = Data.BUF[Data.CURRENT_RULER_OFFSET+1]*256+Data.BUF[Data.CURRENT_RULER_OFFSET]
        ruler_no = int((Data.RULER_OFFSET - current_ruler_offset)/Data.RULER_SIZE)
        advisor_offset = Data.BUF[current_ruler_offset+5]*256+Data.BUF[current_ruler_offset+4]
        return RoTK2.GetOfficerByOffset(advisor_offset)

    @staticmethod
    def GetAdvisorProvince():
        advisor = RoTK2.GetAdvisor()
        if advisor is not None:
            for p in RoTK2.GetProvinceList():
                for o in p.OfficerList:
                    if o.Offset == advisor.Offset:
                        return p.No

        return -1

    @staticmethod
    def GetSimahui():
        return Data.BUF[0x2B30] + 1

    @staticmethod
    def GetXuzijiang():
        return Data.BUF[0x2B31] + 1

    @staticmethod
    def GetRulerProvinceNo(province_offset):
        return int((province_offset - 0x2DC4)/0x23)

    @staticmethod
    def GetHuatuo():
        return Data.BUF[0x2B32]

    @staticmethod
    def IsGoverner(officer:Officer):
        for i in range(0, 41):
            if officer.Offset == Data.BUF[Data.PROVINCE_START + Data.PROVINCE_SIZE * i  + 3] * 256 + Data.BUF[Data.PROVINCE_START + Data.PROVINCE_SIZE * i  + 2]:
                return True
        return False

    @staticmethod
    def GetOfficerFromBuffer(buffer, gen_no, year)->Officer:
        o = Officer()
        o.Offset = Data.OFFICER_OFFSET + Data.OFFICER_SIZE * gen_no
        o.NextOfficerOffset = (buffer[0x01] << 8) + buffer[0x00]

        o.Name = RoTK2.GetOfficeName((buffer[0x1D] << 8) + buffer[0x1C], (buffer[0x1F] << 8) + buffer[0x1E], (buffer[0x21] << 8) + buffer[0x20],
                           (buffer[0x23] << 8) + buffer[0x22], (buffer[0x25] << 8) + buffer[0x24], (buffer[0x27] << 8) + buffer[0x26]
                           )
        o.Int = buffer[0x04]
        o.War = buffer[0x05]
        o.Chm = buffer[0x06]
        o.yili = buffer[0x07]
        o.rende = buffer[0x08]
        o.yewang = buffer[0x09]
        o.RulerNo = buffer[0x0A]
        o.Loyalty = buffer[0x0B]
        o.shiwei = buffer[0x0C]
        o.SpyBlongedToRuler = buffer[0x0D]
        o.SpyInCityNo = buffer[0x0E]
        o.xiangxing = buffer[0x0F]

        o.xueyuan = (buffer[0x11] << 8) + buffer[0x10]
        o.Soldiers = (buffer[0x13] << 8) + buffer[0x12]
        o.Weapons = (buffer[0x15] << 8) + buffer[0x14]
        if o.Soldiers==0:
            o.Arms = 100
        else:
            o.Arms = min(int((100*o.Weapons)/o.Soldiers),100)
        o.TrainingLevel = buffer[0x16]
        o.Age = year - buffer[0x19] + 1

        o.IsSick = (buffer[0x03] &0x0f)>0
        o.SickMonth = buffer[0x03] & 0x0f

        o.WillDieInNextYear = buffer[0x02] >> 4
        o.CanMoveNow = ((buffer[0x02] & 0x0f) != 1)
        o.MonthCannotMove = buffer[0x03] >> 4
        o.Portrait = (buffer[0x1B] << 8) + buffer[0x1A] - 1
        return o

    @staticmethod
    def GetOfficerByOffset(offset)->Officer:
        if offset==0:
            return None

        if (offset - Data.OFFICER_OFFSET)%Data.OFFICER_SIZE>0:
            raise Exception("Invalid officer offset.")

        seq = int((offset - Data.OFFICER_OFFSET)/Data.OFFICER_SIZE)

        return RoTK2.GetOfficerFromBuffer(Data.BUF[offset:offset+Data.OFFICER_SIZE],seq,Data.BUF[0x45]*256+Data.BUF[0x44])

    @staticmethod
    def GetStoredOfficerList(seq):
        gamedata = bytearray(RoTK2.SCENARIO)
        size = 0x2b

        pos_list = [0x16,0x33c5,0x6774,0x9b23,0xced2,0x10281]
        year_list = [189,194,201,208,215,220]
        pos = pos_list[seq]
        #for pos in pos_list:
        gen_no = 0
        gen_list = []

        while True:
            gen = gamedata[pos + size * gen_no:pos + size * gen_no + size]
            tmp = RoTK2.GetOfficerFromBuffer(gen, gen_no, pos, size, year_list[seq])

            gen_no += 1

            if tmp.Int==0 and tmp.War==0 and tmp.Chm==0:
                break

            gen_list.append(tmp)

            gen_no += 1

        print("===============================================")

        return gen_list

    @staticmethod
    def get_taiki_gen_list():
        gamedata = RoTK2.TAIKI
        size = 0x2E

        pos = 0
        gen_no = 0
        gen_list = []

        while True:
            if pos + size * gen_no+9>len(gamedata):
                break
            gen = gamedata[pos + size * gen_no+3:pos + size * gen_no + size]
            tmp = RoTK2.GetOfficerFromBuffer(gen, gen_no, pos, size, 220)

            if tmp.Int==0 and tmp.War==0 and tmp.Chm==0:
                break

            gen_list.append(tmp)

            gen_no += 1

        print("===============================================")

        return gen_list

    @staticmethod
    def FlushGenerals():
        for o in RoTK2.GetList():
            if o.Name=="":
                continue

            RoTK2.SaveData[o.Offset+0x00] = (o.NextOfficerOffset+0x38)%256
            RoTK2.SaveData[o.Offset + 0x01] = (o.NextOfficerOffset + 0x38) >>8

            RoTK2.SaveData[o.Offset +0x04]=o.Int
            RoTK2.SaveData[o.Offset +0x05]=o.War
            RoTK2.SaveData[o.Offset +0x06]=o.Chm
            RoTK2.SaveData[o.Offset + 0x07] = o.yili
            RoTK2.SaveData[o.Offset + 0x08] = o.rende
            RoTK2.SaveData[o.Offset + 0x09] = o.yewang
            RoTK2.SaveData[o.Offset + 0x0A] = o.RulerNo
            RoTK2.SaveData[o.Offset +0x0B]=o.Loyalty
            RoTK2.SaveData[o.Offset + 0x12] = o.Soldiers % 256
            RoTK2.SaveData[o.Offset + 0x13] = o.Soldiers >>8
            RoTK2.SaveData[o.Offset + 0x14] = o.Weapons % 256
            RoTK2.SaveData[o.Offset + 0x15] = o.Weapons >> 8
            RoTK2.SaveData[o.Offset + 0x16] = o.TrainingLevel

            RoTK2.SaveData[o.Offset + 0x0C] = o.shiwei
            RoTK2.SaveData[o.Offset + 0x0D] = o.SpyBlongedToRuler

            RoTK2.SaveData[o.Offset + 0x0E] = o.SpyInCityNo
            RoTK2.SaveData[o.Offset + 0x0F] = o.xiangxing


    @staticmethod
    def GetRulerList()->Sequence[Ruler]:
        rlist = []
        ruler_num = 0x0f
        start = Data.RULER_OFFSET
        size = Data.RULER_SIZE

        for i in range(0,0x10):
            ruler_offset = (Data.BUF[start + i * size + 1] << 8) + Data.BUF[start + i * size + 0]
            if ruler_offset==0:
                continue
            ruler_city_offset = (Data.BUF[start + i * size + 3] << 8) + Data.BUF[start + i * size + 2]
            aa_offset = (Data.BUF[start + i * size + 5] << 8) + Data.BUF[start + i * size + 4]
            relationships_data = "{0:b}".format(Data.BUF[start + i * size + 0x0A]).zfill(8)[::-1] + "{0:b}".format(Data.BUF[start + i * size + 0x0B]).zfill(8)[::-1]

            order = (Data.BUF[start + i * size + 0x0d] << 8) + Data.BUF[start + i * size + 0x0c]

            k = Ruler()
            k.Offset = start + i*size
            k.No = i
            k.RulerSelf = RoTK2.GetOfficerByOffset(ruler_offset)
            if ruler_city_offset>-1:#君主可能流浪了
                k.HomeCity = RoTK2.GetProvinceByOffset(ruler_city_offset)
            if aa_offset>-1:#君主可能流浪了
                k.Advisor = RoTK2.GetOfficerByOffset(aa_offset)
            k.TrustRating = Data.BUF[start + i * size + 6]
            k.Order = order

            k.RelationShips = {}
            for j in range(0, 16):
                #key:   Alliance
                #value: Hostility
                k.RelationShips[j] =[relationships_data[j], Data.BUF[start + j * size + 0x0e + i]]

            k.IsWandering = (Data.BUF[start+j*size+0x22] != 0xff)
            rlist.append(k)

        return rlist

    @staticmethod
    def GetRulerByNo(no)->Ruler:
        if no==0xff:
            k = Ruler()
            k.RulerSelf = Officer()
            k.No = no
            k.RulerSelf.name = ""

            return k

        ret = None
        rlist = RoTK2.GetRulerList()
        for k in rlist:
            if k.No == no:
                ret = k
                break

        return ret

    def GetCityList(self):
        self.CityList.clear()

        for c in Province.Init():
            if c.RulerNo == self.No:
                self.CityList.append(c)

        return self.CityList

    @staticmethod
    def GetCurrentRulerName():
        return RoTK2.GetOfficerByOffset((Data.BUF[RoTK2.CURRENT_RULER_OFFICER_OFFSET+1]<<8)+Data.BUF[RoTK2.CURRENT_RULER_OFFICER_OFFSET]-0x38).Name

    @staticmethod
    def GetCurrentRulerOfficerOffset():
        return Data.BUF[Data.CURRENT_RULER_OFFICER_OFFSET+1]*256+Data.BUF[Data.CURRENT_RULER_OFFICER_OFFSET+0]
    @staticmethod
    def CanOfficerDoAction(officer:Officer)->bool:
        return ((Data.BUF[officer.Offset+2] & 1) != 1)
        # 生病暂时不知道是否需要判断
        #or ((Data.BUF[officer.Offset+3] & 1) != 1)

    @staticmethod
    def SetOfficerAlreadyDoAction(officer:Officer):
        status = Data.BUF[officer.Offset+2]
        Data.BUF[officer.Offset + 2] = status | 1

    @staticmethod
    def IsAllOfficerFreeze(province:Province)->bool:
        freeze = True
        p = RoTK2.GetProvinceBySequence(province)
        for o in p.OfficerList:
            if RoTK2.CanOfficerDoAction(o) is True:
                freeze = False
                break

        return freeze
    @staticmethod
    def Save(fname):
        header=bytearray(
            [0x31,0x39,0x39,0x30,0x2e,0x30,0x32,0x2e,0x31,0x39,0x00,0x00,0xbd,0x00,0x00,0x0f,
            0x03,0x06,0x0a,0x0a,0x04,0x05,0x0b,0x08,0x00,0x0f,0x02,0x0e,0x0c,0x09,0x0d,0x07]
                         )

        buf = header+Data.BUF[0x58:]
        with open(fname,"wb") as f:
            f.write(buf)

    @staticmethod
    def GetRulersOrder():
        ruler_list = RoTK2.GetRulerList()

        for ruler in ruler_list:
            magic = 0

            for province in RoTK2.GetProvincesByRulerNo(ruler.No):
                magic += len(province.OfficerList)*100 + int(province.Soldiers/100)

            Data.BUF[ruler.Offset+0x0c] = magic % 256
            Data.BUF[ruler.Offset + 0x0d] = int(magic / 256)

        ruler_list = RoTK2.GetRulerList()
        ruler_list = sorted(ruler_list, key=lambda x: x.Order, reverse=False)

        index = 0
        for ruler in ruler_list:
            Data.BUF[0x3370 + index + 0] = ruler.Offset % 256
            Data.BUF[0x3370 + index + 1] = int(ruler.Offset / 256)

            index += 2

    @staticmethod
    def IsProvinceRuledByCurrentRuler(province_no):
        offset = Data.PROVINCE_OFFSET + (province_no-1)*Data.PROVINCE_SIZE
        ruler_no = Data.BUF[offset+0x10]

        offset = Data.BUF[0x335D+Data.OFFSET]*256+Data.BUF[0x335C+Data.OFFSET]
        ruler_no2 = int((offset-Data.RULER_OFFSET)/Data.RULER_SIZE)

        return ruler_no == ruler_no2

    @staticmethod
    def GetProvinceDelegateStatus(province_no):
        offset = Data.PROVINCE_OFFSET + (province_no - 1) * Data.PROVINCE_SIZE
        return Data.BUF[offset+0x12]
