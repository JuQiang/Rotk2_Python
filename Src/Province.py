from Officer import Officer
from Data import Data, ShowOfficerFlag, DelegateMode

class Province(object):
    # region properties
    No = 0  # 从1开始
    Offset = 0
    NextProvince = 0
    RulerNo = 0
    WarRulerNo = 0
    GovernorOffset = 0
    FirstUnClaimedOfficerOffset = 0
    UnClaimedOfficerNumber = 0
    ClaimedOfficerNumber = 0
    FreeOfficerOffset = 0
    FreeOfficerNumber = 0
    DelegateControl = ""
    ProvinceSendGoods = ""
    ProvinceInvade = ""
    Gold = 0
    Food = 0
    Population = 0
    Land = 0
    Loyalty = 0
    Flood = 0
    Horses = 0
    Castle = 0
    RicePrice = 0
    Name = ""
    Soldiers = 0
    X = 0
    Y = 0
    NameIndex = 0
    # endregion properties

    def GetOfficerBySequence(self, sequence) -> Officer:
        return self.GetOfficerList()[sequence - 1]

    def Flush(self):
        Data.BUF[self.Offset + 0x00] = self.NextProvince % 256
        Data.BUF[self.Offset + 0x01] = self.NextProvince >> 8
        Data.BUF[self.Offset + 0x02] = self.GovernorOffset % 256
        Data.BUF[self.Offset + 0x03] = self.GovernorOffset >> 8
        Data.BUF[self.Offset + 0x04] = self.FirstUnClaimedOfficerOffset % 256
        Data.BUF[self.Offset + 0x05] = self.FirstUnClaimedOfficerOffset >> 8
        Data.BUF[self.Offset + 0x06] = self.FreeOfficerOffset % 256
        Data.BUF[self.Offset + 0x07] = self.FreeOfficerOffset >> 8
        Data.BUF[self.Offset + 0x08] = self.Gold % 256
        Data.BUF[self.Offset + 0x09] = self.Gold >> 8
        Data.BUF[self.Offset + 0x0A] = self.Food % 256
        Data.BUF[self.Offset + 0x0B] = (self.Food >> 8) % 256
        Data.BUF[self.Offset + 0x0C] = (self.Food >> 16) % 256
        Data.BUF[self.Offset + 0x0D] = self.Food >> 24
        Data.BUF[self.Offset + 0x0E] = int((self.Population / 100)) % 256
        Data.BUF[self.Offset + 0x0F] = int((self.Population / 100)) >> 8
        Data.BUF[self.Offset + 0x10] = self.RulerNo
        Data.BUF[self.Offset + 0x11] = self.WarRulerNo
        # TODO: 12~15
        Data.BUF[self.Offset + 0x16] = self.Land
        Data.BUF[self.Offset + 0x17] = self.Loyalty
        Data.BUF[self.Offset + 0x18] = self.Flood
        Data.BUF[self.Offset + 0x19] = self.Horses
        Data.BUF[self.Offset + 0x1A] = self.Castle
        Data.BUF[self.Offset + 0x1B] = self.RicePrice

    @staticmethod
    def FromOffset(offset):
        city_names = ["幽州", "幷州", "冀州", "青州", "兗州", "司州", "雍州", "涼州", "徐州", "予州", "荊州", "揚州",
                      "益州", "交州"]


        p = Province()

        province_buf = Data.BUF[offset: offset+Data.PROVINCE_SIZE]

        x = province_buf[0x20]
        y = province_buf[0x21]
        p.X = x
        p.Y = y
        name_index = province_buf[0x22]
        p.NameIndex = name_index
        p.No = Data.MapIndex[y][x]
        p.Name = city_names[name_index] + "-" + str(p.No)
        p.Offset = offset
        p.NextProvince = Data.GetWordFromOffset(province_buf, 0)
        p.RulerNo = province_buf[0x10]

        p.WarRulerNo = province_buf[0x11]
        daili = province_buf[0x12]
        zhanzhengjun = province_buf[0x14]
        yunshujun = province_buf[0x15]

        p.GovernorOffset = Data.GetWordFromOffset(province_buf, 2)
        p.FirstUnClaimedOfficerOffset = Data.GetWordFromOffset(province_buf, 4)
        p.FreeOfficerOffset = Data.GetWordFromOffset(province_buf, 6)

        daili_mappings = {0: "", 3: "未知", 4: "全权", 5: "内政", 6: "军事", 7: "人事"}
        if daili < 8:
            p.DelegateControl = daili_mappings[daili]

        if yunshujun < 41:
            name_index = Data.BUF[Data.PROVINCE_START + Data.PROVINCE_SIZE * yunshujun + Data.PROVINCE_SIZE - 1]
            p.ProvinceSendGoods = city_names[name_index] + "-" + str(yunshujun + 1)
        if zhanzhengjun < 41:
            name_index = Data.BUF[Data.PROVINCE_START + Data.PROVINCE_SIZE * zhanzhengjun + Data.PROVINCE_SIZE - 1]
            p.ProvinceInvade = city_names[name_index] + "-" + str(name_index + 1)

        p.Gold = Data.GetWordFromOffset(province_buf, 8)
        p.Food = (province_buf[0x0D] << 24) + (province_buf[0x0C] << 16) + (province_buf[0x0B] << 8) + province_buf[
            0x0A]
        p.Population = (Data.GetWordFromOffset(province_buf, 0x0E)) * 100
        p.Land = province_buf[0x16]
        p.Loyalty = province_buf[0x17]
        p.Flood = province_buf[0x18]
        p.Horses = province_buf[0x19]
        p.Castle = province_buf[0x1A]
        p.RicePrice = province_buf[0x1B]

        return p

    @staticmethod
    def GetList():

        province_list = []
        for i in range(0, 41):
            province = Province.FromOffset(Data.PROVINCE_START + Data.PROVINCE_SIZE * i)
            province_list.append(province)

        return province_list

    def GetOfficerList(self):
        olist = []

        next = Data.GetWordFromOffset(Data.BUF, self.Offset + 2)
        while next > 0:
            officer = Officer.FromOffset(next)
            olist.append(officer)
            next = officer.NextOfficerOffset

        return olist

    def GetUnclaimedOfficerList(self):
        olist = []

        next = Data.GetWordFromOffset(Data.BUF, self.Offset + 4)
        while next > 0:
            officer = Officer.FromOffset(next)
            officer.IsUnClaimed = True
            olist.append(officer)
            next = officer.NextOfficerOffset

        return olist

    def GetFreeOfficerList(self):
        olist = []

        next = Data.GetWordFromOffset(Data.BUF, self.Offset + 6)
        while next > 0:
            officer = Officer.FromOffset(next)
            officer.IsFree = True
            olist.append(officer)
            next = officer.NextOfficerOffset

        return olist

    @staticmethod
    def FromSequence(sequence):
        return Province.GetList()[sequence - 1]

    def IsAllOfficerFreeze(self):
        freeze = True

        for o in self.GetOfficerList():
            if o.CanAction() is True:
                freeze = False
                break

        return freeze

    @staticmethod
    def GetListByRulerNo(ruler_no):
        start = Data.RULER_START+Data.RULER_SIZE*ruler_no
        province_offset = Data.GetWordFromOffset(Data.BUF,start+0x02)

        plist = []
        while province_offset>0:
            plist.append(Province.FromOffset(province_offset))
            province_offset = Data.GetWordFromOffset(Data.BUF,province_offset)

        return plist

    @staticmethod
    def ReOrderOfficers(prov_no, flag: ShowOfficerFlag):
        officer_list = Province.FromSequence(prov_no).GetOfficerList()
        if len(officer_list) < 1:
            return

        governor = officer_list[0]
        if len(officer_list) > 1:
            new_list = []
            for o in officer_list[1:]:
                new_list.append(o)

            if flag == ShowOfficerFlag.Int:
                olist = sorted(new_list, key=lambda x: x.Int, reverse=True)
            elif flag == ShowOfficerFlag.War:
                olist = sorted(new_list, key=lambda x: x.War, reverse=True)
            elif flag == ShowOfficerFlag.Chm:
                olist = sorted(new_list, key=lambda x: x.Chm, reverse=True)
            elif flag == ShowOfficerFlag.Soldiers:
                olist = sorted(new_list, key=lambda x: x.Soldiers, reverse=True)
            elif flag == ShowOfficerFlag.Loyalty:
                olist = sorted(new_list, key=lambda x: x.Loyalty, reverse=True)
            else:
                raise Exception("Invalid sorted flag.")

            governor.NextOfficerOffset = olist[0].Offset
            governor.Flush()

            for i in range(0, len(olist)):
                if i == len(olist) - 1:
                    olist[i].NextOfficerOffset = 0
                else:
                    olist[i].NextOfficerOffset = olist[i + 1].Offset

                olist[i].Flush()

    @staticmethod
    def GetActiveNo():
        size = Data.GetWordFromOffset(Data.BUF, Data.CURRENT_PROVINCE_OFFSET) - Data.PROVINCE_START
        return int(size / Data.PROVINCE_SIZE) + 1

    @staticmethod
    def GetAdvisorProvince():
        advisor = Officer.GetAdvisor()
        if advisor is not None:
            for p in Province.GetList():
                for o in p.GetOfficerList():
                    if o.Offset == advisor.Offset:
                        return p.No

        return -1

    @staticmethod
    def SetGovernor(province_no, governor_offset):
        p = Province.FromSequence(province_no)
        p.GovernorOffset = governor_offset

        new_list = []
        for o in p.GetOfficerList():
            if o.Offset != governor_offset:
                new_list.append(o)

        i = -1
        for i in range(0, len(new_list) - 1):
            new_list[i].NextOfficerOffset = new_list[i + 1].NextOfficerOffset
            new_list[i].Flush()

        if len(new_list) > 0:
            new_list[i + 1].NextOfficerOffset = 0
            new_list[i + 1].Flush()

            governor = Officer.FromOffset(governor_offset)
            governor.NextOfficerOffset = new_list[0].Offset
            governor.Flush()


        p.Flush()


    @staticmethod
    def TransitOfficers(officer_list, from_province, to_province):
        _from = Province.FromSequence(from_province)
        _to = Province.FromSequence(to_province)

        from_list = []
        to_list = []
        for i in range(1, len(_from.GetOfficerList()) + 1):
            if i not in officer_list:
                from_list.append(_from.GetOfficerList()[i - 1])
            else:
                to_list.append(_from.GetOfficerList()[i - 1])

        i = -1
        for i in range(0, len(from_list) - 1):
            from_list[i].NextOfficerOffset = from_list[i + 1].Offset
            from_list[i].Flush()


        if len(from_list) > 0:
            from_list[i + 1].NextOfficerOffset = 0
            from_list[i + 1].Flush()


            # ensure all of the officers can be visited from this province
            # and, we MUST announce a new governor at 8.1 action
            _from.GovernorOffset = from_list[0].Offset
            _from.Flush()

        i = -1
        for i in range(0, len(to_list) - 1):
            to_list[i].NextOfficerOffset = to_list[i + 1].Offset
            to_list[i].Flush()

        if len(to_list) > 0:
            to_list[i + 1].NextOfficerOffset = 0
            to_list[i + 1].Flush()


            # ensure all of the officers can be visited from this province
            # and, we MUST announce a new governor at 8.1 action
            _to.GovernorOffset = to_list[0].Offset
            _to.Flush()

    def GetSoldiers(self):
        soldiers = 0
        for officer in self.GetOfficerList():
            soldiers += officer.Soldiers

        return soldiers

    @staticmethod
    def Is2ProvincesBelongToSameRuler(province_no, p_no):
        ruler_no_1 = Province.FromSequence(province_no).RulerNo
        ruler_no_2 = Province.FromSequence(p_no).RulerNo

        return ruler_no_1 == ruler_no_2

    @staticmethod
    def GetDelegateStatus(province_no):
        offset = Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE
        return Data.BUF[offset + 0x12]

    @staticmethod
    def IsRuledByCurrentRuler(province_no):
        offset = Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE
        ruler_no = Data.BUF[offset + 0x10]

        offset = Data.BUF[0x335D + Data.DATA_OFFSET] * 256 + Data.BUF[0x335C + Data.DATA_OFFSET]
        ruler_no2 = int((offset - Data.RULER_START) / Data.RULER_SIZE)

        return ruler_no == ruler_no2