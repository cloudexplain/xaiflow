#!/bin/bash

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Build Svelte components
echo "Building Svelte components..."
npm run build

echo "Build complete! The compiled bundle is in src/ce_mlflow_extension/templates/assets/bundle.js"
