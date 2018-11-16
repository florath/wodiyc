from woodiyc.Reference import Reference
from woodiyc.gcode.GCodeFile import GCodeFile

def main():
    obj = Reference()
    gf = GCodeFile("Reference")
    # gf.set_tool(3.175, 2.5)
    gf.set_tool(2.5, 2.5, 3.175 / 8)
    obj.generate_gcode(gf)
    gf.close()

if __name__ == '__main__':
    main()
