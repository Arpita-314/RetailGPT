# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 00:53:37 2024

@author: ge83sax
"""
# -*- coding: utf-8 -*-
"""
Created on 2023-10-15

@author:
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Function to recursively find all CSV files in a directory and subdirectories
def find_csv_files(directory):
    """
    Recursively finds all CSV files in the given directory and subdirectories.

    Parameters:
    - directory (str): The directory path where to look for CSV files.

    Returns:
    - csv_files (list): A list of paths to CSV files.
    """
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    if not csv_files:
        print("No CSV files found in the directory and its subdirectories.")
    return csv_files

# Function to automatically plot data from CSV files
def auto_plot_csv_file(file_path):
    """
    Automatically reads the CSV file and generates plots.

    Parameters:
    - file_path (str): The full path to the CSV file.
    """
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)
        # Check if data is empty
        if data.empty:
            print(f"Warning: The file '{file_path}' is empty. Skipping.")
            return

        # Identify the x-axis column
        x_column = None
        for col in data.columns:
            if 'freq' in col.lower():
                x_column = col
                break

        if x_column is None:
            # If no frequency column is found, use the first column as x-axis
            x_column = data.columns[0]
            print(f"No frequency column found in '{file_path}'. Using '{x_column}' as x-axis.")

        # Check if x_column is numeric
        if not np.issubdtype(data[x_column].dtype, np.number):
            print(f"Error: The x-axis column '{x_column}' in '{file_path}' is not numeric. Skipping.")
            return

        # Use the remaining columns as y-axis
        y_columns = [col for col in data.columns if col != x_column]

        if not y_columns:
            print(f"No data columns found for plotting in '{file_path}'.")
            return

        # Determine the directory of the CSV file
        csv_dir = os.path.dirname(file_path)
        # Get the subfolder name
        subfolder_name = os.path.basename(csv_dir)
        # Create the plot folder inside the CSV file's directory
        plot_folder_name = f"{subfolder_name} plot"
        plot_folder = os.path.join(csv_dir, plot_folder_name)
        os.makedirs(plot_folder, exist_ok=True)

        # For each y-axis column, generate plots
        for y_column in y_columns:
            # Check if y_column is numeric
            if not np.issubdtype(data[y_column].dtype, np.number):
                print(f"Warning: The y-axis column '{y_column}' in '{file_path}' is not numeric. Skipping.")
                continue

            # Generate linear plot
            plot_data(
                data,
                x_column,
                y_column,
                title=f"{y_column} vs {x_column} (Linear Scale)",
                x_scale='linear',
                y_scale='linear',
                plot_folder=plot_folder,
                filename_prefix=os.path.splitext(os.path.basename(file_path))[0]
            )

            # Generate logarithmic plot
            plot_data(
                data,
                x_column,
                y_column,
                title=f"{y_column} vs {x_column} (Logarithmic Scale)",
                x_scale='log',
                y_scale='linear',
                plot_folder=plot_folder,
                filename_prefix=os.path.splitext(os.path.basename(file_path))[0]
            )

    except pd.errors.EmptyDataError:
        print(f"Warning: The file '{file_path}' is empty or contains only headers. Skipping.")
    except pd.errors.ParserError as e:
        print(f"Error parsing '{file_path}': {e}. Skipping.")
    except Exception as e:
        print(f"Error processing '{file_path}': {e}. Skipping.")

# Function to plot data from DataFrame and save as TIFF
def plot_data(data, x_column, y_column, title, x_scale='linear', y_scale='linear', plot_folder='.', filename_prefix='plot'):
    """
    Plots the specified data columns with given scaling options and saves the plot as a TIFF file.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x_column (str): The name of the column for the x-axis.
    - y_column (str): The name of the column for the y-axis.
    - title (str): The title of the plot.
    - x_scale (str): The scale for the x-axis ('linear' or 'log').
    - y_scale (str): The scale for the y-axis ('linear' or 'log').
    - plot_folder (str): The directory where the plot will be saved.
    - filename_prefix (str): The prefix for the plot filename.
    """
    try:
        # Prepare the plot
        plt.figure(figsize=(10, 6))
        plt.plot(data[x_column], data[y_column], marker='o', label=y_column)
        plt.xscale(x_scale)
        plt.yscale(y_scale)
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(title)
        plt.grid(True)
        plt.legend()

        # Prepare filename
        scale = 'log' if x_scale == 'log' else 'linear'
        safe_y_column = y_column.replace('/', '_').replace('\\', '_').replace(':', '_')
        filename = f"{filename_prefix}_{safe_y_column}_{scale}.tiff"
        save_path = os.path.join(plot_folder, filename)

        # Save the plot as TIFF with high DPI
        plt.savefig(save_path, format='tiff', dpi=300)
        plt.close()  # Close the figure to free memory
        print(f"Plot saved as {save_path}")
    except Exception as e:
        print(f"Error plotting '{y_column}' vs '{x_column}' in '{filename_prefix}': {e}")
        plt.close()

def select_directory():
    """
    Opens a GUI dialog to select a directory and returns the selected path.

    Returns:
    - directory (str): The selected directory path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring the dialog to the front
    directory = filedialog.askdirectory(title="Select Directory Containing CSV Files")
    root.destroy()
    return directory

def main():
    """
    Main function to execute the script.
    """
    # Select the directory using GUI
    directory = select_directory()

    if not directory:
        print("No directory selected. Exiting.")
        sys.exit(1)

    # Normalize the path to handle any issues with slashes
    directory = os.path.normpath(directory)

    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        sys.exit(1)

    # Find all CSV files in the directory and subdirectories
    csv_files = find_csv_files(directory)
    if not csv_files:
        sys.exit(1)  # Exit if no CSV files are found

    # Process each CSV file
    for csv_file in csv_files:
        print(f"\nProcessing file: {csv_file}")
        auto_plot_csv_file(csv_file)

    print("\nProcessing complete.")

if __name__ == '__main__':
    main()
