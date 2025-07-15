<script>
    export let metadata = {};
    export let title = "Model Metadata";
</script>

<div class="metadata-container">
    <h3>{title}</h3>
    <div class="metadata-table">
        {#each Object.entries(metadata) as [key, value]}
            <div class="metadata-row">
                <div class="metadata-key">{key}</div>
                <div class="metadata-value">{value}</div>
            </div>
        {/each}
    </div>
</div>

<style>
    .metadata-container {
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    h3 {
        margin: 0 0 15px 0;
        color: #333;
        font-size: 18px;
        font-weight: bold;
    }

    .metadata-table {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .metadata-row {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 15px;
        padding: 8px 0;
        border-bottom: 1px solid #e9ecef;
    }

    .metadata-row:last-child {
        border-bottom: none;
    }

    .metadata-key {
        font-weight: 600;
        color: #495057;
    }

    .metadata-value {
        color: #212529;
        word-break: break-word;
    }
</style>