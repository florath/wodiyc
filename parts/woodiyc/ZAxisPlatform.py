'''
Z Axis Platform

The original size of about 150mm x 225mm x 18mm had some flaws:

* for me the tool does not reach the table, therefore the size
  was increased from 225mm height to 335mm.

* This leads to the problem that the larger platform bends (some mm)
  when using only 18mm thikness.  The thickest MDF I can currently get
  is 19mm (with some effort 22mm).  Therefore I decided to go for a 
  'double' platform of 2 x 16mm.  (16mm MDF is cheap and can often be
  found in leftover-boxes in hardware stores.)

* The tool holder I'm using is made of aluminium and is only
  80mm wide.  To get rid of some unneccessary weight, the platform
  is shrinked in the width from 150mm to 120mm.
'''
import bpy
import woodiyc.BY as BY


class ZAxisPlatformFront:
    '''The part of the platform where the tool is mounted.'''

    def __init__(self, platform_thick,
                 platform_height,
                 platform_width):
        # Z Axis of Z Axix Platform
        self.__platform_thick = platform_thick
        # X Axis of Z Axix Platform
        self.__platform_height = platform_height
        # Y Axis of Z Axix Platform
        self.__platform_width = platform_width

    def _construct_basic_plate(self):
        '''The basic part'''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        plate = bpy.context.object
        plate.dimensions = (self.__platform_width,
                            self.__platform_height,
                            self.__platform_thick)
        return plate

    def construct(self):
        plate = self._construct_basic_plate()

class ZAxisPlatformBack:
    '''The part of the platform that is mounted to the rail support'''
    def __init__(self, platform_thick,
                 platform_height,
                 platform_width,
                 cutout_distance,
                 cutout_length,
                 cutout_width, cutout_depth,
                 screw_hole_diameter,
                 screw_hole_distance_from_edge, screw_tool_diameter,
                 screw_tool_depth):
        # Z Axis of Z Axix Platform
        self.__platform_thick = platform_thick
        # X Axis of Z Axix Platform
        self.__platform_height = platform_height
        # Y Axis of Z Axix Platform
        self.__platform_width = platform_width

        self.__cutout_distance = cutout_distance
        self.__cutout_length = cutout_length
        self.__cutout_width = cutout_width
        self.__cutout_depth = cutout_depth

        self.__screw_hole_diameter = screw_hole_diameter
        self.__screw_hole_distance_from_edge = screw_hole_distance_from_edge
        self.__screw_tool_diameter = screw_tool_diameter
        self.__screw_tool_depth = screw_tool_depth

    def _construct_basic_plate(self):
        '''The basic part'''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        plate = bpy.context.object
        plate.dimensions = (self.__platform_width,
                            self.__platform_height,
                            self.__platform_thick)
        return plate

    def __subtract_cutoffs(self, plate):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cutoff = bpy.context.object
        cutoff.dimensions \
            = (self.__cutout_width, self.__cutout_length + 2,
               self.__cutout_depth + 2)
        for x in (- self.__cutout_distance / 2,
                  self.__cutout_distance / 2):
            cutoff.location \
                = (x,
                   (self.__platform_height - self.__cutout_length) / 2,
                   self.__platform_thick/2 - self.__cutout_depth/2)
            BY.mod_boolean(plate, cutoff, 'DIFFERENCE')
        BY.delete(cutoff)

    def __cut_holes_for_screws(self, plate):
        # Holes for Screws
        ex_height = self.__platform_thick + 2
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        screw_hole = bpy.context.object
        screw_hole.dimensions = (self.__screw_hole_diameter,
                                 self.__screw_hole_diameter,
                                 ex_height)

        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        tool_hole = bpy.context.object
        tool_hole.dimensions = (self.__screw_tool_diameter,
                                self.__screw_tool_diameter,
                                self.__screw_tool_depth + 1)
        
        # The screw holes in the cutoffs
        for x in (- self.__cutout_distance / 2,
                  self.__cutout_distance / 2):
            for y in ( self.__platform_height / 2
                       - self.__screw_hole_distance_from_edge,
                       self.__platform_height / 2
                       - self.__cutout_length
                       + self.__screw_hole_distance_from_edge ):
                screw_hole.location = (x, y, 0)
                BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')

        # The screw holes in the bottom part to fit the front
        # and back together.
        for x in (self.__platform_width /2
                  - self.__screw_hole_distance_from_edge,
                  - self.__platform_width /2
                  + self.__screw_hole_distance_from_edge):
            for y in (self.__platform_height / 2
                      - self.__cutout_length
                      - self.__screw_hole_distance_from_edge,
                      - self.__platform_height / 2 
                      + self.__screw_hole_distance_from_edge):
                screw_hole.location = (x, y, 0)
                BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')
                tool_hole.location = (x, y,
                                      self.__platform_thick/2
                                      - self.__screw_tool_depth/2)
                BY.mod_boolean(plate, tool_hole, 'DIFFERENCE')
       
        BY.delete(screw_hole)
        BY.delete(tool_hole)

    def construct(self):
        plate = self._construct_basic_plate()
        self.__subtract_cutoffs(plate)
        self.__cut_holes_for_screws(plate)

class ZAxisPlatform:

    def __init__(self,
                 # This is used for front and back
                 platform_thick_half=16,
                 platform_height=335,
                 platform_width=120,
                 # The size the front is bigger than the back
                 front_exceeds=20,
                 # Center to center distance
                 cutout_distance=60,
                 cutout_length=150,
                 # This is added to the cutout because
                 # of the inner radius of the tool.
                 cutout_length_add=10,
                 cutout_width=19,
                 cutout_depth=6,
                 screw_hole_diameter=6.2,
                 screw_hole_distance_from_edge=25,
                 screw_tool_diameter=15, screw_tool_depth=4):
#        self.__front = ZAxisPlatformFront(
#            platform_thick_half, platform_height, platform_width)
        self.__back = ZAxisPlatformBack(
            platform_thick_half, platform_height-front_exceeds, platform_width,
            cutout_distance, cutout_length + cutout_length_add,
            cutout_width, cutout_depth, screw_hole_diameter,
            screw_hole_distance_from_edge, screw_tool_diameter,
            screw_tool_depth)

    def construct(self):
##        self.__front.construct()
        self.__back.construct()
