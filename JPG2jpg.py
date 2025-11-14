import streamlit as st
from PIL import Image
import os

def convert_image(input_image):
    # Mengubah ekstensi file menjadi .jpg
    image = Image.open(input_image)
    output_image_path = "converted_image.jpg"
    image = image.convert("RGB")  # Pastikan gambar di-convert ke mode RGB
    image.save(output_image_path, "JPEG")
    return output_image_path

# Judul aplikasi
st.title("Konversi Gambar JPG ke jpg")

# Deskripsi aplikasi
st.write("Unggah file gambar dengan ekstensi .JPG, dan aplikasi ini akan mengonversinya menjadi .jpg.")

# Unggah file gambar
uploaded_file = st.file_uploader("Pilih file gambar (.JPG)", type=["JPG"])

if uploaded_file is not None:
    # Menampilkan gambar yang diunggah
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang Diupload", use_column_width=True)

    # Mengonversi gambar dan simpan dengan ekstensi .jpg
    converted_file = convert_image(uploaded_file)

    # Tampilkan tombol untuk mengunduh gambar yang telah dikonversi
    with open(converted_file, "rb") as file:
        st.download_button(
            label="Unduh Gambar yang Dikonversi (.jpg)",
            data=file,
            file_name="converted_image.jpg",
            mime="image/jpeg"
        )
    
    # Hapus file sementara setelah download (opsional)
    os.remove(converted_file)
