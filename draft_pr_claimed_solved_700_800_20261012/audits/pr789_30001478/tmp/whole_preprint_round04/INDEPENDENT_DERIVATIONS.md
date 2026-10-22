# Additional independent derivations

UTC timestamp: 2026-10-16T18:06:38.683068+00:00. Derived after initial strategy freeze and before receipt/reading of candidate pins.

Let `a,b` be standard homogeneous coordinates on P1 and let the pullback of a projective automorphism act by `sigma*(a)=a+beta*b`, `sigma*(b)=beta*a+b`. Its determinant is `1-beta^2`, hence nonzero in every allowed characteristic. Use THCR product `f star g=f sigma*(g)` on degree-one sections. Then

`beta*(a star a)-(a star b)+(b star a)-beta*(b star b)`
`=a[beta(a+beta*b)-(beta*a+b)]+b[(a+beta*b)-beta(beta*a+b)]`
`=(beta^2-1)ab+(1-beta^2)ba=0`.

The binary relation therefore gives a graded surjection `A -> B(P1,O(1),sigma)` once degree-one generation is checked. Since O(1) is sigma-invariant and the twisted polynomial algebra is a Zhang twist, degree-one generation follows inductively: the span of products of degree n elements and degree-one elements is `k[a,b]_n * sigma^n(k[a,b]_1)=k[a,b]_(n+1)`. The target degree n space has dimension n+1.

Injectivity can be proved without a classification theorem. If char(k) is not 2, change to `u=a+b, v=a-b`. The relation is `(beta+1)uv+(beta-1)vu=0`; beta plus/minus 1 are nonzero, so this is a quantum plane, whose PBW basis is `u^i v^j`. If char(k)=2, change to `u=a+b, v=a`. The relation is `beta*u^2+(beta+1)(uv+vu)=0`, equivalently `vu=uv+[beta/(beta+1)]u^2`. With `v>u`, degree-lex rewriting of `vu` terminates, and `vu` has no self-overlap, giving PBW basis `u^i v^j`. In both cases `dim A_n=n+1`, proving injectivity of the surjection. Both presentations are Ore extensions of k[u] with injective automorphism (quantum case) or derivation (characteristic 2), hence domains. Alternatively B embeds in the skew Laurent extension of its function field.

Thus the stronger target exclusion fails even when 'map' means a surjective graded homomorphism onto a positive-dimensional integral ample THCR. The explicit composite sends `x1,x3` to `a` and `x2,x4` to `b` in this B. Relations 1–4 cancel pairwise after these identifications; relations 5–6 equal the binary relation.
