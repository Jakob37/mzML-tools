#!/usr/bin/env python3


import argparse
from xml.etree import ElementTree as et

NAMESPACE = "http://psi.hupo.org/ms/mzml"


def main():

    args = parse_arguments()
    register_namespaces()
    tree = et.parse(args.input)

    if args.is_indexed:
        root = tree.getroot()
        mzml_root = root.find(prepend_ns('mzML'))
        out_tree = et.ElementTree(mzml_root)
    else:
        mzml_root = tree.getroot()
        out_tree = tree

    run_node = mzml_root.find(prepend_ns('run'))
    spectrum_list_node = run_node.find(prepend_ns('spectrumList'))

    spectrum_list = spectrum_list_node.findall(prepend_ns('spectrum'))

    stats_dict = calculate_stats_dict(spectrum_list, args.ms1_count)
    print('Number of spectra: {}'.format(len(spectrum_list)))
    print('MS1/MS2: {}/{}'.format(stats_dict['MS1'], stats_dict['MS2']))

    if not args.check_only:

        if args.ms1_count is not None:
            reduce_spectras(spectrum_list_node, stats_dict['ms1_threshold'])

            spectrum_list_after = spectrum_list_node.findall(prepend_ns('spectrum'))
            stats_dict_after = calculate_stats_dict(spectrum_list_after, args.ms1_count)
            print('Number of spectra after: {}'.format(len(spectrum_list_after)))
            print('MS1/MS2 after: {}/{}'.format(stats_dict_after['MS1'], stats_dict_after['MS2']))

        out_tree.write(args.output)


def register_namespaces():
    et.register_namespace('', NAMESPACE)
    et.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    et.register_namespace('schemaLocation', "http://psi.hupo.org/ms/mzml http://psidev.info/files/ms/mzML/xsd/mzML1.1.0.xsd")
    # et.register_namespace('schemaLocation', 'http://psi.hupo.org/ms/mzml http://psidev.info/files/ms/mzML/xsd/mzML1.1.2_idx.xsd')


def prepend_ns(s):
    return "{" + NAMESPACE + "}" + s


def calculate_stats_dict(spectrum_list, ms1_threshold=None):

    stats_dict = dict()
    stats_dict['MS1'] = 0
    stats_dict['MS2'] = 0
    stats_dict['ms1_threshold'] = None

    total_spectras = 0
    for spectrum in spectrum_list:

        total_spectras += 1
        spec_dict = get_spect_dict(spectrum)
        if spec_dict['ms level'] == '1':
            stats_dict['MS1'] += 1

            if ms1_threshold is not None and \
                    stats_dict['ms1_threshold'] is None and \
                    stats_dict['MS1'] == ms1_threshold:
                stats_dict['ms1_threshold'] = total_spectras

        elif spec_dict['ms level'] == '2':
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


def reduce_spectras(spectrum_list_node, threshold):

    print('Threshold: {}'.format(threshold))

    remove_nodes = list()

    passed_spect = 0
    for child in spectrum_list_node:
        passed_spect += 1
        if passed_spect > threshold:
            remove_nodes.append(child)

    for node in remove_nodes:
        spectrum_list_node.remove(node)

    return spectrum_list_node


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output')

    parser.add_argument('--is_indexed', action='store_true', default=False)

    parser.add_argument('--ms1_count', type=int)
    parser.add_argument('--tot_count', type=int)

    parser.add_argument('--check_only', action='store_true', help='Print information about sample')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
