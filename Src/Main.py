import pygame.display

from Helper import Helper
from Command1 import Command1
from Command2 import Command2
from Command4 import Command4
from Command5 import Command5
from Command8 import Command8
from Command9_10_12 import Command9,Command10,Command12
from Command11 import Command11
from Command13 import Command13
from Command14 import Command14
from Command15 import Command15
from Command16 import Command16
from Command18 import Command18
from Command19 import Command19
from Data import Data
from RoTK2 import RoTK2
from Open import Open
from MainMenu import MainMenu

class KeyboardDrivenFramework(object):
    def generate_images(self):
        msg = Data.DSBUF.copy()
        buf = []
        buf2 = []

        i = 0x3000
        start = i
        while True:
            if i>=len(msg):
                break

            b = msg[i]
            if b==0:
                text = ''.join(buf2)
                if len(text)>0:
                    buf.append(text)
                    print(text)
                    img = Helper.DrawText(text,scaled=True)
                    pygame.image.save(img,"images/{0}.png".format((hex(start)[2:]).upper()))
                buf2 = []
                i += 1
                start = i
            elif b==0x0a:
                buf2.append("_")
                i += 1
            elif b<0x20:
                buf2.append(".")
                i+=1
            elif b==0x24:
                buf2.append(".")
                i += 1
            elif b<0x80:
                buf2.append(chr(b))
                i+=1
            elif b>=0x80:
                b2 = msg[i + 1]
                zh_cn = Data.CNINDEX.get(b*256+b2)
                if zh_cn is not None:
                    buf2.append("$")
                    buf2.append(str(zh_cn))
                    i += 2
                    buf2.append("$")
                else:
                    i += 1
            else:
                i+=1
                continue


    def __init__(self):
        RoTK2.Init()
        Helper.Init(2, 4)

        self.mappings={-1:None,1:Command1(),2:Command2(),4:Command4(),5:Command5(), 8:Command8(),9:Command9(),10:Command10(),11:Command11(),12:Command12(),13:Command13(),14:Command14(),15:Command15(),16:Command16(),18:Command18(),19:Command19()}
        self.map_command_switch = True

    def switch_map_command(self):
        Data.ProvinceList = RoTK2.GetProvinceList()
        Data.OfficerList = RoTK2.GetOfficerList()

        if self.map_command_switch is True:
            Helper.ShowMap(Helper.CurrentProvinceNo)
        else:
            bmp = Helper.GetAll20Commands()
            Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
            pygame.display.flip()

        self.map_command_switch = not self.map_command_switch

    def Start(self):

        open = Open()
        open.Start()

        main = MainMenu()
        ret = main.Start()

        if ret==-1:
            return

        Helper.GetCurrentProvinceNo()
        Helper.MainMap = Helper.GetMap()

        Helper.ShowMap(Helper.CurrentProvinceNo)


        while True:
            cmd = Helper.GetBuiltinText(0x5CEB).replace("%d-%d","1-41").replace("%d", str(Helper.CurrentProvinceNo))
            gov_off = RoTK2.GetProvinceBySequence(Helper.CurrentProvinceNo).Governor
            prompt = cmd.replace("%s", RoTK2.GetOfficerName(gov_off))

            self.switch_map_command()
            Helper.ClearInputArea()
            input = Helper.GetInput(prompt,300,298,"",required_number_min=0,required_number_max=19,allow_enter_exit=True)

            if input>-1:
                cmd = self.mappings.get(input)
                if cmd is None:
                    Helper.ShowDelayedText("$685$$545$$97$$854$$825$!")
                    continue
                ret = cmd.Start(Helper.CurrentProvinceNo)
                self.map_command_switch = True
                if ret==-1:
                    return

def main():
    kdf = KeyboardDrivenFramework()
    #kdf.generate_images()
    kdf.Start()

if __name__=="__main__":
    main()