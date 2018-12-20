'''
Adjustment Block
'''
from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class AdjustmentBlock:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf = GCodeGenerator(
            host_cnc, "%s-Part" % self.__class__.__name__)
        self.size = self.half_size * 2

    def platform(self):
        self.__gf.cutout_octagon(
            0, 0, self.size, self.z_size)
        self.__gf.free_movement()

    def center(self):
        '''Center with circle and notches for the screws'''
        self.__gf.cutout_circle(self.size / 2, self.size / 2,
                                self.center_diameter,
                                self.z_size)
        self.__gf.free_movement()

    def center_nuts(self):
        self.__gf.comment("Center nuts")
        nut_complte_cutoff = self.z_size / 2 + self.nut_cutoff
        for y in (self.size / 2 + self.center_diameter / 2
                  - self.nut_indent,
                  self.size / 2 - self.center_diameter / 2
                  + self.nut_indent - self.nut_height):
            # Top / Down
            self.__gf.pocket(
                self.size / 2 - self.nut_width / 2, y,
                self.nut_width, self.nut_height, nut_complte_cutoff)
            self.__gf.free_movement()
            # Left / Right
            self.__gf.pocket(y, 
                self.size / 2 - self.nut_width / 2,
                self.nut_height, self.nut_width, nut_complte_cutoff)
            self.__gf.free_movement()

    def screw(self, x, y):
        # Notch
        self.__gf.cylinder(
            x, y,
            self.screwholes_notch_diameter, self.screwholes_notch_depth)
        # Screw
        self.__gf.cylinder(
            x, y,
            self.screwholes_diameter, self.z_size,
            self.screwholes_notch_depth)
        self.__gf.free_movement()

    def screws(self):
        self.__gf.comment("Four screws with notches")
        for x in (self.screwholes_distance_from_corner,
                  self.size - self.screwholes_distance_from_corner):
            for y in (self.screwholes_distance_from_corner,
                      self.size - self.screwholes_distance_from_corner):
                self.screw(x, y)
            
    def generate(self):
        self.screws()
        self.center()
        self.center_nuts()
        self.platform()
        self.__gf.close()
