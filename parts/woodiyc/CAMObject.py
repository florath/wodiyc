'''
Generic object description of something that will be 
created in real world.
This can be a collection of different objects.
'''

class CAMObjects:

    def __init__(self, name, strategy, cut_type, objs,
                 bridges_name=None, bridges=None):
        self.__name = name
        self.__strategy = strategy
        self.__cut_type = cut_type
        self.__objs = list(objs)
        self.__bridges_name = bridges_name
        self.__bridges = bridges

    def bo(self, idx=0):
        return self.__objs[idx]

    def get_name(self):
        return self.__name

    def get_strategy(self):
        return self.__strategy

    def get_cut_type(self):
        return self.__cut_type

    def has_bridges(self):
        return self.__bridges is not None

    def get_bridges_name(self):
        return self.__bridges_name


class CAMObjectsList:

    def __init__(self):
        self.__cam_objects = []

    def add(self, name, strategy, cut_type, objs,
            bridges_name=None, bridges=None):
        self.__cam_objects.append(
            CAMObjects(name, strategy, cut_type, objs, bridges_name, bridges))

    def get_objs(self):
        return self.__cam_objects
