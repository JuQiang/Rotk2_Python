import pygame.display

from Helper import Helper
from Data import Data,ShowOfficerFlag
from RoTK2 import RoTK2

class Command8(object):
    def __init__(self):
        self.cmds = Helper.GetBuiltinText(0x7978,0x797D)+","+Helper.GetBuiltinText(0x7983,0x7986)+","+Helper.GetBuiltinText(0x798C,0x7991)+","+Helper.GetBuiltinText(0x7998,0x799D)+","+Helper.GetBuiltinText(0x79A3,0x79A6)+","+Helper.GetBuiltinText(0x79AC,0x79B3)
        self.commands = self.cmds.split(",")
        self.palette_no = 5

    def Start(self,province_no):
        view_other_rulers = False
        province_no_original = province_no

        while True:
            Helper.ClearInputArea()
            Helper.ShowMap(province_no)
            Helper.ShowCommandsInInputArea(self.commands,3,palette_no=self.palette_no)
            cmd = Helper.GetInput(Helper.GetBuiltinText(0x9365)+" (1-{0})?".format(len(self.commands)), row=2,required_number_min=1,required_number_max=6)

            if cmd==-1:
                if view_other_rulers is True:
                    self.commands = self.cmds.split(",")
                    self.palette_no = 5
                    province_no = province_no_original
                    view_other_rulers = False
                else:
                    break
            if cmd==1:
                Helper.ClearInputArea()
                p_no = Helper.GetInput(Helper.GetBuiltinText(0x689F)+"(1-41)? ",required_number_min=1,required_number_max=41)
                if p_no==-1:
                    continue

                is_same_ruler = Helper.Is2ProvincesAreSameRuler(province_no_original,int(p_no))
                if is_same_ruler is False:
                    who = Helper.SelectOfficer(province_no_original,Helper.GetBuiltinText(0x6896),ShowOfficerFlag.Empty)
                    if who==0:
                        continue

                view_other_rulers = True
                province_no = int(p_no)
                self.commands = self.cmds.split(",")
                self.commands.pop(4)
                self.palette_no = 3

            if cmd==2:
                while True:
                    who = Helper.SelectOfficer(province_no, Helper.GetBuiltinText(0x650A), ShowOfficerFlag.Empty,
                                               check_can_action=False)
                    print("Selected {0}".format(who))
                    if who==0:
                        break

                    officer_list = RoTK2.GetProvinceBySequence(province_no).OfficerList
                    if who>=1 and who<=len(officer_list):
                        bmp = Helper.GetOfficerDetailedInformation(officer_list[who-1])
                        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
                        pygame.display.flip()

                        Helper.ClearInputArea()
                        Helper.GetInput(Helper.GetBuiltinText(0x588A),required_number=False)

            if cmd==3 or cmd==4:
                page = 0
                while True:
                    Helper.ClearInputArea()
                    if cmd == 3:
                        bmp, have_more_pages = Helper.GetOfficersSummary(province_no, page)
                    else:
                        bmp, have_more_pages = Helper.GetOfficersSummary2(province_no, page)

                    Helper.Screen.blit(bmp, (296 * Helper.Scale, 8 * Helper.Scale))
                    if have_more_pages is False:
                        Helper.GetInput(Helper.GetBuiltinText(0x588A),required_number=False)
                        break
                    else:
                        yn = Helper.GetInput(Helper.GetBuiltinText(0x6685)+"(Y/N)?",required_number=False)
                        if yn in [-1,"n"]:
                            break
                        elif yn in ["0","y"]:
                            page += 1

            if cmd==5:
                if view_other_rulers is True:
                    self.Command8_6(province_no)
                else:
                    page = 0
                    ruler_no = RoTK2.GetProvinceBySequence(province_no).RulerNo
                    province_list = RoTK2.GetProvincesByRulerNo(ruler_no)
                    only_one_page = (len(province_list) <= 7)

                    while True:
                        Helper.ClearInputArea()
                        bmp, have_more_pages = Helper.DisplayProvinces(ruler_no, page)
                        Helper.Screen.blit(bmp, (296 * Helper.Scale, 8 * Helper.Scale))
                        pygame.display.flip()

                        if 7 * (page + 1) < len(province_list):
                            yn = Helper.GetInput(Helper.GetBuiltinText(0x6685)+"(Y/N)?",required_number=False)
                            if yn in [-1, "n"]:
                                break
                            elif yn in ["0", "y"] and only_one_page is False:
                                page += 1
                        else:
                            Helper.GetInput(Helper.GetBuiltinText(0x588A),required_number=False)
                            break

            if cmd==6:
                self.Command8_6(province_no)

    def Command8_6(self,province_no):
        bmp = Helper.ShowCommand8_Sort()
        Helper.Screen.blit(bmp, (300 * Helper.Scale, 298 * Helper.Scale))

        Helper.ClearInputArea(3)
        cmd = Helper.GetInput(Helper.GetBuiltinText(0x63EF),row=2,required_number_min=1,required_number_max=5)
        if cmd>0:
            RoTK2.ReOrderOfficers(province_no, int(cmd))
