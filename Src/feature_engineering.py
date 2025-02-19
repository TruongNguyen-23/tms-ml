import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer

# Handle missing symbols or fill values
# Example

class FeatureEngineering:
    def __init__(self, numerical_strategy="mean", categorical_strategy="most_frequent", scaling_method="standard"):
        self.numerical_imputer = SimpleImputer(strategy=numerical_strategy)
        self.categorical_imputer = SimpleImputer(strategy=categorical_strategy, fill_value="missing")
        self.scaling_method = scaling_method
        self.scaler = StandardScaler() if scaling_method == "standard" else MinMaxScaler()
        self.encoder = OneHotEncoder(handle_unknown="ignore")

    def handle_missing_values(self, df, numerical_cols, categorical_cols):
        df[numerical_cols] = self.numerical_imputer.fit_transform(df[numerical_cols])
        df[categorical_cols] = self.categorical_imputer.fit_transform(df[categorical_cols])
        return df

    def encode_categorical(self, df, categorical_cols):
        for col in categorical_cols:
            if df[col].nunique() > 10:
                df[col] = LabelEncoder().fit_transform(df[col])
            else:
                encoded = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, encoded], axis=1).drop(columns=[col])
        return df

    def scale_features(self, df, numerical_cols):
        df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        return df

    def feature_engineering(self, df, numerical_cols, categorical_cols):
        df = self.handle_missing_values(df, numerical_cols, categorical_cols)
        df = self.encode_categorical(df, categorical_cols)
        df = self.scale_features(df, numerical_cols)
        return df
