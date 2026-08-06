from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PHASE1 = ROOT.parent
sys.path.insert(0, str(PHASE1))

from phase2_trigger_drain.src.support_regimes import certify_safe_support, q_count
from src.generator import Reaction


def test_q_count():
    assert q_count((2, 1, 0), {0, 2}) == 2


def test_safe_support_conservation_dichotomy():
    rs = [
        Reaction((1, 0), (1, 1), Fraction(2)),
        Reaction((1, 1), (1, 0), Fraction(3)),
    ]
    cert = certify_safe_support(rs, {0})
    assert cert.q_is_conserved
    assert cert.strict_q_descents == ()
