import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

def download_video(url, output_path, quality):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': quality,
        'noplaylist': True,  
        'retries': 10,
        'fragment-retries': 10,
        'concurrent-fragments': 5
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            messagebox.showinfo("BIEEN", "Tu video se ha descargado")
        except Exception as e:
            messagebox.showerror("Error", f"Tu video no ha podido ser descargado por: {e}")

def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

def start_download():
    url = url_entry.get()
    path = folder_path.get()
    quality = quality_var.get()

    if not url:
        messagebox.showwarning("Advertencia", "Por favor, introduce una URL.")
        return
    if not path:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una carpeta de destino.")
        return

    download_video(url, path, quality)

root = tk.Tk()
root.title("Descargador de Videos")
root.geometry("400x250")

tk.Label(root, text="URL del Video:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)


tk.Label(root, text="Carpeta de destino:").pack(pady=5)
folder_path = tk.StringVar()
tk.Entry(root, textvariable=folder_path, width=40).pack(pady=5, side=tk.LEFT, padx=(20, 5))
tk.Button(root, text="Seleccionar carpeta", command=select_folder).pack(pady=5, side=tk.LEFT)


tk.Label(root, text="Calidad del video:").pack(pady=5)
quality_var = tk.StringVar(value="best")
tk.Radiobutton(root, text="Mejor calidad disponible (video)", variable=quality_var, value="best").pack()
tk.Radiobutton(root, text="Solo audio", variable=quality_var, value="bestaudio").pack()
tk.Radiobutton(root, text="Especificar resolución (ej. 720p, 480p)", variable=quality_var, value="720p").pack()


tk.Button(root, text="Descargar", command=start_download).pack(pady=20)


root.mainloop()
