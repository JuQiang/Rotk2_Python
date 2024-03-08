import random

import pygame.display

from Helper import Helper, Province, Officer, Ruler
from Command1 import Command1
from Command2 import Command2
from Command3 import Command3
from Command4 import Command4
from Command5 import Command5
from Command8 import Command8
from Command9_10_12 import Command9, Command10, Command12
from Command11 import Command11
from Command13 import Command13
from Command14 import Command14
from Command15 import Command15
from Command16 import Command16
from Command18 import Command18
from Command19 import Command19
from Data import Data
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
            if i >= len(msg):
                break

            b = msg[i]
            if b == 0:
                text = ''.join(buf2)
                if len(text) > 0:
                    buf.append(text)
                    print(text)
                    img = Helper.DrawText(text, scaled=True)
                    pygame.image.save(img, "images/{0}.png".format((hex(start)[2:]).upper()))
                buf2 = []
                i += 1
                start = i
            elif b == 0x0a:
                buf2.append("_")
                i += 1
            elif b < 0x20:
                buf2.append(".")
                i += 1
            elif b == 0x24:
                buf2.append(".")
                i += 1
            elif b < 0x80:
                buf2.append(chr(b))
                i += 1
            elif b >= 0x80:
                b2 = msg[i + 1]
                zh_cn = Data.CNINDEX.get(b * 256 + b2)
                if zh_cn is not None:
                    buf2.append("$")
                    buf2.append(str(zh_cn))
                    i += 2
                    buf2.append("$")
                else:
                    i += 1
            else:
                i += 1
                continue

    def __init__(self):
        Helper.Init(2, 4)

        self.mappings = {-1: None, 1: Command1(), 2: Command2(), 3: Command3(), 4: Command4(), 5: Command5(),
                         8: Command8(), 9: Command9(), 10: Command10(), 11: Command11(), 12: Command12(),
                         13: Command13(), 14: Command14(), 15: Command15(), 16: Command16(), 18: Command18(),
                         19: Command19()}
        self.map_command_switch = True

    def switch_map_command(self):
        if self.map_command_switch is True:
            Helper.ShowMap(Province.GetActiveNo())
        else:
            bmp = self.GetAll20Commands()
            Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))
            pygame.display.flip()

        self.map_command_switch = not self.map_command_switch

    def get_palettes(self):
        with open("palettes", "rb") as f:
            palettes = f.read()
            for i in range(0, 4):
                p = palettes[48 * i:48 * (i + 1)]

                bmp = pygame.Surface((60, 60))

                for j in range(0, 16):
                    p2 = p[3 * j:3 * (j + 1)]

                    bmp.fill((p2[0], p2[1], p2[2]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 1))

                    bmp.fill((p2[0], p2[2], p2[1]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 2))

                    bmp.fill((p2[1], p2[0], p2[2]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 3))

                    bmp.fill((p2[1], p2[2], p2[0]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 4))

                    bmp.fill((p2[2], p2[0], p2[1]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 5))

                    bmp.fill((p2[2], p2[1], p2[0]))
                    pygame.image.save(bmp, "./调色板{0}/变化{2}/序号{1}.png".format(i + 1, j + 1, 6))

    def validate_helper_palettes(self):
        for i in range(0, 16):
            bmp = pygame.Surface((60, 60))
            bmp.fill(Helper.RulerPalettes[i])
            pygame.image.save(bmp, "palette_{0}.png".format(i))

    def Start(self):
        # self.get_fonts()
        # self.get_palettes()
        # self.validate_helper_palettes()
        splash = Open()
        splash.Start()

        main = MainMenu()
        ret = main.Start()

        if ret == -1:
            return

        Helper.MainMap = Helper.GetMap()

        # Helper.ShowMap(Province.GetActiveNo())

        while True:
            cmd = Helper.GetBuiltinText(0x5CEB).replace("%d-%d", "0-19").replace("%d", str(Province.GetActiveNo()))
            gov_off = Province.FromSequence(Province.GetActiveNo()).GovernorOffset
            prompt = cmd.replace("%s", Officer.FromOffset(gov_off).GetName())

            self.switch_map_command()
            Helper.ClearInputArea()
            input = Helper.GetInput(prompt, 300, 295, "", required_number_min=0, required_number_max=19,
                                    allow_enter_exit=True)

            if input > -1:
                cmd = self.mappings.get(input)
                if cmd is None:
                    Helper.ShowDelayedText("$685$$545$$97$$854$$825$!")
                    continue
                ret = cmd.Start(Province.GetActiveNo())
                self.map_command_switch = True
                if ret == -1:
                    return

    def GetAll20Commands(self):
        bmp = pygame.Surface((330, 160))
        bmp.fill((0, 0, 0))

        top = 5
        left = 5

        for i in range(0, 20):
            cmd_no = i

            row = cmd_no % 4
            col = int(cmd_no / 4)

            cmd_bmp = Helper.DrawText(Helper.GetBuiltinText(0x609d + cmd_no * 5), back_color=(0, 0, 0),
                                      palette_no=7)
            num_bmp = Helper.DrawText("{0:2}.".format(cmd_no), (0, 0, 0), 3, scaled=False)

            bmp.blit(num_bmp, (left + 65 * (col + 0) + (24 - num_bmp.get_width()), top + 38 * row))
            bmp.blit(cmd_bmp, (left + 65 * col + 24, top + 38 * row))

        return pygame.transform.scale(bmp,
                                      (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))


def main():
    kdf = KeyboardDrivenFramework()
    # kdf.generate_images()
    kdf.Start()


if __name__ == "__main__":
    main()
