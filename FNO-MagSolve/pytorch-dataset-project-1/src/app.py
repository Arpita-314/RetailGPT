from torch.utils.data import Dataset, DataLoader
import numpy as np
import torch

class NVMagnetometryDataset(Dataset):
    def __init__(self, size=(128, 128)):
        self.data = self.generate_synthetic_nv_data(size)
        self.fourier_data = self.fourier_transform(self.data)
        self.norm_fourier_data = self.normalize_data(np.abs(self.fourier_data))

    def generate_synthetic_nv_data(self, size):
        x = np.linspace(-1, 1, size[0])
        y = np.linspace(-1, 1, size[1])
        X, Y = np.meshgrid(x, y)
        field_map = np.sin(5 * np.pi * X) * np.cos(5 * np.pi * Y)
        return field_map

    def fourier_transform(self, field_map):
        ft = np.fft.fft2(field_map)
        ft_shifted = np.fft.fftshift(ft)
        return ft_shifted

    def normalize_data(self, data):
        data_min, data_max = data.min(), data.max()
        return 2 * (data - data_min) / (data_max - data_min) - 1

    def __len__(self):
        return len(self.norm_fourier_data)

    def __getitem__(self, idx):
        sample = self.norm_fourier_data[idx]
        return torch.tensor(sample, dtype=torch.float32)

if __name__ == "__main__":
    dataset = NVMagnetometryDataset()
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    for batch in dataloader:
        print(batch.shape)  # Example of processing a batch