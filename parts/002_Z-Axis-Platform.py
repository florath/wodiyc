from woodiyc.BlenderInit import BlenderInit
from woodiyc.ZAxisPlatform import ZAxisPlatform


def main():
    bi = BlenderInit()

    obj = ZAxisPlatform()
    obj.construct()


if __name__ == '__main__':
    main()
