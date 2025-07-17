export interface Explanation {
  explanation_name: string;
  explanation_id: string;
  environment: string;
  count: number;
  observation_id_column: string;
  explanation_description: string;
  explanation_date: Date;
}

export interface Model {
  model_id: string;
  model_name: string;
  feature_names: string[];
  model_framework: string;
  model_framework_version: string;
  model_description: string;
  model_hash: string;
  register_date: Date;
}

export interface DataSource {
  data_source_id: string;
  data_source_name: string;
}

export interface DataSourceInfo {
  data_source_name: string;
  data_source_description: string;
  data_source_id: string;
}

export interface DataSource2Models {
  data_source_id: string;
  models: {
    model_id: string;
  }[];
}

export interface Model2Explanations {
  model_id: string;
  explanations: {
    explanation_id: string;
  }[];
}

export interface ModelFeature {
  feature_order: number;
  feature_description: string | null;
  feature_display_description: string;
  feature_display_name: string;
  feature_name: string;
  json_information: { [key: string]: any } | null;
}

export interface ExplanationDetail {
  explanation_detail_id: string;
  shap_value_json: Array<number>;
  observation_id: string;
  feature_value_json: Array<number | boolean | string>;
  prediction_probability: string | null;
  prediction_value: string;
}

export interface ExplanationSummary {
  explanation_id: string;
  feature_name: string;
  std: number;
  mean: number;
  importance: number;
  percentile_10: number;
  percentile_25: number;
  percentile_50: number;
  percentile_75: number;
  percentile_90: number;
  summary: string;
  max: number;
  min: number;
}

export interface FeatureCorrelation {
  explanation_id: string;
  feature_name1: string;
  feature_name2: string;
  correlation: number;
}
export interface ExplanationMetadata {
  explanation_id: string;
  base_values: Array<number>;
  prediction_meaning: string | null;
  observation_instance: string | null;
  observation_description: string | null;
}

export interface ExplanationMetadata {
  explanation_id: string;
  base_values: Array<number>;
}

export interface OverviewMetadata {
  data_source_name: string;
  explanation_name: string;
  explanation_count: number;
  environment: string;
  ml_type: string;
  run_mode: string;
  explanation_date: Date;
}

export interface ExplanationEntry {
  EXPLANATION_ID: string;
  EXPLANATION_COUNT: number;
  EXPLANATION_NAME: string;
  ENVIRONMENT: string;
  ML_TYPE: string;
  REMARKS: string;
  EXPLANATION_DATE: Date;
}

export interface User {
  user_id: string;
  email: string;
  role: string;
  created_at: Date;
  last_login?: Date;
  permissions?: Record<string, boolean>;
  avatar?: string | null;
  surname?: string | null;
  last_name?: string | null;
  is_active?: boolean;
  tutorial_completed?: boolean;
}
