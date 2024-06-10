from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from PIL import Image
import base64

SIZE = 32

app = Flask(__name__)

# Carregue o modelo
model = load_model('cifarmodel.h5')

# Dicionário de mapeamento de classes CIFAR-10 em português
cifar10_classes = {
    0: 'avião',
    1: 'automóvel',
    2: 'pássaro',
    3: 'gato',
    4: 'veado',
    5: 'cachorro',
    6: 'sapo',
    7: 'cavalo',
    8: 'navio',
    9: 'caminhão'
}

# Pré processar a imagem para servir de entrada no modelo
def prepare_image(img):
    img = img.resize((SIZE, SIZE))  # Defina o tamanho desejado
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalização se necessário
    return img

@app.route('/predict', methods=['POST'])
def predict():
    # Verificação para encontrar arquivo, ou se é um arquivo válido
    if 'file' not in request.files:
        return jsonify({'error': 'Arquivo não encontrado'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo foi selecionado'})
    if file:
        # Leitura da imagem
        img = Image.open(io.BytesIO(file.read()))
        # Preparando imagem para predição
        prepared_img = prepare_image(img)
        # Realizar predição
        preds = model.predict(prepared_img)
        result = np.argmax(preds, axis=1)[0]
        # Converte o resultado no nome da classe
        class_name = cifar10_classes[result]

        return jsonify({'Classificação': class_name})

if __name__ == '__main__':
    app.run(debug=True)
