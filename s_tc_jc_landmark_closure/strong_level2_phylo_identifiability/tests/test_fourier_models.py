from src.fourier_models import (
    SOURCE_LABELS,
    TARGET_LABELS,
    displayed_splits,
    source_parameterization,
    target_parameterization,
    zero_sum_assignments,
)


def test_zero_sum_assignments():
    assignments = zero_sum_assignments()
    assert len(assignments) == 64
    assert len(set(assignments)) == 64
    assert all(g[0] ^ g[1] ^ g[2] ^ g[3] == 0 for g in assignments)


def test_displayed_trees_have_all_leaves():
    for labels in (SOURCE_LABELS, TARGET_LABELS):
        for splits in displayed_splits(labels).values():
            pendant_singletons = {
                next(iter(desc))
                for name, desc in splits.items()
                if name.startswith("p")
            }
            assert pendant_singletons == {1, 2, 3, 4}


def test_parameter_counts_and_normalization():
    expected = {"JC": 14, "K2P": 26, "K3P": 38}
    for model, count in expected.items():
        for build in (source_parameterization, target_parameterization):
            coordinates, parameters = build(model)
            assert len(coordinates) == 64
            assert len(parameters) == count
            assert coordinates[(0, 0, 0, 0)] == 1

