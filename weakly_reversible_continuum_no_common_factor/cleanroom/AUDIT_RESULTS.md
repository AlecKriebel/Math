# Clean-room audit results

Disposition: **PASS for all checklist items 1–20.**

| Item | Status | Independent certificate |
|---:|:---:|:---|
| 1 | PASS | Raw complex tuple validation; maximum degree also checked |
| 2 | PASS | Twenty raw rates checked as positive integers |
| 3 | PASS | Reverse-arc dictionary test; ten reversible pairs |
| 4 | PASS | Independent breadth-first traversal |
| 5 | PASS | Connected-component count equals one |
| 6 | PASS | Exact matrix rank; determinant witness \(-3\) |
| 7 | PASS | Field reconstructed reaction-by-reaction and compared coefficientwise |
| 8 | PASS | Quotients by \(L\), then \(Q\), derived rather than supplied |
| 9 | PASS | Conic determinant \(-256\), absolute irreducibility argument, Gröbner staircase |
| 10 | PASS | Exact rational substitution; pole and injectivity certificates |
| 11 | PASS | Exact positive-definite ellipse and positivity inequalities |
| 12 | PASS | Exact total and pairwise multivariate gcds over \(\mathbb Q\) |
| 13 | PASS | Characteristic-zero field-extension lemma |
| 14 | PASS | Zero determinant and nonzero minor \(243223374815232\) |
| 15 | PASS | Height-two prime containment plus gcd-one height exclusion |
| 16 | PASS | Residual ideal derived by saturation; intersection recomputed by elimination |
| 17 | PASS | Triangular degree-15 basis, squarefreeness, and sum ideal \((1)\) |
| 18 | PASS | Independent species-minimality proof in `PROOF_AUDIT.md` |
| 19 | PASS | Independent weighted-scaling/transversality proof in `PROOF_AUDIT.md` |
| 20 | PASS | Independent kinetic-matrix maximum-principle proof in `PROOF_AUDIT.md` |

No gap was found under the hypotheses in the finalization checklist.  The
scope qualifications are explicit in `PROOF_AUDIT.md`: the continua are
algebraic or semialgebraic; item 19 assumes one linkage class; item 20 assumes
weak reversibility and full stoichiometric rank.

## Replay output

Command:

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/cleanroom/verify_v1_cleanroom.py
```

Expected terminal line:

```text
PASS: all clean-room exact checks 1--17 succeeded
```
