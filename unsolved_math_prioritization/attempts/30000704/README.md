# Boundary regularity for complete conformal metrics

Problem 30000704 / OWR-1460-010, queue rank 660. **Unsolved, 5/5 approaches exhausted; independently audited partial results only.** The minimum general boundary-regularity problem remains unresolved. No novelty or priority claim is established.

## Required correction: controlling Theorem C statement

**[Audit correction C1](audit/CORRECTIONS.md#c1-explicit-hypotheses-in-theorem-c-required-statement-correction) controls and supersedes the abbreviated standalone Theorem C sentence in the frozen original ANALYSIS.md. The curvature and positive C² metric hypotheses are essential. The original sentence is false if read without them.** The corrected statement is:

**Theorem C (free-Jordan equivalence).** Let Ω be a connected open subset of C, let λ:Ω→(0,∞) be C² with curvature κλ≥−4, and let Γ⊂∂Ω satisfy the explicit one-sided local Jordan condition (J). Then (B), density blow-up at every point of Γ through unrestricted approaches in Ω, and (C), metric-distance divergence at every such point, are equivalent. No boundary differentiability is required. The reverse direction uses the localized disk completeness comparison stated in the 2007 primary report.

Read the definitions of (J), (B), and (C) in [the frozen analysis](safe/ANALYSIS.md) together with this controlling correction. The original proof already uses the missing hypotheses. The audit also gives the counterexample λ=(1−|z|²)^(−1/2) on the disk, whose density diverges but whose radial length is finite and whose curvature is unbounded below.

## Verified partial scope and remaining gap

The authored results establish the equivalence for explicit one-sided free-Jordan arcs with positive C² λ and curvature at least −4, and a componentwise regular-open sufficient criterion for the forward implication. Two constant-curvature counterexamples obstruct punctures and arbitrary distinguished subsets even of smooth boundaries. These sufficient conditions do not classify the weakest boundary assumptions or arbitrary thin endpoint geometries.

The reverse direction uses an established localized disk completeness comparison stated in the 2007 primary report. That statement was inspected; the original detailed KRR 2007 proof was not available for inspection. The dependence is explicit. Neither complete current-literature coverage nor novelty has been established.

## Complete evidence and reproduction

- [Frozen authored analysis and five-approach record](safe/README.md)
- [Full independent mathematical audit](audit/AUDIT.md)
- [Required correction and source limitation](audit/CORRECTIONS.md)
- [Exact author binding](audit/BINDING.json)
- [Fresh repository/queue gate](LIVE_GATE.json)

All 12 frozen author files and all 10 safe audit files are retained byte-for-byte, as are both original ZIP archives. The frozen author pending-audit status and no-remote-write statements describe their creation stage; this wrapper and the later bound audit give the current partial verdict. The abbreviated theorem is preserved only as a historical original subject to C1, not as an unqualified current claim.

Requires Python 3.10+ and SymPy 1.14.0. From this directory run:

    python3 verify_release.py

The verifier checks the exact file set and hashes, fixed archive and manifest bindings, ZIP/extracted equality, required correction, status and five-turn count, author and audit verifiers, 22 original controls and 27 independent controls, and a fresh archive-only replay. It uses no network. Exact controls are algebraic/limit stress checks, not proof certificates for topology, compactness, or the cited theorem.

This package includes authored mathematics/code and public-source verification metadata only. Scholarly PDFs/text, raw datasets, private coordination records and credentials are excluded. The sole queue changes are this target's Status and Turns; all other queue bytes are preserved.
