#!/usr/bin/env python3


import argparse
from xml.etree import ElementTree as et


def main():

    args = parse_arguments()

    register_namespaces()
    tree = et.parse(args.input)
    tree.write(args.output)


def register_namespaces():
    et.register_namespace('', "http://psi.hupo.org/ms/mzml")
    et.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    et.register_namespace('schemaLocation', "http://psi.hupo.org/ms/mzml http://psidev.info/files/ms/mzML/xsd/mzML1.1.0.xsd")


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
