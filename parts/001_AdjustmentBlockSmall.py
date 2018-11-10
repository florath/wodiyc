'''
Adjustment Block

All units are given in mm
'''

import bpy
import time
import math

from woodiyc.BlenderInit import BlenderInit
import woodiyc.BY as BY

def deg2rad(d):
    return d * math.pi/180

def by_group(name, objs):
    group = bpy.data.groups.get(name, bpy.data.groups.new(name))
    for obj in objs:
        if obj.name not in group.objects:
            group.objects.link(obj)
    
def by_add_bridge(x, y, z, rot, sizex, sizey):
    bpy.ops.mesh.primitive_plane_add(radius=sizey, view_align=False, enter_editmode=False, location=(0, 0, 0))
    b=bpy.context.active_object
    b.name = 'bridge'
    b.dimensions.x = sizex
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bpy.ops.object.editmode_toggle()
    bpy.ops.transform.translate(
        value=(0, sizey, 0),
        constraint_axis=(False, True, False),
        constraint_orientation='GLOBAL',
        mirror=False,
        proportional='DISABLED',
        proportional_edit_falloff='SMOOTH',
        proportional_size=1)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.convert(target='CURVE')

    b.location = x, y, z
    b.rotation_euler.z = rot
    return b

class AdjustmentBlock:

    def __init__(self, size=80, height=19, hole_diam=36, notch_width=10, notch_height=4,
                 screw_hole_diam=6.2, screw_hole_pos_ratio=0.95):
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

        BY.mod_boolean(plate, cut_off_edges, 'INTERSECT')
        BY.delete(cut_off_edges)

    def _cut_central_hole(self, plate):
        '''Central hole'''
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        central_hole = bpy.context.object
        central_hole.dimensions = (self.__hole_diam, self.__hole_diam, self.__ex_height)

        BY.mod_boolean(plate, central_hole, 'DIFFERENCE')
        BY.delete(central_hole)

    def _cut_notches_for_nuts(self, plate):
        '''Notches for Nuts'''
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        notch = bpy.context.object
        notch.dimensions = (self.__notch_width, self.__hole_diam/2, self.__ex_height)

        notch.location = (0, self.__hole_diam/4 + self.__notch_height, 0)
        BY.mod_boolean(plate, notch, 'DIFFERENCE')
        
        notch.location = (0, -(self.__hole_diam/4 + self.__notch_height), 0)
        BY.mod_boolean(plate, notch, 'DIFFERENCE')

        bpy.context.object.rotation_euler[2] = deg2rad(90)

        notch.location = (0, self.__hole_diam/4 + self.__notch_height, 0)
        BY.mod_boolean(plate, notch, 'DIFFERENCE')

        notch.location = (0, -(self.__hole_diam/4 + self.__notch_height), 0)
        BY.mod_boolean(plate, notch, 'DIFFERENCE')

        BY.delete(notch)

    def _cut_holes_for_screws(self, plate):
        # Holes for Screws
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        screw_hole = bpy.context.object
        screw_hole.dimensions = (self.__screw_hole_diam, self.__screw_hole_diam, self.__ex_height)

        screw_hole_pos = (self.__size - self.__hole_diam) / 2 * self.__screw_hole_pos_ratio
        screw_hole.location = (screw_hole_pos, screw_hole_pos, 0)
        BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')

        screw_hole.location = (-screw_hole_pos, screw_hole_pos, 0)
        BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')

        screw_hole.location = (screw_hole_pos, -screw_hole_pos, 0)
        BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')
        
        screw_hole.location = (-screw_hole_pos, -screw_hole_pos, 0)
        BY.mod_boolean(plate, screw_hole, 'DIFFERENCE')

        BY.delete(screw_hole)

    def _create_bridges(self):
        '''Bridges for the inside

        There is the need to have bridges on the inside to avoid, that the
        inside sticks into the router
        '''
        half_size = self.__size / 2
        half_off = half_size - 5 # Half of the size of the bridge
        half_hole_size = self.__hole_diam / 2
        half_hole_off = half_hole_size - 2 # ??? Half of the size of the bridge
        half_height = self.__height / 2
        bridges = []
        # Outer Bridges
        bridges.append(by_add_bridge(0, half_off, half_height, deg2rad( 0), 2, 10))
        bridges.append(by_add_bridge(-half_off, 0, half_height, deg2rad(90), 2, 10))
        bridges.append(by_add_bridge(0, -half_off, half_height, deg2rad(180), 2, 10))
        bridges.append(by_add_bridge(half_off, 0, half_height, deg2rad(270), 2, 10))
        # Inner Bridges
        bridges.append(by_add_bridge(half_hole_off, -half_hole_off, half_height, deg2rad(45), 2, 10))
        bridges.append(by_add_bridge(half_hole_off, half_hole_off, half_height, deg2rad(135), 2, 10))
        bridges.append(by_add_bridge(-half_hole_off, half_hole_off, half_height, deg2rad(225), 2, 10))
        bridges.append(by_add_bridge(-half_hole_off, -half_hole_off, half_height, deg2rad(315), 2, 10))

        self.__bridges = bridges

        by_group("AdjustmentBlockBridges", bridges)

    def transform(self, dx, dy, dz):
        L = self.__adjustment_block.location
        self.__adjustment_block.location = (L[0] + dx, L[1] + dy, L[2] + dz)

        for b in self.__bridges:
            L = b.location
            b.location = (L[0] + dx, L[1] + dy, L[2] + dz)
        
    def construct(self):
        plate = self._construct_basic_plate()
        self._cut_edges(plate)
        self._cut_central_hole(plate)
        self._cut_notches_for_nuts(plate)
        self._cut_holes_for_screws(plate)
        self._create_bridges()
        self.__adjustment_block = plate
        self.__adjustment_block.name = "AdjustmentBlock"
        self.transform(self.__size/2, self.__size/2, -self.__height/2)

    def get_cut_obj(self):
        return self.__adjustment_block

    def get_bridges_name(self):
        return "AdjustmentBlockBridges"

class CAMMachine:

    def __init_params(self):
        d = bpy.context.scene.cam_machine
        s = bpy.context.scene.unit_settings

        d.post_processor = 'EMC'
        s.system = 'METRIC'
        d.use_position_definitions = False
        d.starting_position = (0.0, 0.0, 0.0)
        d.mtc_position = (0.0, 0.0, 0.0)
        d.ending_position = (0, 0, 0)
        d.working_area = (500, 500, 100)
        d.feedrate_min = 0.0
        d.feedrate_max = 900
        d.feedrate_default = 900
        d.spindle_min = 5000.0
        d.spindle_max = 30000.0
        d.spindle_default = 15000.0
        d.axis4 = False
        d.axis5 = False
        d.collet_size = 33.0
        d.output_tool_change = True
        d.output_block_numbers = False
        d.output_tool_definitions = True
        d.output_g43_on_tool_change = False

    def __init__(self, obj, cutter_diameter=3.175, cutter_diameter_delta=1.0):
        bpy.context.scene.render.engine = 'BLENDERCAM_RENDER'
        self.__init_params()
        self.__obj = obj
        self.__cutter_diameter = cutter_diameter
        self.__cutter_diameter_delta = cutter_diameter_delta
        self.__ocut = obj.get_cut_obj()
        self.__name = obj.get_cut_obj().name

    def process(self):
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.scene.cam_operation_add()
        bpy.context.scene.cam_operations[0].auto_export = False
        bpy.context.scene.cam_operations[0].object_name = self.__name
        bpy.context.scene.cam_operations[0].material_radius_around_model = 10
        bpy.context.scene.cam_operations[0].free_movement_height = 7

        #bpy.ops.object.cam_position()
        bpy.context.scene.cam_operations[0].strategy = 'CUTOUT'
        bpy.context.scene.cam_operations[0].cut_type = 'OUTSIDE'

        # Bridges
        bpy.context.scene.cam_operations[0].use_bridges = True
        bpy.context.scene.cam_operations[0].bridges_group_name = self.__obj.get_bridges_name()

        bpy.context.scene.cam_operations[0].bridges_width = 2
        bpy.context.scene.cam_operations[0].bridges_height = 2
        #bpy.ops.scene.cam_bridges_add()

        # Compute stepdown
        # ToDo: 22 is 22 mm thick plate - need to be variable.
        stepdown_max = 3.175 / 2.1
        stepdown_cnt = int(self.__ocut.dimensions.z / stepdown_max) + 1
        stepdown = self.__ocut.dimensions.z / stepdown_cnt

        bpy.context.scene.cam_operations[0].imgres_limit = 1
        bpy.context.scene.cam_operations[0].stepdown = stepdown
        bpy.context.scene.cam_operations[0].first_down = True

        bpy.context.scene.cam_operations[0].cutter_diameter \
            = self.__cutter_diameter * self.__cutter_diameter_delta

        bpy.ops.object.calculate_cam_path()

        # Save
        bpy.context.scene.cam_operations[0].filename = "AdjustmentBlockSmall"
        bpy.ops.object.cam_export()

        
def main():
    bi = BlenderInit()

    ab = AdjustmentBlock()
    ab.construct()

    # This is for my personal machine and for 3.175 diameter tool
    cam = CAMMachine(ab, cutter_diameter=3.175, cutter_diameter_delta=1.16)
    cam.process()

if __name__ == '__main__':
    main()
