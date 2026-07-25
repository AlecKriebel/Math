# Verification

## Commands

```text
/usr/bin/python3 verify_companion_infinity_sympy.py
./verify_companion_infinity_pari_strict.sh
./test_companion_infinity_guards.sh
/usr/bin/python3 audit_hostile/audit_orbits_and_gauges_sympy.py
./audit_hostile/verify_resonance_pari_strict.sh
./audit_hostile/test_resonance_fail_closed.sh
```

The SymPy certificate covers every orbit, including the enlarged
\(t=-2\) resonance kernel and its full lower compatibility tree.  The
primary PARI/GP and clean-room audit reconstruct the outer and nonresonant
finite charts, all orbit endpoints, gauges, special ranks, and forcing
minors.  The hostile PARI/GP backend independently reconstructs the
resonance raw kernel, polynomial \(E_6\) compatibility, constant-rank
converse, and \(K=0/K\ne0\) degree-five split.

The scripts use exact arithmetic.  They provide evidence about the encoded
algebra and do not constitute peer review.
