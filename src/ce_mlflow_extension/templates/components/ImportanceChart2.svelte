<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';

  Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

  // Props using Svelte 5 runes
  interface Props {
    data?: { feature_name: string; importance: number }[];
    selectedLabel?: string | null;
  }
  
  let { data = [], selectedLabel = $bindable(null) }: Props = $props();
  console.log("ImportanceChart2: Loaded with data:", data, "and selectedLabel:", selectedLabel);
  
  // Debug the derived values
  $effect(() => {
    console.log("ImportanceChart2: orderedData:", orderedData);
    console.log("ImportanceChart2: totalImportance:", totalImportance);
    console.log("ImportanceChart2: percentageData:", percentageData);
    console.log("ImportanceChart2: displayData:", displayData);
  });

  // Event dispatcher
  const dispatch = createEventDispatcher<{
    labelSelected: string | null;
  }>();

  // Internal state
  let previousSelectedIndex: number | null = $state(null);
  let chart: Chart | null = $state(null);
  let chartCanvas: HTMLCanvasElement | null = $state(null);

  const DEFAULT_COLOR: string = '#36a2eb';
  const CLICKED_COLOR: string = '#0000eb';
  const MAX_DISPLAYED_ITEMS: number = 20;

  // Derived values using $derived with safety checks
  const orderedData = $derived(
    Array.isArray(data) ? [...data].sort((a, b) => b.importance - a.importance) : []
  );

  const totalImportance = $derived(
    orderedData.length > 0 ? orderedData.reduce((sum, item) => sum + Math.abs(item.importance), 0) : 1
  );

  const percentageData = $derived(
    orderedData.map(item => ({
      feature_name: item.feature_name,
      importance: Math.round((Math.abs(item.importance) / totalImportance) * 10000) / 100
    }))
  );

  const displayData = $derived(
    percentageData.length > MAX_DISPLAYED_ITEMS 
      ? (() => {
          const topItems = percentageData.slice(0, MAX_DISPLAYED_ITEMS);
          const othersSum = percentageData
            .slice(MAX_DISPLAYED_ITEMS)
            .reduce((sum, item) => sum + item.importance, 0);
          
          if (othersSum > 0) {
            return [...topItems, { feature_name: 'Others', importance: Math.round(othersSum * 100) / 100 }];
          }
          return topItems;
        })()
      : percentageData
  );

  let maxY = $derived(
    Math.max(...displayData.map(item => item.importance)) * 1.1
  );

  // Effect to initialize canvas cleanup
  $effect(() => {
    if (!chartCanvas) return;
    
    console.log("ImportanceChart2: Canvas ready");
    
    // Cleanup function
    return () => {
      if (chart) {
        console.log("ImportanceChart2: Cleaning up chart");
        chart.destroy();
        chart = null;
      }
    };
  });

  // Effect to create/update chart when data changes
  $effect(() => {
    console.log("ImportanceChart2: Effect triggered");
    console.log("ImportanceChart2: chartCanvas:", chartCanvas);
    console.log("ImportanceChart2: displayData:", displayData);
    console.log("ImportanceChart2: displayData.length:", displayData.length);
    
    if (!chartCanvas) {
      console.log("ImportanceChart2: No canvas yet");
      return;
    }
    
    if (!displayData.length) {
      console.log("ImportanceChart2: No data yet");
      return;
    }

    console.log("ImportanceChart2: Creating/updating chart with displayData:", displayData);

    const ctx = chartCanvas.getContext('2d') as CanvasRenderingContext2D;
    if (!ctx) {
      throw new Error('Failed to get 2D context');
    }

    try {
      // If chart exists, update it instead of recreating
      if (chart) {
        console.log("ImportanceChart2: Updating existing chart");
        chart.data.labels = displayData.map(d => d.feature_name);
        chart.data.datasets[0].data = displayData.map(d => d.importance);
        chart.data.datasets[0].backgroundColor = displayData.map(() => DEFAULT_COLOR);
        chart.data.datasets[0].borderColor = displayData.map(() => DEFAULT_COLOR);
        chart.update('none'); // Use 'none' to avoid animations
        return;
      }

      // Create new chart
      console.log("ImportanceChart2: Creating new chart");
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
          animation: {
            duration: 0 // Disable animations to prevent effect loops
          },
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
            max: Math.ceil(maxY * 1.05 / 10) * 10,
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
          chart.update('none'); // Use 'none' to avoid animation loops
        }
      }});
      console.log("ImportanceChart2: Chart created successfully");
    } catch (error) {
      console.error("ImportanceChart2: Error creating chart:", error);
    }
  });
    console.log("ImportanceChart2: Component mounted and chart created");
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