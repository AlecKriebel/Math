# Verification record

**Recorded:** 2026-07-25T07:49:45Z.

The theorem is encoded independently in SymPy and PARI/GP.

## Commands

```text
/usr/bin/python3 -u verify_resonance_c3_sympy.py
./verify_resonance_c3_pari_strict.sh
./test_fail_closed.sh
```

## Exact checks

Both backends reconstruct:

- \(\operatorname{Jac}(P,Q,R)=0\) and the compact \(E_7\) identity;
- the raw \(36\times26\) \(E_7\) matrix, rank \(14\), and constant maximal
  minor \(-1039973956284579840\);
- twelve explicit kernel directions, independence minor \(49152\), and the
  four-coordinate gauge determinant \(-36\);
- four staged, literal, division-free \(E_6\) coefficient combinations
  forcing \(g=f=C=0\) and \(D=-2e\);
- cleared polynomial left-kernel pairings that independently reproduce the
  four \(E_6\) compatibility squares;
- the surviving rank-eight \(E_6\) system, constant minor \(5159780352\),
  complete six-parameter solve, and direct converse;
- the \(E_5\) column determinant
  \(-96(-6A+3B+48e+16w)\);
- the resonant rank-four \(E_5\) solve with constant minor \(20736\); and
- the two exact \(E_4\) pivots
  \(\frac{16}{3}\ell_{32}(3e^2-\ell_{33})\) and
  \(\frac{16}{3}\ell_{32}^2\).

The strict PARI wrapper supplies a 128 MB stack and accepts only the exact
one-line success sentinel.

## Fail-closed checks

The harness verifies:

- optimized Python is rejected;
- a forged SymPy raw maximal minor is rejected;
- a forged PARI \(E_4\) pivot is rejected;
- the strict PARI baseline succeeds; and
- an extra forged PARI diagnostic is rejected.

## Hostile reconstruction

At 2026-07-25T09:55:40Z, the separate verifier in `audit_hostile/`
reconstructed the theorem from the full determinant with reversed
coefficient and variable orders. It confirmed:

- raw \(E_7\) rank \(14\), nullity \(12\), the complete legal gauge, and
  the normal complement;
- the same constant \(E_6\) rank-eight minor \(5159780352\) before and
  after every staged compatibility condition;
- augmented ranks \(9,9,9,9,8\), proving that the four displayed square
  conditions are the complete successive compatibility locus;
- the rank-two floor and constant rank-four resonance pivot in \(E_5\);
- both terminal \(E_4\) coefficients and the exact \(c=\pm3\) orbit
  symmetry.

The hostile strict wrapper and four mutation tests pass. See
`audit_hostile/REPORT.md` for the scoped PASS verdict.

## Independence and limitations

SymPy and PARI/GP construct the determinant and coefficient systems
separately. Both also check the literal sparse coefficient combinations,
while the left-kernel reconstruction is retained as adversarial redundancy.
They remain computer-algebra checks of the same encoded theorem, not peer
review.

The artifacts were developed with AI assistance. Exact execution is evidence
about the encoded identities and is not a substitute for expert review.
