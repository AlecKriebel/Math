#!/usr/bin/env python3
"""Fresh literal Section 8 matrix bridge; requires SymPy, no project imports."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sympy as s

I = s.eye(2)
X = s.Matrix([[0,1],[1,0]])
Z = s.diag(1,-1)
J = X*Z
Y = s.I*J
letters = {"I": I, "X": X, "Y": Y, "Z": Z, "J": J}

def word(w):
    return s.kronecker_product(*(letters[c] for c in w))

def zero(a):
    return all(s.expand(x) == 0 for x in a)

rt2 = s.sqrt(2)
M = (-word("ZIZZ")-word("ZIJJ")-word("JIZJ")+word("JIJZ"))/2
E = word("XIXX")
aa, bb = -s.I*rt2*M, s.I*E
uk, vk = (aa+aa*bb)/2, (aa-aa*bb)/2
u, v = s.I*word("IZZI"), s.I*word("XIXX")
S = s.Matrix([
    [2+rt2, -s.I*rt2, s.I*rt2, 2-rt2],
    [rt2, s.I*(2+rt2), s.I*(2-rt2), -rt2],
    [-(2-rt2), -s.I*rt2, s.I*rt2, -(2+rt2)],
    [-rt2, s.I*(2-rt2), s.I*(2+rt2), rt2],
])/4
swap = s.zeros(16)
for a in range(4):
    for b in range(4):
        swap[4*b+a,4*a+b] = 1
ss = s.kronecker_product(S,S)
frame = swap*ss

def C(t):
    return (frame.conjugate().T*t*frame).applyfunc(s.expand)

checks = {}
checks["S_unitary"] = zero(S.conjugate().T*S-s.eye(4))
checks["U_bridge"] = zero(C(u)-uk)
checks["V_bridge"] = zero(C(v)-vk)
checks["UV_bridge"] = zero(C(u*v)-uk*vk)
checks["U_square"] = zero(uk*uk+s.eye(16))
checks["V_square"] = zero(vk*vk+s.eye(16))
checks["UV_product"] = zero(uk*vk-bb)
r0k = (s.eye(16)+uk+vk+uk*vk)/2
witness = (word("YIYY")-word("YIYZ")+word("YIZY")-word("YIZZ")
           -word("ZIYY")+word("ZIYZ")-word("ZIZY")+word("ZIZZ"))/(2*rt2)
checks["standard_frame_non_Clifford_witness"] = zero(r0k*word("XIII")*r0k.conjugate().T-witness)
assert all(checks.values()), checks
print(json.dumps({
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "sympy_version": s.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks": checks,
    "all_passed": True
}, indent=2))
