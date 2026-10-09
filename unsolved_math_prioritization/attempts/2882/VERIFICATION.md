# Verification status for reconstructed turn 3

## Status

Reconstructed on 2026-10-09, with fresh primary-source inspection and supplementary arithmetic checks. **Fresh independent audit completed and accepted for the stated partial obstruction.** The claim-check table below preserves the reconstruction-stage verification record. AUDIT.md and ACCEPTANCE.md record the later review. This is a proof-only editorial edition; no historical byte equality or inherited acceptance of missing files is asserted.

The original target remains an absolute exotic pair of compact connected orientable fillings for every prescribed closed orientable 3-manifold, possibly disconnected, as the entire boundary. Infinite families and simple connectivity are not required. The connected-boundary restriction applies only to this detector family. Problem 2882 / KP-4.6 remains UNSOLVED 3/5. No queue was edited and no publication was attempted.

## Claim checks

| Report component | Check performed | Result and scope |
| --- | --- | --- |
| Original target | Checked the target separately from the connected test-boundary convention | Exotic pair; prescribed boundary may be disconnected; fillings connected and orientable; no infinite-family or simple-connectivity requirement |
| Source family | Visually checked DLM printed page 3357, including all minus signs and both plumbing orientations | Family is mP # k(-O), m >= 1, k > 8m; no restriction on filling b1 or pi1 |
| Definite filling scope | Read DLM Propositions 1.1 and 2.1 and the latter's preliminary surgery argument on page 3359 | Killing rational first homology is part of a proof, not an input restriction |
| Nondegenerate form | Checked the real homology sequence and Poincare-Lefschetz pairing argument | Applies to arbitrary first homology in the filling |
| Rank-zero escape | Checked the interior connected sum with CP2 | Preserves boundary and creates a forbidden nonzero definite form |
| Explicit filling | Exact rational arithmetic for standard E7/E8 Cartan matrices; plumbing homology argument | E8 determinant 1, E7 determinant 2; example indices 63 and 8; boundary H1 is (Z/2)^9 |
| Integral coefficient claim | Visually checked OS Definition 1.1, Section 2, Proposition 2.3 | Uses free abelian HFhat and integral reduced vanishing; no F2-to-Z inference |
| Direct transplant | Checked the placement of the puncture, internal S3 cut, two positive indices and cut cohomology | Full integral mixed map vanishes by factorization through reduced HF of S3 |
| All caps and gluings | Checked real Mayer-Vietoris and orthogonality, independently of the gluing map | Both sides remain positive, and the closure has b2+ >= 2 |
| Individual closed OS invariant | Checked integral H1-cohomology of the boundary and OS Theorem 10.1 | H^1(Y;Z)=0 gives unique global Spin-c extension for given restrictions; no cancellation inference |
| All ordinary OS insertions | Checked the actual mixed-map domain and Section 9 definition; first homology surjectivity across connected Y | Full Z[U] and exterior-algebra domain included |
| SW scope | Checked the interior connected sum moves outside any boundary gluing | Claimed only for capped transplants E # N, not all closures of all fillings |
| SW mixed composition | Visually checked KM page 64 and pages 558, 560-565 | Choose N with b2+ >= 2 first and E with b2+ > 0 second; ordinary check map of the latter is zero |
| SW insertion and component selectors | Checked KM configuration-space disjoint union, arbitrary cohomology composition, Definitions 27.1.6-7 and Proposition 27.4.1 | Degree-zero selectors distinguish torsion Spin-c structures; no reliance on a vanishing total sum or real Chern-class weights |
| SW arbitrary b1 | Checked insertion decomposition using integral connected-sum H1 | No simply connected or b1=0 assumption introduced |
| Plus/minus distinction | Checked exact-sequence injectivity/surjectivity for integral L-spaces | Only ordinary undecorated plus/minus maps claimed in this separate paragraph |
| Attribution | Visually checked EMM Remark 1.8 | Connected-sum method and generic warning are credited to EMM |
| Remaining gap | Re-read statements and final section | No exotic family constructed; no universal nonexistence or actual diffeomorphism claim; no claim about hat, twisted, local, stable or families detectors |

## Historical supplementary arithmetic

During reconstruction, an exact-arithmetic program produced the same recorded output in normal, -O and -OO modes. Its runtime validation used explicit exceptions rather than removable assertions. Those are historical checks of the Cartan data, not gauge theory or formal verification. The program and standalone output are excluded from this proof-only edition and were not rerun to prepare it. REPORT.md now supplies a written chain-determinant and Schur-complement derivation of the same elementary arithmetic.

## Source fidelity caveats

1. The DLM PDF's plain-text extraction drops some minus signs. The family and the orientations were therefore checked on rendered PDF pages.
2. The KM PDF's plain-text extraction loses the slash in the nonzero condition of Proposition 3.5.2. The rendered page says b+(W) is nonzero; the report uses b+(W) > 0.
3. OS math/0110169v2 Theorem 10.1 has a harmless mismatch of variable names in the source statement. The report uses the consistent restriction t = s|Y and the proof directly below the theorem.
4. The Mukherjee restatement is corroborating evidence only; the integral claim is independently grounded in the integral OS sources.
5. Fresh inspection of cited theorem statements and relevant constructions is not a line-by-line reproof of each published paper or the book.

## Completed independent audit and editorial boundary

The independent audit checked the quantifiers over fillings, caps and boundary maps; the integral coefficient chain; the precise mixed-map scope; the all-insertion and individual Spin-c SW deduction; and the distinction between detector failure and failure of exoticness. It accepted the reconstructed input without a mathematical correction or scope narrowing. The exact input digest, subsequent editorial treatment and current file identities are stated separately in ACCEPTANCE.md, PROVENANCE.md and MANIFEST.json. This preserves the distinction between the original audited bytes and the later proof-only edition.
