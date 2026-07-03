import tkinter as tk

from eventos import processar

class AppGeradorSQL:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Script de Deleção - eSocial")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        self.label = tk.Label(root, text="Cole a lista de IDs abaixo (um por linha):", font=("Arial", 10, "bold"))
        self.label.pack(pady=10, anchor="w", padx=15)

        self.container_texto = tk.Frame(root)
        self.container_texto.pack(fill="both", expand=True, padx=15, pady=5)

        self.scrollbar = tk.Scrollbar(self.container_texto)
        self.scrollbar.pack(side="right", fill="y")

        self.txt_ids = tk.Text(self.container_texto, yscrollcommand=self.scrollbar.set, font=("Consolas", 10))
        self.txt_ids.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.txt_ids.yview)

        self.btn_gerar = tk.Button(root, text="Gerar Script SQL", command=self.processar, bg="#107c41", fg="white", font=("Arial", 11, "bold"), height=2)
        self.btn_gerar.pack(fill="x", padx=15, pady=15)
        
    def processar(self):
        processar(self.txt_ids.get("1.0", tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGeradorSQL(root)
    root.mainloop()