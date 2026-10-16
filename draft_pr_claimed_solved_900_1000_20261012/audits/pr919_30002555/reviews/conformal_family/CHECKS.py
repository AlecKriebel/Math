#!/usr/bin/env python3
"""Bounded exact arithmetic and immutable-source controls; not a proof checker."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
AUDIT_ROOT = HERE.parents[1]
EXPECTED_HEAD = "704685791ec0053dc0a52590fdef49ed4aae61d9"
EXPECTED_PROOF = "78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464"

def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

snapshot = json.loads((AUDIT_ROOT / "ORIGINAL_SNAPSHOT.json").read_text())
mismatches = [name for name, digest in snapshot["files"].items()
              if sha256((AUDIT_ROOT / "original" / name).read_bytes()).hexdigest() != digest]
A = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
I = [[F(1), F(0)], [F(0), F(1)]]
AT = [list(row) for row in zip(*A)]
B = [[3, -4], [4, 3]]
B2 = mul(B, B)
cayley_hamilton = all(B2[i][j] - 6 * B[i][j] + 25 * I[i][j] == 0 for i in range(2) for j in range(2))
orthogonal = mul(AT, A) == I
determinant_one = A[0][0] * A[1][1] - A[0][1] * A[1][0] == 1
u = [2, 6]
for n in range(1, 40):
    u.append(6 * u[-1] - 25 * u[-2])
trace_mod5_control = all(x % 5 == 1 for x in u[1:])
proof = AUDIT_ROOT / "original/unsolved_math_prioritization/attempts/30002555/public/PROOF.md"
out = {
    "description": "Exact controls only; universal arguments are in AUDIT.md and INDEPENDENT_DERIVATION.md.",
    "expected_head_matches_snapshot": snapshot["head"] == EXPECTED_HEAD,
    "original_count": len(snapshot["files"]),
    "original_mismatches": mismatches,
    "proof_sha256": sha256(proof.read_bytes()).hexdigest(),
    "proof_hash_matches": sha256(proof.read_bytes()).hexdigest() == EXPECTED_PROOF,
    "A_transpose_A_identity": orthogonal,
    "det_A_one": determinant_one,
    "B_cayley_hamilton": cayley_hamilton,
    "bounded_trace_mod5_control_n1_to40": trace_mod5_control,
    "infinite_order_proof": "For every n>=1, the recurrence gives u_n=1 mod5 by induction; A^n=I would give u_n=2*5^n=0 mod5. Negative exponents reduce to positive ones.",
    "independent_infinite_order_proof": "If lambda=(3+4i)/5 were a root of unity, lambda+lambda^-1=6/5 would be a rational algebraic integer, contradiction."
}
assert len(snapshot["files"]) == 27 and not mismatches
assert all((snapshot["head"] == EXPECTED_HEAD, out["proof_hash_matches"], orthogonal, determinant_one, cayley_hamilton, trace_mod5_control))
(HERE / "CHECK_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
