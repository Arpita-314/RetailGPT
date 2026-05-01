# PyTorch Dataset Project

This project implements a PyTorch Dataset for synthetic NV magnetometry data. It includes functionality for data generation, preprocessing, and model training or evaluation.

## Project Structure

```
pytorch-dataset-project
├── src
│   ├── dataset.py       # Defines the PyTorch Dataset class for loading and preprocessing data
│   ├── app.py           # Main application entry point for initializing the dataset and model
│   └── utils.py         # Utility functions for data generation and preprocessing
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Data Generation**: The dataset is generated using synthetic NV magnetometry data. The `dataset.py` file contains the logic for loading and preprocessing this data.

2. **Running the Application**: Use the `app.py` file to initialize the dataset and create a DataLoader. This file may also include training or evaluation logic for a model.

3. **Utility Functions**: The `utils.py` file provides additional functions for data normalization and other preprocessing tasks.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.