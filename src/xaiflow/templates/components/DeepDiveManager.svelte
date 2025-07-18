<script lang="ts">
    import DeepDiveChart from './DeepDiveChart.svelte';

    interface Props {
      shapValues: number[][];
      featureValues: number[][];
      selectedFeatureIndex: number;
      selectedFeature: string;
      baseValues: number[] | number;
      featureEncodings?: { [key: string]: any }[]; // For feature value mapping
      isHigherOutputBetter?: boolean; // Optional prop to determine if higher output is better
      featureNames?: string[]; // Optional prop for feature names
    }

    const maxDisplayedValues = 10;
    let { shapValues,
          featureValues,
          selectedFeatureIndex,
          selectedFeature,
          baseValues,
          featureEncodings=[{}],
          isHigherOutputBetter=false,
          featureNames=[] }: Props = $props();

    console.log('DeepDiveManager: Loaded with props:', {
        shapValues,
        selectedFeatureIndex,
        selectedFeature,
        featureEncodings,
        isHigherOutputBetter,
        featureNames
    });
    let selectedObservationIndex = $state(0);
    let currentPage = $state(0);
    let totalObservations = shapValues.length;
    let filterText = $state("");

    let allObservations = $derived(
        Array.from({length: totalObservations}, (_, idx) => ({
            name: `#${idx + 1}`,
            index: idx
        }))
    );

    let filteredObservations = $derived(
        allObservations.filter(obs =>
            obs.name.toLowerCase().includes(filterText.toLowerCase()) ||
            obs.index.toString().includes(filterText)
        )
    );

    let totalPages = $derived(Math.max(1, Math.ceil(filteredObservations.length / maxDisplayedValues)));

    let pagedObservations = $derived(
        filteredObservations.slice(currentPage * maxDisplayedValues, (currentPage + 1) * maxDisplayedValues)
    );

    function selectObservation(idx: number) {
        selectedObservationIndex = idx;
    }
    function nextPage() {
        if (currentPage < totalPages - 1) currentPage += 1;
    }
    function prevPage() {
        if (currentPage > 0) currentPage -= 1;
    }

    $effect(() => {
        console.log('Selected observation index:', selectedObservationIndex);
        console.log('Current page:', currentPage);
        console.log('Total pages:', totalPages);
    });
</script>

<div class="deepdive-flex-row">
  <div class="deepdive-observation-dropdown">
    <label for="observation-filter">Observations</label>
    <input id="observation-filter" type="text" bind:value={filterText} placeholder="Search..." autocomplete="off" />
    <ul class="job-list">
      {#each pagedObservations as obs}
        <li
          class:selected={obs.index === selectedObservationIndex}
          on:click={() => selectObservation(obs.index)}
        >
          {obs.name}
          {#if obs.index === selectedObservationIndex}
            <span class="selected-dot"></span>
          {/if}
        </li>
      {/each}
      {#if pagedObservations.length === 0}
        <li class="no-matches">No matches</li>
      {/if}
    </ul>
    <div class="deepdive-pagination">
      <button on:click={prevPage} disabled={currentPage === 0}>&lt;</button>
      <span>{currentPage + 1}/{totalPages}</span>
      <button on:click={nextPage} disabled={currentPage === totalPages - 1}>&gt;</button>
    </div>
  </div>
  <div class="deepdive-chart-container">
    <DeepDiveChart
        shapValues={shapValues}
        featureValues={featureValues}
        selectedFeatureIndex={selectedFeatureIndex}
        selectedFeature={selectedFeature}
        baseValues={baseValues}
        featureEncodings={featureEncodings}
        isHigherOutputBetter={isHigherOutputBetter}
        observationIndex={selectedObservationIndex}
        featureNames={featureNames}
    />
  </div>
</div>