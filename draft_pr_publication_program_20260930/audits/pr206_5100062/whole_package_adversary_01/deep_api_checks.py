"""Adversarial finite API checks from authenticated source buffers."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import os
import sys
import types

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parent / "publication_package_v1/verification/portable_exact_verifier.py"
PIN = "dfa1ff339e1f3a6004563aec9c01f6f14d6bb65a94e2437f3ba3a41e5b393d85"


def main():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PIN:
        raise RuntimeError("source changed")
    output = OWN / ("api_optimized_v2" if sys.flags.optimize else "api_normal_v2")
    output.mkdir(exist_ok=False)

    def safe_writes(event, args):
        if event == "open":
            path, mode, flags = args
            writing = isinstance(mode, str) and any(x in mode for x in "wax+")
            writing = writing or isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if writing and isinstance(path, (str, bytes, os.PathLike)):
                if not Path(path).resolve().is_relative_to(output):
                    raise PermissionError("outside audit output")

    sys.addaudithook(safe_writes)
    m = types.ModuleType("independently_audited_portable_verifier")
    m.__file__ = str(SOURCE)
    sys.modules[m.__name__] = m
    exec(compile(raw, str(SOURCE), "exec", optimize=sys.flags.optimize), m.__dict__)
    results = []

    def reject(label, action):
        try:
            action()
        except Exception as e:
            results.append({"label": label, "result": "rejected", "exception": type(e).__name__, "message": str(e)})
        else:
            raise RuntimeError("Invalid input accepted: "+label)

    for value in (True, False, 0.0, 1.0, float("nan"), float("inf"), -float("inf"), complex(1), "1", None):
        reject("scalar "+repr(value), lambda value=value: m.exact(value))
    for bad in ([], (), [1], [Fraction(0)]*16, tuple([0]*16), tuple([Fraction(0)]*15), tuple([Fraction(0)]*17)):
        reject("MQ coefficients "+repr(bad), lambda bad=bad: m.MQ(bad))
    for value in (True, False, 0, -1, Fraction(3), 3.0, float("nan"), "3"):
        reject("repetition "+repr(value), lambda value=value: m.positive_integer(value))
    for value in ([], (), [(0,0),(1,1)], [(0,0)]*3, [(0,0),(1,0),(True,1)], ((p, 0) for p in range(3))):
        reject("polygon "+repr(value), lambda value=value: m.polygon(value))
    for value in (0, -1, Fraction(-1,2), True, 1.0, float("nan"), float("inf")):
        reject("radius "+repr(value), lambda value=value: m.invert_polygon([(0,0),(1,0),(0,1)], m.exact(2), value))
    reject("zero inversion denominator", lambda: m.invert_polygon([(0,0),(1,0),(0,1)], 0))
    reject("zero divisor", lambda: m.exact(0).inverse())
    reject("guard integer truthy", lambda: m.require(1, "x"))
    reject("guard false optimized", lambda: m.require(False, "x"))
    reject("field truthiness", lambda: bool(m.exact(1)))
    reject("empty ledger", lambda: m.Ledger().finish())
    reject("unknown ledger", lambda: m.Ledger().check("not-real", True))
    reject("false ledger", lambda: m.Ledger().check("arithmetic_basis", False))
    reject("unsupported square root", lambda: m.sqrt_rational(7))
    reject("zero square root", lambda: m.sqrt_rational(0))
    reject("negative square root", lambda: m.sqrt_rational(-1))
    # Deliberately too close to sqrt(2) for the bounded enclosure oracle.
    from math import isqrt
    q = 1 << 5000
    nearly = m.basis(1)-Fraction(isqrt(2*q*q),q)
    reject("finite sign budget unresolved", nearly.sign)
    changed = m.fixed_controls()[0]
    points = list(changed["vertices"])
    points[1] = (points[1][0]+Fraction(1,1000), points[1][1])
    reject("perturbed physical vertex", lambda: m.validate_orbit(points, 3, 8, 5, Fraction(40,9), m.Ledger()))
    reject("wrong caustic", lambda: m.validate_orbit(m.fixed_controls()[0]["vertices"],3,8,5,Fraction(40,13),m.Ledger()))
    # Independent sparse-basis multiplication and inverse sanity checks over all basis pairs.
    basis_checks = 0
    for i in range(16):
        for j in range(16):
            factor = 1
            for bit, prime in enumerate((2,3,5,13)):
                if i & j & (1 << bit):
                    factor *= prime
            if m.basis(i)*m.basis(j) != factor*m.basis(i ^ j):
                raise RuntimeError("basis multiplication failure")
            basis_checks += 1
    for i in range(1,16):
        x = 1+m.basis(i)/17
        if x*x.inverse() != 1:
            raise RuntimeError("inverse failure")
    result = {"status":"PASS", "source_sha256":PIN, "python":sys.version, "flags":repr(sys.flags), "rejections":results, "basis_pair_checks":basis_checks,"mixed_inverse_checks":15,"write_guard":"audit output only"}
    (output / "results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":"PASS","rejections":len(results),"basis_pairs":basis_checks,"mixed_inverses":15,"output":str(output)}))


if __name__ == "__main__":
    main()
