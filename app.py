from flask import Flask, request, jsonify
from scipy.stats import norm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()

        media = float(data['media'])
        desvio = float(data['desvio_padrao'])
        x = float(data['valor_x'])

        # Cálculo principal
        z = (x - media) / desvio
        p_menor = norm.cdf(z)
        p_maior = 1 - p_menor

        resposta = {
            'z': round(z, 4),
            'P(x < X)': round(p_menor, 6),
            'P(x > X)': round(p_maior, 6)
        }

        # Se o usuário escolheu outro tipo de visualização de probabilidade
        tipo = data.get('tipo')
        a = data.get('a')
        b = data.get('b')

        if tipo == "igual":
            resposta["P(x = X)"] = 0.0  # Variável contínua, probabilidade exata = 0

        elif tipo == "intervalo" and a is not None and b is not None:
            a = float(a)
            b = float(b)
            z1 = (a - media) / desvio
            z2 = (b - media) / desvio
            prob = norm.cdf(z2) - norm.cdf(z1)
            resposta[f'P({a} < x < {b})'] = round(prob, 6)

        elif tipo == "fora-intervalo" and a is not None and b is not None:
            a = float(a)
            b = float(b)
            z1 = (a - media) / desvio
            z2 = (b - media) / desvio
            prob = norm.cdf(z1) + (1 - norm.cdf(z2))
            resposta[f'P(x < {a} ou x > {b})'] = round(prob, 6)

        return jsonify(resposta)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
