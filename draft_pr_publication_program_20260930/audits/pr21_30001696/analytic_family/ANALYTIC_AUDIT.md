# PR 21 analytic-family audit

**Verdict: the assigned universal analytic mechanism passes.** For every
`d >= 2` and `0 <= i <= d-2`, the frozen candidate constructs a
semialgebraic homeomorphism from the bounded-switch realization to
`S^i x D^(d-i-1)`. The endpoint `i=d-1` and `d=1,i=0` have the immediate
whole-sphere descriptions and do not use the ratio construction. No analytic
counterexample, circularity, or unsupported local extension was found.

This verdict does not certify historical priority, novelty, refereeing, or
the separate semialgebraic-to-PL transfer. Those require the other audit
families and the root's reconciliation. The candidate conclusion was treated
as a hypothesis throughout this family, not inferred from the saved review
or finite test results.

## Independence and exact input

The exact audited input is frozen PR head
`096aacd71a1dc6dd3a73bea3c1055877dc8c0451`, problem 30001696, proof SHA-256
`58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305`.
The universal first pass was sealed before reading historical diagnostics,
historical review, or root/sibling conclusions. Its timestamp, input ledger,
and hash are in `first_pass_seal.json`; the mathematical audit is
`FIRST_PASS_SEALED.md`, SHA-256
`ff60fd704c7f9579a856ea7d28c5be64827535aca31b0cfdd6306785f164f455`.
I did not subsequently rewrite that sealed argument.

All writes stayed in `analytic_family/`. Frozen scripts were copied unchanged
to ignored `_scratch/reproduce/` before execution. Downloaded foreign full
text also stayed in ignored `_scratch/`. No installation, branch change,
Git mutation, publication, outside communication, or new central-problem
attempt was undertaken by this family.

## Universal audit findings

The detailed independent arguments in the sealed pass cover the following
dependencies, with locators in frozen `PROOF.md`:

| Dependency | Frozen locator | Universal evidence and exact boundary checked |
|---|---|---|
| Closed set and ambient-sphere interior | Section 2, lines 37–70, (2.1)–(2.2) | Minimum completion equals `s^-`; maximum completion characterizes interior; forbidden completions perturb zeros arbitrarily slightly. Leading, trailing, long zero blocks and sparse vectors are included. The origin is excluded. |
| Polynomial spectrum and algebraic basis | Section 3, lines 72–103, (3.1)–(3.3) | Evaluation is a Vandermonde isomorphism. Monomial action is triangular with distinct diagonal `N-2k`, and rational monic eigenpolynomials follow by downward substitution. Positive binomial weights symmetrize the operator. |
| Strict TP for every positive time | Lemma 3.1, lines 105–124 | Every surviving adjacent exterior move has positive wedge sign. Moving subsets toward the initial segment proves connectedness. Positive paths in the exponential series prove every proper compound entry positive; determinant is 1. |
| Strict zero-sensitive variation | Equation (3.4), lines 126–142 | The primary theorem uses exactly `s^+(Ax) <= s^-(x)` for nonzero vectors and strict TP. The sealed audit additionally proves it directly using ordered sign-block column sums and positive cofactors. This is stronger than merely preserving `s^-`. |
| E/F separation | Section 4, lines 146–189, (4.2)–(4.3) | Interpolation at an alternating completion contradicts the polynomial degree bound. A sign-matching polynomial contradicts orthogonality for every hypothetical low-variation F vector. Neither assumes nonzero eigenvector coordinates. |
| Spectral ratio and global section | Section 5, lines 191–237, (5.1)–(5.4) | Derivative of `log R` with respect to `log a` is the difference of weighted index means in `[1,N]`, including sparse spectral support. Bounds give limits 0 and infinity, a unique orbit section, continuous inverse, and a semialgebraic graph. |
| Continuous finite positive hitting graph | Section 6, lines 239–277 | Compact E/F separation supplies uniform small/large orbit parameters. Strict trapping makes membership a lower interval with a single boundary endpoint. Interior/complement bracketing proves continuity; the boundary graph proves semialgebraicity. |
| Identity near core and product extension | Section 7, lines 279–333, (7.1)–(7.4) | A positive cutoff below the uniform minimum of beta gives monotone rescaling. `R<epsilon^N` forces the identity part in both directions. The map therefore extends across every core point with no directional limit problem. |

The most delicate dependencies admit independent mechanisms: strict variation
has a determinant proof without appealing to spectral oscillation, and F
separation has a sign-matching polynomial proof without appealing to strict
variation or the desired product. The global cross-section uses only a strict
spectral gap; the hitting graph uses only closedness, compact separation, and
strict trapping. These do not transfer the central conclusion to an equivalent
unsupported claim.

The complete parameter ledger is in the sealed pass. In particular, `i=0`
has a two-point core, `N=1` gives exactly `R=a`, and `i=d-2` has two F
directions. Neither connectedness of the section nor positive-dimensional
component spheres is assumed. Endpoint `F=0` is kept out of every division
and logarithmic ratio expression.

## Primary-source check

I read the actual primary PDFs, including the proof locators. The relevant
references are [Margaliot–Sontag, Automatica 101 (2019)](https://www.sontaglab.org/FTPDIR/margaliot_sontag_totally_positive_automatica2019.pdf),
Definition 1 p. 2, Theorem 3 / equation (10) p. 4, and Appendix Proposition 1
p. 12 / Theorem 11 pp. 12–13; and
[Schwarz, Pacific J. Math. 32 (1970)](https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf),
Theorem 3 pp. 213–214 and Theorem 4 / equation (4.1) pp. 214–215.

The terminology differs materially: Schwarz's STP is modern strict TP;
Schwarz's TP is modern TN. The candidate's own compound argument proves the
strict hypothesis. Merely entrywise positive, irreducible, or TN matrices
would not suffice, as the controls below demonstrate. Retrieved bytes,
hashes, source versions, URLs and exact locators are in `source_records.json`.

## Frozen diagnostic reproduction

Both original scripts reproduced without changes or dependency installation:

* `verify.py`, SHA-256
  `9e4aa454a9392770794f0949e857427edb237c09c98a4f740abc24dbb49b2902`,
  ran under Python 3.14.6 and passed. Its receipt reports 16,967 checks over
  the ten categories, including 2,534 positive minors and 3,270 zero-sensitive
  variation cases. The receipt is reproduced in `reproduction_results.json`.
* `review/independent_checks.py`, SHA-256
  `6f108e94a4bb6a21e0b1894fc252b64ab4766a406515e497bea4de3b1193e8b7`,
  ran under `/usr/bin/python3` 3.9.6 with SymPy 1.14.0. All 20,326 assertions
  passed, and every saved category count and assertion total matched the
  frozen `review/independent_results.json` exactly.

These are bounded finite diagnostics. They supply reproducibility evidence,
not a proof certificate for the homeomorphism or PL theorem.

## Distinct new falsification controls

The first-party `new_controls.py` adds independent exact integer/fraction
diagnostics and writes `new_control_results.json`. Its constructions differ
from the historical scripts:

* A closed zero-block formula is checked against brute-force completions in
  dimensions 1–8, including all-zero inputs solely as a domain control.
* Hilbert matrices replace the spectral flow in dimensions 2–6. Arbitrary
  signed magnitudes and sparse inputs exercise sign-block compression,
  positivity of compressed minors, and cofactor annihilation identities.
* Fresh monic rational eigenpolynomials are solved from the monomial action,
  without using the historical Krawtchouk evaluation formula, up to `N=24`.
* Sparse physical F vectors are built as barycentric Vandermonde circuits on
  every `(r+1)`-node support up to dimension 12. Their moment orthogonality
  and sharp `s^-=r` bound exercise zero blocks missed by small spectral
  coefficient grids. E cases also include repeated and between-node roots.
* All singleton E/F spectral supports, plus sparse mixed supports, are tested
  through `N=16`, including the sharp minimum and maximum gaps, exact `N=1`
  equality, and the cutoff neighborhood implication.
* Every adjacent-edge deletion disconnects each tested compound graph.
  Cutoff endpoints approach epsilon within `2^-64`, or grow to `2^64`;
  inverses and fixed neighborhoods are checked exactly, without instability
  hidden by floating-point rounding.

Eight deliberately false hypothesis mutations were detected with explicit
witnesses:

1. TN identity preserves `e_0`, for which `s^+=2>s^-=0` in dimension 3.
2. Permitting the zero input invalidates the strict theorem's domain.
3. The positive symmetric irreducible generator `J=ones_3-I_3` has
   `exp(log(2)J)=(1/2)I+(7/6)ones`. Its rows `(0,1)`, columns `(1,2)` minor
   is `-7/12`. It sends `(10,-9,-1/10)` to `(121/20,-69/20,1)`, increasing
   sign variation from one to two. This is an exact long-jump counterexample
   to replacing tridiagonality with positivity and irreducibility.
4. Cutting an adjacent edge leaves a sparse coordinate direction unchanged
   and destroys strict trapping.
5. Overlapping spectral indices make the ratio constant and destroy a unique
   section.
6. Reversing the spectral ordering makes the ratio decrease.
7. Taking beta below epsilon makes the proposed cutoff slope negative.
8. Naive rescaling `a -> a/beta(s)` can have direction-dependent core limits.
   A rationally parametrized toy section with E indices 0,1 and F index 2
   gives two sequences with the same original core direction `(1,1)` and
   different image directions `(1,1)` and `(2,1)`. Exact finite ratios and
   vanishing F/E bounds are tested. This is a necessity control for the
   cutoff, explicitly **not** a counterexample to the candidate's actual
   beta function or to `C_i`.

The saved new receipt contains the exact script hash, counts, runtime and
witnesses. The mathematical arguments, rather than these finite tests, carry
the universal analytic verdict.

## Remaining scope and recommendation

No analytic repair is required in Sections 2–7 for the stated parameter range.
The strongest independently verified result is the complete semialgebraic
sphere–ball product homeomorphism, with all coordinate zeros and parameter
edges accounted for. Promotion to a PL result remains dependent on the
separately audited Hauptvermutung and source/parameter interpretation, and
publication claims remain dependent on priority and evidence reconciliation.
The exact first-party artifacts and frozen-input preservation check are listed
in `artifact_manifest.json`.
