import os.path
import random
from Data import Data
import pygame, sys
from Helper import Helper, Province, Officer, Ruler
from Data import DelegateMode


class Command18(object):
    def __init__(self):
        self.commands = [Helper.GetBuiltinText(0x89DE, 0x89E1), Helper.GetBuiltinText(0x89EB, 0x89EE),
                         Helper.GetBuiltinText(0x89F8, 0x89FB)]
        self.palette_no = 5
        self.commands_color = [self.palette_no] * 3
        self.province_no = -1

    def GetPassenger(self):
        current_ruler_province = Data.GetWordFromOffset(Data.BUF, 0x339A)
        province_no = int((current_ruler_province - 0x2DC4) / 0x23)
        passenger_no = self.GetPassengerInProvince(province_no)
        if passenger_no <= 2:
            return passenger_no

        x = Data.BUF[current_ruler_province + 0x20]
        y = Data.BUF[current_ruler_province + 0x21]

        Helper.NeighborsRandomChoice()
        for i in range(0, 6):
            loop = Data.DSBUF[0xAFF6 + i]
            province_no = Helper.GetNeighbor(x, y, loop)
            if province_no != 0xFF:
                passenger_no = self.GetPassengerInProvince(province_no)
                if passenger_no < 2:
                    return passenger_no

        return 0xFF

    def ShowTalk(self, passenger_no, talk):
        talk_data = talk.split("_")

        if passenger_no < 3:
            if passenger_no < 2:
                passenger_name = Helper.GetBuiltinText(
                    Data.DSBUF[0x8710 + 2 * passenger_no + 1] * 256 + Data.DSBUF[0x8710 + 2 * passenger_no + 0])
                passenger_name = Helper.GetBuiltinText(0x6189).replace("%s", passenger_name)
            else:
                passenger_name = Helper.GetBuiltinText(Data.DSBUF[0x8714 + 1] * 256 + Data.DSBUF[0x8714 + 0])
                passenger_name = Helper.GetBuiltinText(0x6192).replace("%s", passenger_name)
            passenger_face = Data.DSBUF[0x871C + 2 * passenger_no + 1] * 256 + Data.DSBUF[
                0x871C + 2 * passenger_no + 0] - 1
        else:
            advisor = Officer.GetAdvisor()
            passenger_name = advisor.GetName()
            passenger_name = Helper.GetBuiltinText(0x619b).replace("%s", passenger_name)
            passenger_face = advisor.Portrait

        max_length = 0

        for i in range(0, len(talk_data)):
            img = Helper.DrawText(talk_data[i], back_color=(255, 255, 255), palette_no=0)
            if img.get_width()>max_length:
                max_length = img.get_width()

        max_length += 8
        bmp = pygame.Surface((330, 160))
        bmp.fill((0, 0, 0))

        img = Helper.DrawText(passenger_name)
        bmp.blit(img, (90, 2))

        img = Helper.GetFace(passenger_face)
        bmp.blit(img, (10, 30))

        pygame.draw.rect(bmp, (255, 255, 255), (100, 40, max_length, 80), border_radius=5)
        left = 90
        top = 80
        pygame.draw.rect(bmp, (255, 255, 255), (left, top, 5, 2))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 5, top - 3, 2, 6))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 7, top - 6, 2, 12))
        pygame.draw.rect(bmp, (255, 255, 255), (left + 9, top - 9, 2, 18))


        for i in range(0, len(talk_data)):
            img = Helper.DrawText(talk_data[i], back_color=(255, 255, 255), palette_no=0)
            bmp.blit(img, (105, 50 + 30 * i))

        bmp = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
        pygame.display.flip()

        Helper.ClearInputArea()
        Helper.GetInput(Helper.GetBuiltinText(0x588A))

    def GetPassengerInProvince(self, province_no):
        if Data.BUF[0x2B30 + 0] == province_no and Data.BUF[0x2B30 + 1] == province_no:
            index = random.randint(0, 1)
            return index
        elif Data.BUF[0x2B30 + 0] == province_no:
            return 0
        elif Data.BUF[0x2B30 + 1] == province_no:
            return 1
        if Data.BUF[0x2B30 + 2] == province_no:
            return 2

        return 0xFF

    def Start(self, province_no):
        self.province_no = province_no

        passenger = self.GetPassenger()

        Helper.ClearInputArea()
        if Province.GetAdvisorProvince() != province_no:
            self.commands_color[0] = 4

        if passenger > 1:
            self.commands_color[1] = 4
        if passenger > 2:
            self.commands_color[2] = 4

        Helper.ShowCommandsInInputArea(self.commands, 3, palette_no=self.palette_no, width=70,
                                       commands_color=self.commands_color)

        cmd = Helper.GetInput(Helper.GetBuiltinText(0x5342) + "(1-{0})?".format(len(self.commands)), row=1,
                              required_number_min=1, required_number_max=3, allow_enter_exit=True)

        if cmd == 1:
            ruler_offset = Data.BUF[Data.CURRENT_RULER_OFFSET + 1] * 256 + Data.BUF[Data.CURRENT_RULER_OFFSET + 0]
            advisor_offset = Data.BUF[ruler_offset + 1] * 256 + Data.BUF[ruler_offset + 0]

            if advisor_offset == 0 or Province.GetAdvisorProvince() != province_no:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x89BA), palette_no=7)
                return

            if ((Data.BUF[ruler_offset + 7] & 0x20) == 0x20) or (
                    Data.BUF[advisor_offset + 0x0B] <= random.randint(0, 100)):
                choice = random.randint(0, 1)
                text = Data.DSBUF[0x89D4 + 2 * choice + 1] * 256 + Data.DSBUF[0x89D4 + 2 * choice + 0]
                self.ShowTalk(3, Helper.GetBuiltinText(text))
                return

            while True:
                choice = random.randint(-2, 2)
                # choice = random.randint(0, 2)
                if choice < 0:
                    self.AdviceNo()
                    return

                if choice == 0 and self.AdviceWar() is True:
                    break
                if choice == 1 and self.AdviceOfficer() is True:
                    break
                if choice == 2 and self.AdviceSpy() is True:
                    break

            self.AdviceSetStatus()

        if cmd == 2:
            if passenger > 1:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x8830), palette_no=7)
                return

            if passenger == 0:
                self.Simahui()
            else:
                self.Xuzijiang()

        if cmd == 3:
            if Helper.GetHuatuo() != province_no:
                Helper.ShowDelayedText(Helper.GetBuiltinText(0x8779), palette_no=7)
                return

            province = Province.FromSequence(self.province_no)
            sick_officers = []
            for o in province.GetOfficerList():
                if o.IsSick is True:
                    sick_officers.append(o)

            if len(sick_officers) == 0:
                self.ShowTalk(2, Helper.GetBuiltinText(Data.DSBUF[0x8785] * 256 + Data.DSBUF[0x8784]))
            else:
                self.ShowTalk(2, Helper.GetBuiltinText(Data.DSBUF[0x8787] * 256 + Data.DSBUF[0x8786]))
                for o in sick_officers:
                    Data.BUF[o.Offset + 3] &= 0xF0

    def AdviceSetStatus(self):
        ruler_offset = Data.BUF[Data.CURRENT_RULER_OFFSET + 1] * 256 + Data.BUF[Data.CURRENT_RULER_OFFSET + 0]
        Data.BUF[ruler_offset + 7] &= 0x20

    def AdviceNo(self):
        choice = random.randint(0, 1)
        text = Data.DSBUF[0x89D4 + 2 * choice + 0x01] * 256 + Data.DSBUF[0x89D4 + 2 * choice + 0x00]
        self.ShowTalk(3, Helper.GetBuiltinText(text))

    def AdviceWar(self):
        neighbors = Helper.GetNeighbors(self.province_no)

        choice = random.randint(-2, 3)
        # choice = random.randint(0, 3)
        if choice < 0:
            return False

        succ = False
        war_province = 0
        for i in range(0, 3):
            if choice == 0:
                war_province = self.AdviceWar1(neighbors)
                if war_province > 0:
                    break
            elif choice == 1:
                war_province = self.AdviceWar2(neighbors)
                if war_province > 0:
                    break
            elif choice == 2:
                war_province = self.AdviceWar3(neighbors)
                if war_province > 0:
                    break
            elif choice == 3:
                war_province = self.AdviceWar4(neighbors)
                if war_province > 0:
                    break

        if war_province == 0:
            return False

        choice2 = choice + i
        choice2 &= 3

        choice = random.randint(0, 2)
        choice3 = random.randint(0, 6)
        text2 = Data.DSBUF[0x8982 + 2 * choice3 + 0x01] * 256 + Data.DSBUF[0x8982 + 2 * choice3 + 0x00]
        text = Helper.GetBuiltinText(0x896F) + str(war_province) + Helper.GetBuiltinText(text2) + "_"

        # if choice2==2 and choice==0:
        #     text += Helper.GetBuiltinText(0x8963)
        # else:
        #     text += Helper.GetBuiltinText(0x895A)

        self.ShowTalk(3, text)
        return True
        # return False

    def IsNeighborCanAttack(self, neighbor):
        if neighbor == 256:
            return False

        province = Province.FromSequence(neighbor)

        if province.RulerNo == Ruler.GetActiveNo() or province.RulerNo == 0xFF or province.WarRulerNo != 0xFF:
            return False
        return True

    def AdviceWar1(self, neighbors):
        for neighbor in neighbors:
            if self.IsNeighborCanAttack(neighbor):
                province = Province.FromSequence(neighbor)
                if province.Soldiers / 2 > province.Food:
                    return neighbor

        return 0

    def AdviceWar2(self, neighbors):
        me = Province.FromSequence(Province.GetActiveNo())

        for neighbor in neighbors:
            if self.IsNeighborCanAttack(neighbor):
                province = Province.FromSequence(neighbor)
                if province.Soldiers > me.Soldiers:
                    return neighbor

        return 0

    def AdviceWar3(self, neighbors):
        me = Province.FromSequence(Province.GetActiveNo())
        for neighbor in neighbors:
            if self.IsNeighborCanAttack(neighbor):
                province = Province.FromSequence(neighbor)
                if province.Soldiers < me.Soldiers / 3:
                    return neighbor

        return 0

    def AdviceWar4(self, neighbors):
        me = Province.FromSequence(Province.GetActiveNo())
        for neighbor in neighbors:
            if self.IsNeighborCanAttack(neighbor):
                province = Province.FromSequence(neighbor)
                if len(province.GetOfficerList()) >= 0x14:
                    return neighbor

        return 0

    def AdviceOfficer(self):
        ruler_list = []

        for ruler in Ruler.GetList():
            if ruler.RulerSelf.Offset == Helper.GetCurrentRulerOfficerOffset():
                continue
            ruler_list.append(ruler)

        choice = random.randint(0, 100)
        if choice >= 0x46:
            choice = random.randint(0, 1) + 1
        else:
            choice = 0

        ruler = ruler_list[random.randint(0, len(ruler_list) - 1)]
        officer_list = []

        province_list = Province.GetListByRulerNo(ruler.No)
        for province in province_list:
            for officer in province.GetOfficerList():
                if officer.Offset == ruler.RulerSelf.Offset:
                    continue

                if choice == 0 and officer.Loyalty <= 50:
                    officer_list.append(officer)
                if choice == 1 and officer.Int >= 95:
                    officer_list.append(officer)
                if choice == 2 and officer.War >= 95:
                    officer_list.append(officer)

        if len(officer_list) > 0:
            text = [Data.DSBUF[0x88C7] * 256 + Data.DSBUF[0x88C6], Data.DSBUF[0x88C9] * 256 + Data.DSBUF[0x88C8],
                    Data.DSBUF[0x88CB] * 256 + Data.DSBUF[0x88CA]]
            choice2 = random.randint(0, len(officer_list) - 1)
            name = officer_list[choice2].GetName()

            self.ShowTalk(3, name + Helper.GetBuiltinText(text[choice]))
            return True
        else:
            return False

    def AdviceSpy(self):
        officer_list = []

        province_list = Province.GetListByRulerNo(Ruler.GetActiveNo())
        for province in province_list:
            for officer in province.GetOfficerList():
                if (Data.BUF[officer.Offset + 2] & 0x20 == 0x20) or (Data.BUF[officer.Offset + 3] & 0xF0 == 0xF0):
                    officer_list.append(officer)

        if len(officer_list) > 0:
            choice = random.randint(0, 1)
            text = [Data.DSBUF[0x887B] * 256 + Data.DSBUF[0x887A], Data.DSBUF[0x887D] * 256 + Data.DSBUF[0x887C]]
            choice2 = random.randint(0, len(officer_list) - 1)
            name = officer_list[choice2].GetName()

            self.ShowTalk(3, name + Helper.GetBuiltinText(text[choice]))
            return True
        else:
            return False

    def Simahui(self):
        ruler_list = Ruler.GetList()
        ruler1 = random.randint(0, len(ruler_list) - 1)
        ruler1_name = ""
        ruler2_name = ""

        index = -1
        for ruler in ruler_list:
            index += 1
            if (ruler.No == Helper.GetCurrentRulerNo()) or (Data.BUF[ruler.Offset + 0x22] != 0xFF):
                continue

            if index == ruler1:
                ruler1_name = Ruler.GetNameFromProvinceSequence(self.province_no)
                ruler2 = Data.BUF[ruler.Offset + 0x09]
                if ruler2 != 0xFF:
                    ruler2_name = ruler_list[ruler2].RulerSelf.GetName()
                    break

        if len(ruler1_name) > 0:
            choice = random.randint(0, 99)
            if choice < 0x32:
                self.ShowTalk(0, ruler1_name + Helper.GetBuiltinText(0x8817) + ruler2_name)
            else:
                self.ShowTalk(0, ruler1_name + Helper.GetBuiltinText(0x8820))
        else:
            for i in range(0, 41):
                province_offset = Data.PROVINCE_START + Data.PROVINCE_SIZE * i
                if (Data.BUF[province_offset + 5] * 256 + Data.BUF[province_offset + 4] > 0) or (
                        Data.BUF[province_offset + 7] * 256 + Data.BUF[province_offset + 6] > 0):
                    choice = random.randint(0, 100)
                    if choice < 50:
                        province_name = Helper.GetProvinceName(i + 1, without_no=True)
                        self.ShowTalk(0, province_name + Helper.GetBuiltinText(0x87F0))
                        return
                    else:
                        self.ShowTalk(0, Helper.GetBuiltinText(0x8803) + Helper.GetBuiltinText(0x880C))
                        return

            choice = random.randint(0, 7)
            text_offset = Data.DSBUF[0x8734 + 2 * choice + 0x01] * 256 + Data.DSBUF[0x8734 + 2 * choice + 0x00]
            self.ShowTalk(Helper.GetBuiltinText(text_offset))

    def Xuzijiang(self):
        choice = random.randint(0, 1)

        special_list = self.GetOfficerSpecialList(choice)
        if len(special_list) > 0:
            officer = random.randint(0, len(special_list) - 1)

            text = random.randint(0, 1)
            offset = [0x87DC, 0x87C0]

            text_offset = Data.DSBUF[offset[choice] + 1 + 2 * text] * 256 + Data.DSBUF[offset[choice] + 0 + 2 * text]
            self.ShowTalk(1, special_list[officer] + Helper.GetBuiltinText(text_offset))

            return

        num = random.randint(0, 100)
        if num < 50:
            choice = random.randint(0, 7)
            text_offset = Data.DSBUF[0x8722 + 2 * choice + 0x01] * 256 + Data.DSBUF[0x8722 + 2 * choice + 0x00]
            self.ShowTalk(1, Helper.GetBuiltinText(text_offset))
            return

        choice = random.randint(0, 1)
        special_list = self.GetOfficerSpecialList(choice + 2)

        if len(special_list) > 0:
            officer = random.randint(0, len(special_list) - 1)

            text = random.randint(0, 1)
            offset = [0x8795, 0x8788]

            self.ShowTalk(1, special_list[officer] + Helper.GetBuiltinText(offset[text]))

            return

    def GetOfficerSpecialList(self, choice):
        special_list = []

        current_ruler_province = Data.BUF[0x339B] * 256 + Data.BUF[0x339A]
        province_list = Province.GetListByRulerNo(Data.BUF[current_ruler_province + 0x10])
        for p in province_list:
            for o in p.GetOfficerList():
                if choice == 0:
                    if (Data.BUF[o.Offset + 0x02] >> 4) % 2 == 1:  # dead
                        special_list.append(o.GetName())
                elif choice == 1:
                    if ((Data.BUF[o.Offset + 0x02] & 2) == 2) or (Data.BUF[o.Offset + 0x03] >> 4) > 0:  # spy
                        special_list.append(o.GetName())
                elif choice == 2:
                    if Data.BUF[o.Offset + 0x09] >= 0x50:  # yewang
                        special_list.append(o.GetName())
                elif choice == 3:
                    if Data.BUF[o.Offset + 0x09] <= 0x50:  # yili
                        special_list.append(o.GetName())

        return special_list
