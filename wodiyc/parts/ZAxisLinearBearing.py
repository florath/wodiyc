'''
Z Axis Linear Bearing
'''

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator, Direction


class ZAxisLinearBearing:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf = GCodeGenerator(
            host_cnc, "%s-side" % self.__class__.__name__,
            feed_rates_name=self.feed_rates,
            tool=self.tool)

        self.__gf_cut = GCodeGenerator(
            host_cnc, "%s-cut" % self.__class__.__name__,
            feed_rates_name=self.feed_rates,
            tool=self.tool)


    def generate(self):
        cleanup_runs = int(self.z_size / self.cleanup_depth)
        cleanup_depth_per_run = self.z_size / (cleanup_runs + 1)

        depth_end = 0
        for cl in range(cleanup_runs + 1):
            self.__gf.cylinder(
                self.threadhole_distance_from_top,
                self.threadhole_distance_from_edge,
                self.threadhole_diameter,
                (cl + 1) * cleanup_depth_per_run,
                depth_end, times=self.milling_times)
            self.__gf.free_movement()
            depth_end = (cl + 1) * cleanup_depth_per_run
            self.__gf.set_tool(self.tool_cleanup)
            self.__gf.set_tool(self.tool)

            #        self.__gf.cutout_rect(
            #            0, 0, 15, 15, self.z_size)
            #        self.__gf.free_movement()

        self.__gf_cut.cut_line(
            (Direction.top, ),
            0 - self.cut_offset , 0,
            self.bearing_leg + self.cut_offset, 0,
            self.cut_depth, 0, milling_times=self.milling_times,
            comment="Bearing leg cut off")
        self.__gf_cut.free_movement()

        self.__gf.close()
        self.__gf_cut.close()
