import platform

system = platform.system()

if system == 'Linux':
    if __file__.split('/')[-2] != 'mccaffertyp':
        print("Invalid file path")
        exit(0)

else:
    if __file__.split('\\')[-2] != 'mccaffertyp':
        print("Invalid file path")
        exit(0)
