$('#btn-calcular').click(function () {
    const li = $('#li').val().split(',').map(x => parseFloat(x.trim()));
    const ls = $('#ls').val().split(',').map(x => parseFloat(x.trim()));
    const fi = $('#fi').val().split(',').map(x => parseInt(x.trim()));

    if (li.length !== ls.length || li.length !== fi.length) {
        alert('Todos os campos devem ter o mesmo número de elementos!');
        return;
    }

    // Calcula pontos médios (xi)
    const xi = li.map((valor, i) => (valor + ls[i]) / 2);

    // Envia os dados de fi para o iframe do gráfico
    const iframe = document.getElementById('grafico-frame');
    iframe.contentWindow.postMessage({ tipo: 'atualizarFi', fi: fi }, '*');

    fetch('http://localhost:5000/frequencia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ xi: xi, fi: fi })
    })
    .then(response => response.json())
    .then(data => {
        $('.resultadoclasses').html(`
            <p><strong>Média:</strong> ${data.media}</p>
            <p><strong>Variância:</strong> ${data.variancia}</p>
            <p><strong>Desvio Padrão:</strong> ${data.desvio_padrao}</p>
            <p><strong>Coeficiente de Variação:</strong> ${data.coeficiente_variacao}%</p>
        `);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao processar os dados.');
    });
});
