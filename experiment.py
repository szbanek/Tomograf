from tomograph import Tomograph
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

path = 'Input/Img/CT_large.jpg'
initial_img = Image.open(path).convert('L')
# t = Tomograph(path, n_detectors=180, alpha=2, phi=np.pi) # wartości domyślne

n_detectors = [i for i in range(90, 721, 90)]
n_steps = [i for i in range(90, 721, 90)]
alpha = [180/i for i in range(90, 721, 90)]
degrees = [i for i in range(45, 271, 45)]
phi = [np.pi/180 * i for i in degrees]

# Zależność rekonstrukcji obrazu od liczby detektorów
rmse = []
for step in n_detectors:
    t = Tomograph(initial_img, n_detectors=step, alpha=2, phi=np.pi)
    t.generate_sinogram()
    for img in t.reconstruct(n_images=1):
        diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
        rmse.append(diff)

plt.plot(n_detectors, rmse)
plt.title('Zależność rekonstrukcji obrazu od liczby detektorów')
plt.xlabel('Liczba detektorów')
plt.ylabel('Błąd średniokwadratowy')
plt.xlim((n_detectors[0], n_detectors[-1]))
plt.savefig('Experiment_Results/fig1')
#plt.show()
plt.clf()

# Zależność rekonstrukcji obrazu od liczby kroków
rmse = []
for step in alpha:
    t = Tomograph(initial_img, n_detectors=180, alpha=step, phi=np.pi)
    t.generate_sinogram()
    for img in t.reconstruct(n_images=1):
        diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
        rmse.append(diff)

plt.plot(n_steps, rmse)
plt.title('Zależność rekonstrukcji obrazu od liczby kroków')
plt.xlabel('Liczba kroków')
plt.ylabel('Błąd średniokwadratowy')
plt.xlim((n_steps[0], n_steps[-1]))
plt.savefig('Experiment_Results/fig2')
#plt.show()
plt.clf()

# Zależność rekonstrukcji obrazu od rozpiętości wachlarza
rmse = []
for step in phi:
    t = Tomograph(initial_img, n_detectors=180, alpha=2, phi=step)
    t.generate_sinogram()
    for img in t.reconstruct(n_images=1):
        diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
        rmse.append(diff)

plt.plot(degrees, rmse)
plt.title('Zależność rekonstrukcji obrazu od rozpiętości wachlarza')
plt.xlabel('Rozpiętość wachlarza (°)')
plt.ylabel('Błąd średniokwadratowy')
plt.xlim((degrees[0], degrees[-1]))
plt.savefig('Experiment_Results/fig3')
#plt.show()
plt.clf()

# Zalezność rekonstrukcji obrazu od implementacji filtru
path = 'Input/Img/CT_large.jpg'
initial_img = Image.open(path).convert('L')

t = Tomograph(initial_img, n_detectors=180, alpha=2, phi=270 * np.pi/180, hamm_filter=True)
t.generate_sinogram()
for img in t.reconstruct(n_images=1):
    diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
    print('Błąd średniokwadratowy dla', path, 'z użyciem filtra:', diff)
    img.save('Experiment_Results/CT_large_filtered.png')

t = Tomograph(initial_img, n_detectors=180, alpha=2, phi=270 * np.pi/180, hamm_filter=False)
t.generate_sinogram()
for img in t.reconstruct(n_images=1):
    diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
    print('Błąd średniokwadratowy dla', path, 'bez filtra:', diff)
    img.save('Experiment_Results/CT_large_unfiltered.png')

path = 'Input/Img/Shepp_logan.jpg'
initial_img = Image.open(path).convert('L')
t = Tomograph(initial_img, n_detectors=180, alpha=2, phi=270 * np.pi/180, hamm_filter=True)
t.generate_sinogram()
for img in t.reconstruct(n_images=1):
    diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
    print('Błąd średniokwadratowy dla', path, 'z użyciem filtra:', diff)
    img.save('Experiment_Results/Shepp_logan_filtered.png')

t = Tomograph(initial_img, n_detectors=180, alpha=2, phi=270 * np.pi/180, hamm_filter=False)
t.generate_sinogram()
for img in t.reconstruct(n_images=1):
    diff = t.rmse(np.asarray(img), np.asarray(t.get_initial_img()))
    print('Błąd średniokwadratowy dla', path, 'bez filtra:', diff)
    img.save('Experiment_Results/Shepp_logan_unfiltered.png')