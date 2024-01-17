def main():
    SEG1 = 0x76c0 # Reference "How to find base CS segment in debug.exe"
    SEG2 = 0x10000 - SEG1

    content = ""
    with open("../References/main.asm","r") as f:
        content = f.readlines()

    content_new = []
    for line in content:
        csip = ""
        if line.startswith("s_"):
            index = line.find("\t\t")
            # some functions will show as
            # s_1596C:
            # instead of
            # s_1596C proc far
            if index<0:
                index = line.find(":")

            addr = int(line[2:index],16)
            addr += SEG1
            csip = get_dos_csip(addr)
        elif line.startswith("loc_"):
            index = line.find(":")
            if index>-1:
                addr = int(line[4:index],16)
                addr -= SEG2
                csip = get_dos_csip(addr)

        content_new.append(line.strip()+csip)

    with open ("../References/main_csip_refactoring.asm", "w") as f:
        f.writelines("\n".join(content_new))

def get_dos_csip(addr):
    addr_str = "{0:X}".format(addr)
    csip = "\t\t /* DOS offset ---> {0}:{1} */".format(addr_str[0:-1],addr_str[-1])

    return csip

if __name__=="__main__":
    main()