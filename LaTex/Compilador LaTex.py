import subprocess
import os

# Caminho do arquivo .tex
tex_file = 'samurai.tex'
tex_dir = r"LaTex\D_D_5e_LaTeX_Template__1_"
# Compila usando XeLaTeX (pode trocar por pdflatex ou lualatex)
subprocess.run(["xelatex", "-interaction=nonstopmode", tex_file], cwd= tex_dir)

pdf_path = os.path.join(tex_dir, 'example.pdf')

if not os.path.exists(pdf_path):
    print("PDF não gerado. Veja o log.")
