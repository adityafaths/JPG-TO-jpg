import streamlit as st
import zipfile
import os
from PIL import Image
import io
import tempfile

st.title("Konversi JPG → jpg (Multi Folder)")

st.write("""
Upload folder dalam format **ZIP**.  
Aplikasi akan memindai seluruh isi folder dan mengubah file **.JPG** menjadi **.jpg**
tanpa mengubah struktur folder.
""")

uploaded_zip = st.file_uploader("Upload ZIP Folder", type=["zip"])

if uploaded_zip:
    # Membuat direktori sementara
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "input.zip")

        # Simpan zip ke direktori sementara
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        # Ekstrak zip
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Direktori root dari folder
        root_folder = os.listdir(temp_dir)[1]  # index 1, karena index 0 = input.zip
        root_path = os.path.join(temp_dir, root_folder)

        # Output zip buffer
        output_buffer = io.BytesIO()

        with zipfile.ZipFile(output_buffer, "w", zipfile.ZipFile.ZIP_DEFLATED) as output_zip:

            # Telusuri semua file dan folder
            for folder_path, subfolders, files in os.walk(root_path):
                for file in files:
                    file_path = os.path.join(folder_path, file)

                    # Relatif path untuk disimpan di zip
                    arcname = os.path.relpath(file_path, root_path)

                    # Jika ekstensi .JPG → konversi ke .jpg
                    if file.lower().endswith(".jpg") and not file.endswith(".jpg"):
                        new_filename = file[:-4] + ".jpg"
                        arcname = os.path.relpath(os.path.join(folder_path, new_filename), root_path)

                        img = Image.open(file_path).convert("RGB")
                        img_byte = io.BytesIO()
                        img.save(img_byte, format="JPEG")
                        img_byte.seek(0)

                        output_zip.writestr(arcname, img_byte.read())

                    else:
                        # File lain → copy apa adanya
                        output_zip.write(file_path, arcname)

        output_buffer.seek(0)

        st.success("Berhasil! Unduh folder hasil konversi di bawah:")

        st.download_button(
            label="Download ZIP Hasil Konversi",
            data=output_buffer,
            file_name="converted_folder.zip",
            mime="application/zip"
        )
