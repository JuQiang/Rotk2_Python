from Src.UI.CpuRegister import CpuRegister
import pygame

class DrawMapLines(object):
    def __init__(self,map,dsbuf, width, height,color):
        self.log = []
        self.display_buf = [0] * 0x4000  # 640*200的尺寸为640/8*200=16000字节=0x3E80字节

        self.map = map
        self.DS_BUF= dsbuf
        self.w = width
        self.h = height
        self.ruler_color = color

        self.index = 0x00

        self.r = CpuRegister()
        self.r.AX = 0xffff
        self.r.BX = self.h
        self.r.CX = self.w
        self.r.DX = 0
        self.r.SI = 0x342B
        self.r.DI = 0x1059

        self.SP = 0xe424

        self.rcr_mappings = [0, 0x80, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc, 0xfe, 0xff]

    def init(self):
        # 76c:939
        self.r.BX >>= 1
        self.r.Push(self.r.BX)
        self.r.BX >>= 1
        self.r.AX = self.r.BX
        self.r.BX <<= 2
        self.r.BX += self.r.AX
        self.r.BX <<= 4
        self.r.AX = self.r.CX
        self.r.AX >>= 3
        self.r.BX += self.r.AX
        self.r.AX = self.r.Pop()
        self.r.AX &= 0x01
        if self.r.AX == 0x01:
            self.r.BX += 0x2000
        # 76c:96e
        self.WriteDSBufferWord(self.SP, 0x3415)
        self.WriteDSBufferWord(self.SP, 0x3417)
        self.WriteDSBufferWord(self.SP, 0x3419)

        self.SP -= 0x1c2
        self.WriteDSBufferWord(self.SP, 0x3413)
        self.WriteDSBufferWord(self.SP, 0x340D)
        self.WriteDSBufferWord(self.SP, 0x340F)
        self.WriteDSBufferWord(self.SP, 0x3411)

        self.SP -= 0x96
        self.WriteDSBufferWord(self.SP, 0x340B)

        self.r.CX &= 7
        self.r.CX += 1
        self.r.AL = self.rcr_mappings[self.r.CX]
        self.r.CH = self.r.AL
        self.r.CL = 0
        self.r.DX = 0x9090
        self.r.DI = 0xD0F6

        self.v_c48 = self.r.DI

        # call 1221: flash small cursor

    def Start(self):
        self.init()
        # a6b
        # self.r.Push(self.r.CS)

        self.r.DI = 0x340b
        self.func_9XX()
        self.r.CH = 0x00
        # self.r.Push(self.r.CS)
        self.r.DI = 0x340b
        self.func_9XX()

        break_to_a7c = False
        break_to_a77 = False
        call_ac7 = False

        while True:
            # self.r.Push(self.r.CS)#a77
            self.r.DI = 0x3413
            self.func_9XX()

            while True:
                # self.r.Push(self.r.CS)#a7c
                self.r.DI = 0x340B
                self.func_A0X()
                self.r.CH |= self.r.CH
                if self.r.CH != 0:
                    # self.r.Push(self.r.CS)#a88
                    self.func_C28()
                    self.r.CL = self.r.AL
                    self.r.AL &= self.r.CH
                    if self.r.AL != 0:
                        self.r.CH <<= 1  # a93
                        self.r.CH = 0xFF - self.r.CH
                        if (self.r.AL & self.r.CH) != 0:
                            # a7c
                            continue
                    else:
                        while True:
                            # self.r.Push(self.r.CS)#a9d
                            if self.func_A1E() is True:
                                # ac7,copy ac7 to here, because of below ac7 is belong to a if ch==0 code snippet
                                self.r.CH = 0xff  # ac7
                                call_ac7 = True
                                break
                                # call ac7
                                pass
                            else:
                                self.r.BX -= 1
                                # self.r.Push(self.r.CS)
                                self.func_C28()
                                self.r.CL = self.r.AL
                                self.r.AL |= self.r.AL
                                if self.r.AL != 0:  # aae
                                    break

                    if call_ac7 is False:
                        # ab0
                        self.r.CH = 0
                        carry = "0"
                        while True:
                            self.r.AL, carry = self.rcr(self.r.AL, carry)
                            if carry == "0":
                                # next carry flag always is 1,
                                # 76c:ab6 stc
                                # 76c:ab7 rcl ch,1
                                self.r.CH, carry = self.rcl(self.r.CH, "1")
                            else:
                                break
                        self.r.CH |= self.r.CH #abb
                        if self.r.CH == 0:
                            self.r.BX += 1  # abe
                            # self.r.Push(self.r.CS)
                            self.func_C28()
                            self.r.CL = self.r.AL
                            self.r.CH = 0xff  # ac7
                    else:
                        call_ac7 = False
                    # ac9
                    # self.r.Push(self.r.CS)
                    self.r.DI = 0x3413
                    self.func_9XX()
                    self.r.AL = self.r.CL
                    self.r.CL = 3

                    while True:
                        self.r.AL &= self.r.CH  # ad2
                        if self.r.AL != 0:
                            self.r.AH = 0  # ad6
                            carry = "0"
                            while True:
                                self.r.AL, carry = self.rcl(self.r.AL, carry)
                                if carry == "0":
                                    self.r.AH, carry = self.rcr(self.r.AH, "1")
                                else:
                                    break
                            self.r.AH &= self.r.CH  # ae1
                            if self.r.AH == 0:
                                self.r.CH = self.r.DH  # ae5
                                self.r.BX -= 1  # ae7
                                # self.r.Push(self.r.CS)
                                self.r.DI = 0x3413
                                self.func_9XX()
                                break
                                # jmp a7c
                            else:  # aef
                                self.r.CH = self.r.AH
                                # self.r.Push(self.r.CS)
                                self.r.DI = 0x3413
                                self.func_9XX()  # af3

                        self.r.AL = self.r.CH  # af6
                        self.r.DI, self.r.BX = self.r.BX, self.r.DI
                        # self.r.Push(self.r.CS)#b09
                        self.func_c4B()
                        self.r.DI, self.r.BX = self.r.BX, self.r.DI  # b0d
                        if self.r.BX > 0x2000:
                            self.r.BX -= 0x2000
                        else:
                            self.r.BX -= 0x50
                            self.r.BX += 0x2000

                        self.r.DH = self.r.CH
                        self.r.DH = 0xff - self.r.DH  # b22
                        if self.r.BX < 0x1fb0 or self.r.BX >= 0x2000:
                            # self.r.Push(self.r.CS)#b33
                            self.func_A38()

                            while True:
                                self.r.BX += 0x50  # b37
                                if self.r.BX < 0x1F40 or self.r.BX >= 0x1F90:
                                    self.r.CL, carry = self.ror(self.r.CL)  # b46
                                    # self.r.Push(self.r.CS)
                                    self.func_A38()
                                    self.r.CL, carry = self.rol(self.r.CL)
                                    # b4f
                                if self.r.BX < 0x2000:
                                    self.r.BX -= 0x50
                                    self.r.BX += 0x2000
                                else:
                                    self.r.BX -= 0x2000
                                self.r.CH = self.r.DH
                                self.r.CH = 0xFF - self.r.CH
                                if ((self.r.CH & 0x01) == 0x01):
                                    # b6e
                                    self.r.BX += 1
                                    # self.r.Push(self.r.CS)
                                    if self.func_A1E() is True: # game中，以下这个分支从来没走过
                                        # jmp ae7, below is ae7
                                        self.r.BX -= 1  # ae7
                                        # self.r.Push(self.r.CS)
                                        self.r.DI = 0x3413
                                        self.func_9XX()
                                        break_to_a7c = True
                                        break
                                        # jmp a7c
                                    else:
                                        self.r.DH = self.r.CH  # b79
                                        self.r.CH = 0xff
                                        # self.r.Push(self.r.CS)
                                        self.func_C28()
                                        break
                                        # jmp ad2
                                else:
                                    break_to_a7c = True
                                    break

                            if break_to_a7c is True:
                                break_to_a7c = False
                                break
                else:
                    # a85: jmp b85
                    # below is b85
                    # self.r.Push(self.r.CS)
                    self.r.DI = 0x340b
                    self.func_9XX()
                    # self.r.Push(self.r.CS)

                    while True:
                        self.r.DI = 0x3413  # b8a
                        self.func_A0X()
                        self.r.CH &= self.r.CH
                        if self.r.CH == 0:
                            if self.r.SI == self.ReadDSBufferWord(0x3417):
                                return
                            else:
                                break_to_a77 = True
                                break
                        else:
                            self.r.CL = self.r.CH  # b9d
                            self.r.Push(self.r.BX)
                            # self.r.Push(self.r.CS)
                            self.r.DI = 0x3413
                            self.func_A0X()
                            self.r.CH, self.r.CL = self.r.CL, self.r.CH
                            self.r.DX, self.r.BX = self.r.BX, self.r.DX
                            self.r.BX = self.r.Pop()
                            self.r.Push(self.r.DX)
                            self.r.DI = 0x50
                            self.r.AX = self.r.BX
                            self.r.DX = 0
                            if self.r.AX < 0x2000:
                                tmp = int(self.r.AX / self.r.DI)
                                self.r.DX = self.r.AX % self.r.DI
                                self.r.AX = tmp
                                self.r.AX <<= 1
                            else:
                                self.r.AX -= 0x2000
                                tmp = int(self.r.AX / self.r.DI)
                                self.r.DX = self.r.AX % self.r.DI
                                self.r.AX = tmp
                                self.r.AX <<= 1
                                self.r.AX += 1
                            self.r.DI = 2  # bc5, check here
                            self.r.DX = 0
                            tmp = int(self.r.AX / self.r.DI)
                            self.r.DX = self.r.AX % self.r.DI
                            self.r.AX = tmp

                            self.r.DI = self.r.DX
                            self.r.DI += self.ruler_color
                            self.r.DX = self.r.Pop()
                            if self.r.BX != self.r.DX:
                                # self.r.Push(self.r.CS)#bd7
                                self.func_C03()
                                while True:
                                    self.r.BX += 1
                                    if self.r.BX != self.r.DX:
                                        self.r.AL = self.DS_BUF[self.r.DI]  # be5，3712:3b36=81
                                        self.display_buf[self.r.BX] = self.r.AL
                                        self.map[self.r.BX] = self.r.AL
                                        print("Main -> {0}:{1}".format(self.r.BX, self.r.AL))
                                    else:
                                        break
                            self.r.CH = self.r.CL  # bfa
                            self.func_C03()
                            # jmp b8a

                    if break_to_a77 is True:
                        break

            if break_to_a77 is True:
                break_to_a77 = False

    def rcl(self, num: int, carry_flag):
        buf = "{0:08b}".format(num)
        carry = buf[0]
        num_new = buf[1:] + carry_flag
        return int(num_new, 2), carry

    def rcr(self, num: int, carry_flag):
        buf = "{0:08b}".format(num)
        carry = buf[-1]
        num_new = str(carry_flag) + buf[0:-1]
        return int(num_new, 2), carry

    def rol(self, num: int):
        buf = "{0:08b}".format(num)
        carry = buf[0]
        num_new = buf[1:] + buf[0]
        return int(num_new, 2), carry

    def ror(self, num: int):
        buf = "{0:08b}".format(num)
        carry = buf[-1]
        num_new = buf[-1] + buf[0:-1]
        return int(num_new, 2), carry

    def func_A1E(self):
        if ((self.r.BX & 0x0f) != 0x00):
            return False
        else:
            self.r.AX = self.r.BX  # a25
            self.r.Push(self.r.BX)
            if self.r.AX >= 0x2000:
                self.r.AX -= 0x2000

            self.r.BL = 0x50
            tmp = int(self.r.AX / self.r.BL)
            self.r.AH = self.r.AX % self.r.BL
            self.r.AL = tmp

            self.r.BX = self.r.Pop()
            self.r.AH |= self.r.AH
            return self.r.AH == 0

    def func_A38(self):
        # self.r.Push(self.r.CS)
        self.func_C28()
        self.r.AL |= self.r.DH
        if self.r.AL != 0xFF:
            self.r.CH = 0x80  # a43

            while True:
                self.r.AL, carry = self.rcl(self.r.AL, "0")  # a45, always "CLC" before RCL
                if carry == "0":
                    if ((self.r.CL & 0x01) == 0x01):
                        # self.r.Push(self.r.CS) #a50
                        self.r.DI = 0x340b
                        self.func_9XX()
                        self.r.CL &= 0xFE
                    self.r.AL |= self.r.AL  # a57
                    if self.r.AL != 0:
                        self.r.CH, carry = self.rcr(self.r.CH, "1")  # a5c
                        if carry == "0":
                            # jmp a45
                            continue
                    return
                else:
                    self.r.CL |= 0x01  # a62
                    self.r.CH, carry = self.rcr(self.r.CH, "1")  # a5c
                    if carry == "0":
                        # jmp a45
                        continue
                    return


        else:
            self.r.CL |= 1  # a67
            return

    def func_c4B(self):
        self.r.Push(self.r.DS)
        self.r.Push(self.r.DX)
        self.r.Push(self.r.AX)
        self.r.DH = self.r.AL
        self.r.AL = 0xFF - self.r.AL
        self.r.DL = self.r.AL
        self.map[self.r.DI] &= self.r.DL
        self.r.AX = self.r.Pop()
        self.r.DX = self.r.Pop()
        self.r.DS = self.r.Pop()
        return

    def ReadDSBufferWord(self, offset):
        return self.DS_BUF[offset + 1] * 256 + self.DS_BUF[offset]

    def WriteDSBufferWord(self, value, offset):
        self.DS_BUF[offset] = value % 256
        self.DS_BUF[offset + 1] = int(value / 256)
        return

    def func_9XX(self):
        self.r.SI = self.ReadDSBufferWord(self.r.DI + 4)
        self.r.SI -= 2
        self.WriteDSBufferWord(self.r.BX, self.r.SI)
        self.r.SI -= 1
        self.DS_BUF[self.r.SI] = self.r.CH
        if self.r.SI <= self.ReadDSBufferWord(self.r.DI):
            self.r.SI = self.ReadDSBufferWord(self.r.DI + 2)
        if self.r.SI == self.ReadDSBufferWord(self.r.DI + 6):
            self.exit()
            return
        # 9fd
        self.WriteDSBufferWord(self.r.SI, self.r.DI + 4)

    def exit(self):
        self.r.AX = 0xFFFF
        self.SP = self.DS_BUF[0x3415]
        self.r.DI = self.r.Pop()
        self.r.SI = self.r.Pop()
        self.r.ES = self.r.Pop()
        self.r.BP = self.r.Pop()

    def func_A0X(self):
        self.r.SI = self.ReadDSBufferWord(self.r.DI + 6)
        self.r.SI -= 2
        self.r.BX = self.ReadDSBufferWord(self.r.SI)
        self.r.SI -= 1
        self.r.CH = self.DS_BUF[self.r.SI]
        if self.r.SI <= self.ReadDSBufferWord(self.r.DI):
            self.r.SI = self.ReadDSBufferWord(self.r.DI + 2)
        self.WriteDSBufferWord(self.r.SI, self.r.DI + 6)

        return

    def func_C03(self):
        self.r.AH = self.r.CH
        self.r.AH = 0xFF - self.r.AH
        self.r.AL = self.DS_BUF[self.r.DI]
        self.r.AL &= self.r.CH
        self.display_buf[self.r.BX] &= self.r.AH
        self.display_buf[self.r.BX] |= self.r.AL
        print("C03 -> {0}:{1}".format(self.r.BX, self.r.AL))
        self.map[self.r.BX] &= self.r.AH
        self.map[self.r.BX] |= self.r.AL

        return

    def func_C28(self):
        # self.r.AL = self.map[self.r.BX]
        self.display_buf[self.r.BX] &= self.map[self.r.BX]
        print("C28 -> {0}:{1}".format(self.r.BX, self.map[self.r.BX]))
        self.r.AL = 0xFF - self.map[self.r.BX]
        return


# def get_rgb(b):
#     if b == 0:
#         return 0, 0, 0
#     else:
#         return 0xff, 0xff, 0xf8
#
# def save(buf):
#     with open("map.save","wb") as f:
#         f.write(bytes(buf))
#
# def show(map_buf):
#     data = map_buf
#     width = 640
#     height = 200
#     size = 16384
#     size2 = int(size / 2)
#     bmp = pygame.Surface((width, height))
#
#     for k in range(0, 2):
#         for i in range(0, size2):
#             row = int(i / int(width / 8)) * 2 + k
#             if size2 * k + i >= len(data):
#                 continue
#             b = data[size2 * k + i]
#
#             col = i % int(width / 8)
#             for j in range(0, 8):
#                 b2 = (b & (0x80 >> j)) >> (7 - j)
#                 bmp.set_at((8 * col + j, row), get_rgb(b2))
#
#     return bmp
#
# def main():
#     with open("../../Resources/abcdef", "rb") as f:
#         buf = bytes(f.read())
#     with open("../fullmap.dat", "rb") as f:
#         map_buf = list(f.read())
#     bmp = show(map_buf)
#     bmp = pygame.transform.scale(bmp, (bmp.get_width() * 2, bmp.get_height() * 2))
#     pygame.image.save(bmp, "fullmap.png")
#
#     # d = DrawMapLines([], 0x108, 0x37, 0x3b5a)
#     # d.Start()
#     #
#     # img = show(d.display_buf)
#     # #img = pygame.transform.scale(img,(img.get_width(),img.get_height()*1))
#     # pygame.image.save(img,"1.png")
#     #
#     #
#     #
#     # for mmm in range(0, len(map_buf)):
#     #     map_buf[mmm] ^= d.display_buf[mmm]
#     # bmp = show(map_buf)
#     # pygame.image.save(bmp, "mergedmap.png")
#     #
#     # save(d.display_buf)
#     all = pygame.Surface((640, 256))
#     tmp_buf = [0] * 0x4000 #不用上面的map原图，只用下面这个，则会得到该省的单独的上色的地图
#
#     for p in range(0, 41):
#         p1 = buf[0x2d8c + 0x23 * p + 0x1c] + buf[0x2d8c + 0x23 * p + 0x1d] * 256
#         p2 = buf[0x2d8c + 0x23 * p + 0x1e] + buf[0x2d8c + 0x23 * p + 0x1f] * 256
#
#         ruler_no = buf[0x2d8c + 0x23 * p + 0x10]
#         if ruler_no==0xff:
#             continue
#         ruler_color = buf[0x10+ruler_no]
#         ruler_color = ruler_color*6+0x3b30
#
#         d = DrawMapLines([], p1, p2,ruler_color)
#         d.Start()
#
#         for mmm in range(0, len(tmp_buf)):
#             tmp_buf[mmm] |= d.display_buf[mmm]
#
#         # bmp = show(map_buf)
#         bmp2 = show(d.display_buf)
#         bmp2 = pygame.transform.scale(bmp2, (bmp2.get_width() * 2, bmp2.get_height() * 2))
#         #pygame.image.save(bmp,"p{0}.png".format(p+1))
#         pygame.image.save(bmp2, "full_p{0}.png".format(p + 1))
#
#     tmp = show(tmp_buf)
#     tmp = pygame.transform.scale(tmp,(tmp.get_width()*2,tmp.get_height()*2))
#     pygame.image.save(tmp, "tmp.png")
#
#     with open("../fullmap.dat", "rb") as f:
#         map_buf = list(f.read())
#
#     for mmm in range(0, len(map_buf)):
#         map_buf[mmm] &= tmp_buf[mmm]
#     bmp = show(map_buf)
#     bmp = pygame.transform.scale(bmp,(bmp.get_width()*2,bmp.get_height()*2))
#
#     pygame.image.save(bmp, "mapand.png".format(p + 1))
#
#     with open("../fullmap.dat", "rb") as f:
#         map_buf = list(f.read())
#
#     for mmm in range(0, len(map_buf)):
#         map_buf[mmm] |= tmp_buf[mmm]
#     bmp = show(map_buf)
#     bmp = pygame.transform.scale(bmp, (bmp.get_width() * 2, bmp.get_height() * 2))
#     pygame.image.save(bmp, "mapor.png".format(p + 1))
#
#     with open("../fullmap.dat", "rb") as f:
#         map_buf = list(f.read())
#
#     for mmm in range(0, len(map_buf)):
#         map_buf[mmm] ^= tmp_buf[mmm]
#     bmp = show(map_buf)
#     bmp = pygame.transform.scale(bmp, (bmp.get_width() * 2, bmp.get_height() * 2))
#     pygame.image.save(bmp, "mapxor.png".format(p + 1))
#
# if __name__ == "__main__":
#     main()
