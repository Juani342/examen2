import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import random

def fetch_records(base_url):
    """Obtiene todos los registros desde la API."""
    try:
        with urllib.request.urlopen(base_url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Error en la solicitud: {e}")
        return []

def setup_treeview(tree):
    """Configura las columnas del Treeview."""
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())

def load_records(tree, records):
    """Carga los registros desde la API y los muestra en el Treeview."""
    clear_treeview(tree)
    if records:
        for record in records:
            insert_record(tree, record)
    else:
        messagebox.showwarning("Advertencia", "No se pudieron cargar los registros.")

def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)

def insert_record(tree, record):
    values = (
        record.get('id', 'N/A'),
        record.get('equipo', 'N/A'),
        record.get('nombre', 'N/A'),
        record.get('nacionalidad', 'N/A'),
        record.get('puntuacion', 'N/A'),
        record.get('accidentes', 'N/A'),
    )
    tree.insert("", "end", values=values)

def search_record(tree, records, search_entry):
    id = search_entry.get()
    found = False
    clear_treeview(tree)

    for record in records:
        if record.get('id', '') == id:
            found = True
            insert_record(tree, record)
            break

    if not found:
        messagebox.showwarning("Advertencia", "Corredor no encontrado.")

def show_random_record(tree, records):
    """Muestra un corredor aleatorio en el Treeview."""
    if records:
        random_record = random.choice(records)
        clear_treeview(tree)
        insert_record(tree, random_record)
    else:
        messagebox.showwarning("Advertencia", "No hay registros disponibles.")

def update_records(api_url, tree, records):
    """Actualiza los registros desde la API."""
    records = fetch_records(api_url)
    load_records(tree, records)
    return records

def main():
    base_url = "https://67203872e7a5792f0530cc8c.mockapi.io/eq"
    records = fetch_records(base_url)

    root = tk.Tk()
    root.title("Historial de Corredores de F1")
    root.geometry("1340x400")
    root.resizable(False, False)

    search_entry = tk.Entry(root)
    search_entry.pack(pady=10)

    search_button = tk.Button(root, text="Buscar Corredor por ID", command=lambda: search_record(tree, records, search_entry))
    search_button.pack(pady=5)

    tree = ttk.Treeview(root, columns=("id", "equipo", "nombre", "nacionalidad", "puntuacion", "accidentes"), show="headings")
    setup_treeview(tree)
    tree.pack(expand=True, fill='both')

    random_button = tk.Button(root, text="Mostrar Corredor Aleatorio", command=lambda: show_random_record(tree, records))
    random_button.pack(pady=10)

    refresh_button = tk.Button(root, text="Actualizar Registros", command=lambda: update_records(base_url, tree, records))
    refresh_button.pack(pady=10)

    load_records(tree, records)

    root.mainloop()


main()
