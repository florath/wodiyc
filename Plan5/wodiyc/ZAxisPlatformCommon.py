'''
ZAxisPlatform Common
'''

class ZAxisPlatformCommon:
    '''ZAxisPlatform Common

    The common part of the ZAxis Platform. It contains all
    the measurements and the common part of back and front.
    '''
    def __init__(self, config):
        cfg = config[self.__class__.__name__]

        self.__dict__.update(cfg)

#        self._cutout_distance = cutout_distance
#        self._cutout_length = cutout_length
#        self._cutout_length_add = cutout_length_add
#        self._cutout_width = cutout_width
#        self._cutout_depth = cutout_depth

#        self._tool_support_hole_diameter = tool_support_hole_diameter
#        self._tool_support_hole_distance = tool_support_hole_distance
#        self._tool_support_hole_distance_from_edge = tool_support_hole_distance_from_edge
#        self._tool_support_hole_notch_diameter = tool_support_hole_notch_diameter
#        self._tool_support_hole_notch_depth = tool_support_hole_notch_depth

#        self._screw_hole_diameter = screw_hole_diameter
#        self._screw_hole_distance_from_edge \
#            = screw_hole_distance_from_edge
#        self._screw_notch_diameter = screw_notch_diameter
#        self._screw_notch_depth = screw_notch_depth

    def tool_support_holes(self, gf):
        # Screw holes for the tool support
        for x in (self.x_size / 2 - self.toolsupportholes_distance / 2,
                  self.x_size / 2 + self.toolsupportholes_distance / 2):
            self.tool_support_holes_callback(gf, x)

    def lower_screw_holes(self, gf):
        for x in (self.screwholes_distance_from_edge,
                  self.x_size
                  - self.screwholes_distance_from_edge):
            for y in (self.toolsupportholes_distance_from_edge
                      + self.screwholes_distance_from_edge,
                      self.y_size
                      - self.cutouts_length
                      - self.screwholes_notch_diameter
                      - self.screwholes_distance_from_edge):
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

    def upper_part(self, gf):
        # pockets
        for px in (self.x_size / 2 - self.cutouts_distance / 2,
                   self.x_size / 2 + self.cutouts_distance / 2 ):
            self.upper_part_callback(gf, px)

            for sy in (self.y_size - self.cutouts_length
                       + self.screwholes_distance_from_edge,
                       self.y_size
                       - self.screwholes_distance_from_edge):
                self.upper_part_screws_callback(gf, px, sy)

    def platform(self, gf):
        # Cutout the complete platform
        gf.cutout_rect(0, 0, self.x_size, self.y_size, self.z_size)
        gf.free_movement()

    def generate(self, gf):
        gf.open()
        # Screw holes for the tool support
        self.tool_support_holes(gf)
        # Lower holes for screws to fit front and back together
        self.lower_screw_holes(gf)
        # Pockets and screws
        self.upper_part(gf)
        # Platform
        self.platform(gf)
        gf.close()
