<script lang="ts">
  import ImportanceChart2 from './ImportanceChart2.svelte';
  import ScatterShapValues from './ScatterShapValues.svelte';
  import DeepDiveManager from './DeepDiveManager.svelte';
  
  // Props using Svelte 5 runes
  interface Props {
    importanceData: { feature_name: string; importance: number }[];
    shapValues: number[][];
    featureValues: number[][];
    featureEncodings?: { [key: string]: any }[]; // For feature value mapping
    baseValues: number[] | number; // Base values for SHAP calculations
    featureNames?: string[]; // Optional prop for feature names
    isHigherOutputBetter?: boolean; // Optional prop to determine if higher output is better
  }
  
  let { importanceData,
        shapValues,
        featureValues,
        featureEncodings = {},
        baseValues,
        featureNames,
        isHigherOutputBetter,
       }: Props = $props();
  
  // Reactive state for selected label using $state
  let selectedLabel: string | null = $state(null);
  let showDeepDive = $state(false);

  console.log("ChartManager", importanceData);
  console.log('ChartManager: 1/4 command in file');
  // let featureNames = $derived(
  //   importanceData.map(item => item.feature_name)
  // );
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
  <div style="display: flex; gap: 1.5rem; align-items: center; margin-bottom: 1.5rem;">
    <button type="button" on:click={() => showDeepDive = false} class:selected={!showDeepDive}>Charts</button>
    <button id="deepdive-button" type="button" on:click={() => showDeepDive = true} class:selected={showDeepDive}>Deep Dive</button>
  </div>
  {#if !showDeepDive}
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
            bind:selectedFeature={selectedLabel}
            isHigherOutputBetter={true} 
            featureEncodings={featureEncodings}
          />
        </div>
      </div>
    </div>
  {:else}
    <DeepDiveManager
      shapValues={shapValues}
      featureValues={featureValues}
      selectedFeatureIndex={selectedFeatureIndex}
      selectedFeature={selectedLabel}
      baseValues={baseValues}
      featureEncodings={featureEncodings}
      isHigherOutputBetter={true}
      featureNames={featureNames}
    />
  {/if}
</div>