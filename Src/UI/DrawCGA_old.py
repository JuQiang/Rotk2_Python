from Src.UI.CpuRegister import CpuRegister

class DrawCGA(object):
    def __init__(self,mappings,data,is_draw_logo=False):
        self.is_draw_logo = is_draw_logo
        self.log = []
        self.display_buf = [0]*0x4000 # 640*200的尺寸为640/8*200=16000字节=0x3E80字节

        # data in grpdata.dat, starts with offset 0x37ae

        self.data = data
        self.w = (data[0x01] << 8) + data[0x00]
        self.h = (data[0x03] << 8) + data[0x02]

        self.index = 0x04

        # g76c: 3593
        self.r = CpuRegister()
        self.r.AX = 0
        self.r.BX = int((self.w+3)/4)
        self.r.CX = self.h
        self.r.DX = 0
        self.r.SI = 0

        bp6 =mappings[1]
        bp8 = mappings[2]
        di = int(bp8 / 2) * 16 * 10 + int(bp6 / 4)#mappings[1]->bp6
        if bp8 % 2 == 1:
            di += 0x4000

        self.r.DI = di#每次画一个完整的大图，这里是第一个有效像素位置。所以实际上每次都是640*200的图，然后xor显示上去。

    #https://bumbershootsoft.wordpress.com/2015/09/05/cga-the-oldest-tricks-in-the-pcs-book/
    #http://www.columbia.edu/~em36/wpdos/videomodes.txt

    def Start(self):
        # Let's start from 76c:32AD
        while True:
            #self.log.append("!!!!!!Start 3593 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI,self.r.AL,self.r.CX))
            flag_drawlogo = False
            #32AD
            self.r.Push(self.r.BX)
            self.r.Push(self.r.CX)
            self.r.Push(self.r.DI)

            self.r.CX = self.r.BX

            # endregion data
            while True:#32B2
                #self.log.append("Loop 32AD - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI,self.r.DI,self.r.AL,self.r.CX))
                self.GetPixel()
                while True:
                    self.log.append("Loop after getpixel - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI,self.r.DI,self.r.AL,self.r.CX))
                    flag_346b = False

                    if (self.r.AL & 0x80)!=0x80:
                        # region data
                        # 32BC->33a7
                        self.GetPixel2()#33a7
                        # 33ad
                        self.func_33ad()

                        is_odd = self.r.DI % 2
                        self.r.DI = int(self.r.DI>>1)

                        if is_odd == 1:
                            #3449
                            while True:
                                self.Draw_Pixel_5()#3449
                                if self.r.CX == 0:
                                    flag_346b = True
                                    break

                                self.Draw_Pixel_6()#3432
                                if self.r.CX == 0:
                                    flag_346b = True
                                    break
                        else:
                            while True:
                                self.Draw_Pixel_6()#3432
                                if self.r.CX==0:
                                    flag_346b = True
                                    break

                                self.Draw_Pixel_5()  # 3449
                                if self.r.CX == 0:
                                    flag_346b = True
                                    break
                                    # self.DrawPixel()

                    else:
                        # region data
                        self.r.CL = self.r.AL  # 32BF
                        self.r.AX &= 0x30 # get bit 4/5 from index 0
                        # endregion data

                        if (self.r.CL & 0x40)==0x40: #bit 6 is 1
                            # 32CB
                            self.func_3337()

                            self.r.SI = int(self.r.SI>>1)
                            is_odd = self.r.DI % 2
                            self.r.DI = int(self.r.DI >> 1)

                            if is_odd==1:  # 3388
                                while True:
                                    self.Draw_Pixel_2()#3388
                                    if self.r.CX == 0:
                                        flag_346b = True
                                        break

                                    self.Draw_Pixel_4()#3370
                                    if self.r.CX == 0:
                                        flag_346b = True
                                        break
                            else:
                                while True:
                                    self.Draw_Pixel_4()#3370
                                    if self.r.CX == 0:
                                        flag_346b = True
                                        break

                                    self.Draw_Pixel_2()#3388
                                    if self.r.CX == 0:
                                        flag_346b = True
                                        break
                        else:
                            # 32CB
                            is_odd = self.func_32cb(is_odd)

                            if is_odd==1:  # 32E0
                                is_odd = self.r.DI % 2#32E9
                                self.r.DI =int(self.r.DI>>1)

                                if is_odd == 0:
                                    while True:
                                        self.Draw_Pixel_3()#32f0
                                        if self.r.CX==0:
                                            flag_346b = True
                                            break

                                        self.Draw_Pixel_1()#3311
                                        if self.r.CX==0:
                                            flag_346b = True
                                            break
                                else:
                                    while True:
                                        self.Draw_Pixel_2()#3388
                                        if self.r.CX == 0:
                                            flag_346b = True
                                            break

                                        self.Draw_Pixel_4()#3370
                                        if self.r.CX==0:
                                            flag_346b = True
                                            break
                            else:
                                is_odd = self.r.DI % 2
                                self.r.DI =int(self.r.DI>>1)  # 32E2

                                if is_odd == 1:
                                    # region something
                                    while True:
                                        self.Draw_Pixel_1()#3311
                                        if self.r.CX == 0:
                                            flag_346b=True
                                            break

                                        self.Draw_Pixel_3()#32f0
                                        if self.r.CX == 0:
                                            flag_346b=True
                                            break
                                    # endregion something
                                else:#32e6->3370
                                    while True:
                                        self.Draw_Pixel_4()#3370
                                        if self.r.CX==0:
                                            flag_346b = True
                                            break

                                        self.Draw_Pixel_2()#3388
                                        if self.r.CX == 0:
                                            flag_346b = True
                                            break

                    if flag_346b is True:
                        self.RestoreStack()
                        if self.r.CX <= 0:
                            self.func_3477()
                            if self.r.CX == 0:
                                # 377b
                                self.r.AX = 0
                                return
                            else:
                                flag_drawlogo = True
                                break
                                #self.DrawLogo()
                            # jmp 3593
                        else:
                            break
                            # self.DrawPixel()

                if flag_drawlogo is True:
                    break

    def func_3337(self):
        #region data
        self.r.DX = self.r.AX
        self.r.SI = self.r.DI

        if (self.r.DL & 0x10)==0x10:
            # jmp 3353
            self.r.AX += 0x10
        else:
            if self.r.SI < 0x4000:#3626
                # region 334c
                self.r.SI += 0x4000
                self.r.AX += 0x10
                # 3353
                self.r.AX += 0x10
                # endregion 3632
            else:
                self.r.SI -= 0x4000

        self.r.AL = int(self.r.AL >> 1)
        self.r.BX = self.r.AX
        self.r.AX <<= 2
        self.r.AX += self.r.BX
        self.r.AX <<= 1
        self.r.SI -= self.r.AX
        self.r.CX &= 0x0f
        self.r.CX += 1
        self.r.Push(self.r.CX)
        self.r.Push(self.r.DI)

        #self.log.append("func_361d - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,self.r.CX))
        # endregion data

    def Draw_Pixel_4(self):
        # region data
        # 3370
        # self.r.AH = self.display_buf[self.r.SI]# ah = 该si指向的b800显存位置的值
        # self.r.AH &= 0xf0
        # self.r.AL = self.display_buf[self.r.DI]# al = 该di指向的b800显存位置的值
        # self.r.AL &= 0x0f
        # self.r.AL |= self.r.AH
        #
        # self.display_buf[self.r.DI] = self.r.AL # 该di指向的b800显存位置 = al
        self.display_buf[self.r.DI] = int(self.display_buf[self.r.DI]/16)+int(self.display_buf[self.r.SI]/16)*16
        self.r.CX -= 1

        # endregion data

        self.log.append("Draw4 3370 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,
                                                                             self.r.CX))

    def RestoreStack(self):
        # region data
        self.r.DI = self.r.Pop()
        self.r.AX = self.r.Pop()
        self.r.DI += self.r.AX
        self.r.CX = self.r.Pop()
        self.r.CX -= self.r.AX

        # endregion data
        #self.log.append("Restore: SI:0x{0:4X}, DI:0x{1:4X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,self.r.CX))

    def Draw_Pixel_2(self):
        # 3388
        # region data
        # self.r.AH = self.display_buf[self.r.SI]# ah = 该si指向的b800显存位置的值
        # self.r.AH &= 0x0f
        # self.r.AL = self.display_buf[self.r.DI]# al = 该di指向的b800显存位置的值
        # self.r.AL &= 0xf0
        # self.r.AL |= self.r.AH
        #
        #
        # self.display_buf[self.r.DI] = self.r.AL# 该di指向的b800显存位置 = al
        self.display_buf[self.r.DI] = int(self.display_buf[self.r.DI] / 16) * 16 + self.display_buf[self.r.SI] % 16
        self.r.SI += 1
        self.r.DI += 1
        self.r.CX -= 1
        # endregion data
        self.log.append("Draw2 3388 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,
                                                                                     self.r.CX))

    def Draw_Pixel_3(self):
        #region data
        # 32f0
        # self.r.AH = self.display_buf[self.r.SI]# ah = 该si指向的b800显存位置的值
        # self.r.AH <<= 4
        # self.r.AH &= 0xf0
        # self.r.AL = self.display_buf[self.r.DI]# al = 该di指向的b800显存位置的值
        # self.r.AL &= 0x0f
        # self.r.AL |= self.r.AH
        #
        # self.display_buf[self.r.DI] = self.r.AL# 该di指向的b800显存位置 = al
        self.display_buf[self.r.DI] = int((self.display_buf[self.r.SI]*16)%256/16*16)+self.display_buf[self.r.DI]%16
        self.r.SI += 1
        self.r.CX -= 1
        # endregion data

        self.log.append("Draw3 32f0 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,
                                                                                     self.r.CX))

    def Draw_Pixel_6(self):
        #3432
        # dl high 4 bits ++ pixel low 4 bits
        # self.r.AH = self.display_buf[self.r.DI]
        # self.r.AH &= 0x0f   #get pixel low 4 bits
        # self.r.AL = self.r.DL
        # self.r.AL &= 0xf0   #get DL high 4 bits -> AL
        # self.r.AL |= self.r.AH
        #
        # self.display_buf[self.r.DI] = self.r.AL  # 该di指向的b800显存 = al
        self.display_buf[self.r.DI] = int(self.r.DL/16)*16+self.display_buf[self.r.DI]%16
        self.r.CX -= 1

    def Draw_Pixel_1(self):
        #region data
        # 3311
        #self.display_buf[self.r.DI] = (((self.display_buf[self.r.DI]&0xf0)*16)%256 + int(self.display_buf[self.r.SI]/16))%256
        # self.r.AH = self.display_buf[self.r.SI]# ah = 该si指向的b800显存位置的值
        # self.r.AH = int(self.r.AH >> 4)
        # #self.r.AH &= 0x0f
        # self.r.AL = self.display_buf[self.r.DI]# al = 该di指向的b800显存位置的值
        # self.r.AL &= 0xf0
        # self.r.AL |= self.r.AH
        #
        # self.display_buf[self.r.DI] = self.r.AL# 该di指向的b800显存位置 = al

        self.display_buf[self.r.DI] = int(self.display_buf[self.r.SI]/16)+int(self.display_buf[self.r.DI]/16)*16

        self.r.DI += 1
        self.r.CX -= 1
        # endregion data

        self.log.append("Draw1 3311 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,
                                                                                 self.r.CX))

    def Draw_Pixel_5(self):
        #3449
        #region data
        # dl high 4 bits ++ pixel high 4 bits
        self.display_buf[self.r.DI] = int(self.r.DL/16)+int(self.display_buf[self.r.DI]/16)*16

        # self.r.AH = self.display_buf[self.r.DI]# ah = 该di指向的b800显存位置的值
        # self.r.AH &= 0xf0 #get 4 bits
        # self.r.AL = self.r.DL
        # self.r.AL = int(self.r.AL>>4)
        # self.r.AL &= 0x0f
        # self.r.AL |= self.r.AH
        #
        # self.display_buf[self.r.DI] = self.r.AL# 该di指向的b800显存 = al
        self.r.DI += 1
        self.r.CX -= 1
        # endregion data
        self.log.append("Draw5 3449 - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,
                                                                                     self.r.CX))

    def func_3477(self):
        #Mode 6 uses what’s called an “even/odd” layout, designed, I would guess, to make it easier to produce an image on interlaced displays.
        # With 8 bits per pixel and 640 pixels across, 80 bytes suffices to specify one complete
        # scanline in this mode. Like the text mode, this starts at B8000.
        # Unlike the text mode, though,
        # instead of just being a solid block of (in this case) 16,000 bytes to represent the whole screen,
        # it’s two blocks of 8,000 bytes; one for the even-numbered rows (0, 2, 4, etc.) and one at BA000 for the odd-numbered rows (1, 3, 5, etc.).
        # Given how annoying it is to juggle values in segment registers, when programming this mode
        # I would normally suggest keeping the ES register at B800 and then just adding 0x2000 to your offset register
        # when writing to odd-numbered rows.
        #region data
        self.r.DI = self.r.Pop()
        self.r.AX = 0xa0
        if self.r.DI < 0x4000:
            # jmp 3489
            self.r.DI += 0x4000
        else:
            self.r.DI += self.r.AX
            self.r.DI -= 0x4000
            # jmp 348d

        # 348d
        self.r.CX = self.r.Pop()
        self.r.BX = self.r.Pop()
        self.r.CX -= 1
        # endregion data

        #self.log.append("func_375d - SI:0x{0:04X}, DI:0x{1:04X},  AL: 0x{2:02X}, CX: 0x{3:04X}".format(self.r.SI, self.r.DI, self.r.AL,self.r.CX))

    def GetPixel(self):
        # region data
        # 32B4
        self.r.Push(self.r.CX) #JUQIANG 11/13/2023

        self.r.AL = self.data[self.index]
        self.index += 1
        # endregion data
        self.log.append("Get pixel 32B4: 0x{0:02X} - 0x{1:02X}".format(self.index - 1, self.r.AL))

    def GetPixel2(self):
        # region data
        # 33a7
        self.r.Push(self.r.AX)
        self.r.AL = self.data[self.index]
        self.index += 1
        # endregion data
        self.log.append("Get pixel2 33a7: 0x{0:02X} - 0x{1:02X}".format(self.index - 1, self.r.AL))

    def Exit(self):#3495
        self.r.AX = 0xFFFF
        self.r.DI = self.r.Pop()
        self.r.SI = self.r.Pop()
        self.r.BP = self.r.Pop()
        return

    v3428 = 0


    def func_32cb(self, is_odd):
        self.r.AX = int(self.r.AX >> 4)
        self.r.AX += 1                      #get high 4 bits and + 1
        self.r.SI = self.r.DI
        self.r.SI -= self.r.AX              #back to ax pixels
        self.r.CX &= 0x0f                   #get low 4 bits and +1
        self.r.CX += 1
        self.r.Push(self.r.CX)
        self.r.Push(self.r.DI)
        is_odd = self.r.SI % 2
        self.r.SI = int(self.r.SI >> 1)
        return is_odd

    def func_33ad(self):
        self.r.DL = int(self.r.AL/16)*16#pixel_2[0] + "0",16)
        self.r.BL = int(self.r.AL%16)*16#pixel_2[1] + "0", 16)

        # self.r.BL = self.r.AL   # 2nd pixel->AL
        # self.r.BL &= 0x0f       # get low 4 bits
        # self.r.BL <<= 4         # grow up 16 times
        # self.r.DL = self.r.AL
        # self.r.DL &= 0xf0       # get high 4 bits. 截止到这里，0x49就是变化为了DL=40,BL=90,

        # 33BF 1st piexl->AX
        pixel_1 = self.r.Pop()

        self.r.DH = int(pixel_1*16)# pixel_1<<4  # grow up to 16 times, 0x09->0x90
        # 3409，这里有判断mod 4的那个逻辑,I changed it to 6
        self.r.DL |= self.r.DH # 这里龙虎用
        if self.is_draw_logo is False:
            self.r.DL = self.r.DH # 这里地图用
        # 341E
        # self.r.AL = int(self.r.AL >> 4) #get high 4 bits
        # self.r.AX &= 7 #get low 3 bits
        # self.r.AX += 1
        self.r.AX = (int(pixel_1/16) & 7)+1
        self.r.CX = self.r.AX
        self.r.Push(self.r.CX)
        self.r.Push(self.r.DI)