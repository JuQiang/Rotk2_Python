import os.path

from Data import Data
import pygame,sys
from Helper import Helper,Province,Officer,Ruler


class Command19(object):
    def __init__(self):
        self.commands = [Helper.GetBuiltinText(0x8BFC,0x8BFF),Helper.GetBuiltinText(0x8C05,0x8C08),Helper.GetBuiltinText(0x8C11,0x8C14),Helper.GetBuiltinText(0x8C1D,0x8C21),Helper.GetBuiltinText(0x8C27,0x8C2A),Helper.GetBuiltinText(0x8C30,0x8C33),Helper.GetBuiltinText(0x8C3D,0x8C40),Helper.GetBuiltinText(0x8C46,0x8C49)]
        self.palette_no = 5

    def Start(self,province_no):
        while True:
            Helper.ClearInputArea()
            Helper.ShowMap(province_no)
            Helper.ShowCommandsInInputArea(self.commands,4, palette_no=self.palette_no)
            cmd = Helper.GetInput(Helper.GetBuiltinText(0x5342) + "(1-{0})?".format(len(self.commands)), row=2,required_number_min=1, required_number_max=8,allow_enter_exit=True)

            if cmd==-1:
                return

            if cmd==1:
                cmds = [Helper.GetBuiltinText(0x8B37,0x8B3E),Helper.GetBuiltinText(0x8B45,0x8B4C)]
                Helper.ShowCommandsInInputArea(cmds,cols=2, palette_no=3)

                tmp = Helper.GetInput(Helper.GetBuiltinText(0x8B52)+"(1-2)? ",row=1,required_number_min=1,required_number_max=2)
                if tmp==1:
                    Helper.ClearInputArea()
                    img = Helper.DrawText(Helper.GetBuiltinText(0x8B02,0x8B17),scaled=True)
                    Helper.Screen.blit(img, (300* Helper.Scale, 295 * Helper.Scale))

                    img2 = Helper.DrawText(str(int(Data.BUF[0x337D+Data.DATA_OFFSET])),palette_no=1,scaled=True)
                    Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))
                    tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AF8)+"(1-10)? ",cursor_user_prompt_location=True,row=1,required_number_min=1,required_number_max=10)
                    if tmp>0:
                        Data.BUF[0x337D+Data.DATA_OFFSET] = tmp
                elif tmp==2:
                    Helper.ClearInputArea()
                    options_text = [Helper.GetBuiltinText(0x8ABA),Helper.GetBuiltinText(0x8AC1),Helper.GetBuiltinText(0x8AC6),Helper.GetBuiltinText(0x8ACB)]
                    option = int(Data.BUF[0x337E+Data.DATA_OFFSET] / 2)

                    Helper.ShowCommandsInInputArea(options_text,4,palette_no=3,top=32)

                    img = Helper.DrawText(Helper.GetBuiltinText(0x8AD0,0x8AD9),scaled=True)
                    Helper.Screen.blit(img,(300*Helper.Scale,295*Helper.Scale))

                    img2 = Helper.DrawText("<"+options_text[option]+">",palette_no=1,scaled=True)
                    Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))

                    tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AF8)+"(1-4)? ",cursor_user_prompt_location=True,row=2,required_number_min=1,required_number_max=4)
                    if tmp>0:
                        Data.BUF[0x337E+Data.DATA_OFFSET] = tmp*2-2

            if cmd==2:
                option = Data.BUF[0x337C+Data.DATA_OFFSET]
                if option & 0x04 == 0x04:
                    pic = Helper.GetBuiltinText(0x8A89)
                else:
                    pic = Helper.GetBuiltinText(0x8A8E)


                Helper.ClearInputArea()
                img = Helper.DrawText(Helper.GetBuiltinText(0x8A94,0x8A9B).replace("%s",Helper.GetBuiltinText(0x8A7A)),scaled=True)
                Helper.Screen.blit(img, (300* Helper.Scale, 295 * Helper.Scale))

                img2 = Helper.DrawText(pic,palette_no=1,scaled=True)
                Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))
                tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AA9)+"(1-2)? ",cursor_user_prompt_location=True,row=1,required_number_min=1,required_number_max=10)
                if tmp==1:
                    Data.BUF[0x337C+Data.DATA_OFFSET] |= 0x04
                elif tmp==2:
                    Data.BUF[0x337C+Data.DATA_OFFSET] &= 0xfb

            if cmd==3:
                option = Data.BUF[0x337C+Data.DATA_OFFSET]
                if option & 0x02 == 0x02:
                    music = Helper.GetBuiltinText(0x8A89)
                else:
                    music = Helper.GetBuiltinText(0x8A8E)


                Helper.ClearInputArea()
                img = Helper.DrawText(Helper.GetBuiltinText(0x8A94,0x8A9B).replace("%s",Helper.GetBuiltinText(0x8A7F)),scaled=True)
                Helper.Screen.blit(img, (300* Helper.Scale, 295 * Helper.Scale))

                img2 = Helper.DrawText(music,palette_no=1,scaled=True)
                Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))
                tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AA9)+"(1-2)? ",cursor_user_prompt_location=True,row=1,required_number_min=1,required_number_max=10)
                if tmp==1:
                    Data.BUF[0x337C+Data.DATA_OFFSET] |= 0x02
                elif tmp==2:
                    Data.BUF[0x337C+Data.DATA_OFFSET] &= 0xfd

            if cmd==4:
                option = Data.BUF[0x337C+Data.DATA_OFFSET]
                if option & 0x01 == 0x01:
                    music = Helper.GetBuiltinText(0x8A89)
                else:
                    music = Helper.GetBuiltinText(0x8A8E)


                Helper.ClearInputArea()
                img = Helper.DrawText(Helper.GetBuiltinText(0x8A94,0x8A9B).replace("%s",Helper.GetBuiltinText(0x8A84)),scaled=True)
                Helper.Screen.blit(img, (300* Helper.Scale, 295 * Helper.Scale))

                img2 = Helper.DrawText(music,palette_no=1,scaled=True)
                Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))
                tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AA9)+"(1-2)? ",cursor_user_prompt_location=True,row=1,required_number_min=1,required_number_max=10)
                if tmp==1:
                    Data.BUF[0x337C+Data.DATA_OFFSET] |= 0x01
                elif tmp==2:
                    Data.BUF[0x337C+Data.DATA_OFFSET] &= 0xfe

            if cmd==5:
                Helper.ClearInputArea()
                bmp = Helper.DrawText(Helper.GetBuiltinText(0x6919), scaled=True, palette_no=7)
                Helper.Screen.blit(bmp, (300 * Helper.Scale, 300 * Helper.Scale))

                bmp = Helper.DrawText("----------------------", scaled=True, palette_no=7)
                Helper.Screen.blit(bmp, (300 * Helper.Scale, 360 * Helper.Scale))

                file_name = Helper.GetInput("", 300, 345, width=200, required_number=False)
                if file_name == -1:
                    return ""

                if os.path.exists(Data.GamePath + file_name):
                    Helper.ClearInputArea()
                    yn = Helper.GetInput(Helper.GetBuiltinText(0x6933)+"(Y/N)? ",required_number=False)
                    if yn in [-1, "n"]:
                        continue

                with open(Data.GamePath + file_name,"wb") as f:
                    # research save logics in ida 2b3b0
                    # 1. write 0x0A bytes from ds:0x3E2C, 1990.02.19 flags
                    f.write(bytes(Data.DSBUF[0x3E2C:0x3E2C+0x0A]))
                    # 2. write 0x33af bytes from ds:0x42
                    f.write(bytes(Data.BUF[0x42:0x42+0x33AF]))
                    # 3. write 0x18fc bytes from hexdata:0
                    f.write(bytes(Data.HEXDATA[0:0x18fc]))
                    # 4. write 0x2ac3 bytes from unknown area, but all of the save data have same data
                    buf = [0] * 0x2ac3
                    with open(Data.GamePath+"2ac3_963.dat","rb") as f2:
                        tmp = f2.read(98)
                        for i in range(0,98):
                            buf[0x963+i] = tmp[i]
                    with open(Data.GamePath+"2ac3_c84.dat","rb") as f2:
                        tmp = f2.read(96)
                        for i in range(0,96):
                            buf[0xc84+i] = tmp[i]
                    with open(Data.GamePath+"2ac3_1e3f.dat","rb") as f2:
                        tmp = f2.read(224)
                        for i in range(0,224):
                            buf[0x1e3f+i] = tmp[i]

                    f.write(bytes(buf))

            if cmd==6:
                option = Data.BUF[0x337C+Data.DATA_OFFSET]
                if option & 0x08 == 0x08:
                    war = Helper.GetBuiltinText(0x8A89)
                else:
                    war = Helper.GetBuiltinText(0x8A8E)


                Helper.ClearInputArea()
                img = Helper.DrawText(Helper.GetBuiltinText(0x8B64,0x8B6D),scaled=True)
                Helper.Screen.blit(img, (300* Helper.Scale, 295 * Helper.Scale))

                img2 = Helper.DrawText(war,palette_no=1,scaled=True)
                Helper.Screen.blit(img2,((300+int(img.get_width()/Helper.Scale))*Helper.Scale,295*Helper.Scale))
                tmp = Helper.GetInput(Helper.GetBuiltinText(0x8AA9)+"(1-2)? ",cursor_user_prompt_location=True,row=1,required_number_min=1,required_number_max=10)
                if tmp==1:
                    Data.BUF[0x337C+Data.DATA_OFFSET] |= 0x08
                elif tmp==2:
                    Data.BUF[0x337C+Data.DATA_OFFSET] &= 0xf7

            if cmd==8:
                Helper.ClearInputArea()
                yn = Helper.GetInput(Helper.GetBuiltinText(0x8A0E,0x8A19),next_prompt="(Y/N)? ",cursor_user_prompt_location=True, palette_no=self.palette_no,yesno=True)
                if yn=="y":
                    return -1