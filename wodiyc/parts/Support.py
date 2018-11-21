'''
Support Standard
'''

from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


class Support:

    def __init__(self, host_cnc, config):
        cfg = config[self.__class__.__name__]
        self.__dict__.update(cfg)
        self.__gf_part = GCodeGenerator(
            host_cnc, "%s-Part" % self.__class__.__name__)
        self.__gf_holes_horizontal = GCodeGenerator(
            host_cnc, "%s-Holes-Horizontal" % self.__class__.__name__)
        self.__gf_holes_vertical = GCodeGenerator(
            host_cnc, "%s-Holes-Vertical" % self.__class__.__name__)
        self.__gf_v_part = GCodeGenerator(
            host_cnc, "%s-VPart" % self.__class__.__name__)
        self.__gf_v_front = GCodeGenerator(
            host_cnc, "%s-VPart-Front" % self.__class__.__name__)

        self.__host_cnc = host_cnc
        
        # for loops
        self._loop_support_scews_dists \
            = (self.screwhole_distance_from_edge_small,
               2 * self.screwhole_distance_from_edge_small)

    def platform(self):
        for gf in [self.__gf_part, self.__gf_v_part]:
            gf.cutout_rect(
                0, 0, self.x_size, self.y_size, self.z_size)
            gf.free_movement()

        self.__gf_v_front.cutout_rect(
            0, 0, self.x_size, self.v_y_size, self.z_size)
        self.__gf_v_front.free_movement()

    def screws(self):
        for x in (self.screwhole_distance_from_edge,
                  self.x_size / 2,
                  self.x_size - self.screwhole_distance_from_edge):
            for y in (self.screwhole_distance_from_edge,
                      self.y_size
                      - self.z_size
                      - self.screwhole_distance_from_edge):
                for gf in [self.__gf_part, self.__gf_v_part]:
                    # Notch
                    gf.cylinder(
                        x, y,
                        self.screwhole_notch_diameter,
                        self.screwhole_notch_depth)
                    # Screw
                    gf.cylinder(
                        x, y, self.screwhole_diameter,
                        self.z_size, self.screwhole_notch_depth)
                    self.__gf_part.free_movement()
                    gf.free_movement()

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

            # Cross Nuts
            self.__gf_v_front.cylinder(
                x, self.cross_nut_distance_from_edge,
                self.cross_nut_diameter,
                self.z_size)
            self.__gf_v_front.free_movement()

    def cutouts(self):
        # The big one
        self.__gf_v_part.pocket(-2, self.y_size - self.z_size,
                                self.x_size + 2, self.z_size,
                                self.cutout_depth)
        self.__gf_v_part.free_movement()

        for x in (self.screwhole_distance_from_edge,
                  self.x_size / 2,
                  self.x_size - self.screwhole_distance_from_edge):
            self.__gf_v_part.cylinder(
                x, self.y_size - self.z_size / 2,
                self.screwhole_diameter,
                self.z_size, self.cutout_depth)
            self.__gf_v_part.free_movement()

        for x in (self.x_size / 2 - self.cutout_distance / 2,
                  self.x_size / 2 + self.cutout_distance / 2):
            self.__gf_v_part.pocket(x - self.z_size/2, -2,
                                    self.z_size, self.y_size+2-self.z_size,
                                    self.cutout_depth)
            self.__gf_v_part.free_movement()

            # Part
            for y in self._loop_support_scews_dists:
                self.__gf_v_part.cylinder(
                    x, y,
                    self.screwhole_diameter,
                    self.z_size, self.cutout_depth)
                self.__gf_v_part.free_movement()

            # Front
            self.__gf_v_front.pocket(x - self.z_size/2, - 2,
                                     self.z_size, self.v_y_size + 4,
                                     self.cutout_depth)
            self.__gf_v_front.free_movement()

            for y in self._loop_support_scews_dists:
                self.__gf_v_front.cylinder(
                    x, self.v_y_size - y,
                    self.screwhole_diameter,
                    self.z_size, self.cutout_depth)
                self.__gf_v_front.free_movement()

    def support(self):
        gf = GCodeGenerator(
            self.__host_cnc, "%s-VPart-Support" % self.__class__.__name__)

        support_x_size = self.y_size - self.z_size + self.cutout_depth
        support_y_size = self.v_y_size + self.cutout_depth

        for x in self._loop_support_scews_dists:
            gf.cylinder(x, self.cross_nut_distance_from_edge,
                        self.cross_nut_diameter, self.z_size)
            gf.free_movement()

        for y in self._loop_support_scews_dists:
            gf.cylinder(support_x_size - self.cross_nut_distance_from_edge,
                        support_y_size - y, self.cross_nut_diameter,
                        self.z_size)
            gf.free_movement()

        gf.cutout_rect(0, 0, support_x_size, support_y_size, self.z_size)
        gf.free_movement()

        gf.close()

    def generate(self):
        self.screws()
        self.cutouts()
        self.platform()
        self.__gf_part.close()
        self.__gf_holes_horizontal.close()
        self.__gf_holes_vertical.close()
        self.__gf_v_part.close()
        self.__gf_v_front.close()

        self.support()