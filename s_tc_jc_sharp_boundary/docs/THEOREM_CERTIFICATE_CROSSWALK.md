# Theorem–certificate crosswalk

Status labels refer only to the active sharpness manuscript.

| Manuscript item | Mathematical role | Primary implementation | Independent implementation | Status |
|---|---|---|---|---|
| Proposition 3.1 | Binary/LSA/tree-child base rootings; level 2; `W_TC \ S_TC`; labelled nonisomorphism; non-`T` | `reproducibility/verify_primary.py` graph checks | `reproducibility/independent/verify_sharpness.py`, graph audit and exhaustive rooting census | **PROVED / EXACTLY COMPUTED** |
| Proposition 4.1 | Six identities on both full symbolic JC maps | `check_invariants` derives every displayed-tree coordinate and expands each pullback | independent sparse-polynomial Fourier maps | **EXACTLY COMPUTED** |
| Lemma 4.2 | Common irreducible localized locus, dimension at most eight, smooth positive sheet | reconstruction formulas and derivative check; algebraic proof in manuscript | independent invariant upper-bound and irreducibility audit | **PROVED** |
| Equations (14)–(18) | Strict algebraic common point in `Theta_0` | exact SymPy algebraic-number isolation and 14-orbit check | custom rational interval arithmetic and custom `Q(beta)` field | **PROVED / EXACTLY COMPUTED** |
| Equations (19)–(20) | Rank-eight lower certificates | symbolic determinant derivation and factor comparison | automatic differentiation plus two independent exact determinant algorithms | **EXACTLY COMPUTED** |
| Proposition 5.1 | Equality of complete distributions and regular full-dimensional overlap | all 256 Fourier coordinates plus inverse-transform orthogonality | all 256 Fourier and all 256 pattern coordinates; strict pattern positivity | **PROVED** |
| Corollary 5.2 | Ambiguity occupies a Euclidean-open parameter set and is not algebraically exceptional | rank/submersion check | independent inverse-function audit | **PROVED** |
| Lemma 6.1 | Positive analytic inverse for cherry substitution; exactly two added dimensions | formula proof in manuscript | exact one-step check on all 1,024 five-leaf coordinates plus structural inverse proof | **PROVED** |
| Theorem 1.1 | Pair exists for every `n >= 4`, dimension `2n`, topology properties persist | induction from Lemma 6.1 | quantified structural proof; finite `4 <= n <= 12` checks used only as mutation regressions | **PROVED** |

## Independent certificate lock

The active independent implementation imports only the Python standard
library and shares no code with the primary verifier.  Its canonical output
is `reproducibility/independent/expected_certificate.json`, SHA-256:

```text
38266537a7966d83bdb94c6fb90fa68f93fbd227b82579f1bf311005925366d7
```

The full adversarial review, including failed mutations and convention
warnings, is preserved at `repair/reviews/SHARPNESS_GATE_REVIEW.md`.

## Explicit nonclaims

No row certifies generic identifiability within `S_TC`, a finite local atlas,
one-sided containment, bridge-tree reconstruction, K2P, or K3P.  Those claims
belonged to the withdrawn positive release and remain outside the active
paper.
