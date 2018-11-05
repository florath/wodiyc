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

    def __init__(self, size=80, height=22, hole=36, notch_width=10, notch_height=3, screw_holes=6):
        self.__size = size
        self.__height = height
        self.__hole = hole
        self.__notch_width = notch_width
        self.__notch_height = notch_height
        self.__screw_holes = screw_holes

    def construct(self):
        # The basic part where everything is subtracted from
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        plate = bpy.context.object
        plate.dimensions = (self.__size, self.__size, self.__height)

        # All things which are subtraced are a little bit higher - so that also
        # the top and bottom plane are removed.
        ex_height = self.__height + 2

        # Cutoff Edges
        # Create another cube to cut off the edges
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        cut_off_edges = bpy.context.object
        cut_off_edges.dimensions = (self.__size, self.__size, ex_height)
        bpy.context.object.rotation_euler[2] = deg2rad(45)

        by_mod_boolean(plate, cut_off_edges, 'INTERSECT')
        by_delete(cut_off_edges)
        
        # Central hole
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        central_hole = bpy.context.object
        central_hole.dimensions = (self.__hole, self.__hole, ex_height)

        by_mod_boolean(plate, central_hole, 'DIFFERENCE')
        by_delete(central_hole)

        


def main():
    bi = BlenderInit()

    ab = AdjustmentBlock()
    ab.construct()


if __name__ == '__main__':
    main()
