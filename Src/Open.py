import pygame
from Helper import Helper
from Data import Data
from DrawCGA import DrawCGA

class Open(object):
    def __init__(self):
        self.splash_index = 1
        self.Event_RefreshSplashScreen = pygame.USEREVENT + 1

        pygame.time.set_timer(self.Event_RefreshSplashScreen, 2000)

        self.open_data = {
            "logo1":[0,0xd8,0x42],
            "logo2":[0x2f8, 0xE1,0x88],
            "logo3":[0x4ca, 0x8a,0x58],
            "logo4":[0x88b, 0xe0,0x40],
            "logo5":[0xa51, 0x00,0x5E],
            # 0x8755: ["logo5_2", 0x5e, 0x9c, 0x18, 0x1d60, 0x7b, 0x1d60],
            "logo7":[0xc655,0x60,0x1c],# 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            "logo8":[0xeeb2,0x60,0x1c],# 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            "logo9":[0x11865,0x60,0x1c],# 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            "logo10": [0x14637,0x60,0x1c],# 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            "logo11":[0x171e3,0x60,0x1c],# 0x1c, 0x6e, 0x80, 0x8c0, 0x7b, 0x8d8],
            "logo12":[0x1ABBF,0x28,0x32],#] 0x32, 0x8c, 0x5b, 0xfa0, 0x7b, 0xfaa],
        }

    def Start(self):
        self.ShowSplashScreen()

        while True:
            for event in pygame.event.get():
                if event.type == self.Event_RefreshSplashScreen:
                    self.ShowSplashScreen()
                if event.type == pygame.KEYUP:
                    return

    def GetBackgroundText(self) -> pygame.Surface:
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
                        bmp.set_at((x + 8 * j + k, y + i), (255, 255, 255))

            x = 0
        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    def GetSplashScreen(self, keyname) -> pygame.Surface:
        mappings = self.open_data[keyname]
        dc = DrawCGA(mappings, Data.OPENING[mappings[0]:mappings[0] + 0x4000], True)
        dc.Start()

        img = Helper.DrawData(dc.display_buf, 7)
        #pygame.image.save(img,"logo_"+keyname+".png")
        return pygame.transform.scale(img, (img.get_width() * Helper.Scale, img.get_height() * Helper.Scale))

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
                    bmp.set_at((8 * col + j,row),Helper.get_rgb(b2, palette_no))

        return pygame.transform.scale(bmp,(width,height*2))

    def GetSplashText(self, splash_index)->pygame.Surface:
        bmp = pygame.Surface((640, 100))
        bmp.fill((0,0,0))
        x = 0
        y = 30
        height = 28

        text_array = Data.LOGOTEXT[splash_index - 7]
        for index in text_array:
            pos = 30*index+2
            one = Data.MSG16P[pos:pos+30]

            for i in range(0, int(height / 2)):
                left = one[2 * i]
                right = one[2 * i + 1]

                for j in range(0, 8):
                    if (left & (0x80 >> j)):
                        bmp.set_at((x + j, y + i),(255,255,255))
                    if (right & (0x80 >> j)):
                        bmp.set_at((x + j + 8, y + i),(255,255,255))

            x += 16

        return pygame.transform.scale(bmp,(bmp.get_width()*Helper.Scale,bmp.get_height()*Helper.Scale))

    def ShowSplashScreen(self):
        if self.splash_index > 12:
            self.splash_index = 1

        if self.splash_index==6:
            Helper.Screen.fill((0, 0, 0))
            pygame.display.flip()

            splash = self.GetBackgroundText()
            Helper.Screen.blit(splash, (200*Helper.Scale, 0))
            pygame.display.flip()
            self.splash_index += 1
            return

        splash = self.GetSplashScreen("logo{0}".format(self.splash_index))

        if splash is not None:
            if self.splash_index==1:
                Helper.Screen.fill((0,0,0))
                pygame.display.flip()
                Helper.Screen.blit(splash,(0,0))#-150*Helper.Scale))
            elif self.splash_index==2:
                splash = splash.subsurface(pygame.Rect(0,250*Helper.Scale,640*Helper.Scale,100*Helper.Scale))
                Helper.Screen.blit(splash,(0,250*Helper.Scale))
            elif self.splash_index==12:
                Helper.Screen.fill((255,255,255))
                pygame.display.flip()
                splash = splash.subsurface(pygame.Rect(50*Helper.Scale,100*Helper.Scale,550*Helper.Scale,170*Helper.Scale))
                Helper.Screen.blit(splash,(50*Helper.Scale,100*Helper.Scale))
            else:
                Helper.Screen.fill((0, 0, 0))
                pygame.display.flip()
                Helper.Screen.blit(splash, (0, 0))

            if self.splash_index>6 and self.splash_index<12:
                splash_text = self.GetSplashText(self.splash_index)
                Helper.Screen.blit(splash_text,(100*Helper.Scale,300*Helper.Scale))

            pygame.display.flip()

        self.splash_index += 1