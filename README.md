# Weekly Model Comparison DAG

An Astro project (Astro Runtime 12.1.1) containing a single Airflow DAG that runs a
weekly model-comparison workflow on the breast cancer dataset.

## Start command

```bash
astro dev start
```

The Airflow UI is then available at http://localhost:8083 (login `admin` / `admin`).

> The webserver port is set to 8083 in `.astro/config.yaml` because port 8080 was
> already in use on the development machine. With the default configuration the UI
> is served at http://localhost:8080.

## DAG ID

`weekly_model_comparison` — defined in [`dags/weekly_model_comparison.py`](dags/weekly_model_comparison.py).

| Property | Value |
|---|---|
| Schedule | `@weekly` |
| Start date | 1 January 2026 |
| Catchup | Disabled |

## Pipeline

Four tasks built with the TaskFlow API, wired together purely by passing task
outputs as arguments:

```
                    ┌─> train_baseline  ─┐
preprocess_data ────┤                    ├─> evaluate_models
                    └─> train_candidate ─┘
```

1. `preprocess_data` — loads the breast cancer dataset and writes a train/test split.
2. `train_baseline` — trains a scaled logistic regression.
3. `train_candidate` — trains a random forest.
4. `evaluate_models` — scores both models on the test set and reports the better one
   by ROC AUC.

`train_baseline` and `train_candidate` are independent of each other and run in
parallel; `evaluate_models` runs only after both have succeeded.

The underlying functions live in `include/ml_pipeline.py` and are used unmodified.

## Useful commands

```bash
astro dev run dags list
```

```bash
astro dev run dags list-import-errors
```

```bash
astro dev stop
```
