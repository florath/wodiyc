'''
ZAxisPlatform Back
'''

import woodiyc.ZAxisPlatformCommon

class ZAxisPlatformBack:
    '''ZAxisPlatform - Back

    The Z axis platform consists of two parts: the front, where the
    tool is mounted and the back where the rails are mounted.

    The Z axis Platform back consists of a base platform, two cutoffs
    for the rail mount and two set of holes.  One set fits the
    platform to the rail mount and the other set fits the back to the
    front
    '''
    
    def __init__(self, zacommon):
        self._zac = zacommon

    @staticmethod
    def _cb_tool_support_holes(zac, gf, x):
        # Notch
        gf.cylinder(
            x, zac._tool_support_hole_distance_from_edge,
            zac._tool_support_hole_notch_diameter,
            zac._tool_support_hole_notch_depth)
        # Screw
        gf.cylinder(
            x, zac._tool_support_hole_distance_from_edge,
            zac._tool_support_hole_diameter,  zac._platform_z,
            zac._tool_support_hole_notch_depth)
        gf.free_movement()

    @staticmethod
    def _cb_upper_part_screws(zac, gf, x, y):
        # Screw
        gf.cylinder(
            x, y,
            zac._screw_hole_diameter, zac._platform_z,
            zac._cutout_depth)
        gf.free_movement()

    @staticmethod
    def _cb_upper_part(zac, gf, x):
        real_cutout_length = zac._cutout_length + zac._cutout_length_add
        gf.pocket(x - zac._cutout_width / 2,
                  zac._platform_y - real_cutout_length,
                  zac._cutout_width,
                  # Increase the cutout a bit to get a clean cut
                  real_cutout_length + 3,
                  zac._cutout_depth)
        gf.free_movement()

    def generate_gcode(self, gf):
        zac = self._zac
        # Screw holes for the tool support
        zac._tool_support_holes(gf, ZAxisPlatformBack._cb_tool_support_holes)

        # Lower holes for screws to fit front and back together
        zac._lower_screw_holes(gf)

        # Pockets and screws
        zac._upper_part(gf, ZAxisPlatformBack._cb_upper_part,
                        ZAxisPlatformBack._cb_upper_part_screws)
        
        # Platform
        zac._platform(gf)
