import pygame, sys
from Data import Data, ShowOfficerFlag, Officer
from Src.UI.DrawCGA import DrawCGA
from Src.UI.DrawMapLines import DrawMapLines
from RoTK2 import RoTK2
from collections.abc import Mapping, Sequence
import random


class ColorText(object):
    text: str
    back_color: int = 0
    fore_color: int = 7


class Helper(object):
    Scale = 1.0

    @staticmethod
    def Init(scale, current_province_no):
        pygame.init()

        Helper.Screen = pygame.display.set_mode((640 * scale, 400 * scale))
        Helper.Event_CursorShining = pygame.USEREVENT + 1
        pygame.display.set_caption("三國誌2")

        Helper.Scale = scale
        Helper.Palettes = [pygame.color.Color(0, 0, 0), pygame.color.Color(0x50, 0xff, 0x50),
                           pygame.color.Color(0xff, 0x50, 0x50), pygame.color.Color(0xff, 0xff, 0x50),
                           pygame.color.Color(0x50, 0x50, 0xf8), pygame.color.Color(0x50, 0xff, 0xf8),
                           pygame.color.Color(0xff, 0x50, 0xf8), pygame.color.Color(0xff, 0xff, 0xf8)]

        Helper.RulerPalettes = [
            pygame.color.Color(0x80, 0x80, 0x80), pygame.color.Color(0xff, 0xff, 0x00),
            pygame.color.Color(0xff, 0xda, 0x89), pygame.color.Color(0x8a, 0x2b, 0xe2),
            pygame.color.Color(0xff, 0x69, 0xb4), pygame.color.Color(0x06, 0x52, 0x79),
            pygame.color.Color(0x00, 0x80, 0x00), pygame.color.Color(0x87, 0xce, 0xfa),

            pygame.color.Color(0xad, 0xd8, 0xe6), pygame.color.Color(0x00, 0x00, 0xff),
            pygame.color.Color(0xff, 0x00, 0x00), pygame.color.Color(0x94, 0x00, 0xd3),
            pygame.color.Color(0xbc, 0x8f, 0x8f), pygame.color.Color(0x80, 0x80, 0x80),
            pygame.color.Color(0x00, 0x64, 0x00), pygame.color.Color(0xff, 0xa5, 0x00)]

        Helper.head_picture = None
        Helper.cur_flag = True

        Helper.CurrentProvinceNo = current_province_no

    @staticmethod
    def GetCurrentProvinceNo():
        province_offset = Data.BUF[0x3363 + Data.OFFSET] * 256 + Data.BUF[0x3362 + Data.OFFSET]
        Helper.CurrentProvinceNo = int((province_offset - Data.PROVINCE_OFFSET) / Data.PROVINCE_SIZE) + 1

    @staticmethod
    def ClearInputArea(row=0):
        if row == 0:
            bmp = pygame.Surface((330, 90))
            bmp.fill((0, 0, 0))
            Helper.Screen.blit(
                pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)),
                (300 * Helper.Scale, 298 * Helper.Scale))
        elif row in [1, 2, 3]:
            bmp = pygame.Surface((330, 30))
            bmp.fill((0, 0, 0))
            Helper.Screen.blit(
                pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)),
                (300 * Helper.Scale, (298 + 30 * row) * Helper.Scale))
        else:
            raise Exception("Invalid input area row.")

        pygame.display.flip()

    @staticmethod
    def get_rgb(b, palette_no):
        if b == 0:
            return 0, 0, 0
        else:
            return Helper.Palettes[palette_no].r, Helper.Palettes[palette_no].g, Helper.Palettes[palette_no].b

    @staticmethod
    def get_ruler_rgb(b, palette_no):
        if b == 0:
            return 0, 0, 0
        else:
            return Helper.RulerPalettes[palette_no].r, Helper.RulerPalettes[palette_no].g, Helper.RulerPalettes[
                palette_no].b

    @staticmethod
    def GetInput(prompt: str, x=300, y=300, next_prompt="", row=0, width=300, cursor_user_prompt_location=False,
                 palette_no=7, required_number=True, required_number_min=-1, required_number_max=-1,
                 allow_enter_exit=True, yesno=False, max_chars=8, keydown_mode=False):
        bmp = Helper.DrawText(prompt, scaled=True, palette_no=palette_no)
        pygame.draw.rect(Helper.Screen, (0, 0, 0),
                         (x * Helper.Scale, (y + 30 * row) * Helper.Scale, width * Helper.Scale, bmp.get_height()))
        Helper.Screen.blit(bmp, (x * Helper.Scale, (y + 30 * row) * Helper.Scale))
        cursor_x = bmp.get_width() + x * Helper.Scale
        cursor_y = (y + 30 * row) * Helper.Scale

        if len(next_prompt.strip()) > 0:
            bmp = Helper.DrawText(next_prompt, scaled=True)
            if cursor_user_prompt_location is True:
                cursor_x = bmp.get_width() + x * Helper.Scale
                cursor_y = (y + 30 * (row + 1)) * Helper.Scale

            pygame.draw.rect(Helper.Screen, (0, 0, 0), (
                x * Helper.Scale, (y + 30 * (row + 1)) * Helper.Scale, width * Helper.Scale, bmp.get_height()))
            Helper.Screen.blit(bmp, (x * Helper.Scale, (y + 30 * (row + 1)) * Helper.Scale))

        pygame.display.flip()

        input = []

        pygame.time.set_timer(Helper.Event_CursorShining, 300)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == Helper.Event_CursorShining:
                    Helper.CursorShining(''.join(input), cursor_x, cursor_y)
                if event.type == pygame.KEYDOWN and keydown_mode is True:
                    return Helper.GetChar(event.key).lower().strip()
                if event.type == pygame.KEYUP:
                    if keydown_mode is True:
                        continue

                    if yesno is True:
                        input.append(Helper.GetChar(event.key))
                        ret = ''.join(input).lower().strip()
                        if ret == 'y':
                            return 'y'
                        if ret in ['', 'n']:
                            return ''
                    if event.key == pygame.K_RETURN:
                        ret = ''.join(input).lower().strip()

                        if required_number is False and len(ret) > 0:
                            return ret

                        if allow_enter_exit is True and len(ret) == 0:
                            return -1

                        if ret.isdigit() is False:
                            input = []
                            continue

                        ret = int(ret)
                        if ret < required_number_min or ret > required_number_max:
                            input = []
                            continue

                        return ret
                    if event.key == pygame.K_BACKSPACE:
                        if len(input) > 0:
                            input = input[0:-1]
                    else:
                        if required_number is True:
                            if event.key < 48 or event.key > 57:
                                continue
                        if max_chars > 0 and len(input) < max_chars:
                            input.append(Helper.GetChar(event.key))
                    Helper.CursorShining(''.join(input), cursor_x, cursor_y)

    @staticmethod
    def SetProvinceGovernor(province_no, governor_offset):
        p = RoTK2.GetProvinceBySequence(province_no)
        p.GovernorOffset = governor_offset

        new_list = []
        for o in p.OfficerList:
            if o.Offset != governor_offset:
                new_list.append(o)

        i = -1
        for i in range(0, len(new_list) - 1):
            new_list[i].NextOfficerOffset = new_list[i + 1].NextOfficerOffset
            RoTK2.FlushOfficer(new_list[i])
        if len(new_list) > 0:
            new_list[i + 1].NextOfficerOffset = 0
            RoTK2.FlushOfficer(new_list[i + 1])
            governor = RoTK2.GetOfficerByOffset(governor_offset)
            governor.NextOfficerOffset = new_list[0].Offset
            RoTK2.FlushOfficer(governor)

        RoTK2.FlushProvince(p)

    @staticmethod
    def MoveOfficersToProvince(officer_list, from_province, to_province):
        _from = RoTK2.GetProvinceBySequence(from_province)
        _to = RoTK2.GetProvinceBySequence(to_province)

        from_list = []
        to_list = []
        for i in range(1, len(_from.OfficerList) + 1):
            if i not in officer_list:
                from_list.append(_from.OfficerList[i - 1])
            else:
                to_list.append(_from.OfficerList[i - 1])

        i = -1
        for i in range(0, len(from_list) - 1):
            from_list[i].NextOfficerOffset = from_list[i + 1].Offset
            RoTK2.FlushOfficer(from_list[i])

        if len(from_list) > 0:
            from_list[i + 1].NextOfficerOffset = 0
            RoTK2.FlushOfficer(from_list[i + 1])

            # ensure all of the officers can be visited from this province
            # and, we MUST announce a new governor at 8.1 action
            _from.GovernorOffset = from_list[0].Offset
            RoTK2.FlushProvince(_from)

        i = -1
        for i in range(0, len(to_list) - 1):
            to_list[i].NextOfficerOffset = to_list[i + 1].Offset
            RoTK2.FlushOfficer(to_list[i])
        if len(to_list) > 0:
            to_list[i + 1].NextOfficerOffset = 0
            RoTK2.FlushOfficer(to_list[i + 1])

            # ensure all of the officers can be visited from this province
            # and, we MUST announce a new governor at 8.1 action
            _to.GovernorOffset = to_list[0].Offset
            RoTK2.FlushProvince(_to)

    @staticmethod
    def GetRulerName(province_no):
        ruler_no = RoTK2.GetProvinceBySequence(province_no).RulerNo
        ruler = RoTK2.GetRulerByNo(ruler_no).RulerSelf
        ruler_name_data = RoTK2.GetOfficerName(ruler.Offset)

        return ruler_name_data

    @staticmethod
    def GetChar(key: int):
        if ((key >= 48 and key <= 57) or (key >= 65 and key <= 90) or (key >= 97 and key <= 122)):
            return chr(key)
        else:
            return ""

    @staticmethod
    def GetGraphData(key) -> pygame.Surface:
        grp = Data.GrpdataMappings.get(key)
        if grp is None:
            raise Exception("Invalid key :" + key)

        dc = DrawCGA(grp, Data.GRPDATA[grp[0]:grp[0] + 0x4000])
        dc.Start()

        with open(key + ".grp", "wb") as f:
            f.write(bytes(dc.display_buf))

        bmp = Helper.DrawData(dc.display_buf, 7)
        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def DrawData(data, palette_no) -> pygame.Surface:
        ori_width = (Data.GRPDATA[1] << 8) + Data.GRPDATA[0]
        ori_height = (Data.GRPDATA[3] << 8) + Data.GRPDATA[2]

        width = 640
        height = 200
        size = 16384
        size2 = int(size / 2)
        bmp = pygame.Surface((width, height))

        for k in range(0, 2):
            for i in range(0, size2):
                row = int(i / int(width / 8)) * 2 + k
                if size2 * k + i >= len(data):
                    continue
                b = data[size2 * k + i]

                col = i % int(width / 8)
                for j in range(0, 8):
                    b2 = (b & (0x80 >> j)) >> (7 - j)
                    bmp.set_at((8 * col + j, row), Helper.get_rgb(b2, palette_no))

        return pygame.transform.scale(bmp, (width, height * 2))

    @staticmethod
    def DrawCharacterInternal(character, back_color, palette_no):
        # fname = "inaimathimn"
        # fname="timesnewroman"
        # fname = "dincondensed"
        fname = "arial"
        f = pygame.font.SysFont(fname, 14)
        bmp = f.render(character, True, Helper.Palettes[palette_no], back_color)
        # bmp = bmp.subsurface((0, 7, bmp.get_width(), bmp.get_height()-7)).copy()
        return bmp
        # if bmp.get_width()==11 and bmp.get_height()==30:
        #     bmp = bmp.subsurface((1,7,9,14)).copy()
        # return pygame.transform.scale(bmp,(8,14))

    @staticmethod
    def DrawWordInternal(index, back_color, palette_no):
        x = 0
        bmp = pygame.Surface((16, 14))
        bmp.fill(back_color)

        if index > 1150:
            return bmp

        if index in [55536, 55537, 55538, 55539, 55540, 55541]:
            index2 = (index - 55536) * 28
            one = Data.BUF[0x7778 + 0x38 + index2:0x7778 + 0x38 + index2 + 28]
        else:
            index2 = 30 * int(str(index).strip()) + 2
            one = Data.MSG16P[index2:index2 + 30]

        for i in range(0, 14):
            left = one[2 * i]
            right = one[2 * i + 1]

            for j in range(0, 8):
                if (left & (0x80 >> j)):
                    bmp.set_at((x + j, 0 + i), Helper.Palettes[palette_no])
                if (right & (0x80 >> j)):
                    bmp.set_at((x + j + 8, 0 + i), Helper.Palettes[palette_no])

        return bmp

    @staticmethod
    def DrawText(text, back_color=(0, 0, 0), palette_no=7, scaled=False):
        buf = []
        i = 0
        # every element which starts with $ and ends with $, will DrawWord by piexles
        # other elements will DrawText .
        while True:
            if i >= len(text):
                break

            if text[i] == "$":
                name = []
                while True:
                    i += 1
                    if i >= len(text) or text[i] == "$":
                        break

                    name.append(text[i])

                buf.append(Helper.DrawWordInternal(int(''.join(name)), back_color, palette_no))
                i += 1
            else:
                buf.append(Helper.DrawCharacterInternal(text[i], back_color, palette_no))
                i += 1

        width = 0
        for i in range(0, len(buf)):
            width += buf[i].get_width()

        bmp = pygame.Surface((width, 14))
        bmp.fill(back_color)

        pos = 0
        for b in buf:
            bmp.blit(b, (pos, 0))
            pos += b.get_width()

        scale_value = 1
        if scaled == True:
            scale_value = Helper.Scale

        return pygame.transform.scale(bmp, (bmp.get_width() * scale_value * 1.0, bmp.get_height() * scale_value * 2.0))

    @staticmethod
    def GetBuiltinTextOne(offset):
        return Helper.GetBuiltinText(offset, offset + 1)

    @staticmethod
    def GetProvinceFreeOfficerList(province):
        free_list = []
        free_officer = RoTK2.GetOfficerByOffset(Helper.GetWordFromOffset(Data.BUF, province.Offset + 6))
        free_officer.IsFree = True
        free_list.append(free_officer)

        next = free_officer.NextOfficerOffset
        while next > 0:
            free_officer = RoTK2.GetOfficerByOffset(next)
            free_officer.IsFree = True
            free_list.append(free_officer)

            next = free_officer.NextOfficerOffset

        return free_list

    @staticmethod
    def ShowDelayedText(text, palette_no=6, wait_time=1000, top=360, clear_input_area=True):
        if clear_input_area is True:
            Helper.ClearInputArea()
        img = Helper.DrawText(text, palette_no=palette_no, scaled=True)
        Helper.Screen.blit(img, (300 * Helper.Scale, top * Helper.Scale))
        pygame.display.flip()
        pygame.time.wait(wait_time)

    @staticmethod
    def GetBuiltinText(offset, end=99999999):
        buf = []

        while True:
            if offset > end:
                return ''.join(buf)
            if offset >= len(Data.DSBUF):
                break

            b = Data.DSBUF[offset]
            if b == 0:
                return ''.join(buf)
            elif b == 0x01:
                buf.append("@")
                offset += 1
            elif b == 0x0a:
                buf.append("_")
                offset += 1
            elif b == 0x1b:
                buf.append("@")
                offset += 1
            elif b < 0x20:
                buf.append(".")
                offset += 1
            elif b == 0x24:
                buf.append(".")
                offset += 1
            elif b < 0x80:
                buf.append(chr(b))
                offset += 1
            elif b >= 0x80:
                b2 = Data.DSBUF[offset + 1]
                zh_cn = Data.CNINDEX.get(b * 256 + b2)
                if zh_cn is not None:
                    buf.append("$")
                    buf.append(str(zh_cn))
                    offset += 2
                    buf.append("$")
                else:
                    offset += 1
            else:
                offset += 1
                continue

    @staticmethod
    def ShowCommandsInInputArea(commands, cols, palette_no=1, width=90, commands_color=[], top=2):
        bmp = pygame.Surface((330, 90))
        bmp.fill((0, 0, 0))

        left = 2

        for i in range(0, len(commands)):
            row = int(i / cols)
            col = i % cols

            if len(commands_color) > 0:
                palette_no = commands_color[i]
            cmd_bmp = Helper.DrawText("{0}.{1}".format(i + 1, commands[i]), back_color=(0, 0, 0), palette_no=palette_no)
            bmp.blit(cmd_bmp, (left + width * col, top + 30 * row))

        bmp = pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        Helper.Screen.blit(bmp, (300 * Helper.Scale, 298 * Helper.Scale))
        pygame.display.flip()

    @staticmethod
    def GetOfficerList(officer_list, show_flag: ShowOfficerFlag, page, multi_select, officer_status, can_action=True,
                       enemy_province=False):
        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        col1 = Helper.DrawText(Helper.GetBuiltinText(0x3FF2, 0x3FF5), (0, 0, 0), palette_no=3)
        col2 = Helper.DrawText(Helper.GetBuiltinText(0x3FF9, 0x3FFD), (0, 0, 0), palette_no=3)

        col3 = None
        if show_flag != ShowOfficerFlag.Empty:
            mappings = {ShowOfficerFlag.Int: Helper.GetBuiltinText(0x3FD0),
                        ShowOfficerFlag.War: Helper.GetBuiltinText(0x3FD5),
                        ShowOfficerFlag.Chm: Helper.GetBuiltinText(0x3FDA),
                        ShowOfficerFlag.Loyalty: Helper.GetBuiltinText(0x3FE4),
                        ShowOfficerFlag.Soldiers: Helper.GetBuiltinText(0x3FDF),
                        ShowOfficerFlag.Weapons: Helper.GetBuiltinText(0x3FE9)}
            col3 = Helper.DrawText(mappings[show_flag], (0, 0, 0), palette_no=3)

        more_columns = 1
        if len(officer_list) > 8 * page + 4:
            more_columns = 2

        for i in range(0, more_columns):
            bmp.blit(col1, (5 + 160 * i, 2))
            bmp.blit(col2, (50 + 160 * i, 2))
            if col3 is not None:
                bmp.blit(col3, (120 + 160 * i, 2))

        for i in range(8 * page, 8 * (page + 1)):
            if i >= len(officer_list):
                break

            row = (i % 8) % 4
            col = int((i % 8) / 4)

            star = None
            if multi_select is True and officer_status[i] is True:
                star = Helper.DrawText("*", palette_no=1)
                seq = Helper.DrawText("{0}.".format(i + 1))
            else:
                seq = Helper.DrawText("{0}.".format(i + 1))

            palette_no = 7
            if can_action is True and RoTK2.CanOfficerDoAction(officer_list[i]) is False and enemy_province is False:
                palette_no = 2
            name = Helper.DrawText(RoTK2.GetOfficerName(officer_list[i].Offset), palette_no=palette_no)
            mappings = {ShowOfficerFlag.Empty: 0, ShowOfficerFlag.Int: officer_list[i].Int,
                        ShowOfficerFlag.War: officer_list[i].War, ShowOfficerFlag.Chm: officer_list[i].Chm,
                        ShowOfficerFlag.Loyalty: officer_list[i].Loyalty,
                        ShowOfficerFlag.Soldiers: officer_list[i].Soldiers}
            value = mappings[show_flag]

            v = Helper.DrawText(str(value), palette_no=palette_no)

            if star is not None:
                bmp.blit(star, (160 * col + (40 - seq.get_width()) - 10, 33 + 30 * row))
            bmp.blit(seq, (160 * col + (40 - seq.get_width()), 33 + 30 * row))
            bmp.blit(name, (160 * col + 50, 33 + 30 * row))
            if col3 is not None:
                bmp.blit(v, (120 + 160 * col + (30 - v.get_width()), 33 + 30 * row))

        have_more_pages = True
        if len(officer_list) <= 8 * (page + 1):
            have_more_pages = False
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages, officer_status

    @staticmethod
    def GetCurrentRulerNo():
        current_ruler_province = Helper.GetWordFromOffset(Data.BUF, Data.CURRENT_PROVINCE_OFFSET)
        return Data.BUF[current_ruler_province + 0x10]

    @staticmethod
    def GetOfficerDetailedInformation(officer: Officer):
        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        face_bmp = Helper.GetFace(officer.Portrait)
        bmp.blit(face_bmp, (10, 30))

        name_indexes = RoTK2.GetOfficerName(officer.Offset)
        name_bmp = Helper.DrawText(name_indexes, scaled=False)
        bmp.blit(name_bmp, ((10 + (face_bmp.get_width() - name_bmp.get_width()) / 2), 120))

        ruler_offset = RoTK2.GetRulerByNo(officer.RulerNo).RulerSelf.Offset
        is_ruler = ruler_offset == officer.Offset
        if is_ruler:
            ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), palette_no=2, scaled=False)
            bmp.blit(ruler_bmp, (30, 0))

            if Data.BUF[RoTK2.GetRulerByNo(officer.RulerNo).Offset + 0x21] == 0xFF:
                marriage_status = Helper.GetBuiltinText(0x6422)
            else:
                marriage_ruler = RoTK2.GetRulerByNo(
                    Data.BUF[RoTK2.GetRulerByNo(officer.RulerNo).Offset + 0x21]).RulerSelf
                marriage_status = RoTK2.GetOfficerName(marriage_ruler.Offset)

            marry_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6425).replace("%s", marriage_status), palette_no=2,
                                        scaled=False)
            bmp.blit(marry_bmp, (80, 10))
        else:
            if ruler_offset > 0:
                name_indexes = RoTK2.GetOfficerName(ruler_offset)
                name_bmp = Helper.DrawText(name_indexes, palette_no=2, scaled=False)
                bmp.blit(name_bmp, (80, 10))
                buxia_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6448, 0x644B), scaled=False)
                bmp.blit(buxia_bmp, (80 + name_bmp.get_width(), 10))
            else:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x6439), palette_no=6, scaled=False), (80, 10))

        # 531
        wuzhuang = Helper.DrawText(Helper.GetBuiltinText(0x6575), palette_no=5, scaled=False)
        xunlian = Helper.DrawText(Helper.GetBuiltinText(0x6570), palette_no=5, scaled=False)
        shibing = Helper.DrawText(Helper.GetBuiltinText(0x6583), palette_no=5, scaled=False)
        bmp.blit(wuzhuang, (80, 40))
        bmp.blit(xunlian, (80, 75))
        bmp.blit(shibing, (80, 110))

        wuzhuang = Helper.DrawText(str(officer.Arms))
        xunlian = Helper.DrawText(str(officer.TrainingLevel))
        shibing = Helper.DrawText(str(officer.Soldiers))

        bmp.blit(wuzhuang, (160 - wuzhuang.get_width(), 40))
        bmp.blit(xunlian, (160 - xunlian.get_width(), 75))
        bmp.blit(shibing, (160 - shibing.get_width(), 110))

        juewei = Helper.DrawText(Helper.GetBuiltinText(0x648F, 0x6492), palette_no=3)
        shiweiwei = Helper.DrawText(Helper.GetBuiltinText(0x6494, 0x6497), palette_no=3)
        nianling = Helper.DrawText(Helper.GetBuiltinText(0x6499, 0x649C), palette_no=3)
        bmp.blit(juewei, (170, 40))
        bmp.blit(shiweiwei, (170, 75))
        bmp.blit(nianling, (170, 110))

        na = Helper.DrawText("---")
        if is_ruler or officer.IsUnClaimed or officer.IsFree:
            bmp.blit(na, (210, 40))
            bmp.blit(na, (210, 75))
        else:
            if officer.IsUnClaimed:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x6439)), (210, 40))
                bmp.blit(na, (210, 75))
            else:
                bmp.blit(Helper.DrawText(Helper.GetBuiltinText(0x640F)), (210, 40))
                shiwei = Helper.DrawText(str(officer.shiwei))
                bmp.blit(shiwei, (210 + na.get_width() - shiwei.get_width(), 75))

        age = Helper.DrawText(str(officer.Age), scaled=False)
        bmp.blit(age, (210 + na.get_width() - age.get_width(), 110))

        zhongcheng = Helper.DrawText(Helper.GetBuiltinText(0x6532), palette_no=1)
        caizhi = Helper.DrawText(Helper.GetBuiltinText(0x653B), palette_no=1)
        zhanli = Helper.DrawText(Helper.GetBuiltinText(0x6540), palette_no=1)
        haozhao = Helper.DrawText(Helper.GetBuiltinText(0x6545), palette_no=1)
        bmp.blit(zhongcheng, (250, 5))
        bmp.blit(caizhi, (250, 40))
        bmp.blit(zhanli, (250, 75))
        bmp.blit(haozhao, (250, 110))

        if is_ruler or officer.IsUnClaimed or officer.IsFree:
            bmp.blit(na, (290, 5))
        else:
            zhongcheng = Helper.DrawText(str(officer.Loyalty))
            bmp.blit(zhongcheng, (320 - zhongcheng.get_width(), 5))
        caizhi = Helper.DrawText(str(officer.Int))
        bmp.blit(caizhi, (320 - caizhi.get_width(), 40))
        zhanli = Helper.DrawText(str(officer.War))
        bmp.blit(zhanli, (320 - zhanli.get_width(), 75))
        haozhao = Helper.DrawText(str(officer.Chm))
        bmp.blit(haozhao, (320 - haozhao.get_width(), 110))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def CursorShining(prompt, cursor_x, cursor_y):
        cursor_background = {True: (255, 255, 255), False: (0, 0, 0)}

        bmp = Helper.DrawText(prompt, scaled=True)
        pygame.draw.rect(Helper.Screen, (0, 0, 0), (cursor_x, cursor_y, bmp.get_width(), bmp.get_height()))

        Helper.Screen.blit(bmp, (cursor_x, cursor_y))
        pygame.draw.rect(Helper.Screen, cursor_background[Helper.cur_flag],
                         (cursor_x + bmp.get_width(), cursor_y, 8 * Helper.Scale, 28 * Helper.Scale), 0)
        Helper.cur_flag = not Helper.cur_flag
        pygame.display.flip()

    @staticmethod
    def GetMap():
        list = [Data.GrpdataMappings["MapTop"], Data.GrpdataMappings["MapBottom"],
                Data.GrpdataMappings["MapHead"], ]

        grp = Data.GrpdataMappings["Map"]
        do = DrawCGA(grp, Data.GRPDATA[grp[0]:grp[0] + 0x4000])
        do.Start()
        map_buf = do.display_buf

        tmp_buf = Helper.GetMapLines()
        for mmm in range(0, len(map_buf)):
            map_buf[mmm] ^= tmp_buf[mmm]

        map = Helper.DrawData(map_buf, 7)
        # pygame.image.save(map,"juqiang.png")
        map = Helper.DrawData(tmp_buf, 7)
        # pygame.image.save(map,"juqiang2.png")

        for grp in list:
            do = DrawCGA(grp, Data.GRPDATA[grp[0]:grp[0] + 0x4000])
            do.Start()

            for i in range(0, len(map_buf)):
                map_buf[i] |= do.display_buf[i]

        map = Helper.DrawData(map_buf, 7)

        # fix general picture rectangle aligns too left
        Helper.head_picture = map.subsurface(pygame.Rect(511, 10, 82, 105)).copy()
        line = map.subsurface(pygame.Rect(296, 120, 335, 4)).copy()

        # fill province area information by WHITE
        pygame.draw.rect(map, (255, 255, 255), (296, 7, 335, 114))
        map.blit(line, (296, 290))

        return pygame.transform.scale(map, (map.get_width() * Helper.Scale, map.get_height() * Helper.Scale))

    @staticmethod
    def GetMapLines():
        with open("../Resources/map.grp", "rb") as f:  # content loaded from debug.exe: d ds:0
            map_buf = list(f.read())

        buf = Data.BUF
        tmp_buf = [0] * 0x4000  # 不用上面的map原图，只用下面这个，则会得到该省的单独的上色的地图

        for p in range(0, 41):
            p1 = buf[0x2d8c + 0x38 + 0x23 * p + 0x1c] + buf[0x2d8c + 0x38 + 0x23 * p + 0x1d] * 256
            p2 = buf[0x2d8c + 0x38 + 0x23 * p + 0x1e] + buf[0x2d8c + 0x38 + 0x23 * p + 0x1f] * 256

            ruler_no = buf[0x2d8c + 0x38 + 0x23 * p + 0x10]
            if ruler_no == 0xff:
                continue
            ruler_color = Data.RulerPalette[ruler_no]
            ruler_color = ruler_color * 6 + 0x3b30

            d = DrawMapLines(map_buf, Data.DSBUF, p1, p2, ruler_color)
            d.Start()

            for mmm in range(0, len(tmp_buf)):
                tmp_buf[mmm] |= d.display_buf[mmm]

        # bmp = Helper.DrawData(tmp_buf,ruler_no)
        # pygame.image.save(bmp,"bmp.png".format(p+1))

        return tmp_buf

    @staticmethod
    def GetProvinceName(prov_no, without_no=False):
        prov_name_index = Data.PROVINCE_START + Data.PROVINCE_SIZE * (prov_no - 1) + 0x22

        name_list = []
        for i in range(0, 14):
            name_list.append(Helper.GetBuiltinText(0x4520 + 6 * i))

        if without_no is True:
            prov_name = name_list[Data.BUF[prov_name_index]] + Helper.GetBuiltinText(0x6309, 0x630A)
        else:
            prov_name = name_list[Data.BUF[prov_name_index]] + Helper.GetBuiltinText(0x6309, 0x630A) + "-" + str(
                prov_no)

        return prov_name

    @staticmethod
    def GetProvinceNameImage(prov_no):
        prov_name = Helper.GetProvinceName(prov_no)
        prov_name_bmp = Helper.DrawText(prov_name, back_color=(255, 255, 255), palette_no=0)
        return prov_name_bmp

    @staticmethod
    def GetGovernorInformation(prov_no):
        bmp = pygame.Surface((330, 105))
        bmp.fill((255, 255, 255))

        prov_name_bmp = Helper.GetProvinceNameImage(prov_no)
        bmp.blit(prov_name_bmp, (0, 20))

        province_offset = Data.PROVINCE_START + Data.PROVINCE_SIZE * (prov_no - 1)
        ruler_no = Data.BUF[province_offset + 0x10]

        if ruler_no == 255:
            empty_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6310), back_color=(255, 255, 255), palette_no=0)
            bmp.blit(empty_bmp, (60, 20))
            return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

        ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), back_color=(255, 255, 255), palette_no=2)
        bmp.blit(ruler_bmp, (60, 20))

        officer_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(255, 255, 255), palette_no=4)
        bmp.blit(officer_bmp, (60, 70))

        ruler_offset = Data.RULER_START + Data.RULER_SIZE * (ruler_no - 0)
        ruler_province_offset = Data.BUF[(ruler_offset + 3)] * 256 + Data.BUF[ruler_offset + 2]
        ruler_as_general_offset = Data.BUF[(ruler_offset + 1)] * 256 + Data.BUF[ruler_offset]

        ruler_name_data = RoTK2.GetOfficerName(ruler_as_general_offset)
        ruler_name_bmp = Helper.DrawText(ruler_name_data, back_color=(255, 255, 255), palette_no=0)
        bmp.blit(ruler_name_bmp, (105, 20))

        ruler_trust = Data.BUF[ruler_offset + 0x06]
        trust_text = Helper.GetBuiltinText(0x67D2).replace("%3d", str(ruler_trust))
        trust_bmp = Helper.DrawText(trust_text, back_color=(255, 255, 255), palette_no=0)
        bmp.blit(trust_bmp, (152, 20))
        officer_offset = Data.BUF[(province_offset + 3)] * 256 + Data.BUF[province_offset + 2]
        officer_name_data = RoTK2.GetOfficerName(officer_offset)
        officer_bmp = Helper.DrawText(officer_name_data, back_color=(255, 255, 255), palette_no=0)
        bmp.blit(officer_bmp, (105, 70))

        bmp.blit(Helper.head_picture, (250, 0))
        portrait = Data.BUF[officer_offset + 0x1B] * 256 + Data.BUF[officer_offset + 0x1A] - 1
        face = Helper.GetFace(portrait)
        bmp.blit(face, (259, 14))

        advisor_offset = Data.BUF[(ruler_offset + 5)] * 256 + Data.BUF[ruler_offset + 4]
        if advisor_offset > 0:
            offlist = RoTK2.GetProvinceBySequence(prov_no).OfficerList
            exist_advisor = False
            for officer in offlist:
                if officer.Offset == advisor_offset:
                    exist_advisor = True
                    break
            if exist_advisor:
                assistant_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640a), back_color=(255, 255, 255), palette_no=6)
                bmp.blit(assistant_bmp, (152, 70))

                advisor_name_data = RoTK2.GetOfficerName(advisor_offset)
                advisor_offset_bmp = Helper.DrawText(advisor_name_data, back_color=(255, 255, 255), palette_no=0)
                bmp.blit(advisor_offset_bmp, (235 - assistant_bmp.get_width(), 70))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def ShowMap(prov_no):
        Helper.Screen.blit(Helper.MainMap, (0, 0))

        date_bmp = Helper.DrawDate()
        Helper.Screen.blit(date_bmp, (25, 15))

        officer = Helper.GetGovernorInformation(prov_no)
        Helper.Screen.blit(officer, (300 * Helper.Scale, 12 * Helper.Scale))

        province = Helper.GetProvinceInformation(prov_no)
        Helper.Screen.blit(province, (300 * Helper.Scale, 130 * Helper.Scale))

        pygame.display.flip()

    @staticmethod
    def GetGenericFace(index):
        info = "{0:b}".format(index).zfill(16)
        wenxu = int(info[0:3], 2)  # 100武将，110文官
        kou = int(info[3:5], 2)
        bi = int(info[5:7], 2)
        yan = int(info[7:9], 2)
        shang = int(info[9:11], 2)
        xia = int(info[11:13], 2)
        group = int(info[13:16], 2)

        width = 64
        size = int(width * (18 * 4 + 22 * 4 + 8 * 4 + 10 * 4 + 8 * 4) * 3 / 8)

        height_list = [18, 22, 8, 10, 8]
        face_data = []
        face = Data.MONTAGE[group * size:group * size + size]

        pos = 0
        for h in height_list:
            for k in range(0, 4):
                block_size = int(width * h * 3 / 8)

                face_buf = []
                for i in range(0, block_size, 3):
                    a = "{0:b}".format(face[i + 0 + pos]).zfill(8)
                    b = "{0:b}".format(face[i + 1 + pos]).zfill(8)
                    c = "{0:b}".format(face[i + 2 + pos]).zfill(8)
                    for j in range(0, 8):
                        face_buf.append(int(a[j] + b[j] + c[j], 2))

                face_data.append(face_buf)
                pos += block_size

        img = pygame.Surface((64, 40))
        img.fill((0, 0, 0))
        pos_list = [shang, 4 + xia, 8 + kou, 12 + bi, 16 + yan]
        s = 0
        for i in range(0, 18):
            for j in range(0, 64):
                true_color = Helper.Palettes[face_data[shang][64 * i + j]]
                img.set_at((j, i), (true_color.r, true_color.g, true_color.b))

        for i in range(0, 22):
            for j in range(0, 64):
                true_color = Helper.Palettes[face_data[4 + xia][64 * i + j]]
                img.set_at((j, i + 18), (true_color.r, true_color.g, true_color.b))

        for i in range(0, 8):
            for j in range(0, 64):
                true_color = Helper.Palettes[face_data[8 + yan][64 * i + j]]
                if true_color.r == 0 and true_color.g == 0 and true_color.b == 0:
                    continue
                img.set_at((j, i + 10), (true_color.r, true_color.g, true_color.b))

        for i in range(0, 8):
            for j in range(0, 64):
                true_color = Helper.Palettes[face_data[16 + bi][64 * i + j]]
                if true_color.r == 0 and true_color.g == 0 and true_color.b == 0:
                    continue
                img.set_at((j, i + 16), (true_color.r, true_color.g, true_color.b))

        for i in range(0, 10):
            for j in range(0, 64):
                true_color = Helper.Palettes[face_data[12 + kou][64 * i + j]]
                if true_color.r == 0 and true_color.g == 0 and true_color.b == 0:
                    continue
                img.set_at((j, i + 22), (true_color.r, true_color.g, true_color.b))

        return pygame.transform.scale(img, (64, 80))

    @staticmethod
    def GetFace(index):
        if index < 219:
            return Helper.GetSingleFace(index)
        else:
            return Helper.GetGenericFace(index)

    @staticmethod
    def GetSingleFace(index):
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
                true_color = Helper.Palettes[face_buf[64 * i + j]]
                img.set_at((j, i), (true_color.r, true_color.g, true_color.b))

        return pygame.transform.scale(img, (64, 80))

    @staticmethod
    def GetProvincePromptText(officer):
        list = []

        list.append(["", officer, "，"])

    @staticmethod
    def DrawDate():
        year = Data.BUF[0x45] * 256 + Data.BUF[0x44]
        month = Data.BUF[0x46] + 1
        season = Helper.GetBuiltinText(0x3dbb + 3 * int((month - 1) / 3))
        info = "{0}{3} {1}{4} {2}".format(year, month, season, Helper.GetBuiltinTextOne(0x3DD2),
                                          Helper.GetBuiltinTextOne(0x3DD7))
        bmp = Helper.DrawText(info, back_color=(255, 255, 255), palette_no=0)

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def GetProvinceInformation(prov_no):
        p = RoTK2.GetProvinceBySequence(prov_no)

        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        province_offset = Data.PROVINCE_START + Data.PROVINCE_SIZE * (prov_no - 1)

        polutions = Helper.DrawText(Helper.GetBuiltinText(0x621A, 0x621D), palette_no=5)
        polutions_num = (Data.BUF[(province_offset + 0x0f)] << 8) + (Data.BUF[(province_offset + 0x0e)] << 0)
        polutions_bmp = Helper.DrawText(str(polutions_num * 100), palette_no=7)
        soldiers = Helper.DrawText(Helper.GetBuiltinText(0x6251, 0x6254), palette_no=5)
        soldiers_num = Helper.DrawText(str(p.Soldiers), palette_no=7)
        onlines = Helper.DrawText(Helper.GetBuiltinText(0x6288, 0x628F), palette_no=6)
        onlines_num = Helper.DrawText(str(p.ClaimedOfficerNumber), palette_no=7)
        offlines = Helper.DrawText(Helper.GetBuiltinText(0x62C4, 0x62CB), palette_no=6)
        offlines_num = Helper.DrawText(str(p.UnClaimedOfficerNumber), palette_no=7)

        gold = Helper.DrawText(Helper.GetBuiltinText(0x7C37), palette_no=3)
        gold_num = Data.BUF[(province_offset + 9)] * 256 + Data.BUF[province_offset + 8]
        gold_bmp = Helper.DrawText(str(gold_num), palette_no=7)

        food = Helper.DrawText(Helper.GetBuiltinText(0x6263, 0x6266), palette_no=3, )
        food_num = (Data.BUF[(province_offset + 0x0d)] << 24) + (Data.BUF[(province_offset + 0x0c)] << 16) + (
                Data.BUF[(province_offset + 0x0b)] << 8) + (Data.BUF[(province_offset + 0x0a)] << 0)
        food_bmp = Helper.DrawText(str(food_num), palette_no=7)

        rice_price = Helper.DrawText(Helper.GetBuiltinText(0x629E, 0x62A1), palette_no=3)
        rice_price_value = Data.BUF[(province_offset + 0x1B)]
        rice_price_bmp = Helper.DrawText(str(rice_price_value), palette_no=7)
        horse = Helper.DrawText(Helper.GetBuiltinText(0x62DA, 0x62DD), palette_no=3, scaled=False)
        horse_value = Data.BUF[(province_offset + 0x19)]
        horse_bmp = Helper.DrawText(str(horse_value), palette_no=7)

        loyal = Helper.DrawText(Helper.GetBuiltinText(0x623D, 0x6244), palette_no=1)
        loyal_value = Data.BUF[(province_offset + 0x17)]
        loyal_bmp = Helper.DrawText(str(loyal_value), palette_no=7)
        land = Helper.DrawText(Helper.GetBuiltinText(0x6274, 0x6277), palette_no=1)
        land_value = Data.BUF[(province_offset + 0x16)]
        land_bmp = Helper.DrawText(str(land_value), palette_no=7)
        flood = Helper.DrawText(Helper.GetBuiltinText(0x62AF, 0x62B4), palette_no=1)
        flood_value = Data.BUF[(province_offset + 0x18)]
        flood_bmp = Helper.DrawText(str(flood_value), palette_no=7)
        port = Helper.DrawText(Helper.GetBuiltinText(0x62EC, 0x62EF), palette_no=1)
        port_value = Data.BUF[(province_offset + 0x1A)]
        port_bmp = Helper.DrawText(str(port_value), palette_no=7)

        bmp.blit(polutions, (5, 0))
        bmp.blit(polutions_bmp, (110 - polutions_bmp.get_width(), 0))
        bmp.blit(soldiers, (5, 40))
        bmp.blit(soldiers_num, (110 - soldiers_num.get_width(), 40))
        bmp.blit(onlines, (5, 80))
        bmp.blit(onlines_num, (110 - onlines_num.get_width(), 80))
        bmp.blit(offlines, (5, 120))
        bmp.blit(offlines_num, (110 - offlines_num.get_width(), 120))

        bmp.blit(gold, (115, 0))
        bmp.blit(gold_bmp, (220 - gold_bmp.get_width(), 0))
        bmp.blit(food, (115, 40))
        bmp.blit(food_bmp, (220 - food_bmp.get_width(), 40))
        bmp.blit(rice_price, (115, 80))
        bmp.blit(rice_price_bmp, (220 - rice_price_bmp.get_width(), 80))
        bmp.blit(horse, (115, 120))
        bmp.blit(horse_bmp, (220 - horse_bmp.get_width(), 120))

        bmp.blit(loyal, (225, 0))
        bmp.blit(loyal_bmp, (325 - loyal_bmp.get_width(), 0))
        bmp.blit(land, (225, 40))
        bmp.blit(land_bmp, (325 - land_bmp.get_width(), 40))
        bmp.blit(flood, (225, 80))
        bmp.blit(flood_bmp, (325 - flood_bmp.get_width(), 80))
        bmp.blit(port, (225, 120))
        bmp.blit(port_bmp, (325 - port_bmp.get_width(), 120))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def GetOfficersSummary(prov_no, page):
        bmp = pygame.Surface((335, 284))
        bmp.fill((0, 0, 0))

        header = pygame.Surface((335, 40))
        header.fill((255, 255, 255))

        guanjie = Helper.DrawText(Helper.GetBuiltinText(0x651f, 0x6522), back_color=(255, 255, 255), palette_no=0)
        jiangling = Helper.DrawText(" {0}   ".format(Helper.GetBuiltinText(0x6528)), back_color=(255, 255, 255),
                                    palette_no=4)
        zhongcheng = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6532)), back_color=(255, 255, 255),
                                     palette_no=2)
        caizhi = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x653B, 0x653E)), back_color=(255, 255, 255),
                                 palette_no=6)
        zhanli = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6540)), back_color=(255, 255, 255),
                                 palette_no=6)
        haozhao = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6545)), back_color=(255, 255, 255),
                                  palette_no=6)
        shibing = Helper.DrawText(" {0}".format(Helper.GetBuiltinText(0x654E, 0x6552)), back_color=(255, 255, 255),
                                  palette_no=0)

        name_list = [guanjie, jiangling, zhongcheng, caizhi, zhanli, haozhao, shibing]
        x_list = [0, 36, 99, 146, 194, 241, 292]

        index = 0
        for i in range(0, len(name_list)):
            header.blit(name_list[i], (x_list[i], 8))
            if i < len(name_list) - 1:
                pygame.draw.line(header, (0, 0, 0), (x_list[i + 1] - 1, 0), (x_list[i + 1] - 1, 40), 1)

        bmp.blit(header, (0, 0))

        body = pygame.Surface((335, bmp.get_height() - header.get_height()))
        body.fill((0, 0, 0))

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                pygame.draw.line(body, Helper.Palettes[3], (x_list[i + 1] - 1, 0),
                                 (x_list[i + 1] - 1, body.get_height()), 1)

        height = 2
        official_officer_list = RoTK2.GetProvinceBySequence(prov_no).OfficerList
        unclaimed_officer_list = RoTK2.GetProvinceBySequence(prov_no).UnclaimedOfficerList

        officer_list = official_officer_list + unclaimed_officer_list

        i = 0
        for officer in officer_list:
            if i < 7 * page:
                i += 1
                continue

            if RoTK2.IsRuler(officer):
                ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), back_color=(0, 0, 0), palette_no=2)
                body.blit(ruler_bmp, (0, height + 2))
            elif RoTK2.IsGoverner(officer) is True and RoTK2.IsRuler(officer) is False:
                officer_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(0, 0, 0), palette_no=5)
                body.blit(officer_bmp, (0, height + 2))
            elif RoTK2.IsAdvisor(officer):
                advisor_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640A), back_color=(0, 0, 0), palette_no=1)
                body.blit(advisor_bmp, (0, height + 2))
            else:
                if officer.IsUnClaimed is False and officer.IsFree is False:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640F), back_color=(0, 0, 0), palette_no=7)
                else:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6414), back_color=(0, 0, 0), palette_no=6)
                body.blit(is_online_bmp, (0, height + 2))

            general_name_data = RoTK2.GetOfficerName(officer.Offset)
            p_no = 7
            if officer.IsUnClaimed is True or officer.IsFree is True or officer.IsSick is True:
                p_no = 6
            general_name_bmp = Helper.DrawText(general_name_data, back_color=(0, 0, 0), palette_no=p_no)
            body.blit(general_name_bmp, (x_list[1] + 10, height + 2))

            if RoTK2.IsRuler(officer) or officer.IsUnClaimed is True:
                loyal = "---"
            else:
                loyal = str(officer.Loyalty)
            loyal_bmp = Helper.DrawText(loyal, (0, 0, 0), 7)
            body.blit(loyal_bmp, (x_list[3] - loyal_bmp.get_width() - 8, height + 2))

            zhili_bmp = Helper.DrawText(str(officer.Int), (0, 0, 0), 7)
            body.blit(zhili_bmp, (x_list[4] - zhili_bmp.get_width() - 8, height + 2))

            zhanli_bmp = Helper.DrawText(str(officer.War), (0, 0, 0), 7)
            body.blit(zhanli_bmp, (x_list[5] - zhanli_bmp.get_width() - 8, height + 2))

            haozhao_bmp = Helper.DrawText(str(officer.Chm), (0, 0, 0), 7)
            body.blit(haozhao_bmp, (x_list[6] - haozhao_bmp.get_width() - 8, height + 2))

            shibing_bmp = Helper.DrawText(str(officer.Soldiers), (0, 0, 0), 7)
            body.blit(shibing_bmp, (338 - shibing_bmp.get_width() - 5, height + 2))

            height += 35

        bmp.blit(body, (0, 40))

        have_more_pages = False
        if len(officer_list) > 7 * (page + 1):
            have_more_pages = True
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages

    @staticmethod
    def GetOfficersSummary2(prov_no, page):
        bmp = pygame.Surface((335, 284))
        bmp.fill((0, 0, 0))

        header = pygame.Surface((335, 40))
        header.fill((255, 255, 255))

        guanjie = Helper.DrawText(Helper.GetBuiltinText(0x651f, 0x6522), back_color=(255, 255, 255), palette_no=0)
        jiangling = Helper.DrawText(" {0}   ".format(Helper.GetBuiltinText(0x6528)), back_color=(255, 255, 255),
                                    palette_no=4)

        shiwei = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6567, 0x656A)), back_color=(255, 255, 255),
                                 palette_no=2)
        wuzhuang = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6575)), back_color=(255, 255, 255),
                                   palette_no=6)
        wuqi = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x657A)), back_color=(255, 255, 255), palette_no=6)
        xunlian = Helper.DrawText(" {0}  ".format(Helper.GetBuiltinText(0x6570)), back_color=(255, 255, 255),
                                  palette_no=6)
        shibing = Helper.DrawText(" {0}".format(Helper.GetBuiltinText(0x6583)), back_color=(255, 255, 255),
                                  palette_no=0)

        name_list = [guanjie, jiangling, shiwei, xunlian, wuzhuang, wuqi, shibing]
        x_list = [0, 36, 99, 146, 194, 241, 292]

        index = 0
        for i in range(0, len(name_list)):
            header.blit(name_list[i], (x_list[i], 8))
            if i < len(name_list) - 1:
                pygame.draw.line(header, (0, 0, 0), (x_list[i + 1] - 1, 0), (x_list[i + 1] - 1, 40), 1)

        bmp.blit(header, (0, 0))

        body = pygame.Surface((335, bmp.get_height() - header.get_height()))
        body.fill((0, 0, 0))

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                pygame.draw.line(body, Helper.Palettes[3], (x_list[i + 1] - 1, 0),
                                 (x_list[i + 1] - 1, body.get_height()), 1)

        height = 2
        i = 0
        official_officer_list = RoTK2.GetProvinceBySequence(prov_no).OfficerList
        unclaimed_officer_list = RoTK2.GetProvinceBySequence(prov_no).UnclaimedOfficerList

        officer_list = official_officer_list + unclaimed_officer_list

        for officer in officer_list:
            if i < 7 * page:
                i += 1
                continue

            if RoTK2.IsRuler(officer):
                ruler_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6400), back_color=(0, 0, 0), palette_no=2)
                body.blit(ruler_bmp, (0, height + 2))
            elif RoTK2.IsGoverner(officer) is True and RoTK2.IsRuler(officer) is False:
                officer_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(0, 0, 0), palette_no=5)
                body.blit(officer_bmp, (0, height + 2))
            elif RoTK2.IsAdvisor(officer):
                advisor_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640A), back_color=(0, 0, 0), palette_no=1)
                body.blit(advisor_bmp, (0, height + 2))
            else:
                if officer.IsUnClaimed is False and officer.IsFree is False:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x640F), back_color=(0, 0, 0), palette_no=7)
                else:
                    is_online_bmp = Helper.DrawText(Helper.GetBuiltinText(0x6414), back_color=(0, 0, 0), palette_no=6)
                body.blit(is_online_bmp, (0, height + 2))

            general_name_data = RoTK2.GetOfficerName(officer.Offset)
            p_no = 7
            if officer.IsUnClaimed is True or officer.IsFree is True or officer.IsSick is True:
                p_no = 6
            general_name_bmp = Helper.DrawText(general_name_data, back_color=(0, 0, 0), palette_no=p_no)
            body.blit(general_name_bmp, (x_list[1] + 10, height + 2))

            shiwei_text = "---" if officer.IsUnClaimed else str(officer.shiwei)
            shiwei_bmp = Helper.DrawText(shiwei_text, (0, 0, 0), 7)
            body.blit(shiwei_bmp, (x_list[3] - shiwei_bmp.get_width() - 8, height + 2))

            xunlian_bmp = Helper.DrawText(str(officer.TrainingLevel), (0, 0, 0), 7)
            body.blit(xunlian_bmp, (x_list[4] - xunlian_bmp.get_width() - 8, height + 2))

            wuzhuang_bmp = Helper.DrawText(str(officer.Arms), (0, 0, 0), 7)
            body.blit(wuzhuang_bmp, (x_list[5] - wuzhuang_bmp.get_width() - 8, height + 2))

            wuqi_bmp = Helper.DrawText(str(officer.Weapons), (0, 0, 0), 7)
            body.blit(wuqi_bmp, (x_list[6] - wuqi_bmp.get_width() - 8, height + 2))

            shibing_bmp = Helper.DrawText(str(officer.Soldiers), (0, 0, 0), 7)
            body.blit(shibing_bmp, (338 - shibing_bmp.get_width() - 5, height + 2))

            height += 35
            i += 1
        bmp.blit(body, (0, 40))

        have_more_pages = False
        if len(officer_list) > 7 * (page + 1):
            have_more_pages = True
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages

    @staticmethod
    def RemoveProvinceFromRuler(ruler_no, province_no):
        plist = RoTK2.GetProvincesByRulerNo(ruler_no)
        new_list = []
        for p in plist:
            if p.No != province_no:
                new_list.append(p)
        i = -1
        for i in range(0, len(new_list) - 1):
            new_list[i].NextProvince = new_list[i + 1].Offset
            RoTK2.FlushProvince(new_list[i])
        if len(new_list) > 0:
            new_list[i + 1].NextProvince = 0

    @staticmethod
    def Is2ProvincesAreSameRuler(province_no, p_no):
        ruler_no_1 = RoTK2.GetProvinceBySequence(province_no).RulerNo
        ruler_no_2 = RoTK2.GetProvinceBySequence(p_no).RulerNo

        return ruler_no_1 == ruler_no_2

    @staticmethod
    def GetNeighbor(x, y, loop):
        # maine.exe:  from ds:36a0, stored in dsbuf.dat 36ao offset. or main.exe, just search below binaries.
        # main.exe from ds:3f66
        magic = [0x01, 0x02, 0x01, 0x00, 0x00, 0x00, 0x02, 0x02, 0x02, 0x01, 0x00, 0x01]
        # maine.exe from ds:3c06
        # main.exe from ds:44ca
        magic2 = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x03, 0x02, 0x05, 0xFF, 0xFF
            , 0xFF, 0xFF, 0xFF, 0x04, 0x06, 0x08, 0x07, 0xFF, 0x0E, 0xFF, 0xFF, 0x0A, 0x09, 0x10, 0x0F, 0x17
            , 0x0D, 0x0C, 0x0B, 0x13, 0x12, 0x1B, 0x11, 0x18, 0xFF, 0x1D, 0x1C, 0x1E, 0x14, 0x15, 0x1A, 0x19
            , 0xFF, 0x20, 0x1F, 0x27, 0x16, 0x25, 0x24, 0xFF, 0xFF, 0x22, 0x21, 0x28, 0x26, 0xFF, 0xFF, 0xFF
            , 0xFF, 0xFF, 0x23, 0xFF, 0xFF
                  ]

        al = magic[loop + 6 * (x % 2)] + y
        x += loop % 3

        if x == 0 or x > 8 or al == 0 or al > 9:
            return 0xff

        return magic2[x - 1 + (al - 1) * 8]

    @staticmethod
    def GetNeighbors(province_no):
        p = RoTK2.GetProvinceBySequence(province_no)
        neighbors = []

        for i in range(0, 6):
            no = Helper.GetNeighbor(p.X, p.Y, i)
            neighbors.append(no + 1)

        return neighbors

    @staticmethod
    def GetSortedNeighbors(province_no):
        sorted_neighbors = []
        neighbors = Helper.GetNeighbors(province_no)
        for neighbor in neighbors:
            if neighbor > 0:
                sorted_neighbors.append(neighbor)

        return sorted(sorted_neighbors)

    @staticmethod
    def NeighborsRandomChoice():
        sequences = Data.DSBUF[0xAFF6:0xAFFC]
        random.shuffle(sequences)
        for i in range(0, 6):
            Data.DSBUF[0xAFF6 + i] = sequences[i]

    @staticmethod
    def SelectOfficer(province_no, prompt, show_flag: ShowOfficerFlag, multi_select=False, check_can_action=True,
                      show_governor=True, row=0, clear_area=True, offical=True, enemy_province=False):
        if offical is True:
            officer_list = RoTK2.GetProvinceBySequence(province_no).OfficerList
        else:
            officer_list = RoTK2.GetProvinceBySequence(province_no).UnclaimedOfficerList

        if show_governor is False:
            officer_list = officer_list[1:]

        page = 0
        only_one_page = (len(officer_list) <= 8)
        officer_status = [False] * len(officer_list)

        while True:
            if clear_area is True:
                Helper.ClearInputArea()
            bmp, have_more_pages, officer_status = Helper.GetOfficerList(officer_list, show_flag, page, multi_select,
                                                                         officer_status, check_can_action,
                                                                         enemy_province)
            Helper.Screen.blit(bmp, (300 * Helper.Scale, 130 * Helper.Scale))

            if only_one_page:
                yn = Helper.GetInput(prompt + " (1-{0})? ".format(len(officer_list)), required_number_min=1,
                                     required_number_max=len(officer_list), row=row)
            else:
                yn = Helper.GetInput(prompt + " (0-{0})?".format(len(officer_list)),
                                     next_prompt=Helper.GetBuiltinText(0x6393), required_number_min=0,
                                     required_number_max=len(officer_list), row=row)

            if yn == -1:
                break
            elif yn == 0 and only_one_page is False:
                page += 1
                if 8 * page > len(officer_list):
                    page = 0
            elif check_can_action is True and RoTK2.CanOfficerDoAction(officer_list[yn - 1]) is False:
                continue
            else:
                officer_status[yn - 1] = not officer_status[yn - 1]
                if multi_select is False:
                    break

        if multi_select is False:
            ret = 0
            for i in range(0, len(officer_status)):
                if officer_status[i] is True:
                    ret = i + 1
                    if show_governor is False:
                        ret += 1
                    break
            return ret
        else:
            ret = []
            for i in range(0, len(officer_status)):
                if officer_status[i] is True:
                    if show_governor is False:
                        ret.append(i + 1)
                    else:
                        ret.append(i + 2)

            return ret

    @staticmethod
    def ComapreValueWithRandom100(value):
        num = random.randint(0, 100)
        if value >= num:
            return 1
        else:
            return 0

    @staticmethod
    def DisplayProvinces(ruler_no, page):
        bmp = pygame.Surface((335, 284))
        bmp.fill((0, 0, 0))

        header = pygame.Surface((335, 40))
        header.fill((255, 255, 255))

        no = Helper.DrawText("#", back_color=(255, 255, 255), palette_no=4)
        taishou = Helper.DrawText(Helper.GetBuiltinText(0x6405), back_color=(255, 255, 255), palette_no=0)
        huangjin = Helper.DrawText(Helper.GetBuiltinText(0x7C37), back_color=(255, 255, 255), palette_no=1)
        liangshi = Helper.DrawText(Helper.GetBuiltinText(0x6263, 0x6266), back_color=(255, 255, 255), palette_no=1)
        shibing = Helper.DrawText(Helper.GetBuiltinText(0x6251, 0x6254), back_color=(255, 255, 255), palette_no=2)
        zhongcheng = Helper.DrawText(Helper.GetBuiltinText(0x623F, 0x6242), back_color=(255, 255, 255), palette_no=1,
                                     scaled=False)
        jiangling = Helper.DrawText(Helper.GetBuiltinText(0x6528, 0x652C), back_color=(255, 255, 255), palette_no=6,
                                    scaled=False)

        name_list = [no, taishou, huangjin, liangshi, shibing, zhongcheng, jiangling]
        x_list = [5, 25, 85, 135, 195, 255, 295]

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                header.blit(name_list[i], (x_list[i] + (x_list[i + 1] - x_list[i] - name_list[i].get_width()) / 2, 8))
            else:
                header.blit(name_list[i], (
                    x_list[len(name_list) - 1] + (335 - x_list[len(name_list) - 1] - name_list[i].get_width()) / 2, 8))
            if i < len(name_list) - 1:
                pygame.draw.line(header, (0, 0, 0), (x_list[i + 1] - 1, 0), (x_list[i + 1] - 1, 40), 1)

        bmp.blit(header, (0, 0))

        body = pygame.Surface((335, bmp.get_height() - header.get_height()))
        body.fill((0, 0, 0))

        index = 0
        for i in range(0, len(name_list)):
            if i < len(name_list) - 1:
                pygame.draw.line(body, Helper.Palettes[3], (x_list[i + 1] - 1, 0),
                                 (x_list[i + 1] - 1, body.get_height()), 1)

        height = 2

        province_list = RoTK2.GetProvincesByRulerNo(ruler_no)
        i = 0
        for province in province_list:
            if i < 7 * page:
                i += 1
                continue

            palette_no = 7
            if province.DelegateControl != "":
                palette_no = 5
            body.blit(Helper.DrawText(str(province.No)), (x_list[0], height + 2))
            governor_name_data = RoTK2.GetOfficerName(province.GovernorOffset)
            governor_name = Helper.DrawText(governor_name_data, palette_no=palette_no)
            body.blit(governor_name, (x_list[1] + (x_list[2] - x_list[1] - governor_name.get_width()) / 2, height + 2))
            huangjin = Helper.DrawText(str(province.Gold), scaled=False, palette_no=palette_no)
            body.blit(huangjin, (x_list[3] - huangjin.get_width() - 3, height + 2))
            liangshi = Helper.DrawText(str(province.Food), scaled=False, palette_no=palette_no)
            body.blit(liangshi, (x_list[4] - liangshi.get_width() - 3, height + 2))
            shibing = Helper.DrawText(str(province.Soldiers), scaled=False, palette_no=palette_no)
            body.blit(shibing, (x_list[5] - shibing.get_width() - 3, height + 2))
            zhongcheng = Helper.DrawText(str(province.Loyalty), scaled=False, palette_no=palette_no)
            body.blit(zhongcheng, (x_list[6] - zhongcheng.get_width() - 3, height + 2))
            jiangling = Helper.DrawText(str(province.ClaimedOfficerNumber), scaled=False, palette_no=palette_no)
            body.blit(jiangling, (335 - name_list[i % 7].get_width() - 3, height + 2))

            height += 35
            continue

        bmp.blit(body, (0, 40))

        have_more_pages = False
        if len(province_list) > 7 * (page + 1):
            have_more_pages = True
        return pygame.transform.scale(bmp, (
            bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale)), have_more_pages

    @staticmethod
    def ShowCommand8_Sort():
        bmp = pygame.Surface((330, 90))
        bmp.fill((0, 0, 0))

        left = 2
        top = 2

        p_no = 5
        command8 = [Helper.GetBuiltinText(0x63B6, 0x63B9), Helper.GetBuiltinText(0x63C2, 0x63C7),
                    Helper.GetBuiltinText(0x63CE, 0x63D4), Helper.GetBuiltinText(0x63D7, 0x63DC),
                    Helper.GetBuiltinText(0x63E2, 0x63E8)]

        for i in range(0, len(command8)):
            row = int(i / 3)
            col = i % 3

            cmd_bmp = Helper.DrawText("{0}.{1}".format(i + 1, command8[i]), back_color=(0, 0, 0), palette_no=p_no)
            bmp.blit(cmd_bmp, (left + 90 * col, top + 30 * row))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def GetAll20Commands():
        bmp = pygame.Surface((330, 150))
        bmp.fill((0, 0, 0))

        top = 5
        left = 5

        for i in range(0, 20):
            cmd_no = i

            row = cmd_no % 4
            col = int(cmd_no / 4)

            cmd_bmp = Helper.DrawText(Helper.GetBuiltinText(0x609d + cmd_no * 5), back_color=(0, 0, 0), palette_no=7)
            num_bmp = Helper.DrawText("{0:2}.".format(cmd_no), (0, 0, 0), 3, scaled=False)

            bmp.blit(num_bmp, (left + 65 * (col + 0) + (24 - num_bmp.get_width()), top + 38 * row))
            bmp.blit(cmd_bmp, (left + 65 * col + 24, top + 38 * row))

        return pygame.transform.scale(bmp, (bmp.get_width() * Helper.Scale, bmp.get_height() * Helper.Scale))

    @staticmethod
    def LinklistAppendObject(parent, offset):
        current = Helper.GetWordFromOffset(Data.BUF, parent)
        if current == 0:
            Helper.SetWordToOffset(Data.BUF, offset, parent)
            return

        while True:
            next = Helper.GetWordFromOffset(Data.BUF, current)
            if next == 0:
                Helper.SetWordToOffset(Data.BUF, offset, current)
                return

            current = next

    @staticmethod
    def GetWordFromOffset(buf, offset):
        return buf[offset + 1] * 256 + buf[offset]

    @staticmethod
    def SetWordToOffset(buf, word, offset):
        buf[offset + 1] = word >> 8
        buf[offset + 0] = word % 256

    @staticmethod
    def LinkListRemoveObjectFromOffset(parent, offset):
        current = Helper.GetWordFromOffset(Data.BUF, parent)
        if current == offset:
            next = Helper.GetWordFromOffset(Data.BUF, current)
            Helper.SetWordToOffset(Data.BUF, next, parent)
            Helper.SetWordToOffset(Data.BUF, 0, current)
            return

        while current > 0:
            next = Helper.GetWordFromOffset(Data.BUF, current)
            if next == offset:
                Helper.SetWordToOffset(Data.BUF, Helper.GetWordFromOffset(Data.BUF, next), current)
                Helper.SetWordToOffset(Data.BUF, 0, next)
                return

            current = next

    @staticmethod
    def GetColorTextInformation(text):
        items = text.split("@")

        text_list = []

        index = len(items) - 1
        while True:
            if index == -1:
                ct = ColorText()
                ct.text = items[index + 1]

                text_list.append(ct)
                break

            if items[index].strip().startswith("C"):
                ct = ColorText()
                ct.text = items[index + 1]
                ct.fore_color = items[index].strip()[1:]

                text_list.append(ct)

                items.pop()
                items.pop()
            index -= 1

        text_list.reverse()

        return text_list

    @staticmethod
    def RenderColorText(text_list, x, y):
        x2 = x

        for ct in text_list:
            img = Helper.DrawText(ct.text, back_color=Helper.Palettes[int(ct.back_color)], palette_no=int(ct.fore_color))
            img = pygame.transform.scale(img, (img.get_width() * Helper.Scale, img.get_height() * Helper.Scale))

            Helper.Screen.blit(img, (x2, y))
            x2 += img.get_width()

        pygame.display.flip()

        img_width = int((x2 - x) / Helper.Scale)
        return img_width + 3
