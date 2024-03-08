class CommenRegister(object):
    def __init__(self):
        self.__X = 0
        self.__H = 0
        self.__L = 0

    def getX(self):
        return self.__X

    def setX(self, value):
        self.__X = value & 0xffff
        self.__H = self.__X >> 8 & 0xff
        self.__L = self.__X & 0xff

    X = property(getX, setX)

    def getH(self):
        return self.__H

    def setH(self, value):
        self.__H = value & 0xff
        self.__X = ((self.__H << 8) + self.__L) & 0xffff

    H = property(getH, setH)

    def getL(self):
        return self.__L

    def setL(self, value):
        self.__L = value & 0xff
        self.__X = ((self.__H << 8) + self.__L) & 0xffff

    L = property(getL, setL)

class CpuRegister(object):
    def __init__(self):
        # ax = CommenRegister()
        # self.AX = property(ax.getX,ax.setX)
        # self.AH = property(ax.getH,ax.setH)
        # self.AL = property(ax.getL,ax.setL)
        #
        # bx = CommenRegister()
        # self.BX = property(bx.getX,bx.setX)
        # self.BH = property(bx.getH,bx.setH)
        # self.BL = property(bx.getL,bx.setL)
        #
        # cx = CommenRegister()
        # self.CX = property(cx.getX,cx.setX)
        # self.CH = property(cx.getH,cx.setH)
        # self.CL = property(cx.getL,cx.setL)
        #
        # dx = CommenRegister()
        # self.DX = property(dx.getX,dx.setX)
        # self.DH = property(dx.getH,dx.setH)
        # self.DL = property(dx.getL,dx.setL)

        self.__AX = 0
        self.__AH = 0
        self.__AL = 0
        self.__BX = 0
        self.__BH = 0
        self.__BL = 0
        self.__CX = 0
        self.__CH = 0
        self.__CL = 0
        self.__DX = 0
        self.__DH = 0
        self.__DL = 0
        self.SI = 0
        self.DI = 0
        self.CS = 0
        self.DS = 0
        self.ES = 0
        self.SS = 0

        self.stack = []

    def Push(self, obj):
        self.stack.append(obj)

    def Pop(self):
        return self.stack.pop()


    def getAX(self):
        return self.__AX

    def setAX(self, value):
        self.__AX = value & 0xffff
        self.__AH = self.__AX >> 8 & 0xff
        self.__AL = self.__AX & 0xff

    AX = property(getAX, setAX)

    def getAH(self):
        return self.__AH

    def setAH(self, value):
        self.__AH = value & 0xff
        self.__AX = ((self.__AH << 8) + self.__AL) & 0xffff

    AH = property(getAH, setAH)

    def getAL(self):
        return self.__AL

    def setAL(self, value):
        self.__AL = value & 0xff
        self.__AX = ((self.__AH << 8) + self.__AL) & 0xffff

    AL = property(getAL, setAL)

    def getBX(self):
        return self.__BX

    def setBX(self, value):
        self.__BX = value & 0xffff
        self.__BH = self.__BX >> 8 & 0xff
        self.__BL = self.__BX & 0xff

    BX = property(getBX, setBX)

    def getBH(self):
        return self.__BH

    def setBH(self, value):
        self.__BH = value & 0xff
        self.__BX = ((self.__BH << 8) + self.__BL) & 0xffff

    BH = property(getBH, setBH)

    def getBL(self):
        return self.__BL

    def setBL(self, value):
        self.__BL = value & 0xff
        self.__BX = ((self.__BH << 8) + self.__BL) & 0xffff

    BL = property(getBL, setBL)

    def getCX(self):
        return self.__CX

    def setCX(self, value):
        self.__CX = value & 0xffff
        self.__CH = self.__CX >> 8 & 0xff
        self.__CL = self.__CX & 0xff

    CX = property(getCX, setCX)

    def getCH(self):
        return self.__CH

    def setCH(self, value):
        self.__CH = value & 0xff
        self.__CX = ((self.__CH << 8) + self.__CL) & 0xffff

    CH = property(getCH, setCH)

    def getCL(self):
        return self.__CL

    def setCL(self, value):
        self.__CL = value & 0xff
        self.__CX = ((self.__CH << 8) + self.__CL) & 0xffff

    CL = property(getCL, setCL)

    def getDX(self):
        return self.__DX

    def setDX(self, value):
        self.__DX = value & 0xffff
        self.__DH = self.__DX >> 8 & 0xff
        self.__DL = self.__DX & 0xff

    DX = property(getDX, setDX)

    def getDH(self):
        return self.__DH

    def setDH(self, value):
        self.__DH = value & 0xff
        self.__DX = ((self.__DH << 8) + self.__DL) & 0xffff

    DH = property(getDH, setDH)

    def getDL(self):
        return self.__DL

    def setDL(self, value):
        self.__DL = value & 0xff
        self.__DX = ((self.__DH << 8) + self.__DL) & 0xffff

    DL = property(getDL, setDL)
