import os
import numpy as np
from utils import data_files, switch, convert_dna_seq_to_matrix, complement_base

bases = 4
project_root = os.environ.get('PYTHONPATH')
print(project_root)

def convert_csv_to_npy(csv_filepath):
    forward_file, reverse_file, bind_v_file = data_files(os.path.join(project_root, 'data'))

    file = open(csv_filepath, "r")

    dna_seq = []
    binding_vals = []

    i = 1
    for line in file:
        if (i % 2 == 0):  # i.e. every 2nd row contains the binding values
            binding_vals.append(float(line.rstrip()))
        else:
            one_dna_seq = [switch(i.rstrip()) for i in line.split(',')]
            seq_matrix = convert_dna_seq_to_matrix(one_dna_seq)
            dna_seq.append(seq_matrix)

        i = i + 1

    # convert DNA seq to matrix of 0s and 1s
    identity_matrix = np.eye(bases, dtype=int)
    forward = np.asarray(dna_seq)

    rev_seqs = []

    for fwd_seq in forward:  # for each fwd sequence
        fwd_seq_transpose = np.transpose(fwd_seq)
        rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
        rev = np.transpose(rev)
        rev_seqs.append(rev)

    reverse = np.asarray(rev_seqs)
    binding_value = np.asarray(binding_vals)

    np.save(forward_file + '.npy', forward)
    np.save(reverse_file + '.npy', reverse)
    np.save(bind_v_file + '.npy', binding_value)

    x_fwd = os.path.splitext(os.path.basename(forward_file + '.npy'))[0] + '.npy'
    x_rev = os.path.splitext(os.path.basename(reverse_file + '.npy'))[0] + '.npy'
    y = os.path.splitext(os.path.basename(bind_v_file + '.npy'))[0] + '.npy'

    return x_fwd, x_rev, y

if __name__ == '__main__':
    # filepath = '../../a.csv'
    # print(convert_csv_to_npy(filepath))
    x = np.load('../data/x_forward_9.npy')
    print(x.shape)
    print(x)
    print(x.dtype)
    xr = np.load('../data/x_reverse_9.npy')
    print(xr.shape)
    print(xr)
    print(xr.dtype)
    y = np.load('../data/y_9.npy')
    print(y.shape)
    print(y)
    print(y.dtype)

    # x2 = np.load('../data/x_forward_1.npy')
    # print(x2.shape)
    # print(x2)
    # print(x2.dtype)
    # xr2 = np.load('../data/x_reverse_1.npy')
    # print(xr2.shape)
    # print(xr2)
    # print(xr2.dtype)
    # y2 = np.load('../data/y_1.npy')
    # print(y2.shape)
    # print(y2)
    # print(y2.dtype)