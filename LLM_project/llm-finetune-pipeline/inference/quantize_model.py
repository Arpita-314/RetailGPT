"""Script to quantize a fine-tuned model (placeholder).
Integrate bitsandbytes/Intel or Hugging Face quantization tools here.
"""


def quantize_model(model_path: str, output_path: str, bits: int = 8):
    print(f"Quantizing {model_path} -> {output_path} at {bits}-bit")


if __name__ == '__main__':
    quantize_model('model/', 'model-8bit/')
