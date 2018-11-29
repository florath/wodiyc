'''
Support Bearing

This is used as a support for manufacuring the bearings
'''
from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class SupportBearing:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_screwholes = GCodeGenerator(
            host_cnc, "%s-ScrewHoles" % self.__class__.__name__,
            tool=self.tool_holes)
        self.__gf_surface = GCodeGenerator(
            host_cnc, "%s-Surface" % self.__class__.__name__,
            tool=self.tool_surface)
        self.__gf_tool_change = GCodeGenerator(
            host_cnc, "%s-ToolChange" % self.__class__.__name__,
            tool=self.tool_holes)

    def screws(self):
        for x in (self.screwhole_distance_from_edge,
                  self.fix_x_size / 2,
                  self.fix_x_size - self.screwhole_distance_from_edge):
            for y in (self.screwhole_distance_from_edge,
                      self.fix_y_size
                      - self.fix_z_size
                      - self.screwhole_distance_from_edge):
                # Notch
                self.__gf_screwholes.cylinder(
                    y, x,
                    self.screwhole_notch_diameter,
                    self.screwhole_notch_depth + self.surface_clean_depth)
                # Screw
                self.__gf_screwholes.cylinder(
                    y, x, self.screwhole_diameter,
                    self.fix_z_size + self.surface_clean_depth,
                    self.screwhole_notch_depth + self.surface_clean_depth)
                self.__gf_screwholes.free_movement()
    
    def generate(self):
        self.__gf_surface.pocket(
            -self.overlap, -self.overlap,
            self.x_size + 2 * self.overlap,
            self.y_size + 2 * self.overlap,
            self.surface_clean_depth)
        self.__gf_surface.free_movement()

        self.__gf_tool_change.cylinder(
            0, 0, self.tool_change_diameter,
            self.tool_change_depth)
        
        self.screws()
        self.__gf_surface.close()
        self.__gf_screwholes.close()
        self.__gf_tool_change.close()
