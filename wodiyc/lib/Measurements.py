'''
Measurements
'''

class Measurements:
    '''All measurements of the the CNC machine.

    For easy access, use attribute acceess - use values stored in
    internal dict.
    '''

    def __init__(self):
        self.__values = {}

    def __getattr__(self, name):
        if name.startswith('_Measurements'):
            return self.__dict__[name]
        else:
            return self.__values[name]

    def __setattr__(self, name, value):
        if name.startswith('_Measurements'):
            self.__dict__[name] = value
        else:
            self.__values[name] = value

    def sub(self, name):
        self.__values[name] = Measurements()
        return self.__values[name]

    def update(self, c):
        self.__values.update(c)
