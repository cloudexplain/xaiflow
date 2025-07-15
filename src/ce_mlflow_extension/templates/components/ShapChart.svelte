<script>
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';

    export let shapValues = [];
    export let featureNames = [];

    let chart;

    onMount(() => {
        const ctx = document.getElementById('shapChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: featureNames,
                datasets: [{
                    label: 'SHAP Values',
                    data: shapValues,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });

    $: if (chart) {
        chart.data.labels = featureNames;
        chart.data.datasets[0].data = shapValues;
        chart.update();
    }
</script>

<div>
    <canvas id="shapChart"></canvas>
</div>

<style>
    canvas {
        max-width: 600px;
        margin: auto;
    }
</style>