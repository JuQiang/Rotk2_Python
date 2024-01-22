import math
import os.path
import random

from Data import Data, ShowOfficerFlag
import pygame, sys
from Helper import Helper
from RoTK2 import RoTK2
from Data import DelegateMode


class Command5(object):
    def __init__(self):
        pass

    def Start(self, province_no):
        self.province_no = province_no
        self.province = RoTK2.GetProvinceBySequence(province_no)

        commands = [Helper.GetBuiltinText(0x6F78, 0x6F7B), Helper.GetBuiltinText(0x6F81, 0x6F84),
                    Helper.GetBuiltinText(0x6F8A, 0x6F8D), Helper.GetBuiltinText(0x6F93, 0x6F96)]
        Helper.ClearInputArea()

        commands_color = [5, 5, 5, 5]
        is_ruler = RoTK2.IsRuler(self.province.OfficerList[0])
        if is_ruler is False:
            commands_color = [5, 5, 4, 4]
        Helper.ShowCommandsInInputArea(commands, 4, width=60, palette_no=5, commands_color=commands_color)

        cmd = Helper.GetInput(Helper.GetBuiltinText(0x7E5C, 0x7E61) + "(1-4)? ", row=1, required_number_min=1,
                              required_number_max=4)
        if cmd == 1:
            self.Hire(is_ruler)
        if cmd == 2:
            self.Find(is_ruler)
        if cmd == 3:
            self.Assign(is_ruler)
        if cmd == 4:
            self.Fire(is_ruler)

    def Hire(self, is_ruler):
        Helper.ClearInputArea()
        officer_list = []

        is_enemy = False
        if is_ruler is True:
            while True:
                province_no = Helper.GetInput(Helper.GetBuiltinText(0x6F49) + "(1-41)? ", required_number_min=1,
                                              required_number_max=41)
                if province_no < 1:
                    return
                province = RoTK2.GetProvinceBySequence(province_no)
                if province.RulerNo != 0xFF and province.WarRulerNo == 0xFF and Helper.Is2ProvincesAreSameRuler(
                        self.province_no, province_no) is False:
                    # enemy's province
                    is_enemy = True
                    num = len(province.OfficerList)
                    if RoTK2.GetRulerByNo(province.RulerNo).RulerSelf.Offset == province.OfficerList[0].Offset:
                        num -= 1
                    if num == 0:
                        Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F63), clear_input_area=False)
                        return
                    officer_list = province.OfficerList
                    break

                if Helper.Is2ProvincesAreSameRuler(self.province_no, province_no) and self.province_no != province_no:
                    continue
                if self.province.Offset == province.Offset:  # ruler's central province
                    if self.province.UnClaimedOfficerNumber == 0:
                        Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F56))
                        return
                    province = self.province
                    officer_list = province.UnclaimedOfficerList
                    break
        else:  # ruler's general province
            if self.province.UnClaimedOfficerNumber == 0:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F56))
                return
            province = self.province
            officer_list = province.UnclaimedOfficerList

        Helper.ClearInputArea()
        # will hire who?
        is_ruler = RoTK2.IsRuler(RoTK2.GetOfficerByOffset(RoTK2.GetProvinceBySequence(province.No).GovernorOffset))
        officer_no = Helper.SelectOfficer(province.No, Helper.GetBuiltinText(0x6F37), ShowOfficerFlag.Empty,
                                          offical=is_enemy,
                                          show_governor=not is_ruler, enemy_province=True,check_can_action=False)
        if officer_no < 1:
            return

        officer_will_be_hired = officer_list[officer_no - 1]
        self.ShowOfficer(officer_will_be_hired)
        yn = Helper.GetInput(
            RoTK2.GetOfficerName(officer_will_be_hired.Offset) + Helper.GetBuiltinText(0x3D7D) + "(Y/N)? ", yesno=True)
        if yn != "y":
            return

        Helper.ClearInputArea()
        # hire method
        commands = [Helper.GetBuiltinText(0x6EFF, 0x6F06), Helper.GetBuiltinText(0x6F0C, 0x6F0F),
                    Helper.GetBuiltinText(0x6F15, 0x6F18), Helper.GetBuiltinText(0x6F1E, 0x6F21)]
        Helper.ShowCommandsInInputArea(commands, 4, palette_no=3, width=80)
        cmd = Helper.GetInput(Helper.GetBuiltinText(0x6F27, 0x6F2C) + "(1-4)? ", required_number_min=1,
                              required_number_max=4, row=1)
        v_b10c = self.ValidateResourceLimit(cmd)
        if v_b10c == -1:
            return

        if v_b10c > 0:
            officer_no = Helper.SelectOfficer(province.No, Helper.GetBuiltinText(0x6F3E), ShowOfficerFlag.Chm,
                                              offical=True)
            if officer_no < 1:
                return

            officer_will_hire = province.OfficerList[officer_no - 1]
        else:
            officer_will_hire = RoTK2.GetOfficerByOffset(province.GovernorOffset)

        data = self.GetSuccessPercentage(v_b10c, officer_will_be_hired, officer_will_hire,
                                         (province.Offset == self.province.Offset))

        print(data)
        hired_result = Helper.ComapreValueWithRandom100(data)
        continue_seek = self.AdvisorTalkCalculate(hired_result)
        if continue_seek == 0:
            return

        if v_b10c == 1:
            Data.BUF[self.province.Offset + 0x19] -= 1
        if v_b10c == 2:
            Helper.SetWordToOffset(Data.BUF, Helper.GetWordFromOffset(Data.BUF, self.province.Offset + 0x08) - 100,
                                   self.province.Offset + 0x08)

        if province.Offset != self.province.Offset:
            # 29f92
            # TODO
            pass
        else:
            if hired_result == 0:
                self.Talk(officer_will_hire,
                          RoTK2.GetOfficerName(officer_will_be_hired.Offset) +
                          Helper.GetBuiltinText(0x6E93))
            else:
                self.SetNewOfficerState(province.Offset, officer_will_be_hired, officer_will_hire)
                self.Talk(officer_will_hire,
                          Helper.GetBuiltinText(0x6E72) +
                          RoTK2.GetOfficerName(officer_will_be_hired.Offset) +
                          Helper.GetBuiltinText(0x6E79))
                Helper.ShowMap(self.province_no)

    def SetOfficerLoyal(self, officer, ruler):
        compatibility = self.GetCompatibility(officer, ruler)
        officer.Loyalty = abs(100 - int(math.sqrt(int(officer.Loyalty / 2) * compatibility))) - random.randint(0, 5)

    def SetNewOfficerState(self, province_offset, officer_will_be_hired, officer_will_hire):
        rs = self.GetOfficerRulerRelationship(officer_will_be_hired)
        if rs != 4:
            # TODO
            pass
        else:
            officer_will_be_hired.RulerNo = officer_will_hire.RulerNo
            officer_will_be_hired.Loyalty = 0x28
            ruler = RoTK2.GetRulerByNo(officer_will_be_hired.RulerNo)
            self.SetOfficerLoyal(officer_will_be_hired, ruler.RulerSelf)
            # TODO
            # skip spy operation
            # see 243E8
            officer_will_be_hired.shiwei = 1

            Helper.LinkListRemoveObjectFromOffset(province_offset + 4, officer_will_be_hired.Offset)
            Helper.LinklistAppendObject(province_offset + 2, officer_will_be_hired.Offset)

    def GetOfficerRulerRelationship(self, officer_will_be_hired):
        if officer_will_be_hired.RulerNo == 0xFF:
            return 4
        else:
            # TODO
            pass

    def GetRelationShipInDifferentProvince(self, v_b10c, officer_will_be_hired, officer_will_hire):
        pass

    def GetCompatibility(self, officer_1, officer_2):
        return abs(officer_1.Compatibility - officer_2.Compatibility)

    def GetSuccessPercentage(self, v_b10c, officer_will_be_hired, officer_will_hire, is_same_city):
        if is_same_city:
            diff = self.GetCompatibility(officer_will_be_hired, officer_will_hire)
            compatibility = 120 - int(diff / 2) - random.randint(0, 10)
        else:
            compatibility = 100 - officer_will_be_hired.Loyalty
            if RoTK2.IsRuler(officer_will_hire):
                compatibility = int(1.1 * compatibility)

        data = self.GetRelationShip(officer_will_be_hired, officer_will_hire, v_b10c, compatibility)
        if (Data.BUF[officer_will_be_hired.Offset + 2] & 2) == 2:
            data *= 2

        return data % 256

    def GetRelationShip(self, officer_will_be_hired, officer_will_hire, cmd, compatibility):
        data = 0
        trust = RoTK2.GetRulerByNo(self.province.RulerNo).TrustRating

        if cmd == 0:
            data = officer_will_be_hired.Chm + officer_will_be_hired.Int
        elif cmd == 1:
            data = officer_will_be_hired.War * 3 + officer_will_be_hired.Chm
        elif cmd == 2:
            data = 2 * (100 - officer_will_be_hired.yili) - officer_will_be_hired.Chm + officer_will_be_hired.yewang
        elif cmd == 3:
            data = 2 * trust + officer_will_hire.Chm
        else:
            raise Exception("Invalid cmd.")

        diff = (Data.GAME_DIFFCULTY + 3) * 0x32
        ruler_data = trust + data

        return int(compatibility * diff / ruler_data) % 256

    def ValidateResourceLimit(self, cmd):
        if cmd == 1:
            # check governor can do action
            # if self.province.Governor
            pass
        if cmd == 2 and self.province.Horses < 1:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6F2E))
            return -1
        if cmd == 3 and self.province.Gold < 100:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6070))
            return -1

        return cmd - 1

    def Find(self, is_ruler):
        Helper.ClearInputArea()
        officer_no = Helper.SelectOfficer(self.province_no, Helper.GetBuiltinText(0x6EA5), ShowOfficerFlag.Chm)
        if officer_no < 1:
            return

        officer = self.province.OfficerList[officer_no - 1]
        num1 = int(officer.Int / 3) + int(officer.Chm / 2)
        num2 = random.randint(0, 20)
        magic = num1 - min(num1, num2)
        if self.province.FreeOfficerOffset == 0:
            magic = 0

        magic = Helper.ComapreValueWithRandom100(magic)
        continue_seek = self.AdvisorTalkCalculate(magic)
        if continue_seek == 0:
            return

        if magic == 1 or Helper.GetWordFromOffset(Data.BUF, self.province.Offset + 6) == 0:
            self.Talk(officer, Helper.GetBuiltinText(0x6ECF))
            return

        free_list = Helper.GetProvinceFreeOfficerList(self.province)
        general = free_list[random.randint(0, len(free_list) - 1)]
        Helper.LinkListRemoveObjectFromOffset(self.province.Offset + 6, general.Offset)
        Helper.LinklistAppendObject(self.province.Offset + 4, general.Offset)

        Data.BUF[general.Offset + 0x0B] = 0
        Data.BUF[general.Offset + 0x0C] = 0

        self.ShowOfficer(general)
        self.Talk(officer, RoTK2.GetOfficerName(general.Offset) + Helper.GetBuiltinText(0x6EB5))

    def ShowOfficer(self, officer):
        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        img = Helper.GetFace(officer.Portrait)
        bmp.blit(img, (5, 35))
        img = Helper.DrawText(RoTK2.GetOfficerName(officer.Offset))
        bmp.blit(img, (85, 95))

        bmp = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
        pygame.display.flip()

    def Talk(self, officer, talk):
        bmp = pygame.Surface((330, 90))
        bmp.fill((0, 0, 0))

        img = Helper.GetFace(officer.Portrait)
        bmp.blit(img, (5, 5))

        left = 80
        top = 50

        pygame.draw.rect(bmp, (255, 255, 255), (left + 10, 5, 200, 80), border_radius=5)

        pygame.draw.rect(bmp, (255, 255, 255), (left, top, 5, 2))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 5, top - 3, 2, 6))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 7, top - 6, 2, 12))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 9, top - 9, 2, 18))

        talk_data = talk.split("_")
        for i in range(0, len(talk_data)):
            img = Helper.DrawText(talk_data[i], back_color=(255, 255, 255), palette_no=0)
            bmp.blit(img, (left + 15, 15 + 30 * i))

        bmp = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 300 * Helper.Scale))
        pygame.display.flip()

        pygame.time.delay(1000)

    def AdvisorTalkCalculate(self, magic):
        advisor = RoTK2.GetAdvisor()
        if advisor is None:
            return 1

        exist_advisor = False
        for officer in self.province.OfficerList:
            if officer.Offset == advisor.Offset:
                exist_advisor = True
                break

        if exist_advisor is False:
            return 1

        # num1 = (2*(0xE4 - advisor.Int))%256
        num1 = 200 - 2 * advisor.Int
        num2 = random.randint(0, 100)
        magic = 1 if num1 >= num2 else 0

        return 1

    def Assign(self,is_ruler):
        if is_ruler is False:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x605C))
            return

        commands = [Helper.GetBuiltinText(0x6DD0), Helper.GetBuiltinText(0x6DD5)]
        Helper.ShowCommandsInInputArea(commands, 4, palette_no=3)

        cmd = Helper.GetInput(Helper.GetBuiltinText(0x6E28) + "(1-2)? ", row=1, required_number_min=1,
                              required_number_max=2)
        if cmd < 1:
            return

        if cmd == 1:
            self.AssignGovernor()
        if cmd == 2:
            self.AssignAdvisor()

    def Fire(self, is_ruler):
        if is_ruler is False:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x605C))
            return

        commands = [Helper.GetBuiltinText(0x6D6F, 0x6D76), Helper.GetBuiltinText(0x6D7B, 0x6D7E)]
        Helper.ShowCommandsInInputArea(commands, 4, palette_no=3)

        cmd = Helper.GetInput(Helper.GetBuiltinText(0x6D84) + "(1-2)? ", row=1, required_number_min=1,
                              required_number_max=2)
        if cmd < 1:
            return

        if cmd == 1:
            self.FireOfficer()
        if cmd == 2:
            self.FireAdvisor()

    def FireAdvisor(self):
        advisor = RoTK2.GetAdvisor()
        if advisor is None:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x6D22))
            return

        Helper.ClearInputArea()

        text = Helper.GetBuiltinText(0x6D2B).replace("%s",RoTK2.GetOfficerName(advisor.Offset))
        text_list = Helper.GetColorTextInformation(text)
        img_width = Helper.RenderColorText(text_list,300*Helper.Scale,300*Helper.Scale)

        yn = Helper.GetInput("(Y/N)? ", x=300 + img_width, width=300 - img_width - 10, yesno=True)
        if yn != "y":
            return

        ruler_offset = Helper.GetWordFromOffset(Data.BUF, Data.CURRENT_RULER_OFFSET)
        Helper.SetWordToOffset(Data.BUF, 0, ruler_offset + 4)

        Helper.ShowDelayedText(Helper.GetBuiltinText(0x6D46).replace("%s", RoTK2.GetOfficerName(advisor.Offset)),
                               top=330, palette_no=7)

        Helper.ShowMap(self.province_no)

    def FireOfficer(self):
        while True:
            Helper.ClearInputArea()
            province_no = Helper.GetInput(Helper.GetBuiltinText(0x6D5C) + "(1-41)? ", required_number_min=1,
                                          required_number_max=41,allow_enter_exit=True)

            if province_no==-1:
                break

            if self.CanFireOfficer(province_no) is False:
                continue

            province = RoTK2.GetProvinceBySequence(province_no)

            show_governor = not (RoTK2.GetCurrentRulerOfficerOffset() == province.OfficerList[0].Offset)
            while True:
                officer_no = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x6CEE), ShowOfficerFlag.Loyalty,
                                                  show_governor=show_governor, check_can_action=False)
                if officer_no >= 0:
                    break

            if officer_no == 0:
                continue

            if self.ConfirmFireOfficer(province,officer_no) is False:
                continue

            officer = province.OfficerList[officer_no - 1]

            # remove officer
            officer.Soldiers = 0
            officer.Loyalty = 0
            officer.Weapons = 0
            RoTK2.FlushOfficer(officer)

            Helper.ShowDelayedText(RoTK2.GetOfficerName(officer.Offset) + Helper.GetBuiltinText(0x6D15, 0x6D1C))

            province.OfficerList.pop(officer_no - 1)

            Helper.LinkListRemoveObjectFromOffset(province.Offset+2, officer.Offset)

            num = min(0x7530, int((officer.Soldiers + province.Population) / 100))
            province.Population = num * 100

            RoTK2.FlushProvince(province)

            if len(province.OfficerList)==0:
                # empty province now.
                Helper.SetWordToOffset(Data.BUF,0,province.Offset+2)
                Data.BUF[province.Offset + 0x10] = 0xFF
                Data.BUF[province.Offset + 0x12] = 0x00
                Data.BUF[province.Offset + 0x14] = 0xFF
                Data.BUF[province.Offset + 0x15] = 0xFF

                ruler_offset = Helper.GetWordFromOffset(Data.BUF,Data.CURRENT_RULER_OFFSET)
                Helper.LinkListRemoveObjectFromOffset(ruler_offset+2,province.Offset)

                Helper.MainMap = Helper.GetMap()
                pygame.display.flip()
            else:
                if len(province.OfficerList)==1:
                    governor = province.OfficerList[0]
                else:
                    if RoTK2.GetProvinceDelegateStatus(province_no)>0:
                        governor = sorted(province.OfficerList,key=lambda x:x.Loyalty,reverse=True)[0]
                    else:
                        while True:
                            officer_no = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x3F75).replace("%s",RoTK2.GetOfficerName(RoTK2.GetCurrentRulerOfficerOffset())).replace("%2d",str(province_no)),
                                                              ShowOfficerFlag.Loyalty,show_governor=False,check_can_action=False)
                            if officer_no>0:
                                break

                        governor = province.OfficerList[officer_no-2]
                        province.OfficerList.pop(officer_no-2)

                Helper.SetWordToOffset(Data.BUF,province.Offset+2,officer.Offset)


            # move officer to other province as a free officer
            neighbors = Helper.GetNeighbors(province_no)
            while True:
                neighbor = random.randint(0, len(neighbors) - 1)
                if neighbors[neighbor]<256:
                    break
            neighbor_province = RoTK2.GetProvinceBySequence(neighbors[neighbor])
            Helper.LinklistAppendObject(neighbor_province.Offset + 6, officer.Offset)


    def ConfirmFireOfficer(self,province,officer_no):
        text = Helper.GetBuiltinText(0x6CF7).replace("%s",RoTK2.GetOfficerName(province.OfficerList[officer_no - 1].Offset))
        text_list = Helper.GetColorTextInformation(text)
        img_width = Helper.RenderColorText(text_list,300*Helper.Scale,330*Helper.Scale)

        yn = Helper.GetInput("(Y/N)? ", x=300+img_width, y=330, width=300 - img_width - 10, yesno=True)

        return yn == "y"
    def CanFireOfficer(self,province_no):
        can_fire_officer = True
        if province_no < 1:
            can_fire_officer = False

        if Helper.Is2ProvincesAreSameRuler(self.province_no, province_no) is False:
            can_fire_officer = False

        province = RoTK2.GetProvinceBySequence(province_no)
        if province.WarRulerNo != 0xFF:
            can_fire_officer = False

        return can_fire_officer

    def CanAssignGovernor(self,province_no):
        can_assign_governor = True
        if province_no < 1:
            can_assign_governor = False

        if Helper.Is2ProvincesAreSameRuler(self.province_no, province_no) is False:
            can_assign_governor = False

        province = RoTK2.GetProvinceBySequence(province_no)
        if province.WarRulerNo != 0xFF:
            can_assign_governor = False

        if province_no==self.province_no:
            can_assign_governor = False

        if len(province.OfficerList)==1:
            can_assign_governor = False

        return can_assign_governor
    def AssignGovernor(self):
        while True:
            Helper.ClearInputArea()
            province_no = Helper.GetInput(Helper.GetBuiltinText(0x6D5C) + "(1-41)? ", required_number_min=1,
                                          required_number_max=41, allow_enter_exit=True)

            if province_no == -1:
                break

            if self.CanAssignGovernor(province_no) is False:
                continue

            province = RoTK2.GetProvinceBySequence(province_no)
            while True:
                officer_no = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x6D9A), ShowOfficerFlag.Loyalty,check_can_action=False)
                if officer_no >= 0:
                    break

            if officer_no == 0:
                continue

            officer = province.OfficerList[officer_no - 1]
            province.OfficerList.pop(officer_no-1)

            Helper.SetWordToOffset(Data.BUF,province.OfficerList[0].Offset,officer.Offset)
            for i in range(0,len(province.OfficerList)-1):
                Helper.SetWordToOffset(Data.BUF, province.OfficerList[i+1].Offset, province.OfficerList[i].Offset)
            Helper.SetWordToOffset(Data.BUF, 0, province.OfficerList[i+1].Offset)

            Helper.SetWordToOffset(Data.BUF, officer.Offset,province.Offset + 2)
            Helper.ShowDelayedText(RoTK2.GetOfficerName(officer.Offset)+Helper.GetBuiltinText(0x6DE4,0x6DE7)+Helper.GetBuiltinText(0x6DD0))

    def AssignAdvisor(self):
        self.RenderColorText(0x6E3D)
        while True:
            Helper.ClearInputArea()
            text = Helper.GetBuiltinText(0x6E3D)
            province_no = Helper.GetInput(Helper.GetBuiltinText(0x6D5C) + "(1-41)? ", required_number_min=1,
                                          required_number_max=41, allow_enter_exit=True)

            if province_no == -1:
                break

            if self.CanAssignGovernor(province_no) is False:
                continue

            province = RoTK2.GetProvinceBySequence(province_no)
            while True:
                officer_no = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x6D9A), ShowOfficerFlag.Loyalty,check_can_action=False)
                if officer_no >= 0:
                    break

            if officer_no == 0:
                continue

            officer = province.OfficerList[officer_no - 1]
            province.OfficerList.pop(officer_no-1)

            Helper.SetWordToOffset(Data.BUF,province.OfficerList[0].Offset,officer.Offset)
            for i in range(0,len(province.OfficerList)-1):
                Helper.SetWordToOffset(Data.BUF, province.OfficerList[i+1].Offset, province.OfficerList[i].Offset)
            Helper.SetWordToOffset(Data.BUF, 0, province.OfficerList[i+1].Offset)

            Helper.SetWordToOffset(Data.BUF, officer.Offset,province.Offset + 2)
            Helper.ShowDelayedText(RoTK2.GetOfficerName(officer.Offset)+Helper.GetBuiltinText(0x6DE4,0x6DE7)+Helper.GetBuiltinText(0x6DD0))
