import pygame.time

from Data import Data,ShowOfficerFlag
from Helper import Helper,Province,Officer,Ruler


class Command2(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        province = Province.FromSequence(province_no)
        Helper.ClearInputArea()

        if province.Gold<1 and province.Food<1:
            img = Helper.DrawText(Helper.GetBuiltinText("0x6A2C"),scaled=True,palette_no=6)
            Helper.Screen.blit(img,(300*Helper.Scale,295*Helper.Scale))
            pygame.time.wait(1000)
            return

        Helper.ClearInputArea()
        where = Helper.GetInput(Helper.GetBuiltinText(0x6A18)+"(1-41)? ")
        if where==-1:
            return

        whos = Helper.SelectOfficer(province_no,Helper.GetBuiltinText(0x6A23),ShowOfficerFlag.Soldiers)
        if whos==-1:
            return

        gold = Helper.GetInput(Helper.GetBuiltinText(0x69EF)+" (0-{0})?".format(province.Gold),row=1)
        if len(gold)==0:
            return

        food = Helper.GetInput(Helper.GetBuiltinText(0x69FC).replace("%lu%",str(province.Food)), row=2)
        if len(food)==0:
            return

        print("{0}->gold={1}, food={2}".format(whos,gold,food))

