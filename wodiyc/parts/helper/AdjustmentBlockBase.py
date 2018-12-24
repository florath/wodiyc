'''
Adjustment Block Base
'''
from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class AdjustmentBlockBase:

    def __init__(self, host_cnc, measurements, name):
        self.m = measurements
        self.p = measurements.__getattr__(name)

    def platform(self, gf):
        gf.cutout_octagon(0, 0, self.p.size, self.p.z_size)
        gf.free_movement()

    def center(self, gf):
        '''Center with circle and notches for the screws'''
        gf.cutout_circle(self.p.size / 2, self.p.size / 2,
                         self.p.center_diameter, self.p.z_size)
        gf.free_movement()

    def center_nuts(self, gf):
        gf.comment("Center nuts")
        nut_complte_cutoff = self.p.z_size / 2 + self.p.nut_cutoff
        for y in (self.p.size / 2 + self.p.center_diameter / 2
                  - self.p.nut_indent,
                  self.p.size / 2 - self.p.center_diameter / 2
                  + self.p.nut_indent - self.p.nut_height):
            # Top / Down
            gf.pocket(self.p.size / 2 - self.p.nut_width / 2, y,
                      self.p.nut_width, self.p.nut_height, nut_complte_cutoff)
            gf.free_movement()
            # Left / Right
            gf.pocket(y, self.p.size / 2 - self.p.nut_width / 2,
                      self.p.nut_height, self.p.nut_width, nut_complte_cutoff)
            gf.free_movement()

    def screw(self, gf, x, y):
        # Notch
        gf.cylinder(x, y, self.p.screwhole_notch_diameter,
                    self.p.screwhole_notch_depth)
        # Screw
        gf.cylinder(x, y, self.p.screwhole_diameter, self.p.z_size,
                    self.p.screwhole_notch_depth)
        gf.free_movement()

    def screws(self, gf):
        gf.comment("Four screws with notches")
        for x in (self.p.screwholes_distance_from_corner,
                  self.p.size - self.p.screwholes_distance_from_corner):
            for y in (self.p.screwholes_distance_from_corner,
                      self.p.size - self.p.screwholes_distance_from_corner):
                self.screw(gf, x, y)
            
    def base_generate(self, gf):
        self.screws(gf)
        self.center(gf)
        self.center_nuts(gf)
        self.platform(gf)
        gf.comment("AdjustmentBlock ")
        gf.close()

    def generate(self):
        pass
