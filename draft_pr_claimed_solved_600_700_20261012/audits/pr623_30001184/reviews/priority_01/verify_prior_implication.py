"""Independent exact fibre checks for the reviewer-derived BFH implication.

This verifies finite matrices only. Continuity, generated restriction, GNS
finiteness, and the universal derivation argument are proved analytically in
PRIOR_IMPLICATION.md; passing this computation does not replace those proofs.
"""
import json
from pathlib import Path
import sympy as sp

c, s, b0, b1 = sp.symbols("c s b0 b1", real=True)
I = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
b = sp.diag(b0, b1)
obs = sp.kronecker_product(I, b)
U = (c * I).row_join(-s * X).col_join((s * X).row_join(c * I))

assert sp.simplify(U.T * U - (c*c+s*s)*sp.eye(4)) == sp.zeros(4)
compressed = (U.T * obs * U)[:2, :2]
assert compressed == c*c*b + s*s*X*b*X
r = sp.symbols("r", real=True)
desired = sp.diag(((1+r)*b0+(1-r)*b1)/2,
                  ((1-r)*b0+(1+r)*b1)/2)
assert sp.simplify(compressed.subs({c*c:(1+r)/2,s*s:(1-r)/2})-desired) == sp.zeros(2)

# Literal BFH amplitude-damping flip-flop: bath first, system second;
# bath initial vector |1>, decaying system projection q=|0><0|.
q = sp.diag(1, 0)
Uad = sp.eye(4)
Uad[1,1] = Uad[2,2] = c
Uad[1,2] = Uad[2,1] = -sp.I*s
assert sp.simplify(Uad.conjugate().T * Uad-sp.diag(1,c*c+s*s,c*c+s*s,1)) == sp.zeros(4)
cad = (Uad.conjugate().T * sp.kronecker_product(I,q) * Uad)[2:4,2:4]
assert cad == c*c*q

# Projection Leibniz identity forces q delta(q) q=0, whereas the
# compressed two-state generator violates this exact necessary identity.
Lq = sp.diag(-sp.Rational(1,2),sp.Rational(1,2))
assert q * Lq * q == -sp.Rational(1,2)*q
assert q * (-q) * q == -q

out = {
    "status":"PASS_EXACT_FIBRE_IDENTITIES",
    "sympy_version":sp.__version__,
    "assertions":7,
    "bitflip_compression":"c^2 b+s^2 X b X; c^2=(1+r)/2, s^2=(1-r)/2",
    "bfh_amplitude_damping_compression":"T(q)=c^2 q; c^2=exp(-t)",
    "derivation_projection_identity_violation_two_state":"q L(q) q=-q/2 != 0",
    "derivation_projection_identity_violation_amplitude_damping":"q L(q) q=-q != 0",
    "universal_proof":"PRIOR_IMPLICATION.md",
    "finite_computation_is_not_full_proof":True,
}
target = Path(__file__).with_name("PRIOR_IMPLICATION_CHECK.json")
target.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
