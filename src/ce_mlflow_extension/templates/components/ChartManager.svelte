<script lang="ts">
  import ImportanceChart2 from './ImportanceChart2.svelte';
  import ScatterShapValues from './ScatterShapValues.svelte';
  
  // Props using Svelte 5 runes
  interface Props {
    importanceData: { feature_name: string; importance: number }[];
    shapValues: number[][];
    featureValues: number[][];
  }
  
  let { importanceData, shapValues, featureValues }: Props = $props();
  
  // Reactive state for selected label using $state
  let selectedLabel: string | null = $state(null);

  console.log("ChartManager", importanceData);
  let featureNames = $derived(
    importanceData.map(item => item.feature_name)
  );
  
  console.log('ChartManager: called');
  console.log('ChartManager: importanceData:', importanceData);
  console.log('ChartManager: selectedLabel:', selectedLabel);
  console.log('ChartManager: featureValues:', featureValues);
  
  // Handle label selection changes
  function handleLabelSelection(event: CustomEvent<string | null>) {
    selectedLabel = event.detail;
    console.log('ChartManager: selectedLabel updated to:', selectedLabel);
  }

  let selectedFeatureIndex = $derived(featureNames.indexOf(selectedLabel || null));
  $effect(() => {
    console.log('ChartManager: selectedFeatureIndex updated to:', selectedFeatureIndex);
  });
</script>

<div class="chart-manager">
  <!-- Debug information -->
  <div style="background: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 4px;">
    <h4 style="margin: 0 0 10px 0; color: #666;">Debug Info:</h4>
    <p style="margin: 5px 0; font-size: 12px;">
      ImportanceData length: {importanceData?.length || 0}
    </p>
    <p style="margin: 5px 0; font-size: 12px;">
      ShapValues length: {shapValues?.length || 0}
    </p>
    <p style="margin: 5px 0; font-size: 12px;">
      FeatureValues length: {featureValues?.length || 0}
    </p>
    <p style="margin: 5px 0; font-size: 12px;">
      Selected Label: {selectedLabel || 'None'}
    </p>
  </div>

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
          selectedFeature="Feature Name" 
          bind:selectedLabel={selectedLabel}
          isHigherOutputBetter={true} 
        />
      </div>
    </div>
  </div>
  
  {#if selectedLabel}
    <div class="selected-info">
      <p><strong>Selected Feature:</strong> {selectedLabel}</p>
    </div>
  {/if}
  
  <!-- You can add more charts here that will react to the same selectedLabel -->
  <!-- 
  <div class="chart-section">
    <h3>Another Chart</h3>
    <div class="chart-container">
      <AnotherChart 
        data={someOtherData} 
        bind:selectedLabel={selectedLabel} 
      />
    </div>
  </div>
  -->
</div>

<style>
  .chart-manager {
    width: 100%;
  }
  
  .charts-row {
    display: flex;
    flex-direction: row;
    gap: 20px;
    margin-bottom: 30px;
    width: 100%;
    align-items: stretch;
  }
  
  .chart-section {
    flex: 1;
    min-width: 0; /* Allows flex items to shrink below their natural width */
    width: 50%;
    max-width: 50%;
  }
  
  .chart-section h3 {
    margin-bottom: 15px;
    color: #ff0000; /* Changed to red to test props propagation */
    text-align: center;
    font-weight: bold;
  }
  
  .chart-container {
    height: 500px;
    width: 100%;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    background-color: #fafafa;
    box-sizing: border-box;
  }
  
  .selected-info {
    background-color: #f0f8ff;
    padding: 15px;
    border-radius: 5px;
    border-left: 4px solid #007acc;
    margin-top: 20px;
  }
  
  .selected-info p {
    margin: 0;
    font-size: 16px;
  }
  
  /* Responsive design for smaller screens */
  @media (max-width: 768px) {
    .charts-row {
      flex-direction: column;
    }
    
    .chart-container {
      height: 400px;
    }
  }
</style>
