import tkinter as tk
from tkinter import ttk, messagebox
import random


class RecordViewer(tk.Tk):
    def __init__(self, api):
        super().__init__()
        self.__api = api
        self.__records = self.__api.fetch_records()
        self.__init_ui()
        self.__load_records()

    def __init_ui(self):
        self.title("Historial de Corredores de F1")
        self.geometry("1340x400")
        self.resizable(False, False)

        # Campo de entrada para buscar por ID
        self.__search_entry = tk.Entry(self)
        self.__search_entry.pack(pady=10)

        self.__search_button = tk.Button(self, text="Buscar Corredor por ID", command=self.__search_record)
        self.__search_button.pack(pady=5)

        self.__tree = ttk.Treeview(self,
                                   columns=("id", "equipo", "nombre", "nacionalidad", "puntuacion", "accidentes"),
                                   show="headings")
        self.__setup_treeview()
        self.__tree.pack(expand=True, fill='both')

        self.__random_button = tk.Button(self, text="Mostrar Corredor Aleatorio", command=self.__show_random_record)
        self.__random_button.pack(pady=10)

        self.__refresh_button = tk.Button(self, text="Actualizar Registros", command=self.__update_records)
        self.__refresh_button.pack(pady=10)

    def __setup_treeview(self):
        for col in self.__tree["columns"]:
            self.__tree.heading(col, text=col.capitalize())

    def __load_records(self):
        self.__clear_treeview()
        if self.__records:
            for record in self.__records:
                self.__insert_record(record)
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los registros.")

    def __clear_treeview(self):
        for item in self.__tree.get_children():
            self.__tree.delete(item)

    def __insert_record(self, record):
        values = (
            record.get('id', 'N/A'),
            record.get('equipo', 'N/A'),
            record.get('nombre', 'N/A'),
            record.get('nacionalidad', 'N/A'),
            record.get('puntuacion', 'N/A'),
            record.get('accidentes', 'N/A'),
        )
        self.__tree.insert("", "end", values=values)

    def __search_record(self):
        id = self.__search_entry.get()
        found = False
        self.__clear_treeview()

        for record in self.__records:
            if record.get('id', '') == id:
                found = True
                self.__insert_record(record)
                break

        if not found:
            messagebox.showwarning("Advertencia", "Corredor no encontrado.")

    def __show_random_record(self):
        if self.__records:
            random_record = random.choice(self.__records)
            self.__clear_treeview()
            self.__insert_record(random_record)
        else:
            messagebox.showwarning("Advertencia", "No hay registros disponibles.")

    def __update_records(self):
        self.__records = self.__api.fetch_records()
        self.__load_records()