import numpy as np


def parse_vector(vector_value):
    if isinstance(vector_value, list):
        return np.array(vector_value, dtype=float)

    if isinstance(vector_value, str):
        return np.array(
            list(
                map(
                    float,
                    vector_value.strip("[]").split(","),
                )
            )
        )

    return np.array(vector_value, dtype=float)
