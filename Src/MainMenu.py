import os.path

from Data import Data
import pygame,sys
from Helper import Helper
from RoTK2 import RoTK2
from Src.UI.Draw import Draw

class MainMenu(object):
    def __init__(self):
        self.mm = None
        self.scenario_name = [Helper.GetBuiltinText(0x4f9e), Helper.GetBuiltinText(0x4fac), Helper.GetBuiltinText(0x4fba), Helper.GetBuiltinText(0x4fc8), Helper.GetBuiltinText(0x4fd6), Helper.GetBuiltinText(0x4fe4)]

        self.scenario_no = 0
        self.player_list=[]
        self.level = 0
        self.seewar = 0
        self.history = 0

        self.v_343c = 0
        self.v_343b = 0
        self.v_3434 = 0
        self.v_3432 = 0
        self.v_3436 = 0
        self.v_343a = 0
        self.v_3448 = 0
        self.v_33b5 = 0
        self.v_33f4 = 0
        self.v_33f2 = 0

    def printf(self,format_and_data:[]):
        i = 0
        while True:
            if i>=len(format_and_data):
                break

            b = format_and_data[i]
            if b==0:
                break

            self.printf_internal(b)
            i += 1
            b = format_and_data[i]
            if b==0:
                break

    def printf_internal(self,b):
        if self.v_343c==0:
            ax = 0xffff
        else:
            ax = self.v_343c - 1

        if ax>6:
            if self.v_343b==0:
                if b<0x81:
                    if b==0x1b:
                        self.v_343c = 1
                        return b
                    elif b<0x20:#6cc
                        self.func_5d8()
                        return
                    else:
                        if b<0x200:
                            ax = 0x4f
                        else:
                            ax = 0x4e
                        if ax<self.v_3432:
                            self.func_5c0()
                        ax = self.v_343a
                        ax |= ax
                        if ax!=0:
                            ax = self.v_3448

                        ax = int(ax/256)*256+self.v_3439
                        ret = self.func_4d6(ax,self.v_3434,self.v_3432)
                        if ret>0x200:
                            ax = 2
                        else:
                            ax = 1

                        self.v_3432 += ax
                        return


        else:
            ax *= 2
            #cs:[bx+0x67a] -> 73a, 7be, 7da, 7ea, 7fa, 808, 812
            if ax==0:
                self.func_73a(b)
            elif ax==2:
                self.func_67c(b)
            elif ax==4:
                self.func_7da(b)
                self.v_343c = 0
                return
            elif ax==8:
                self.func_7fa(b)

    def func_5d8(self,ax):
        ax -=7
        if ax==0:#5f6
            ax = 6
            self.func_1145_c(ax)
            return
        ax -=1
        if ax==0:#606
            if self.v_3432<1:
                self.v_3432 -= 1
            return
        ax -=2
        if ax==0:#616
            self.func_5c0()
            return

        ax -=3
        if ax==0:#61e
            self.v_3432 = self.v_3436
            return

        return

    def func_7fa(self,b):
        b -= 0x20
        self.v_3436 = b
        self.v_343c = 0

    def func_7da(self,b):
        b -= 0x20
        self.set_v_3434_status_and_v3432(b)

    def set_v_3434_status_and_v3432(self,b):
        self.v_3432 = b
        self.set_v_3434_status(b)

    def func_fbd_a4(self,ax):
        ax = ax*self.v_33b5*2
        self.func_fbd_8a(ax)
    def func_fbd_8a(self,ax):
        ax *=6
        self.func_fbd_6c(ax)

    def func_fbd_6c(self,ax):
        #sleep for some clock ticks
        return
        ax /= 2
        ax += 1
        self.func_76c_297d(ax)
        while ax==0:
            ax = self.func_76c_2993()

    def func_76c_297d(self,ax):
        self.v_33f4 = clock_count # ah=0, int 1a
        self.v_33f2 = ax+self.v_33f4

    def func_76c_2993(self):
        dx = clock_count
        ax = self.v_33f4
        bx = self.v_33f2
        if ax>bx:#29ac
            if dx>ax:
                if dx>bx:
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            if dx>bx:
                if dx>=ax:
                    return 1
                else:
                    return 0
            else:
                return 0

    def func_73a(self, b):
        al = b
        if b==0x57:#7b0
            ax = 1
            self.func_fbd_a4(ax)
        elif b<0x57:
            if b==0x4c:#78c
                self.v_3448 = 0
                self.v_343c = 0
                return
            elif b>0x4c:#75e
                b -= 0x4d
                if b==0: #796
                    self.v_343c = 6
                    return
                b -= 5
                if b==0:
                    self.v_343c = 5
                    return
                else:#766
                    al -= 1
                    if al==0:
                        self.v_343c = 4
                        return
                    else:
                        return
            else:
                b -= 0x3d
                if b==0:
                    self.v_343c = 2
                    return

    def func_67c(self,b):
        b -= 0x20
        b *= 8
        self.set_v_3434_status_by_byte(b)

    def set_v_3434_status_by_byte(self,b):
        self.v_3434 = b
        self.set_v_3434_status(b)
        self.v_343c = 3
        return

    def set_v_3434_status(self,b):
        if self.v_3432>=0:
            ax = self.v_3432
            if ax>0x4f:
                ax = 0x4f
        else:
            ax = 0

        self.v_3432 = ax

        if self.v_3434<0:
            self.v_3434 = 0 #3fe
        else:
            ax = self.v_3434
            if ax<=0xc0:
                self.v_3434 = ax
            else:
                self.v_3434 = 0xc0

    def show(self):
        if self.mm is None:
            self.mm = Helper.GetGraphData("MainMenu")
        Helper.Screen.blit(self.mm, (0, 0))

        main_cmds = Helper.GetBuiltinText(0x531D).split("__")
        m = Helper.DrawText(main_cmds[0],scaled=True)
        Helper.Screen.blit(m, (250 * Helper.Scale, 100 * Helper.Scale))
        m = Helper.DrawText(main_cmds[1],scaled=True)
        Helper.Screen.blit(m, (250 * Helper.Scale, 150 * Helper.Scale))
        m = Helper.DrawText(main_cmds[2],scaled=True)
        Helper.Screen.blit(m, (250 * Helper.Scale, 200 * Helper.Scale))

        pygame.display.flip()

        self.draw = Draw(Helper.Scale)

    def Start(self):
        #self.printf([0x1b,0x3d,0x25,0x41,0x1b,0x52,0x41,0x31,0x2e,0x9d,0xf5,0x9d,0x45,0xa2,0xba,0xa4,0x41,0xaa,0x82,0x0a,0x0a,0x32,0x2e,0xa3,0xd1,0x92,0xaa,0xa7,0x46,0xa8,0xe2,0x0a,0x0a,0x33,0x2e,0xa1,0x4e,0x95,0xd5,0x00])
        Helper.Screen.fill((0, 0, 0))
        pygame.display.flip()

        while True:
            self.show()

            cmd = Helper.GetInput(Helper.GetBuiltinText(0x5342)+"(1-3)? ", 250, 250, width=200, required_number_min=1, required_number_max=3,
                                  allow_enter_exit=False)
            if cmd==1:
                ret = self.NewGame()
            elif cmd==2:
                ret = self.LoadGame()
            elif cmd==3:
                ret = self.EndGame()

            if ret == "OK":
                break

        if cmd==3:
            return -1
        else:
            return 0
    def EndGame(self):
        yn = Helper.GetInput(Helper.GetBuiltinText(0x534d)+"(Y/N)? ",x=250,y=300,width=200,yesno=True)
        if yn=="y":
            return "OK"

    def SelectScenario(self):
        Helper.Screen.blit(self.mm, (0, 0))
        pygame.draw.rect(Helper.Screen, (0, 0, 0),(250 * Helper.Scale, 50 * Helper.Scale, 230 * Helper.Scale, 300 * Helper.Scale))
        pygame.display.flip()

        buf_len = 0x33AF

        for i in range(0,6):
            img = Helper.DrawText("{0}. {1}".format(i+1,self.scenario_name[i]),scaled=True)
            Helper.Screen.blit(img,(250*Helper.Scale,(100+30*i)*Helper.Scale))

            year = Data.SCENARIO[buf_len*i+3]*256+Data.SCENARIO[buf_len*i+2] + 1
            img = Helper.DrawText("{0}{1}".format(year,Helper.GetBuiltinText(0x3DD2,0x3DD3)), scaled=True,palette_no=1)
            Helper.Screen.blit(img, (380 * Helper.Scale, (100 + 30 * i) * Helper.Scale))

        no = Helper.GetInput(Helper.GetBuiltinText(0x52FC) + "(1-6)? ", x=285, width=200, required_number_min=1, required_number_max=6, allow_enter_exit=True)
        if no==-1:
            return -1

        self.scenario_no = no - 1
        total_bytes = 0x33f0 - 0x42 # debug.exe 1411:68 call 76c:25e
        Data.BUF[0x42:0x42+total_bytes] = Data.SCENARIO[self.scenario_no * 0x33AF:self.scenario_no * 0x33AF + total_bytes]
        #rulers number in six generations: 0c 0c 09 0b 05 05
        #stored in dsbuf:4ce8 offset
        #dsbuf:4cee, current scenerio number(from 0)
        #dsbuf:4cef, number of players
        #dsbuf:4cf2, players sequence. player "1" stored in 4cf2, 2 in 4cf3, etc.

    def ShowScenario(self, bmp):
        img = Helper.DrawText(Helper.GetBuiltinText(0x51E4,0x51EF),palette_no=3)
        bmp.blit(img,(5,10))
        img = Helper.DrawText("{0}.{1}".format(self.scenario_no+1, self.scenario_name[self.scenario_no]))
        bmp.blit(img, (100, 10))

    def ShowPlayers(self,bmp):
        img = Helper.DrawText(Helper.GetBuiltinText(0x51FE),palette_no=3)
        bmp.blit(img,(5,40))

        for i in range(len(self.player_list)):
            row_offset = 40+30*int(i/3)
            img = Helper.DrawText(RoTK2.GetOfficerName(self.player_list[i].RulerSelf.Offset))
            bmp.blit(img,(100 + 70 * (i % 3),row_offset))

    def SelectPlayers(self, bmp):
        RoTK2.Init()

        limit = [0x0c, 0x0c, 0x09, 0x0b, 0x05, 0x05]
        ruler_list = RoTK2.GetRulerList()

        img = Helper.DrawText(Helper.GetBuiltinText(0x5559),scaled=True,palette_no=0,back_color=(255,255,255))
        Helper.Screen.blit(img, (32*Helper.Scale, 10*Helper.Scale))

        max_rulers = min(limit[self.scenario_no], len(ruler_list) + 1)
        num = Helper.GetInput(Helper.GetBuiltinText(0x5290)+ "(0-{0})? ".format(max_rulers),required_number_min=0,required_number_max=max_rulers,allow_enter_exit=False)

        player_list = []
        for i in range(0,num):
            page = 0
            while True:
                Helper.ClearInputArea()
                img = self.draw.NewGameSelectRuler(self.scenario_no, page, player_list)
                Helper.Screen.blit(img,(295*Helper.Scale,5*Helper.Scale))
                if limit[self.scenario_no]>6:
                    ruler_no = Helper.GetInput("{2}{0},{3}(0-{1})? ".format(i+1,max_rulers,Helper.GetBuiltinText(0x5299,0x529E),Helper.GetBuiltinText(0x52A3,0x52A8)),next_prompt=Helper.GetBuiltinText(0x52B3),required_number_min=0,required_number_max=max_rulers,allow_enter_exit=False)
                else:
                    ruler_no = Helper.GetInput("{2}{0},{3}(1-{1})? ".format(i + 1, max_rulers,Helper.GetBuiltinText(0x5299,0x529E),Helper.GetBuiltinText(0x52A3,0x52A8)),required_number_min=1,required_number_max=max_rulers,allow_enter_exit=False)

                if ruler_no==0:
                    page = 1 if page==0 else 0
                    continue
                elif ruler_no-1 in player_list:
                    continue
                else:
                    break

            player_list.append(ruler_no-1)

            if limit[self.scenario_no]==ruler_no:
                Data.BUF[0x3360+0x0F] = len(player_list)
            else:
                Data.BUF[0x3360 + ruler_no - 1] = len(player_list)
            img = self.draw.NewGameSelectRuler(self.scenario_no, page, player_list)
            Helper.Screen.blit(img, (295 * Helper.Scale, 5 * Helper.Scale))

            print(ruler_no)


        if limit[self.scenario_no]-1 in player_list:
            self.NewRuler()
            Data.BUF[0x47] = max_rulers

        RoTK2.GetRulersOrder()
        ruler_list = RoTK2.GetRulerList()


        self.ShowScenario(bmp)
        self.player_list = []
        for i in range(0,len(player_list)):
            rno = player_list[i]
            if limit[self.scenario_no] == rno+1:
                rno = 0x0f
            self.player_list.append(ruler_list[rno])

        self.ShowPlayers(bmp)
        bmp2 = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))
        Helper.Screen.blit(bmp2, (295 * Helper.Scale, 5 * Helper.Scale))

    def ShowLevel(self,bmp):
        row_offset = 40 + 30 * int((len(self.player_list)-1) / 3) + 30
        level_mappings = {1: Helper.GetBuiltinText(0x5530), 2: Helper.GetBuiltinText(0x5535), 3: Helper.GetBuiltinText(0x553A)}
        img = Helper.DrawText("3."+Helper.GetBuiltinText(0x5597,0x55A1), palette_no=3)
        bmp.blit(img, (5, row_offset))
        img = Helper.DrawText(level_mappings[self.level])
        bmp.blit(img, (100, row_offset))

    def SelectLevel(self,bmp):

        Helper.ClearInputArea()

        self.level = Helper.GetInput("1."+Helper.GetBuiltinText(0x5530)+" 2."+Helper.GetBuiltinText(0x5535)+" 3."+Helper.GetBuiltinText(0x553A),next_prompt=Helper.GetBuiltinText(0x55C0)+"(1-3)? ",cursor_user_prompt_location=True, required_number_min=1,required_number_max=3,allow_enter_exit=False,palette_no=3)
        self.ShowLevel(bmp)
        bmp2 = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))
        Helper.Screen.blit(bmp2, (295 * Helper.Scale, 5 * Helper.Scale))

    def ShowWar(self,bmp):
        row_offset = 40 + 30 * int((len(self.player_list)-1) / 3) + 30 * 2

        img = Helper.DrawText("4."+Helper.GetBuiltinText(0x55D7,0x55E1), palette_no=3)
        bmp.blit(img,(5,row_offset))

        if self.seewar==1:
            img = Helper.DrawText(Helper.GetBuiltinText(0x5526))
        else:
            img = Helper.DrawText(Helper.GetBuiltinText(0x552B))
        bmp.blit(img, (100, row_offset))

    def SeeWar(self,bmp):
        Helper.ClearInputArea()
        see_war = Helper.GetInput(Helper.GetBuiltinText(0x55E8)+"(Y/N)? ",allow_enter_exit=False,keydown_mode=True)#嚒
        self.seewar = 1 if see_war == "y" else 0

        self.ShowWar(bmp)
        bmp2 = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))
        Helper.Screen.blit(bmp2, (295 * Helper.Scale, 5 * Helper.Scale))


    def ShowHistory(self,bmp):
        row_offset = 40 + 30 * int((len(self.player_list)-1) / 3) + 30*3
        history_mappings = {1: Helper.GetBuiltinText(0x553F), 2: Helper.GetBuiltinText(0x5548)}

        img = Helper.DrawText(Helper.GetBuiltinText(0x55F9,0x5604), palette_no=3)
        bmp.blit(img, (5, row_offset))
        img = Helper.DrawText(history_mappings[self.history])
        bmp.blit(img, (100, row_offset))

    def SelectHistory(self,bmp):
        Helper.ClearInputArea()

        self.history = Helper.GetInput("1."+Helper.GetBuiltinText(0x553F)+" 2."+Helper.GetBuiltinText(0x5548),next_prompt=Helper.GetBuiltinText(0x561F)+"(1-2)? ",cursor_user_prompt_location=True, required_number_min=1,required_number_max=2,allow_enter_exit=False,palette_no=3)
        self.ShowHistory(bmp)

        bmp2 = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))
        Helper.Screen.blit(bmp2, (295 * Helper.Scale, 5 * Helper.Scale))

    def ShowOptions(self):
        bmp = pygame.Surface((336, 280))
        bmp.fill((0, 0, 0))

        self.ShowScenario(bmp)
        self.ShowPlayers(bmp)
        self.ShowLevel(bmp)
        self.ShowWar(bmp)
        self.ShowHistory(bmp)

        bmp2 = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))
        Helper.Screen.blit(bmp2, (295 * Helper.Scale, 5 * Helper.Scale))

    def NewGame(self):
        self.SelectScenario()
        if self.scenario_no<0:
            return -1

        map = Helper.GetMap()
        Helper.Screen.blit(map,(0,0))

        bmp = pygame.Surface((336, 280))
        bmp.fill((0, 0, 0))

        self.SelectPlayers(bmp)
        self.SelectLevel(bmp)
        self.SeeWar(bmp)
        self.SelectHistory(bmp)

        while True:
            Helper.ClearInputArea()
            yn = Helper.GetInput(Helper.GetBuiltinText(0x558C)+Helper.GetBuiltinText(0x3D7D)+"(Y/N)? ",yesno=True)
            if yn in ["","n"]:
                cmd = Helper.GetInput(Helper.GetBuiltinText(0x558C)+"(0-5)? ",required_number_min=0,required_number_max=5)
                if cmd<1:
                    return -1
                if cmd==1:
                    self.SelectScenario()
                    if self.scenario_no < 0:
                        return -1
                    self.SelectPlayers(bmp)
                if cmd==2:
                    self.SelectPlayers(bmp)
                if cmd==3:
                    self.SelectLevel(bmp)
                if cmd==4:
                    self.SeeWar(bmp)
                if cmd==5:
                    self.SelectHistory(bmp)
                self.ShowOptions()
            else:
                break

        year = Data.BUF[0x45]*256+Data.BUF[0x44]
        Data.BUF[0x44] = (year+1)%256 # new year
        Data.BUF[0x45] = int((year + 1) / 256)  # new year
        Data.BUF[0x46] = 0  # 1st month of new year

        for i in range(0,16):
            if Data.BUF[0x3360+i]==1:
                break

        off = Data.RULER_OFFSET+i*Data.RULER_SIZE

        Data.BUF[0x335A + Data.OFFSET] = 0  # start from 0
        Data.BUF[0x335C + Data.OFFSET] = off%256
        Data.BUF[0x335D + Data.OFFSET] = int(off / 256)

        off2 = Data.BUF[off+1]*256+Data.BUF[off]
        Data.BUF[0x335E + Data.OFFSET] = off2%256
        Data.BUF[0x335F + Data.OFFSET] = int(off2 / 256)

        off3 = Data.BUF[off + 3] * 256 + Data.BUF[off+2]
        Data.BUF[0x3362 + Data.OFFSET] = off3%256
        Data.BUF[0x3363 + Data.OFFSET] = int(off3/256)

        Data.BUF[0x337b+Data.OFFSET] = self.level
        option = 0x0
        option |= self.seewar
        if self.history==1:
            option |= 0x80

        Data.BUF[0x337C + Data.OFFSET] = option
        Data.BUF[0x337D+Data.OFFSET] = 5
        Data.BUF[0x337E + Data.OFFSET] = 4

        RoTK2.Init()
        Helper.MainMap = Helper.GetMap()

        return "OK"

    def NewRuler_GetName(self):
        Helper.ClearInputArea()
        eng_chn = Helper.GetInput(Helper.GetBuiltinText(0x57BE,0x57BF)+Helper.GetBuiltinText(0x57B9)+Helper.GetBuiltinText(0x57C2),next_prompt=Helper.GetBuiltinText(0x57C6)+Helper.GetBuiltinText(0x57DC)+"    "+"(1-2)? ",cursor_user_prompt_location=True,required_number_min=1,required_number_max=2,allow_enter_exit=False)
        if eng_chn==1:
            while True:
                Helper.ClearInputArea()
                img = Helper.DrawText("------", scaled=True, palette_no=7)
                Helper.Screen.blit(img, (350 * Helper.Scale, 360 * Helper.Scale))

                img = Helper.DrawText(Helper.GetBuiltinText(0x57BE,0x57BF)+Helper.GetBuiltinText(0x57B9)+Helper.GetBuiltinText(0x57C2), scaled=True, palette_no=7)
                Helper.Screen.blit(img, (300 * Helper.Scale, 298 * Helper.Scale))

                Helper.ClearInputArea(1)
                name = Helper.GetInput("",350, 345,width=200,palette_no=1,required_number=False,max_chars=6)
                yn = Helper.GetInput(Helper.GetBuiltinText(0x57F9)+Helper.GetBuiltinText(0x3D7D)+"(Y/N)? ",keydown_mode=True)
                if yn in ["","n"]:
                    continue

                pygame.draw.rect(Helper.Screen,(0,0,0),(400*Helper.Scale,40*Helper.Scale,100*Helper.Scale,30*Helper.Scale))
                img = Helper.DrawText(name,scaled=True)
                Helper.Screen.blit(img,(400*Helper.Scale,40*Helper.Scale))
                break

            for i in range(0, len(name)):
                Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x1C + i] = ord(name[i])

    def NewRuler_GetBirthday(self):
        Helper.ClearInputArea()
        birth_month = Helper.GetInput(Helper.GetBuiltinText(0x5387)+"(1-12)? ", required_number_min=1,
                                      required_number_max=12, allow_enter_exit=False)
        birth_day = Helper.GetInput(Helper.GetBuiltinText(0x53B0)+"(1-31)? ", required_number_min=1,
                                    required_number_max=31, allow_enter_exit=False)
        Helper.ClearInputArea()
        age = Helper.GetInput(Helper.GetBuiltinText(0x53BD)+"(1-99)? ", required_number_min=1, required_number_max=99,
                              allow_enter_exit=False)
        img = Helper.DrawText("{0}{3} {1}{4}    {2}{5}".format(birth_month, birth_day, age,Helper.GetBuiltinText(0x5849),Helper.GetBuiltinText(0x584E),Helper.GetBuiltinText(0x5854)), scaled=True)
        Helper.Screen.blit(img, (400 * Helper.Scale, 75 * Helper.Scale))

        Data.BUF[Data.RULER_AS_OFFICER_OFFSET+0x19] = Data.BUF[0x45] * 256 + Data.BUF[0x44] + 2 - age
        return age

    def NewRuler_GetSex(self,age):
        Helper.ClearInputArea()
        sex = Helper.GetInput("1."+Helper.GetBuiltinText(0x536E)+" 2."+Helper.GetBuiltinText(0x5373), next_prompt=Helper.GetBuiltinText(0x53DB)+"(1-2)? ",
                              cursor_user_prompt_location=True, palette_no=3, required_number_min=1,
                              required_number_max=2, allow_enter_exit=False)
        img = Helper.DrawText([Helper.GetBuiltinText(0x536E), Helper.GetBuiltinText(0x53DB)][sex - 1], scaled=True)
        Helper.Screen.blit(img, (400 * Helper.Scale, 110 * Helper.Scale))

        if age < 21:
            age_index = 0
        elif age < 41:
            age_index = 1
        else:
            age_index = 2

        return sex, age_index

    def NewRuler_GetAbility(self,sex,age_index):
        # dsbuf 4fa2~ 4fb4:
        # 3c 50 32, 3c 37 4b
        # 41 4b 37, 41 32 50
        # 46 3c 46 46 2d 55
        values = [
            [[0x3c, 0x50, 0x32], [0x3c, 0x37, 0x4b]],
            [[0x41, 0x4b, 0x37], [0x41, 0x32, 0x50]],
            [[0x46, 0x3c, 0x46], [0x46, 0x2d, 0x55]]]
        values = values[age_index][sex - 1]
        values_original = values.copy()

        index = 0
        award = 50

        self.show_values(index, values, award)
        determin = Helper.GetBuiltinText(0x53FB,0x5407)
        while True:
            Helper.ClearInputArea()

            cmd = Helper.GetInput(determin, next_prompt=Helper.GetBuiltinText(0x5409),
                                  cursor_user_prompt_location=True, required_number=False, allow_enter_exit=False,
                                  keydown_mode=True)
            if cmd == "4":
                index = index - 1
                if index < 0:
                    index = 2
                self.show_values(index, values, award)
                continue
            if cmd == "6":
                index = index + 1
                if index > 2:
                    index = 0
                self.show_values(index, values, award)
                continue

            if cmd == "2":
                if values[index] > values_original[index]:
                    values[index] -= 1
                    award += 1
            if cmd == "8":
                if values[index] < 100 and award > 0:
                    values[index] += 1
                    award -= 1
            self.show_values(index, values, award)

            if award == 0:
                Helper.ClearInputArea()
                yn = Helper.GetInput(Helper.GetBuiltinText(0x5464)+Helper.GetBuiltinText(0x3D7D)+"(Y/N)? ", yesno=True, keydown_mode=True)  # 麽麼
                if yn == "y":
                    break
                determin = Helper.GetBuiltinText(0x5469,0x5471)

        self.show_values(-1, values, 0)
        inte = values[0]
        war = values[1]
        chm = values[2]

        if inte > war:
            head_pic = 0xc0 + 2 * age_index + sex
        else:
            head_pic = 0xc6 + 2 * age_index + sex

        face = Helper.GetFace(head_pic - 2)
        face = pygame.transform.scale(face, (face.get_width() * Helper.Scale, face.get_height() * Helper.Scale))
        Helper.Screen.blit(face, (550 * Helper.Scale, 35 * Helper.Scale))

        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x04] = inte
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x05] = war
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x06] = chm

        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x0A] = 0x0F

        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x12] = 0x10
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x13] = 0x27
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x14] = 0x88
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x15] = 0x13
        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x16] = 0x32

        Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x1A] = head_pic - 1

    def NewRuler_GetRuledProvince(self):
        while True:
            Helper.ClearInputArea()
            pno = Helper.GetInput(Helper.GetBuiltinText(0x54A8)+"(1-41)? ", required_number_min=1, required_number_max=41,
                                  allow_enter_exit=False)
            rno = RoTK2.GetProvinceBySequence(pno).RulerNo
            if rno == 255:
                break

        img = Helper.DrawText(str(pno), scaled=True)
        Helper.Screen.blit(img, (400 * Helper.Scale, 215 * Helper.Scale))

        return pno

    def NewRuler_AddFollower(self):
        name = ""
        yn = Helper.GetInput(Helper.GetBuiltinText(0x548F)+"(Y/N)? ", yesno=True, keydown_mode=True)
        if yn == "y":
            Helper.ClearInputArea()
            eng_chn = Helper.GetInput(Helper.GetBuiltinText(0x57BE,0x57BF)+Helper.GetBuiltinText(0x57B4)+Helper.GetBuiltinText(0x57C2),
                                      next_prompt=Helper.GetBuiltinText(0x57C6) + Helper.GetBuiltinText(0x57DC) + "    " + "(1-2)? ",
                                      cursor_user_prompt_location=True, required_number_min=1,
                                      required_number_max=2, allow_enter_exit=False)
            if eng_chn == 1:
                while True:
                    Helper.ClearInputArea()
                    img = Helper.DrawText("------", scaled=True, palette_no=7)
                    Helper.Screen.blit(img, (350 * Helper.Scale, 350 * Helper.Scale))

                    img = Helper.DrawText(Helper.GetBuiltinText(0x57BE,0x57BF)+Helper.GetBuiltinText(0x57B4)+Helper.GetBuiltinText(0x57C2), scaled=True, palette_no=7)
                    Helper.Screen.blit(img, (300 * Helper.Scale, 298 * Helper.Scale))

                    name = Helper.GetInput("", 350, 335, width=200, palette_no=1, required_number=False, max_chars=6)
                    yn = Helper.GetInput(Helper.GetBuiltinText(0x57F9)+Helper.GetBuiltinText(0x3D7D)+"(Y/N)? ",keydown_mode=True)
                    if yn == "":
                        continue
                    else:
                        break
                img = Helper.DrawText(name, scaled=True)
                Helper.Screen.blit(img, (400 * Helper.Scale, 250 * Helper.Scale))

                Helper.ClearInputArea()
                age = Helper.GetInput(Helper.GetBuiltinText(0x53BD) + "(1-99)? ", required_number_min=1,
                                      required_number_max=99,
                                      allow_enter_exit=False)
                img = Helper.DrawText("{0}{1}".format(age,Helper.GetBuiltinText(0x5854)), scaled=True)
                Helper.Screen.blit(img, (450 * Helper.Scale, 250 * Helper.Scale))

                Helper.ClearInputArea()
                sex = Helper.GetInput("1." + Helper.GetBuiltinText(0x536E) + " 2." + Helper.GetBuiltinText(0x5373),
                                      next_prompt=Helper.GetBuiltinText(0x53DB) + "(1-2)? ",
                                      cursor_user_prompt_location=True, palette_no=3, required_number_min=1,
                                      required_number_max=2, allow_enter_exit=False)
                img = Helper.DrawText([Helper.GetBuiltinText(0x536E), Helper.GetBuiltinText(0x53DB)][sex - 1],
                                      scaled=True)

                Helper.Screen.blit(img, (500 * Helper.Scale, 250 * Helper.Scale))
        else:
            img = Helper.DrawText(Helper.GetBuiltinText(0x54A4), scaled=True)
            Helper.Screen.blit(img, (400 * Helper.Scale, 250 * Helper.Scale))
            return None

        follower_offset = 0x2A9F + Data.OFFSET
        Data.BUF[follower_offset+0x00:follower_offset+0x00+0x2B] = [0]*0x2B
        Data.BUF[follower_offset+0x04] = 50
        Data.BUF[follower_offset + 0x05] = 60
        Data.BUF[follower_offset + 0x06] = 70
        Data.BUF[follower_offset + 0x0A] = 0x0F
        Data.BUF[follower_offset + 0x0B] = 100
        Data.BUF[follower_offset + 0x12] = 0xe8
        Data.BUF[follower_offset + 0x13] = 0x03
        Data.BUF[follower_offset + 0x14] = 0xe8
        Data.BUF[follower_offset + 0x15] = 0x03
        Data.BUF[follower_offset + 0x16] = 0x64
        Data.BUF[follower_offset + 0x19] = Data.BUF[0x45] * 256 + Data.BUF[0x44] + 2  - age
        Data.BUF[follower_offset + 0x1A] = 0xcC
        Data.BUF[follower_offset + 0x1B] = 0x00
        for i in range(0,len(name)):
            Data.BUF[follower_offset+0x1C+i] = ord(name[i])

        follower = RoTK2.GetOfficerFromBuffer(Data.BUF[follower_offset:follower_offset+0x2b].copy(),253,Data.BUF[0x45] * 256 + Data.BUF[0x44] + 1)

        return follower



    def NewRuler(self):
        bmp = pygame.Surface((336, 280))
        bmp.fill((0, 0, 0))

        img = Helper.DrawText("<"+Helper.GetBuiltinText(0x5114)+">",palette_no=1)
        bmp.blit(img,((bmp.get_width()-img.get_width())/2,5))
        info1 = Helper.GetBuiltinText(0x54EB).split("_")
        info2 = Helper.GetBuiltinText(0x550F,0x551F).split("_")
        img = Helper.DrawText(info1[0],palette_no=3)
        bmp.blit(img, (5, 35))
        img = Helper.DrawText(info1[1],palette_no=3)
        bmp.blit(img, (5, 70))
        img = Helper.DrawText(info1[2],palette_no=3)
        bmp.blit(img, (5, 105))
        img = Helper.DrawText(info1[3],palette_no=3)
        bmp.blit(img, (5, 140))
        img = Helper.DrawText(info2[0],palette_no=3)
        bmp.blit(img, (5, 210))
        img = Helper.DrawText(info2[1],palette_no=3)
        bmp.blit(img, (5, 245))

        bmp = pygame.transform.scale(bmp,(bmp.get_width()*Helper.Scale,bmp.get_height()*Helper.Scale))
        Helper.Screen.blit(bmp,(295*Helper.Scale,5*Helper.Scale))

        self.NewRuler_GetName()
        age = self.NewRuler_GetBirthday()
        sex,age_index = self.NewRuler_GetSex(age)
        self.NewRuler_GetAbility(sex,age_index)
        pno = self.NewRuler_GetRuledProvince()
        follower = self.NewRuler_AddFollower()

        while True:
            Helper.ClearInputArea()
            yn = Helper.GetInput(Helper.GetBuiltinText(0x54B3)+"(Y/N)? ", keydown_mode=True)
            if yn in ["","n"]:
                change_no = Helper.GetInput(Helper.GetBuiltinText(0x54BE)+"(1-6)? ",required_number_min=1,required_number_max=6,allow_enter_exit=True)
                if change_no==1:
                    self.NewRuler_GetName()
                elif change_no==2:
                    age = self.NewRuler_GetBirthday()
                    sex, age_index = self.NewRuler_GetSex(age)
                    self.NewRuler_GetAbility(sex, age_index)
                elif change_no==3:
                    sex, age_index = self.NewRuler_GetSex(age)
                    self.NewRuler_GetAbility(sex, age_index)
                elif change_no==4:
                    self.NewRuler_GetAbility(sex, age_index)
                elif change_no==5:
                    pno = self.NewRuler_GetRuledProvince()
                elif change_no==6:
                    follower = self.NewRuler_AddFollower()
            elif yn=="y":
                break
        # create a new ruler

        if follower is not None:
            Data.BUF[follower.Offset+0x0a] = 0x0F
            Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x00] = follower.Offset%256
            Data.BUF[Data.RULER_AS_OFFICER_OFFSET + 0x01] = int(follower.Offset / 256)

        province_offset = Data.PROVINCE_OFFSET+Data.PROVINCE_SIZE*(pno-1)
        Data.BUF[province_offset + 0x02 ] = Data.RULER_AS_OFFICER_OFFSET % 256
        Data.BUF[province_offset + 0x03 ] = int(Data.RULER_AS_OFFICER_OFFSET / 256)
        Data.BUF[province_offset + 0x08] = 0xd0
        Data.BUF[province_offset + 0x09] = 0x07
        Data.BUF[province_offset + 0x0A] = 0x20
        Data.BUF[province_offset + 0x0B] = 0x4E
        Data.BUF[province_offset + 0x0C] = 0x00
        Data.BUF[province_offset + 0x0D] = 0x00

        Data.BUF[province_offset + 0x10 ] = 0x0F
        Data.BUF[province_offset + 0x17] = 65

        ruler_offset = Data.RULER_OFFSET+Data.RULER_SIZE*0x0F
        Data.BUF[ruler_offset + 0x00] = Data.RULER_AS_OFFICER_OFFSET % 256
        Data.BUF[ruler_offset + 0x01] = int(Data.RULER_AS_OFFICER_OFFSET / 256)
        Data.BUF[ruler_offset + 0x02] = province_offset % 256
        Data.BUF[ruler_offset + 0x03] = int(province_offset / 256)
        Data.BUF[ruler_offset + 0x06] = 0x32
        for i in range(0x0E,0x1D):
            Data.BUF[ruler_offset + i] = 0x32
        Data.BUF[ruler_offset + 0x22] = 0xFF


        return ruler_offset

    def show_values(self,index,values,award):
        cols = [Helper.GetBuiltinText(0x5378),Helper.GetBuiltinText(0x537D),Helper.GetBuiltinText(0x5382)]

        pygame.draw.rect(Helper.Screen,(0,0,0),(400* Helper.Scale,140* Helper.Scale,200* Helper.Scale,70* Helper.Scale))

        for i in range(0,3):
            palette_no = 7
            if i==index:
                palette_no = 5

            img = Helper.DrawText(cols[i],scaled=True,palette_no=palette_no)
            Helper.Screen.blit(img, ((400+50*i) * Helper.Scale, 140 * Helper.Scale))

            img = Helper.DrawText(str(values[i]), scaled=True,palette_no=palette_no)
            Helper.Screen.blit(img, ((410+50*i) * Helper.Scale, 175 * Helper.Scale))

        img = Helper.DrawText(Helper.GetBuiltinText(0x542D,0x5431),scaled=True)
        Helper.Screen.blit(img, (550 * Helper.Scale, 140 * Helper.Scale))

        img = Helper.DrawText(str(award), scaled=True)
        Helper.Screen.blit(img, (560 * Helper.Scale, 175 * Helper.Scale))

    def LoadGame(self):
        while True:
            pygame.draw.rect(Helper.Screen,(0,0,0),(250 * Helper.Scale, 100 * Helper.Scale,200*Helper.Scale,200*Helper.Scale))
            pygame.display.flip()

            bmp = Helper.DrawText(Helper.GetBuiltinText(0x58E8), scaled=True,palette_no=7)
            Helper.Screen.blit(bmp, (250 * Helper.Scale, 180 * Helper.Scale))

            bmp = Helper.DrawText("----------------------", scaled=True,palette_no=7)
            Helper.Screen.blit(bmp, (250 * Helper.Scale, 250 * Helper.Scale))

            file_name = Helper.GetInput("", 250, 235, width=200,required_number=False)
            if file_name==-1:
                return ""

            if os.path.exists(Data.GamePath + file_name):

                # with open(Data.GamePath + "h.bin", "rb") as f:
                #     tmp_buf = f.read(0x42)

                tmp_buf = Data.DSBUF[0:0x42]
                with open(Data.GamePath + file_name, "rb") as f:
                    tmp_buf2 = f.read(30584)

                Data.BUF = bytearray(tmp_buf) + bytearray(tmp_buf2)[0x0A:]
                Data.RulerPalette = bytearray(tmp_buf2)[0x10:0x20]
                RoTK2.Init()

                return "OK"
            else:
                pygame.draw.rect(Helper.Screen, (0, 0, 0),(250 * Helper.Scale, 100 * Helper.Scale, 200 * Helper.Scale, 200 * Helper.Scale))
                pygame.display.flip()

                bmp = Helper.DrawText(file_name, scaled=True, palette_no=2)
                Helper.Screen.blit(bmp, (250 * Helper.Scale, 180 * Helper.Scale))

                Helper.GetInput(Helper.GetBuiltinText(0x590C), 250, 210, width=200)
