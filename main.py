import numpy as np
import os
from generator import DNASeqGenerator


def data_files():
    i = 1
    while os.path.exists(os.path.join('data', 'x_forward_' + str(i) + '.npy')):
        i += 1

    if not os.path.exists('data'):
        os.makedirs('data')

    return (os.path.join('data', 'x_forward_' + str(i)),
            os.path.join('data', 'x_reverse_' + str(i)),
            os.path.join('data', 'y_' + str(i)))


if __name__ == '__main__':
    seq_generator = DNASeqGenerator(300)

    seq = np.asarray([seq_generator.create_random_seq() for _ in range(500)])
    forward = np.asarray(seq)[:, 0]
    reverse = np.asarray(seq)[:, 1]
    binding_value = [seq_generator.create_random_bind_value() for _ in range(500)]
    forward_file, reverse_file, bind_v_file = data_files()
    np.save(forward_file + '.npy', forward)
    np.save(reverse_file + '.npy', reverse)
    np.save(bind_v_file + '.npy', binding_value)
