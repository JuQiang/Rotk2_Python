from Data import Data,ShowOfficerFlag
from Helper import Helper,Province,Officer,Ruler


class Command1(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        province = Province.FromSequence(province_no)
        officers_num = len(province.GetOfficerList())

        while True:
            Helper.ClearInputArea()
            where = Helper.GetInput(Helper.GetBuiltinText(0x6998)+"(1-41)? ",required_number_min=1,required_number_max=41)
            if where==-1:
                return

            neighbors = Helper.GetNeighbors(province_no)
            if where not in neighbors:
                continue

            where_province = Province.FromSequence(where)
            if where_province.RulerNo==255:
                break

            if province.RulerNo==where_province.RulerNo:
                break


        whos = Helper.SelectOfficer(province_no,Helper.GetBuiltinText(0x695C),ShowOfficerFlag.Soldiers,True)
        if len(whos)==0:
            return

        gold = Helper.GetInput(Helper.GetBuiltinText(0x6965)+" (0-{0})?".format(province.Gold),row=1,required_number_min=0,required_number_max=province.Gold)
        if gold<0:
            return

        food = Helper.GetInput(Helper.GetBuiltinText(0x6974,0x697F)+" (0-{0})?".format(province.Food),required_number_min=0,required_number_max=province.Food, row=2)
        giveup = False

        if food<0:
            return

        print("{0}->gold={1}, food={2}".format(whos,gold,food))

        if len(whos)==officers_num:
            yn = Helper.GetInput(Helper.GetBuiltinText(0x698A),row=2)
            if yn in ["0","y"]:
                giveup = True
                #Ruler.RemoveProvinceFromRuler(province.RulerNo, Province.GetActiveNo())
                #Helper.CurrentProvinceNo = where

        ruler_offset = Ruler.FromNo(province.RulerNo).RulerSelf.Offset
        ruler_moved = False
        if 1 in whos:
            ruler_moved = (ruler_offset == province.GetOfficerList()[0].Offset)

        where_province.RulerNo = province.RulerNo
        where_province.Flush()
        Province.TransitOfficers(whos,province_no,where)

        if ruler_moved:
            Province.SetGovernor(where,ruler_offset)

            if giveup:
                # set governor empty
                Province.SetGovernor(province_no,0)
            else:
                prompt = Helper.GetBuiltinText(0x3F75)
                prompt = prompt.replace("%s", Ruler.GetNameFromProvinceSequence(province_no)).replace("%2d", str(province_no))
                prompt += "(1-{0})?".format(len(whos))
                Helper.ClearInputArea()
                governor = Helper.SelectOfficer(province_no, prompt, ShowOfficerFlag.Loyalty)
                Province.SetGovernor(province_no, province.GetOfficerList()[governor-1].Offset)
        else:
            prompt = Helper.GetBuiltinText(0x3F75)
            prompt = prompt.replace("%s", Ruler.GetNameFromProvinceSequence(province_no)).replace("%2d", str(where))
            prompt += "(1-{0})?".format(len(whos))

            Helper.ClearInputArea()
            governor = Helper.SelectOfficer(where,prompt, ShowOfficerFlag.Loyalty)
            Province.SetGovernor(where,Province.FromSequence(where).GetOfficerList()[governor-1].Offset)

            governor_moved = (1 in whos)
            if governor_moved:
                if giveup:
                    Province.SetGovernor(province_no,0)
                else:
                    prompt = Helper.GetBuiltinText(0x3F75)
                    prompt = prompt.replace("%s", Ruler.GetNameFromProvinceSequence(province_no)).replace("%2d", str(province_no))
                    prompt += "(1-{0})?".format(len(whos))

                    Helper.ClearInputArea()
                    governor = Helper.SelectOfficer(province_no, prompt, ShowOfficerFlag.Loyalty)
                    Province.SetGovernor(province_no, province.GetOfficerList()[governor-1].Offset)
