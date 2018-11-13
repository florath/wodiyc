'''
GCode File - overall settings
'''

class GCodeFile:

    def _w(self, s):
        self.__fd.write(s.encode())

    def __init__(self, filename,
                 feed_rate_work=500,
                 feed_rate_move=1000,
                 free_movement=7):
        self.__olabel = 0
        self.__feed_rate_work = feed_rate_work
        self.__feed_rate_move = feed_rate_move
        self.__free_movement = free_movement
        self.__fd = open(filename + ".ng", "wb")
        self._w("""G21
G17 G90
T1 M06
S12000.00 M03 G00 X0.000 Y0.000 Z7.000 F%d
Z%.5f
""" % (feed_rate_move, free_movement))

    def close(self):
        self._w("M2\n")
        self.__fd.close()

    def set_tool(self, tool_diameter, tool_diff, tool_depth=None):
        assert tool_diameter >= tool_diff
        self.__tool_diameter = tool_diameter
        self.__tool_diff = tool_diff
        self.__tool_depth = tool_depth if tool_depth is not None \
                            else tool_diameter / 2.0

    def next_o(self):
        self.__olabel += 1
        return "o%03d" % self.__olabel

    def free_movement(self):
        self._w("G0 Z%.5f\n" % (self.__free_movement))

    def cylinder(self, pos_x, pos_y, diameter, depth,
                 depth_start=0):
        '''Create a (hole) cylinder

        pos_x and pos_y are the center with the diameter and depth.
        '''
        tool_runs = int((depth - depth_start) / self.__tool_depth) + 1
        tool_depth_per_run = (depth-depth_start) / tool_runs
        
        self._w("(--- Create cylinder [%.5f, %.5f] diam [%.5f] depth [%.5f]"
                " depth start [%.5f])\n"
                 % (pos_x, pos_y, diameter, depth, depth_start))

        radius = diameter / 2.0
        tool_radius = self.__tool_diameter / 2.0
        real_x = pos_x - radius + tool_radius
        real_radius = radius - tool_radius

        # #4 is Z idx
        self._w("#4 = 1\n")
        z_olabel = self.next_o()
        self._w("%s while [#4 LE %d]\n" % (z_olabel, tool_runs))
        self._w("  F%d\n" % self.__feed_rate_move)
        self._w("  G0 X%.5f Y%.5f\n" % (real_x, pos_y))
        # #5 is Z
        self._w("  #5 = [-%.5f + #4 * -%.5f]\n"
                % (depth_start, tool_depth_per_run))
        self._w("  Z#5\n")

        # #1 is radius
        self._w("  #1 = %.5f\n" % radius)

        r_olabel = self.next_o()
        self._w("  %s while [#1 GT %.5f]\n"
                % (r_olabel, self.__tool_diff / 2.0))
        # #2 is real_x
        self._w("    #2 = [%.5f - #1]\n" % (pos_x + tool_radius))
        # #3 is real_radius
        self._w("    #3 = [#1 - %.5f]\n" % tool_radius)
        self._w("    F%d\n" % self.__feed_rate_work)
        self._w("    G1 X#2 Y%.5f\n" % (pos_y))
        self._w("    G2 X#2 Y%.5f I#3\n" % (pos_y))
        self._w("    #1 = [#1 - %.5f]\n" % (self.__tool_diff))
        self._w("  %s endwhile\n" % (r_olabel))
        self._w("  G1 X%.5f Y%.5f\n" % (pos_x, pos_y))
        self._w("  #4 = [#4 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)

    def pocket(self, low_x, low_y, size_x, size_y, depth, depth_start=0):
        '''Create a pocket'''
        tool_runs = int((depth - depth_start) / self.__tool_depth) + 1
        tool_depth_per_run = (depth-depth_start) / tool_runs
        
        self._w("(--- Create pocket [%.5f, %.5f] size [%.5f, %.5f] depth [%.5f]"
                " depth start [%.5f])\n"
                 % (low_x, low_y, size_x, size_y, depth, depth_start))

        tool_radius = self.__tool_diameter / 2.0
        real_x = low_x + tool_radius
        real_y = low_y + tool_radius

        # Goto initial position
        self._w("G0 X%.5f Y%.5f\n"
                % (low_x + tool_radius, low_y + tool_radius))
        
        # #1 - x (with tool diff included)
        self._w("#1 = %.5f\n" % (low_x + tool_radius))
        # #2 - y (with tool diff included)
        self._w("#2 = %.5f\n" % (low_y + tool_radius))
        # #3 - dx (with tool diff included)
        self._w("#3 = %.5f\n" % (size_x - self.__tool_diameter))
        # #4 - dy (with tool diff included)
        self._w("#4 = %.5f\n" % (size_y - self.__tool_diameter))
        # #5 - z idx
        self._w("#5 = 1\n")

        self._w("F%d\n" % self.__feed_rate_work)
        z_olabel = self.next_o()
        self._w("%s while [#5 LE %d]\n" % (z_olabel, tool_runs))
        # #5 is Z
        self._w("  #6 = [-%.5f + #5 * -%.5f]\n"
                % (depth_start, tool_depth_per_run))
        self._w("  Z#5\n")

        r_olabel = self.next_o()
        self._w("  %s while [#3 GE 0.0] AND [#4 GE 0.0]\n" % (r_olabel))
        # One square
        self._w("    G1 X#1 Y#2\n")
        self._w("    X[#1 + #3]\n")
        self._w("    Y[#2 + #4]\n")
        self._w("    X#1\n")
        self._w("    Y#2\n")

        # Re-compute
        self._w("    #1 = [#1 + %.5f]\n" % self.__tool_diff)
        self._w("    #2 = [#2 + %.5f]\n" % self.__tool_diff)
        self._w("    #3 = [#3 - %.5f]\n" % (2 * self.__tool_diff))
        self._w("    #4 = [#4 - %.5f]\n" % (2 * self.__tool_diff))

        self._w("  %s endwhile\n" % (r_olabel))
        self._w("  #5 = [#5 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)
