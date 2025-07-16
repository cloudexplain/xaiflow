<script lang="ts">
  import { run } from 'svelte/legacy';

    import { onMount, onDestroy } from 'svelte';
    // import { colorMap } from '../utils/colormap';
    import { Chart, ScatterController, PointElement, LinearScale, Title, Tooltip, Legend, BarController, BarElement, CategoryScale } from 'chart.js';
  

  interface Props {
    shapValues: number[][];
    selectedFeatureIndex: number;
    selectedFeature: string;
    featureValueNameMapping?: { [key: string]: any }[]; // For feature value mapping
    isHigherOutputBetter?: boolean; // Optional prop to determine if higher output is better
  }

    let { shapValues,
          selectedFeatureIndex,
          selectedFeature,
          featureValueNameMapping= [],
          isHigherOutputBetter=false }: Props = $props();
    let chart: Chart | undefined = $state();
    let chartCanvas: HTMLCanvasElement | undefined = $state();

    console.log('ScatterShapValues: Loaded with props:', {
        shapValues,
        selectedFeatureIndex,
        selectedFeature,
        featureValueNameMapping,
        isHigherOutputBetter
    });

    $effect(() => {
        console.log('ScatterShapValues: Props changed:', {
            shapValues,
            selectedFeatureIndex,
            selectedFeature,
            featureValueNameMapping,
            isHigherOutputBetter
        });
    });

    let dataToPlot = $derived(
        shapValues.map((row, index) => {
            console.log('Mapping row:', row, 'for feature:', selectedFeature);
            return {
                x: selectedFeature,
                y: row[selectedFeatureIndex]
            };
        })
    );
    
    // Color mapping based on isHigherOutputBetter prop
    let pointBackgroundColor = $derived(dataToPlot.map(d => {
        // const normalizedValue = (d.y - minOfData) / (maxOfData - minOfData) * 100;
        const normalizedValue = (d.y) * 100;
        
        // If higher output is better, use inverted color mapping (green=high, red=low)
        // If higher output is NOT better, use normal color mapping (red=high, green=low)
        const colorValue = isHigherOutputBetter ? (100 - normalizedValue) : normalizedValue;
        
        return '#36a2eb'; // Default color, replace with colorMap logic if needed
        // return colorMap(colorValue);
    }));

    let labels = $derived([... new Set(dataToPlot.map(d => d.x))]);

    function updateChart(dataToPlot: any[], pointBackgroundColor: string[], labels: any[]) {
      console.log("ScatterShapValues: In update chart", dataToPlot);
      if (chart) {
        // todo: not really performant, we could transform this before somewhere
        if ((dataToPlot[0].x === true) || (dataToPlot[0].x === false)) {
            labels = labels.map(l => l ? 'True' : 'False');
            dataToPlot = dataToPlot.map(d => {
                return {
                    x: d.x ? 'True' : 'False',
                    y: d.y
                };
            });
        };
        chart.data.datasets[0].data = dataToPlot;
        (chart.data.datasets[0] as any).pointBackgroundColor = pointBackgroundColor;

        chart.options.plugins.title.text = [`Shap Values for ${selectedFeature}`] 
        
        if (chart.options.scales) {
            chart.options.scales.x = getXConfig(labels) as any;
        } 
        
        if (chart.options.plugins?.tooltip?.callbacks) {
            chart.options.plugins.tooltip.callbacks.label = function(context: any) {
                return [
                    `Feature: ${selectedFeature}`,
                    `Shap Value: ${context.raw.y}`,
                ];
            }
        }
        
        chart.update();
      }
    }
  
    run(() => {
    updateChart(dataToPlot, pointBackgroundColor, labels);
  });


    run(() => {
    if (chart) {
          updateChart(dataToPlot, pointBackgroundColor, labels);
      }
  });

    function getXConfig(labels: boolean[] | string[] | number[]) {
        if (typeof labels[0] === 'boolean') {
            return {
                type: 'category',
                labels: labels.map(l => l ? 'True' : 'False'),
                offset: true,
            };
        } else if (typeof labels[0] === 'string') {
            return {
                type: 'category',
                labels: labels,
                offset: true,
            };
        } else {
            return {
                type: 'linear',
                position: 'left'
            };
        }
    }

    function createChart() {
        let df = {
            datasets: [{
                // label: [`Shap Values for ${selectedFeature.feature_display_name}\n${selectedFeatureDisplayDescription}`, ],
                data: dataToPlot,
                labels: labels,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                // borderColor: 'rgba(75, 192, 192, 1)',
                pointBackgroundColor: pointBackgroundColor,
                borderWidth: 1
            }]
        };
        console.log('ScatterShapValues: Creating chart with data:', df);

      // Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);
      Chart.register(ScatterController, PointElement, LinearScale, Title, Tooltip, Legend);
      const ctx = chartCanvas?.getContext('2d');
      if (!ctx) {
          throw new Error('Failed to get 2D context');
      }
      chart = new Chart(ctx, {
            type: 'scatter',
            data: df,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                  padding: {
                    top: 10,
                    bottom: 10,
                    left: 10,
                    right: 10
                  }
                },
                interaction: {
                    intersect: false,
                    mode: 'nearest',
                    axis: 'xy'
                },
                plugins: {
                    title: {
                        display: true,
                        text: [`Shap Values for ${selectedFeature}`],
                        padding: {
                            top: 10,
                        },
                        font: {
                            size: 16
                        }
                    },
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        mode: 'nearest',
                        intersect: false,
                        filter: function(tooltipItem) {
                            // Only show tooltip for the nearest point
                            return true;
                        },
                        callbacks: {
                            label: function(context) {
                                return [
                                    `Feature: ${selectedFeature}`,
                                    `Shap Value: ${context.raw.y}`,
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: getXConfig(labels) as any,
                    y: {
                        type: 'linear' as const,
                        position: 'left' as const
                    }
                }
            }
        });
      updateChart(dataToPlot, pointBackgroundColor, labels);
    }

    onMount(() => {
        createChart();
    });

    // Cleanup chart instance on component destroy
    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="scatter-shap-container">
  <canvas bind:this={chartCanvas}></canvas>
</div>

<style>
  .scatter-shap-container {
    position: relative;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  
  canvas {
    width: 100% !important;
    height: 100% !important;
    max-width: 100%;
    max-height: 100%;
    display: block;
  }
</style>