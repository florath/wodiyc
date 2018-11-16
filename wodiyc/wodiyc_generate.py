'''
The complete machine
'''
import argparse
import yaml

from wodiyc.lib.ZAxisPlatformBack import ZAxisPlatformBack
from wodiyc.lib.ZAxisPlatformFront import ZAxisPlatformFront
from wodiyc.lib.gcode.GCodeGenerator import GCodeGenerator


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
    wodiyc, host_cnc = parse_args()
    gcg = GCodeGenerator(host_cnc)

    z_axix_platform_back = ZAxisPlatformBack(wodiyc)
    z_axix_platform_back.generate(gcg)

    z_axix_platform_front = ZAxisPlatformFront(wodiyc)
    z_axix_platform_front.generate(gcg)
    
if __name__ == '__main__':
    main()
