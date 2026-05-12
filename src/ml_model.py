"""Train a simple Random Forest classifier from features.csv."""
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sklearn.model_selection import train_test_split


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default="results/features.csv")
    parser.add_argument("--label", default="class")
    args = parser.parse_args()

    df = pd.read_csv(args.features)
    if args.label not in df.columns:
        raise ValueError(f"Label column '{args.label}' not found. Check sample_metadata.csv and features.csv")

    df = df.dropna(subset=[args.label])
    X = df.drop(columns=[args.label, "sample_id"], errors="ignore")
    X = X.select_dtypes(include=["number"]).fillna(0)
    y = df[args.label]

    if y.nunique() < 2:
        raise ValueError("Need at least two classes for classification.")

    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=stratify
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print("Precision:", precision_score(y_test, pred, average="weighted", zero_division=0))
    print("Recall:", recall_score(y_test, pred, average="weighted", zero_division=0))
    print("\nClassification report:\n", classification_report(y_test, pred, zero_division=0))


if __name__ == "__main__":
    main()
