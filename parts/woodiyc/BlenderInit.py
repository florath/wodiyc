'''
Initializes the Blender (Engine)
'''
import bpy

import woodiyc.BY as BY


class BlenderInit:

    def __set_unit_mm(self):
        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 0.001

    def __init__(self):
        # Set unit mm
        self.__set_unit_mm()
        # Remove initial cube
        BY.delete(bpy.data.objects['Cube'])
