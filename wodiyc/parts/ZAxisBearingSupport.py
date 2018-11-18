'''
ZAxis Bearing Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class ZAxisBearingSupport:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_right_front = GCodeGenerator(host_cnc)
        self.__gf_right_back = GCodeGenerator(host_cnc)

        self.__bearing_center \
            = math.sqrt(self.bearing_leg * self.bearing_leg / 2)
        
    def platform(self):
        self.__gf_right_front.cutout_rect(
            0, 0, self.x_size, self.y_size, self.z_size)
        self.__gf_right_front.free_movement()

    def cross_nuts(self):
        for y in (self.y_size - self.cross_nut_distance_from_edge_y,
                  self.cross_nut_distance_from_edge_y):
            self.__gf_right_front.cylinder(
                self.x_size - self.cross_nut_distance_from_edge_x,
                y, self.cross_nut_diameter, self.z_size)
            self.__gf_right_front.free_movement()

    def bearing_screws(self):
        # Notch
        self.__gf_right_front.cylinder(
            self.__bearing_center, self.y_size / 2,
            self.screwhole_notch_diameter, self.screwhole_notch_depth)
        # Screw
        self.__gf_right_front.cylinder(
            self.__bearing_center, self.y_size / 2, self.screwhole_diameter,
            self.z_size,
            self.screwhole_notch_depth)
        self.__gf_right_front.free_movement()

    def cutouts(self):
        for y in (self.y_size - self.cutout_distance,
                  self.cutout_distance):
            self.__gf_right_front.pocket(-2, y - self.cutout_width / 2,
                      self.x_size + 4, self.cutout_width,
                      self.cutout_depth)
            self.__gf_right_front.free_movement()

            # Holes to fix the platform of the Z backlash nut
            for x in (self.cutout_screwhole_distance_from_edge,
                      self.x_size - self.cutout_screwhole_distance_from_edge):
                self.__gf_right_front.cylinder(
                    x, y, self.screwhole_diameter, self.z_size,
                    self.cutout_depth)
                self.__gf_right_front.free_movement()

    def generate(self):
        self.__gf_right_front.open("%s-Right-Front" % self.__class__.__name__)
        self.cross_nuts()
        self.bearing_screws()
        self.cutouts()
        self.platform()
        self.__gf_right_front.close()

        self.__gf_right_back.open("%s-Right-Back" % self.__class__.__name__)
        for y in (self.y_size - self.cutout_distance,
                  self.cutout_distance):
            for x in (self.cutout_screwhole_distance_from_edge,
                      self.x_size - self.cutout_screwhole_distance_from_edge):
                self.__gf_right_back.cylinder(
                    x, y, self.screwhole_notch_diameter,
                    self.screwhole_notch_depth)
                self.__gf_right_back.free_movement()
            
        for x in (self.bearing_distance_from_edge,
                  self.bearing_distance_from_edge + 2 * self.__bearing_center):
            self.__gf_right_back.line(
                x, -2, x, self.y_size + 2, 3)
            self.__gf_right_back.free_movement()

        self.__gf_right_back.close()
