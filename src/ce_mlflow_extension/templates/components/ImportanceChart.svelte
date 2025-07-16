<script>
    import { onMount } from 'svelte';
    
    // Chart.js will be loaded globally via script tag
    
    let {
        importanceValues = [],
        featureNames = [],
        title = "Feature Importance"
    } = $props();

    let chartContainer;
    let chart;

    onMount(() => {
        console.log('ImportanceChart onMount called');
        console.log('Global Chart object:', window.Chart);
        console.log('chartContainer:', chartContainer);
        console.log('importanceValues:', importanceValues);
        
        if (chartContainer && importanceValues.length > 0 && window.Chart) {
            try {
                const ctx = chartContainer.getContext('2d');
                console.log('Creating chart with context:', ctx);
                chart = new window.Chart(ctx, {
                type: 'bar',
                data: {
                    labels: featureNames,
                    datasets: [{
                        label: 'Importance',
                        data: importanceValues,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: title,
                            font: {
                                size: 16,
                                weight: 'bold'
                            }
                        }
                    }
                }
            });
            console.log('Chart created successfully:', chart);
        } catch (error) {
            console.error('Error creating chart:', error);
        }
    } else {
        console.log('Cannot create chart:', { 
            hasContainer: !!chartContainer, 
            dataLength: importanceValues.length,
            hasChart: !!window.Chart
        });
    }
    });

    $effect(() => { if (chart && importanceValues.length > 0) {
        chart.data.labels = featureNames;
        chart.data.datasets[0].data = importanceValues;
        chart.update();
    }});
</script>

<div class="chart-wrapper">
    <canvas bind:this={chartContainer}></canvas>
</div>

<style>
    .chart-wrapper {
        width: 100%;
        height: 400px;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    canvas {
        width: 100% !important;
        height: 100% !important;
    }
</style>