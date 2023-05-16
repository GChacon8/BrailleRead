import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
#import keyboard

class IDE:

    def __init__(self, master):
        self.master = master
        self.master.title("BrailleRead IDE")
        self.master.geometry("1100x650")
        self.master.resizable(False, False)
        self.master.configure(bg= '#1E1E1E')
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
        self.coding_area = tk.Text(root, height=25, width=129, bg= "#1E1E1E", fg='aqua')
        self.coding_area.place(x=50,y=10)
        self.coding_area.bind('<Key>', self.line_number)
        self.coding_area.bind('<Motion>', self.line_number)
        self.coding_area.bind('<MouseWheel>', self.line_number)

        self.error_area = tk.Text(self.master)
        self.error_area = tk.Text(root, height=10, width=134, bg= "#1E1E1E", fg='light gray', state='disabled')
        self.error_area.place(x=10,y=470)
        
        self.console_area = tk.Text(self.master)
        self.console_area = tk.Text(root, height=10, width=134, bg= "#1E1E1E", fg='light gray', state='disabled')
        self.console_area.place(x=10,y=470)
        
        self.lineno_area = tk.Text(self.master)
        self.lineno_area = tk.Text(root, height=25, width=3, bg= '#1E1E1E', fg='light gray', bd=0)
        self.lineno_area.place(x=10,y=10)
        self.lineno_area.config(state='disabled')

        self.console_button = tk.Button(self.master)
        self.console_button = tk.Button(root, text="Console", command= self.display_console, bg='#1E1E1E', fg='light gray', font= ('Segoe UI', '10', 'bold', 'underline'), bd=0)
        self.console_button.place(x = 15, y = 440)

        self.errors_button = tk.Button(self.master)
        self.errors_button = tk.Button(root, text="Errors", command= self.display_errors, bg='#1E1E1E', fg='light gray', font= ('Segoe UI', '10'), bd=0)
        self.errors_button.place(x = 80, y = 440)

        # Función para deshacer
       #def undo(event):
        #    self.console_area.event_generate('<Control-z>')
        
        #keyboard.on_press_key("ctrl", undo)

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

    def display_console(self):
        self.error_area.place_forget()
        self.console_area.place(x=10,y=470)
        self.console_button.config(font= ('Segoe UI', '10', 'bold', 'underline'))
        self.errors_button.config(font= ('Segoe UI', '10'))
    
    def display_errors(self):
        self.console_area.place_forget()
        self.error_area.place(x=10,y=470)
        self.errors_button.config(font= ('Segoe UI', '10', 'bold', 'underline'))
        self.console_button.config(font= ('Segoe UI', '10'))
    
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
        self.lineno_area.config(state="disable")

root = tk.Tk()
app = IDE(root)
root.mainloop()