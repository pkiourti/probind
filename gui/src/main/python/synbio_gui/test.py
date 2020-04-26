import os
import numpy as np
from utils import data_files, switch, convert_dna_seq_to_matrix, complement_base

bases = 4
project_root = os.environ.get('PYTHONPATH')
print(project_root)

def gen_save_rev_seq(fwd_seq_filepath):
    fwd_seq_file_name = os.path.splitext(os.path.basename(fwd_seq_filepath))[0]
    fwd_seqs = np.load(fwd_seq_filepath)
    identity_matrix = np.eye(bases, dtype=int)
    rev_seqs = []

    for f in fwd_seqs:  # for each fwd sequence
        fwd_seq_transpose = np.transpose(f)
        rev = np.flip([identity_matrix[complement_base(np.argmax(i))].tolist() for i in fwd_seq_transpose], 0)
        rev = np.transpose(rev)
        rev_seqs.append(rev)

    reverse = np.asarray(rev_seqs)

    # name_int = fwd_seq_file_name[fwd_seq_file_name.find('_', 2) + 1:]
    rev_file_name = fwd_seq_file_name + '_reverse.npy'

    np.save(os.path.join(project_root, 'data', rev_file_name), reverse)

    return rev_file_name

if __name__ == '__main__':
    filepath = '../data/x_forward_1_reverse.npy'
    x = np.load(filepath)
    print(x)
    print(x.shape)
