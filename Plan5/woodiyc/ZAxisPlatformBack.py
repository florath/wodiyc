'''
ZAxisPlatform Back
'''

class ZAxisPlatformBack:
    '''ZAxisPlatform - Back

    The Z axis platform consists of two parts: the front, where the
    tool is mounted and the back where the rails are mounted.

    The Z axis Platform back consists of a base platform, two cutoffs
    for the rail mount and two set of holes.  One set fits the
    platform to the rail mount and the other set fits the back to the
    front
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
            cutout_length_add=10,
            cutout_width=19,
            cutout_depth=6,

            # Screw holes
            screw_hole_diameter=6.2,
            screw_hole_distance_from_edge=25,
            # There are some notches that the bolts do not raise
            # above the surface
            screw_notch_diameter=15,
            screw_notch_depth=4):

        self.__platform_x = platform_x
        self.__platform_y = platform_y
        self.__platform_z = platform_z
        self.__cutout_distance = cutout_distance
        self.__cutout_length = cutout_length
        self.__cutout_length_add = cutout_length_add
        self.__cutout_width = cutout_width
        self.__cutout_depth = cutout_depth
        self.__screw_hole_diameter = screw_hole_diameter
        self.__screw_hole_distance_from_edge \
            = screw_hole_distance_from_edge
        self.__screw_notch_diameter = screw_notch_diameter
        self.__screw_notch_depth = screw_notch_depth

    def generate_gcode(self, gf):
        # Lower holes for scrwes to fit front and back together
        for x in (self.__screw_hole_distance_from_edge,
                  self.__platform_x
                  - self.__screw_hole_distance_from_edge):
            for y in (self.__screw_hole_distance_from_edge,
                      self.__platform_y
                      - self.__cutout_length
                      - self.__screw_notch_diameter
                      - self.__screw_hole_distance_from_edge):
                # Notch
                gf.cylinder(
                    x, y,
                    self.__screw_notch_diameter, self.__screw_notch_depth)
                # Screw
                gf.cylinder(
                    x, y,
                    self.__screw_hole_diameter, self.__platform_z,
                    self.__screw_notch_depth)
                gf.free_movement()
            
        # pockets
        for px in (self.__platform_x / 2 - self.__cutout_distance / 2,
                   self.__platform_x / 2 + self.__cutout_distance / 2 ):
            real_cutout_length = self.__cutout_length + self.__cutout_length_add
            gf.pocket(px - self.__cutout_width / 2,
                      self.__platform_y - real_cutout_length,
                      self.__cutout_width,
                      # Increase the cutout a bit to get a clean cut
                      real_cutout_length + 3,
                      self.__cutout_depth)
            gf.free_movement()

            for sy in ( self.__platform_y - real_cutout_length
                        + self.__screw_hole_distance_from_edge,
                        self.__platform_y
                        - self.__screw_hole_distance_from_edge ):
                # Screw
                gf.cylinder(
                    px, sy,
                    self.__screw_hole_diameter, self.__platform_z,
                    self.__screw_notch_depth)
                gf.free_movement()

        # Cutout the complete platform
        gf.cutout_rect(0, 0, self.__platform_x, self.__platform_y,
                       self.__platform_z)
        gf.free_movement()
