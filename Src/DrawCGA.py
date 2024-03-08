from CpuRegister import CpuRegister

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

        bp6 = mappings[1]
        bp8 = mappings[2]
        di = int(bp8 / 2) * 16 * 10 + int(bp6 / 4)
        if bp8 % 2 == 1:
            di += 0x4000

        self.disp_index = di#每次画一个完整的大图，这里是第一个有效像素位置。所以实际上每次都是640*200的图，然后xor显示上去。

    #https://bumbershootsoft.wordpress.com/2015/09/05/cga-the-oldest-tricks-in-the-pcs-book/
    #http://www.columbia.edu/~em36/wpdos/videomodes.txt

    def Start(self):
        # Let's start from 76c:32AD
        while True:
            flag_drawlogo = False
            #32AD
            self.r.Push(self.r.BX)
            self.r.Push(self.r.CX)
            self.r.Push(self.disp_index)

            self.r.CX = self.r.BX

            # endregion data
            while True:#32B2
                self.r.Push(self.r.CX)  # JUQIANG 11/13/2023

                self.r.AL = self.data[self.index]
                self.index += 1

                while True:
                    flag_346b = False

                    if (self.r.AL & 0x80)!=0x80:
                        # region data
                        # 32BC->33a7
                        #self.GetPixel2()#33a7
                        pixel = self.r.AL

                        self.r.AL = self.data[self.index]
                        self.pixel2 = self.r.AL
                        self.index += 1
                        # 33ad
                        new_pixel = (int(self.pixel2 / 16) * 16 % 256) | int((pixel * 16)%256)
                        if self.is_draw_logo is False:
                            new_pixel = int(pixel * 16)%256
                        disp_index_offset = (int(pixel / 16) & 7) + 1

                        self.r.Push(disp_index_offset)
                        self.r.Push(self.disp_index)

                        is_odd = self.disp_index % 2
                        self.disp_index = int(self.disp_index>>1)

                        if is_odd == 1:
                            #3449
                            while disp_index_offset>0:
                                self.display_buf[self.disp_index] = int(new_pixel / 16) + int(self.display_buf[self.disp_index] / 16) * 16
                                self.disp_index += 1
                                disp_index_offset -= 1

                                if disp_index_offset > 0:
                                    self.display_buf[self.disp_index] = int(new_pixel / 16) * 16 + self.display_buf[self.disp_index] % 16
                                    disp_index_offset -= 1
                        else:
                            while disp_index_offset>0:
                                self.display_buf[self.disp_index] = int(new_pixel / 16) * 16 + self.display_buf[self.disp_index] % 16
                                disp_index_offset -= 1
                                if disp_index_offset>0:
                                    self.display_buf[self.disp_index] = int(new_pixel / 16) + int(self.display_buf[self.disp_index] / 16) * 16
                                    self.disp_index += 1
                                    disp_index_offset -= 1

                    else:
                        # region data
                        self.r.CL = self.r.AL  # 32BF
                        self.r.AX &= 0x30 # get bit 4/5 from index 0
                        # endregion data

                        if (self.r.CL & 0x40)==0x40: #bit 6 is 1
                            # 32CB
                            self.func_3337()

                            self.r.SI = int(self.r.SI>>1)
                            is_odd = self.disp_index % 2
                            self.disp_index = int(self.disp_index >> 1)

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
                                is_odd = self.disp_index % 2#32E9
                                self.disp_index =int(self.disp_index>>1)

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
                                is_odd = self.disp_index % 2
                                self.disp_index =int(self.disp_index>>1)  # 32E2

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
        self.r.SI = self.disp_index

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
        self.r.Push(self.disp_index)

        # endregion data

    def Draw_Pixel_4(self):
        self.display_buf[self.disp_index] = int(self.display_buf[self.disp_index]/16)+int(self.display_buf[self.r.SI]/16)*16
        self.r.CX -= 1

    def RestoreStack(self):
        # region data
        self.disp_index = self.r.Pop()
        self.r.AX = self.r.Pop()
        self.disp_index += self.r.AX
        self.r.CX = self.r.Pop()
        self.r.CX -= self.r.AX

    def Draw_Pixel_2(self):
        self.display_buf[self.disp_index] = int(self.display_buf[self.disp_index] / 16) * 16 + self.display_buf[self.r.SI] % 16
        self.r.SI += 1
        self.disp_index += 1
        self.r.CX -= 1

    def Draw_Pixel_3(self):
        self.display_buf[self.disp_index] = int((self.display_buf[self.r.SI]*16)%256/16*16)+self.display_buf[self.disp_index]%16
        self.r.SI += 1
        self.r.CX -= 1

    def Draw_Pixel_6(self):
        self.display_buf[self.disp_index] = int(self.r.DL/16)*16+self.display_buf[self.disp_index]%16
        self.r.CX -= 1

    def Draw_Pixel_1(self):
        self.display_buf[self.disp_index] = int(self.display_buf[self.r.SI]/16)+int(self.display_buf[self.disp_index]/16)*16

        self.disp_index += 1
        self.r.CX -= 1

    def Draw_Pixel_5(self):
        self.display_buf[self.disp_index] = int(self.r.DL/16)+int(self.display_buf[self.disp_index]/16)*16
        self.disp_index += 1
        self.r.CX -= 1

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
        self.disp_index = self.r.Pop()
        self.r.AX = 0xa0
        if self.disp_index < 0x4000:
            # jmp 3489
            self.disp_index += 0x4000
        else:
            self.disp_index += self.r.AX
            self.disp_index -= 0x4000
            # jmp 348d

        # 348d
        self.r.CX = self.r.Pop()
        self.r.BX = self.r.Pop()
        self.r.CX -= 1

    def GetPixel(self):
        # region data
        # 32B4
        self.r.Push(self.r.CX) #JUQIANG 11/13/2023

        self.r.AL = self.data[self.index]
        self.index += 1

    def GetPixel2(self):
        # region data
        # 33a7
        self.r.Push(self.r.AX)
        self.r.AL = self.data[self.index]
        self.index += 1
        # endregion data

    def Exit(self):#3495
        self.r.AX = 0xFFFF
        self.disp_index = self.r.Pop()
        self.r.SI = self.r.Pop()
        self.r.BP = self.r.Pop()
        return

    v3428 = 0


    def func_32cb(self, is_odd):
        self.r.AX = int(self.r.AX >> 4)
        self.r.AX += 1                      #get high 4 bits and + 1
        self.r.SI = self.disp_index
        self.r.SI -= self.r.AX              #back to ax pixels
        self.r.CX &= 0x0f                   #get low 4 bits and +1
        self.r.CX += 1
        self.r.Push(self.r.CX)
        self.r.Push(self.disp_index)
        is_odd = self.r.SI % 2
        self.r.SI = int(self.r.SI >> 1)
        return is_odd

    def func_33ad(self):
        self.r.DL = int(self.r.AL/16)*16#pixel_2[0] + "0",16)
        self.r.BL = int(self.r.AL%16)*16#pixel_2[1] + "0", 16)

        pixel_1 = self.r.Pop()

        self.r.DH = int(pixel_1*16)# pixel_1<<4  # grow up to 16 times, 0x09->0x90
        self.r.DL |= self.r.DH # 这里龙虎用
        if self.is_draw_logo is False:
            self.r.DL = self.r.DH # 这里地图用
        self.r.AX = (int(pixel_1/16) & 7)+1
        self.r.CX = self.r.AX
        self.r.Push(self.r.CX)
        self.r.Push(self.disp_index)