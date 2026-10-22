# Research log and bounded attempt accounting

Date: 2026-10-05 UTC. No remote writes were made. The percentages below are rough progress-to-goal judgments, not probabilities of correctness or novelty. The target has two different statuses after source recovery: the literal imported statement is disproved; the correctly qualified primary conjecture is unresolved.

## Source and history preflight, approximately 10:10–10:17

Checked the exact target URL (failed), descriptor, primary OWR contribution, Batyrev–Moreau formulation and definitions, a January 2026 primary smoothness preprint, and a separate Mori-program paper. Read repository research instructions and inspected PR, branch, and attempt-folder evidence; limitations are recorded separately. A first public exact-ID dataset query timed out, and a bounded longer retry was launched. Primary PDF statements were checked against rendered pages. No target-specific prior attempt was verified; this is not an absence proof. Estimated progress toward the qualified conjecture: 5% (source identification and known-case separation, not a central proof).

## Approach 1: toric lattice criterion

Mechanism: local factoriality gives integral dual Cartier data; the ray generators form a direct summand of the lattice. Retained: a complete proof that locally factorial toric varieties are smooth. The horospherical theorem was recognized as prior work. Obstruction: colors and spherical-root data are not removed by integral cone regularity. Estimated progress toward qualified conjecture: 8%.

## Approach 2: single-divisor cone resolution

Mechanism: compute the exceptional discrepancy from adjunction and bound the Fano index by roots of the Hilbert polynomial. Retained: complete cone formula and equality theorem under explicitly stated subcanonical, very-ample, normal/Q-Gorenstein, degree-one, and odd-cohomology-vanishing hypotheses; projective-cone corollary. The basic formula was checked against De Deyn's prior result. Obstruction: no reduction of general spherical slices to this one-divisor Fano situation. Estimated progress toward qualified conjecture: 15%.

## Approach 3: orbitwise Euler integration

Mechanism: express the global deficit as a finite sum of orbit Euler numbers times local weighted deficits. Retained: the exact reduction, nonnegativity of homogeneous-orbit Euler numbers, and the resolution upper bound e_st(X)<=e(Y). Obstruction: the local lower and strict bounds needed by the conjecture do not follow from these positivity statements; Mori monotonicity supplies a different comparison. Estimated progress toward qualified conjecture: 15% (better diagnosis, no advancement of the missing local bound).

## Approach 4: products and hypothesis sensitivity

Mechanism: factor the log-resolution strata under products. Retained: exact multiplicativity and deficit formulas, an explicit factorial four-dimensional quadric cone, and its product with C*. The latter is singular but has e_st=e=0; its closed orbit is not projective. Initially retained only as a negative control because the complete dataset statement had not yet been recovered. Estimated progress toward qualified conjecture: 15%; a potentially complete counterexample to the overbroad formulation was available, pending source identity.

## Approach 5: degeneration transport

Mechanism: test an invariant-transfer argument on a proper flat SO(5)-spherical quadric family. Retained: flatness, spherical open-orbit calculation, local factoriality of the singular fibre, and exact Euler values: smooth fibre (e,e_st)=(6,6), singular fibre (5,16/3). Obstruction: ordinary, stringy, and deficit invariants are not constant even here; an additional specialization inequality with strictness would be necessary. Estimated progress toward qualified conjecture: 15%.

## Exact source recovery and stopping decision, approximately 10:24–10:27

The longer public dataset query returned one complete row for ID 30002003, index 10787, with no truncated cells. Its statement is unrestricted: it omits the projective-closed-orbit condition. Its UTF-8 SHA-256 matches the pre-existing descriptor exactly, with 126 statement bytes. Therefore the already completed Approach 4 is a counterexample to the actual literal imported statement. No further proof search was undertaken after this identity check.

Literal imported statement: 100% mathematical counterexample prepared, subject to independent verification; qualified primary conjecture: unresolved, approximately 15% as above. This split avoids counting a missing-hypothesis correction as a solution of a famous or currently open conjecture.

## Artifact checks

Prepared a self-contained authored packet with proofs, source-status distinctions, metadata-only verification, and standard-library exact arithmetic checks. The replay passes 321 checks and rejects nine deliberately false shortcuts, including denominator, integrality, product strictness, and deformation-constancy errors. Those checks corroborate calculations but do not independently prove algebraic geometry. A fresh adversarial mathematical/source audit and publication review remain required.

No repository queue mutation was performed. The parent should choose the appropriate statement-repair/counterexample status after the audit, while preserving that the qualified conjecture was not resolved and while not inventing a complete historical attempt count.
