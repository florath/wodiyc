'''
Anti Backlash Nut
'''

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator, Direction


def measurements_AntiBacklashNut(m):
    '''Compute all the measurements for LinearBearing'''
    p = m.AntiBacklashNut

    p.x_dist_holes = p.x_size - 2 * p.holes_distance_from_edge
    print("AntiBacklashNut x_dist_holes [%.5f]" % p.x_dist_holes)
    p.y_dist_holes = p.y_size - 2 * p.holes_distance_from_edge
    print("AntiBacklashNut y_dist_holes [%.5f]" % p.y_dist_holes)


class AntiBacklashNut:

    def __init__(self, host_cnc, measurements, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf = GCodeGenerator(
            host_cnc, "%s-Mount" % self.__class__.__name__,
            feed_rates_name=self.feed_rates,
            tool=self.tool)

    def generate(self):
        # This needs refactoring: extract to dedicated GCode.
        cleanup_runs = int(self.z_size / self.cleanup_depth)
        cleanup_depth_per_run = self.z_size / (cleanup_runs + 1)

        depth_end = 0
        for cl in range(cleanup_runs + 1):
            self.__gf.cylinder(
                self.threadhole_distance_from_edge,
                self.threadhole_distance_from_top,
                self.threadhole_diameter,
                (cl + 1) * cleanup_depth_per_run,
                depth_end, times=self.milling_times)
            self.__gf.free_movement()
            depth_end = (cl + 1) * cleanup_depth_per_run
            self.__gf.set_tool(self.tool_cleanup)
            self.__gf.set_tool(self.tool)

        for x in (self.holes_distance_from_edge,
                  self.x_size - self.holes_distance_from_edge):
            for y in (self.holes_distance_from_edge,
                      self.y_size - self.holes_distance_from_edge):
                depth_end = 0
                for cl in range(cleanup_runs + 1):
                    self.__gf.cylinder(
                        x, y,
                        self.holes_diameter,
                        (cl + 1) * cleanup_depth_per_run,
                        depth_end, times=self.milling_times)
                    self.__gf.free_movement()
                    depth_end = (cl + 1) * cleanup_depth_per_run
                    self.__gf.set_tool(self.tool_cleanup)
                    self.__gf.set_tool(self.tool)

        self.__gf.cut_line(
            (Direction.top, ),
            0 - self.cut_offset , self.y_size,
            self.x_size + self.cut_offset, self.y_size,
            self.cut_depth, 0, milling_times=self.milling_times,
            comment="Bearing leg cut off")
        self.__gf.free_movement()

        self.__gf.close()
