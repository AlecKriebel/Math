# Verification

## One-command replay

From this directory, run

```sh
./verify_all_strict.sh
```

The aggregate runner executes the complete primary certificate, both
independent PARI/GP reconstructions, the external hostile reconstruction,
every exact-transcript guard, and all fault-injection tests. It exits
nonzero unless every component finishes and prints its required final
marker.

The replayed environment on 2026-07-25 used Python 3.9.6, SymPy 1.14.0,
and PARI/GP 2.17.4.

## Primary exact certificate

```sh
./verify_rankone_triple_sympy_strict.sh
./test_fail_closed.sh
```

`verify_rankone_triple_sympy.py` reconstructs:

- the raw \(36\times26\) \(E_7\) matrix, its rank-eight minor, its full
  nullspace, and the four-dimensional legal gauge space;
- the complete \(E_6\) compatibility system;
- every \(A=0\) branch, including fresh origin, \(xz\), and \(xy\)
  rank drops;
- the repaired \(A=0,w_3\ne0,D\ne0\) split: the \(a_3\ne0\) completeness
  minor \(648a_3^4\), and the freshly rebuilt \(a_3=0\) minor
  \(2048s^8/81\);
- the scalar normalization and every \(A\ne0\) factor/resonance chart.

The strict wrapper compares the entire transcript with a fixed expected
transcript. The fault guard corrupts the raw \(E_7\) minor, a plus-resonance
square, the repaired \(a_3=0\) minor, and the final attestation. It also
requires optimized Python (`-O`) to be rejected so assertions cannot be
silently disabled.

## Independent \(A=0\) reconstruction

```sh
./verify_a0_pari_strict.sh
./test_a0_pari_fail_closed.sh
```

`verify_a0_pari.gp` rebuilds the weighted Jacobian determinant directly in
PARI/GP; it does not import or call the SymPy program. It deliberately uses
the opposite monomial-equation order. In particular, it verifies:

- the complete \(w_3\ne0\) tail by exact augmented-rank minors;
- \(D=0\), \(D\ne0,a_3\ne0\), and a fresh
  \(D\ne0,a_3=0\) reconstruction;
- the \(q\)-preserving source shear and the legal source-translation/free-
  \(V\)-tail gauge identity used to reach the \(xz\) axis;
- the origin \(a_3=0/a_3\ne0\) split;
- every \(xz\) augmented-minor and \(C_7\) rank-drop chart;
- every \(xy\) tail chart, both \(E_4\) factors, and all lower descendants.

Because of the reversed equation order, PARI finds an \(s^8\) pivot already
on the symbolic-\(a_3\) chart; it nevertheless discards that solve and
rebuilds \(a_3=0\) separately. This is methodologically independent of the
primary \(a_3^4\)-localized solve.

The fault guard changes an \(xz\) augmented minor, an \(xz\) \(E_4\)
residual, the repaired \(a_3=0\) pivot, the \(G=0\) remainder identity, and
the final attestation. Every mutation must be rejected.

## External hostile replay

```sh
./audit_hostile_external/verify_a0_external_pari_strict.sh
./audit_hostile_external/test_fail_closed.sh
```

The hostile audit starts again from the raw \(E_7\) matrix and does not
import either supplied verifier. It found the hidden
\(D\ne0,a_3=0\) completeness gap in the provisional primary certificate,
rebuilt that rank drop with independent \(s^8\) pivots, and corrected the
axis-gauge explanation to source \(x\)-translation plus free-\(V\)-tail
relabeling. It also independently closes every \(xz\) and \(xy\) rank drop.
Seven hostile mutations are rejected. The final scoped verdict is **PASS**
in [`audit_hostile_external/REPORT.md`](audit_hostile_external/REPORT.md).

## Independent \(A\ne0\) reconstruction

```sh
./aopen_independent/verify_aopen_pari_strict.sh
./aopen_independent/test_fail_closed.sh
```

This PARI/GP program independently rebuilds the normalization \(A\mapsto1\),
the four-factor cover, the \(s=0\) branch, the equal branch, both resonances,
and every zero divisor of a localized pivot. Its local proof and coverage
ledger are in
[`aopen_independent/NOTE.md`](aopen_independent/NOTE.md).

## Supplementary checks

The following smaller scripts isolate the formerly delicate \(A\ne0,w_3=0\)
leaves:

```sh
/usr/bin/python3 verify_w3zero_leaves_sympy.py
/opt/homebrew/bin/gp -q verify_w3zero_leaves_pari.gp
```

They are supplementary and are not counted as the two primary independent
full-branch checks.

## Verification limits

All arithmetic is exact. No numerical sampling is used as a proof step.
The strict wrappers reject PARI diagnostics even where the `gp` process
itself might return status zero after an internal parser or algebra error.

These programs verify the polynomial identities and branch certificates
they encode. They do not constitute peer review, certify the prose against
all possible transcription errors, or guarantee worldwide priority.
