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
    let totalPages = Math.ceil(totalObservations / maxDisplayedValues);

    console.log('DeepDiveManager: 1/3 command in file');
    let pagedObservations = $derived(
        Array.from({length: Math.min(maxDisplayedValues, totalObservations - currentPage * maxDisplayedValues)}, (_, i) => {
            const idx = i + currentPage * maxDisplayedValues;
            return {
                name: `Observation ${idx + 1}`,
                index: idx
            };
        })
    );
    console.log('DeepDiveManager: 2/3 command in file');

    function selectObservation(idx: number) {
        selectedObservationIndex = idx;
    }
    function nextPage() {
        if (currentPage < totalPages - 1) {
            currentPage += 1;
        }
    }
    function prevPage() {
        if (currentPage > 0) {
            currentPage -= 1;
        }
    }

    $effect(() => {
        console.log('Selected observation index:', selectedObservationIndex);
        console.log('Current page:', currentPage);
        console.log('Total pages:', totalPages);
        console.log('DeepDiveManager: 3/3 command in file');
    });


    $effect(() => {
        console.log('Selected observation index:', selectedObservationIndex);
        console.log('Current page:', currentPage);
        console.log('Total pages:', totalPages);
    });
</script>

<div>
<div class="observation-dropdown">
    <label for="observation-select">Select Observation:</label>
    <select id="observation-select" bind:value={selectedObservationIndex}>
        {#each pagedObservations as obs}
            <option value={obs.index}>{obs.name}</option>
        {/each}
    </select>
    <button on:click={prevPage} disabled={currentPage === 0}>Prev</button>
    <button on:click={nextPage} disabled={currentPage === totalPages - 1}>Next</button>
</div>
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