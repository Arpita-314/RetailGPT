from torch.utils.data import Dataset
import numpy as np

class NVMagnetometryDataset(Dataset):
    def __init__(self, size=(128, 128), transform=None):
        self.size = size
        self.transform = transform
        self.data = self.generate_synthetic_nv_data()
        self.labels = self.create_labels()

    def generate_synthetic_nv_data(self):
        x = np.linspace(-1, 1, self.size[0])
        y = np.linspace(-1, 1, self.size[1])
        X, Y = np.meshgrid(x, y)
        field_map = np.sin(5 * np.pi * X) * np.cos(5 * np.pi * Y)
        return field_map

    def create_labels(self):
        # For simplicity, let's assume labels are just the sum of the field_map values
        return np.sum(self.data)

    def __len__(self):
        return 1  # Since we are generating a single sample

    def __getitem__(self, idx):
        sample = self.data
        label = self.labels
        
        if self.transform:
            sample = self.transform(sample)

        return sample, label