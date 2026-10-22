# Audit correction addendum

Original files remain unchanged. This addendum applies to original manifest SHA-256 860f342d02acf761c40c3bca59f959fd1e4e3d3e7c028292ccdcf7b3dca46255.

## C1: Explicit hypotheses in Theorem C (required statement correction)

Location: ANALYSIS.md, Section 2, standalone statement of Theorem C.

Replace the abbreviated statement with:

**Theorem C (free-Jordan equivalence).** Let Ω be a connected open subset of C, let λ:Ω→(0,∞) be C² with curvature κλ≥−4, and let Γ⊂∂Ω satisfy the explicit one-sided local Jordan condition (J). Then (B), density blow-up at every point of Γ through unrestricted approaches in Ω, and (C), metric-distance divergence at every such point, are equivalent. No boundary differentiability is required. The reverse direction uses the localized disk completeness comparison stated in the 2007 primary report.

Reason: The original standalone sentence begins “Under (J)” without explicitly repeating the lower-curvature assumption. The proof already uses that assumption correctly. Omitting it from the mathematical claim would be false: λ=(1−|z|²)^(−1/2) on D blows up on the whole boundary and has finite radial length, while κλ=−2/(1−|z|²). This is a statement-level clarification, not a repair of the intended proof.

## C2: Known-source dependence (clarification; existing scope is acceptable)

When summarizing the audit, distinguish verification of the disk implication's statement in OWR 9/2007 p.529 from inspection of its original proof in the KRR 2007 article. Only the former was completed. Do not upgrade the author's accurate source-access limitation or make a novelty claim.

## Status

No correction changes the full target's disposition: unsolved / exhausted partial, five substantive approaches out of five. No original bytes were modified and no remote write was performed by this audit.
