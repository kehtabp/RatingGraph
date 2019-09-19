import matplotlib.pyplot as plt
import numpy as np

# Make a 9x9 grid...
from get_moves import get_moves

ranks, files = 8, 8
image = np.array(list(reversed(get_moves('kewko', piece='N', takes=True))))

# Set every other cell to a random number (this would be your data)
# image[::2] = np.random.random(1)

# Reshape things into a 9x9 grid.
# image = image.reshape((files, ranks))

rank_labels = range(files, 0, -1)
file_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
plt.matshow(image)
plt.xticks(range(files), file_labels)
plt.yticks(range(ranks), rank_labels)
plt.tick_params(right=False, bottom=False, direction='in', color='black')
for y in range(files):
    plt.plot([7.5, -.5], [y + .5, y + .5], "-", color="black")
    plt.plot([y + .5, y + .5], [7.5, -.5], "-", color="black")
# plt.plot(5, 1, "-", color="white", alpha=1)
# for x in range(ranks):
#     plt.plot(range(0, ranks),  len(range(0, ranks)) * [x] , "-", lw=0.5, color="white")

plt.show()
