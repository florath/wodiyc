'''
ZAxisPlatform Front
'''

from wodiyc.lib.ZAxisPlatformCommon import ZAxisPlatformCommon

class ZAxisPlatformFront(ZAxisPlatformCommon):
    '''ZAxisPlatform - Front

    The Z axis platform consists of two parts: the front, where the
    tool is mounted and the back where the rails are mounted.
    '''

    def __init__(self, wodiyc):
        super().__init__(wodiyc)

    def tool_support_holes_callback(self, gf, x):
        # Screw
        gf.cylinder(
            x, self.toolsupportholes_distance_from_edge,
            self.toolsupportholes_diameter, self.z_size, 0)
        gf.free_movement()

    def upper_part_screws_callback(self, gf, x, y):
        # Notch
        gf.cylinder(
            x, y,
            self.screwholes_notch_diameter, self.screwholes_notch_depth)
        # Screw
        gf.cylinder(
            x, y,
            self.screwholes_diameter, self.z_size,
            self.screwholes_notch_depth)
        gf.free_movement()

    def upper_part_callback(self, gf, x):
        # Nothing to do here....
        pass
