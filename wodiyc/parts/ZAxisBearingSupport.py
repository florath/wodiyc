'''
ZAxis Bearing Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class ZAxisBearingSupport:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_front = GCodeGenerator(
            host_cnc, "%s-Front" % self.__class__.__name__)
        self.__gf_back = GCodeGenerator(
            host_cnc, "%s-Back" % self.__class__.__name__)

        self.__bearing_center \
            = math.sqrt(self.bearing_leg * self.bearing_leg / 2)
        print("BEARING CENTER", self.__bearing_center)
        self.__cut_depth \
            = math.sqrt(self.bearing_thick * self.bearing_thick / 2)
        print("CUT DEPTH", self.__cut_depth)

        self.computed_x_size \
            = self.cutout_depth + self.security_distance \
            + self.pipe_distance \
            + self.__bearing_center + self.bearing_distance_from_edge
        print("COMPUTED SIZE", self.computed_x_size)
        

    def platform(self):
        self.__gf_front.cutout_rect(
            0, 0, self.x_size, self.y_size, self.z_size)
        self.__gf_front.free_movement()

    def cross_nuts(self):
        for y in (self.y_size - self.cross_nut_distance_from_edge_y,
                  self.cross_nut_distance_from_edge_y):
            self.__gf_front.cylinder(
                self.x_size - self.cross_nut_distance_from_edge_x,
                y, self.cross_nut_diameter, self.z_size)
            self.__gf_front.free_movement()

    def bearing_screws(self):
        # Notch
        self.__gf_front.cylinder(
            self.__bearing_center + self.bearing_distance_from_edge,
            self.y_size / 2,
            self.screwhole_notch_diameter, self.screwhole_notch_depth)
        # Screw
        self.__gf_front.cylinder(
            self.__bearing_center + self.bearing_distance_from_edge,
            self.y_size / 2, self.screwhole_diameter,
            self.z_size,
            self.screwhole_notch_depth)
        self.__gf_front.free_movement()

    def cutouts(self):
        for y in (self.y_size - self.cutout_distance,
                  self.cutout_distance):
            self.__gf_front.pocket(-2, y - self.cutout_width / 2,
                                         self.x_size + 4, self.cutout_width,
                                         self.cutout_depth)
            self.__gf_front.free_movement()

            # Holes to fix the platform of the Z backlash nut
            for x in (self.cutout_screwhole_distance_from_edge + 10,
                      self.x_size - self.cutout_screwhole_distance_from_edge):
                self.__gf_front.cylinder(
                    x, y, self.screwhole_diameter, self.z_size,
                    self.cutout_depth)
                self.__gf_front.free_movement()

    def generate(self):
        self.cross_nuts()
        self.bearing_screws()
        self.cutouts()
        self.platform()
        self.__gf_front.close()

        for y in (self.y_size - self.cutout_distance,
                  self.cutout_distance):
            for x in (self.cutout_screwhole_distance_from_edge + 10,
                      self.x_size - self.cutout_screwhole_distance_from_edge):
                self.__gf_back.cylinder(
                    x, y, self.screwhole_notch_diameter,
                    self.screwhole_notch_depth_small)
                self.__gf_back.free_movement()

        self.__gf_back.set_tool(self.bearing_line_cut_tool)

        for x in (self.bearing_distance_from_edge,
                  self.bearing_distance_from_edge + 2 * self.__bearing_center):
            self.__gf_back.line(
                x, -2, x, self.y_size + 2, self.__cut_depth)
            self.__gf_back.free_movement()

        self.__gf_back.close()
