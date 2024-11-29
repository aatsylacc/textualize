# ocr_model.py
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


def extract_with_ocr(image_path):
    """
    Menggunakan python-doctr untuk mengekstrak teks dari gambar.

    Args:
        image_path (str): Path gambar yang akan diproses.

    Returns:
        str: Teks yang diekstrak dari gambar.
    """
    # Load pretrained model
    model = ocr_predictor(det_arch='db_resnet50',
                          reco_arch='crnn_mobilenet_v3_small',
                          pretrained=True,
                          assume_straight_pages=False,  # Tidak mengasumsikan gambar lurus
                          detect_orientation=True,      # Deteksi orientasi gambar
                          disable_crop_orientation=True,
                          disable_page_orientation=True,
                          straighten_pages=True)

    # Load image
    single_img_doc = DocumentFile.from_images(image_path)

    # Perform OCR
    result = model(single_img_doc)

    # Export results JSON
    # text_output = result.export()

    # Export results XML
    # text_output = result.export_as_xml()

    # Export results Plain Text
    text_output = result.render()
    return text_output

    # # Extract words
    # separated_words = []
    # for page in output['pages']:
    #   for block in page['blocks']:
    #     for line in block['lines']:
    #       for word in line['words']:
    #         separated_words.append(word.get('text') or word.get('value'))  # Gunakan key yang sesuai


    # # Combine words into a single string
    # return ' '.join(separated_words)    """




# Contoh penggunaan
  image_path = "image.png"  # Ganti dengan path gambar Anda
  extracted_text = extract_with_ocr(image_path)
  print("Extracted Text:")
  print(extracted_text)