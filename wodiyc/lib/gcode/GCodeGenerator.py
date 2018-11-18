'''
GCode File - overall settings
'''
import os
import pathlib


# pylint: disable=too-many-instance-attributes
class GCodeGenerator:
    '''Generate GCode'''

    def _w(self, wstr):
        self.__fd.write(wstr.encode())

    def __init__(self, config, filename, output_dir="NGC"):

        self.__olabel = 0

        self.__feed_rate_work = config['feed_rates']['work']
        self.__feed_rate_move = config['feed_rates']['move']
        self.__free_movement = config['free_movement']

        self.__tool_diameter = config['tools'][1]['diameter']
        self.__tool_diff = config['tools'][1]['diff']
        assert self.__tool_diameter >= self.__tool_diff
        self.__tool_depth = config['tools'][1]['depth']

        self.__output_dir = output_dir
        pathlib.Path(self.__output_dir).mkdir(parents=True, exist_ok=True)

        self.__fd = open(os.path.join(
            self.__output_dir, filename + ".ngc"), "wb")
        self._w("""G21
G17 G90
T1 M06
S12000.00 M03 G00 X0.000 Y0.000 Z7.000 F%d
Z%.5f
""" % (self.__feed_rate_move, self.__free_movement))

    def close(self):
        '''Close the file

        Write the tailer and close the file
        '''
        self._w("M2\n")
        self.__fd.close()

    def next_o(self):
        '''Get next O label

        O Labels must be unique in the file.
        It looks that the max number is 999
        '''
        self.__olabel += 1
        assert self.__olabel <= 999
        return "o%03d" % self.__olabel

    def free_movement(self):
        '''Move the tool to standard free movement hight'''
        self._w("G0 Z%.5f\n" % (self.__free_movement))

    def compute_tool_runs(self, depth):
        '''Compute how many runs of the tool need to go to given depth'''
        tool_runs = int((depth) / self.__tool_depth) + 1
        tool_depth_per_run = (depth) / tool_runs
        return tool_runs, tool_depth_per_run

    # pylint: disable=too-many-arguments
    def cylinder(self, pos_x, pos_y, diameter, depth,
                 depth_start=0):
        '''Create a (hole) cylinder

        pos_x and pos_y are the center with the diameter and depth.
        '''
        tool_runs, tool_depth_per_run \
            = self.compute_tool_runs(depth - depth_start)

        self._w("(--- Create cylinder [%.5f, %.5f] diam [%.5f] depth [%.5f]"
                " depth start [%.5f])\n"
                % (pos_x, pos_y, diameter, depth, depth_start))

        radius = diameter / 2.0
        tool_radius = self.__tool_diameter / 2.0
        real_x = pos_x - radius + tool_radius

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
        self._w("    G3 X#2 Y%.5f I#3\n" % (pos_y))
        self._w("    #1 = [#1 - %.5f]\n" % (self.__tool_diff))
        self._w("  %s endwhile\n" % (r_olabel))
        self._w("  G1 X%.5f Y%.5f\n" % (pos_x, pos_y))
        self._w("  #4 = [#4 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)

    # pylint: disable=too-many-arguments
    def pocket(self, low_x, low_y, size_x, size_y, depth, depth_start=0):
        '''Create a pocket'''
        tool_runs, tool_depth_per_run \
            = self.compute_tool_runs(depth - depth_start)

        self._w("(--- Create pocket [%.5f, %.5f] size [%.5f, %.5f] "
                "depth [%.5f] depth start [%.5f])\n"
                % (low_x, low_y, size_x, size_y, depth, depth_start))

        tool_radius = self.__tool_diameter / 2.0

        # Goto initial position
        self._w("G0 X%.5f Y%.5f\n"
                % (low_x + tool_radius, low_y + tool_radius))

        # #5 - z idx
        self._w("#5 = 1\n")

        self._w("F%d\n" % self.__feed_rate_work)
        z_olabel = self.next_o()
        self._w("%s while [#5 LE %d]\n" % (z_olabel, tool_runs))
        # #1 - x (with tool diff included)
        self._w("  #1 = %.5f\n" % (low_x + tool_radius))
        # #2 - y (with tool diff included)
        self._w("  #2 = %.5f\n" % (low_y + tool_radius))
        # #3 - dx (with tool diff included)
        self._w("  #3 = %.5f\n" % (size_x - self.__tool_diameter))
        # #4 - dy (with tool diff included)
        self._w("  #4 = %.5f\n" % (size_y - self.__tool_diameter))
        # #6 is Z
        self._w("  #6 = [-%.5f + #5 * -%.5f]\n"
                % (depth_start, tool_depth_per_run))
        self._w("  Z#6\n")

        r_olabel = self.next_o()
        self._w("  %s while [#3 GE 0.0 AND #4 GE 0.0]\n" % (r_olabel))
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

    # pylint: disable=too-many-arguments
    def cutout_rect(self, low_x, low_y, size_x, size_y,
                    depth, depth_start=0,
                    bridges_width=2.5, bridges_height=2.5,
                    bridges_distance=70):
        '''Create a rect coutout

        Bridges are included.
        '''
        bridges_start_z = depth - bridges_height - depth_start
        tool_runs, tool_depth_per_run \
            = self.compute_tool_runs(bridges_start_z)

        self._w("(--- Create rect cutout [%.5f, %.5f] "
                "size [%.5f, %.5f] depth [%.5f]"
                " depth start [%.5f])\n"
                % (low_x, low_y, size_x, size_y, depth, depth_start))

        tool_radius = self.__tool_diameter / 2.0

        self._w("G0 X%.5f Y%.5f\n"
                % (low_x - tool_radius, low_y - tool_radius))

        # *** The part of the rect that does not touch the bridges

        # #5 - z idx
        self._w("#5 = 1\n")

        self._w("F%d\n" % self.__feed_rate_work)
        z_olabel = self.next_o()
        self._w("%s while [#5 LE %d]\n" % (z_olabel, tool_runs))
        # #6 is Z
        self._w("  #6 = [-%.5f + #5 * -%.5f]\n"
                % (depth_start, tool_depth_per_run))
        self._w("  Z#6\n")
        self._w("  G1 X%.5f Y%.5f\n" %
                (low_x - tool_radius, low_y - tool_radius))
        self._w("  X%.5f\n" % (low_x + size_x + tool_radius))
        self._w("  Y%.5f\n" % (low_y + size_y + tool_radius))
        self._w("  X%.5f\n" % (low_x - tool_radius))
        self._w("  Y%.5f\n" % (low_y - tool_radius))
        self._w("  #5 = [#5 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)

        # *** Bridges handling
        tool_runs, tool_depth_per_run \
            = self.compute_tool_runs(bridges_height)

        # Compute bridges
        bridges_cnt_x = int(size_x / bridges_distance) + 1
        bridges_cnt_y = int(size_y / bridges_distance) + 1

        # #5 - z idx
        self._w("#5 = 1\n")

        z_olabel = self.next_o()
        self._w("%s while [#5 LE %d]\n" % (z_olabel, tool_runs))
        # #6 is Z
        self._w("  #6 = [-%.5f + #5 * -%.5f]\n"
                % (bridges_start_z, tool_depth_per_run))
        self._w("  Z#6\n")
        self._w("  G1 X%.5f Y%.5f\n" %
                (low_x - tool_radius, low_y - tool_radius))

        delta_x_down = size_x / bridges_cnt_x - bridges_width / 2
        delta_x_offset = delta_x_down / 2
        delta_x_bridge = 2 * tool_radius + bridges_width

        delta_y_down = size_y / bridges_cnt_y - bridges_width / 2
        delta_y_offset = delta_y_down / 2
        delta_y_bridge = 2 * tool_radius + bridges_width

        for cutidx in range(bridges_cnt_x):
            self._w("  X%.5f\n" %
                    (low_x + delta_x_down * cutidx + delta_x_offset))
            self._w("  Z-%.5f\n" % (bridges_start_z))
            self._w("  X%.5f\n" %
                    (low_x + delta_x_down * cutidx
                     + delta_x_bridge + delta_x_offset))
            self._w("  Z#6\n")
        self._w("  X%.5f\n" % (low_x + size_x + tool_radius))

        for cutidx in range(bridges_cnt_y):
            self._w("  Y%.5f\n" % (low_y + delta_y_down * cutidx
                                   + delta_y_offset))
            self._w("  Z-%.5f\n" % (bridges_start_z))
            self._w("  Y%.5f\n" % (low_y + delta_y_down * cutidx
                                   + delta_y_bridge + delta_y_offset))
            self._w("  Z#6\n")
        self._w("  Y%.5f\n" % (low_y + size_y + tool_radius))

        for cutidx in range(bridges_cnt_x):
            self._w("  X%.5f\n" %
                    (low_x + delta_x_down *
                     (bridges_cnt_x-cutidx-1) + delta_x_offset
                     + delta_x_bridge))
            self._w("  Z-%.5f\n" % (bridges_start_z))
            self._w("  X%.5f\n" %
                    (low_x + delta_x_down
                     * (bridges_cnt_x-cutidx-1) + delta_x_offset))
            self._w("  Z#6\n")
        self._w("  X%.5f\n" % (low_x - tool_radius))

        for cutidx in range(bridges_cnt_y):
            self._w("  Y%.5f\n" % (low_y + delta_y_down
                                   * (bridges_cnt_y-cutidx-1)
                                   + delta_y_offset + delta_x_bridge))
            self._w("  Z-%.5f\n" % (bridges_start_z))
            self._w("  Y%.5f\n"
                    % (low_y + delta_y_down
                       * (bridges_cnt_y-cutidx-1) + delta_y_offset))
            self._w("  Z#6\n")
        self._w("  Y%.5f\n" % (low_y - tool_radius))

        self._w("  #5 = [#5 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)

    # pylint: disable=too-many-arguments
    def line(self, start_x, start_y, end_x, end_y, depth,
             depth_start=0):
        '''Create a line using the current tool'''
        tool_runs, tool_depth_per_run \
            = self.compute_tool_runs(depth - depth_start)

        self._w("(--- Create line [%.5f, %.5f] to [%.5f, %.5f] depth [%.5f]"
                " depth start [%.5f])\n"
                % (start_x, start_y, end_x, end_y, depth, depth_start))

        # Position tool
        self._w("F%d\n" % self.__feed_rate_move)
        self._w("G0 X%.5f Y%.5f\n" % (start_x, start_y))
        # #4 is Z idx
        self._w("#4 = 1\n")
        z_olabel = self.next_o()
        self._w("%s while [#4 LE %d]\n" % (z_olabel, tool_runs))
        # #5 is Z
        self._w("  #5 = [-%.5f + #4 * -%.5f]\n"
                % (depth_start, tool_depth_per_run))
        self._w("  Z#5\n")
        self._w("  G1 X%.5f Y%.5f\n" % (end_x, end_y))
        self._w("  #4 = [#4 + 1]\n")
        zif_olabel = self.next_o()
        self._w("  %s if [#4 GT %d]\n" % (zif_olabel, tool_runs))
        self._w("    %s break\n" % z_olabel)
        self._w("  %s endif\n" % (zif_olabel))
        self._w("  G1 X%.5f Y%.5f\n" % (start_x, start_y))
        self._w("  #4 = [#4 + 1]\n")
        self._w("%s endwhile\n" % z_olabel)
