import numpy as np
from skimage.transform import radon
from skimage.transform import iradon

def single_slit_diffraction(intensity, wavelength, slit_width, distance, x):
    """
    Calculate the diffraction pattern for a single slit.

    Parameters:
    intensity (float): The intensity of the light source.
    wavelength (float): The wavelength of the light (in meters).
    slit_width (float): The width of the slit (in meters).
    distance (float): The distance from the slit to the screen (in meters).
    x (numpy array): The positions on the screen where the intensity is calculated (in meters).

    Returns:
    numpy array: The intensity pattern on the screen.
    """
    beta = (np.pi * slit_width * x) / (wavelength * distance)
    return intensity * (np.sinc(beta / np.pi) ** 2)

def phase_retrieval(intensity_pattern, iterations=100):
    """
    Perform phase retrieval from an intensity pattern using the Gerchberg-Saxton algorithm.

    Parameters:
    intensity_pattern (numpy array): The intensity pattern from which to retrieve the phase.
    iterations (int): The number of iterations to perform.

    Returns:
    numpy array: The retrieved phase.
    """
    # Initial guess for the phase
    phase = np.exp(1j * np.random.rand(*intensity_pattern.shape))
        
    for _ in range(iterations):
        # Apply the intensity constraint in the spatial domain
        field = np.sqrt(intensity_pattern) * np.exp(1j * np.angle(phase))
            
        # Fourier transform to the frequency domain
        field_ft = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(field)))
            
        # Apply the intensity constraint in the frequency domain
        phase = np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(field_ft)))
            
    return np.angle(phase)
    
def compute_sinogram(image, angles):
    """
    Compute the sinogram of an image for a set of projection angles.

    Parameters:
    image (numpy array): The 2D image to be projected.
    angles (numpy array): The projection angles (in degrees).

    Returns:
    numpy array: The sinogram of the image.
    """
    return radon(image, theta=angles, circle=True)

def reconstruct_image(sinogram, angles):
    """
    Reconstruct an image from its sinogram using the filtered back projection algorithm.

    Parameters:
    sinogram (numpy array): The sinogram of the image.
    angles (numpy array): The projection angles (in degrees).

    Returns:
    numpy array: The reconstructed image.
    """
    return iradon(sinogram, theta=angles, circle=True)

# modules/tomography.py


import numpy as np
import matplotlib.pyplot as plt

# Define a 2D Fourier Transform
def dft2(image):
    M, N = image.shape
    F = np.zeros((M, N), dtype=complex)
    for u in range(M):
        for v in range(N):
            for x in range(M):
                for y in range(N):
                    F[u, v] += image[x, y] * np.exp(-2j * np.pi * ((u * x / M) + (v * y / N)))
    return F

# Create a simple image (e.g., Gaussian aperture)
x = np.linspace(-10, 10, 50)
y = np.linspace(-10, 10, 50)
X, Y = np.meshgrid(x, y)
aperture = np.exp(-X**2 - Y**2)

# Compute DFT
fft_aperture = dft2(aperture)

# Visualize
plt.imshow(np.abs(fft_aperture), extent=(-10, 10, -10, 10))
plt.title("Hard-coded Fourier Transform")
plt.show()

