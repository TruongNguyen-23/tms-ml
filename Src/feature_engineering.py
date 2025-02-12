import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer

# Xử lý các đặc trưng còn thiếu thêm hoặc điền giá trị

# Example
class FeatureEngineering:
    def __init__(self, numerical_strategy="mean", categorical_strategy="most_frequent", scaling_method="standard"):
        """
        Khởi tạo các phương pháp xử lý dữ liệu.
        :param numerical_strategy: Chiến lược điền khuyết dữ liệu số ("mean", "median", "most_frequent")
        :param categorical_strategy: Chiến lược điền khuyết dữ liệu danh mục ("most_frequent", "constant")
        :param scaling_method: Phương pháp chuẩn hóa ("standard", "minmax")
        """
        self.numerical_imputer = SimpleImputer(strategy=numerical_strategy)
        self.categorical_imputer = SimpleImputer(strategy=categorical_strategy, fill_value="missing")
        self.scaling_method = scaling_method
        self.scaler = StandardScaler() if scaling_method == "standard" else MinMaxScaler()
        self.encoder = OneHotEncoder(handle_unknown="ignore")

    def handle_missing_values(self, df, numerical_cols, categorical_cols):
        """
        Điền khuyết giá trị thiếu cho dữ liệu số và dữ liệu danh mục.
        """
        df[numerical_cols] = self.numerical_imputer.fit_transform(df[numerical_cols])
        df[categorical_cols] = self.categorical_imputer.fit_transform(df[categorical_cols])
        return df

    def encode_categorical(self, df, categorical_cols):
        """
        Mã hóa biến danh mục bằng One-Hot Encoding hoặc Label Encoding.
        """
        for col in categorical_cols:
            if df[col].nunique() > 10:  # Nếu có quá nhiều giá trị duy nhất, dùng Label Encoding
                df[col] = LabelEncoder().fit_transform(df[col])
            else:
                encoded = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, encoded], axis=1).drop(columns=[col])
        return df

    def scale_features(self, df, numerical_cols):
        """
        Chuẩn hóa hoặc scale dữ liệu số.
        """
        df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        return df

    def feature_engineering(self, df, numerical_cols, categorical_cols):
        """
        Áp dụng toàn bộ pipeline xử lý đặc trưng.
        """
        df = self.handle_missing_values(df, numerical_cols, categorical_cols)
        df = self.encode_categorical(df, categorical_cols)
        df = self.scale_features(df, numerical_cols)
        return df

# Ví dụ sử dụng
if __name__ == "__main__":
    data = {
        "age": [25, 30, np.nan, 40, 50],
        "salary": [50000, 60000, 75000, np.nan, 90000],
        "city": ["New York", "San Francisco", "Los Angeles", "New York", np.nan],
        "gender": ["Male", "Female", "Female", np.nan, "Male"]
    }

    df = pd.DataFrame(data)

    numerical_cols = ["age", "salary"]
    categorical_cols = ["city", "gender"]

    fe = FeatureEngineering()
    df_processed = fe.feature_engineering(df, numerical_cols, categorical_cols)
    print(df_processed)
