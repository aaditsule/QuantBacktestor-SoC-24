var labels = data.labels;
var stock_cummulative_retuns = data.stock_cummulative_return;
var nifty_cummulative_returns = data.nifty_cummulative_return;

var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',  // Specify the chart type
        data: {
            labels: labels,  // X-axis labels (datetime)
            datasets: [{
                label: 'Stock Cumulative Returns',  // Dataset label
                data: stock_cummulative_retuns,  // Data points for the chart (cumulative returns)
                borderColor: 'blue',  // Line color
                backgroundColor: 'transparent'  // No fill color
            }
            , {
                label: 'Nifty Cumulative Returns',  // Dataset label
                data: nifty_cummulative_returns,  // Data points for the chart (cumulative returns)
                borderColor: 'red',  // Line color
                backgroundColor: 'transparent'  // No fill color
            }]
        },
        options: {
            plugins: {
                zoom: {
                    zoom: {
                        wheel: {
                            enabled: true,
                        },
                        pinch: {
                            enabled: true
                        },
                    },
                    pan: {
                        enabled: true,
                    },
                }
            }
        }
    });