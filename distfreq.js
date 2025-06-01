$(document).ready(function () {
    $('#btn-calcular').click(function () {
        const xiStr = $('#input-xi').val();
        const fiStr = $('#input-fi').val();
        const resultadoDiv = $('#resultado');

        resultadoDiv.html(''); // Limpa o resultado anterior

        if (!xiStr || !fiStr) {
            resultadoDiv.html('Por favor, preencha ambos os campos.');
            return;
        }

        // Converte os valores para arrays numéricos
        const xi = xiStr.split(',').map(x => parseFloat(x.trim()));
        const fi = fiStr.split(',').map(f => parseInt(f.trim()));

        if (xi.length !== fi.length) {
            resultadoDiv.html('Os arrays Xi e Fi devem ter o mesmo tamanho.');
            return;
        }
            // Envia os dados de fi para o iframe do gráfico
    const iframe = document.getElementById('grafico-frame');
    iframe.contentWindow.postMessage({ tipo: 'atualizarFi', fi: fi }, '*');

    
        // Envia para o backend
        $.ajax({
            url: 'http://localhost:5000/frequencia',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ xi, fi }),
            success: function (data) {
                if (data.error) {
                    resultadoDiv.html(`Erro: ${data.error}`);
                    return;
                }

                // Exibe os resultados
                resultadoDiv.html(`
                    <p><strong>Média:</strong> ${data.media}</p>
                    <p><strong>Variância:</strong> ${data.variancia}</p>
                    <p><strong>Desvio Padrão:</strong> ${data.desvio_padrao}</p>
                    <p><strong>Coeficiente de Variação (%):</strong> ${data.coeficiente_variacao}</p>
                `);
                // Preenche os inputs da distribuição normal, se existirem na mesma página
                if ($('#input-media').length && $('#input-desvio').length) {
                    $('#input-media').val(data.media.toFixed(4));
                    $('#input-desvio').val(data.desvio_padrao.toFixed(4));
                }


            },
            error: function (xhr, status, error) {
                resultadoDiv.html('Erro ao comunicar com o servidor.');
                console.error(error);
            }
        });
    });
});