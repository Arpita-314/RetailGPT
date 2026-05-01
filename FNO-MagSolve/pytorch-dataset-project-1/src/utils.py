def generate_synthetic_nv_data(size=(128, 128)):
    """Generate a synthetic real-space magnetic field map."""
    x = np.linspace(-1, 1, size[0])
    y = np.linspace(-1, 1, size[1])
    X, Y = np.meshgrid(x, y)
    field_map = np.sin(5 * np.pi * X) * np.cos(5 * np.pi * Y)  # Simulated field pattern
    return field_map

def normalize_data(data):
    """Normalize data to [-1, 1] range for stable training."""
    data_min, data_max = data.min(), data.max()
    return 2 * (data - data_min) / (data_max - data_min) - 1