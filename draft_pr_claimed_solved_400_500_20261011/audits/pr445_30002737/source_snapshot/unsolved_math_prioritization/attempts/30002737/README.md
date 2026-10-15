# Planar singular diffraction with an absolutely continuous dynamical component

**Status: claimed_solved, 1/5 substantive attempts.** A fresh independent AI adversarial audit reports **PASS** for the dimension-unrestricted statement with absolute continuity measured against ambient Haar measure. This is an unrefereed AI-assisted research result, without a novelty, historical-priority or human-peer-review claim.

The construction gives an unweighted, aperiodic, repetitive FLC Meyer set in the plane with uniquely ergodic translation hull. Its diffraction consists of lattice Bragg peaks and horizontal/vertical line measures, hence is singular relative to two-dimensional Lebesgue measure. A bounded observable on its hull has spectral density sinc²(k1)sinc²(k2), equivalent to planar Lebesgue measure.

**Scope is essential: this is a planar product counterexample to the printed unrestricted implication. It does not resolve a separately restricted one-dimensional question.** No exact spectral multiplicity or purely absolutely continuous full dynamical spectrum is asserted.

## Read the mathematics

- [Complete frozen proof](author/attempts/turn_01.md)
- [Full independent audit](audit/independent_audit.md)
- [Additive source and action-convention clarifications](CLARIFICATIONS.md)
- [Primary-source verification and limits](SOURCE_GATE.md)
- [Attempt and verification record](RESEARCH_LOG.md)

The three original proof/check files are preserved byte for byte. Their historical “audit pending” language is superseded by this README and the full audit. The earlier separate manuscript draft is excluded and is not covered by the audit.

## Reproduce the controls

Python 3.10 or later; standard library only. From this directory run:

    python author/checks/verify_counterexample.py
    python audit/independent_controls.py

Each script writes its adjacent result JSON. The audit control replays the author checker in a temporary copy and verifies original-file hashes before and after. Finite checks supplement the analytic proof; they do not replace the infinite Rudin–Shapiro theorem. The independent physical-point controls retain finite imbalance and boundary terms rather than treating sample correlations as exact limits.

For portability, the independent script's original absolute root was replaced by a path relative to this package and its manifest name was adjusted. Its mathematical code and expected results are unchanged. The full audit was sanitized only to use public relative paths and clarify the excluded manuscript. Source PDFs, source images, corpus extracts and private workflow records are not included.

Problem: [30002737 / OWR-13355-001](https://www.unsolvedmath.com/problems/30002737), queue rank 480. The authoritative target is van Enter's Conjecture 1, [Oberwolfach Report 53/2014, p.2996](https://doi.org/10.4171/OWR/2014/53).
