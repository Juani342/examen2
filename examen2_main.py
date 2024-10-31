from examen2_api import API
from examen2_recordviewer import RecordViewer

if __name__ == "__main__":
    base_url = "https://67203872e7a5792f0530cc8c.mockapi.io/eq"
    api = API(base_url)
    app = RecordViewer(api)
    app.mainloop()
