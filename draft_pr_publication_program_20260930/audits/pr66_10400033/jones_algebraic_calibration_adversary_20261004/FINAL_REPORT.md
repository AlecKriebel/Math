# Independent Jones / algebraic calibration report

Eligible head: `78f4a7fadac0fd24e147a617956cb409eb6a579e`.
Family: independent exact algebraic normalization and adversarial calibration.

**Verdict within this family's scope: PASS; no mathematical counterexample
found.** No universal knot theorem is inferred from finite computations.
The mathematical/publication decision remains ROOT's.

The first assessment was sealed at `2026-10-04T16:27:36.365395+00:00` as
`FIRST_CONCLUSION.md`, SHA256
`8ffdb9498aa5f0132b5e5d65777366627e8a25d0a3010feaaac8fa89cf181395`.
Before that seal, the only original-program files read were the prescribed
authenticated candidate and source record. Primary papers and this family's
new independent code/results were the other evidence. No old verifier or
historical opinions supplied the first assessment.

## Strongest independently checked result

The fresh evaluator computes complete exact integer Laurent Jones
polynomials by Temperley–Lieb matching multiplication and a closure trace.
It independently converts signed braids to Gauss diagrams by strand
traversal. On 344 knot closure rows, representing 311 distinct
strand-count/word pairs, its derivative normalization agrees exactly with
the candidate's signed subset arrow expression. There are 265 mixed-sign
rows, 54 rows with nonzero signed P counts, strand counts 1–5, and every
diagram crossing count 0–14. Every normalized v3 is integral and obeys both
the floor target and the stated even-n refinement.

The finite corpus contains trefoils and mirrors, the figure-eight, multiple
torus knots, bounded exhaustive signed 3-braids, seeded larger signed
closures, reverse-orientation checks, both Markov stabilization signs,
RII cancellation insertion, positive and negative braid-RIII relations,
cyclic-word closure invariance, and connected sums. The connected-sum
full polynomials multiply correctly and v3 adds. Link closures are
explicitly excluded and counted as skipped, rather than treated as knots.

The primary publisher Ohtsuki source confirms the problem and normalization.
Willerton gives the derivative equation. The visually inspected PV equation
(5) supports the stated P/T direction transcription and single arrow
multiplicities. CDM's coefficient-of-subdiagrams pairing explains the
subset convention (its general construction is presented for based/long
diagrams), and CDM separately identifies PV's first degree-three formula as
unbased. The source normalization plus the trefoil calibration rules out
silently counting three cyclic T embeddings with the same coefficient.
See `FIRST_CONCLUSION.md` for the algebraic derivation and primary URLs.

## Phase two: original reproducibility and falsification controls

Only after saving that assessment, I read and preserved the original
`verify_jones.py` (3567 bytes, SHA256
`6c07deb50ce2054b935a7132ecace73439316c884c23f3dcaa10bbe24bc07205`).
The byte-for-byte replay in this family's own directory passes with
59 diagrams / 183 assertions. Its mechanism is a crossing-state
enumeration with a truncated derivative expression, materially different
from the fresh complete-polynomial Temperley–Lieb multiplication.

The original and fresh models agree on all 311 distinct fresh examples,
through 14 crossings. Gauss endpoints, signed PV values, and independent
Jones v3 agree. This comparison is post-seal corroboration, not evidence
that generated the first conclusion.

Executed false-convention controls produce concrete discrepancies:

| False convention | Witness | Wrong value | Correct value |
| --- | --- | ---: | ---: |
| Three cyclic T embeddings, coefficient 1 | right trefoil | 3 | 1 |
| P coefficient 1 instead of 1/2 | 3-braid (-2,-1,-2,-1) | -2 | -1 |
| Ignore crossing signs | figure-eight | 2 | 0 |
| Reverse one T arrow in the pattern | right trefoil | 0 | 1 |

An additional boundary control shows that a formal P diagram with three
positive signs evaluates to 1/2. It is not classically realizable: its
chord intersection degrees are (2,1,1), violating the even-intersection
condition for a planar immersed circle. Thus integrality on arbitrary
formal/virtual arrow diagrams is a false extension. The candidate correctly
avoids making that extension; this is not a candidate counterexample.

For even n=2k, the refinement's right side is k(k-1)(k+1)/3, hence an integer.
The finite boundary table also checks n=0,2,4,...,14, including n=8 where
the refinement is 20 while the original target floor is 21. Negative n
does not describe a crossing count and is outside the claim.

## Evidence and limits

`independent_results.json` preserves every successful fresh row's full Jones
coefficients and signed/unsigned arrow counts. `phase_two_results.json`
preserves the cross-model comparisons and convention witnesses.
`boundary_results.json` records scope/rounding controls. `receipts/`
records actual subprocess argv, PID, cwd, UTC start/end, exit code, and
stdout/stderr body paths with hashes. `source_manifest.json` locks the
authenticated inputs and private source PDFs. Copyrighted source copies,
renderings, and long source-extraction bodies are outside the repository.

There was one fresh-code execution failure, corrected before successful
evaluation: Python exponentiation by a negative writhe produced a floating
point sign. Integer parity fixes it. The failed receipt remains. A failed
Pillow source crop was replaced by native pdftoppm cropping. One mistaken
arXiv link click opened an unrelated FAQ; it supplied no evidence. These
execution events do not create unreported mathematical discrepancies.

This family has not independently re-proved PV's imported all-classical-knots
theorem, audited historical novelty, or decided publication readiness.
Finite agreement cannot establish a universal arrow/Jones bridge; that
bridge rests on the genuine primary theorem and its correctly matched
conventions. No new central proof search was undertaken. No shared
native/original/Git/index/ref/PR/editor/Zenodo/Sheets files or state were
modified. No outside human was contacted. The original 1/5 program ledger
is preserved.

Assigned audit completion estimate: **100%**. This percentage concerns this
family's requested calibration audit, not discovery or overall-program
completion.
