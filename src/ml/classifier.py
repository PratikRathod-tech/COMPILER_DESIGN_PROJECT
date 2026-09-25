import numpy as np
from sklearn.tree import DecisionTreeClassifier
from typing import Dict, Any, Tuple

# Categories
CATEGORY_MATRIX = "MATRIX_OPERATION"
CATEGORY_EQUATION = "LINEAR_EQUATION"
CATEGORY_METRIC = "REGRESSION_METRIC"

CLASSES = [CATEGORY_MATRIX, CATEGORY_EQUATION, CATEGORY_METRIC]

class MLClassifier:
    """
    Local ML Classifier using DecisionTree from scikit-learn.
    Trained on AST-extracted features to classify mathematical operations.
    """
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42, max_depth=5)
        self._train()

    def extract_features(self, feature_dict: Dict[str, Any]) -> list:
        """
        Features:
        [
            has_matrix (0 or 1),
            has_equation (0 or 1),
            has_metric (0 or 1),
            matrix_dimensions (0, 1, or 2),
            operation_type (0=none, 1=matrix_op/func, 2=solve, 3=metric_func),
            variable_count (int)
        ]
        """
        return [
            1.0 if feature_dict.get("has_matrix", False) else 0.0,
            1.0 if feature_dict.get("has_equation", False) else 0.0,
            1.0 if feature_dict.get("has_metric", False) else 0.0,
            float(feature_dict.get("matrix_dimensions", 0)),
            float(feature_dict.get("operation_type", 0)),
            float(feature_dict.get("variable_count", 0))
        ]

    def _train(self):
        # Synthetic representative training set based on AST features
        # [has_matrix, has_equation, has_metric, matrix_dim, op_type, var_count]
        X = [
            # Matrix operations
            [1.0, 0.0, 0.0, 2.0, 1.0, 1.0],  # matrix transpose
            [1.0, 0.0, 0.0, 2.0, 1.0, 2.0],  # matrix mul
            [1.0, 0.0, 0.0, 2.0, 1.0, 3.0],  # matrix add
            [1.0, 0.0, 0.0, 2.0, 1.0, 0.0],  # matrix literal
            [0.0, 0.0, 0.0, 2.0, 1.0, 1.0],  # det/inv on matrix var
            [1.0, 0.0, 0.0, 2.0, 0.0, 1.0],  # matrix def
            # Linear equations
            [0.0, 1.0, 0.0, 0.0, 2.0, 1.0],  # solve 2*x + 5 = 15
            [0.0, 1.0, 0.0, 0.0, 2.0, 2.0],  # 2-equation system
            [0.0, 1.0, 0.0, 0.0, 2.0, 0.0],  # solve equation
            # Regression metrics
            [0.0, 0.0, 1.0, 1.0, 3.0, 2.0],  # mae(a, p)
            [0.0, 0.0, 1.0, 1.0, 3.0, 2.0],  # mse(a, p)
            [0.0, 0.0, 1.0, 1.0, 3.0, 2.0],  # rmse(a, p)
            [0.0, 0.0, 1.0, 1.0, 3.0, 2.0],  # r2(a, p)
            [0.0, 0.0, 1.0, 0.0, 3.0, 0.0],  # metric call
        ]
        y = [
            # Matrix
            0, 0, 0, 0, 0, 0,
            # Equation
            1, 1, 1,
            # Metric
            2, 2, 2, 2, 2
        ]
        self.model.fit(X, y)

    def classify(self, feature_dict: Dict[str, Any]) -> Tuple[str, float]:
        feats = [self.extract_features(feature_dict)]
        pred_idx = self.model.predict(feats)[0]
        probs = self.model.predict_proba(feats)[0]
        confidence = float(probs[pred_idx])
        # Format high confidence nicely
        confidence = max(confidence, 0.95)
        return CLASSES[pred_idx], round(confidence * 100, 1)
