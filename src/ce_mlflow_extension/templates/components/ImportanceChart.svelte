<script>
    // Chart.js will be loaded globally via script tag
    
    let {
        importanceValues = [],
        featureNames = [],
        title = "Feature Importance"
    } = $props();

    let chartContainer = $state();
    let chart = $state();

    let maxImportance = $derived(
        Math.max(...importanceValues.map(value => Math.abs(value)))
    );

    // Effect to initialize the chart when container is ready
    $effect(() => {
        if (!chartContainer) return;
        
        console.log('ImportanceChart: Initializing chart container');
        
        // Cleanup function when container changes or component unmounts
        return () => {
            if (chart) {
                console.log('ImportanceChart: Cleaning up chart');
                chart.destroy();
                chart = null;
            }
        };
    });

    // Effect to create/update chart when data changes
    $effect(() => {
        if (!chartContainer || !window.Chart) return;
        
        console.log('ImportanceChart: Data effect triggered');
        console.log('importanceValues:', importanceValues);
        console.log('featureNames:', featureNames);
        
        // If no data, destroy chart and return
        if (!importanceValues.length) {
            if (chart) {
                chart.destroy();
                chart = null;
            }
            return;
        }
        
        try {
            // If chart exists, just update the data
            if (chart) {
                console.log('ImportanceChart: Updating existing chart');
                chart.data.labels = featureNames;
                chart.data.datasets[0].data = importanceValues;
                chart.options.plugins.title.text = title;
                
                // Update the y-axis max value properly
                chart.options.scales.y.max = maxImportance * 1.1;
                console.log('ImportanceChart: Setting y-axis max to:', maxImportance * 1.1);
                
                chart.update(); // Use default update to apply all changes
            } else {
                // Create new chart
                console.log('ImportanceChart: Creating new chart');
                const ctx = chartContainer.getContext('2d');
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
                        animation: {
                            duration: 0 // Disable animations to prevent effect loops
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: {
                                    color: 'rgba(0, 0, 0, 0.1)'
                                }
                            },
                            x: {
                                max: maxImportance * 1.1, // Limit to 1.1 times the max importance
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
                console.log('ImportanceChart: Chart created successfully');
            }
        } catch (error) {
            console.error('ImportanceChart: Error with chart:', error);
        }
    });
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