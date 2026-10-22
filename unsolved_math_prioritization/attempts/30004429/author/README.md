# Discontinuities of two-sided specifications: audited-research candidate

Problem 30004429 · OWR-17474-001 · catalog rank 751

## Verdict

**NO RESOLUTION of the Schonmann-projection almost-Gibbs question.** This packet contains proved reductions and countercontrols, not a proof that the exceptional set has zero or positive measure. No novelty or priority claim is made. An independent audit is required before publication; this is the author's frozen candidate, not an audit certificate.

The governing question concerns the marginal on a horizontal line of the plus phase of the two-dimensional, nearest-neighbor, zero-field ferromagnetic Ising model at finite inverse temperature β > βc. It asks for the existence of a two-sided conditional specification whose discontinuities form a null set for that marginal. Continuity means continuity in the full product topology at almost every boundary configuration. Merely restricting a conditional-probability function to a full-measure set, or proving pointwise convergence of finite conditionals, is insufficient.

## Main findings

1. The exact model and the almost-sure two-sided question are recovered from the primary workshop report, printed pages 602 and 619–620. The underlying primary paper supplies the product topology and the single-site almost-Gibbs definition.
2. Van Enter and Shlosman, published in 2024, prove everywhere **one-sided** continuity at sufficiently low temperature. Their Theorem 3 is not a resolution of the two-sided almost-sure question. The all-subcritical-temperature extension is described as prospective in that paper.
3. A fully proved, version-invariant reduction replaces ambiguous discontinuity sets by essential oscillations on finite exterior cylinders. For the attractive Ising marginal the extrema are limits obtained by fixing the outer line annulus entirely plus or entirely minus.
4. The remaining task is precisely to show that the difference between these two limits tends to zero for almost every growing central line configuration. The required control is uniform over arbitrarily long outer annuli. Known one-sided mixing and almost-sure martingale convergence do not establish it.
5. The catalog's appended reference to long-range Ising models does not identify an interaction, marginal map, phase or parameter range. The nearby long-range open question in the workshop introduction concerns an Aizenman–Higuchi result. Under the separate interpretation of the **original** summable Dyson interaction, its canonical two-sided specification is everywhere continuous; a short proof is included. That does not resolve an unspecified transformed long-range model or the Schonmann question.

## Files and reproduction

- `PROOFS.md`: exact setup; finite energy; essential-oscillation theorem; FKG annulus reduction; one-sided likelihood criterion; two explicit countercontrols; the native long-range calculation.
- `APPROACHES.md`: five routes, what each establishes, and its precise stopping gap.
- `SOURCE_VERIFICATION.json`: public source metadata, retrieved-byte hashes where actually available, inspection scope, and access limits.
- `PRIOR_WORK_CHECK.json`: exact-target prior-work checks, pinned corpus matches, and search limits.
- `verify_controls.py`: standard-library-only exact rational checks.
- `CHECK_RESULTS.json`: recorded output of the controls.
- `MANIFEST.json`: SHA-256 and byte counts for the allowed files, excluding the manifest itself.

Run `python3 verify_controls.py` from any directory. It writes `CHECK_RESULTS.json` alongside the script. These are finite algebraic/control checks, not a simulation or proof of the infinite-volume target.

## Sources

- [OWR report, DOI 10.4171/OWR/2020/11](https://ems.press/journals/owr/articles/17474), pp. 602, 619–620.
- [Bethuelsen–Conache, One-sided continuity properties for the Schonmann projection](https://arxiv.org/abs/1802.02059), Definition 2.1, Proposition 3.2, Theorem 3.3 and §3.2.
- [Van Enter–Shlosman, The Schonmann projection: How Gibbsian is it?](https://doi.org/10.1214/22-AIHP1266), Theorem 3 and §5.
- [Bethuelsen–Forsström, Mixing for Poisson representable processes and consequences for the Ising model and the contact process](https://arxiv.org/abs/2501.14445), Lemma 2.4 and Proposition 2.5; published in SPA 192 (2026), 104831.
- [Fernández–Gallo–Maillard, Regular g-measures are not always Gibbsian](https://arxiv.org/abs/1106.4188), §1 and Theorem 3.1. Their example is itself almost Gibbsian; it is not a counterexample to this target.

No PDFs, source extracts, dataset records, raw datasets, or private coordination files belong to this packet. The literature search found no verified later resolution; it does not certify exhaustive absence of one.
