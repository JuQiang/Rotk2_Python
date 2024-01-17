from Src.UI.DrawCGA import DrawCGA
from Src.Data import Data
import pygame
import datetime
import time
from Src.RoTK2 import RoTK2
from Src.Data import ShowOfficerFlag
from Src.Officer import Officer

class Draw(object):
    def __init__(self,scale):
        self.open_data = {
            0: ["logo1", 0x2976, 0x34, 0x38, 0x2940, 0x7b, 0x2976],
            0x2f8: ["logo2", 0x88, 0x32, 0x10, 0x2a80, 0x7b, 0x2ab8],
            0x4ca: ["logo3", 0x58, 0x60, 0x10, 0x1b80, 0x7b, 0x1ba2],
            0x88b: ["logo4", 0x40, 0x24, 0x20, 0x1400, 0x7b, 0x1438],
            0xa51: ["logo5", 0x5e, 0x9c, 0x18, 0x1d60, 0x7b, 0x1d60],
            # 0x8755: ["logo5_2", 0x5e, 0x9c, 0x18, 0x1d60, 0x7b, 0x1d60],
            0xc655: ["logo7", 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            0xeeb2: ["logo8", 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            0x11865: ["logo9", 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            0x14637: ["logo10", 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            0x171e3: ["logo11", 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            0x1ABBF: ["logo12", 0x32, 0x8c, 0x5b, 0xfa0, 0x7b, 0xfaa],
        }

        self.RulerPalettes = [
            pygame.color.Color(0x80, 0x80, 0x80), pygame.color.Color(0xff, 0xff, 0x00),
            pygame.color.Color(0xff, 0xda, 0x89), pygame.color.Color(0x8a, 0x2b, 0xe2),
            pygame.color.Color(0xff, 0x69, 0xb4), pygame.color.Color(0x06, 0x52, 0x79),
            pygame.color.Color(0x00, 0x80, 0x00), pygame.color.Color(0x87, 0xce, 0xfa),

            pygame.color.Color(0xad, 0xd8, 0xe6), pygame.color.Color(0x00, 0x00, 0xff),
            pygame.color.Color(0xff, 0x00, 0x00), pygame.color.Color(0x94, 0x00, 0xd3),
            pygame.color.Color(0xbc, 0x8f, 0x8f), pygame.color.Color(0x80, 0x80, 0x80),
            pygame.color.Color(0x00, 0x64, 0x00), pygame.color.Color(0xff, 0xa5, 0x00)]


        self.palettes = [pygame.color.Color(0,0,0), pygame.color.Color(0x50,0xff,0x50),pygame.color.Color(0xff,0x50,0x50),pygame.color.Color(0xff,0xff,0x50),
                         pygame.color.Color(0x50,0x50,0xf8), pygame.color.Color(0x50,0xff,0xf8), pygame.color.Color(0xff,0x50,0xf8), pygame.color.Color(0xff,0xff,0xf8)]

        self.scale = scale
        #self.MainMap = self.GetMap()

    def log(self,msg):
        now = datetime.datetime.now()
        micro_second = int(now.microsecond / 1000)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + f'. {micro_second:03d}'
        print("{0} : {1}".format(current_time, msg))

    def get_rgb(self,b,palette_no):
        if b == 0:
            return 0, 0, 0
        else:
            return self.palettes[palette_no].r,self.palettes[palette_no].g,self.palettes[palette_no].b


    def DrawData(self, data, palette_no)->pygame.Surface:
        ori_width = (Data.GRPDATA[1] << 8) + Data.GRPDATA[0]
        ori_height = (Data.GRPDATA[3] << 8) + Data.GRPDATA[2]

        width = 640
        height = 200
        size = 16384
        size2 = int(size / 2)
        bmp = pygame.Surface((width,height))

        for k in range(0, 2):
            for i in range(0, size2):
                row = int(i / int(width / 8)) * 2 + k
                if size2 * k + i >= len(data):
                    continue
                b = data[size2 * k + i]

                col = i % int(width / 8)
                for j in range(0, 8):
                    b2 = (b & (0x80 >> j)) >> (7 - j)
                    bmp.set_at((8 * col + j,row),self.get_rgb(b2, palette_no))

        return pygame.transform.scale(bmp,(width,height*2))
        return pygame.transform.scale2x(bmp)


    def GetBackgroundText(self)->pygame.Surface:
        bmp = pygame.Surface((640, 0x1b8))
        bmp.fill((0, 0, 0))

        x = 0
        y = 0
        buf = Data.OPENING[0x4975:0x4975 + 0x3de0]
        rows = 0x1b8
        cols = 0x24
        for i in range(0, rows):
            for j in range(0, cols):
                b = buf[cols * i + j]
                for k in range(0, 8):
                    if (b & (0x80 >> k)):
                        bmp.set_at((x + 8 * j + k, y + i),(255,255,255))

            x = 0
        return pygame.transform.scale(bmp,(bmp.get_width()*self.scale,bmp.get_height()*self.scale))

    def GetGraphData(self,key)->pygame.Surface:
        grp = Data.GrpdataMappings.get(key)
        if grp is None:
            raise Exception("Invalid key :"+key)

        dc = DrawCGA(grp,Data.GRPDATA[grp[0]:grp[0]+0x4000])
        dc.Start()

        bmp = self.DrawData(dc.display_buf, 7)
        return pygame.transform.scale(bmp,(bmp.get_width()*self.scale,bmp.get_height()*self.scale))

    def DrawCharacterInternal(self, w, back_color, palette_no):
        # list = "!().0123456789?-:, "
        # index = -1
        # for i in range(0,len(list)):
        #     if list[i]==w:
        #         index = i
        #         break
        # if index==-1:
        #     raise Exception("Character not found!")
        #
        # one = Data.CHARACTER[336*index:336*(index+1)]
        # bmp = pygame.image.frombytes(bytes(one),(8,14),"RGB")
        # for h in range(0,bmp.get_height()):
        #     for w in range(0,bmp.get_width()):
        #         b = bmp.get_at((w,h))
        #         if b.r==0 and b.g==0 and b.b==0:
        #             bmp.set_at((w,h),(back_color[0],back_color[1],back_color[2]))
        #         else:
        #             b.r = self.palettes[palette_no].r
        #             b.g = self.palettes[palette_no].g
        #             b.b = self.palettes[palette_no].b
        #             bmp.set_at((w, h), (b.r, b.g,b.b))
        #
        # return bmp
        #fname = "arialnarrow"
        fname = "inaimathimn"
        # fname="timesnewroman"
        #fname = "dincondensed"
        f = pygame.font.SysFont(fname, 24)
        bmp = f.render(w, True, self.palettes[palette_no], back_color)
        #pygame.image.save(bmp, w + ".png")
        if bmp.get_width()==11 and bmp.get_height()==30:
            bmp = bmp.subsurface((1,7,9,14)).copy()
        #pygame.image.save(bmp,w+".png")
        return pygame.transform.scale(bmp,(8,14))

    def DrawWordInternal(self,index,back_color,palette_no):
        x = 0
        bmp = pygame.Surface((16,14))
        bmp.fill(back_color)

        index2 = 30 * int(str(index).strip()) + 2
        one = Data.MSG16P[index2:index2 + 30]

        for i in range(0, 14):
            left = one[2 * i]
            right = one[2 * i + 1]

            for j in range(0, 8):
                if (left & (0x80 >> j)):
                    bmp.set_at((x + j, 0 + i), self.palettes[palette_no])
                if (right & (0x80 >> j)):
                    bmp.set_at((x + j + 8, 0 + i), self.palettes[palette_no])

        return bmp

    def DrawText(self, text,back_color=(0,0,0), palette_no=7, scaled=True):
        buf = []
        i=0
        # every element which starts with $ and ends with $, will DrawWord by piexles
        # other elements will DrawText .
        while True:
            if i>=len(text):
                break

            if text[i]=="$":
                name = []
                while True:
                    i +=1
                    if i>=len(text) or text[i]=="$":
                        break

                    name.append(text[i])
                buf.append(self.DrawWordInternal(int(''.join(name)),back_color,palette_no))
                i+=1
            else:
                buf.append(self.DrawCharacterInternal(text[i], back_color, palette_no))
                i+=1

        width = 0
        for i in range(0,len(buf)):
            width += buf[i].get_width()

        bmp = pygame.Surface((width, 14))
        bmp.fill(back_color)

        pos = 0
        for b in buf:
            bmp.blit(b,(pos,0))
            pos+= b.get_width()

        scale_value = 1
        if scaled==True:
            scale_value = self.scale

        return pygame.transform.scale(bmp,(bmp.get_width()*scale_value*1.0,bmp.get_height()*scale_value*2.0))


    def Get_Stored_Fonts_Picture(self):
        fonts = pygame.font.get_fonts()
        bmp_list = []
        index = 0
        for fname in fonts:
            f = pygame.font.SysFont(fname, 18)
            bmp_list.append(f.render(fname + ":     0123456789", True, (255, 255, 255), (0, 0, 0)))
            index += 1
        width = 0
        for bmp in bmp_list:
            width += bmp.get_width()
        bmp = pygame.Surface((600, 8000))
        width = 0
        height = 0
        index = 0
        for b in bmp_list:
            bmp.blit(b, (width, height))

            index += 1
            if index % 2 == 1:
                width = 300
            else:
                width = 0
                height += 20
        #pygame.image.save(bmp, "number_fonts.png")

    def GetGenericFace(self,index):
        info = "{0:b}".format(index).zfill(16)
        wenxu = int(info[0:3],2)#100武将，110文官
        kou = int(info[3:5],2)
        bi = int(info[5:7],2)
        yan = int(info[7:9],2)
        shang = int(info[9:11],2)
        xia = int(info[11:13],2)
        group = int(info[13:16], 2)

        width = 64
        size = int(width*(18*4+22*4+8*4+10*4+8*4)*3/8)

        height_list = [18,22,8,10,8]
        face_data=[]
        face = Data.MONTAGE[group * size:group * size + size]

        pos = 0
        for h in height_list:
            for k in range(0,4):
                block_size = int(width*h*3/8)

                face_buf=[]
                for i in range(0, block_size, 3):
                    a = "{0:b}".format(face[i + 0+pos]).zfill(8)
                    b = "{0:b}".format(face[i + 1+pos]).zfill(8)
                    c = "{0:b}".format(face[i + 2+pos]).zfill(8)
                    for j in range(0, 8):
                        face_buf.append(int(a[j] + b[j] + c[j], 2))

                face_data.append(face_buf)
                pos += block_size

        img = pygame.Surface((64, 40))
        img.fill((0, 0, 0))
        pos_list = [shang,4+xia,8+kou,12+bi,16+yan]
        s = 0
        for i in range(0,18):
            for j in range(0, 64):
                true_color = self.palettes[face_data[shang][64 * i + j]]
                img.set_at((j, i), (true_color.r, true_color.g, true_color.b))

        for i in range(0,22):
            for j in range(0, 64):
                true_color = self.palettes[face_data[4+xia][64 * i + j]]
                img.set_at((j, i+18), (true_color.r,true_color.g, true_color.b))

        for i in range(0,8):
            for j in range(0, 64):
                true_color = self.palettes[face_data[8+yan][64 * i + j]]
                if true_color.r == 0 and true_color.g == 0 and true_color.b == 0:
                    continue
                img.set_at((j, i+10), (true_color.r, true_color.g, true_color.b))

        for i in range(0,8):
            for j in range(0, 64):
                true_color = self.palettes[face_data[16+bi][64 * i + j]]
                if true_color.r==0 and true_color.g==0 and true_color.b==0:
                    continue
                img.set_at((j, i+16), (true_color.r, true_color.g, true_color.b))

        for i in range(0,10):
            for j in range(0, 64):
                true_color = self.palettes[face_data[12+kou][64 * i + j]]
                if true_color.r == 0 and true_color.g == 0 and true_color.b == 0:
                    continue
                img.set_at((j, i+22), (true_color.r, true_color.g, true_color.b))

        return pygame.transform.scale(img,(64,80))

    def GetFace(self,index):
        if index<219:
            return self.GetSingleFace(index)
        else:
            return self.GetGenericFace(index+1)

    def GetSingleFace(self,index):
        face_buf = []

        face = Data.KAODATA[index * 960:index * 960 + 960]
        for i in range(0, len(face), 3):
            a = "{0:b}".format(face[i + 0]).zfill(8)
            b = "{0:b}".format(face[i + 1]).zfill(8)
            c = "{0:b}".format(face[i + 2]).zfill(8)
            for j in range(0, 8):
                face_buf.append(int(a[j] + b[j] + c[j], 2))

        # http://xycq.online/forum/redirect.php?tid=34607&goto=lastpost&highlight=
        # 上面link的描述严重错误！顺序是RBG，而不是BGR，更不是RGB！
        img = pygame.Surface((64, 40))
        img.fill((0, 0, 0))

        for i in range(0, 40):
            for j in range(0, 64):
                true_color = self.palettes[face_buf[64 * i + j]]
                img.set_at((j, i), (true_color.r, true_color.g, true_color.b))

        return pygame.transform.scale(img,(64,80))


    def NewGameSelectRuler(self,no,page,player_list):
        limit = [0x0c,0x0c,0x09,0x0b,0x05,0x05]
        bmp = pygame.Surface((336, 280))
        bmp.fill((0, 0, 0))

        ruler_list = RoTK2.GetRulerList()
        left = 30
        top = 20

        width = 64+2
        height = 80+2

        max_rulers = min(limit[no],6*(page+1))
        for i in range(6*page,max_rulers):
            border_coords = (
                (left+110*int(i%3),top+140*int(i%6/3)),
                (left+110*int(i%3)+width,top+140*int(i%6/3)),
                (left+110*int(i%3)+width,top+140*int(i%6/3)+height),
                (left+110*int(i%3),top+140*int(i%6/3)+height)
            )
            pygame.draw.lines(bmp,self.palettes[6],True,border_coords,1)

            if i!=limit[no]-1:
                face_bmp = self.GetFace(ruler_list[i].RulerSelf.Portrait)
                bmp.blit(face_bmp, (left+1+110*int((i%3)), top+1+140*int(i%6/3)))

            back_color = self.RulerPalettes[Data.BUF[0x48+i]]
            pygame.draw.rect(bmp,back_color,(left+2+110*int((i%3)),top+5+height+140*int(i%6/3),8*self.scale,14*self.scale))

            fname = "inaimathimn"
            f = pygame.font.SysFont(fname, 24)
            num = f.render(str(i+1), True, (0,0,0),back_color )
            if num.get_width() == 11 and num.get_height() == 30:
                num = num.subsurface((1, 7, 9, 14)).copy()
            num =  pygame.transform.scale(num, (8, 14*self.scale))
            bmp.blit(num,(left+6+110*int((i%3)),top+5+height+140*int(i%6/3)))

            if i!=limit[no]-1:
                name_indexes = RoTK2.GetOfficerName(ruler_list[i].RulerSelf.Offset)
            else:
                name_indexes = Helper.GetBuiltinText(0x5114)

            palette_no=7
            if i in player_list:
                palette_no = 4
            name_bmp = self.DrawText("{0}".format(name_indexes), scaled=False,palette_no=palette_no)
            bmp.blit(name_bmp, (left+20+110*int((i%3)),top+5+height+140*int(i%6/3)))

        return pygame.transform.scale(bmp,(bmp.get_width()*self.scale,bmp.get_height()*self.scale))