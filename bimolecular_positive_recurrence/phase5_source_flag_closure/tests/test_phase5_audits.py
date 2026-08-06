from fractions import Fraction
from random import Random

from src.generator import Reaction
from phase5_source_flag_closure.src.bad_sequence_flags import verify_certificate
from phase5_source_flag_closure.src.bounded_defect_full_audit import audit_lifted_path
from phase5_source_flag_closure.src.episode_library import shortest_designated_path
from phase5_source_flag_closure.src.global_foster_verifier import calibration_report
from phase5_source_flag_closure.src.source_rate_flag import (
    bimolecular_complexes,
    top_availability_or_conservation,
)


def test_lifted_path_audit():
    rs = (
        Reaction((0, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (0, 1), Fraction(3)),
        Reaction((0, 1), (0, 0), Fraction(5)),
    )
    path = shortest_designated_path(rs, (0, 0), (0, 1))
    cert = audit_lifted_path(rs, (200, 0), path)
    assert cert.jump_bound == 3
    assert cert.max_coordinate_overshoot == 6


def test_random_four_species_top_alternatives():
    rng = Random(20260805)
    allc = bimolecular_complexes(4)
    for _ in range(5000):
        C = tuple(y for y in allc if rng.random() < 0.3)
        if not C:
            C = (allc[rng.randrange(len(allc))],)
        I = {i for i in range(4) if rng.random() < 0.5}
        if not I:
            I = {rng.randrange(4)}
        w = [Fraction(0)] * 4
        while not any(w):
            for i in I:
                w[i] = Fraction(rng.randrange(4))
        cert = top_availability_or_conservation(C, I, w)
        verify_certificate(C, I, w, cert)


def test_calibration_report():
    report = calibration_report()
    assert set(report) == {
        "canonical_trigger_drain",
        "immigration_linear_death",
        "several_I_types",
    }
