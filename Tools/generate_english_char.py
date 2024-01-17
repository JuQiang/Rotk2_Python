import pygame,sys

def str_2_bin(str):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in str])

def bin_2_str(bin):
    return ''.join([chr(i) for i in [int(b, 2) for b in bin.split(' ')]])

def main2():
    pygame.init()
    new_buf = []

    name_list = ["!","(",")",".","0","1","2","3","4","5","6","7","8","9","?","-","mao"]
    for name in name_list:
        num = pygame.image.load("{0}.bmp".format(name))
        print("Processing {0}".format(name))

        buf = []
        for h in range(0,num.get_height()):
            for w in range(0, num.get_width()):
                pixel = num.get_at((w,h))
                if pixel.r>127:
                    buf.append(1)
                else:
                    buf.append(0)
                print("{0}-{1}: {2}".format(w,h,pixel))

        bmp = pygame.Surface((8,14))
        bmp.fill((0,0,0))
        for m in range(0,14):
            s = ""
            for n in range(0,8):
                if buf[8*m+n]==1:
                    bmp.set_at((n,m),(255,255,255))
                else:
                    bmp.set_at((n, m), (0,0,0))
                s+=str(buf[8*m+n])
            new_buf.append(int(s,2))

        pygame.image.save(bmp,name+".png")

    # space
    for i in range(0,14):
        new_buf.append(i)
    with open("character.dat","wb") as f:
        f.write(bytes(new_buf))

def main():
    pygame.init()
    new_buf = []

    name_list = ["!","(",")",".","0","1","2","3","4","5","6","7","8","9","?","-","mao",","]
    for name in name_list:
        buf = pygame.image.load(name+".bmp").get_buffer().raw
        for b in buf:
            new_buf.append(b^0xff)

    for i in range(0,336):
        new_buf.append(0xff^0xff)

    with open("character.8p","wb") as f:
        f.write(bytes(new_buf))

def PreProcessNumberImage(self):
    bmp = pygame.image.load("number.png")
    # 24*91
    # Row starts from 103 at 2nd line

    for i in range(0, 6):
        n = bmp.subsurface((25 * i, 0, 25, 96)).copy()
        pygame.image.save(n, str(i) + ".png")

    for i in range(0, 4):
        n = bmp.subsurface((25 * i, 103, 25, 89)).copy()
        n2 = pygame.Surface((25, 96))
        n2.blit(n, (0, 4))
        pygame.image.save(n2, str(i + 6) + ".png")

    for i in range(0, 9):
        bmp_1 = pygame.image.load(str(i) + ".png")
        bmp_2 = pygame.Surface((25, 96))
        for r in range(0, 96):
            for j in range(0, 25):
                p = bmp_1.get_at((j, r))
                if p.r > 0 or p.g > 0 or p.b > 0:
                    p.r = p.g = p.b = 255
                bmp_2.set_at((j, r), (p.r, p.g, p.b))
        pygame.image.save(bmp_2, "new_{0}.png".format(i))
if __name__=="__main__":
    main()