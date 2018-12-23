'''
Common
'''

def measurements_Common(m):
    '''Compute all the measurements for Common'''
    p = m.Common

    p.threaded_rod_x_free_movement_diameter = p.threaded_rod_x_diameter * 1.2
    print("Common threaded_rod_x_free_movement_diameter [%.5f]"
          % p.threaded_rod_x_free_movement_diameter)
