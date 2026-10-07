"""Exact rational certificate in upstream jet interiority; no full proof claim."""
from fractions import Fraction as F
from math import factorial
import runpy
from pathlib import Path

exp_upper = sum(F(4, 3) ** j / factorial(j) for j in range(9))
exp_upper += (F(4, 3) ** 9 / factorial(9)) / (1 - F(4, 30))
exp_lower = sum(F(1, factorial(j)) for j in range(7))
assert exp_upper == F(917330371, 241805655)
assert exp_upper < F(1897, 500)
assert exp_lower == F(1957, 720)
assert exp_lower > F(1359, 500)
certificate = F(3, 4) * F(1897, 500) - F(1, 3) * F(1359, 500)
assert certificate == F(3879, 2000) < 2
print("Exact exponential upper tail:", exp_upper)
print("Exact exponential lower sum:", exp_lower)
print("C* upper certificate:", certificate, "< 2")
runpy.run_path(str(Path(__file__).resolve().parents[1] / "agent_notes/fourfold_constants_check.py"), run_name="__main__")
