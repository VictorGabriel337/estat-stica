const ctx = document.getElementById('radar');

new Chart(ctx, {
  type: 'radar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: 'Amostra dos dados',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 2,
      borderColor: 'rgba(54, 162, 235, 1)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      pointBackgroundColor: 'white'
    }]
  },
  options: {
    scales: {
      r: {
        grid: {
          color: 'white', // Cor da grade
          lineWidth: 1.5             // Espessura da linha
        },
        angleLines: {
          color: 'white', // Linhas em direção aos labels
          lineWidth: 1.5
        },
        ticks: {
          beginAtZero: true,
          backdropColor: 'transparent',
          color: '#000'
        },
        pointLabels: {
          color: 'white', // Cor dos nomes dos pontos
          font: {
            size: 14
          }
        }
      }
    }
  }
});
