'''
ZAxis Nut Support
'''
import math

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class ZAxisNutSupport:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_upper = GCodeGenerator(
            host_cnc, "%s-Upper" % self.__class__.__name__)
        self.__gf_lower = GCodeGenerator(
            host_cnc, "%s-Lower" % self.__class__.__name__)

    def generate(self):
        # Platform
#        for gf in (self.__gf_upper, self.__gf_lower):
#            gf.cutout_rect(0, 0, 
        self.__gf_upper.close()
        self.__gf_lower.close()
