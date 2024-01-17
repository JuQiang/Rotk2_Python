from Data import Data,ShowOfficerFlag
from Helper import Helper
from RoTK2 import RoTK2

class Command1(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        province = RoTK2.GetProvinceBySequence(province_no)
        officers_num = len(province.OfficerList)

        while True:
            Helper.ClearInputArea()
            where = Helper.GetInput(Helper.GetBuiltinText(0x6998)+"(1-41)? ",required_number_min=1,required_number_max=41)
            if where==-1:
                return

            where_province = RoTK2.GetProvinceBySequence(where)
            if where_province.RulerNo==255:
                break

            if province.RulerNo!=where_province.RulerNo:
                continue
            else:
                break

        whos = Helper.SelectOfficer(province_no,Helper.GetBuiltinText(0x695C),ShowOfficerFlag.Soldiers,True)
        if len(whos)==0:
            return

        gold = Helper.GetInput(Helper.GetBuiltinText(0x6965)+" (0-{0})?".format(province.Gold),row=1)
        if len(gold)==0:
            return

        food = Helper.GetInput(Helper.GetBuiltinText(0x6974,0x697F)+" (0-{0})?".format(province.Food), row=2)
        giveup = False

        if len(food)==0:
            return

        print("{0}->gold={1}, food={2}".format(whos,gold,food))

        if len(whos)==officers_num:
            yn = Helper.GetInput(Helper.GetBuiltinText(0x698A),row=2)
            if yn in ["0","y"]:
                giveup = True
                #Helper.RemoveProvinceFromRuler(province.RulerNo, Helper.CurrentProvinceNo)
                Helper.CurrentProvinceNo = where

        ruler_offset = RoTK2.GetRulerByNo(province.RulerNo).RulerSelf.Offset
        ruler_moved = False
        if 1 in whos:
            ruler_moved = (ruler_offset == province.OfficerList[0].Offset)

        where_province.RulerNo = province.RulerNo
        RoTK2.FlushProvince(where_province)
        Helper.MoveOfficersToProvince(whos,province_no,where)

        if ruler_moved:
            Helper.SetProvinceGovernor(where,ruler_offset)

            if giveup:
                # set governor empty
                Helper.SetProvinceGovernor(province_no,0)
            else:
                prompt = Helper.GetBuiltinText(0x3F75)
                prompt = prompt.replace("%s", Helper.GetRulerName(province_no)).replace("%2d", str(province_no))
                prompt += "(1-{0})?".format(len(whos))
                Helper.ClearInputArea()
                governor = Helper.SelectOfficer(province_no, prompt, ShowOfficerFlag.Loyalty)
                Helper.SetProvinceGovernor(province_no, province.OfficerList[governor-1].Offset)
        else:
            prompt = Helper.GetBuiltinText(0x3F75)
            prompt = prompt.replace("%s", Helper.GetRulerName(province_no)).replace("%2d", str(where))
            prompt += "(1-{0})?".format(len(whos))

            Helper.ClearInputArea()
            governor = Helper.SelectOfficer(where,prompt, ShowOfficerFlag.Loyalty)
            Helper.SetProvinceGovernor(where,RoTK2.GetProvinceBySequence(where).OfficerList[governor-1].Offset)

            governor_moved = (1 in whos)
            if governor_moved:
                if giveup:
                    Helper.SetProvinceGovernor(province_no,0)
                else:
                    prompt = Helper.GetBuiltinText(0x3F75)
                    prompt = prompt.replace("%s", Helper.GetRulerName(province_no)).replace("%2d", str(province_no))
                    prompt += "(1-{0})?".format(len(whos))

                    Helper.ClearInputArea()
                    governor = Helper.SelectOfficer(province_no, prompt, ShowOfficerFlag.Loyalty)
                    Helper.SetProvinceGovernor(province_no, province.OfficerList[governor-1].Offset)
