<script lang="ts">
  import ImportanceChart2 from './ImportanceChart2.svelte';
  import { createEventDispatcher } from 'svelte';
  
  // Props
  export let importanceData: { feature_name: string; importance: number }[] = [];
  
  // Reactive state for selected label
  let selectedLabel: string | null = null;
  
  console.log('ChartManager: called');
  console.log('ChartManager: importanceData:', importanceData);
  console.log('ChartManager: selectedLabel:', selectedLabel);
  
  // Handle label selection changes
  function handleLabelSelection(event: CustomEvent<string | null>) {
    selectedLabel = event.detail;
    console.log('ChartManager: selectedLabel updated to:', selectedLabel);
  }
</script>

<div class="chart-manager">
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
  
  .chart-section {
    margin-bottom: 30px;
  }
  
  .chart-section h3 {
    margin-bottom: 15px;
    color: #333;
  }
  
  .chart-container {
    height: 500px;
    width: 100%;
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
</style>
