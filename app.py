from flask import Flask, request, jsonify
from scipy.stats import norm
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# ======================= DISTRIBUIÇÃO NORMAL =======================
@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        data = request.get_json()

        media = float(data['media'])
        desvio = float(data['desvio_padrao'])
        x = float(data['valor_x'])

        tamanho_amostra = data.get('tamanho_amostra')
        erro_padrao = desvio  # default: cálculo populacional

        if tamanho_amostra:
            tamanho_amostra = int(tamanho_amostra)
            erro_padrao = desvio / math.sqrt(tamanho_amostra)
            print(f"Usando cálculo amostral com n = {tamanho_amostra}")

        # Cálculo do z-score
        z = (x - media) / erro_padrao
        p_menor = norm.cdf(z)
        p_maior = 1 - p_menor

        resposta = {
            # 'tipo_calculo': 'amostral' if tamanho_amostra else 'populacional',
            'z': round(z, 4),
            # 'erro_padrao': round(erro_padrao, 4),
            'P(x < X)' if not tamanho_amostra else 'P(x̄ < X)': round(p_menor, 6),
            'P(x > X)' if not tamanho_amostra else 'P(x̄ > X)': round(p_maior, 6)
        }

        tipo = data.get('tipo')
        a = data.get('a')
        b = data.get('b')

        if tipo == "igual":
            resposta["P(x = X)" if not tamanho_amostra else "P(x̄ = X)"] = 0.0

        elif tipo == "intervalo" and a is not None and b is not None:
            a = float(a)
            b = float(b)
            z1 = (a - media) / erro_padrao
            z2 = (b - media) / erro_padrao
            prob = norm.cdf(z2) - norm.cdf(z1)
            resposta[f'P({a} < x < {b})' if not tamanho_amostra else f'P({a} < x̄ < {b})'] = round(prob, 6)

        elif tipo == "fora-intervalo" and a is not None and b is not None:
            a = float(a)
            b = float(b)
            z1 = (a - media) / erro_padrao
            z2 = (b - media) / erro_padrao
            prob = norm.cdf(z1) + (1 - norm.cdf(z2))
            resposta[f'P(x < {a} ou x > {b})' if not tamanho_amostra else f'P(x̄ < {a} ou x̄ > {b})'] = round(prob, 6)

        return jsonify(resposta)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ======================= DISTRIBUIÇÃO DE FREQUÊNCIA =======================

def calcular_estatisticas_frequencia(xi, fi):
    if len(xi) != len(fi):
        raise ValueError("Xi e Fi devem ter o mesmo tamanho.")

    total_fi = sum(fi)
    media = sum(x * f for x, f in zip(xi, fi)) / total_fi

    variancia = sum(f * ((x - media) ** 2) for x, f in zip(xi, fi)) / total_fi
    desvio_padrao = variancia ** 0.5
    coeficiente_variacao = (desvio_padrao / media) * 100 if media != 0 else 0

    return {
        "media": round(media, 2),
        "variancia": round(variancia, 2),
        "desvio_padrao": round(desvio_padrao, 2),
        "coeficiente_variacao": round(coeficiente_variacao, 2)
    }


@app.route('/frequencia', methods=['POST'])
def frequencia():
    try:
        data = request.get_json()

        xi = data.get('xi')
        fi = data.get('fi')

        # Validar e converter os dados
        xi = [float(x) for x in xi]
        fi = [int(f) for f in fi]

        resultado = calcular_estatisticas_frequencia(xi, fi)
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    






# ======================= AGRUPAMENTO EM CLASSES =======================

def calcular_classes(amostra, numero_classes=None):
    n = len(amostra)
    minimo = min(amostra)
    maximo = max(amostra)
    amplitude_total = maximo - minimo

    if numero_classes is None:
        numero_classes = round(1 + 3.3 * math.log10(n))  # Regra de Sturges

    numero_classes = int(numero_classes)
    amplitude_classe = math.ceil(amplitude_total / numero_classes)

    classes = []
    inicio = minimo

    frequencias = []
    pontos_medios = []

    for _ in range(numero_classes):
        fim = inicio + amplitude_classe
        frequencia = sum(1 for x in amostra if inicio <= x < fim)
        classes.append({
            "intervalo": f"{round(inicio, 2)} - {round(fim, 2)}",
            "frequencia": frequencia
        })
        frequencias.append(frequencia)
        pontos_medios.append((inicio + fim) / 2)
        inicio = fim

    total_freq = sum(frequencias)
    if total_freq == 0:
        # Evitar divisão por zero
        media = variancia = desvio_padrao = coeficiente_variacao = 0
    else:
        media = sum(pm * f for pm, f in zip(pontos_medios, frequencias)) / total_freq
        variancia = sum(f * (pm - media) ** 2 for pm, f in zip(pontos_medios, frequencias)) / total_freq
        desvio_padrao = variancia ** 0.5
        coeficiente_variacao = (desvio_padrao / media) * 100 if media != 0 else 0

    return {
        "numero_classes": numero_classes,
        "amplitude_classe": amplitude_classe,
        "classes": classes,
        "media": round(media, 2),
        "variancia": round(variancia, 2),
        "desvio_padrao": round(desvio_padrao, 2),
        "coeficiente_variacao": round(coeficiente_variacao, 2)
    }


# ======================= RODAR SERVIDOR =======================
if __name__ == '__main__':
    app.run(debug=True)
