import math

from RoTK2 import RoTK2

def game_mil_train_soldiers_calc(province_no,general_no):
    p = RoTK2.GetProvinceBySequence(province_no)
    g = p.GetOfficerBySequence(general_no)

    s = 0
    for officer in p.OfficerList:
        s += int(officer.Soldiers / 100)
    s2 = int(math.sqrt(s+1))
    inc = int(g.War*2/s2)

    for officer in p.OfficerList:
        officer.TrainingLevel += inc
        RoTK2.BUF[officer.Offset+0x16] = officer.TrainingLevel

    RoTK2.SetOfficerAlreadyDoAction(g)
