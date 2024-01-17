import pygame.time
import math
from Data import Data,ShowOfficerFlag
from Helper import Helper
from RoTK2 import RoTK2

class Command9_10_12(object):
    def __init__(self,prompt,resources,result,show_flag,cost_field,affected_field,max_cost):
        self.prompt = prompt
        self.resources = resources
        self.result = result
        self.show_flag = show_flag
        self.cost_field = cost_field
        self.affected_field = affected_field
        self.max_cost = max_cost

    def Start(self,province_no):
        province = RoTK2.GetProvinceBySequence(province_no)

        resources = int(province.__getattribute__(self.cost_field))
        if resources < 1:
            if self.cost_field == "Gold":
                not_enough = Helper.GetBuiltinText(0x7A90)
            else:
                not_enough = Helper.GetBuiltinText(0x7CEB)

            img = Helper.DrawText(not_enough, palette_no=6, scaled=True)
            Helper.Screen.blit(img, (300 * Helper.Scale, 358 * Helper.Scale))
            pygame.display.flip()
            pygame.time.wait(1000)
            return

        Helper.ClearInputArea()
        who = Helper.SelectOfficer(province_no,self.prompt, self.show_flag)
        if who>0:

            affect_resource = int(province.__getattribute__(self.affected_field))
            max_cost = min(resources,self.max_cost)
            really_cost = Helper.GetInput(self.resources +"(1-{0})?".format(max_cost), row=1,cursor_user_prompt_location=True,required_number_min=1,required_number_max=max_cost)
            if really_cost>0:
                province.__setattr__(self.cost_field,resources-int(really_cost))

                if self.affected_field!="Loyalty":
                    diff = self.game_development_land_flood_calc(province_no,who,really_cost,self.affected_field)
                else:
                    diff = self.game_give_population_calc(province_no,who,really_cost)

                affect = affect_resource+diff
                if affect>100:
                    affect = 100
                province.__setattr__(self.affected_field,affect)

                RoTK2.FlushProvince(province)

                if diff<1:
                    if self.cost_field == "Gold":
                        not_enough = Helper.GetBuiltinText(0x7A82,0x7A89)
                    else:
                        not_enough = Helper.GetBuiltinText(0x7D2A)

                    img = Helper.DrawText(not_enough, palette_no=6, scaled=True)
                    Helper.Screen.blit(img, (300 * Helper.Scale, 358 * Helper.Scale))
                else:
                    img = Helper.DrawText(self.result+str(affect),palette_no=3,scaled=True)
                    Helper.Screen.blit(img,(300*Helper.Scale,358*Helper.Scale))

                pygame.display.flip()
                pygame.time.wait(1000)

    def game_development_land_flood_calc(self,province_no, general_no, gold, land_flood):
        p = RoTK2.GetProvinceBySequence(province_no)

        if land_flood=="Land":
            value = p.Land
        else:
            value = p.Flood

        if value==100:
            return 0
        value = int(value / 2)
        o = p.GetOfficerBySequence(general_no)

        v1 = int(math.sqrt(int((100 - value) * gold / 100) * (int(o.Chm / 2) + o.Int)))
        dif = int((Data.GAME_DIFFCULTY + 1) / 2)
        v2 = int(math.sqrt(int(v1 / dif))) - dif

        RoTK2.SetOfficerAlreadyDoAction(o)
        return v2

    def game_give_population_calc(self,province_no,general_no,food):
        p = RoTK2.GetProvinceBySequence(province_no)
        if p.Loyalty==100:
            return 0

        r = RoTK2.GetRulerByNo(p.RulerNo).RulerSelf
        o = p.GetOfficerBySequence(general_no)

        v1 = int(math.sqrt(food)) * int((r.Chm+o.Chm)/2)
        v2 = (6+Data.GAME_DIFFCULTY)*int(math.sqrt(p.Population/100))

        RoTK2.SetOfficerAlreadyDoAction(o)

        return int(v1/v2)
class Command9(Command9_10_12):
    def __init__(self):
        super().__init__(Helper.GetBuiltinText(0x7A41),Helper.GetBuiltinText(0x7A4E),Helper.GetBuiltinText(0x7A6C,0x7A79),ShowOfficerFlag.Int,"Gold","Land",100)

class Command10(Command9_10_12):
    def __init__(self):
        super().__init__(Helper.GetBuiltinText(0x7AD0),Helper.GetBuiltinText(0x7A4E),Helper.GetBuiltinText(0x7AFB,0x7B06),ShowOfficerFlag.Int,"Gold","Flood",100)

class Command12(Command9_10_12):
    def __init__(self):
        super().__init__(Helper.GetBuiltinText(0x7CF5),Helper.GetBuiltinText(0x7CFE),Helper.GetBuiltinText(0x7D14,0x7D20),ShowOfficerFlag.Chm,"Food","Loyalty",10000)
