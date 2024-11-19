import numpy as np
from doctr.models import detection_predictor
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

import tensorflow as tf
import warnings

# Menonaktifkan peringatan TensorFlow
tf.get_logger().setLevel('ERROR')

def extract_with_ocr(image_path):
    """
    Menggunakan python-doctr untuk mengekstrak teks dari gambar.

    Args:
        image_path (str): Path gambar yang akan diproses.

    Returns:
        str: Teks yang diekstrak dari gambar.
    """
    # Load pretrained model
    model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small', pretrained=True)

    # Load image
    single_img_doc = DocumentFile.from_images(image_path)

    # Perform OCR
    result = model(single_img_doc)

    # Export results
    output = result.export()

    text_output = result.render()

    # Extract words
    separated_words = []
    for page in output['pages']:
      for block in page['blocks']:
        for line in block['lines']:
          for word in line['words']:
            separated_words.append(word.get('text') or word.get('value'))  # Gunakan key yang sesuai


    # Combine words into a single string
    return ' '.join(separated_words)

if __name__ == "__main__":
    image_path = "./image2.png"  # Ganti dengan path gambar
    extracted_text = extract_with_ocr(image_path)
    print("Teks yang diekstrak:")
    print(extracted_text)