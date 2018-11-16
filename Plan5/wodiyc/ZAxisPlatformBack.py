'''
ZAxisPlatform Back
'''

from wodiyc.ZAxisPlatformCommon import ZAxisPlatformCommon

class ZAxisPlatformBack(ZAxisPlatformCommon):
    '''ZAxisPlatform - Back

    The Z axis platform consists of two parts: the front, where the
    tool is mounted and the back where the rails are mounted.

    The Z axis Platform back consists of a base platform, two cutoffs
    for the rail mount and two set of holes.  One set fits the
    platform to the rail mount and the other set fits the back to the
    front
    '''

    def __init__(self, wodiyc):
        super().__init__(wodiyc)

    def tool_support_holes_callback(self, gf, x):
        # Notch
        gf.cylinder(
            x, self.toolsupportholes_distance_from_edge,
            self.toolsupportholes_notch_diameter,
            self.toolsupportholes_notch_depth)
        # Screw
        gf.cylinder(
            x, self.toolsupportholes_distance_from_edge,
            self.toolsupportholes_diameter, self.z_size,
            self.toolsupportholes_notch_depth)
        gf.free_movement()

    def upper_part_screws_callback(self, gf, x, y):
        # Screw
        gf.cylinder(
            x, y,
            self.screwholes_diameter, self.z_size,
            self.cutouts_depth)
        gf.free_movement()

    def upper_part_callback(self, gf, x):
        real_cutout_length = self.cutouts_length + self.cutouts_length_add
        gf.pocket(x - self.cutouts_width / 2,
                  self.y_size - real_cutout_length,
                  self.cutouts_width,
                  # Increase the cutout a bit to get a clean cut
                  real_cutout_length + 3,
                  self.cutouts_depth)
        gf.free_movement()

