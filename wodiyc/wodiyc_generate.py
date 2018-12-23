'''
The complete machine
'''
import argparse
import importlib
import yaml

from wodiyc.lib.Measurements import Measurements


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

    # The measurements of all parts
    measurements = Measurements()

    # The modules must be initialized in a special order
    modules = {}
    
    for module_name in module_parts.__all__:
        module = importlib.import_module("wodiyc.parts.%s" % module_name)
        modules[module_name] = module

    # First: Get the measurements correctly set.
    modules_todo = set(modules.keys())

    while len(modules_todo) > 0:
        modules_done = set()

        for module_name in modules_todo:

            if hasattr(modules[module_name], "measurements_%s" % module_name):
                try:
                    print("Compute measurements for [%s]" % module_name)
                    measurement_computation \
                        = getattr(modules[module_name], "measurements_%s" % module_name)
            
                    sub = measurements.sub(module_name)
                    sub.update(wodiyc[module_name])

                    measurement_computation(measurements)
                    modules_done.add(module_name)
                except KeyError as ke:
                    print("Aborted computation because of [%s]" % ke)
            else:
                # If there is no measurement function, skip this for this phase.
                modules_done.add(module_name)

        modules_todo -= modules_done

    # Call the generators
    for module_name, module in modules.items():
        if not hasattr(module, module_name):
            continue
        part_class = getattr(module, module_name)
        instance = part_class(host_cnc, measurements, wodiyc)
        instance.generate()


if __name__ == '__main__':
    main()
