import os

def delete(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        pass

pasta = r"C:\Users\Otávio Augusto\OneDrive\Documentos\GitHub\DnD_Usefully_codes\O Samurai\img"
elementos = elementos = os.listdir(pasta)
for elemento in elementos:
    if elemento.endswith(".jpg"):
        delete(os.path.join(pasta, elemento))
