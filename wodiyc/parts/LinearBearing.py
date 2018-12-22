'''
Z Axis Linear Bearing
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator, Direction


def measurements_LinearBearing(m):
    '''Compute all the measurements for LinearBearing'''
    p = m.LinearBearing

    # The 'lower' or 'inner' legs length
    p.inner_leg_length = p.outer_leg_length - p.thickness
    
    # This is half the with of the bearing when they touch a plate
    p.half_width_inner \
        = math.sqrt(p.inner_leg_length * p.inner_leg_length / 2)
    print("LinearBearing half_width_inner [%.5f]" % p.half_width_inner)
    # Same for the outer (bigger) size
    p.half_width_outer \
        = math.sqrt(p.outer_leg_length * p.outer_leg_length / 2)
    print("LinearBearing half_width_outer [%.5f]" % p.half_width_outer)
    # Outer to inner depth: difference between the outer and inner triangle
    # in height.
    p.outer_inner_height_diff \
        = math.sqrt(p.thickness * p.thickness / 2)
    print("LinearBearing outer_inner_height_diff [%.5f]"
          % p.outer_inner_height_diff)


class LinearBearing:

    def __init__(self, host_cnc, measurements, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)

        self.__gf_right = {}
        self.__gf_left = {}
        
        for y_size in (self.y_size_short,
                       self.y_size_long):
            self.__gf_right[y_size] = GCodeGenerator(
                host_cnc, "%s-%d-Right" % (self.__class__.__name__, y_size),
                feed_rates_name=self.feed_rates,
                tool=self.tool)
            self.__gf_left[y_size] = GCodeGenerator(
                host_cnc, "%s-%d-Left" % (self.__class__.__name__, y_size),
                feed_rates_name=self.feed_rates,
                tool=self.tool)

    def holes(self, y_size, gf):
        cleanup_runs = int(self.z_size / self.cleanup_depth)
        cleanup_depth_per_run = self.z_size / (cleanup_runs + 1)

        for y in (self.threadhole_distance_from_top,
                  y_size - self.threadhole_distance_from_top):
            depth_end = 0
            for cl in range(cleanup_runs + 1):
                gf.cylinder(
                    self.threadhole_distance_from_edge, y,
                    self.threadhole_diameter,
                    (cl + 1) * cleanup_depth_per_run,
                    depth_end, times=self.milling_times)
                gf.free_movement()
                depth_end = (cl + 1) * cleanup_depth_per_run
                gf.set_tool(self.tool_cleanup)
                gf.set_tool(self.tool)

    def generate_one(self, y_size, gf_right, gf_left):
        self.holes(y_size, gf_right)
        self.holes(y_size, gf_left)

        gf_right.cut_line(
            ( ),
            0 - self.cut_offset, y_size / 2,
            self.marker_x, y_size / 2,
            self.marker_z, 0, milling_times=self.milling_times,
            comment="Marker")
        gf_right.free_movement()

        gf_right.cut_line(
            (Direction.top, ),
            0 - self.cut_offset, y_size,
            self.bearing_leg + self.cut_offset, y_size,
            self.cut_depth, 0, milling_times=self.milling_times,
            comment="Bearing leg cut off")
        gf_right.free_movement()

        gf_left.cut_line(
            (Direction.bottom, ),
            0 - self.cut_offset, 0,
            self.bearing_leg + self.cut_offset, 0,
            self.cut_depth, 0, milling_times=self.milling_times,
            comment="Bearing leg cut off")
        gf_left.free_movement()

        gf_right.close()
        gf_left.close()

    def generate(self):
        for y_size in (self.y_size_short,
                       self.y_size_long):
            self.generate_one(
                y_size,
                self.__gf_right[y_size], self.__gf_left[y_size])
