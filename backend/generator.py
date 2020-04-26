import numpy as np


class Generator(object):

    def __init__(self, seq_length, num_seqs):
        super().__init__()
        self.length = seq_length
        self.num = num_seqs
        self.channels = 1
        self.bases = 4

    def __complement_base__(self, idx):
        if idx == 0:
            return 1
        elif idx == 1:
            return 0
        elif idx == 2:
            return 3
        elif idx == 3:
            return 2

    def create_random_seq(self):
        identity_matrix = np.eye(self.bases, dtype=int)
        forward_seq = np.asarray([identity_matrix[np.random.choice(self.bases)] for _ in range(self.length)])
        reverse_complement = np.flip([identity_matrix[self.__complement_base__(np.argmax(i))].tolist() for i in forward_seq], 0)

        return np.transpose(forward_seq), np.transpose(reverse_complement)

    def create_random_bind_value(self):
        return np.random.random()

    def create_random_dataset(self):
        seq = np.asarray([self.create_random_seq() for _ in range(self.num)])
        forward = np.asarray(seq)[:, 0]
        reverse = np.asarray(seq)[:, 1]

        binding_values = np.asarray([self.create_random_bind_value() for _ in range(self.num)])

        return forward, reverse, binding_values