# Positive-construction approaches and exact gaps

Checkpoint 2026-10-24. Full-problem completion estimate8%; no positive
commensurability mechanism has been obtained.

## Reflection and arrangement models

The standard complex reflection realization labels F4 as G28 and H4 as G30.
Relabeling a reflection group does not change the problem. General complex
braid-group presentations and Garside structures provide finite K(pi,1)
models, not common covers or isomorphic finite-index groups. The existence
of a common ambient complex braid group, even with injective embeddings,
would not establish that the two images are internally commensurable.

The projective arrangement route was made concrete rather than left at
this observation: the exact log-volume calculation in
`ALGEBRAIC_COVER_FILTER.md` gives a candidate obstruction to a common
finite étale **algebraic** cover of the given complements. It remains
compatible with arbitrary abstract commensurability, because finite
algebraic covers having isomorphic groups can have different algebraic
structures. The additional statement that their group isomorphism comes
from an algebraic isomorphism is unsupported here.

The previously studied arrangement deletion maps and finite-parameter CHL
monodromy maps are not reopened: they have infinite kernels. Matching a
holonomy lattice or repairing a map by a central extension leaves the
noncentral kernel issue and cannot produce the required finite-index
isomorphism.

## Common larger spherical Artin group

Crisp-type folding embeds H4 into E8 and F4 into E6 (and then into E8 by a
standard parabolic inclusion). This is not a common finite-index model:
their cohomological dimensions are4, while those of E6/E8 are6/8; finite
index preserves cohomological dimension. Nor does the existence of the
embeddings identify the intersection of their images as finite index in
either image. No such intersection theorem was obtained.

Primary references located for the embeddings are J.Crisp, *Injective maps
between Artin groups*, in *Geometric Group Theory Down Under* (1999),
pp119–138, DOI10.1515/9783110806861.119, and I.Marin, *On the residual
nilpotence of pure Artin groups* (2011), the explicit H4→E8 folding in its
proof. These are established tools; no new embedding or injectivity claim
is made in this record. The Crisp chapter publisher page was accessible,
but the chapter PDF itself was paywalled in this session; the search-found
Marin primary PDF explicitly describes the folding. The source-access
limitation does not affect the log-volume proof, which uses neither.

## Euler-index constraints are consistent, not a positive construction

Writing Q_T=P_T/Z(P_T), the two groups have Euler characteristics−240 and
−5040. If a common finite-index subgroup has indices a in Q_F4 and b in
Q_H4, then a/b=21. This is arithmetically consistent. Both groups map onto
F2, hence each has subgroups of every positive index; index availability
does not supply an isomorphism between any such subgroups.

For the full central quotients G_T=A[T]/Z(A[T]), the pure central quotient
has index|W(T)|/2 because w0=−1 in both types. Thus their rational Euler
characteristics are−5/12 and−7/10. A common torsion-free finite-index group
with indices a in G_F4 and b in G_H4 would obey

    a/b=42/25,   a=42k, b=25k.

These constraints exclude some particularly small proposed covers, but
they are not sufficient and do not apply to the full Artin-group indices
without controlling the central indices. Full Artin-group Euler
characteristics vanish. Any use of the displayed quotient ratio must
explicitly pass to the central quotients, not silently apply it to A[T].

## What would reopen the positive family

A new candidate must specify an actual group map with finite kernel and
finite-index image (then deal with the kernel), an actual finite-index
presentation isomorphism, or an independently verified common model. A
shared dimension, nonzero Euler characteristic, Garside formalism, complex
reflection catalog, or ambient embedding does not fulfill that contract.
No complete affirmative or negative answer to21.128 follows from this
family's work.
