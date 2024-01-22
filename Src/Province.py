from Src.Officer import  Officer
from collections.abc import  Mapping, Sequence

class Province(object):
    # region properties
    No = 0#从1开始
    Offset = 0
    NextProvince = 0
    RulerNo  = 0
    WarRulerNo = 0
    GovernorOffset = 0
    FirstUnClaimedOfficerOffset = 0
    UnClaimedOfficerNumber = 0
    ClaimedOfficerNumber = 0
    FreeOfficerOffset = 0
    FreeOfficerNumber = 0
    DelegateControl = ""
    ProvinceSendGoods= ""
    ProvinceInvade= ""
    Gold = 0
    Food = 0
    Population = 0
    Land = 0
    Loyalty = 0
    Flood = 0
    Horses = 0
    Castle = 0
    RicePrice = 0
    Name= ""
    Soldiers = 0
    X = 0
    Y = 0
    NameIndex = 0
    # endregion properties

    OfficerList = Sequence[Officer]
    UnclaimedOfficerList = Sequence[Officer]

    def GetOfficerBySequence(self,sequence)->Officer:
        return self.OfficerList[sequence-1]

