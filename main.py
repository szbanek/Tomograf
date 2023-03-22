from PIL import Image
import numpy as np
from skimage.draw import line


class Tomograph:
    def __init__(self, img, alpha=1, n_detectors=1000, phi=np.pi):
        self.img = img
        self.reshape_img()
        self.img = np.asarray(self.img)
        self.alpha = alpha
        self.n_detectors = n_detectors
        self.phi = phi
        self.n_steps = int(np.floor(180 / self.alpha))
        self.generated_sinogram = np.zeros((self.n_steps, self.n_detectors), dtype=int)
        self.bresenham_lines = []

    def reshape_img(self):
        width, height = self.img.size
        new_size = max(width, height)
        self.img = self.img.resize((new_size, new_size))

    def map_coords(self, angle):
        width = int(self.img.shape[0] / 2)
        x = int(np.cos(angle) * width) + width - 1
        y = -int(np.sin(angle) * width) + width - 1
        return x, y

    def get_sinogram(self):
        return Image.fromarray(self.generated_sinogram).convert('L')

    def normalize_img(self, img):
        brightest_pixel = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i][j] > brightest_pixel:
                    brightest_pixel = img[i][j]
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                img[i][j] = int(img[i][j] / brightest_pixel * 255)
        return img

    def generate_sinogram(self):
        i = 0
        sl_filter = self.hamming_filter(self.n_detectors)
        for angle in np.arange(0, np.pi, self.alpha * (np.pi / 180)):
            for detector in range(self.n_detectors):
                emitter_angle = angle + self.phi / 2 - detector * self.phi / (self.n_detectors - 1)
                emitter_coordX, emitter_coordY = self.map_coords(emitter_angle)
                detector_angle = angle + np.pi - self.phi / 2 + detector * self.phi / (self.n_detectors - 1)
                detector_coordX, detector_coordY = self.map_coords(detector_angle)

                rr, cc = line(emitter_coordX, emitter_coordY, detector_coordX, detector_coordY)
                self.generated_sinogram[i][detector] += self.img[rr, cc].sum()
                self.bresenham_lines.append([rr, cc])

            self.generated_sinogram[i] = np.array(np.convolve(self.generated_sinogram[i], sl_filter, 'same'))
            i += 1
            print(i)

        self.generated_sinogram = self.normalize_img(self.generated_sinogram)

    def reconstruct(self, n_images=1):
        reconstructed_img = np.zeros((self.img.shape[0], self.img.shape[1]))
        i = 0
        p = int(self.n_steps * self.n_detectors / n_images)
        generated_sinogram_flattened = self.generated_sinogram.flatten()

        for bresenham_line in self.bresenham_lines:
            rr, cc = bresenham_line
            reconstructed_img[rr, cc] += generated_sinogram_flattened[i]
            i += 1
            if i % p == 0:
                print(i, p)
                norm_reconstructed_img = reconstructed_img.copy()
                norm_reconstructed_img = self.normalize_img(norm_reconstructed_img)
                yield Image.fromarray(norm_reconstructed_img).convert('L')

    # Ram-Lak with hamming filter
    def hamming_filter(self, length):
        filter = []
        ham = np.hamming(length)
        length = int(length/2)
        for i, j in zip(range(-length, length), ham):
            if i % 2 != 0:
                val = ((-4/np.pi**2)/(i**2)) * j
                filter.append(val)
            else:
                filter.append(0)
        filter[int(length)] = 1

        return filter

    def rmse(self, img1, img2):
        return np.sqrt(np.mean((img1-img2)**2))


initial_img = Image.open('Input/Kwadraty2.jpg').convert('L')
tomograph = Tomograph(initial_img)
tomograph.generate_sinogram()
i = 0
for img in tomograph.reconstruct(n_images=3):
    path = 'Output/Reconstructed_Image/part' + str(i) + '.jpg'
    img.save(path)
    i += 1
else:
    complete_img = img
path = 'Output/Sinogram/sinogram.jpg'
tomograph.get_sinogram().save(path)
print(tomograph.rmse(np.asarray(initial_img), np.asarray(complete_img)))