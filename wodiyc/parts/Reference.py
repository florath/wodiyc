'''
Reference
'''
from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class Reference:
    '''A small reference pice'''

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf = GCodeGenerator(
            host_cnc, "%s" % self.__class__.__name__)
    
    def generate(self):
        self.__gf.cylinder(
            15, 20, 10, self.z_size)
        self.__gf.free_movement()

        # Notch
        self.__gf.cylinder(
            30, 40, 15, 4)
        # Screw
        self.__gf.cylinder(
            30, 40, 6, self.z_size)
        self.__gf.free_movement()

        # Pocket
        self.__gf.pocket(50, 15, 10, 30, 5)
        self.__gf.free_movement()

        self.__gf.cutout_rect(
            0, 0, 70, 50, self.z_size)
        self.__gf.free_movement()
        
        self.__gf.close()
