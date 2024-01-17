import math
import os.path
import random

from Data import Data, ShowOfficerFlag
import pygame,sys
from Helper import Helper
from RoTK2 import RoTK2
from Data import DelegateMode

class Command5(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        self.province_no = province_no
        self.province = RoTK2.GetProvinceBySequence(province_no)

        commands = [Helper.GetBuiltinText(0x6F78,0x6F7B),Helper.GetBuiltinText(0x6F81,0x6F84),Helper.GetBuiltinText(0x6F8A,0x6F8D),Helper.GetBuiltinText(0x6F93,0x6F96)]
        Helper.ClearInputArea()

        commands_color=[5,5,5,5]
        is_ruler = RoTK2.IsRuler(self.province.OfficerList[0])
        if is_ruler is False:
            commands_color = [5,5,1,1]
        Helper.ShowCommandsInInputArea(commands,4,width=60,palette_no=5,commands_color=commands_color)

        cmd = Helper.GetInput(Helper.GetBuiltinText(0x7E5C, 0x7E61) + "(1-4)? ", row=1, required_number_min=1,
                              required_number_max=4)
        if cmd==1:
            self.Hire(is_ruler)
        if cmd==2:
            self.Find(is_ruler)

    def Hire(self,is_ruler):
        Helper.ClearInputArea()

        if is_ruler is True:
            while True:
                province_no = Helper.GetInput(Helper.GetBuiltinText(0x6F49)+"(1-41)? ",required_number_min=1,required_number_max=41)
                if province_no<1:
                    return
                province = RoTK2.GetProvinceBySequence(province_no)
                if province.RulerNo!=0xFF and province.WarRulerNo==0xFF and Helper.Is2ProvincesAreSameRuler(self.province_no,province_no) is False:
                    num = len(province.OfficerList)
                    if RoTK2.GetRulerByNo(province.RulerNo).RulerSelf.Offset == province.OfficerList[0].Offset:
                        num -= 1
                    if num==0:
                        Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F63),clear_input_area=False)
                        return
                    break
        else:
            if self.province.UnClaimedOfficerNumber==0:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F56))
                return


    def Find(self,is_ruler):
        Helper.ClearInputArea()
        officer_no = Helper.SelectOfficer(self.province_no, Helper.GetBuiltinText(0x6EA5), ShowOfficerFlag.Chm)
        if officer_no<1:
            return

        officer = self.province.OfficerList[officer_no-1]
        num1 = int(officer.Int/3)+int(officer.Chm/2)
        num2 = random.randint(0,20)
        magic = num1 - min(num1,num2)
        if self.province.FreeOfficerOffset==0:
            magic = 0
        num2 = random.randint(0,100)
        magic = 1 if magic>=num2 else 0
        continue_seek = self.AdvisorTalkCalculate(magic)
        if continue_seek==0:
            return

        if magic==1 or Helper.GetWordFromOffset(Data.BUF,self.province.Offset+6)==0:
            self.Talk(officer,Helper.GetBuiltinText(0x6ECF))
            return

        free_list = Helper.GetProvinceFreeOfficerList(self.province)
        general = free_list[random.randint(0,len(free_list)-1)]
        Helper.LinkListRemoveObjectFromOffset(self.province.Offset+6,general.Offset)
        Helper.LinklistAppendObject(self.province.Offset+4,general.Offset)

        Data.BUF[general.Offset + 0x0B] = 0
        Data.BUF[general.Offset+0x0C] = 0

        self.OfficerFound(general)
        self.Talk(officer,Helper.GetBuiltinText(0x6EB5))

    def OfficerFound(self,officer):
        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        img = Helper.GetFace(officer.Portrait)
        bmp.blit(img, (5, 35))
        img = Helper.DrawText(RoTK2.GetOfficerName(officer.Offset))
        bmp.blit(img, (85, 95))

        bmp = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
        pygame.display.flip()

    def Talk(self,officer,talk):
        bmp = pygame.Surface((330, 90))
        bmp.fill((0, 0, 0))

        img = Helper.GetFace(officer.Portrait)
        bmp.blit(img,(5,5))

        left = 80
        top = 50

        pygame.draw.rect(bmp,(255,255,255),(left+10,5,200,80),border_radius=5)

        pygame.draw.rect(bmp, (255, 255, 255), (left, top, 5, 2))
        pygame.draw.rect(bmp, (255, 255, 255), (left+5, top-3, 2, 6))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 7, top - 6, 2, 12))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 9, top - 9, 2, 18))

        talk_data = talk.split("_")
        for i in range(0,len(talk_data)):
            img = Helper.DrawText(talk_data[i],back_color=(255,255,255),palette_no=0)
            bmp.blit(img,(left+15,15+30*i))

        bmp = pygame.transform.scale(bmp,(bmp.get_width()*Helper.Scale,bmp.get_height()*Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 300 * Helper.Scale))
        pygame.display.flip()

        pygame.time.delay(1000)

    def AdvisorTalkCalculate(self,magic):
        advisor = RoTK2.GetAdvisor()
        if advisor is None:
            return 1

        exist_advisor = False
        for officer in self.province.OfficerList:
            if officer.Offset==advisor.Offset:
                exist_advisor = True
                break

        if exist_advisor is False:
            return 1

        #num1 = (2*(0xE4 - advisor.Int))%256
        num1 = 200-2*advisor.Int
        num2 = random.randint(0,100)
        magic = 1 if num1>=num2 else 0

        return 1


    def Assign(self):
        pass

    def Fire(self):
        pass

