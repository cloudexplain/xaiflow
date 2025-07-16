<script lang="ts">
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';

  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

  // Props
  export let data: { feature_name: string; importance: number }[] = [];
  export let selectedLabel: string | null = null;

  // Event dispatcher
  const dispatch = createEventDispatcher<{
    labelSelected: string | null;
  }>();

  let previousSelectedIndex: number | null = null;
  let chart: Chart | null = null;

  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);


  interface Props {
    data?: { feature_name: string; importance: number }[];
    selectedLabel: string | null;
  }

  console.log('ImportanceChart2: ImportanceChart2 onMount called');
  console.log('ImportanceChart2: Global Chart object:', chart);
  console.log('ImportanceChart2: importanceValues:', data);

  let chartCanvas: HTMLCanvasElement;

    const DEFAULT_COLOR: string = '#36a2eb';
    const CLICKED_COLOR: string = '#0000eb';
    const MAX_DISPLAYED_ITEMS: number = 20;
  
    onMount(() => {
      // Sort data by importance in descending order
      let orderedData = data.sort((a, b) => b.importance - a.importance);
      
      // Calculate total sum for percentage calculation
      let totalImportance = orderedData.reduce((sum, item) => sum + Math.abs(item.importance), 0);
      
      // Convert to percentages (relative values)
      let percentageData = orderedData.map(item => ({
        feature_name: item.feature_name,
        importance: Math.round((Math.abs(item.importance) / totalImportance) * 10000) / 100 // Round to 2 decimal places
      }));
      
      let displayData: { feature_name: string; importance: number }[] = [];
      let originalIndices: (number | 'others')[];
      
      // Handle case where we have more items than MAX_DISPLAYED_ITEMS
      if (percentageData.length > MAX_DISPLAYED_ITEMS) {
        // Get top N items
        displayData = percentageData.slice(0, MAX_DISPLAYED_ITEMS);
        
        // Calculate the sum of importance for the rest
        const othersSum = percentageData
          .slice(MAX_DISPLAYED_ITEMS)
          .reduce((sum, item) => sum + item.importance, 0);
        
        // Add "Others" category
        if (othersSum > 0) {
          displayData.push({ feature_name: 'Others', importance: Math.round(othersSum * 100) / 100 });
        }
        
        // Track original indices for selection
        originalIndices = [...Array(MAX_DISPLAYED_ITEMS).keys(), 'others'];
      } else {
        displayData = percentageData;
        originalIndices = [...Array(percentageData.length).keys()];
      }
      console.log("displayData", displayData);

      const ctx = chartCanvas.getContext('2d') as CanvasRenderingContext2D;

      if (!ctx) {
        throw new Error('Failed to get 2D context');
      }
      
      chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: displayData.map(d => d.feature_name),
          datasets: [{
            label: 'Feature Importance',
            data: displayData.map(d => d.importance),
            backgroundColor: displayData.map(() => DEFAULT_COLOR),
            borderColor: displayData.map(() => DEFAULT_COLOR),
            borderWidth: 1,
          }]
        },
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
          plugins: {
              title: {
                  display: true,
                  text: ["Feature Importance (%)"],
                  padding: {
                      top: 10,
                      bottom: 20
                  },
                  font: {
                      size: 16
                  }
              },
              legend: {
                  display: false
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return `${context.dataset.label}: ${context.parsed.x}%`;
                  }
                }
              }
          },
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true,
              max: 100, // Set max to 100 since we're showing percentages
              ticks: {
                callback: function(value) {
                  return value + '%';
                }
              }
            },
            y: {
              ticks: {
                autoSkip: false,
                font: {
                  size: 16
                }
              }
            }
          },
          onClick: (event: any, elements: any) => {
          if (!chart || elements.length === 0) return;
          
          const elementIndex = elements[0].index;
          const backgroundColor = Array.isArray(chart.data.datasets[0].backgroundColor) 
            ? [...chart.data.datasets[0].backgroundColor as string[]] 
            : new Array(displayData.length).fill(DEFAULT_COLOR);
          
          // Reset previous selection
          if (previousSelectedIndex !== null) {
            backgroundColor[previousSelectedIndex] = DEFAULT_COLOR;
          }
          
          // Toggle selection
          if (previousSelectedIndex === elementIndex) {
            selectedLabel = null;
            dispatch('labelSelected', null);
            previousSelectedIndex = null;
          } else {
            const selectedFeature = displayData[elementIndex].feature_name;
            
            // Special handling for "Others" category
            if (selectedFeature === 'Others') {
              selectedLabel = null;
              dispatch('labelSelected', null);
            } else {
              selectedLabel = selectedFeature;
              dispatch('labelSelected', selectedFeature);
            }
            
            previousSelectedIndex = elementIndex;
            backgroundColor[elementIndex] = CLICKED_COLOR;
          }
          
          chart.data.datasets[0].backgroundColor = backgroundColor;
          chart.update();
        }
      }
    });
  });
</script>

<div class="importance-chart-container">
  <canvas bind:this={chartCanvas}></canvas>
</div>

<style>
  .importance-chart-container {
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