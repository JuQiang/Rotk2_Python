import math
import os.path
import random

from Data import Data, ShowOfficerFlag
import pygame, sys
from Helper import Helper,Province,Officer,Ruler
from Data import DelegateMode


class Command13(object):
    def __init__(self):
        pass

    def Start(self, province_no):
        self.province_no = province_no
        self.province = Province.FromSequence(self.province_no)

        if self.MerchantCheckExist() is False:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x7E22), palette_no=6)
            # return

        commands = [
            Helper.GetBuiltinText(0x7E36, 0x7E39),
            Helper.GetBuiltinText(0x7E3F, 0x7E42),
            Helper.GetBuiltinText(0x7E48, 0x7E4B),
            Helper.GetBuiltinText(0x7E51, 0x7E56),
        ]

        Helper.ClearInputArea()
        Helper.ShowCommandsInInputArea(commands, 4, palette_no=5, width=60)
        cmd = Helper.GetInput(Helper.GetBuiltinText(0x7E5C, 0x7E61) + "(1-4)? ", row=1, required_number_min=1,
                              required_number_max=4)
        if cmd == -1:
            return

        if self.MerchantCheckResourceLimit(cmd) is False:
            return

        officer_no = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x7E63), ShowOfficerFlag.Empty)
        if officer_no == 0:
            return

        if cmd == 1:
            self.SellFood(officer_no)
        if cmd == 2:
            self.BuyFood(officer_no)
        if cmd == 3:
            self.BuyHorse(officer_no)
        if cmd == 4:
            self.BuyWeapons(officer_no)

    def SellFood(self, officer_no):
        Helper.ShowMap(Province.GetActiveNo())

        food_min = self.province.RicePrice

        gold = int(self.province.Food / self.province.RicePrice)
        if gold + self.province.Gold > 30000:
            gold = 30000 - self.province.Gold

        food_max = gold * self.province.RicePrice

        food_sold = Helper.GetInput(Helper.GetBuiltinText(0x7DE6, 0x7DEF) + "({0}-{1})? ".format(food_min, food_max),
                                    required_number_min=food_min, required_number_max=food_max)

        if food_sold > 0:
            self.province.Gold += int(food_sold / self.province.RicePrice)
            self.province.Food -= food_sold
            Helper.ShowDelayedText(
                Helper.GetBuiltinText(0x7DAD, 0x7DC2).replace("%u", str(self.province.Gold)).replace("%lu",
                                                                                                     str(self.province.Food)))

            self.province.Flush()

    def BuyFood(self, officer_no):
        Helper.ShowMap(Province.GetActiveNo())

        food_max = self.province.Gold * self.province.RicePrice
        if food_max + self.province.Food > 3000000:
            food_max = 3000000 - self.province.Food

        food_buy = Helper.GetInput(Helper.GetBuiltinText(0x7DD1).replace("%lu", str(food_max)),
                                   required_number_min=1, required_number_max=food_max)

        if food_buy > 0:
            self.province.Gold -= int(food_buy / self.province.RicePrice) + 1
            self.province.Food += food_buy
            Helper.ShowDelayedText(
                Helper.GetBuiltinText(0x7DAD, 0x7DC2).replace("%u", str(self.province.Gold)).replace("%lu",
                                                                                                     str(self.province.Food)))

            self.province.Flush()

    def BuyHorse(self, officer_no):
        horses_max = min(int(self.province.Gold / 100) + self.province.Horses, 100)
        horses_can_buy = horses_max - self.province.Horses

        num = Helper.GetInput(Helper.GetBuiltinText(0x7D7A) + "(1-{0})? ".format(horses_can_buy), required_number_min=1,
                              required_number_max=horses_can_buy)
        if num > 0:
            self.province.Horses += num
            self.province.Gold -= 100 * num
            self.province.Flush()
            Helper.ShowDelayedText(
                Helper.GetBuiltinText(0x7D8C, 0x7D9A).replace("%d", str(Data.BUF[self.province.Offset + 0x19])))

    def BuyWeapons(self, officer_no):
        officer = self.province.GetOfficerList()[officer_no-1]
        if officer.Weapons==10000:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x7D46))
            return

        weapons_max = 100 - int(officer.Weapons/100)
        weapons_buy = Helper.GetInput(Helper.GetBuiltinText(0x7D58)+"(1-{0})? ".format(weapons_max),required_number_min=1,required_number_max=weapons_max)
        if weapons_buy>0:
            self.province.Gold -= weapons_buy
            officer.Weapons += weapons_buy*100
            if officer.Weapons>10000:
                officer.Weapons = 10000

            self.province.Flush()
            officer.Flush()

            Helper.ShowDelayedText(Helper.GetBuiltinText(0x7D6B).replace("%s",officer.GetName()).replace("%d",str(officer.Weapons)))

    def MerchantCheckExist(self, ):
        province = Province.FromSequence(self.province_no)
        return (Data.BUF[province.Offset + 0x13] & 3) > 0

    def MerchantCheckResourceLimit(self, cmd):
        ret = True
        if cmd == 1:
            if self.province.RicePrice > self.province.Food or self.province.Gold > 30000:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x7DFC))
                ret = False

        if cmd == 2:
            if self.province.Food >= 3000000:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x7E18))
                ret = False

        if cmd == 3:
            if self.province.Horses >= 100:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x7E08))
                ret = False
            if self.province.Gold < 100:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x6070))
                ret = False

        if cmd == 4:
            if self.province.Gold <= 0:
                ret = False

        return ret
