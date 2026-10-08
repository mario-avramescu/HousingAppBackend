from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"


for dir_parh in [DATA_DIR, MODEL_DIR]:
    dir_parh.mkdir(parents=True, exist_ok=True)

DATA_PATH = DATA_DIR / "housing.csv"
MODEL_PATH = MODEL_DIR / "best_model.pkl"

TEST_SIZE = 0.2
RANDOM_STATE = 42
TARGET_COLUMN = "median_house_value"
