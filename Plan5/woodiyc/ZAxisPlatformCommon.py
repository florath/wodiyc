'''
ZAxisPlatform Common
'''

class ZAxisPlatformCommon:
    '''ZAxisPlatform Common

    The common part of the ZAxis Platform. It contains all
    the measurements and the common part of back and front.
    '''
    def __init__(
            self,

            # Overall
            platform_x=120,  # Width
            platform_y=335,  # Height
            platform_z=16,   # Thick

            # Cutoffs
            # Center to center distance 
            cutout_distance=60,
            cutout_length=150,
            # This is added to the cutout because
            # of the inner radius of the tool.
            cutout_length_add=5,
            cutout_width=19,
            cutout_depth=6,

            # Tool support sdcrew holes
            tool_support_hole_diameter=8.1,
            tool_support_hole_distance=55,
            tool_support_hole_distance_from_edge=20,
            tool_support_hole_notch_diameter=18,
            tool_support_hole_notch_depth=6,

            # Screw holes
            screw_hole_diameter=6.1,
            screw_hole_distance_from_edge=25,
            # There are some notches that the bolts do not raise
            # above the surface
            screw_notch_diameter=15,
            screw_notch_depth=4):

        self._platform_x = platform_x
        self._platform_y = platform_y
        self._platform_z = platform_z
        self._cutout_distance = cutout_distance
        self._cutout_length = cutout_length
        self._cutout_length_add = cutout_length_add
        self._cutout_width = cutout_width
        self._cutout_depth = cutout_depth

        self._tool_support_hole_diameter = tool_support_hole_diameter
        self._tool_support_hole_distance = tool_support_hole_distance
        self._tool_support_hole_distance_from_edge = tool_support_hole_distance_from_edge
        self._tool_support_hole_notch_diameter = tool_support_hole_notch_diameter
        self._tool_support_hole_notch_depth = tool_support_hole_notch_depth

        self._screw_hole_diameter = screw_hole_diameter
        self._screw_hole_distance_from_edge \
            = screw_hole_distance_from_edge
        self._screw_notch_diameter = screw_notch_diameter
        self._screw_notch_depth = screw_notch_depth

    def _tool_support_holes(self, gf, tool_support_holes_callback):
        # Screw holes for the tool support
        for x in (self._platform_x / 2 - self._tool_support_hole_distance / 2,
                  self._platform_x / 2 + self._tool_support_hole_distance / 2):
            tool_support_holes_callback(self, gf, x)

    def _lower_screw_holes(self, gf):
        for x in (self._screw_hole_distance_from_edge,
                  self._platform_x
                  - self._screw_hole_distance_from_edge):
            for y in (self._tool_support_hole_distance_from_edge
                      + self._screw_hole_distance_from_edge,
                      self._platform_y
                      - self._cutout_length
                      - self._screw_notch_diameter
                      - self._screw_hole_distance_from_edge):
                # Notch
                gf.cylinder(
                    x, y,
                    self._screw_notch_diameter, self._screw_notch_depth)
                # Screw
                gf.cylinder(
                    x, y,
                    self._screw_hole_diameter, self._platform_z,
                    self._screw_notch_depth)
                gf.free_movement()

    def _upper_part(self, gf, upper_part_callback, upper_part_screws_callback):
        # pockets
        for px in (self._platform_x / 2 - self._cutout_distance / 2,
                   self._platform_x / 2 + self._cutout_distance / 2 ):
            upper_part_callback(self, gf, px)

            for sy in (self._platform_y - self._cutout_length
                       + self._screw_hole_distance_from_edge,
                       self._platform_y
                       - self._screw_hole_distance_from_edge):
                upper_part_screws_callback(self, gf, px, sy)

    def _platform(self, gf):
        # Cutout the complete platform
        gf.cutout_rect(0, 0, self._platform_x, self._platform_y,
                       self._platform_z)
        gf.free_movement()
