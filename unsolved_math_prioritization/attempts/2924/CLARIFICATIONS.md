# Clarifications following the independent review

The frozen nine-file report and the independent audit are preserved byte-for-byte. These clarifications address the audit's two nonblocking precision advisories. They do not claim a solution or change any numerical result.

## Relative embedding-space convention

In PROOF.md §4, equation (8), use relative codimension-zero embeddings e: C → Δ with e equal to the original inclusion on the outer boundary Σ, e⁻¹(Σ) = Σ, and the inner S³ boundary mapped into the interior. Use the compact-open topology and the parametrized locally flat embedding convention required by relative isotopy extension.

The base is the ambient-isotopy orbit of the original inclusion, rather than an unrestricted space of arbitrary embedding families. The restriction sequence is interpreted as the standard Serre/homotopy fibration on that orbit. This suffices for the long exact homotopy sequence and its disk-fiber comparison. There is no assertion of a global continuous extension section, surjectivity onto all embeddings, or automatic parametrized local flatness of every pointwise locally flat family.

## Cone-chart wording

In PROOF.md §2.3, choose a chart 4-ball V containing the cone vertex v, with Uδ contained in V contained in Uε, and then puncture each neighborhood at v. The fundamental-group map between the punctured conical neighborhoods factors through π₁(V minus {v}) = 0. The original phrase calling V a punctured ball before using it as a neighborhood should be read with this correction.

## Unchanged outcome

The report remains unresolved after five substantive attempts. Even π₁ of the boundary-pointwise homeomorphism group is not determined in general. Weak contractibility is distinguished from an actual continuous contraction of the whole compact-open group; no CW-type or ANR upgrade is assumed.

The historical `independent_review: pending` field in the frozen STATUS.json records the pre-audit state. The separate audit records a pass for publication as an explicitly unresolved investigation.
