import os, shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from storage import register_bird, load_birds
from certificate import generate_certificate, generate_tree

def list_templates(folder):
    try:
        return [f for f in os.listdir(folder) if f.lower().endswith((".png", ".pdf"))]
    except FileNotFoundError:
        return []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestão de Plantel - Certificados")
        self.geometry("700x600")
        self.setup_form()
        self.setup_list()

    def setup_form(self):
        tk.Label(self, text="Nome:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        tk.Label(self, text="Espécie:").pack()
        self.species_entry = tk.Entry(self)
        self.species_entry.pack()
        tk.Label(self, text="Anilha:").pack()
        self.anilha_entry = tk.Entry(self)
        self.anilha_entry.pack()
        tk.Label(self, text="Pai (Anilha):").pack()
        self.father_entry = tk.Entry(self)
        self.father_entry.pack()
        tk.Label(self, text="Mãe (Anilha):").pack()
        self.mother_entry = tk.Entry(self)
        self.mother_entry.pack()

        tk.Label(self, text="Modelo de Certificado:").pack(pady=(10, 0))
        self.cert_templates = list_templates("assets/certificates")
        self.cert_choice = ttk.Combobox(self, values=self.cert_templates, state="readonly")
        self.cert_choice.pack()

        btn_add_template = tk.Button(self, text="Cadastrar Modelo", command=self.add_template)
        btn_add_template.pack(pady=(5, 10))

        btn_generate = tk.Button(self, text="Cadastrar e Gerar Certificado", command=self.save_and_generate)
        btn_generate.pack()

    def add_template(self):
        file_path = filedialog.askopenfilename(
            title="Selecione um modelo de certificado",
            filetypes=[("Certificado (PNG, PDF)", "*.png *.pdf"), ("Todos os arquivos", "*.*")]
        )
        if not file_path:
            return
        if not file_path.lower().endswith((".png", ".pdf")):
            messagebox.showerror("Erro", "Selecione apenas PNG ou PDF.")
            return

        dest_folder = "assets/certificates"
        os.makedirs(dest_folder, exist_ok=True)
        name = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(dest_folder, name))

        self.cert_choice["values"] = list_templates(dest_folder)
        messagebox.showinfo("Sucesso", "Template cadastrado!")

    def save_and_generate(self):
        name = self.name_entry.get().strip()
        species = self.species_entry.get().strip()
        anilha = self.anilha_entry.get().strip()
        father = self.father_entry.get().strip() or None
        mother = self.mother_entry.get().strip() or None
        template = self.cert_choice.get().strip()

        if not name or not species or not anilha:
            messagebox.showerror("Erro", "Campos obrigatórios.")
            return
        if not template:
            messagebox.showerror("Erro", "Selecione um modelo de certificado.")
            return

        bird = register_bird(name, species, anilha, father=father, mother=mother)
        cert_path = generate_certificate(bird.to_dict(), template)
        tree_path = generate_tree(bird.to_dict(), load_birds())

        messagebox.showinfo("Sucesso", f"Certificado:\n{cert_path}\n\nÁrvore:\n{tree_path}")
        self.refresh_list()

    def setup_list(self):
        self.tree = ttk.Treeview(self, columns=("Nome","Espécie","Anilha","Pai","Mãe"), show="headings")
        for col in ["Nome","Espécie","Anilha","Pai","Mãe"]:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both", pady=15)
        self.refresh_list()

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for b in load_birds():
            self.tree.insert("", "end",
                values=(b["name"], b["species"], b["anilha"], b.get("father"), b.get("mother")))