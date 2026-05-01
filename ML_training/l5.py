import torch
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon

# ==============================================================
# Diffraction Simulation with PyTorch
# ==============================================================

def generate_aperture(shape: str, size: int) -> torch.Tensor:
    aperture = torch.zeros((size, size))
    center = size // 2

    if shape == "circle":
        radius = size // 4
        y, x = torch.meshgrid(torch.arange(size), torch.arange(size))
        mask = (x - center) ** 2 + (y - center) ** 2 <= radius ** 2
        aperture[mask] = 1
    elif shape == "rectangle":
        aperture[size // 4: 3 * size // 4, size // 4: 3 * size // 4] = 1
    elif shape == "slit":
        aperture[center - size // 8: center + size // 8, :] = 1
    else:
        raise ValueError("Unsupported aperture shape.")
    return aperture

def simulate_diffraction(aperture: torch.Tensor) -> torch.Tensor:
    fft_aperture = torch.fft.fftshift(torch.fft.fft2(aperture))
    intensity = torch.abs(fft_aperture) ** 2
    return intensity

# ==============================================================
# Phase Retrieval with PyTorch
# ==============================================================

def gerchberg_saxton(intensity: torch.Tensor, iterations: int = 50) -> torch.Tensor:
    phase = torch.exp(1j * torch.rand_like(intensity))
    amplitude = torch.sqrt(intensity)

    for _ in range(iterations):
        guess = amplitude * phase
        guess_fft = torch.fft.fft2(guess)
        phase_fft = torch.angle(guess_fft)
        guess_fft = amplitude * torch.exp(1j * phase_fft)
        guess = torch.fft.ifft2(guess_fft)
        phase = torch.angle(guess)
    return phase

# ==============================================================
# Tomographic Reconstruction with Total Variation Regularization
# ==============================================================

def simulate_tomography(image: torch.Tensor, angles: torch.Tensor) -> torch.Tensor:
    image_np = image.detach().numpy()
    sinogram_np = radon(image_np, theta=angles.numpy(), circle=True)
    return torch.tensor(sinogram_np)

def tv_regularized_reconstruction(sinogram: torch.Tensor, angles: torch.Tensor, lambd: float = 0.1, iterations: int = 100) -> torch.Tensor:
    size = sinogram.shape[1]
    reconstruction = torch.zeros((size, size), dtype=torch.float32, requires_grad=True)
    optimizer = torch.optim.Adam([reconstruction], lr=0.01)

    for _ in range(iterations):
        optimizer.zero_grad()
        projection = simulate_tomography(reconstruction, angles)
        data_loss = torch.nn.functional.mse_loss(projection, sinogram)
        tv_loss = lambd * torch.sum(torch.abs(reconstruction[:-1, :] - reconstruction[1:, :])) + \
                  lambd * torch.sum(torch.abs(reconstruction[:, :-1] - reconstruction[:, 1:]))
        loss = data_loss + tv_loss
        loss.backward()
        optimizer.step()

    return reconstruction.detach()

# ==============================================================
# Main Demonstration
# ==============================================================

if __name__ == "__main__":
    aperture = generate_aperture("circle", 256)
    diffraction_pattern = simulate_diffraction(aperture)

    plt.subplot(1, 2, 1)
    plt.title("Aperture")
    plt.imshow(aperture, cmap="gray")
    plt.subplot(1, 2, 2)
    plt.title("Diffraction Pattern")
    plt.imshow(torch.log(1 + diffraction_pattern).numpy(), cmap="hot")
    plt.show()

    # Phase Retrieval Example
    original_phase = torch.rand(256, 256)
    intensity = torch.abs(torch.fft.fft2(torch.exp(1j * original_phase))) ** 2
    reconstructed_phase = gerchberg_saxton(intensity)

    plt.subplot(1, 2, 1)
    plt.title("Original Phase")
    plt.imshow(original_phase.numpy(), cmap="jet")
    plt.subplot(1, 2, 2)
    plt.title("Reconstructed Phase")
    plt.imshow(reconstructed_phase.numpy(), cmap="jet")
    plt.show()

    # Tomography Example
    image = torch.zeros((256, 256))
    image[100:150, 100:150] = 1
    angles = torch.linspace(0, 180, 180)
    sinogram = simulate_tomography(image, angles)
    reconstruction = tv_regularized_reconstruction(sinogram, angles)

    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(image.detach().numpy(), cmap="gray")
    plt.subplot(1, 3, 2)
    plt.title("Sinogram")
    plt.imshow(sinogram.numpy(), cmap="gray", aspect='auto')
    plt.subplot(1, 3, 3)
    plt.title("Reconstruction")
    plt.imshow(reconstruction.numpy(), cmap="gray")
    plt.show()

import streamlit as st
import torch
import matplotlib.pyplot as plt
from xray_toolkit import generate_aperture, simulate_diffraction, tv_regularized_reconstruction

st.title("X-ray Imaging Toolkit")

st.sidebar.title("Parameters")
shape = st.sidebar.selectbox("Aperture Shape", ["circle", "rectangle", "slit"])
size = st.sidebar.slider("Aperture Size", 128, 512, 256)
iterations = st.sidebar.slider("Iterations", 10, 100, 50)

if st.button("Run Diffraction"):
    aperture = generate_aperture(shape, size)
    diffraction_pattern = simulate_diffraction(aperture)

    st.subheader("Aperture")
    st.image(aperture.numpy(), caption="Aperture", use_column_width=True)

    st.subheader("Diffraction Pattern")
    st.image(torch.log(1 + diffraction_pattern).numpy(), caption="Diffraction Pattern", use_column_width=True)
