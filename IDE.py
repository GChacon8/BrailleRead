import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename

class IDE:

    def __init__(self, master):
        self.master = master
        self.master.title("BrailleRead IDE")
        self.master.geometry("1400x800")
        self.create_widgets()

    def create_widgets(self):
        # Crea un menú con tres opciones: Nuevo archivo, Abrir archivo y Guardar archivo.
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        prog_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Program", menu=prog_menu)

        filemenu.add_command(label="New File", command=self.new_file)
        filemenu.add_command(label="Open File", command=self.open_file)
        filemenu.add_command(label="Save File", command=self.save_file)
        
        prog_menu.add_command(label="Compile")
        prog_menu.add_command(label="Run")
        
       
        self.master.config(menu=menubar)

        # Crea un área de texto para editar el código.
        self.coding_area = tk.Text(self.master)
        self.coding_area = tk.Text(root, height=35, width=130)
        self.coding_area.place(x=10,y=10)

        self.error_area = tk.Text(self.master)
        self.error_area = tk.Text(root, height=45, width=40)
        self.error_area.place(x=1070,y=10)
        
        self.console_area = tk.Text(self.master)
        self.console_area = tk.Text(root, height=8, width=130)
        self.console_area.place(x=10,y=600)

    def new_file(self):
        # Elimina el contenido del área de texto y muestra un mensaje.
        self.coding_area.delete("1.0", tk.END)
        messagebox.showinfo("Nuevo archivo", "Se ha creado un nuevo archivo.")

    def open_file(self):
        # Abre un cuadro de diálogo para seleccionar un archivo y muestra su contenido en el área de texto.
        filepath = askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "r") as file:
                self.coding_area.delete("1.0", tk.END)
                self.coding_area.insert(tk.END, file.read())

    def save_file(self):
        # Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo y guarda el contenido del área de texto.
        filepath = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, "w") as file:
                file.write(self.coding_area.get("1.0", tk.END))
            messagebox.showinfo("Guardar archivo", "El archivo se ha guardado correctamente.")

root = tk.Tk()
app = IDE(root)
root.mainloop()
