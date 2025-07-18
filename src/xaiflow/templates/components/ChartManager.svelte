<script lang="ts">
  import ImportanceChart2 from './ImportanceChart2.svelte';
  import ScatterShapValues from './ScatterShapValues.svelte';
  
  // Props using Svelte 5 runes
  interface Props {
    importanceData: { feature_name: string; importance: number }[];
    shapValues: number[][];
    featureValues: number[][];
    featureEncodings?: { [key: string]: any }[]; // For feature value mapping
  }
  
  let { importanceData, shapValues, featureValues, featureEncodings = {} }: Props = $props();
  
  // Reactive state for selected label using $state
  let selectedLabel: string | null = $state(null);

  console.log("ChartManager", importanceData);
  console.log('ChartManager: 1/4 command in file');
  let featureNames = $derived(
    importanceData.map(item => item.feature_name)
  );
  console.log('ChartManager: 2/4 command in file');
  
  console.log('ChartManager: called');
  console.log('ChartManager: importanceData:', importanceData);
  console.log('ChartManager: selectedLabel:', selectedLabel);
  console.log('ChartManager: featureValues:', featureValues);
  
  // Handle label selection changes
  function handleLabelSelection(event: CustomEvent<string | null>) {
    selectedLabel = event.detail;
    console.log('ChartManager: selectedLabel updated to:', selectedLabel);
    console.log('ChartManager: 3/4 command in file');
  }

  let selectedFeatureIndex = $derived(featureNames.indexOf(selectedLabel || null));
  $effect(() => {
    console.log('ChartManager: selectedFeatureIndex updated to:', selectedFeatureIndex);
    console.log('ChartManager: 4/4 command in file');
  });
</script>

<div class="chart-manager">
  <div class="charts-row">
    <div class="chart-section">
      <h3>Feature Importance Chart</h3>
      <div class="chart-container">
        <ImportanceChart2 
          data={importanceData} 
          bind:selectedLabel={selectedLabel}
          on:labelSelected={handleLabelSelection}
        />
      </div>
    </div>
    
    <div class="chart-section">
      <h3>SHAP Values</h3>
      <div class="chart-container">
        <ScatterShapValues 
          shapValues={shapValues} 
          featureValues={featureValues}
          bind:selectedFeatureIndex={selectedFeatureIndex} 
          selectedFeature={selectedLabel}
          bind:selectedLabel={selectedLabel}
          isHigherOutputBetter={true} 
          featureEncodings={featureEncodings}
        />
      </div>
    </div>
  </div>
</div>