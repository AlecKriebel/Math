"""Fresh sparse cubic audit, written without importing submission verifiers.

Arithmetic is rational polynomial arithmetic; Pauli multiplication is obtained
from the binary rule (X^x Z^z)(X^u Z^v)=(-1)^(zu)X^(x+u)Z^(z+v).
This finite check does not prove localization, minimum dimension or topology.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import hashlib
import json

BITS = {"I": (0, 0), "X": (1, 0), "Z": (0, 1), "J": (1, 1)}
LETTERS = {v: k for k, v in BITS.items()}


def multiply_word(a, b):
    sign, out = 1, []
    for p, q in zip(a, b):
        x, z = BITS[p]
        u, v = BITS[q]
        sign *= (-1) ** (z * u)
        out.append(LETTERS[x ^ u, z ^ v])
    return sign, "".join(out)


def product(a, b):
    out = defaultdict(F)
    for (w, x, y), c in a.items():
        for (v, u, t), d in b.items():
            sign, word = multiply_word(w, v)
            out[word, x + u, y + t] += sign * c * d
    return {k: v for k, v in out.items() if v}


def linear(*items):
    out = defaultdict(F)
    for scalar, terms in items:
        for k, v in terms.items():
            out[k] += scalar * v
    return {k: v for k, v in out.items() if v}


M = {("ZIZZ", 0, 0): F(-1, 2), ("ZIJJ", 0, 0): F(-1, 2),
     ("JIZJ", 0, 0): F(-1, 2), ("JIJZ", 0, 0): F(1, 2)}
E = {("XIXX", 0, 0): F(1)}
assert product(M, M) == {("IIII", 0, 0): 1}
assert product(E, E) == {("IIII", 0, 0): 1}
assert not linear((1, product(M, E)), (1, product(E, M)))
H = {(w, 1, 0): v for (w, _, _), v in M.items()}
H["XIXX", 0, 1] = F(1)
H1 = {(w + "II", x, y): v for (w, x, y), v in H.items()}
H2 = {("II" + w, x, y): v for (w, x, y), v in H.items()}
residual = linear((1, product(product(H1, H2), H1)),
                  (-1, product(product(H2, H1), H2)),
                  (F(-1, 3), H1), (F(1, 3), H2))

expected = {}


def group(words, coeffs):
    for word in words.split():
        for (a, b), coeff in coeffs.items():
            expected[word, a, b] = coeff


group("IIJIJZ JIZJII ZIJJII ZIZZII", {(1, 2): F(-1, 2), (1, 0): F(1, 6)})
group("IIJIZJ IIZIJJ IIZIZZ JIJZII", {(1, 2): F(1, 2), (1, 0): F(-1, 6)})
group("IIXIXX", {(2, 1): F(-1), (0, 3): F(1), (0, 1): F(1, 3)})
group("XIXXII", {(2, 1): F(1), (0, 3): F(-1), (0, 1): F(-1, 3)})
group("JIJZXX JIZJXX XIJXZJ ZIZZXX", {(3, 0): F(1, 2), (1, 2): F(-1)})
group("XIJXJZ XIZXJJ XIZXZZ ZIJJXX", {(3, 0): F(-1, 2), (1, 2): F(1)})
assert residual == expected
assert len({key[0] for key in residual}) == 18

# Trace(P)=8 and either partial trace(P)=2 I follow termwise: each
# four-letter reflection word is nonidentity in both two-qubit sites.
assert all(w[:2] != "II" and w[2:] != "II" for w, _, _ in H)

# The finite-image proof's determinant calculation depends only on the
# multiplicities. Exponents are reduced modulo six for q and modulo three
# for kappa=q^2. This checks the n=2 boundary and the induction congruence.
assert 8 % 6 == 2
assert all(pow(4, n - 2, 3) == 1 for n in range(2, 101))

# Independently reduce the universal norm identity as a rational polynomial
# in eta for c=1/3, using the trace moments derived in the referee notes.
c = F(1, 3)
quadratic = 1 + c - 2 * c
linear_coefficient = -c + c*c
assert quadratic == 1-c and linear_coefficient == -(1-c)*c
norms = {str(eta): str((1-c)*eta*(eta-c)) for eta in (F(1,3), F(1,2), F(2,3))}
assert norms["1/3"] == "0" and norms["1/2"] == "1/18"

source = Path(__file__).resolve().parents[1] / "manuscript" / "main.tex"
report = {
    "description": "Task-specific fresh exact finite audit; no submission verifier imported",
    "manuscript": str(source),
    "manuscript_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "reflection_square_and_anticommutation": "PASS",
    "complete_cubic_table_exact_equality": "PASS",
    "cubic_residual_support": 18,
    "two_partial_trace_termwise_vanishing": "PASS",
    "determinant_congruence_n2_through_n100": "PASS (induction supplied in review)",
    "universal_T_squared_norms": norms,
    "residual": {w: {f"alpha^{a} beta^{b}": str(coef)
                       for (word, a, b), coef in sorted(residual.items()) if word == w}
                 for w in sorted({k[0] for k in residual})},
    "limits": "No all-n theorem is inferred from finite computation. No novelty certification."
}
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "residual"}, indent=2))
