'''
The complete machine
'''
import argparse
import importlib
import yaml


def parse_args():
    '''Parse the command line parameters'''
    parser = argparse.ArgumentParser(
        description='Create G-Code for Wodiyc')
    parser.add_argument('--wodiyc', required=True,
                        help='Config file with all measurements')
    parser.add_argument('--host-cnc', required=True,
                        help='Config file describing the host CNC')

    args = parser.parse_args()

    with open(args.wodiyc, "r") as config_file:
        wodiyc = yaml.load(config_file)
    with open(args.host_cnc, "r") as config_file:
        host_cnc = yaml.load(config_file)

    return wodiyc, host_cnc


def main():
    '''Generate all files for the Wodiyc'''
    wodiyc, host_cnc = parse_args()

    # Import all parts and generate them
    module_parts = importlib.import_module("wodiyc.parts")

    for module_name in module_parts.__all__:
        module = importlib.import_module("wodiyc.parts.%s" % module_name)
        part_class = getattr(module, module_name)
        instance = part_class(host_cnc, wodiyc)
        instance.generate()


if __name__ == '__main__':
    main()
