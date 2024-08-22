from flask import Flask, request , jsonify
from flask_cors import CORS
import base64
from src.recortar import principal


import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
cors = CORS(app, resources={r"/subir-imagenes": {"origins": "*"}})


@app.route('/subir-imagenes', methods=['POST'])
def subir_imagenes():
    try:
        # Obtener todas las imágenes del formulario
        images = []
        for i in range(6):
            data = request.form.get('images' + str(i+1))
            if data:
                data_parts = data.split(',')
                base64_data = data_parts[1]

                # Decodificar la imagen base64
                image_data = base64.b64decode(base64_data)
                # Guardar la imagen en el servidor o realizar cualquier otro procesamiento necesario
                filename = os.path.join('img', f'images' + str(i+1)+ '.jpg')
                with open(filename, 'wb') as f:
                    f.write(image_data)
                    # images.append(filename)
        

        return jsonify(principal()), 200
    except Exception as e:
        return 'Error en el servidor , al subir las imagenes', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    app.run(debug=True)

