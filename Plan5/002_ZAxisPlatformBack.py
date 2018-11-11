from woodiyc.ZAxisPlatformBack import ZAxisPlatformBack
from woodiyc.gcode.GCodeFile import GCodeFile

def main():
    obj = ZAxisPlatformBack()
    gf = GCodeFile("ZAxisPlatformBack")
    gf.set_tool(3.175, 2.5)
    obj.generate_gcode(gf)
    gf.close()

if __name__ == '__main__':
    main()
