import math

from RoTK2 import RoTK2

def game_development_land_flood_calc(province_no,general_no,gold,is_land):
    p = RoTK2.GetProvinceBySequence(province_no)

    if is_land is True:
        value = p.Land
    else:
        value = p.Flood

    value = int(value/2)
    o = p.GetOfficerBySequence(general_no)

    v1 = int(math.sqrt(int((100-value)*gold/100)*(int(o.Chm/2)+o.Int)))
    dif = int((RoTK2.GAME_DIFFCULTY+1)/2)
    v2 = int(math.sqrt(int(v1/dif))) - dif

    RoTK2.SetOfficerAlreadyDoAction(o)
    return v2

def game_give_population_calc(province_no,general_no,food):
    p = RoTK2.GetProvinceBySequence(province_no)
    r = RoTK2.GetRulerByNo(p.RulerNo).RulerSelf
    o = p.GetOfficerBySequence(general_no)

    v1 = int(math.sqrt(food)) * int((r.Chm+o.Chm)/2)
    v2 = (11+RoTK2.GAME_DIFFCULTY)*int(math.sqrt(p.Population/100))

    RoTK2.SetOfficerAlreadyDoAction(o)

    return int(v1/v2)