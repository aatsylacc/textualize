import tensorflow as tf
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

# Path model dan tokenizer
model_path = "./textualize_model/"
tokenizer_path = "./textualize_tokenizer/"

# Memuat model dan tokenizer yang telah disimpan
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Fungsi untuk menghasilkan ringkasan teks
def summarize_text(input_text, length_penalty=0.8, num_beams=10, max_input_length=1024):
    """    
    Args:
    - input_text (str): Teks input yang akan dirangkum.
    - length_penalty (float): Penalti panjang untuk hasil ringkasan.
    - num_beams (int): Jumlah beam untuk pencarian beam search.
    - max_input_length (int): Panjang maksimal tokenisasi input.
    
    Returns:
    - str: Teks hasil ringkasan.
    """
    # Tokenisasi input
    inputs = tokenizer.encode(
        input_text, 
        return_tensors="tf", 
        max_length=max_input_length, 
        truncation=True
    )
    
    # Hitung panjang maksimal untuk output
    max_output_length = 60

    # Hasilkan ringkasan menggunakan model
    outputs = model.generate(
        inputs,
        min_length=1,  
        max_length=max_output_length,
        length_penalty=length_penalty,
        num_beams=num_beams,
        early_stopping=True
    )
    
    # Decode token menjadi teks
    summarized_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summarized_text

# Contoh penggunaan
custom_dialogue = """
Sejarah peradaban dunia adalah cerminan perjalanan panjang manusia dari masa prasejarah hingga era modern.
Dalam perjalanan ini, manusia telah membangun masyarakat yang kompleks, menciptakan kebudayaan yang kaya,
dan melahirkan inovasi yang mengubah kehidupan.
"""
    
summarized = summarize_text(custom_dialogue)
print("Hasil Ringkasan:")
print(summarized)
