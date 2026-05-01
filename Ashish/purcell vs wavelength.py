import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# ================================
# Configuration
# ================================

# Define the directory containing the data files
data_directory = os.path.expanduser(r"C:\Users\arpit\Downloads\for data\for data\Thickness\Purcell Factor vs Wavelength")

# List of data files to process
data_files = ['100nm.txt', '200nm.txt', '300nm.txt', '400nm.txt', '500nm.txt']

# Corresponding thickness values in nm
thickness_values = [100, 200, 300, 400, 500]  # in nm

# Define output directories for plots
individual_plots_dir = os.path.join(data_directory, "Individual_Plots")
combined_plots_dir = os.path.join(data_directory, "Combined_Plots")

# Create output directories if they don't exist
os.makedirs(individual_plots_dir, exist_ok=True)
os.makedirs(combined_plots_dir, exist_ok=True)

# ================================
# Define the Lorentzian Function
# ================================

def lorentzian(x, amplitude, center, gamma):
    """
    Lorentzian function for curve fitting.

    Parameters:
    - x (float or array): Independent variable (wavelength in µm).
    - amplitude (float): Peak amplitude.
    - center (float): Center position of the peak.
    - gamma (float): Half-width at half-maximum (HWHM).

    Returns:
    - float or array: Lorentzian function evaluated at x.
    """
    return amplitude * (gamma*2 / ((x - center)*2 + gamma*2))

# ================================
# Matplotlib Settings for High-Quality Plots
# ================================

plt.style.use('ggplot')  # Use a clean and professional style
plt.rcParams.update({
    'font.size': 14,             # Base font size
    'axes.labelsize': 16,        # Axis label size
    'axes.titlesize': 18,        # Plot title size
    'legend.fontsize': 12,       # Legend font size
    'figure.figsize': (10, 6),   # Default figure size (width, height) in inches
    'savefig.dpi': 300,          # Save figures with 300 DPI
    'figure.dpi': 300             # Display figures with 300 DPI
})

# ================================
# Containers to Store Results
# ================================

all_fits = {}    # Stores Lorentzian fit parameters for each thickness
all_fwhm = {}    # Stores FWHM values for each thickness
all_max = {}     # Stores maximum Purcell factor values for each thickness
data_cache = {}

# ================================
# Process Each Data File Individually
# ================================

for file, thickness in zip(data_files, thickness_values):
    if thickness not in data_cache:
        # Construct the full file path
        file_path = os.path.join(data_directory, file)
        print(f"\nProcessing file: {file_path}")
        
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"File {file} does not exist. Skipping.")
            continue
        
        try:
            # Read the data file
            data = pd.read_csv(
                file_path,
                sep=',',               # Comma-separated
                header=0,              # First row is the header
                names=['wavelength_m', 'Purcell'],  # Column names
                engine='python',
                comment='#',           # Skip lines starting with '#'
                skip_blank_lines=True
            )
            print(f"Initial data shape: {data.shape}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        # Convert columns to numeric, coercing errors to NaN
        data['wavelength_m'] = pd.to_numeric(data['wavelength_m'], errors='coerce')
        data['Purcell'] = pd.to_numeric(data['Purcell'], errors='coerce')

        # Drop rows with NaN values
        initial_length = len(data)
        data.dropna(inplace=True)
        final_length = len(data)
        if final_length < initial_length:
            print(f"Warning: Dropped {initial_length - final_length} non-numeric rows from {file}.")

        # Convert wavelength from meters to micrometers (µm)
        data['wavelength'] = data['wavelength_m'] * 1e6  # 1 m = 1e6 µm
        wavelength = data['wavelength'].values
        purcell = data['Purcell'].values

        # Debug: Print first few rows to verify
        print(f"First 5 rows after cleaning and conversion:\n{data.head()}")

        # Check if Purcell data is empty after cleaning
        if len(purcell) == 0:
            print(f"No valid Purcell data in {file}. Skipping.")
            continue

        if not np.any(np.isfinite(purcell)):
            print(f"No valid data points in {file}")
            continue

        # ================================
        # Peak Detection
        # ================================

        try:
            # Detect peaks with height above 10% of the maximum Purcell factor
            peaks, properties = find_peaks(purcell, height=np.max(purcell)*0.1, distance=5)
        except Exception as e:
            print(f"Error finding peaks in {file}: {e}")
            continue

        if len(peaks) == 0:
            print(f"No peaks found in {file}.")
            continue

        # ================================
        # Lorentzian Fitting for Each Peak
        # ================================

        fit_params = []  # To store fit parameters for this file

        for peak in peaks:
            # Initial guesses for Lorentzian parameters
            amplitude_guess = purcell[peak]
            center_guess = wavelength[peak]
            half_max = amplitude_guess / 2

            # Estimate gamma (HWHM) by finding where the signal crosses half max
            try:
                # Left side
                left_side = purcell[:peak]
                left_indices = np.where(left_side < half_max)[0]
                if len(left_indices) == 0:
                    left_idx = 0
                else:
                    left_idx = left_indices[-1]

                # Right side
                right_side = purcell[peak:]
                right_indices = np.where(right_side < half_max)[0]
                if len(right_indices) == 0:
                    right_idx = len(purcell) - 1
                else:
                    right_idx = peak + right_indices[0]

                # Calculate gamma_guess
                gamma_guess = (wavelength[right_idx] - wavelength[left_idx]) / 2
                if gamma_guess <= 0:
                    gamma_guess = 0.1  # Fallback guess
            except Exception as e:
                print(f"Error estimating gamma for peak at {center_guess} µm in {file}: {e}")
                gamma_guess = 0.1  # Fallback guess

            # Define the fitting range around the peak
            fitting_range = 5 * gamma_guess  # +/- 5*gamma_guess
            mask = (wavelength >= (center_guess - fitting_range)) & (wavelength <= (center_guess + fitting_range))
            x_fit = wavelength[mask]
            y_fit = purcell[mask]

            # Avoid fitting if not enough points
            if len(x_fit) < 5:
                print(f"Not enough points to fit peak at {center_guess} µm in {file}. Skipping this peak.")
                continue

            try:
                # Perform Lorentzian curve fitting
                popt, _ = curve_fit(lorentzian, x_fit, y_fit, p0=[amplitude_guess, center_guess, gamma_guess])
                fit_params.append(popt)
                print(f"Fitted peak at {center_guess:.4f} µm with parameters: Amplitude={popt[0]:.6f}, Center={popt[1]:.6f} µm, Gamma={popt[2]:.6f} µm")
            except RuntimeError:
                print(f"Could not fit peak at wavelength {center_guess} µm in file {file}.")
                continue
            except Exception as e:
                print(f"Error fitting peak at {center_guess} µm in file {file}: {e}")
                continue

        if not fit_params:
            print(f"No successful Lorentzian fits for {file}.")
            continue

        # Store the fit parameters
        all_fits[thickness] = fit_params

        # Calculate FWHM and maximum Purcell factor for each fitted peak
        fwhm_list = []
        max_list = []
        for params in fit_params:
            amplitude, center, gamma = params
            fwhm = 2 * gamma  # FWHM = 2 * Gamma
            fwhm_list.append(fwhm)
            max_list.append(amplitude)

        all_fwhm[thickness] = fwhm_list
        all_max[thickness] = max_list

        # ================================
        # Generate and Save Individual Plot
        # ================================

        plt.figure(figsize=(12, 8))  # Increased figure size for better visibility
        plt.plot(wavelength, purcell, label='Purcell Factor', color='blue', linewidth=2)

        for params in fit_params:
            amplitude, center, gamma = params
            x_fit = np.linspace(center - 5*gamma, center + 5*gamma, 1000)  # More points for smoother curve
            plt.plot(x_fit, lorentzian(x_fit, *params), '--', label=f'Lorentzian Fit at {center:.4f} µm', linewidth=1.5)

        plt.title(f'Purcell Factor vs Wavelength for {thickness} nm Thickness', fontsize=20)
        plt.xlabel('Wavelength (µm)', fontsize=18)
        plt.ylabel('Purcell Factor', fontsize=18)
        plt.legend(fontsize=14, loc='upper right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save the individual plot
        individual_plot_filename = f'Purcell_Factor_{thickness}nm.png'
        individual_plot_path = os.path.join(individual_plots_dir, individual_plot_filename)
        plt.savefig(individual_plot_path, dpi=300)  # High DPI
        plt.close()
        print(f"Saved individual plot for {thickness} nm at {individual_plot_path}")

        plt.close('all')  # At the end of processing each file

# ================================
# Generate Combined Plots
# ================================

# -------------------------------
# Combined First Plot: Purcell vs Wavelength with Lorentzian Fits
# -------------------------------
plt.figure(figsize=(14, 10))  # Larger figure for combined plot
for thickness in thickness_values:
    if thickness not in all_fits:
        print(f"Skipping {thickness} nm for the combined Purcell plot due to no fit data.")
        continue
    file = f"{thickness}nm.txt"
    file_path = os.path.join(data_directory, file)
    try:
        data = pd.read_csv(
            file_path,
            sep=',',
            header=0,
            names=['wavelength_m', 'Purcell'],
            engine='python',
            comment='#',
            skip_blank_lines=True
        )
    except Exception as e:
        print(f"Error reading {file} for the combined Purcell plot: {e}")
        continue

    # Convert columns to numeric, coercing errors to NaN
    data['wavelength_m'] = pd.to_numeric(data['wavelength_m'], errors='coerce')
    data['Purcell'] = pd.to_numeric(data['Purcell'], errors='coerce')

    # Drop rows with NaN values
    data.dropna(inplace=True)

    # Convert wavelength from meters to micrometers (µm)
    data['wavelength'] = data['wavelength_m'] * 1e6
    wavelength = data['wavelength'].values
    purcell = data['Purcell'].values

    # Plot Purcell factor
    plt.plot(wavelength, purcell, label=f'{thickness} nm', linewidth=2)

    # Plot Lorentzian fits
    for params in all_fits[thickness]:
        amplitude, center, gamma = params
        x_fit = np.linspace(center - 5*gamma, center + 5*gamma, 1000)
        plt.plot(x_fit, lorentzian(x_fit, *params), '--', linewidth=1.5)

plt.title('Purcell Factor vs Wavelength with Lorentzian Fits', fontsize=22)
plt.xlabel('Wavelength (µm)', fontsize=18)
plt.ylabel('Purcell Factor', fontsize=18)
plt.legend(fontsize=14, loc='upper right')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the combined first plot
combined_purcell_plot_path = os.path.join(combined_plots_dir, 'Purcell_Factor_With_Fits.png')
plt.savefig(combined_purcell_plot_path, dpi=300)  # High DPI
plt.close()
print(f"Saved the combined Purcell Factor plot at {combined_purcell_plot_path}")

# -------------------------------
# Combined Second Plot: FWHM vs Wavelength
# -------------------------------
plt.figure(figsize=(14, 10))  # Larger figure for better visibility
for thickness in thickness_values:
    if thickness not in all_fwhm:
        print(f"Skipping {thickness} nm for the combined FWHM plot due to no fit data.")
        continue
    fwhm = all_fwhm[thickness]
    centers = [params[1] for params in all_fits[thickness]]
    plt.scatter(centers, fwhm, label=f'{thickness} nm', s=100)  # Larger markers

    # Annotate FWHM
    for center, width in zip(centers, fwhm):
        plt.annotate(f'{width:.6f}', (center, width), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)

plt.title('FWHM vs Wavelength', fontsize=22)
plt.xlabel('Wavelength (µm)', fontsize=18)
plt.ylabel('FWHM (µm)', fontsize=18)
plt.legend(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the combined FWHM plot
combined_fwhm_plot_path = os.path.join(combined_plots_dir, 'FWHM_vs_Wavelength.png')
plt.savefig(combined_fwhm_plot_path, dpi=300)  # High DPI
plt.close()
print(f"Saved the combined FWHM vs Wavelength plot at {combined_fwhm_plot_path}")

# -------------------------------
# Combined Third Plot: Maximum Purcell Factor vs Wavelength
# -------------------------------
plt.figure(figsize=(14, 10))  # Larger figure for better visibility
for thickness in thickness_values:
    if thickness not in all_max:
        print(f"Skipping {thickness} nm for the combined Maximum Purcell plot due to no fit data.")
        continue
    maxima = all_max[thickness]
    centers = [params[1] for params in all_fits[thickness]]
    plt.scatter(centers, maxima, label=f'{thickness} nm', s=100)  # Larger markers

    # Annotate maxima
    for center, max_val in zip(centers, maxima):
        plt.annotate(f'{max_val:.6f}', (center, max_val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=12)

plt.title('Maximum Purcell Factor vs Wavelength', fontsize=22)
plt.xlabel('Wavelength (µm)', fontsize=18)
plt.ylabel('Maximum Purcell Factor', fontsize=18)
plt.legend(fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the combined Maximum Purcell factor plot
combined_max_plot_path = os.path.join(combined_plots_dir, 'Maximum_Purcell_vs_Wavelength.png')
plt.savefig(combined_max_plot_path, dpi=300)  # High DPI
plt.close()
print(f"Saved the combined Maximum Purcell Factor plot at {combined_max_plot_path}")

# ================================
# Final Output
# ================================

print("\nAll high-quality plots have been generated and saved successfully.")