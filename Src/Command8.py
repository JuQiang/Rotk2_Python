import pygame.display

from Helper import Helper,Province,Officer,Ruler
from Data import Data,ShowOfficerFlag


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
            cmd = Helper.GetInput(Helper.GetBuiltinText(0x9365)+" (1-{0})? ".format(len(self.commands)), row=2,required_number_min=1,required_number_max=6)

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

                is_same_ruler = Province.Is2ProvincesBelongToSameRuler(province_no_original,int(p_no))
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
                    #print("Selected {0}".format(who))
                    if who==0:
                        break

                    officer_list = Province.FromSequence(province_no).GetOfficerList()
                    if who>=1 and who<=len(officer_list):
                        bmp = self.GetOfficerDetailedInformation(officer_list[who-1])
                        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
                        pygame.display.flip()

                        Helper.ClearInputArea()
                        Helper.GetInput(Helper.GetBuiltinText(0x588A),required_number=False)

            if cmd==3 or cmd==4:
                page = 0
                while True:
                    Helper.ClearInputArea()
                    if cmd == 3:
                        bmp, have_more_pages = self.GetOfficersSummary(province_no, page)
                    else:
                        bmp, have_more_pages = self.GetOfficersSummary2(province_no, page)

                    Helper.Screen.blit(bmp, (296 * Helper.Scale, 8 * Helper.Scale))
                    if have_more_pages is False:
                        Helper.GetInput(Helper.GetBuiltinText(0x588A),required_number=False)
                        break
                    else:
                        yn = Helper.GetInput(Helper.GetBuiltinText(0x6685)+"(Y/N)? ",required_number=False)
                        if yn in [-1,"n"]:
                            break
                        elif yn in ["0","y"]:
                            page += 1

            if cmd==5:
                if view_other_rulers is True:
                    self.Command8_6(province_no)
                else:
                    page = 0
                    province = Province.FromSequence(province_no)
                    ruler_no = province.RulerNo
                    province_list = Province.GetListByRulerNo(province.RulerNo)
                    only_one_page = (len(province_list) <= 7)

                    while True:
                        Helper.ClearInputArea()
                        bmp, have_more_pages = Helper.DisplayProvinces(ruler_no, page)
                        Helper.Screen.blit(bmp, (296 * Helper.Scale, 8 * Helper.Scale))
                        pygame.display.flip()

                        if 7 * (page + 1) < len(province_list):
                            yn = Helper.GetInput(Helper.GetBuiltinText(0x6685)+"(Y/N)? ",required_number=False)
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
        bmp = self.ShowCommand8_Sort()
        Helper.Screen.blit(bmp, (300 * Helper.Scale, 295 * Helper.Scale))

        #Helper.ClearInputArea(3)
        cmd = Helper.GetInput(Helper.GetBuiltinText(0x63EF),row=2,required_number_min=1,required_number_max=5)
        if cmd>0:
            Province.ReOrderOfficers(province_no, int(cmd))

    def ShowCommand8_Sort(self):
        bmp = pygame.Surface((330, 90))
        bmp.fill((0, 0, 0))

        left = 2
        top = 2

        p_no = 5
        command8 = [Helper.GetBuiltinText(0x63B6, 0x63B9), Helper.GetBuiltinText(0x63C2, 0x63C7),
                    Helper.GetBuiltinText(0x63CE, 0x63D3), Helper.GetBuiltinText(0x63D7, 0x63DC),
                    Helper.GetBuiltinText(0x63E3, 0x63E8)]

        for i in range(0, len(command8)):
            row = int(i / 3)
            col = i % 3

            cmd_bmp = Helper.DrawText("{0}.{1}".format(i + 1, command8[i]), back_color=(0, 0, 0), palette_no=p_no)
            bmp.blit(cmd_bmp, (left + 90 * col, top + 30 * row))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    def GetOfficersSummary(self,prov_no, page):
        bmp = pygame.Surface((335, 284))
        bmp.fill((0, 0, 0))

        header = pygame.Surface((335, 40))
        header.fill((255, 255, 255))

        guanjie = Helper.DrawText(Helper.GetBuiltinText(0x651f, 0x6522), back_color=(255, 255, 255), palette_no=0)
        jiangling = Helper.DrawText(" {0}   ".format(Helper.GetBuiltinText(0x6528)), back_color=(255, 255, 255),
                                    palette_no=4)
        zhongcheng = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6532)), back_color=(255, 255, 255),
                                     palette_no=2)
        caizhi = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x653B, 0x653E)), back_color=(255, 255, 255),
                                 palette_no=6)
        zhanli = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6540)), back_color=(255, 255, 255),
                                 palette_no=6)
        haozhao = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6545)), back_color=(255, 255, 255),
                                  palette_no=6)
        shibing = Helper.DrawText(" {0}".format(Helper.GetBuiltinText(0x654E, 0x6552).replace(" ","")), back_color=(255, 255, 255),
                                  palette_no=0)

        name_list = [guanjie, jiangling, zhongcheng, caizhi, zhanli, haozhao, shibing]
        x_list = [0, 36, 99, 146, 194, 241, 292]

        index = 0
        for i in range(0, len(name_list)):
            header.blit(name_list[i], (x_list[i], 8))
            if i < len(name_list) - 1:
                pygame.draw.line(header, (0, 0, 0), (x_list[i + 1] - 1, 0), (x_list[i + 1] - 1, 40), 1)

        bmp.blit(header, (0, 0))

        body = pygame.Surface((335, bmp.get_height() - header.get_height()))
        body.fill((0, 0, 0))

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                pygame.draw.line(body, Helper.Palettes[3], (x_list[i + 1] - 1, 0),
                                 (x_list[i + 1] - 1, body.get_height()), 1)

        height = 2
        official_officer_list = Province.FromSequence(prov_no).GetOfficerList()
        unclaimed_officer_list = Province.FromSequence(prov_no).GetUnclaimedOfficerList()

        officer_list = official_officer_list + unclaimed_officer_list

        i = 0
        for officer in officer_list:
            if i < 7 * page:
                i += 1
                continue

            if officer.IsRuler():
                ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), back_color=(0, 0, 0), palette_no=2)
                body.blit(ruler_bmp, (0, height + 2))
            elif officer.IsGovernor() is True and officer.IsRuler() is False:
                officer_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(0, 0, 0), palette_no=5)
                body.blit(officer_bmp, (0, height + 2))
            elif officer.IsAdvisor():
                advisor_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640A), back_color=(0, 0, 0), palette_no=1)
                body.blit(advisor_bmp, (0, height + 2))
            else:
                if officer.IsUnClaimed is False and officer.IsFree is False:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640F), back_color=(0, 0, 0), palette_no=7)
                else:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6414), back_color=(0, 0, 0), palette_no=6)
                body.blit(is_online_bmp, (0, height + 2))

            general_name_data = officer.GetName()
            p_no = 7
            if officer.IsUnClaimed is True or officer.IsFree is True or officer.IsSick is True:
                p_no = 6
            general_name_bmp = Helper.DrawText(general_name_data, back_color=(0, 0, 0), palette_no=p_no)
            body.blit(general_name_bmp, (x_list[1] + 10, height + 2))

            if officer.IsRuler() or officer.IsUnClaimed is True:
                loyal = "---"
            else:
                loyal = str(officer.Loyalty)
            loyal_bmp = Helper.DrawText(loyal, (0, 0, 0), 7)
            body.blit(loyal_bmp, (x_list[3] - loyal_bmp.get_width() - 8, height + 2))

            zhili_bmp = Helper.DrawText(str(officer.Int), (0, 0, 0), 7)
            body.blit(zhili_bmp, (x_list[4] - zhili_bmp.get_width() - 8, height + 2))

            zhanli_bmp = Helper.DrawText(str(officer.War), (0, 0, 0), 7)
            body.blit(zhanli_bmp, (x_list[5] - zhanli_bmp.get_width() - 8, height + 2))

            haozhao_bmp = Helper.DrawText(str(officer.Chm), (0, 0, 0), 7)
            body.blit(haozhao_bmp, (x_list[6] - haozhao_bmp.get_width() - 8, height + 2))

            shibing_bmp = Helper.DrawText(str(officer.Soldiers), (0, 0, 0), 7)
            body.blit(shibing_bmp, (338 - shibing_bmp.get_width() - 5, height + 2))

            height += 34

        bmp.blit(body, (0, 40))

        have_more_pages = False
        if len(officer_list) > 7 * (page + 1):
            have_more_pages = True
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages

    def GetOfficersSummary2(self,prov_no, page):
        bmp = pygame.Surface((335, 284))
        bmp.fill((0, 0, 0))

        header = pygame.Surface((335, 40))
        header.fill((255, 255, 255))

        guanjie = Helper.DrawText(Helper.GetBuiltinText(0x651f, 0x6522), back_color=(255, 255, 255), palette_no=0)
        jiangling = Helper.DrawText(" {0}   ".format(Helper.GetBuiltinText(0x6528)), back_color=(255, 255, 255),
                                    palette_no=4)

        shiwei = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6567, 0x656A)), back_color=(255, 255, 255),
                                 palette_no=2)
        wuzhuang = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6575)), back_color=(255, 255, 255),
                                   palette_no=6)
        wuqi = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x657A)), back_color=(255, 255, 255), palette_no=6)
        xunlian = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6570)), back_color=(255, 255, 255),
                                  palette_no=6)
        shibing = Helper.DrawText(" {0}".format(Helper.GetBuiltinText(0x6583).replace(" ","")), back_color=(255, 255, 255),
                                  palette_no=0)

        name_list = [guanjie, jiangling, shiwei, xunlian, wuzhuang, wuqi, shibing]
        x_list = [0, 36, 99, 146, 194, 241, 292]

        index = 0
        for i in range(0, len(name_list)):
            header.blit(name_list[i], (x_list[i], 8))
            if i < len(name_list) - 1:
                pygame.draw.line(header, (0, 0, 0), (x_list[i + 1] - 1, 0), (x_list[i + 1] - 1, 40), 1)

        bmp.blit(header, (0, 0))

        body = pygame.Surface((335, bmp.get_height() - header.get_height()))
        body.fill((0, 0, 0))

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                pygame.draw.line(body, Helper.Palettes[3], (x_list[i + 1] - 1, 0),
                                 (x_list[i + 1] - 1, body.get_height()), 1)

        height = 2
        i = 0
        official_officer_list = Province.FromSequence(prov_no).GetOfficerList()
        unclaimed_officer_list = Province.FromSequence(prov_no).GetUnclaimedOfficerList()

        officer_list = official_officer_list + unclaimed_officer_list

        for officer in officer_list:
            if i < 7 * page:
                i += 1
                continue

            if officer.IsRuler():
                ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), back_color=(0, 0, 0), palette_no=2)
                body.blit(ruler_bmp, (0, height + 2))
            elif officer.IsGovernor() is True and officer.IsRuler() is False:
                officer_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(0, 0, 0), palette_no=5)
                body.blit(officer_bmp, (0, height + 2))
            elif officer.IsAdvisor():
                advisor_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640A), back_color=(0, 0, 0), palette_no=1)
                body.blit(advisor_bmp, (0, height + 2))
            else:
                if officer.IsUnClaimed is False and officer.IsFree is False:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640F), back_color=(0, 0, 0), palette_no=7)
                else:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6414), back_color=(0, 0, 0), palette_no=6)
                body.blit(is_online_bmp, (0, height + 2))

            general_name_data = officer.GetName()
            p_no = 7
            if officer.IsUnClaimed is True or officer.IsFree is True or officer.IsSick is True:
                p_no = 6
            general_name_bmp = Helper.DrawText(general_name_data, back_color=(0, 0, 0), palette_no=p_no)
            body.blit(general_name_bmp, (x_list[1] + 10, height + 2))

            shiwei_text = "---" if officer.IsUnClaimed else str(officer.shiwei)
            shiwei_bmp = Helper.DrawText(shiwei_text, (0, 0, 0), 7)
            body.blit(shiwei_bmp, (x_list[3] - shiwei_bmp.get_width() - 8, height + 2))

            xunlian_bmp = Helper.DrawText(str(officer.TrainingLevel), (0, 0, 0), 7)
            body.blit(xunlian_bmp, (x_list[4] - xunlian_bmp.get_width() - 8, height + 2))

            wuzhuang_bmp = Helper.DrawText(str(officer.Arms), (0, 0, 0), 7)
            body.blit(wuzhuang_bmp, (x_list[5] - wuzhuang_bmp.get_width() - 8, height + 2))

            wuqi_bmp = Helper.DrawText(str(officer.Weapons), (0, 0, 0), 7)
            body.blit(wuqi_bmp, (x_list[6] - wuqi_bmp.get_width() - 8, height + 2))

            shibing_bmp = Helper.DrawText(str(officer.Soldiers), (0, 0, 0), 7)
            body.blit(shibing_bmp, (338 - shibing_bmp.get_width() - 5, height + 2))

            height += 34
            i += 1
        bmp.blit(body, (0, 40))

        have_more_pages = False
        if len(officer_list) > 7 * (page + 1):
            have_more_pages = True
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages

    def GetOfficerDetailedInformation(self,officer):
        bmp = pygame.Surface((330, 160))
        bmp.fill((0, 0, 0))

        face_bmp = Helper.GetFace(officer.Portrait)
        bmp.blit(face_bmp, (10, 35))

        name_indexes = officer.GetName()
        name_bmp = Helper.DrawText(name_indexes, scaled=False)
        bmp.blit(name_bmp, ((10 + (face_bmp.get_width() - name_bmp.get_width()) / 2), 120))

        ruler_offset = Ruler.FromNo(officer.RulerNo).RulerSelf.Offset

        if officer.IsRuler():
            ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), palette_no=2, scaled=False)
            bmp.blit(ruler_bmp, (20, 0))

            if Data.BUF[Ruler.FromNo(officer.RulerNo).Offset + 0x21] == 0xFF:
                marriage_status = Helper.GetBuiltinText(0x6422)
            else:
                marriage_ruler = Ruler.FromNo(
                    Data.BUF[Ruler.FromNo(officer.RulerNo).Offset + 0x21]).RulerSelf
                marriage_status = marriage_ruler.GetName()

            marry_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6425).replace("%s", marriage_status), palette_no=2,
                                        scaled=False)
            bmp.blit(marry_bmp, (80, 8))
        else:
            if ruler_offset > 0:
                name_indexes = Ruler.FromNo(officer.RulerNo).RulerSelf.GetName()
                name_bmp = Helper.DrawText(name_indexes, palette_no=2, scaled=False)
                bmp.blit(name_bmp, (80, 8))
                buxia_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6448, 0x644B), scaled=False)
                bmp.blit(buxia_bmp, (80 + name_bmp.get_width(), 8))
            else:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x6439), palette_no=6, scaled=False), (80, 8))

        # 531
        wuzhuang = Helper.DrawText(Helper.GetBuiltinText(0x6575), palette_no=5, scaled=False)
        xunlian = Helper.DrawText(Helper.GetBuiltinText(0x6570), palette_no=5, scaled=False)
        shibing = Helper.DrawText(Helper.GetBuiltinText(0x6583).replace(" ",""), palette_no=5, scaled=False)
        bmp.blit(wuzhuang, (80, 40))
        bmp.blit(xunlian, (80, 75))
        bmp.blit(shibing, (80, 110))

        wuzhuang = Helper.DrawText(str(officer.Arms))
        xunlian = Helper.DrawText(str(officer.TrainingLevel))
        shibing = Helper.DrawText(str(officer.Soldiers))

        bmp.blit(wuzhuang, (160 - wuzhuang.get_width(), 40))
        bmp.blit(xunlian, (160 - xunlian.get_width(), 75))
        bmp.blit(shibing, (160 - shibing.get_width(), 110))

        juewei = Helper.DrawText(Helper.GetBuiltinText(0x648F, 0x6492), palette_no=3)
        shiweiwei = Helper.DrawText(Helper.GetBuiltinText(0x6494, 0x6497), palette_no=3)
        nianling = Helper.DrawText(Helper.GetBuiltinText(0x6499, 0x649C), palette_no=3)
        bmp.blit(juewei, (170, 40))
        bmp.blit(shiweiwei, (170, 75))
        bmp.blit(nianling, (170, 110))

        na = Helper.DrawText("---")
        if officer.IsRuler() or officer.IsUnClaimed or officer.IsFree:
            bmp.blit(na, (210, 40))
            bmp.blit(na, (210, 75))
        else:
            if officer.IsUnClaimed:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x6439)), (210, 40))
                bmp.blit(na, (210, 75))
            else:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x640F)), (210, 40))
                shiwei = Helper.DrawText(str(officer.shiwei))
                bmp.blit(shiwei, (210 + na.get_width() - shiwei.get_width(), 75))

        age = Helper.DrawText(str(officer.Age), scaled=False)
        bmp.blit(age, (210 + na.get_width() - age.get_width(), 110))

        zhongcheng = Helper.DrawText(Helper.GetBuiltinText(0x6532), palette_no=1)
        caizhi = Helper.DrawText(Helper.GetBuiltinText(0x653B), palette_no=1)
        zhanli = Helper.DrawText(Helper.GetBuiltinText(0x6540), palette_no=1)
        haozhao = Helper.DrawText(Helper.GetBuiltinText(0x6545), palette_no=1)
        bmp.blit(zhongcheng, (250, 5))
        bmp.blit(caizhi, (250, 40))
        bmp.blit(zhanli, (250, 75))
        bmp.blit(haozhao, (250, 110))

        if officer.IsRuler() or officer.IsUnClaimed or officer.IsFree:
            bmp.blit(na, (290, 5))
        else:
            zhongcheng = Helper.DrawText(str(officer.Loyalty))
            bmp.blit(zhongcheng, (320 - zhongcheng.get_width(), 5))
        caizhi = Helper.DrawText(str(officer.Int))
        bmp.blit(caizhi, (320 - caizhi.get_width(), 40))
        zhanli = Helper.DrawText(str(officer.War))
        bmp.blit(zhanli, (320 - zhanli.get_width(), 75))
        haozhao = Helper.DrawText(str(officer.Chm))
        bmp.blit(haozhao, (320 - haozhao.get_width(), 110))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))