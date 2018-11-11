#!/usr/bin/python3

def create_hole(fd, pos_x, pos_y, diameter, depth,
                tool_diameter, tool_diff, tool_depth=None):
    # Basic tool computation and optimization
    if not tool_depth:
        tool_depth = tool_diameter / 2
    tool_runs = int(depth / tool_depth) + 1
    tool_depth_per_run = depth / tool_runs
        
    fd.write("(--- Create hole [%.3f, %.3f] diam [%.3f] depth [%.3f])\n"
             % (pos_x, pos_y, diameter, depth))
    assert tool_diameter >= tool_diff
    radius = diameter / 2.0
    tool_radius = tool_diameter / 2.0
    real_x = pos_x - radius + tool_radius
    real_radius = radius - tool_radius

    # #4 is Z
    fd.write("#4 = -%.3f\n" % tool_depth_per_run)
    fd.write("o001 while [#4 GE -%.3f]\n" % (depth))
    fd.write("  G1 X%.3f Y%.3f\n" % (real_x, pos_y))
    fd.write("  Z#4\n")

    # #1 is radius
    fd.write("  #1 = %.3f\n" % radius)

    fd.write("  o002 while [#1 GT %.3f]\n" % (tool_diff / 2.0))
    # #2 is real_x
    fd.write("    #2 = [%.3f - #1]\n" % (pos_x + tool_radius))
    # #3 is real_radius
    fd.write("    #3 = [#1 - %.3f]\n" % tool_radius)
    fd.write("    G1 X#2 Y%.3f\n" % (pos_y))
    fd.write("    G2 X#2 Y%.3f I#3\n" % (pos_y))
    fd.write("    #1 = [#1 - %.3f]\n" % (tool_diff))
    fd.write("  o002 endwhile\n")
    fd.write("  G1 X%.3f Y%.3f\n" % (pos_x, pos_y))
    fd.write("  #4 = [#4 - %.3f]\n" %(tool_depth_per_run))
    fd.write("o001 endwhile\n")

def main():
    with open("q.ng", "w+") as fd:
        fd.write("""
G21
G17 G90
T1 M06
S12000.00 M03 G00 X0.000 Y0.000 Z7.000 F1000
Z7
""")
        create_hole(fd, 10, 20, 30, 15, 3.175, 3)
        fd.write("M2\n")

if __name__ == '__main__':
    main()
