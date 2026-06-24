import os
import subprocess
from PIL import Image




pasta = r"C:\Users\Otávio Augusto\OneDrive\Documentos\GitHub\DnD_Usefully_codes\O Samurai\img"
elementos = os.listdir(pasta)
imgs = []
for elemento in elementos:
    if elemento.endswith(".jpg"):
        caminho_completo = os.path.join(pasta, elemento)
        imgs.append(Image.open(caminho_completo).convert("RGB"))

imgs[0].save(
    "RG.pdf",
    save_all=True,
    append_images=imgs[1:]
)

print("PDF criado!")
