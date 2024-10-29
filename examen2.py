import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import random

class API:
    """Clase para interactuar con la API y obtener registros."""
    def __init__(self, base_url):
        self.__base_url = base_url

    def fetch_records(self):
        """Obtiene todos los registros desde la API."""
        try:
            with urllib.request.urlopen(self.__base_url) as response:
                data = response.read().decode('utf-8')  # Decodificar los datos
                return json.loads(data)  # Procesar datos como JSON
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"Error en la solicitud: {e}")  # Imprime el error en la consola
            return []

class RecordViewer(tk.Tk):
    """Clase principal de la aplicación que muestra los registros."""
    def __init__(self, api):
        super().__init__()
        self.__api = api
        self.__records = self.__api.fetch_records()  # Carga los registros una vez
        self.__init_ui()
        self.__load_records()

    def __init_ui(self):
        """Inicializa la interfaz gráfica."""
        self.title("Historial de Corredores de F1")
        self.geometry("800x400")
        self.resizable(False, False)

        self.__tree = ttk.Treeview(self, columns=("equipo", "nacimiento", "nombre", "nacionalidad", "edad", "dorsal"), show="headings")
        self.__setup_treeview()
        self.__tree.pack(expand=True, fill='both')  # Agregar el Treeview a la ventana

        # Botón para buscar un corredor por nombre
        self.__search_button = tk.Button(self, text="Buscar Corredor", command=self.__input_search)
        self.__search_button.pack(pady=10)

        # Botón para mostrar un corredor aleatorio
        self.__random_button = tk.Button(self, text="Mostrar Corredor Aleatorio", command=self.__show_random_record)
        self.__random_button.pack(pady=10)

    def __setup_treeview(self):
        """Configura las columnas del Treeview."""
        for col in self.__tree["columns"]:
            self.__tree.heading(col, text=col.capitalize())

    def __load_records(self):
        """Carga los registros desde la API y los muestra en el Treeview."""
        self.__clear_treeview()

        if self.__records:
            for record in self.__records:
                self.__insert_record(record)
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los registros.")

    def __clear_treeview(self):
        """Limpia el Treeview de registros anteriores."""
        for item in self.__tree.get_children():
            self.__tree.delete(item)

    def __insert_record(self, record):
        """Inserta un registro en el Treeview."""
        values = (
            record.get('equipo', 'N/A'),
            record.get('nacimiento', 'N/A'),
            record.get('nombre', 'N/A'),
            record.get('nacionalidad', 'N/A'),
            record.get('edad', 'N/A'),
            record.get('dorsal', 'N/A')
        )
        self.__tree.insert("", "end", values=values)

    def __input_search(self):
        """Abre una ventana para buscar un corredor por nombre."""
        search_window = tk.Toplevel(self)
        search_window.title("Buscar Corredor")
        search_window.geometry("300x100")

        tk.Label(search_window, text="Ingresa el nombre del corredor:").pack(pady=10)
        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        tk.Button(search_window, text="Buscar", command=lambda: self.__search_record(entry.get(), search_window)).pack(pady=10)

    def __search_record(self, name, search_window):
        """Busca un corredor por nombre y lo muestra en un mensaje."""
        found = False

        for record in self.__records:
            if record.get('nombre', '').lower() == name.lower():
                found = True
                messagebox.showinfo("Detalles del Corredor",
                                    f"Equipo: {record.get('equipo', 'N/A')}\n"
                                    f"Nacimiento: {record.get('nacimiento', 'N/A')}\n"
                                    f"Nombre: {record.get('nombre', 'N/A')}\n"
                                    f"Nacionalidad: {record.get('nacionalidad', 'N/A')}\n"
                                    f"Edad: {record.get('edad', 'N/A')}\n"
                                    f"Dorsal: {record.get('dorsal', 'N/A')}")
                break

        if not found:
            messagebox.showwarning("Advertencia", "Corredor no encontrado.")

        search_window.destroy()

    def __show_random_record(self):
        """Muestra un corredor aleatorio en un mensaje."""
        if self.__records:
            random_record = random.choice(self.__records)
            messagebox.showinfo("Corredor Aleatorio",
                                f"Equipo: {random_record.get('equipo', 'N/A')}\n"
                                f"Nacimiento: {random_record.get('nacimiento', 'N/A')}\n"
                                f"Nombre: {random_record.get('nombre', 'N/A')}\n"
                                f"Nacionalidad: {random_record.get('nacionalidad', 'N/A')}\n"
                                f"Edad: {random_record.get('edad', 'N/A')}\n"
                                f"Dorsal: {random_record.get('dorsal', 'N/A')}")
        else:
            messagebox.showwarning("Advertencia", "No hay registros disponibles.")