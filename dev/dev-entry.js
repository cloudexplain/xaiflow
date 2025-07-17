// Development entry point for testing Svelte components
import { mount } from 'svelte';
import ChartManager from '../src/xaiflow/templates/components/ChartManager.svelte';
import ImportanceChart2 from '../src/xaiflow/templates/components/ImportanceChart2.svelte';
import ScatterShapValues from '../src/xaiflow/templates/components/ScatterShapValues.svelte';
import DeepDiveManager from '../src/xaiflow/templates/components/DeepDiveManager.svelte';
import DeepDiveChart from '../src/xaiflow/templates/components/DeepDiveChart.svelte';

// Export components immediately
window.DevComponents = {
  ChartManager,
  ImportanceChart2,
  ScatterShapValues,
  DeepDiveManager,
  DeepDiveChart
};

// Export Svelte 5 mount function
window.mount = mount;

// Function to load data asynchronously
async function loadTestData() {
  let testReportData = null;
  let sampleImportanceData = [];
  let sampleShapValues = [];
  let sampleFeatureValues = [];
  let sampleBaseValues = [];
  let sampleFeatureEncodings = {};
  let sampleFeatureNames = [];

  try {
    // Fetch the test data file
    const response = await fetch('../test_report_data.json');
    if (response.ok) {
      testReportData = await response.json();
      console.log('Loaded test report data:', testReportData);
      
      // Extract and transform data from the loaded JSON
      if (testReportData.importance_data && testReportData.importance_data.features && testReportData.importance_data.values) {
        // Transform importance data to the expected format
        sampleImportanceData = testReportData.importance_data.features.map((feature, index) => ({
          feature_name: feature,
          importance: testReportData.importance_data.values[index]
        }));
      } else {
        sampleImportanceData = [];
      }
      
      console.log("Feature Encodings", testReportData.feature_encodings );
      
      sampleShapValues = testReportData.shap_values || [];
      sampleFeatureValues = testReportData.feature_values || [];
      sampleBaseValues = testReportData.base_values || [];
      sampleFeatureEncodings = testReportData.feature_encodings || {};
      sampleFeatureNames = testReportData.feature_names || [];
      
      console.log('Parsed data:');
      console.log('- Importance data:', sampleImportanceData);
      console.log('- SHAP values (sample):', sampleShapValues.slice(0, 3));
      console.log('- Feature values (sample):', sampleFeatureValues.slice(0, 3));
      console.log('- Base values (sample):', sampleBaseValues.slice(0, 3));
      console.log('- Feature encodings:', sampleFeatureEncodings);
      console.log('- Feature Names:', sampleFeatureNames);
    } else {
      throw new Error(`Failed to load test data: ${response.status}`);
    }
  } catch (error) {
    console.warn('Could not load test_report_data.json, using fallback data:', error);
  }

  return {
    sampleImportanceData,
    sampleShapValues,
    sampleFeatureValues,
    sampleBaseValues,
    sampleFeatureEncodings,
    sampleFeatureNames,
  };
}

// Make data loading function available globally
window.loadTestData = loadTestData;

console.log('Development components loaded:', Object.keys(window.DevComponents));
console.log('Svelte mount function available:', typeof window.mount);
console.log('Test data loader available:', typeof window.loadTestData);
