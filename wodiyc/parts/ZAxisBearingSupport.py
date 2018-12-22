'''
ZAxis Bearing Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


def measurements_ZAxisBearingSupport(m):
    '''Compute all the measurements for ZAxisBearingSupport'''
    p = m.ZAxisBearingSupport
    p.x_size \
        = p.cutout_depth + p.security_distance \
        + p.pipe_distance \
        + m.LinearBearing.half_width_inner \
        + p.bearing_distance_from_edge


class ZAxisBearingSupport:

    def __init__(self, host_cnc, measurements, config):
        self.m = measurements
        self.p = measurements.__getattr__(self.__class__.__name__)

        self.__gf_front = GCodeGenerator(
            host_cnc, "%s-Front" % self.__class__.__name__)
        self.__gf_back = GCodeGenerator(
            host_cnc, "%s-Back" % self.__class__.__name__)

    def platform(self):
        self.__gf_front.cutout_rect(
            0, 0, self.p.x_size, self.p.y_size, self.p.z_size)
        self.__gf_front.free_movement()

    def cross_nuts(self):
        for y in (self.p.y_size - self.p.cross_nut_distance_from_edge_y,
                  self.p.cross_nut_distance_from_edge_y):
            self.__gf_front.cylinder(
                self.p.x_size - self.p.cross_nut_distance_from_edge_x,
                y, self.p.cross_nut_diameter, self.p.z_size)
            self.__gf_front.free_movement()

    def bearing_screws(self):
        # Notch
        self.__gf_front.cylinder(
            self.m.LinearBearing.half_width_inner
            + self.p.bearing_distance_from_edge,
            self.p.y_size / 2,
            self.p.screwhole_notch_diameter, self.p.screwhole_notch_depth)
        # Screw
        self.__gf_front.cylinder(
            self.m.LinearBearing.half_width_inner
            + self.p.bearing_distance_from_edge,
            self.p.y_size / 2, self.p.screwhole_diameter,
            self.p.z_size,
            self.p.screwhole_notch_depth)
        self.__gf_front.free_movement()

    def cutouts(self):
        for y in (self.p.y_size - self.p.cutout_distance,
                  self.p.cutout_distance):
            self.__gf_front.pocket(-2, y - self.p.cutout_width / 2,
                                         self.p.x_size + 4, self.p.cutout_width,
                                         self.p.cutout_depth)
            self.__gf_front.free_movement()

            # Holes to fix the platform of the Z backlash nut
            for x in (self.p.cutout_screwhole_distance_from_edge + 10,
                      self.p.x_size - self.p.cutout_screwhole_distance_from_edge):
                self.__gf_front.cylinder(
                    x, y, self.p.screwhole_diameter, self.p.z_size,
                    self.p.cutout_depth)
                self.__gf_front.free_movement()

    def generate(self):
        self.cross_nuts()
        self.bearing_screws()
        self.cutouts()
        self.platform()
        self.__gf_front.close()

        for y in (self.p.y_size - self.p.cutout_distance,
                  self.p.cutout_distance):
            for x in (self.p.cutout_screwhole_distance_from_edge + 10,
                      self.p.x_size - self.p.cutout_screwhole_distance_from_edge):
                self.__gf_back.cylinder(
                    x, y, self.p.screwhole_notch_diameter,
                    self.p.screwhole_notch_depth_small)
                self.__gf_back.free_movement()

        self.__gf_back.set_tool(self.p.bearing_line_cut_tool)

        for x in (self.p.bearing_distance_from_edge,
                  self.p.bearing_distance_from_edge + 2 * self.m.LinearBearing.half_width_inner):
            self.__gf_back.line(
                x, -2, x, self.p.y_size + 2, self.m.LinearBearing.outer_inner_height_diff)
            self.__gf_back.free_movement()

        self.__gf_back.close()
