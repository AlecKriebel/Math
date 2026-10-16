# PR12 exact-head measure/band audit

**Verdict: PASS for the mathematical claim within the stated scope.** No
counterexample, hidden separability assumption, pointwise-uniformity failure,
or missing power-to-operator argument was found. This family independently
reconstructed the whole theorem and particularly audited Sections 3–5.

**Candidate:** PR12 head `19dfaccb52a7640eec79af28a778b4f22f93479a`.
**Source:** `source_snapshot/PROOF.md`, SHA-256
`f38ae2dd97bb2aeb8f1e97da0f4133b84b6d43d803e2b38df2c91acc56817a8e`.
The exact source, target record, and snapshot manifest were read. The existing
review, candidate code, and verification outputs were not read. A child
challenge received only a scalar proposition and maintained independence
from both source proof and parent notes through its completed derivation.

## Strongest verified result

For every real or complex scalar Lp, 1<=p<infinity, satisfying the exact
bounded-invertible dissipative hypotheses, two-sided shadowing implies the
uniform pointwise density criterion and a generalized-hyperbolic split into
complementary measurable support bands. The converse follows by the explicit
bounded Green-series solution. Moving and unbounded fiber cuts, distinct
residue cuts, zero bands, p=1, and nonseparable sigma-finite measure spaces
are included. No central mathematical gap remains in this proof family.

Bibliographic priority, the scope of quoted external source theorems, and
novelty across the broader literature were not audited by this family.

## Source-line findings

| Source lines | Obligation | Result and reason |
|---|---|---|
| 12–28, 46–62 | Positive finite densities and modulo-null wandering coordinates | Pass. Iterated measure bounds make nu_n finite and equivalent to nu; a countable invariant conull restriction makes the partition literal if desired. |
| 150–169 | U is an onto isometry; normalized shift is bounded invertible | Pass. Piecewise inverse on f^nW is measurable, and norm identities sum nonnegative coordinate integrals. Adjacent density ratios are uniformly bounded above/below. |
| 171–184 | Scalar dual identification and adjoint coefficient orientation | Pass. L1*=L∞ is valid here without separability. Weights telescope in the stated direction, including inverse powers. Positive real weights also settle complex conjugation. |
| 189–202 | Operator uniformity becomes a common pointwise estimate | Pass. Finite-measure coordinate indicators localize both scalar factors; countably many n give one exceptional null set. The same fixed d is used everywhere. |
| 206–250 | Direction propagation and power-band decay | Pass. An opposite drop would imply 1<=eta^2. Input-index norm formulas give eta^(m/p), including equality and both-drop boundary points. |
| 260–282 | Finite intersection and complement give B/B^-1 invariance | Pass. Intersections are support bands, complementation commutes with the weighted coordinate permutation, and the finite sum is exactly a measurable union band. |
| 284–319 | Complementary-band uniform decay and passage to all powers | Pass. Finite disjoint partitions and their images remain disjoint, giving the exact p-th-power norm sum even at p=1. Finite remainder bounds yield rate eta^(1/(pd)). |
| 73–137 | Remaining necessary dual estimate | Pass on independent reconstruction. Boundary residual indices are a_a and a_(b+1); finite-dual norm approximations use no attainment/separability assumption. |
| 327–346 | Whole-theorem converse | Pass on independent reconstruction. Uniformly absolutely convergent series telescope to Pb_n+Qb_n; projection commutation is unnecessary. |

## Independent mechanisms and counterexample routes

| Family or route | Mechanism | Evidence/status | Exact remaining gap |
|---|---|---|---|
| Measure/band reconstruction | RN orbit densities, scalar Lp duality, localized indicators, finite intersections/unions | Complete proof in DERIVATION.md; exact-head line audit above | None for the specified theorem |
| Source-independent scalar reconstruction | Log slopes on residue sequences, measurable first nongrowth edges, bounded threshold separation | Complete child proof; no source proof or parent notes read; parent audited its threshold and constant estimates | Does not itself identify an arbitrary operator with a measure model; parent reconstruction supplies that bridge |
| Disagreeing residue cuts | Independent tents on congruence classes | Valid when relative separation is bounded; finite intersection produces the earliest peak cut | Attempt to make relative separation unbounded loses global B/B^-1 boundedness |
| Nonuniform fiber shadowing | Fiber slopes tending to zero | Verified counterexample to the weaker fiberwise premise, with localized dual obstruction | Not a counterexample to the uniform exact premise |
| Flat tails and positive-measure bad fibers | Equal density factors on both sides | Uniform necessary dual estimate rules them out | Does not satisfy exact density premise |
| Unit-circle eigenvectors | Constant original function in finite exponential-tent measure | Explicitly compatible with the non-two-sided-invariant generalized split | Eigenvalue alone is not an obstruction; route to ordinary hyperbolicity is invalid |

## Checkable artifacts and reproducibility

- `DERIVATION.md`: full quantified proof reconstruction, including measure
  completion/nullset details, p=1 duality, source-index checks, and exact decay
  constants for passage from block powers to all powers.
- `ADVERSARIAL_CASES.md`: explicit models and rejected counterexample attempts.
- `stress_checks.py` and `stress_results.json`: independent exact arithmetic
  checks. Ran successfully: 21 fibers; 44,221 density, adjacency, propagation,
  intersection-cut, and invariance samples each; 221,105 block-norm inequalities;
  672 exact p-th vector moments for p=1,2,3,8, including complex moduli.
- `discrete_cut_challenge/independent_derivation.md`: source-independent second
  proof. Its key compatibility bound is

      |t_r-t_s| <= 1 + |r-s| log Q/(-log eta).

- `discrete_cut_challenge/validate.py` and `validation_result.json`: rerun by
  the parent family auditor. All 481,475 exact scalar inequalities passed across
  405 families, including one exceptional residue edge and full/zero bands.
- `RESEARCH_LOG.md`: timestamped checkpoints and completion percentages.
- `artifact_manifest.json`: artifact hashes and final verification metadata.

The finite checks support the derivations and are clearly labeled finite;
the universal conclusion comes from the derivations. No float roots, sampling
claims about all measurable fibers, or finite-horizon inference replace proof.

## Clarifications, not revision blockers

The source's standard modulo-null convention can be expanded into the
explicit invariant conull restriction in DERIVATION.md. The scalar duality
statement needs no separability qualification under the stated sigma-finite
hypotheses. The zero-band cases are legitimate under the definition given;
if discussing spectra on the zero space, using uniform decay avoids any
irrelevant convention about the empty spectrum. These points do not require
changing the theorem or its proof mechanism.

**Completion estimate:** 100% of this assigned bounded mathematical audit.
No Git changes, branches, commits, pushes, canonical source edits, or external
outreach were performed by this family.
