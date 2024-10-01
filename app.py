from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import json

# Archivo de configuración para almacenar la carpeta de descarga
CONFIG_FILE = "config.json"

app = Flask(__name__)

# Función para guardar la carpeta de descarga en un archivo de configuración
def save_download_folder(folder):
    config = {'download_folder': folder}
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file)

# Función para cargar la carpeta de descarga del archivo de configuración
def load_download_folder():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
            return config.get('download_folder', '')
    return ''

# Función para descargar videos usando yt-dlp
def download_video(url, output_path, quality, filename):
    ydl_opts = {
        'outtmpl': os.path.join(output_path, f'{filename}.%(ext)s'),  # Usar el nombre proporcionado por el usuario
        'format': quality,  # Usar la calidad seleccionada
        'noplaylist': True,
        'retries': 10,
        'fragment-retries': 10,
        'concurrent-fragments': 5,
        # Elimina el postprocesador que utiliza ffmpeg
        # No incluir la opción 'merge_output_format'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Función para obtener las calidades del video
def get_video_formats(url):
    ydl_opts = {'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        
        # Filtrar solo los formatos de video (eliminar solo audio)
        video_formats = [
            {"format_id": f['format_id'], "resolution": f.get('resolution', 'unknown')}
            for f in formats if f.get('vcodec') != 'none'
        ]
        return video_formats
        

# Función para obtener el título del video
def get_video_title(url):
    ydl_opts = {'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('title', 'Video')
    
@app.route('/')
def index():
    default_folder = load_download_folder()
    return render_template('index.html', default_folder=default_folder)

@app.route('/get_video_title', methods=['POST'])
def get_video_title_route():
    data = request.get_json()
    url = data.get('url')

    try:
        title = get_video_title(url)
        return jsonify({'status': 'success', 'title': title})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    quality = data['quality']
    filename = data['filename']  # Nombre del archivo proporcionado por el usuario
    folder = data['folder']  # Carpeta seleccionada por el usuario en el frontend
    output_path = folder if folder else "downloads"  # Usar la carpeta seleccionada o default "downloads"
    
    try:
        download_video(url, output_path, quality, filename)
        return jsonify({'status': 'success', 'message': 'Descarga completada'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_formats', methods=['POST'])
def get_formats():
    data = request.get_json()
    url = data['url']
    
    try:
        formats = get_video_formats(url)
        return jsonify({'status': 'success', 'formats': formats})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
