from flask import Flask, render_template, request, jsonify
from scipy.stats import norm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('calculo.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()
        media = float(data['media'])
        desvio = float(data['desvio_padrao'])
        x = float(data['valor_x'])

        # Cálculo do Z
        z = (x - media) / desvio
        p_menor = norm.cdf(z)
        p_maior = 1 - p_menor

        return jsonify({
            'z': round(z, 4),
            'P(x < X)': round(p_menor, 4),
            'P(x > X)': round(p_maior, 4)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
