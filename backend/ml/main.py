import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import DATA_PATH, MODEL_PATH, RANDOM_STATE, TARGET_COLUMN, TEST_SIZE
from .features import CombinedAttributesAdder


def main() -> None:
    dataset = pd.read_csv(DATA_PATH)

    income_cat = pd.cut(
        dataset["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

    X = dataset.drop(columns=[TARGET_COLUMN])
    y = dataset[TARGET_COLUMN].copy()

    X_train, _, y_train, _ = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=income_cat,
        random_state=RANDOM_STATE,
    )

    num_attribs = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_attribs = X_train.select_dtypes(include=["object", "str", "category"]).columns.tolist()

    num_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("attribs_adder", CombinedAttributesAdder()),
            ("std_scaler", StandardScaler()),
        ]
    )

    preprocessing = ColumnTransformer(
        [
            ("num", num_pipeline, num_attribs),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_attribs),
        ]
    )

    forest_reg = RandomForestRegressor(
        max_features=7,
        bootstrap=False,
        n_estimators=33,
        n_jobs=-1,
        random_state=RANDOM_STATE,
    )

    final_pipeline = Pipeline(
        [
            ("preprocessing", preprocessing),
            ("model", forest_reg),
        ]
    )

    print("Training the model...")
    final_pipeline.fit(X_train, y_train)

    joblib.dump(final_pipeline, MODEL_PATH)


if __name__ == "__main__":
    main()
