import os.path
import random
from Data import Data,ShowOfficerFlag
import pygame,sys
from Helper import Helper
from RoTK2 import RoTK2
from Data import DelegateMode

class Command11(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        commands = [Helper.GetBuiltinText(0x7C37),Helper.GetBuiltinText(0x7C3C),Helper.GetBuiltinText(0x7C41)]
        advisor_province = RoTK2.GetAdvisorProvince()

        commands_color=[]
        if province_no!=advisor_province:
            commands_color=[3,3,4]

        Helper.ShowCommandsInInputArea(commands,3,palette_no=3,width=70,commands_color=commands_color)
        award = Helper.GetInput(Helper.GetBuiltinText(0x7C4A) + "(1-3)? ", row=1, required_number_min=1,required_number_max=3)
        if award == -1:
            return

        governor_offset = RoTK2.GetProvinceBySequence(province_no).GovernorOffset
        if governor_offset==RoTK2.GetCurrentRulerOfficerOffset():
            show_ruler = False
        else:
            show_ruler = True
        governor_chm = RoTK2.GetOfficerByOffset(governor_offset).Chm

        if award==1:
            whos = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x7C00), ShowOfficerFlag.Loyalty,
                                        check_can_action=False, show_governor=show_ruler)
            if whos>0:
                Helper.ClearInputArea()
                gold = Helper.GetInput(Helper.GetBuiltinText(0x7C09)+"(1-100)? ",required_number_min=1,required_number_max=100)
                if gold>0:
                    officer_offset = RoTK2.GetProvinceBySequence(province_no).GetOfficerBySequence(whos).Offset
                    result = self.Reward(officer_offset,governor_chm,gold)
                    self.ShowRewardResult(officer_offset,result)
        elif award==2:
            if RoTK2.GetProvinceBySequence(province_no).Horses<1:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x7C55))
                return

            whos = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x7BEE), ShowOfficerFlag.Loyalty, check_can_action=False,
                                        show_governor=show_ruler)
            if whos>0:
                officer_offset = RoTK2.GetProvinceBySequence(province_no).GetOfficerBySequence(whos).Offset
                result = self.Reward(officer_offset,governor_chm, 100)
                self.ShowRewardResult(officer_offset, result)
        else:
            if province_no!=advisor_province:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x7C63))
                return

            whos = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x7B94), ShowOfficerFlag.Int, check_can_action=False,
                                        show_governor=show_ruler)
            if whos>0:
                Helper.ClearInputArea()
                yn = Helper.GetInput(Helper.GetBuiltinText(0x7B9B)+"(Y/N)? ",yesno=True)
                if yn!="y":
                    return

                advisor = RoTK2.GetAdvisor()
                officer_offset = RoTK2.GetProvinceBySequence(province_no).GetOfficerBySequence(whos).Offset
                result = self.RewardBook(officer_offset,advisor.Int)
                if result==-1:
                    Helper.ShowDelayedText(Helper.GetBuiltinText(0x7BBA))
                else:
                    Helper.ShowDelayedText(Helper.GetBuiltinText(0x7BA6).replace("%s",RoTK2.GetOfficerName(officer_offset)),palette_no=3)

    def Reward(self,officer_offset,governor_chm,gold):
        result = int((governor_chm*gold)/0x190)
        if result<1:
            return -1
        else:
            loyalty_original = loyalty = Data.BUF[officer_offset+0x0B]
            loyalty += result
            r = int(2*random.random())
            loyalty += r

            if loyalty>100:
                loyalty = 100

            if loyalty==loyalty_original:
                return -1

            Data.BUF[officer_offset + 0x0B] = loyalty
            return loyalty

    def RewardBook(self,officer_offset,advisor_int):
        int = Data.BUF[officer_offset+4]
        int = int + 1

        if int>=advisor_int:
            return -1
        if int>100:
            int = 100

        Data.BUF[officer_offset+4] = int
        return 0

    def ShowRewardResult(self,officer_offset,result):
        if result==-1:
            info = Helper.GetBuiltinText(0x7BDE).replace("%s", RoTK2.GetOfficerName(officer_offset))
            palette_no = 6
        else:
            info = Helper.GetBuiltinText(0x7BC6).replace("%s", RoTK2.GetOfficerName(officer_offset)).replace("%d",str(result))
            palette_no = 3

        Helper.ShowDelayedText(info,palette_no=palette_no)

