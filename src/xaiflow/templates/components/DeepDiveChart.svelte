<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { Chart, BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend } from 'chart.js';
    // todo: these annotations cause the chart to not render properly, so we disable them for now
    // import annotationPlugin from 'chartjs-plugin-annotation';
    import { colorMap } from '../utils/colormap';
    import ChartDataLabels from 'chartjs-plugin-datalabels';
    import type { Context } from 'chartjs-plugin-datalabels';
    import { createCumulativeStartEndRangesFromValues } from '../utils/utils';
  
    // Register the necessary components
    Chart.register(BarController, BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

    interface Props {
      shapValues: number[][];
      featureValues: number[][];
      selectedFeatureIndex: number;
      selectedFeature: string;
      baseValues: number[] | number;
      featureEncodings?: { [key: string]: any }[]; // For feature value mapping
      isHigherOutputBetter?: boolean; // Optional prop to determine if higher output is better
      featureNames: string[];
      observationIndex: number;
    }

    let { shapValues,
          featureValues,
          selectedFeatureIndex,
          selectedFeature,
          baseValues,
          featureEncodings=[{}],
          isHigherOutputBetter=false,
          featureNames,
          observationIndex }: Props = $props();
  
    function setBaseValue(baseValues: number[]) {
      if (baseValues.length == 2) {
        base_value = baseValues[1];
      }
      else if (typeof baseValues === 'number') {
        base_value = baseValues;
      }
      else if (baseValues.length > 1) {
        base_value = baseValues[0];
      }
      else {
        base_value = baseValues[0];
      }
    }

    console.log('DeepDiveChart: 1/4 command in file');
    let singleShapValues: number[] = $derived(shapValues[observationIndex]);
    let singleFeatureValues: number[] = $derived(featureValues[observationIndex]);
    // todo: we should check fi this is a regression or whatever type we are using and fix things for that
    let base_value: number;
    setBaseValue(baseValues);
    console.log("baseValues in DeepDiveChart", baseValues, base_value);
    console.log("DeepDiveChart: Loaded with props:", {
      shapValues,
      selectedFeatureIndex,
      selectedFeature,
      featureEncodings,
      isHigherOutputBetter,
      featureNames,
      observationIndex
    });
    console.log("DeepDiveChart: singelShapValues:", singleShapValues);
  
    let chart: Chart;
    let chartCanvas: HTMLCanvasElement;
    let maxOfData: number;
    let minOfData: number;
    let pointBackgroundColor;
    let cumulativeValues: number;
    let maxCumulativeValue: number;
  
    function updateChart(singleShapValues: number[]) {
      console.log("updateChart called with singleShapValues:", singleShapValues, "and singleFeatureValues:", singleFeatureValues);
      maxOfData = Math.max(...singleShapValues);
      minOfData = Math.min(...singleShapValues);
      
      // Color mapping based on isHigherOutputBetter prop
      pointBackgroundColor = singleShapValues.map(d => {
        const normalizedValue = (d - minOfData) / (maxOfData - minOfData) * 100;
        
        // If higher output is better, use inverted color mapping (green=high, red=low)
        // If higher output is NOT better, use normal color mapping (red=high, green=low)
        const colorValue = isHigherOutputBetter ? (100 - normalizedValue) : normalizedValue;
        
        return colorMap(colorValue);
        // return colorValue;
      });
      
      console.log("Max of Data", maxOfData);
      console.log("Min of Data", minOfData);
  
      if (chart) {
        chart.data.labels = featureNames;
        cumulativeValues = createCumulativeStartEndRangesFromValues(singleShapValues, base_value)
        chart.data.datasets[0].data = cumulativeValues;
        maxCumulativeValue = Math.max(...cumulativeValues.map(d => d[1]));
        console.log("Max Cumulative Value", maxCumulativeValue);
        // chart.data.datasets[0].data[0][0] += base_value;
        chart.data.datasets[0].backgroundColor = pointBackgroundColor;
        
        // Update x-axis rotation based on screen size
        if (chart.options.scales?.x?.ticks) {
          const isLargeScreen = window.innerWidth >= 1720;
          const isMediumScreen = window.innerWidth < 1024;
          
          chart.options.scales.x.ticks.maxRotation = isLargeScreen ? 45 : 90;
          chart.options.scales.x.ticks.minRotation = isLargeScreen ? 0 : 90;
          chart.options.scales.x.ticks.font = {
            size: window.innerWidth < 768 ? 8 : isMediumScreen ? 10 : 12
          };
        }
        
        // Update y-axis font size
        if (chart.options.scales?.y?.ticks) {
          const isSmallScreen = window.innerWidth < 768;
          const isMediumScreen = window.innerWidth < 1024;
          
          chart.options.scales.y.ticks.font = {
            size: isSmallScreen ? 8 : isMediumScreen ? 10 : 12
          };
        }
        
        // Update layout padding
        if (chart.options.layout?.padding) {
          const isSmallScreen = window.innerWidth < 768;
          chart.options.layout.padding = {
            top: isSmallScreen ? 40 : 60,
            bottom: isSmallScreen ? 5 : 10,
            left: isSmallScreen ? 5 : 10,
            right: isSmallScreen ? 5 : 10
          };
        }
        
        // Update datalabels font size and offset
        if (chart.options.plugins?.datalabels) {
          const isLargeScreen = window.innerWidth >= 1560;
          const isSmallScreen = window.innerWidth < 768;
          const isMediumScreen = window.innerWidth < 1024;
          
          chart.options.plugins.datalabels.display = isLargeScreen; // Only show on large screens
          chart.options.plugins.datalabels.font = {
            weight: 'bold',
            size: isSmallScreen ? 8 : isMediumScreen ? 9 : 10
          };
          chart.options.plugins.datalabels.offset = isSmallScreen ? 2 : 5;
        }
        
        chart.update();
      }
      console.log('DeepDiveChart: 3/4 command in file');
    }
    console.log("DeepDiveChart: Initializing chart with data", shapValues[observationIndex], featureValues[observationIndex]);
    let featureValuesSorted: (number | string | boolean)[] = [];

    $effect(() => {
      console.log('DeepDiveChart: effect 1');
      updateChart(shapValues[observationIndex]);
      console.log('DeepDiveChart: 4/4 command in file');
    });

    // Handle screen resize for responsive label rotation
    function handleResize() {
      if (chart && chart.options.scales?.x?.ticks) {
        const isLargeScreen = window.innerWidth >= 1560;
        const isSmallScreen = window.innerWidth < 768;
        const isMediumScreen = window.innerWidth < 1024;
        
        // Update x-axis
        chart.options.scales.x.ticks.maxRotation = isLargeScreen ? 45 : 90;
        chart.options.scales.x.ticks.minRotation = isLargeScreen ? 0 : 90;
        chart.options.scales.x.ticks.font = {
          size: isSmallScreen ? 8 : isMediumScreen ? 10 : 12
        };
        
        // Update y-axis
        if (chart.options.scales?.y?.ticks) {
          chart.options.scales.y.ticks.font = {
            size: isSmallScreen ? 8 : isMediumScreen ? 10 : 12
          };
        }
        
        // Update layout padding
        if (chart.options.layout?.padding) {
          chart.options.layout.padding = {
            top: isSmallScreen ? 40 : 60,
            bottom: isSmallScreen ? 5 : 10,
            left: isSmallScreen ? 5 : 10,
            right: isSmallScreen ? 5 : 10
          };
        }
        
        // Update datalabels
        if (chart.options.plugins?.datalabels) {
          chart.options.plugins.datalabels.display = isLargeScreen; // Only show on large screens
          chart.options.plugins.datalabels.font = {
            weight: 'bold',
            size: isSmallScreen ? 8 : isMediumScreen ? 9 : 10
          };
          chart.options.plugins.datalabels.offset = isSmallScreen ? 2 : 5;
        }
        
        chart.update('none'); // Update without animation for smoother resize
      }
    }
  
    onMount(() => {
      // sort feature names by featureOrder

    // let sortedFeatureNames = explanationSummary.sort((a, b) => b.importance - a.importance).map((d) => d.feature_name);
    // let sortedFeatures = modelFeatures.sort((a, b) => sortedFeatureNames.indexOf(a.feature_name) - sortedFeatureNames.indexOf(b.feature_name));
    // let sortedIdx = modelFeatures.sort((a, b) => sortedFeatureNames.indexOf(a.feature_name) - sortedFeatureNames.indexOf(b.feature_name)).map((d) => d.feature_order);
    //  const sortedFeatures = modelFeatures.sort((a, b) => a.feature_order - b.feature_order
    //                                          );
    //  
      console.log("DeepDiveChart: onMount called");
      maxOfData = Math.max(...singleShapValues);
      minOfData = Math.min(...singleShapValues);
      
      // Color mapping based on isHigherOutputBetter prop
      pointBackgroundColor = singleShapValues.map(d => {
        const normalizedValue = (d - minOfData) / (maxOfData - minOfData) * 100;
        
        // If higher output is better, use inverted color mapping (green=high, red=low)
        // If higher output is NOT better, use normal color mapping (red=high, green=low)
        const colorValue = isHigherOutputBetter ? (100 - normalizedValue) : normalizedValue;
        
        return colorMap(colorValue);
      });
  
      const data = {
        labels: featureNames,
        datasets: [{
          label: 'SHAP Values',
          data: createCumulativeStartEndRangesFromValues(singleShapValues, base_value),
          pointBackgroundColor: pointBackgroundColor,
        }]
      };
      console.log("IN DEEPDIVE data", data, featureNames);
  
      const config = {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: data,
        options: {
          indexAxis: 'x', // This makes the bar chart vertical
          layout: {
            padding: {
              top: window.innerWidth < 768 ? 40 : 60,
              bottom: window.innerWidth < 768 ? 5 : 10,
              left: window.innerWidth < 768 ? 5 : 10,
              right: window.innerWidth < 768 ? 5 : 10
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: {
                maxRotation: window.innerWidth < 1980 ? 90 : 45,
                minRotation: window.innerWidth < 1980 ? 90 : 0,
                font: {
                  size: window.innerWidth < 768 ? 8 : window.innerWidth < 1024 ? 10 : 12
                }
              }
            },
            y: {
              min: 0,
              max: Math.floor(maxCumulativeValue * 1.3),
              ticks: {
                font: {
                  size: window.innerWidth < 768 ? 8 : window.innerWidth < 1024 ? 10 : 12
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            annotation: {
              annotations: {
                baseline: {
                  type: 'line',
                  yMin: base_value,
                  yMax: base_value,
                  borderColor: 'rgb(255, 99, 132)',
                  borderWidth: 2,
                  borderDash: [6, 6],
                  label: {
                    enabled: true,
                    content: 'Baseline',
                    position: 'end'
                  }
                }
              }
            },
            datalabels: {
              display: window.innerWidth >= 1980, // Only show on large screens
              clamp: true,
              anchor: 'end',
              align: 'top',
              color: '#737373',
              font: {
                weight: 'bold',
                size: window.innerWidth < 768 ? 8 : window.innerWidth < 1024 ? 9 : 10
              },
              offset: window.innerWidth < 768 ? 2 : 5,
              formatter: function(value: [number, number], context: Context) {
                const index = context.dataIndex;
                // const description = featureDescriptions[index]; // Description not needed for datalabel
                console.log("IN DEEPDIVE featureEncodings", featureEncodings, featureEncodings[featureNames[index]]);
                let featureValue;
                
                if (featureEncodings && featureEncodings[featureNames[index]]) {
                  // Use the mapping from featureEncodings if available
                  const encodedFeatureValue = singleFeatureValues[index];
                  const mappedValue = featureEncodings[featureNames[index]][encodedFeatureValue];
                  featureValue = mappedValue;
                }
                else {
                  featureValue = singleFeatureValues[index];
                }

                let diff = value[1] - value[0];
                const shapLabel = diff > 0 ? `▲ ${Math.round(diff * 100) / 100}` : `▼ ${Math.round(diff * 100) / 100}`;

                // Helper function to break text into lines with max 10 characters each
                function breakTextIntoLines(text: string, maxCharsPerLine: number = 10): string[] {
                  if (text.length <= maxCharsPerLine) {
                    return [text];
                  }
                  
                  const lines: string[] = [];
                  const words = text.split(/[\s-_/]+/); // Split on whitespace, hyphens, underscores, slashes
                  let currentLine = '';
                  
                  for (const word of words) {
                    if (word.length > maxCharsPerLine) {
                      // If word itself is too long, break it
                      if (currentLine) {
                        lines.push(currentLine);
                        currentLine = '';
                      }
                      // Break long word into chunks
                      for (let i = 0; i < word.length; i += maxCharsPerLine) {
                        lines.push(word.slice(i, i + maxCharsPerLine));
                      }
                    } else if ((currentLine + (currentLine ? ' ' : '') + word).length <= maxCharsPerLine) {
                      currentLine += (currentLine ? ' ' : '') + word;
                    } else {
                      if (currentLine) {
                        lines.push(currentLine);
                      }
                      currentLine = word;
                    }
                  }
                  
                  if (currentLine) {
                    lines.push(currentLine);
                  }
                  
                  return lines;
                }

                // Convert featureValue to string and break into lines
                const featureValueStr = String(featureValue);
                const featureLines = breakTextIntoLines(featureValueStr, 10);

                // Limit number of lines on small screens
                const maxLines = window.innerWidth < 768 ? 2 : 3;
                const displayLines = featureLines.slice(0, maxLines);
                
                return [shapLabel, ...displayLines];
              },
            },
            tooltip: {
            callbacks: {
              label: function(context) {
                const index = context.dataIndex;
                const description = featureDescriptions[index];
                let featureValue = featureValuesSorted[index];
                let displayValue = featureValue; // Use a different variable for display

                if (featureValueNameMapping[index] !== null) {
                  // console.log("IN DEEPDIVE json_information", featureValueNameMapping[index], featureValue);
                  // console.log("IN DEEPDIVE featureValueNameMapping", featureValue);
                  displayValue = featureValueNameMapping[index][featureValue];
                }

                // Calculate the difference for the SHAP value display
                let diff = 0;
                if (Array.isArray(context.raw) && context.raw.length === 2) {
                    diff = context.raw[1] - context.raw[0];
                }
                // Display the difference in the tooltip, not the raw range
                const shapLabel = `${context.dataset.label}: ${Math.round(diff * 100) / 100}`;

                // Ensure displayValue is a string for the tooltip line
                return [shapLabel, `${description}: ${String(displayValue)}`];
              }
            }
          }
          }
        }
      };
  
      chart = new Chart(chartCanvas, config);
      updateChart(singleShapValues);
      
      // Add resize event listener
      window.addEventListener('resize', handleResize);
    });
  
    onDestroy(() => {
      // Remove resize event listener
      window.removeEventListener('resize', handleResize);
      if (chart) {
        chart.destroy();
      }
    });
  </script>
  
  <canvas bind:this={chartCanvas}></canvas>
  
  <style>
    canvas {
      max-width: 100%;
    }
  </style>