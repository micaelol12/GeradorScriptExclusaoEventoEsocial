from tkinter import messagebox, filedialog
from gerador import gerar_sql_script


def processar(conteudo): 
    if not conteudo.strip():
        messagebox.showwarning("Aviso", "Insira pelo menos um ID para processar.")
        return

    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".sql",
        filetypes=[("Arquivos SQL", "*.sql"), ("Todos os arquivos", "*.*")],
        initialfile="script_delete_esocial.sql",
        title="Salvar Script SQL"
    )

    if caminho_arquivo:
        try:
            linhas = conteudo.split('\n')
            ids = [lin.strip().strip("'\",") for lin in linhas if lin.strip()]
                        
            sql_template = gerar_sql_script(ids)
            
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(sql_template)
                
            messagebox.showinfo("Sucesso", f"Script gerado com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o arquivo:\n{str(e)}")