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
    
    def generate(self):
        self.center()
        self.platform()
        self.__gf.close()
