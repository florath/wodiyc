'''
Adjustment Block for ball bearings
'''

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator
from wodiyc.parts.helper.AdjustmentBlockBase import AdjustmentBlockBase

def measurements_AdjustmentBlockBearing(m):
    '''Compute all the measurements for AdjustmentBlockBearing'''
    p = m.AdjustmentBlockBearing
    abb = m.AdjustmentBlockBase

    # Set / Copy all measurements from AdjustmentBlockBase
    p.screwhole_notch_diameter = m.Common.screwhole_notch_diameter
    p.screwhole_notch_depth = m.Common.screwhole_notch_depth_washer
    p.screwhole_diameter = m.Common.screwhole_diameter
    p.z_size = m.Common.base_material_thickness
    p.nut_cutoff = abb.nut_cutoff
    p.nut_indent = abb.nut_indent
    p.nut_height = abb.nut_height
    p.nut_width = abb.nut_width

class AdjustmentBlockBearing(AdjustmentBlockBase):

    def __init__(self, host_cnc, measurements, config):
        super().__init__(host_cnc, measurements, self.__class__.__name__)
        self.__gf = GCodeGenerator(host_cnc, self.__class__.__name__)

    def generate(self):
        self.base_generate(self.__gf)
