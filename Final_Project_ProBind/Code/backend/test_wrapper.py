from train_wrapper import TrainWrapper
import matplotlib.pyplot as plt

t = TrainWrapper(10, 'x_forward_6.npy', 'x_reverse_6.npy', 'y_6.npy', 'test')
fig = t.train()
fig.canvas.draw()
plt.show()
"""
fig = t.run()
fig.canvas.draw()
plt.show()
"""
