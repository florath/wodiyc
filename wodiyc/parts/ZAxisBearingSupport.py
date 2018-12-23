'''
ZAxis Bearing Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


def measurements_ZAxisBearingSupport(m):
    '''Compute all the measurements for ZAxisBearingSupport'''
    p = m.ZAxisBearingSupport
    p.bearing_center_offset \
        = m.Common.moving_parts_security_distance \
        + m.Common.pipe_distance
    print("ZAxisBearingSupport bearing center offset [%.5f]"
          % p.bearing_center_offset)
    p.cutout_depth = m.Common.base_material_cutout_depth
    p.x_size \
        = p.cutout_depth + p.bearing_center_offset \
        + m.LinearBearing.half_width_outer \
        + p.bearing_distance_from_edge
    print("ZAxisBearingSupport x_size [%.5f]" % p.x_size)
    p.y_size = m.LinearBearing.length_x_axis
    print("ZAxisBearingSupport y_size [%.5f]" % p.y_size)
    p.z_size = m.Common.base_material_thickness
    p.cross_nut_distance_from_edge_y \
        = m.Common.cross_nut_distance_from_edge
    p.cutout_width = m.Common.base_material_thickness

 
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
        for y in (self.p.y_size - self.m.Common.cross_nut_distance_from_edge,
                  self.m.Common.cross_nut_distance_from_edge):
            self.__gf_front.cylinder(
                self.p.cross_nut_distance_from_edge_x,
                y, self.m.Common.cross_nut_diameter, self.p.z_size)
            self.__gf_front.free_movement()

    def bearing_screw(self):
        # Notch
        self.__gf_front.cylinder(
            self.p.bearing_center_offset + self.p.cutout_depth,
            self.p.y_size / 2,
            self.m.Common.screwhole_notch_diameter_washer,
            self.m.Common.screwhole_notch_depth)
        # Screw
        self.__gf_front.cylinder(
            self.p.bearing_center_offset + self.p.cutout_depth,
            self.p.y_size / 2, self.m.Common.screwhole_diameter,
            self.p.z_size,
            self.m.Common.screwhole_notch_depth)
        self.__gf_front.free_movement()

    def cutouts(self):
        for y in (self.p.y_size - self.p.cutout_distance,
                  self.p.cutout_distance):
            self.__gf_front.pocket(-2, y - self.p.cutout_width / 2,
                                         self.p.x_size + 4, self.p.cutout_width,
                                         self.p.cutout_depth)
            self.__gf_front.free_movement()

            # Holes to fix the platform of the Z backlash nut
            for x in (self.p.bearing_center_offset + self.p.cutout_depth,
                      self.p.bearing_center_offset + self.p.cutout_depth
                      - self.m.AntiBacklashNut.x_dist_holes):
                self.__gf_front.cylinder(
                    x, y, self.m.Common.screwhole_diameter, self.p.z_size,
                    self.p.cutout_depth)
                self.__gf_front.free_movement()

    def generate_front(self):
        self.cross_nuts()
        self.bearing_screw()
        self.cutouts()
        self.platform()
        self.__gf_front.close()

    def generate_back(self):
        for y in (self.p.y_size - self.p.cutout_distance,
                  self.p.cutout_distance):
            for x in (self.p.bearing_center_offset + self.p.cutout_depth,
                      self.p.bearing_center_offset + self.p.cutout_depth
                      - self.m.AntiBacklashNut.x_dist_holes):
                self.__gf_back.cylinder(
                    x, y, self.m.Common.screwhole_notch_diameter,
                    self.p.screwhole_notch_depth_small)
                self.__gf_back.free_movement()

        self.__gf_back.set_tool(self.p.bearing_line_cut_tool)

        offset = self.p.bearing_center_offset + self.p.cutout_depth
        for x in (offset + self.m.LinearBearing.half_width_inner,
                  offset - self.m.LinearBearing.half_width_inner):
            self.__gf_back.line(
                x, -2, x, self.p.y_size + 2, self.m.LinearBearing.outer_inner_height_diff)
            self.__gf_back.free_movement()

        self.__gf_back.close()

    def generate(self):
        self.generate_front()
        self.generate_back()

