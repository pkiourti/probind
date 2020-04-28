import time
import sys

from backend.train_wrapper import TrainWrapper
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_done = pyqtSignal(int)
    sig_msg = pyqtSignal(int)

    def __init__(self, train_wrapper: TrainWrapper):
        super().__init__()
        # self.__abort = False
        self.train_wrapper = train_wrapper
        self.text = ""

    @pyqtSlot()
    def work(self):
        self.text = ""
        start_time = time.time()
        batches = self.train_wrapper.get_num_batches()
        for epoch in range(self.train_wrapper.epochs):
            while self.train_wrapper.get_batch_idx() < batches:
                self.text = self.text + self.train_wrapper.one_step_train(epoch)
                self.sig_msg.emit(1)
            self.train_wrapper.test()
            self.train_wrapper.reset()

        total_time = time.time() - start_time
        self.text = self.text + 'Total training time: ' + str(total_time / 60) + ' mins \n'
        self.sig_msg.emit(1)
        self.train_wrapper.save_model()

        self.sig_done.emit(1)
