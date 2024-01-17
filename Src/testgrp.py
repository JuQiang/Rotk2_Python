from Data import Data

def main():
    off = 0x696a
    w=0x50
    h=0x38
    bp6 = 0x200
    bp8=0x04

    a = int((w+3)/4)
    ax = int(bp8/2)*16*10
    bx = int(bp6/4)
    di = ax+bx
    if bp8%2==1:
        di += 0x4000

    for name in Data.GrpdataMappings.keys():
        print(name)
        map = Data.GrpdataMappings[name]
        w = (Data.GRPDATA[map[0]+1]<<8)+Data.GRPDATA[map[0]+0]
        h = (Data.GRPDATA[map[0]+3]<<8)+Data.GRPDATA[map[0]+2]
        bp8 = map[1]

        map[2] = int((w+3)/4)

        ax = int(bp8/2)*16*10
        bx = 0x128/4
        di = ax+bx+0x4000

if __name__=="__main__":
    main()