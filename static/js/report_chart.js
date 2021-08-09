const testChart = {
    type: 'line',
    data: {
        labels: json_data.x,
        datasets: [{
            label: '# of Votes',
            data: json_data,

            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(54, 162, 235, 1)'
            ],
            borderWidth: 3
        }]
    },
    options: {
        parsing: {
            xAxisKey: 'x',
            yAxisKey: 'y'
        },
        plugins: {
   tooltips: {
       callbacks: {
           title: function (tooltipItem, data) {
               return data['y'][tooltipItem[0]['index']];
           },
       }
   },

            legend: {

                display: false,
                labels: {
                    color: 'rgb(255, 99, 132)',

                }
            }
        },
        scales: {

            y: {
                display: true,
                title: {
                    display: true,
                    text: '₴'
                },
                beginAtZero: true
            }
        }
    }
}







