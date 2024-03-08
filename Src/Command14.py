import math
import os.path
import random

from Data import Data
import pygame,sys
from Helper import Helper,Province,Officer,Ruler

from Data import DelegateMode

class Command14(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        game_month = Data.DSBUF[0x46]
        if game_month+1 in (7,8,9):
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x7EA6))
            return

        Helper.ClearInputArea()

        yn = Helper.GetInput(Helper.GetBuiltinText(0x7E82)+"(Y/N)? ",yesno=True)
        if yn!="y":
            return

        #should check governor can do action.
        province = Province.FromSequence(province_no)
        offset = province.Offset
        if Data.BUF[offset+0x13] & 4 == 4:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x7EA6),palette_no=6)
            return

        v1 = int(int(math.sqrt(province.Population/100))/10)
        v1 = max(v1,7)
        v1 += Ruler.FromNo(Ruler.GetActiveNo()).TrustRating
        v1 += province.Loyalty

        v2 = random.randint(1,0x385)
        gold = int(v1*v2/0xc8)
        new_gold = gold + province.Gold
        if new_gold>30000:
            new_gold = 30000

        Data.BUF[province.Offset+9]= new_gold>>8
        Data.BUF[province.Offset + 8] = new_gold % 256

        v3 = random.randint(0,0xAFC9)+0x1388
        food = int(v3*v1/0xc8)
        new_food = food + province.Food

        if new_food>3000000:
            new_food = 3000000

        Data.BUF[province.Offset+0x0D]= new_food>>24
        Data.BUF[province.Offset + 0x0C] = (new_food>>16) & 0xFF
        Data.BUF[province.Offset+0x0B]= (new_food>>8) & 0xFF
        Data.BUF[province.Offset + 0x0A] = new_food % 256

        Data.BUF[province.Offset+0x17] = max(0,Data.BUF[province.Offset+0x17]-0x0A)
        ruler_offset = Data.BUF[0x3395]*256+Data.BUF[0x3394]
        Data.BUF[ruler_offset+6] = max(0,Data.BUF[ruler_offset+6]-5)

        text = Helper.GetBuiltinText(0x7E8E,0x7E9E).replace("%u",str(gold))+str(food)
        Helper.ShowDelayedText(text)
        offset = province.Offset
        Data.BUF[offset+0x13] |= 4

