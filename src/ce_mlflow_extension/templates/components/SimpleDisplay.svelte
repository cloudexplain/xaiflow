<script>
    export let randomNumber = 42;
    export let title = "Random Number Display";
</script>

<div class="simple-display">
    <h2>{title}</h2>
    <div class="number">{randomNumber}</div>
    <p>This number was passed from Python and displayed via Svelte!</p>
</div>

<style>
    .simple-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 20px auto;
        max-width: 400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    h2 {
        margin-top: 0;
        font-size: 1.5rem;
    }
    
    .number {
        font-size: 4rem;
        font-weight: bold;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    p {
        margin-bottom: 0;
        opacity: 0.9;
    }
</style>
