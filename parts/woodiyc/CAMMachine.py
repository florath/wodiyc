import bpy

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

    def __init__(self, objs, cutter_diameter=3.175, cutter_diameter_delta=1.0):
        bpy.context.scene.render.engine = 'BLENDERCAM_RENDER'
        self.__init_params()
        self.__objs = objs
        self.__cutter_diameter = cutter_diameter
        self.__cutter_diameter_delta = cutter_diameter_delta
        self.__obj_idx = 0
        
        #self.__ocut = obj.get_cut_obj()
        #self.__name = obj.get_cut_obj().name

    def process_obj(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.scene.cam_operation_add()
        # Shorthand
        cam_op = bpy.context.scene.cam_operations
        op_idx = self.__obj_idx = 0
        
        cam_op[op_idx].auto_export = False
        cam_op[op_idx].object_name = obj.get_name()
        cam_op[op_idx].material_radius_around_model = 10
        cam_op[op_idx].free_movement_height = 7

        cam_op[op_idx].strategy = obj.get_strategy()
        cam_op[op_idx].cut_type = obj.get_cut_type()

        # Bridges
        if obj.has_bridges():
            cam_op[op_idx].use_bridges = True
            cam_op[op_idx].bridges_group_name = obj.get_bridges_name()

            cam_op[op_idx].bridges_width = 2
            cam_op[op_idx].bridges_height = 2

        # Compute stepdown
        stepdown_max = self.__cutter_diameter / 2.1
        stepdown_cnt = int(obj.bo().dimensions.z / stepdown_max) + 1
        stepdown = obj.bo().dimensions.z / stepdown_cnt

        cam_op[op_idx].imgres_limit = 1
        cam_op[op_idx].stepdown = stepdown
        cam_op[op_idx].first_down = True

        cam_op[op_idx].cutter_diameter \
            = self.__cutter_diameter * self.__cutter_diameter_delta

        bpy.ops.object.calculate_cam_path()

        # Save
        cam_op[op_idx].filename = obj.get_name()
        bpy.ops.object.cam_export()

    def process(self):
        for obj in self.__objs.get_objs():
            self.process_obj(obj)

        

