# Theorem and artifact crosswalk

**Audit date:** 9 August 2026

**Revision baseline for historical line anchors:**
`9cc4d0da42d2c2aea0f5cc5e4d7754ae0350878d`

This inventory was rebuilt from the TeX sources of all three preserved
standalone manuscripts. Stable labels are controlling; historical line
numbers are navigational. “Subsumed” means that the canonical manuscript
contains a result with at least the same mathematical scope, not merely a
citation. Priority status is recorded separately from inclusion status so
that restoration of an internal theorem is not mistaken for a new lead
claim.

## Exact-value manuscript

Source: `cyclic_bell_tsirelson_bound/main.tex`.

| ID | Source item and historical lines | Canonical disposition | Canonical location and priority boundary |
|---|---|---|---|
| EX-01 | Introduction/source benchmark, lines 89--135 | Retained and attribution-corrected. The source's proved \(d\sqrt2\) upper bound, all-dimensional strategy of value \(M_d\), conjecture of equality, and NPA evidence through \(d=6\) are now distinct statements. | Introduction and contribution table. All four source items are **established prior art**. |
| EX-02 | Sharp commuting-operator bound, `thm:main`, lines 136--165 | Retained and hardened with the bicommutant and strong-limit closure argument. | `thm:exact`. The exact \(M_d\) bound is **plausibly new**; \(q=qa=qc\) is a **new strengthening**. |
| EX-03 | Polar positive-factor identity, `lem:polar`, lines 178--230 | Strengthened to use the canonical partial isometry, support projections, \(\mathcal A''\), and commutants without a unitary extension or tensor-factor assumption. | `lem:polar`. Polar decomposition itself is an established tool; no stand-alone priority claim is made. |
| EX-04 | Sharp scalar bound and equality set, `lem:scalar`, lines 240--303 | Retained unchanged in substance. | `lem:scalar` and Appendix `app:scalar`. No stand-alone priority claim for the elementary extremum. |
| EX-05 | Functional-calculus reduction and exact positive gap, lines 305--393 | Retained and used as the input to the finite-dimensional support theorem. | `thm:exact` and `eq:global-certificate`. |
| EX-06 | Self-contained Weyl/polar lower certificate, `prop:lower`, lines 394--537 | Retained, including order-\(d\) and full-spectrum checks. | Appendix `app:attainment`. The source already supplied the canonical attaining strategy; this is exact re-verification. |
| EX-07 | Source Fourier identification and explicit \(d=3\) formula, lines 538--563 | Restored with the source coefficient DFT and the transpose/conjugation conventions explicit. | `eq:source-fourier` and Appendix `app:attainment`. This identifies the source and polar observables; it is not a claim to have invented the source observable. |
| EX-08 | Augmented-value corollary, `cor:barred`, lines 568--600 | Retained for \(q\), \(qa\), and \(qc\). | `cor:first-augmented`. |
| EX-09 | Exact radical table for \(d=2,\ldots,6\), lines 607--620 | Restored with decimals and the source NPA comparison. | `tab:exact-values`. Exact benchmark, not a separate lead novelty claim. |
| EX-10 | Verification, priority, attribution, and disclosure, lines 624--end | Subsumed by the unified verifier, priority audit, source comparison, AI disclosure, and immutable historical package. | Verification and audit directories. |

## First-family randomness manuscript

Source: `cyclic_randomness_counterexample/manuscript.tex`.

| ID | Source item and historical lines | Canonical disposition | Canonical location and priority boundary |
|---|---|---|---|
| RC-01 | Definitions, printed Conjecture 2, and normalization/scope remark, lines 91--168 | Restored precisely. For the displayed operator, \(\max\overline{\mathcal I}_d=M_d+1\); the constructed maximizer refutes the normalized scalar implication for every \(d\ge4\). The source's fixed-canonical-behavior calculation is explicitly untouched. | `rem:normalization`, Section `sec:randomness`, and Appendix `app:conventions`. Family-specific scalar counterexample is **plausibly new**; the general scalar/full-data distinction is prior art. |
| RC-02 | Nonuniform exact maximizers, `thm:main`, lines 169--187 | Retained with the all-dimensional guessing lower bound and uniform local marginals. | `thm:biased`. **Plausibly new** for this family. |
| RC-03 | Value-conditioned guessing corollary, `cor:value`, lines 188--215 | Strengthened to the model-indexed quantities \(G_{\mathrm{val}}^q\), \(G_{\mathrm{val}}^{qa}\), and \(G_{\mathrm{val}}^{qc}\). | `eq:gval-model` and `eq:value-conditioned`. Only a lower bound on the worst-case guessing supremum is claimed. |
| RC-04 | Polar identity, scalar equality lemma, and exact gap, lines 239--351 | Subsumed by the stronger arbitrary-Hilbert-space exact-value section. | `lem:polar`, `lem:scalar`, and `eq:global-certificate`. |
| RC-05 | Every root ordering is a maximizer, lines 353--446 | Strengthened to a conditional polar-linear permutation theorem, then specialized with exact product hypotheses. | `thm:permutation` and `eq:first-strategy`. Sufficient orbit only; no complete maximizing-face classification. |
| RC-06 | Bell-visible first harmonics ignore root order, lines 447--493 | Retained, including all displayed correlators. | `eq:visible-correlators` and `thm:permutation`(iii). |
| RC-07 | Target DFT, Parseval identity, final-two swap, and quantitative bias, lines 494--580 | Retained. | `eq:q-sequence`--`eq:R2` and `thm:biased`. |
| RC-08 | Exhaustive \(d=2,3\) permutation-flat remark, lines 581--595 | Retained as a limitation, not promoted to rigidity or a value-only randomness theorem. | Paragraph following `thm:biased`. |
| RC-09 | Exact \(d=4\) cyclotomic table and \(G=3/32\), lines 596--659 | Retained; the displayed trivial-Eve entropy \(5-\log_2 3\) is explicit. | Appendix `app:d4` and `eq:d4-entropy`. It does not determine the optimized worst-case value. |
| RC-10 | Scalar refutation, behavior nonuniqueness, and endpoint robustness, lines 660--720 | Retained and narrowed. Self-testing language is limited to behavior-level nonuniqueness; the robustness quantifier is “deficit at most \(\varepsilon\).” | `cor:behavior-nonunique` and the endpoint-robustness corollary. |
| RC-11 | Reflection-product rank lemma, `lem:reflection`, lines 726--756 | Restored after independent exact-rank replay. | `lem:reflection-rank`. **Restored historical/internal result**, not a new lead claim. |
| RC-12 | Equal supported multiplicities and divisibility, `prop:multiplicity`, lines 758--908 | Restored as a main theorem with a full appendix proof. Scope is finite-dimensional tensor-product exact maximizers of the first augmented family only. | `thm:support-rigidity` and Appendix `app:rigidity-proof`. **Restored historical/internal result**; no \(qa\), \(qc\), approximate, Weyl-rigidity, or self-testing extension is asserted. |

## Permutation-blind and setting manuscript

Source: `minimum_bell_randomness/manuscript.tex`.

| ID | Source item and historical lines | Canonical disposition | Canonical location and priority boundary |
|---|---|---|---|
| MB-01 | Framework, private conditional states, and one-input theorem, lines 99--163 | Retained; necessity language now refers to device-independent forcing against every compatible realization. | Framework and `prop:one-input`. Standard prior-art baseline. |
| MB-02 | Explicit local model and coherent Eve flag, lines 164--207 | Retained in full. | Proof of `prop:one-input`. Self-contained replay, no novelty claim. |
| MB-03 | General polar-linear factor and permutation theorem, lines 208--376 | Subsumed and strengthened by the kernel-safe conditional theorem. | `lem:polar` and `thm:permutation`. |
| MB-04 | Exact randomness obstruction, `cor:target`, lines 377--417 | Retained for both relevant families at every \(d\ge4\). | `thm:biased` and `eq:value-conditioned`. |
| MB-05 | First-family scalar sum and paired weighted shifts, lines 420--553 | Subsumed by the exact-value/equality and first-family construction sections. | `lem:scalar` and `eq:first-strategy`. |
| MB-06 | Second-family Fourier compression and permutation maximizers, lines 554--739 | Retained. The source's exact value and SOS remain credited; the phase-permuted biased maximizers are the claimed new application. | `lem:lambda-normalization` and `thm:second`. |
| MB-07 | Exact second-family \(d=4\) certificate, lines 740--770 | Retained with an independent verifier. | Appendix `app:d4`. |
| MB-08 | Value-only robustness corollary, lines 771--786 | Retained with the corrected “deficit at most \(\varepsilon\)” quantifier. | Endpoint-robustness corollary. |
| MB-09 | Standard \(2\times2\) qudit tables, \(p_{\max}\), and asymptotic min-entropy, lines 787--826 | Retained, including the asymptotic entropy formula. | Appendix `app:settings`. Background calculation, not a minimum-setting theorem. |
| MB-10 | Direct perfect-anchor failure, lines 827--853 | Retained with the \(d=2\) MUB exception. | Appendix `app:settings`. Scoped construction failure only. |
| MB-11 | Computational-MUB exposure obstruction, lines 854--915 | Retained under its exact operator-span and coefficientwise-bound hypotheses. | `prop:mub`. **Novelty uncertain**; no general \((2,3,d,d)\) impossibility follows. |
| MB-12 | Private-MUB composition lemma, lines 916--961 | Restored as a sufficient state-supported operator criterion. | `lem:private-mub`. **Restored historical/internal design lemma**; no necessity, existence, enforcement, or novelty claim. |
| MB-13 | Setting-resource status table, lines 962--1015 | Restored and updated to distinguish proved, prior-art, conditional, and open regimes. | `tab:setting-status`. |
| MB-14 | Binary \(3\sqrt3\) SOS and operator-valued privacy benchmark, lines 1048--1085 | Restored with all auxiliary equalities stated on the state. After \(B_1\mapsto-B_1\), it is the \(\delta=\pi/6\) Wooltorton--Brown--Colbeck score. | `thm:binary-benchmark` and Appendix `app:binary`. **Established prior art**; retained as calibration, not novelty. |
| MB-15 | Verification, scope, priority, and disclosure, lines 1016--1047 and 1086--end | Subsumed by the unified review, audit, and verification package. Official Coccia--Padovan names are corrected in the canonical bibliography; the historical source remains immutable. | Audit and verification directories. |

## Machine artifacts and exact tables

| Historical artifact | Mathematical role | Canonical disposition |
|---|---|---|
| `cyclic_bell_tsirelson_bound/certificate.json`, `verify_certificate.py`, and tests | Scalar roots, polar identities, Weyl order, source Fourier relations, and exact radicals | Preserved and replayed; supplemented by `verify_exact_benchmarks.py` and a nonunitary-partial-isometry hostile test. |
| `cyclic_randomness_counterexample/certificate.json`, `family_certificate.json`, `verify_exact.py`, and family tests | Exact \(d=4\) table, all-dimensional phase cycles, target DFT, and source-behavior comparison | Preserved and replayed; the exact \(d=4\) implementation remains independent. |
| `minimum_bell_randomness/family_certificate.json`, `verify_second_family_d4_exact.py`, `verify_binary_2x2.py`, and `satwap_ideal_audit.py` | Second-family SOS, binary calibration, and ideal-table/anchor checks | Preserved and replayed; supplemented by the restored binary/private-MUB verifier. |
| Historical PDFs, source hashes, and publication chronology | Integrity and provenance record | Preserved byte-for-byte and linked from the canonical page. |

## Deliberate nonclaims and non-theorems

No proved substantive theorem from the three predecessors is silently
omitted. The following material is intentionally not promoted:

- numerical power-harmonic and third-setting repair experiments, because
  they are failed or exploratory approaches rather than theorems;
- a general \(2\times3\) impossibility or an all-dimensional minimum-setting
  law, because the fixed-basis obstruction proves neither;
- a complete maximizing-face classification, Weyl rigidity, or the exact
  worst-case guessing probability, because the support theorem and explicit
  permutation orbit supply only necessary and sufficient pieces,
  respectively;
- strategy-level self-testing modulo every isometry, ancilla, or
  transposition convention, because behavior-level nonuniqueness is the
  precise invariant established; and
- novelty for the binary benchmark, support-rigidity restoration, or
  private-MUB lemma.

See `CLAIMS_NOT_MADE.md` for the publication-facing negative-scope checklist.

## Crosswalk verdict

Every named theorem, proposition, lemma, corollary, exact quantitative table,
and verifier-supported identity in the three standalone TeX sources is
retained, strengthened, subsumed by an identified stronger result, or listed
above with a mathematical reason for nonpromotion. Historical directories
remain immutable evidence of wording and provenance.
