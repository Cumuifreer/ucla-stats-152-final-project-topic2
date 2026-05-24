import unittest

import numpy as np
import pandas as pd

from project_helpers import compute_vif, time_ordered_split


class ProjectHelperTests(unittest.TestCase):
    def test_time_ordered_split_keeps_early_rows_in_train(self):
        data = pd.DataFrame({"value": np.arange(10)})

        train_data, test_data = time_ordered_split(data, train_fraction=0.6)

        self.assertEqual(train_data["value"].tolist(), [0, 1, 2, 3, 4, 5])
        self.assertEqual(test_data["value"].tolist(), [6, 7, 8, 9])

    def test_compute_vif_is_one_for_uncorrelated_predictors(self):
        predictors = pd.DataFrame(
            {
                "x1": [-2, -1, 0, 1, 2],
                "x2": [2, -1, -2, -1, 2],
            }
        )

        vif_table = compute_vif(predictors)

        self.assertEqual(vif_table["predictor"].tolist(), ["x1", "x2"])
        self.assertTrue(np.allclose(vif_table["VIF"], [1.0, 1.0]))

    def test_compute_vif_flags_strong_collinearity(self):
        predictors = pd.DataFrame(
            {
                "x1": np.arange(20),
                "x2": np.arange(20) * 2 + 0.01,
                "x3": [0, 1] * 10,
            }
        )

        vif_table = compute_vif(predictors)
        x1_vif = vif_table.loc[vif_table["predictor"] == "x1", "VIF"].iloc[0]

        self.assertTrue(np.isinf(x1_vif))


if __name__ == "__main__":
    unittest.main()
