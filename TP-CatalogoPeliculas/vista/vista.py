import tkinter as tk
from tkinter import ttk, messagebox
import modelo.consultas_dao as consulta

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.id_peli = None
        self.fondo = "#FBFCDD"
        self.config(bg=self.fondo)

        self.nombre = tk.StringVar()
        self.duracion = tk.StringVar()
        self.director = tk.StringVar()
        self.anio_lanzamiento = tk.StringVar()

        self.generos_map = {}
        self.generos_nombres = []
        self.cargar_generos_combobox()

        self.label_form()
        self.input_form()
        self.botones_principales()
        self.crear_tabla_estructura()
        self.actualizar_tabla()

    def label_form(self):
        labels_info = [
            ("Nombre: ", 0),
            ("Duración: ", 1),
            ("Genero: ", 2),
            ("Director: ", 3),
            ("Año lanzamiento: ", 4)
        ]
        for text, row_num in labels_info:
            label = tk.Label(self, text=text)
            label.config(font=('Arial', 12, 'bold'), bg=self.fondo, fg="#1931E8")
            label.grid(row=row_num, column=0, padx=10, pady=10)

    def cargar_generos_combobox(self):
        generos_db = consulta.listar_generos()
        self.generos_map = {nombre: id for id, nombre in generos_db}
        self.generos_nombres = ['Seleccione Uno'] + [nombre for id, nombre in generos_db]

    def input_form(self):
        self.entry_nombre = tk.Entry(self, textvariable=self.nombre)
        self.entry_nombre.config(width=50, state='disabled')
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.entry_duracion = tk.Entry(self, textvariable=self.duracion)
        self.entry_duracion.config(width=50, state='disabled')
        self.entry_duracion.grid(row=1, column=1, padx=10, pady=10)

        self.entry_director = tk.Entry(self, textvariable=self.director)
        self.entry_director.config(width=50, state='disabled')
        self.entry_director.grid(row=3, column=1, padx=10, pady=10)

        self.entry_anio_lanzamiento = tk.Entry(self, textvariable=self.anio_lanzamiento)
        self.entry_anio_lanzamiento.config(width=50, state='disabled')
        self.entry_anio_lanzamiento.grid(row=4, column=1, padx=10, pady=10)


        self.entry_genero = ttk.Combobox(self, state="readonly", values=self.generos_nombres, width=25)
        self.entry_genero.current(0)
        self.entry_genero.config(state='disabled')
        self.entry_genero.grid(row=2, column=1, padx=10, pady=10)

    def botones_principales(self):
        self.btn_alta = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.btn_alta.config(width=20, font=('Arial', 12, 'bold'),fg ='#FFFFFF' , bg='#1C500B',cursor='hand2',activebackground='#3FD83F', activeforeground='#000000')
        self.btn_alta.grid(row=5, column=0, padx=10, pady=10)

        self.btn_modi = tk.Button(self, text='Guardar', command=self.guardar_campos)
        self.btn_modi.config(width=20, font=('Arial', 12, 'bold'), fg ='#FFFFFF' ,bg='#0D2A83',cursor='hand2',activebackground='#7594F5', activeforeground='#000000', state='disabled')
        self.btn_modi.grid(row=5, column=1, padx=10, pady=10)

        self.btn_cance = tk.Button(self, text='Cancelar', command=self.bloquear_campos)
        self.btn_cance.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2', activebackground='#F35B5B', activeforeground='#000000', state='disabled')
        self.btn_cance.grid(row=5, column=2, padx=10, pady=10)

    def crear_tabla_estructura(self):
        
        self.tabla = ttk.Treeview(self, columns=('Nombre', 'Duracion', 'Genero', 'Director', 'Año Lanzamiento'))
        self.tabla.grid(row=6, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=6, column=3, sticky='nse', pady=10)
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Nombre')
        self.tabla.heading('#2', text='Duracion')
        self.tabla.heading('#3', text='Genero')
        self.tabla.heading('#4', text='Director')
        self.tabla.heading('#5', text='Año Lanzamiento')

        self.btn_editar = tk.Button(self, text='Editar', command=self.editar_registro)
        self.btn_editar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg="#1C500B", cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_editar.grid(row=7, column=0, padx=10, pady=10)

        self.btn_delete = tk.Button(self, text='Delete', command=self.eliminar_regristro)
        self.btn_delete.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2', activebackground='#F35B5B', activeforeground='#000000')
        self.btn_delete.grid(row=7, column=1, padx=10, pady=10)

    def actualizar_tabla(self):
        
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        self.lista_p = consulta.listar_peli()
        self.lista_p.reverse()

        for p in self.lista_p:
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5]))

    def editar_registro(self):
        try:
            if not self.tabla.selection():
                return

            self.id_peli = self.tabla.item(self.tabla.selection())['text']
            values = self.tabla.item(self.tabla.selection())['values']

            self.habilitar_campos()
            self.nombre.set(values[0])
            self.duracion.set(values[1])
            self.entry_genero.set(values[2])
            self.director.set(values[3])
            self.anio_lanzamiento.set(values[4])

        except Exception:
            pass

    def eliminar_regristro(self):
        try:
            if not self.tabla.selection():
                return

            self.id_peli = self.tabla.item(self.tabla.selection())['text']
            if self.id_peli:
                response = messagebox.askyesno("Confirmar", "¿Desea borrar el registro?")

                if response:
                    consulta.borrar_peli(int(self.id_peli))
                    messagebox.showinfo("Eliminado", "El registro se ha eliminado correctamente.")
                else:
                    messagebox.showinfo("Cancelado", "La eliminación ha sido cancelada.")

                self.id_peli = None
                self.actualizar_tabla()
        except IndexError:
            pass
        except Exception:
            pass

    def guardar_campos(self):
        nombre_genero_seleccionado = self.entry_genero.get()
        genero_id = self.generos_map.get(nombre_genero_seleccionado)

        if genero_id is None or nombre_genero_seleccionado == 'Seleccione Uno':
            return

        nombre_director = self.director.get()
        director_id = consulta.obtener_o_crear_director(nombre_director)

        if director_id is None:
            return

        try:
            anio_lanzamiento_val = int(self.anio_lanzamiento.get())
        except ValueError:
            return

        pelicula = consulta.Peliculas(
            self.nombre.get(),
            self.duracion.get(),
            genero_id,
            director_id,
            anio_lanzamiento_val
        )

        if self.id_peli is None:
            consulta.guardar_peli(pelicula)
        else:
            consulta.editar_peli(pelicula, int(self.id_peli))

        self.actualizar_tabla()
        self.bloquear_campos()

    def habilitar_campos(self):
        self.entry_nombre.config(state='normal')
        self.entry_duracion.config(state='normal')
        self.entry_genero.config(state='normal')
        self.entry_director.config(state='normal')
        self.entry_anio_lanzamiento.config(state='normal')
        self.btn_modi.config(state='normal')
        self.btn_cance.config(state='normal')
        self.btn_alta.config(state='disabled')

    def bloquear_campos(self):
        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')
        self.entry_genero.config(state='disabled')
        self.entry_director.config(state='disabled')
        self.entry_anio_lanzamiento.config(state='disabled')
        self.btn_modi.config(state='disabled')
        self.btn_cance.config(state='disabled')
        self.btn_alta.config(state='normal')
        self.nombre.set('')
        self.duracion.set('')
        self.entry_genero.current(0)
        self.director.set('')
        self.anio_lanzamiento.set('')
        self.id_peli = None