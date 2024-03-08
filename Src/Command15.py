import os.path

from Data import Data
import pygame,sys
from Helper import Helper,Province,Officer,Ruler

from Data import DelegateMode

class Command15(object):
    def __init__(self):
        pass

    def Start(self,province_no):
        bmp = pygame.Surface((330,160))
        bmp.fill((0,0,0))

        descriptions = Data.PROVINCE_DESC[Province.FromSequence(province_no).NameIndex]
        for i in range(0,len(descriptions)):
            img = Helper.DrawText(descriptions[i])
            bmp.blit(img,(10,30+30*i))

        start = 0x33b9 + Data.DATA_OFFSET + 156 * province_no
        map_data = Data.BUF[start:start + 12 * 13]

        x = 210
        y = 30
        start = 0
        for r in range(0, 12):
            for c in range(0, 13):
                fname = Data.GamePath+"hex{0:02}.jpg".format(map_data[start])
                img = pygame.image.load(fname)
                img = pygame.transform.scale(img, (8,8))
                bmp.blit(img,(x + c * 8, y + r * 8 + (c % 2) * 4))

                start += 1

        x = 220
        y = 0
        neighbors = Helper.GetNeighbors(province_no)
        for i in range(0,6):
            p = neighbors[i]
            if p>0 and p<256:
                img = Helper.DrawText(str(p),palette_no=3)
                bmp.blit(img, (x+40*(i%3),y+130*(1-int(i/3))))

        bmp = pygame.transform.scale(bmp,(bmp.get_width()*Helper.Scale,bmp.get_height()*Helper.Scale))
        Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))

        Helper.ClearInputArea()
        img = Helper.DrawText(Helper.GetBuiltinText(0x8394))
        Helper.Screen.blit(img, (300 * Helper.Scale, 295 * Helper.Scale))
        pygame.display.flip()

        Helper.GetInput(Helper.GetBuiltinText(0x8394))
