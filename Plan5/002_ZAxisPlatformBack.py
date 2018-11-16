from woodiyc.ZAxisPlatformCommon import ZAxisPlatformCommon
from woodiyc.ZAxisPlatformBack import ZAxisPlatformBack
from woodiyc.gcode.GCodeFile import GCodeFile

def main():
    zac = ZAxisPlatformCommon()
    obj = ZAxisPlatformBack(zac)
    gf = GCodeFile("ZAxisPlatformBack")
    gf.set_tool(2.675, 2.5, 3.175 / 8)
    obj.generate_gcode(gf)
    gf.close()

if __name__ == '__main__':
    main()
