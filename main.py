import tkinter as tk
from tkinter import messagebox, filedialog
import os

def gerar_sql_script(texto_ids, caminho_salvar):
    # Divide o texto por quebras de linha e limpa espaços/aspas/vírgulas inúteis
    linhas = texto_ids.split('\n')
    ids_limpos = [lin.strip().strip("'\",") for lin in linhas if lin.strip()]
    
    if not ids_limpos:
        raise ValueError("Nenhum ID válido foi encontrado no campo de texto.")

    # Formata as linhas para o INSERT
    valores_insert = ",\n".join([f"\t('{id_str}')" for id_str in ids_limpos])

    # Template SQL Otimizado (Com controle de Transação e Segurança)
    sql_template = f"""DECLARE @IdsParaProcessar TABLE (
    ID_ESOCIAL Varchar(36),
    UID UNIQUEIDENTIFIER
);

-- Inserir id's para deletar!
INSERT INTO @IdsParaProcessar (ID_ESOCIAL)
VALUES
{valores_insert};

    UPDATE p
    SET p.UID = e.UID
    FROM @IdsParaProcessar p
    INNER JOIN ESOCIAL_EVENTO e 
    ON e.ID_ESOCIAL = p.ID_ESOCIAL;

    DELETE FROM ESOCIAL_EVENTO_ALTERADO
    WHERE ID_ESOCIAL_EVENTO IN (SELECT UId FROM @IdsParaProcessar);

    DELETE FROM ESOCIAL_EVENTO_ARQUIVO
    WHERE ID_ESOCIAL_EVENTO IN (SELECT UId FROM @IdsParaProcessar);

    DELETE FROM ESOCIAL_EVENTO_TOTALIZADOR
    WHERE ID_ESOCIAL_EVENTO IN (SELECT UId FROM @IdsParaProcessar);

    DELETE ec FROM 
    ESOCIAL_LOTE_EVENTO_OCORRENCIA as ec
    join ESOCIAL_LOTE_EVENTO e on
    ec.ID_ESOCIAL_LOTE_EVENTO = e.UId
    WHERE e.ID_ESOCIAL_EVENTO IN (SELECT UId FROM @IdsParaProcessar);

    DELETE FROM ESOCIAL_LOTE_EVENTO
    WHERE ID_ESOCIAL_EVENTO IN (SELECT UId FROM @IdsParaProcessar);

    DELETE FROM ESOCIAL_EVENTO
    WHERE UId IN (SELECT UId FROM @IdsParaProcessar);

    DELETE FROM ESOCIAL_IMPORTADOR
    WHERE ID_ESOCIAL IN (SELECT ID_ESOCIAL FROM @IdsParaProcessar);"""

    with open(caminho_salvar, "w", encoding="utf-8") as f:
        f.write(sql_template)


class AppGeradorSQL:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Script de Deleção - eSocial")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)

        # Label de instrução
        self.label = tk.Label(root, text="Cole a lista de IDs abaixo (um por linha):", font=("Arial", 10, "bold"))
        self.label.pack(pady=10, anchor="w", padx=15)

        # Caixa de Texto com barra de rolagem
        self.container_texto = tk.Frame(root)
        self.container_texto.pack(fill="both", expand=True, padx=15, pady=5)

        self.scrollbar = tk.Scrollbar(self.container_texto)
        self.scrollbar.pack(side="right", fill="y")

        self.txt_ids = tk.Text(self.container_texto, yscrollcommand=self.scrollbar.set, font=("Consolas", 10))
        self.txt_ids.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.txt_ids.yview)

        # Botão de Ação
        self.btn_gerar = tk.Button(root, text="Gerar Script SQL", command=self.processar, bg="#107c41", fg="white", font=("Arial", 11, "bold"), height=2)
        self.btn_gerar.pack(fill="x", padx=15, pady=15)

    def processar(self):
        conteudo = self.txt_ids.get("1.0", tk.END)
        
        if not conteudo.strip():
            messagebox.showwarning("Aviso", "Insira pelo menos um ID para processar.")
            return

        # Abre a janela para escolher onde salvar o arquivo .sql
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("Arquivos SQL", "*.sql"), ("Todos os arquivos", "*.*")],
            initialfile="script_delete_esocial.sql",
            title="Salvar Script SQL"
        )

        if caminho_arquivo:  # Se o usuário não cancelou a janela de salvar
            try:
                gerar_sql_script(conteudo, caminho_arquivo)
                messagebox.showinfo("Sucesso", f"Script gerado com sucesso em:\n{caminho_arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o arquivo:\n{str(e)}")

# Execução do App
if __name__ == "__main__":
    root = tk.Tk()
    app = AppGeradorSQL(root)
    root.mainloop()