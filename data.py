import numpy as np


class DNASeqGenerator(object):

    def __init__(self, seq_length):
        super().__init__()
        self.length = seq_length
        self.channels = 1
        self.bases = 4

    @staticmethod
    def complement_base(idx):
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
        reverse_complement = np.flip([identity_matrix[self.complement_base(np.argmax(i))].tolist() for i in forward_seq], 0)

        return np.transpose(forward_seq), np.transpose(reverse_complement)

    def create_random_bind_value(self):
        return np.random.random()
