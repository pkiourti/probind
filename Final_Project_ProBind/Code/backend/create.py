import numpy as np
import argparse
import os
from backend.generator import Generator

project_root = os.environ.get('PYTHONPATH')
try:
    project_root = project_root.split(os.path.pathsep)[1]
except Exception as e:
    pass


def get_parser():
    parser = argparse.ArgumentParser(description='create random data')

    parser.add_argument('--seq_len', type=int, default=300,
                        help='the sequence length should be 300 bases for training but more than 300 bases for '
                             'cross-talk evaluation',
                        dest='seq_len', required=True)
    parser.add_argument('--num_seqs', type=int, default=1000,
                        help='the number of sequences to produce. For training, it should be more than 1, '
                             'for testing you need to have one sequence per numpy so use 1',
                        dest='num_seqs', required=True)

    return parser


def data_files(data_dir_filepath):
    i = 1
    while os.path.exists(os.path.join(data_dir_filepath, 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists(data_dir_filepath):
        os.makedirs(data_dir_filepath)

    return (os.path.join(data_dir_filepath, 'x_forward_' + str(i)),
            os.path.join(data_dir_filepath, 'x_reverse_' + str(i)),
            os.path.join(data_dir_filepath, 'y_' + str(i)))


if __name__ == '__main__':
    args = get_parser().parse_args()
    generator = Generator(args.seq_len, args.num_seqs)

    forward, reverse, binding_values = generator.create_random_dataset()
    forward_file, reverse_file, bind_v_file = data_files(os.path.join(project_root, 'data'))
    np.save(forward_file + '.npy', forward)
    np.save(reverse_file + '.npy', reverse)
    np.save(bind_v_file + '.npy', binding_values)
