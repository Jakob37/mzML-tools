#!/usr/bin/env python3


import argparse
from xml.etree import ElementTree as et

NAMESPACE = "http://psi.hupo.org/ms/mzml"


def main():

    args = parse_arguments()

    register_namespaces()
    tree = et.parse(args.input)
    root = tree.getroot()
    run_node = root.find(prepend_ns('run'))
    spectrum_list_node = run_node.find(prepend_ns('spectrumList'))

    spectrum_list = spectrum_list_node.findall(prepend_ns('spectrum'))

    if args.check_only:

        stats_dict = calculate_stats_dict(spectrum_list)
        print('Number of spectra: {}'.format(len(spectrum_list)))
        print('MS1/MS2: {}/{}'.format(stats_dict['MS1'], stats_dict['MS2']))

    else:
        tree.write(args.output)


def register_namespaces():
    et.register_namespace('', NAMESPACE)
    et.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    et.register_namespace('schemaLocation', "http://psi.hupo.org/ms/mzml http://psidev.info/files/ms/mzML/xsd/mzML1.1.0.xsd")


def prepend_ns(s):
    return "{" + NAMESPACE + "}" + s


def calculate_stats_dict(spectrum_list):

    stats_dict = dict()
    stats_dict['MS1'] = 0
    stats_dict['MS2'] = 0

    for spectrum in spectrum_list:
        spec_dict = get_spect_dict(spectrum)
        if spec_dict['ms level'] == '1':
            stats_dict['MS1'] += 1
        elif spec_dict['ms level'] =='2':
            stats_dict['MS2'] += 1
        else:
            raise ValueError('Unknown MS level: {}'.format(spec_dict['ms level']))
    return stats_dict


def get_spect_dict(spect_node):

    cv_params = spect_node.findall(prepend_ns('cvParam'))
    spect_dict = dict()
    for cv_param in cv_params:
        attrib_name = cv_param.attrib['name']
        attrib_val = cv_param.attrib.get('value')
        spect_dict[attrib_name] = attrib_val
    return spect_dict


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output')

    parser.add_argument('--check_only', action='store_true', help='Print information about sample')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
