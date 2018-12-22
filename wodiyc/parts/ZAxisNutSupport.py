'''
ZAxis Nut Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


def measurements_ZAxisNutSupport(m):
    '''Compute all the measurements for ZAxisNutSupport'''
    p = m.ZAxisNutSupport

    # Same as the ZAxisBearing support without the cutout-depth
    p.x_size = m.ZAxisBearingSupport.x_size \
               - m.ZAxisBearingSupport.cutout_depth
    print("ZAxisNutSupport x_size [%.5f]" % p.x_size)
    p.y_size = m.ZAxisPlatform.cutouts_distance \
               + 2 * p.cutout_depth \
               - m.ZAxisBearingSupport.z_size
    print("ZAxisNutSupport y_size [%.5f]" % p.y_size)
    p.z_size = m.Common.base_material_thickness

class ZAxisNutSupport:

    def __init__(self, host_cnc, measurements, config):
        self.m = measurements
        self.p = measurements.__getattr__(self.__class__.__name__)

        self.__gf_upper = GCodeGenerator(
            host_cnc, "%s-Upper" % self.__class__.__name__)
        self.__gf_lower = GCodeGenerator(
            host_cnc, "%s-Lower" % self.__class__.__name__)

    def generate(self):
        p = self.p
        m = self.m
        # Holes for fixing the nut
        x_center = m.ZAxisBearingSupport.bearing_center_offset
        y_center = p.y_size / 2
        x_diff = m.AntiBacklashNut.x_size / 2 - m.AntiBacklashNut.holes_distance_from_edge
        y_diff = m.AntiBacklashNut.y_size / 2 - m.AntiBacklashNut.holes_distance_from_edge
        for x in (x_center - x_diff, x_center + x_diff):
            for y in (y_center - y_diff, y_center + y_diff):
                self.__gf_upper.cylinder(
                    x, y, m.Common.screwhole_diameter, p.z_size)
                self.__gf_upper.free_movement()

        for gf in (self.__gf_upper, self.__gf_lower):
            # Central hole
            gf.cylinder(x_center, y_center,
                        p.central_hole_diameter, p.z_size)
            gf.free_movement()

            # Crossnuts to fix the platform of the Z axis bearing support
            for x in (m.ZAxisBearingSupport.bearing_center_offset,
                      m.ZAxisBearingSupport.bearing_center_offset
                      - m.AntiBacklashNut.x_dist_holes):
                for y in (p.cross_nut_distance_from_edge,
                          p.y_size - p.cross_nut_distance_from_edge):
                    gf.cylinder(
                        x, y, p.cross_nut_diameter, p.z_size)
                    gf.free_movement()

            # Platform
            gf.cutout_rect(0, 0, p.x_size, p.y_size, p.z_size)
            gf.free_movement()

            gf.comment("ZAxisNutSupport x_size [%.5f] y_size [%.5f]"
                       % (p.x_size, p.y_size))

        self.__gf_upper.close()
        self.__gf_lower.close()
