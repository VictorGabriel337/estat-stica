document.querySelector('.btn-enviar').addEventListener('click', async () => {
  try {
    const media = parseFloat(document.getElementById('media').value);
    const desvio = parseFloat(document.getElementById('desvio').value);
    const valorX = parseFloat(document.getElementById('valorX').value);
    const tamanhoAmostra = parseInt(document.getElementById('tamanhoAmostra').value);

    // Novos campos
    const tipo = document.getElementById('tipo').value;
    const valorA = document.getElementById('valorA').value;
    const valorB = document.getElementById('valorB').value;

    const payload = {
      media: media,
      desvio_padrao: desvio,
      valor_x: valorX,
    };

    if (!isNaN(tamanhoAmostra)) {
      payload.tamanho_amostra = tamanhoAmostra;
    }

    // Adiciona se tiver valores extras
    if (tipo) {
      payload.tipo = tipo;
    }

    if (valorA !== "") {
      payload.a = parseFloat(valorA);
    }

    if (valorB !== "") {
      payload.b = parseFloat(valorB);
    }

    const response = await fetch('http://localhost:5000/calcular', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    // Exibe todos os resultados dinamicamente
    let html = "";
    for (let chave in result) {
      html += `<p><strong>${chave}:</strong> ${result[chave]}</p>`;
    }

    document.getElementById("resultado").innerHTML = html;

    // Envia dados para o gráfico, se necessário
    const graficoiframe = document.getElementById("grafico-frame");
    graficoiframe.contentWindow.postMessage({
      type: "atualizarGrafico",
      media: media,
      desvio: desvio,
      valorX: valorX
    }, "*");

    const iframePizza = document.querySelector('.pizza');
    iframePizza.contentWindow.postMessage({
      type: "atualizarPizza",
      pMenor: result["P(x < X)"],
      pMaior: result["P(x > X)"]
    }, "*");

  } catch (error) {
    console.error("Erro:", error);
    document.getElementById("resultado").innerText = "Erro ao calcular.";
  }
});
