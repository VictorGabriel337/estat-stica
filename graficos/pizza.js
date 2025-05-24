const ctx = document.getElementById('pizza');
let chartPizza = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['P(x < X)', 'P(x > X)'],
    datasets: [{
      data: [0.5, 0.5], // valores iniciais (50/50)
      backgroundColor: ['#36A2EB', '#FF6384'],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          boxWidth: 20,
          padding: 15,
          usePointStyle: true
        }
      }
    },
    layout: {
      padding: {
        top: 10,
        bottom: 10
      }
    }
  }
});

// Ouve mensagens vindas do parent (calculo.html)
window.addEventListener('message', (event) => {
  if (event.data.type === 'atualizarPizza') {
    const menor = event.data.pMenor;
    const maior = event.data.pMaior;

    chartPizza.data.datasets[0].data = [menor, maior];
    chartPizza.update();
  }
});
