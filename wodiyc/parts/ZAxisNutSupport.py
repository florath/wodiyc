'''
ZAxis Nut Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class ZAxisNutSupport:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_upper = GCodeGenerator(
            host_cnc, "%s-Upper" % self.__class__.__name__)
        self.__gf_lower = GCodeGenerator(
            host_cnc, "%s-Lower" % self.__class__.__name__)

        self.y_size = self.z_axis_platform_cutouts_distance \
                      + 2 * self.cutout_depth
        # Mostly duplicate to ZAxisBearingSupport
        self.__bearing_center \
            = math.sqrt(self.bearing_leg * self.bearing_leg / 2)
        self.x_size \
            = self.security_distance \
            + self.pipe_distance \
            + self.__bearing_center + self.bearing_distance_from_edge

        self.zabs_x_size \
            = self.cutout_depth + self.security_distance \
            + self.pipe_distance \
            + self.__bearing_center + self.bearing_distance_from_edge

    def generate(self):
        # Holes for fixing the nut
        x_center = self.security_distance + self.pipe_distance
        y_center = self.y_size / 2
        x_diff = self.abn_x_size / 2 - self.abn_holes_distance_from_edge
        y_diff = self.abn_y_size / 2 - self.abn_holes_distance_from_edge
        for x in (x_center - x_diff, x_center + x_diff):
            for y in (y_center - y_diff, y_center + y_diff):
                self.__gf_upper.cylinder(
                    x, y, self.abn_holes_diameter, self.z_size)
                self.__gf_upper.free_movement()
        
        for gf in (self.__gf_upper, self.__gf_lower):
            # Platform
            gf.cutout_rect(0, 0, self.x_size, self.y_size, self.z_size)
            gf.free_movement()
            # Central hole
            gf.cylinder(x_center, y_center,
                        self.central_hole_diameter, self.z_size)
            gf.free_movement()

            # Crossnuts to fix the platform of the Z axis bearing support
            for x in (self.zabs_cutout_screwhole_distance_from_edge,
                      self.zabs_x_size - self.zabs_cutout_screwhole_distance_from_edge - 10):
                for y in (self.cross_nut_distance_from_edge,
                          self.y_size - self.cross_nut_distance_from_edge):
                    gf.cylinder(
                        x, y, self.cross_nut_diameter, self.z_size)
                    gf.free_movement()
            
        self.__gf_upper.close()
        self.__gf_lower.close()
