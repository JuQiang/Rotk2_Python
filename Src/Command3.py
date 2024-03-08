import pygame.time

from Data import Data,ShowOfficerFlag
from Helper import Helper,Province,Officer,Ruler
from DrawCGA import DrawCGA
import random

class Command3(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        bmp = pygame.Surface((640*Helper.Scale,400*Helper.Scale))

        attack_province_no = 29
        index = 0x33b9 + 156 * (attack_province_no-1) + 0x38
        map_data = Data.BUF[index:index + 12 * 13]

        x = 0
        y = 0
        start = 0

        for r in range(0, 12):
            for c in range(0, 13):
                fname = "./../Resources/hex{0:02}.jpg".format(map_data[start])
                bmp_mini_map = pygame.image.load(fname)
                bmp_mini_map = pygame.transform.scale(bmp_mini_map,(bmp_mini_map.get_width()*Helper.Scale,bmp_mini_map.get_height()*Helper.Scale))
                bmp.blit(bmp_mini_map,(c * 32*Helper.Scale, r * 32*Helper.Scale + (c % 2) * 16*Helper.Scale))

                start += 1

        bmp_warmenu = Helper.GetGraphData("WarMenu",palette_no=5)

        #pygame.image.save(bmp_warmenu, "wm.png")

        warmenu_left = bmp.get_width()*0.65
        warmenu_width = bmp.get_width()*0.35

        bmp_warmenu_sub = bmp_warmenu.subsurface((warmenu_left,0,warmenu_width,bmp_warmenu.get_height()))
        bmp.blit(bmp_warmenu_sub,(warmenu_left,0,warmenu_width,bmp.get_height()))

        bmp_warmenu_top = pygame.Surface((warmenu_width-30, 100))
        bmp_warmenu_top.fill((0xff, 0xff, 0xff))
        bmp.blit(bmp_warmenu_top,(warmenu_left+16,0))

        province_name = Helper.GetProvinceName(attack_province_no)
        bmp_province_name = Helper.DrawText(province_name,(0xff,0xff,0xff),palette_no=0,scaled=True)
        bmp.blit(bmp_province_name,(warmenu_left+16,20))

        date = "{}{}  {}{}".format(Data.BUF[0x46] + 1,Helper.GetBuiltinText(0x5849),"1",Helper.GetBuiltinText(0x584E))
        bmp_date = Helper.DrawText(date,(0xff,0xff,0xff),palette_no=0,scaled=True)
        bmp.blit(bmp_date, (warmenu_left + 150, 20))

        wind_no = random.randint(0,6)
        if wind_no==0:
            bmp_wind = Helper.DrawText(Helper.GetBuiltinText(0x9BDF),(0xff,0xff,0xff),palette_no=0, scaled=True)
            bmp.blit(bmp_wind, (warmenu_left + 150 + bmp_date.get_width() + 30, 20))
        else:
            bmp_wind = Helper.DrawText(Helper.GetBuiltinText(0x9BD1),(0xff,0xff,0xff),palette_no=0,scaled=True)
            bmp.blit(bmp_wind, (warmenu_left + 150 + bmp_date.get_width()+30, 20))

            bmp_wind2 = self.draw_wind(wind_no)
            bmp.blit(bmp_wind2, (warmenu_left + 150 + bmp_date.get_width() + bmp_wind.get_width() + 30+20, 20))

        attack_ruler = Ruler.FromNo(Province.FromSequence(province_no).RulerNo).RulerSelf.GetName()
        attacked_ruler = Ruler.FromNo(Province.FromSequence(attack_province_no).RulerNo).RulerSelf.GetName()

        bmp_attack_ruler = Helper.DrawText(attack_ruler,palette_no=5,scaled=True)
        bmp_attacked_ruler = Helper.DrawText(attacked_ruler,palette_no=2,scaled=True)

        bmp.blit(bmp_attack_ruler, (warmenu_left + 50, 110))
        bmp.blit(bmp_attacked_ruler, (warmenu_left + 330, 110))

        attack_officer = Officer.FromOffset(Province.FromSequence(province_no).GovernorOffset)
        attacked_officer = Officer.FromOffset(Province.FromSequence(attack_province_no).GovernorOffset)

        bmp_attack_officer = Helper.DrawText(attack_officer.GetName(),scaled=True)
        bmp_attacked_officer = Helper.DrawText(attacked_officer.GetName(),scaled=True)

        bmp.blit(bmp_attack_officer, (warmenu_left + 50, 170))
        bmp.blit(bmp_attacked_officer, (warmenu_left + 330, 170))

        grp = Data.GrpdataMappings["Rain"]
        do = DrawCGA(grp, Data.GRPDATA[grp[0]:grp[0] + 0x4000])
        do.Start()
        bmp_weather = Helper.DrawData(do.display_buf,7)

        bmp_weather_sub = bmp_weather.subsurface((498,78,60,50))
        bmp_weather_sub = pygame.transform.scale(bmp_weather_sub,(bmp_weather_sub.get_width()*Helper.Scale,bmp_weather_sub.get_height()*Helper.Scale))
        bmp.blit(bmp_weather_sub,(warmenu_left + 170, 140))

        bmp_attack_soldiers = Helper.DrawText(str(attack_officer.Soldiers),scaled=True)
        bmp_attacked_soldiers = Helper.DrawText(str(attacked_officer.Soldiers), scaled=True)

        bmp.blit(bmp_attack_soldiers, (warmenu_left + 50, 230))
        bmp.blit(bmp_attacked_soldiers, (warmenu_left + 330, 230))

        bmp_attack_soldier2 = Helper.DrawText(Helper.GetBuiltinText(0x9C45,0x9C4A),palette_no=1, scaled=True)
        bmp.blit(bmp_attack_soldier2, (warmenu_left + 180, 230))


        bmp_attack_officers = Helper.DrawText(str("1/  4"),scaled=True)
        bmp_attacked_officers = Helper.DrawText(str("1"), scaled=True)

        bmp.blit(bmp_attack_officers, (warmenu_left + 50, 300))
        bmp.blit(bmp_attacked_officers, (warmenu_left + 330, 300))

        bmp_attack_officers2 = Helper.DrawText(Helper.GetBuiltinText(0x9C6D,0x9C72),palette_no=1, scaled=True)
        bmp.blit(bmp_attack_officers2, (warmenu_left + 180, 300))


        bmp_attack_food = Helper.DrawText(str(Province.FromSequence(province_no).Food), scaled=True)
        bmp_attacked_food = Helper.DrawText(str(Province.FromSequence(attack_province_no).Food), scaled=True)

        bmp.blit(bmp_attack_food, (warmenu_left + 50, 370))
        bmp.blit(bmp_attacked_food, (warmenu_left + 330, 370))

        bmp_attack_food2 = Helper.DrawText(Helper.GetBuiltinText(0x65A0),palette_no=3, scaled=True)
        bmp.blit(bmp_attack_food2, (warmenu_left + 180, 370))


        bmp_attack_gold = Helper.DrawText(str(Province.FromSequence(province_no).Gold), scaled=True)
        bmp_attacked_gold = Helper.DrawText(str(Province.FromSequence(attack_province_no).Gold), scaled=True)

        bmp.blit(bmp_attack_gold, (warmenu_left + 50, 440))
        bmp.blit(bmp_attacked_gold, (warmenu_left + 330, 440))

        bmp_attack_gold2 = Helper.DrawText(Helper.GetBuiltinText(0x7C37),palette_no=3, scaled=True)
        bmp.blit(bmp_attack_gold2, (warmenu_left + 180, 440))

        pygame.draw.rect(bmp, (255, 255, 255), (warmenu_left+15, 518, bmp.get_width()-warmenu_left-30, 270))
        commands = Helper.GetBuiltinText(0x9CC4).replace("_","  ").split("  ")
        for row in range(0,2):
            for col in range(0,3):
                bmp_cmd = Helper.DrawText(commands[3*row+col],(0xff,0xff,0xff), palette_no=4,scaled=True)
                bmp.blit(bmp_cmd,(warmenu_left + 30 + 130*col, 530+60*row))

        bmp_attack_ruler = Helper.DrawText(attack_ruler+",",(0xff,0xff,0xff),palette_no=0, scaled=True)
        bmp.blit(bmp_attack_ruler, (warmenu_left + 30, 650))

        # bmp_dispatch_cmd = Helper.DrawText(Helper.GetBuiltinText(0x9D00,0x9D01)+attack_officer.GetName()+Helper.GetBuiltinText(0x9D05,0x9D09)+" (1-6)? ",(0xff,0xff,0xff),palette_no=0,scaled=True)
        # bmp.blit(bmp_dispatch_cmd, (warmenu_left + 30, 720))

        Helper.Screen.blit(bmp,(0,0))
        pygame.display.flip()

        Helper.GetInput(Helper.GetBuiltinText(0x9D00,0x9D01)+attack_officer.GetName()+Helper.GetBuiltinText(0x9D05,0x9D09)+" (1-6)? ",
                                        int((warmenu_left + 30)/2),int(720/2),cursor_user_prompt_location=True,back_color=(0xff,0xff,0xff),palette_no=0,
                        width=(bmp.get_width()-warmenu_left-60)/2
                                        )

    def draw_wind(self,wind_no):
        img = pygame.Surface((16, 16))
        img.fill((0xff,0xff,0xff),(0,0,img.get_width(),img.get_height()))
        wind_angles = img.copy()
        wind_direct = img.copy()

        pygame.draw.polygon(wind_angles,(0x0,0x0,0x0),[(0,0),(10,0),(12,2),(4,2),(16,14),(14,16),(2,2),(2,8),(0,6)])
        pygame.draw.polygon(wind_direct,(0x0,0x0,0x0),[(8,0),(0,6),(0,8),(6,6),(6,16),(10,16),(10,6),(16,8),(16,6)])

        if wind_no == 1:
            img = wind_angles
        elif wind_no == 2:
            img = wind_direct
        elif wind_no == 3:
            img = pygame.transform.rotate(wind_angles,270)
        elif wind_no == 4:
            img = pygame.transform.rotate(wind_angles,180)
        elif wind_no == 5:
            img = pygame.transform.rotate(wind_direct,180)
        elif wind_no == 6:
            img = pygame.transform.rotate(wind_angles,90)

        return pygame.transform.smoothscale(img,(img.get_width()*Helper.Scale,img.get_height()*2*Helper.Scale))
#            pygame.image.save(img, "wind_{}.png".format(no))
