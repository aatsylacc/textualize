import tensorflow as tf
from transformers import pipeline, AutoTokenizer, TFAutoModelForSeq2SeqLM, logging
from google.cloud import storage

# Setup logging
logging.set_verbosity_error()
tf.get_logger().setLevel('ERROR')

# Path tokenizer yang masih di folder lokal
tokenizer_path = "summarize/text_token"  # Arahkan ke folder tokenizer lokal

# GCS path untuk model
model_path = "gs://textualize-model/tf_model.h5"  # Ganti jadi URL GCS bucket

# Load tokenizer dari folder lokal
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Download model dari GCS bucket
storage_client = storage.Client()
bucket = storage_client.bucket("textualize-model")
blob = bucket.blob("tf_model.h5")  # Ganti dengan path model di GCS
local_model_path = "/app/text_model/tf_model.h5"  # Simpan sementara di dalam container

# Download model dari GCS ke dalam container (di /app/text_model)
blob.download_to_filename(local_model_path)

# Load model setelah di-download ke container
model = TFAutoModelForSeq2SeqLM.from_pretrained(local_model_path)

def summarize_text(custom_dialogue):
    # Hitung jumlah kata dalam input
    word_length = len(custom_dialogue.split())
    
    # Periksa apakah jumlah kata kurang dari 10
    if word_length < 10:  
        return "The input text is too short. Please enter text with at least 10 words."
    
    # Atur panjang minimum dan maksimum output
    min_length = max(10, int(word_length * 0.2))  # Min length: 20% dari input 
    max_length = word_length  # Max length: sepanjang input 

    gen_kwargs = {
        'length_penalty': 0.8,
        'num_beams': 2,
        'min_length': min_length,
        'max_length': max_length
    }
    
    # Jalankan model untuk menghasilkan ringkasan
    summarization_pipeline = pipeline('summarization', model=model, tokenizer=tokenizer, framework='tf')
    summary = summarization_pipeline(custom_dialogue, **gen_kwargs)
    return f"Summary: {summary[0]['summary_text']}"




# Contoh penggunaan
if __name__ == "__main__":
    custom_dialogue = """
    Makassar - The Indonesian national team won its first victory in the third round of the 2026 World Cup Qualifiers in the Asian zone after defeating Saudi Arabia with a score of 2-0. This result made the Garuda squad temporarily rise to third place in the Group C standings. In the match at the Gelora Bung Karno Main Stadium (SUGBK), Jakarta, Indonesia scored a goal in each half. Indonesia's two goals to Saudi Arabia were scored by Marselino Ferdinan.
    """

    summary_result = summarize_text(custom_dialogue)
    print(summary_result)

