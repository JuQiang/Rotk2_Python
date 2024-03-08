from Officer import Officer
from Province import Province
from Data import Data

class Ruler(object):
    # region properties
    Offset = 0
    RulerSelf:Officer = None
    HomeCity = None
    Advisor = None
    No = 0xff
    TrustRating = 0
    RelationShips = {}
    IsWandering = False
    Order = 0
    # endregion properties

    @staticmethod
    def GetList():
        rlist = []
        ruler_num = 0x0f
        start = Data.RULER_START
        size = Data.RULER_SIZE

        for i in range(0, 0x10):
            ruler_offset = Data.GetWordFromOffset(Data.BUF,start + i * size + 0)
            if ruler_offset == 0:
                continue
            ruler_city_offset = Data.GetWordFromOffset(Data.BUF,start + i * size + 2)
            aa_offset = Data.GetWordFromOffset(Data.BUF,start + i * size + 4)
            relationships_data = "{0:b}".format(Data.BUF[start + i * size + 0x0A]).zfill(8)[::-1] + "{0:b}".format(
                Data.BUF[start + i * size + 0x0B]).zfill(8)[::-1]

            order = Data.GetWordFromOffset(Data.BUF,start + i * size + 0x0C)

            k = Ruler()
            k.Offset = start + i * size
            k.No = i
            k.RulerSelf = Officer.FromOffset(ruler_offset)
            if ruler_city_offset > 0:  # 君主可能流浪了
                k.HomeCity = Province.FromOffset(ruler_city_offset)
            if aa_offset > -1:  # 君主可能流浪了
                k.Advisor = Officer.FromOffset(aa_offset)
            k.TrustRating = Data.BUF[start + i * size + 6]
            k.Order = order

            k.RelationShips = {}
            for j in range(0, 16):
                # key:   Alliance
                # value: Hostility
                k.RelationShips[j] = [relationships_data[j], Data.BUF[start + j * size + 0x0e + i]]

            k.IsWandering = (Data.BUF[start + j * size + 0x22] != 0xff)
            rlist.append(k)

        return rlist

    @staticmethod
    def FromNo(no):
        if no == 0xff:
            k = Ruler()
            k.RulerSelf = Officer()
            k.No = no
            k.RulerSelf.name = ""

            return k

        ret = None
        rlist = Ruler.GetList()
        for k in rlist:
            if k.No == no:
                ret = k
                break

        return ret

    @staticmethod
    def GetActiveNo():
        current_ruler_province = Data.GetWordFromOffset(Data.BUF, Data.CURRENT_PROVINCE_OFFSET)
        return Data.BUF[current_ruler_province + 0x10]

    @staticmethod
    def GetNameFromProvinceSequence(province_no):
        ruler_no = Province.FromSequence(province_no).RulerNo
        ruler = Ruler.FromNo(ruler_no).RulerSelf
        ruler_name_data = ruler.GetName()

        return ruler_name_data




