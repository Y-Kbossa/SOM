import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

def user_input():
    config = argparse.ArgumentParser(prog='SOM.py', description='description', add_help=True)
    config.add_argument('row', type=int, help='Number of Row')
    config.add_argument('column', type=int, help='Number of Column')
    config.add_argument('iteration', type=int, help='Number of iteration to run')
    return config

def color_panel(row, column):
    pixel_num = row * column
    image = []
    for _ in range(pixel_num):
        image.append(random.randint(0,256, 3))
    result = np.array(image).reshape(row, column, 3)
    return result

class SOM:
    def __init__(self, image):
        self.image = image
        self.row = image.shape[0]
        self.column = image.shape[1]
    def nearest_color(self):
        sample = random.randint(0,256, 3)
        diff = []
        self.image_flatten = self.image.reshape(self.row*self.column, 3)
        for pixel in self.image_flatten:
            diff.append(np.sum(np.square(pixel - sample)))
        self.min = np.argmin(diff)
    def color_fusion(self):
        min_pixel = self.image_flatten[self.min]
        row = self.min // self.column
        column = self.min % self.column
        if row >= 1:
            self.image[row-1, column] = np.array((self.image[row-1, column] + min_pixel)/2, dtype=int)
        if (row >= 1 and column >= 1):
            self.image[row-1, column-1] = np.array((self.image[row-1, column-1] + min_pixel)/2, dtype=int)
        if (row >= 1 and column <= (self.column-2)):
            self.image[row-1, column+1] = np.array((self.image[row-1, column+1] + min_pixel)/2, dtype=int)
        if column >= 1:
            self.image[row, column-1] = np.array((self.image[row, column-1] + min_pixel)/2, dtype=int)
        if column <= self.column-2:
            self.image[row, column+1] = np.array((self.image[row, column+1] + min_pixel)/2, dtype=int)
        if row <= self.row-2 :
            self.image[row+1, column] = np.array((self.image[row+1, column] + min_pixel)/2, dtype=int)
        if (row <= self.row-2 and column >= 1) :
            self.image[row+1, column-1] = np.array((self.image[row+1, column-1] + min_pixel)/2, dtype=int)
        if (row <= self.row-2  and column <= self.column-2):
            self.image[row+1, column+1] = np.array((self.image[row+1, column+1] + min_pixel)/2, dtype=int)

if __name__ == '__main__':
    parser = user_input()
    args = parser.parse_args()
    image = color_panel(args.row, args.column)
    som = SOM(image)
    fig = plt.figure()
    ims = []
    for _ in range(args.iteration):
        som.nearest_color()
        som.color_fusion()
        ims.append([plt.imshow(image)])
    ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=100)
    ani.save('test.gif', writer="imagemagick")