'''
Blender pYthon utilities
'''
import bpy

def select(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select = True

def delete(obj):
    select(obj)
    bpy.ops.object.delete()

def activate(obj):
    select(obj)
    bpy.context.scene.objects.active = obj

def mod_boolean(obj1, obj2, modifier=None):
    activate(obj1)
    bpy.ops.object.modifier_add(type='BOOLEAN')
    if modifier is not None or modifier != 'INTERSECT':
        bpy.context.object.modifiers["Boolean"].operation = modifier
    bpy.context.object.modifiers["Boolean"].object = obj2
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
