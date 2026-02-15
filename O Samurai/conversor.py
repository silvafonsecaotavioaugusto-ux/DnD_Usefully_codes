import os
import subprocess
from PIL import Image

def convert_webp(input_path, output_path):
    cmd = ['magick', input_path, output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("Conversão concluída!")
    else:
        print("Erro na conversão:")
        print(result.stderr)

def delete(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        pass

def main(delete_ : bool = False, pdf_ : bool = False):
    pasta = r"C:\Users\Otávio Augusto\OneDrive\Documentos\GitHub\DnD_Usefully_codes\O Samurai\img"
    elementos = os.listdir(pasta)

    for elemento in elementos:
        if elemento.endswith(".webp"):
            new_elemento = elemento.replace(".webp", ".jpg")
            convert_webp(os.path.join(pasta, elemento), os.path.join(pasta, new_elemento))
            if delete_:
                delete(os.path.join(pasta, elemento))
    
    elementos = os.listdir(pasta)
    if pdf_:
        imgs = []
        for elemento in elementos:
            if elemento.endswith(".jpg"):
                caminho_completo = os.path.join(pasta, elemento)
                imgs.append(Image.open(caminho_completo).convert("RGB"))

        imgs[0].save(
            "saida.pdf",
            save_all=True,
            append_images=imgs[1:]
        )

        print("PDF criado!")

main(pdf_ = True)