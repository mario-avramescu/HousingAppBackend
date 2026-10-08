# 🏠 Housing App Backend

REST API built with **FastAPI** that suggests housing prices using a **Random Forest** model trained on the California Housing dataset. Includes user authentication and a clean, layered project structure.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E)
![uv](https://img.shields.io/badge/uv-managed-purple)

## ✨ Features

- Price prediction endpoint powered by a scikit-learn pipeline
- Model loaded once at startup via FastAPI `lifespan`
- User authentication
- Layered architecture: routers → services → models/schemas
- Preprocessing bundled inside the model pipeline (imputation, feature engineering, scaling, one-hot encoding
- Interactive API docs (Swagger UI)

## 🧰 Tech Stack

- **API:** FastAPI, Pydantic
- **ML:** scikit-learn, pandas, NumPy, joblib
- **Database:** <!-- e.g. PostgreSQL / SQLite + SQLAlchemy / SQLModel -->
- **Tooling:** [uv](https://docs.astral.sh/uv/)

## 📁 Project Structure

```
backend/
├── app/                    # FastAPI application
│   ├── core/               # config, security, settings
│   ├── db/                 # database session and setup
│   ├── models/             # database models
│   ├── routers/            # API endpoints
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # business logic (incl. price prediction)
│   ├── dependencies.py     # shared dependencies (current user, model, ...)
│   └── main.py             # app entry point
├── ml/                     # machine learning code
│   ├── data/               # dataset (not tracked in git)
│   ├── models/             # trained models (not tracked in git)
│   ├── notebooks/          # exploration notebooks
│   ├── config.py           # paths and training constants
│   ├── features.py         # custom transformers
│   └── main.py             # training script
├── .env.example
├── pyproject.toml
└── uv.lock
```

## 🚀 Getting Started

### Prerequisites

- Python (see `.python-version`)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

```bash
git clone https://github.com/mario-avramescu/HousingAppBackend.git
cd HousingAppBackend/backend
uv sync
```

### Configuration

```bash
cp .env.example .env
```

Then edit `.env` with your own values (database URL, secret key, etc.).

### Train the model

The dataset and the trained model are not stored in the repository. Place `housing.csv` in `ml/data/` and run, from the `backend/` folder:

```bash
uv run python -m ml.main
```

The trained pipeline is saved to the path defined in `ml/config.py`.

### Run the API

```bash
uv run uvicorn app.main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

## 🔌 Example Request

```bash
curl -X POST http://127.0.0.1:8000/suggested-price \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 41,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "ocean_proximity": "NEAR BAY"
  }'
```

> Adjust the route prefix and HTTP method to match your router.

## 🧠 About the Model

| | |
|---|---|
| Algorithm | `RandomForestRegressor` |
| Dataset | California Housing |
| Train/test split | Stratified by income category |
| Numeric preprocessing | Median imputation, combined attributes, standard scaling |
| Categorical preprocessing | One-hot encoding |

