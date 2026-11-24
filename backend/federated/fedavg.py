import numpy as np


def federated_average(models):
    """
    Federated Averaging (FedAvg)

    models:
        List of tuples:
        (trained_model, number_of_training_samples)
    """

    if not models:
        raise ValueError("No hospital models provided.")

    total_samples = sum(
        samples for _, samples in models
    )

    averaged_coef = None
    averaged_intercept = None

    for model, samples in models:

        # Weight based on hospital dataset size
        weight = samples / total_samples

        coef = model.coef_
        intercept = model.intercept_

        if averaged_coef is None:

            averaged_coef = weight * coef
            averaged_intercept = weight * intercept

        else:

            averaged_coef += weight * coef
            averaged_intercept += weight * intercept

    return averaged_coef, averaged_intercept


def update_global_model(global_model, models):
    """
    Update the global model using
    the averaged hospital parameters.
    """

    coef, intercept = federated_average(models)

    global_model.coef_ = np.asarray(coef)
    global_model.intercept_ = np.asarray(intercept)

    return global_model