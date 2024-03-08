import os.path

from Data import Data
import pygame, sys
from Helper import Helper, Province, Officer, Ruler
from Data import DelegateMode


class Command16(object):
    def __init__(self):
        pass

    def Start(self, province_no):
        ruler_no = Province.FromSequence(province_no).RulerNo
        province_list = Province.GetListByRulerNo(ruler_no)

        if len(province_list) == 1:
            Helper.ShowDelayedText(Helper.GetBuiltinText(0x8492))
            pygame.time.wait(1000)

            return

        while True:
            Helper.ClearInputArea()

            province_no = Helper.GetInput(Helper.GetBuiltinText(0x84A5) + "(1-41)? ", required_number_min=1,
                                          required_number_max=41)
            if province_no == -1:
                return

            if Province.IsRuledByCurrentRuler(province_no) is False:
                continue

            Helper.ClearInputArea()
            tmp = Helper.GetBuiltinText(0x84C4)
            text = tmp.replace("%2d", "{0}").replace("@C6@%s@C7@_", "").format(province_no)
            p_status = Province.GetDelegateStatus(province_no)
            if p_status != DelegateMode.No:
                status = Helper.GetBuiltinText(0x84B6)
            else:
                status = Helper.GetBuiltinText(0x84BB)
            img = Helper.DrawText(text, scaled=True)
            Helper.Screen.blit(img, (300 * Helper.Scale, 295 * Helper.Scale))
            img2 = Helper.DrawText(status, palette_no=3, scaled=True)
            Helper.Screen.blit(img2, ((300 + img.get_width() / Helper.Scale + 3) * Helper.Scale, 295 * Helper.Scale))
            pygame.display.flip()

            tmp = Helper.GetBuiltinText(0x84DB).split("_")
            action = Helper.GetInput(tmp[0], next_prompt=tmp[1] + "(1-2)? ", row=1, cursor_user_prompt_location=True,
                                     required_number_min=1, required_number_max=2)
            if action == -1:
                continue
            if action == 2:
                if p_status == DelegateMode.No:
                    continue
                else:
                    Data.BUF[Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE + 0x12] = 0
                    Helper.ShowDelayedText(Helper.GetBuiltinText(0x8502).replace("%2d", str(province_no)))
                    continue

            # delegate
            commands = [Helper.GetBuiltinText(0x83E9), Helper.GetBuiltinText(0x83F2), Helper.GetBuiltinText(0x83F8),
                        Helper.GetBuiltinText(0x83Fd)]

            while True:
                Helper.ShowCommandsInInputArea(commands, 2, palette_no=3, width=150)
                strategy = Helper.GetInput(Helper.GetBuiltinText(0x842D) + "(1-4)? ", row=2, required_number_min=1,
                                           required_number_max=4)
                if strategy == -1:
                    break

                Helper.ClearInputArea()
                yn = Helper.GetInput(Helper.GetBuiltinText(0x83CA) + "(Y/N)? ", yesno=True)
                send_province = -1
                if yn == "y":
                    while True:
                        Helper.ClearInputArea()
                        send_province = Helper.GetInput(Helper.GetBuiltinText(0x83DB) + "(1-41)? ",
                                                        required_number_min=1, required_number_max=41)
                        if (Province.Is2ProvincesBelongToSameRuler(province_no,
                                                                   send_province) is True and send_province != province_no) or (
                                send_province == -1):
                            break

                Helper.ClearInputArea()
                yn = Helper.GetInput(Helper.GetBuiltinText(0x83B2) + "(Y/N)? ", yesno=True)
                war_province = -1
                if yn == "y":
                    while True:
                        Helper.ClearInputArea()
                        war_province = Helper.GetInput(Helper.GetBuiltinText(0x83BF) + "(1-41)? ",
                                                       required_number_min=1, required_number_max=41)
                        neighbors = Helper.GetNeighbors(province_no)
                        if war_province == -1 or war_province in neighbors:
                            break

                Helper.ClearInputArea()

                img = Helper.DrawText(Helper.GetBuiltinText(0x843C, 0x8444), scaled=True)
                Helper.Screen.blit(img, (300 * Helper.Scale, 295 * Helper.Scale))

                img2 = Helper.DrawText(commands[strategy - 1], scaled=True, palette_no=3)
                Helper.Screen.blit(img2, ((300 + img.get_width() / Helper.Scale) * Helper.Scale, 295 * Helper.Scale))

                img = Helper.DrawText(Helper.GetBuiltinText(0x8450, 0x8456), scaled=True)
                Helper.Screen.blit(img, (300 * Helper.Scale, 325 * Helper.Scale))
                if send_province == -1:
                    img2 = Helper.DrawText(Helper.GetBuiltinText(0x845C), scaled=True, palette_no=1)
                else:
                    img2 = Helper.DrawText(Helper.GetBuiltinText(0x8460).replace("%2d", str(send_province)),
                                           scaled=True, palette_no=1)
                Helper.Screen.blit(img2, ((300 + img.get_width() / Helper.Scale) * Helper.Scale, 328 * Helper.Scale))

                img = Helper.DrawText(Helper.GetBuiltinText(0x8472, 0x8478), scaled=True)
                Helper.Screen.blit(img, (450 * Helper.Scale, 325 * Helper.Scale))
                if war_province == -1:
                    img2 = Helper.DrawText(Helper.GetBuiltinText(0x845C), scaled=True, palette_no=2)
                else:
                    img2 = Helper.DrawText(Helper.GetBuiltinText(0x8460).replace("%2d", str(war_province)), scaled=True,
                                           palette_no=2)
                Helper.Screen.blit(img2, ((450 + img.get_width() / Helper.Scale) * Helper.Scale, 325 * Helper.Scale))

                yn = Helper.GetInput(Helper.GetBuiltinText(0x3D7D) + "(Y/N)? ", row=2, yesno=True)
                if yn == "y":
                    Data.BUF[Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE + 0x12] = strategy + 0x04
                    if send_province != -1:
                        Data.BUF[
                            Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE + 0x14] = send_province - 1
                    if war_province != -1:
                        Data.BUF[
                            Data.PROVINCE_START + (province_no - 1) * Data.PROVINCE_SIZE + 0x15] = war_province - 1

                    break
