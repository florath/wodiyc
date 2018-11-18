'''
Support Standard
'''

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class SupportStandard:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_part = GCodeGenerator(host_cnc)
        self.__gf_holes_horizontal = GCodeGenerator(host_cnc)
        self.__gf_holes_vertical = GCodeGenerator(host_cnc)

    def platform(self):
        self.__gf_part.cutout_rect(
            0, 0, self.x_size, self.y_size, self.z_size)
        self.__gf_part.free_movement()

    def screws(self):
        for x in (self.screwhole_distance_from_edge,
                  self.x_size - self.screwhole_distance_from_edge):
            for y in (self.screwhole_distance_from_edge,
                      self.y_size - self.screwhole_distance_from_edge):
                # Notch
                self.__gf_part.cylinder(
                    x, y, 
                    self.screwhole_notch_diameter, self.screwhole_notch_depth)
                # Screw
                self.__gf_part.cylinder(
                    x, y, self.screwhole_diameter,
                    self.z_size, self.screwhole_notch_depth)
                self.__gf_part.free_movement()
                # Screw holes horizontal
                self.__gf_holes_horizontal.cylinder(
                    x, y, self.sleeve_diameter,
                    self.sleeve_depth)
                self.__gf_holes_horizontal.free_movement()
                # Screw holes vertical
                self.__gf_holes_vertical.cylinder(
                    y, x, self.sleeve_diameter,
                    self.sleeve_depth)
                self.__gf_holes_vertical.free_movement()
                
    def generate(self):
        self.__gf_part.open("%s-Part" % self.__class__.__name__)
        self.__gf_holes_horizontal.open(
            "%s-Holes-Horizontal" % self.__class__.__name__)
        self.__gf_holes_vertical.open(
            "%s-Holes-Vertical" % self.__class__.__name__)
        self.screws()
        self.platform()
        self.__gf_part.close()
        self.__gf_holes_horizontal.close()
        self.__gf_holes_vertical.close()
