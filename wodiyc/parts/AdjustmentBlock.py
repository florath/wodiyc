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

    def platform(self):
        self.__gf.cutout_rect(
            0, 0, self.size, self.size, self.z_size)
        self.__gf.free_movement()

    def center(self):
        '''Center with circle and notches for the screws'''
        self.__gf.cutout_circle(self.size / 2, self.size / 2,
                                self.center_diameter,
                                self.z_size)
        self.__gf.free_movement()

    def center_nuts(self):
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
            
    def generate(self):
        self.center()
        self.center_nuts()
        self.platform()
        self.__gf.close()
