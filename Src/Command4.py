import math
import os.path
import random

from Data import Data, ShowOfficerFlag
import pygame,sys
from Helper import Helper,Province,Officer,Ruler
from Data import DelegateMode

class Command4(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        self.province_no = province_no
        self.province = Province.FromSequence(province_no)

        commands = [Helper.GetBuiltinText(0x6C66,0x6C69),Helper.GetBuiltinText(0x6C6E,0x6C71),Helper.GetBuiltinText(0x6C76,0x6C79)]
        Helper.ClearInputArea()
        Helper.ShowCommandsInInputArea(commands,3,width=60,palette_no=5)
        cmd = Helper.GetInput(Helper.GetBuiltinText(0x7E5C, 0x7E61) + "(1-3)? ", row=1, required_number_min=1,
                              required_number_max=3)
        if cmd==1:
            self.MuBing()
        if cmd==2:
            self.PaiBing()
        if cmd==3:
            self.Training()

    def MuBing(self):
        if self.province.Gold<10:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6070))
            return
        if self.province.Food<100:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6C4C))
            return

        capacity = self.GetCapacity()
        if capacity==0:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6C55))
            return

        # who will hire soldiers
        officer_no = Helper.SelectOfficer(self.province_no,Helper.GetBuiltinText(0x6C38), ShowOfficerFlag.Empty)
        # how many soldiers will be hired?
        soldiers_hired = Helper.GetInput(Helper.GetBuiltinText(0x6C41) + "(1-{0})? ".format(capacity),row=1,required_number_min=1,required_number_max=capacity)
        if soldiers_hired<0:
            return

        self.province.Gold -= soldiers_hired * 10
        self.province.Flush()

        self.AdjustSoldiers(soldiers_hired)

    def GetCapacity(self):
        soldiers_divided_by_100 = int(self.province.Soldiers / 100)
        if int(self.province.Population/100)<0x1F4:
            return 0
        if self.province.Population<soldiers_divided_by_100:
            return 0

        people = int(self.province.Population/100)
        min_1 = min(people-0x1F4,int((people-soldiers_divided_by_100)/2))
        min_2 = min(int(self.province.Food/100), int(self.province.Gold/10))

        min_3 = 0
        for officer in self.province.GetOfficerList():
            min_3 += (10000 - officer.Soldiers)
        min_3 = int(min_3/100)

        capacity = min(min_1,min(min_2,min_3))

        return capacity

    def PaiBing(self):
        # who will hire soldiers
        officer_no = Helper.SelectOfficer(self.province_no, Helper.GetBuiltinText(0x6C2B), ShowOfficerFlag.Empty)

        self.AdjustSoldiers(0)

    def Training(self):
        isHighest = True
        for officer_no in self.province.GetOfficerList():
            if officer_no.TrainingLevel!=100:
                isHighest = False
                break

        if isHighest is True:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6BCE))
            return

        officer_no = Helper.SelectOfficer(self.province_no,Helper.GetBuiltinText(0x6BA0),ShowOfficerFlag.War)
        if officer_no<1:
            return

        officer = self.province.GetOfficerBySequence(officer_no)

        s = 0
        for officer_no in self.province.GetOfficerList():
            s += int(officer_no.Soldiers / 100)

        s2 = int(math.sqrt(s + 1))
        inc = int(officer.War * 2 / s2)

        for officer in self.province.GetOfficerList():
            officer.TrainingLevel += inc
            if officer.TrainingLevel>100:
                officer.TrainingLevel = 100
            officer.Flush()

        # after training
        Helper.ShowDelayedText(Helper.GetBuiltinText(0x6BB9),palette_no=3,top=330,clear_input_area=False)

    def AdjustSoldiers(self,soldiers_hired):
        soldiers_remained = soldiers_hired
        while True:
            Helper.ClearInputArea()
            # the remained soldiers
            img = Helper.DrawText(Helper.GetBuiltinText(0x6BF2,0x6BFF).replace("%lu",str(soldiers_remained*100)),scaled=True,palette_no=5)
            Helper.Screen.blit(img,(300*Helper.Scale,300*Helper.Scale))
            pygame.display.flip()
            # change who?
            officer_no = Helper.SelectOfficer(self.province_no, Helper.GetBuiltinText(0x6C06),ShowOfficerFlag.Soldiers, row=1,clear_area=False,check_can_action=False)
            if officer_no<1:
                if soldiers_remained>0:
                    # soldiers transit to people?
                    yn = Helper.GetInput(Helper.GetBuiltinText(0x6C16).replace("%lu",str(soldiers_remained*100))+Helper.GetBuiltinText(0x3D7D)+"(Y/N)? ",yesno=True,row=2)
                    if yn=="y":
                        self.province.Population -= soldiers_remained*100
                        self.province.Flush()

                        return
                else:
                    yn = Helper.GetInput(Helper.GetBuiltinText(0x3D7D) + "(Y/N)? ", yesno=True, row=2)
                    if yn=="y":
                        self.province.Population -= soldiers_hired * 100
                        self.province.Flush()

                        return

            officer = Officer.FromOffset(self.province.GetOfficerBySequence(officer_no).Offset)
            soldiers_remained += int(officer.Soldiers/100)
            max = soldiers_remained if soldiers_remained < 100 else 100
            # how many soldiers will be owner?
            soldiers = Helper.GetInput(Helper.GetBuiltinText(0x6BE2)+"(0-{0})".format(max*100),row=2,required_number_min=0,required_number_max=max*100)
            if soldiers>=0:
                Data.BUF[officer.Offset + 0x13] = soldiers>>8
                Data.BUF[officer.Offset + 0x12] = soldiers%256

                soldiers_remained -= int(soldiers/100)
            else:
                soldiers_remained -= int(officer.Soldiers/100)

