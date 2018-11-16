'''
Reference
'''

class Reference:
    '''Reference part

    This part is for reference only - it is not used
    in the CNC machine.
    The purpose is, to check if the measures are
    correct.
    The size of the part are 60mm x 70mm.
    The pocket is 10mm x 30mm and 10mm depth.
    The cylinder is 10mm diameter.
    '''

    def __init__(self, thick=12):
        self.__z = thick

    def generate_gcode(self, gf):
        # 10mm cylinder cutthrough
        gf.cylinder(15, 20, 10, self.__z)
        gf.free_movement()
        
        # Notch
        gf.cylinder(30, 40, 15, 4)
        # Screw
        gf.cylinder(30, 40, 6.2, self.__z, 4)
        gf.free_movement()
        
        # pocket
        gf.pocket(50, 15, 10, 30, 10)
        gf.free_movement()

        # Cutoff
        gf.cutout_rect(0, 0, 70, 50, self.__z)
        gf.free_movement()
