from examen2 import  RecordViewer(tk.Tk)

def main():
    """Función principal para iniciar la aplicación."""
    url = "https://67203872e7a5792f0530cc8c.mockapi.io/:endpoint"
    api = API(url)
    app = RecordViewer(api)
    app.mainloop()

if __name__ == "__main__":
    main()
