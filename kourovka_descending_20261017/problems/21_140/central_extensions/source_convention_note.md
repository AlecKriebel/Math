# Source convention discrepancy: not used in the proof

Timestamp: 2026-10-17 21:27:48 UTC. Status: unresolved source-normalization discrepancy; narrow proof completion estimate remains 95% pending independent review.

Funar–Sergiescu arXiv:0802.2996v2, §4.2, displays the circle determinant cocycle and states that it evaluates to 2 on the cycle represented in F by `(AB⁻¹,A⁻¹BA)−(A⁻¹BA,AB⁻¹)`, where their §1.2 gives the usual interval formulas for A=x₀ and B=x₁.

With ordinary function composition and the circle convention `g′_l(0)=g′(1−)`, the exact local computation instead gives:

- `u=AB⁻¹`, `v₁=A⁻¹BA`: commute; C(u,v₁)=C(v₁,u)=0.
- `v₂=A⁻²BA²`: commutes with u; C(u,v₂)=−1, C(v₂,u)=1.

If the circle point 0 is omitted from the determinant sum, the corresponding alternating values become 2 and 0, which agree with the source's stated pairings. This observation is diagnostic only; it does not establish why the published formula and computation differ. It may reflect a convention, a transcription issue, or an error. The present notes do not assert a correction to the paper.

The contribution of circle point 0 is explicitly

`C₀(g,h)=λ(g)ρ(h)−λ(h)ρ(g)`.

Thus omitting it changes a cocycle by an endpoint-character cup combination. This distinction matters for stated cycle evaluations but does not threaten the existence of the rational two-class span or the mirrored interior embedding's vanishing properties.

The proof in `../approach_central_extensions.md` avoids the discrepancy entirely: it proves the cocycle identity directly, uses elementary adjacent interior clones for its nonzero value, and uses Brown's H₂ rank theorem for completeness. It does not import the source's η pairing or its normalization of the Godbillon–Vey class.
