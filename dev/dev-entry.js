// Development entry point for testing Svelte components
import { mount } from 'svelte';
import ChartManager from '../src/ce_mlflow_extension/templates/components/ChartManager.svelte';
import ImportanceChart from '../src/ce_mlflow_extension/templates/components/ImportanceChart.svelte';
import ImportanceChart2 from '../src/ce_mlflow_extension/templates/components/ImportanceChart2.svelte';
import SimpleDisplay from '../src/ce_mlflow_extension/templates/components/SimpleDisplay.svelte';
import ScatterShapValues from '../src/ce_mlflow_extension/templates/components/ScatterShapValues.svelte';

// Sample data that matches your MLflow plugin structure
const sampleImportanceData = [
  { feature_name: "age", importance: 0.25 },
  { feature_name: "income", importance: 0.20 },
  { feature_name: "education_years", importance: 0.15 },
  { feature_name: "credit_score", importance: 0.15 },
  { feature_name: "debt_ratio", importance: 0.10 },
  { feature_name: "employment_years", importance: 0.10 },
  { feature_name: "property_value", importance: 0.05 }
];

const sampleShapValues = [
  [0.2, 0.4, 0.5, 0.6, 0.1, 0.2, 0.1],
  [-0.2, -0.4, -0.5, -0.6, -0.1, -0.2, -0.1],
  [0.1, 0.3, 0.4, 0.3, 0.2, 0.1, 0.05],
  [-0.1, -0.3, -0.4, -0.3, -0.2, -0.1, -0.05]
];

// Export components and data to global scope for testing
window.DevComponents = {
  ChartManager,
  ImportanceChart,
  ImportanceChart2,
  SimpleDisplay,
  ScatterShapValues
};

window.DevData = {
  sampleImportanceData,
  sampleShapValues
};

// Export Svelte 5 mount function
window.mount = mount;

console.log('Development components loaded:', Object.keys(window.DevComponents));
console.log('Development data loaded:', Object.keys(window.DevData));
console.log('Svelte mount function available:', typeof window.mount);
