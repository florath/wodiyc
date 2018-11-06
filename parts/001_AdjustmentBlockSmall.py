'''
Adjustment Block

All units are given in mm
'''

import bpy
import time
import math


def by_select(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True

def by_activate(obj):
    by_select(obj)
    bpy.context.scene.objects.active = obj

def by_delete(obj):
    by_select(obj)
    bpy.ops.object.delete()

def by_mod_boolean(obj1, obj2, modifier=None):
    by_activate(obj1)
    bpy.ops.object.modifier_add(type='BOOLEAN')
    if modifier is not None or modifier != 'INTERSECT':
        bpy.context.object.modifiers["Boolean"].operation = modifier
    bpy.context.object.modifiers["Boolean"].object = obj2
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

def deg2rad(d):
    return d * math.pi/180


class BlenderInit:

    def __set_unit_mm(self):
        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 0.001

    def __init__(self):
        # Set unit mm
        self.__set_unit_mm()
        # Remove initial cube
        by_delete(bpy.data.objects['Cube'])


class AdjustmentBlock:

    def __init__(self, size=80, height=22, hole_diam=36, notch_width=10, notch_height=3,
                 screw_hole_diam=6, screw_hole_pos_ratio=0.95):
        self.__size = size
        self.__height = height
        self.__hole_diam = hole_diam
        self.__notch_width = notch_width
        self.__notch_height = notch_height
        self.__screw_hole_diam = screw_hole_diam
        self.__screw_hole_pos_ratio = screw_hole_pos_ratio

        # All things which are subtraced from the initial block
        # are a little bit higher - so that also
        # the top and bottom plane are removed.
        self.__ex_height = self.__height + 2

    def _construct_basic_plate(self):
        '''The basic part where everything is subtracted from'''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        plate = bpy.context.object
        plate.dimensions = (self.__size, self.__size, self.__height)
        return plate

    def _cut_edges(self, plate):
        '''Cutoff Edges

        Create another cube to cut off the edges
        '''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cut_off_edges = bpy.context.object
        cut_off_edges.dimensions = (self.__size, self.__size, self.__ex_height)
        bpy.context.object.rotation_euler[2] = deg2rad(45)

        by_mod_boolean(plate, cut_off_edges, 'INTERSECT')
        by_delete(cut_off_edges)

    def _cut_central_hole(self, plate):
        '''Central hole'''
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        central_hole = bpy.context.object
        central_hole.dimensions = (self.__hole_diam, self.__hole_diam, self.__ex_height)

        by_mod_boolean(plate, central_hole, 'DIFFERENCE')
        by_delete(central_hole)

    def _cut_notches_for_nuts(self, plate):
        '''Notches for Nuts'''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        notch = bpy.context.object
        notch.dimensions = (self.__notch_width, self.__hole_diam/2, self.__ex_height)

        notch.location = (0, self.__hole_diam/4 + self.__notch_height, 0)
        by_mod_boolean(plate, notch, 'DIFFERENCE')
        
        notch.location = (0, -(self.__hole_diam/4 + self.__notch_height), 0)
        by_mod_boolean(plate, notch, 'DIFFERENCE')

        bpy.context.object.rotation_euler[2] = deg2rad(90)

        notch.location = (0, self.__hole_diam/4 + self.__notch_height, 0)
        by_mod_boolean(plate, notch, 'DIFFERENCE')

        notch.location = (0, -(self.__hole_diam/4 + self.__notch_height), 0)
        by_mod_boolean(plate, notch, 'DIFFERENCE')

        by_delete(notch)

    def _cut_holes_for_screws(self, plate):
        # Holes for Screws
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        screw_hole = bpy.context.object
        screw_hole.dimensions = (self.__screw_hole_diam, self.__screw_hole_diam, self.__ex_height)

        screw_hole_pos = (self.__size - self.__hole_diam) / 2 * self.__screw_hole_pos_ratio
        screw_hole.location = (screw_hole_pos, screw_hole_pos, 0)
        by_mod_boolean(plate, screw_hole, 'DIFFERENCE')

        screw_hole.location = (-screw_hole_pos, screw_hole_pos, 0)
        by_mod_boolean(plate, screw_hole, 'DIFFERENCE')

        screw_hole.location = (screw_hole_pos, -screw_hole_pos, 0)
        by_mod_boolean(plate, screw_hole, 'DIFFERENCE')
        
        screw_hole.location = (-screw_hole_pos, -screw_hole_pos, 0)
        by_mod_boolean(plate, screw_hole, 'DIFFERENCE')

        by_delete(screw_hole)
        
    def construct(self):
        plate = self._construct_basic_plate()
        self._cut_edges(plate)
        self._cut_central_hole(plate)
        self._cut_notches_for_nuts(plate)
        self._cut_holes_for_screws(plate)
        
        
def main():
    bi = BlenderInit()

    ab = AdjustmentBlock()
    ab.construct()


if __name__ == '__main__':
    main()
