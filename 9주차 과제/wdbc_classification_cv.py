import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV, cross_validate

# Load dataset
wdbc = datasets.load_breast_cancer()

# Define individual models with RobustScaler
rf_model = Pipeline([
    ('scaler', RobustScaler()),
    ('rf', RandomForestClassifier(n_estimators=700, max_depth=18, min_samples_split=3, min_samples_leaf=2, random_state=42, n_jobs=-1))
])
xgb_model = Pipeline([
    ('scaler', RobustScaler()),
    ('xgb', XGBClassifier(
        n_estimators=1000,
        max_depth=5,
        learning_rate=0.03,
        subsample=0.85,
        colsample_bytree=0.85,
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    ))
])
svc_model = Pipeline([
    ('scaler', RobustScaler()),
    ('svc', SVC(C=1.2, gamma='scale', probability=True, random_state=42))
])
lr_model = Pipeline([
    ('scaler', RobustScaler()),
    ('lr', LogisticRegression(C=1.2, max_iter=2000, random_state=42))
])

# Combine models in a StackingClassifier with XGBoost as meta-model
ensemble_model = StackingClassifier(
    estimators=[('rf', rf_model), ('xgb', xgb_model), ('svc', svc_model), ('lr', lr_model)],
    final_estimator=XGBClassifier(eval_metric='logloss', random_state=42, n_jobs=-1),
    cv=5,
    n_jobs=-1
)

# Define parameter grid for tuning meta-model
param_grid = {
    'final_estimator__learning_rate': [0.02, 0.03, 0.04],
    'final_estimator__max_depth': [3, 4],
    'final_estimator__n_estimators': [200, 250, 300]
}
grid_search = GridSearchCV(
    ensemble_model,
    param_grid,
    cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42),
    scoring='accuracy',
    n_jobs=-1
)
grid_search.fit(wdbc.data, wdbc.target)

# Best model from GridSearchCV
best_model = grid_search.best_estimator_
cv_results = cross_validate(
    best_model,
    wdbc.data,
    wdbc.target,
    cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42),
    return_train_score=True,
    n_jobs=-1
)
acc_train = np.mean(cv_results['train_score'])
acc_test = np.mean(cv_results['test_score'])
score = max(10 + 100 * (acc_test - 0.9), 0)

print(f'* Accuracy @ training data: {acc_train:.3f}')
print(f'* Accuracy @ test data: {acc_test:.3f}')
print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')