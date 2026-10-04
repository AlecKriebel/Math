# KP-3.33 / 2831: degree-one maps and Heegaard genus

**Unsolved; five substantive approaches used.** No general proof, counterexample, or verified complete published resolution was obtained. No novelty claim is made for the partial observations.

- `PARTIAL_RESULTS.md`: precise target, complete elementary partial proofs, explicit external theorem dependencies, and exact gaps.
- `APPROACH_LOG.md`: five distinct approaches and completion estimates.
- `SOURCE_STATUS.md`: primary-source correction, literature scope, provenance, and live duplicate checks.
- `controls.py` and `CONTROL_RESULTS.json`: small deterministic exact-arithmetic consistency checks. These do not verify 3-manifold topology or search for counterexamples.
- `RESULT.json`: proposed status/turn metadata only; no remote state was changed.
- `SHA256SUMS`: frozen release-file hashes.

Run `python3 controls.py` (Python 3.10+ standard library only) and `sha256sum -c SHA256SUMS` from this directory. The controls do not download anything or need private inputs. They create no proof of the universal conjecture and are not a substitute for an independent mathematical audit.

The strongest uniform bound obtained is g(M)≥rank π₁(N). Cover-homology amplification cannot exceed that bound. Geometry beyond rank is still missing. This bundle awaits an independent audit and publication decision; it is not a solution candidate.
