from Compiler import *
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import sys
sys.path.append("..")


class IDE(object):
    def __init__(self, master):
        self.master = master
        self.master.title("BrailleRead IDE")
        self.master.geometry("1100x650")
        self.master.resizable(False, False)
        self.master.configure(bg='#1E1E1E')
        self.saved = False
        self.filepath = ""
        self.create_widgets()

    def create_widgets(self):
        # Crea un menú con tres opciones: Nuevo archivo, Abrir archivo y Guardar archivo.
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        prog_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Program", menu=prog_menu)

        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open File", command=self.open_file)
        filemenu.add_command(label="Save As", command=self.save_file_as)
        filemenu.add_command(label="Save", command=self.save_file)
        
        prog_menu.add_command(label="Compile", command=self.compile_program)
        prog_menu.add_command(label="Run", command=self.run_program)
        
        self.master.config(menu=menubar)

        # Crea un área de texto para editar el código.
        self.coding_area = tk.Text(self.master)
        self.coding_area = tk.Text(root, height=21, width=129, bg= "#1E1E1E", fg='aqua')
        self.coding_area.place(x=50,y=10)
        self.coding_area.bind('<Key>', self.line_number)
        self.coding_area.bind('<Key>', self.changes_made)
        self.coding_area.bind('<Motion>', self.line_number)
        self.coding_area.bind('<MouseWheel>', self.line_number)
        self.coding_area.bind('<Tab>', self.insert_spaces)
        self.coding_area.bind('<Return>', self.handle_enter)
        self.coding_area.config(insertbackground='white')

        self.error_area = tk.Text(self.master)
        self.error_area = tk.Text(root, height=10, width=134, bg= "#1E1E1E", fg='light gray', state='disabled')
        self.error_area.place(x=10,y=470)
        
        self.output_area = tk.Text(self.master)
        self.output_area = tk.Text(root, height=10, width=134, bg= "#1E1E1E", fg='light gray', state='disabled')
        self.output_area.place(x=10,y=470)
        
        self.lineno_area = tk.Text(self.master)
        self.lineno_area = tk.Text(root, height=25, width=3, bg= '#1E1E1E', fg='light gray', bd=0)
        self.lineno_area.place(x=10,y=10)
        self.lineno_area.config(state='disabled')

        self.output = tk.Label(self.master)
        self.output = tk.Label(root, text= "Output", font= ('Segoe UI', '10', 'bold'), bg= '#1E1E1E', fg='light gray')
        self.output.place(x=10,y=440)


        # Habilitar la funcionalidad de deshacer y rehacer
        self.coding_area.configure(undo=True)

        def undo(event):
            self.coding_area.event_generate('<<Undo>>')

        self.coding_area.bind('<Control-z>', undo)

        self.coding_area.bind('<Control-y>', self.redo)

    def run_program(self):
        if self.filepath != "" and self.saved:
            with open(self.filepath, "r") as file:
                result = run_code(file.read())
            if isinstance(result, list):
                self.output_area.configure(state='normal')
                self.output_area.delete("1.0", tk.END)
                for ele in result:
                    self.output_area.insert(tk.END, ele + "\n")
                self.output_area.configure(state='disabled')
        elif self.filepath != "" and self.saved == False:
            request = tk.messagebox.askyesno("Save?", "Do you want to save your last changes before running?")
            if request:
                self.save_file()
                with open(self.filepath, "r") as file:
                    result = run_code(file.read())
                if isinstance(result, list):
                    self.output_area.configure(state='normal')
                    self.output_area.delete("1.0", tk.END)
                    for ele in result:
                        self.output_area.insert(tk.END, ele + "\n")
                    self.output_area.configure(state='disabled')
        else:
            tk.messagebox.showwarning("Warning", "You must save your changes before running the program")
            self.save_file_as()

    def compile_program(self):
        if self.filepath != "" and self.saved:
            with open(self.filepath, "r") as file:
                result = compile_code(file.read())
            if isinstance(result, list):
                self.output_area.configure(state='normal')
                self.output_area.delete("1.0", tk.END)
                for ele in result:
                    self.output_area.insert(tk.END, ele + "\n")
                self.output_area.configure(state='disabled')
        elif self.filepath != "" and self.saved == False:
            request = tk.messagebox.askyesno("Save?", "Do you want to save your last changes before compiling?")
            if request:
                self.save_file()
                with open(self.filepath, "r") as file:
                    result = compile_code(file.read())
                if isinstance(result, list):
                    self.output_area.configure(state='normal')
                    self.output_area.delete("1.0", tk.END)
                    for ele in result:
                        self.output_area.insert(tk.END, ele + "\n")
                    self.output_area.configure(state='disabled')
        else:
            tk.messagebox.showwarning("Warning", "You must save your changes before running the program")
            self.save_file_as()


    def redo(self, event=None):
        # Rehacer la última acción deshecha
        try:
            self.coding_area.edit_redo()
        except:
            pass

    def new_file(self):
        # Elimina el contenido del área de texto y muestra un mensaje.
        self.coding_area.delete("1.0", tk.END)
        messagebox.showinfo("Nuevo archivo", "Se ha creado un nuevo archivo.")
        self.filepath = ""
        self.saved = False

    def open_file(self):
        # Abre un cuadro de diálogo para seleccionar un archivo y muestra su contenido en el área de texto.
        self.filepath = askopenfilename(defaultextension=".br", filetypes=[("Text Files", "*.br"), ("All Files", "*.*")])
        if self.filepath:
            with open(self.filepath, "r") as file:
                self.coding_area.delete("1.0", tk.END)
                self.coding_area.insert(tk.END, file.read())
        self.saved = True

    def save_file_as(self):
        # Abre un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo y guarda el contenido del área de texto.
        self.filepath = asksaveasfilename(defaultextension=".br", filetypes=[("Text Files", "*.br"), ("All Files", "*.*")])
        print(self.filepath)
        if self.filepath:
            with open(self.filepath, "w") as file:
                file.write(self.coding_area.get("1.0", tk.END))
            messagebox.showinfo("Save File", "File has been saved correctly.")

        self.saved = True

    def save_file(self):
        print(self.filepath)
        if self.filepath:
            with open(self.filepath, "w") as file:
                file.write(self.coding_area.get("1.0", tk.END))
            messagebox.showinfo("Save File", "File has been saved correctly.")
        else:
            self.save_file_as()

        self.saved = True

    def line_number(self, event):
        last_line = self.coding_area.index(tk.END)
        first_line = self.coding_area.index('@0,0')
        last_line_int = int(last_line.split('.')[0])-1
        first_line_int = int(first_line.split('.')[0])-1
        self.lineno_area.config(state="normal")
        self.lineno_area.delete("1.0", tk.END)
        for i in range(first_line_int, last_line_int):
            self.lineno_area.insert(tk.END, i+1)
            self.lineno_area.insert(tk.END, "\n")
        self.lineno_area.config(state="disabled")

    def changes_made(self, event):
        self.saved = False

    def insert_spaces(self, event):
        self.coding_area.insert(tk.INSERT, " " * 4)
        return 'break'

    def handle_enter(self, event):
        current_line = self.coding_area.get("insert linestart", "insert")
        indentation = ""

        # Obtener la indentación de la línea actual
        for char in current_line:
            if char == " " or char == "\t":
                indentation += char
            else:
                break

        # Insertar una nueva línea con la indentación
        self.coding_area.insert(tk.INSERT, "\n" + indentation)
        return "break"

root = tk.Tk()
app = IDE(root)
root.mainloop()
