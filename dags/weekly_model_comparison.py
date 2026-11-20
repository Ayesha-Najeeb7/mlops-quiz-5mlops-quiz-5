"""Weekly model comparison pipeline.

Prepares the breast cancer dataset, trains a logistic regression baseline and a
random forest candidate independently of one another, then compares the two
once both have finished training.
"""

from datetime import datetime

from airflow.decorators import dag, task

from include import ml_pipeline


@dag(
    dag_id="weekly_model_comparison",
    start_date=datetime(2026, 1, 1),
    schedule="@weekly",
    catchup=False,
    tags=["mlops", "quiz"],
)
def weekly_model_comparison():
    """Four TaskFlow tasks wired purely by passing outputs as arguments."""

    @task
    def preprocess_data():
        return ml_pipeline.preprocess_data()

    @task
    def train_baseline(data_path):
        return ml_pipeline.train_baseline(data_path)

    @task
    def train_candidate(data_path):
        return ml_pipeline.train_candidate(data_path)

    @task
    def evaluate_models(baseline_path, candidate_path):
        return ml_pipeline.evaluate_models(baseline_path, candidate_path)

    data_path = preprocess_data()

    # Both trainers depend only on the data, never on each other
    baseline_path = train_baseline(data_path)
    candidate_path = train_candidate(data_path)

    evaluate_models(baseline_path, candidate_path)


weekly_model_comparison()
