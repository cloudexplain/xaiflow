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
    let filterText = $state("");
    let dropdownOpen = $state(false);

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
    function handleInputFocus() {
        dropdownOpen = true;
    }
    function handleInputBlur(event: FocusEvent) {
        // Delay closing to allow click selection
        setTimeout(() => { dropdownOpen = false; }, 100);
    }
    function handleObservationClick(idx: number) {
        selectedObservationIndex = idx;
        dropdownOpen = false;
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

    let allObservations = $derived(
        Array.from({length: totalObservations}, (_, idx) => ({
            name: `Observation ${idx + 1}`,
            index: idx
        }))
    );

    let filteredObservations = $derived(
        allObservations.filter(obs =>
            obs.name.toLowerCase().includes(filterText.toLowerCase()) ||
            obs.index.toString().includes(filterText)
        ).slice(0, maxDisplayedValues)
    );
</script>

<div>
<div class="deepdive-observation-dropdown" style="position:relative;max-width:300px;">
    <label for="observation-filter">Filter Observations:</label>
    <input id="observation-filter" type="text" bind:value={filterText} placeholder="Type to filter..."
        on:focus={handleInputFocus} on:blur={handleInputBlur} autocomplete="off" />
    {#if dropdownOpen}
        <ul class="dropdown-list" style="position:absolute;z-index:10;top:40px;left:0;width:100%;background:white;border:1px solid #ccc;max-height:200px;overflow-y:auto;padding:0;margin:0;list-style:none;">
            {#each filteredObservations as obs}
                <li style="padding:8px;cursor:pointer;" on:mousedown={() => handleObservationClick(obs.index)}>{obs.name}</li>
            {/each}
            {#if filteredObservations.length === 0}
                <li style="padding:8px;color:#888;">No matches</li>
            {/if}
        </ul>
    {/if}
    <div style="margin-top:8px;">
        <button on:click={prevPage} disabled={currentPage === 0}>Prev</button>
        <button on:click={nextPage} disabled={currentPage === totalPages - 1}>Next</button>
    </div>
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