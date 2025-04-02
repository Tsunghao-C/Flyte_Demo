import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from flytekit import task, workflow


# # Use flyte ImageSpec function to generate docker image
# import flytekit as fl
# image_spec = fl.ImageSpec(

#     # The name of the image. This image will be used byt he say_hello task
#     name="say-hello-image",

#     # Lock file with dependencies to install in image
#     requirements="uv.lock",
# )


# Task 1: Generate random dataset
@task(container_image="tsuchen/flyte-ml-demo")
def generate_data(n: int) -> pd.DataFrame:
    np.random.seed(42)  # For reproducibility
    mileage = np.random.randint(1000, 100000, size=n)
    price = np.random.randint(0, 6000, size=n)
    df = pd.DataFrame({"Mileage": mileage, "Price": price})
    return df


# Task 2: Standardization (Z-score Normalization)
@task(container_image="tsuchen/flyte-ml-demo")
def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df_scaled


# Task 3: Min-Max Normalization
@task(container_image="tsuchen/flyte-ml-demo")
def minmax_normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df_scaled


# Task 4: Train Linear Regression & Get R² Score
@task(container_image="tsuchen/flyte-ml-demo")
def train_and_evaluate(df: pd.DataFrame) -> float:
    X = df[["Mileage"]]
    y = df["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return r2_score(y_test, y_pred)


# Workflow
@workflow
def ml_workflow(n: int = 100) -> (float, float):
    df = generate_data(n=n)
    standardized_df = standardize_data(df=df)
    minmax_df = minmax_normalize_data(df=df)
    r2_standardized = train_and_evaluate(df=standardized_df)
    r2_minmax = train_and_evaluate(df=minmax_df)
    print(f"R² Score (Standardized): {r2_standardized}")
    print(f"R² Score (Min-Max Normalized): {r2_minmax}")
    return r2_standardized, r2_minmax


# Run the workflow locally
if __name__ == "__main__":
    ml_workflow(n=100)