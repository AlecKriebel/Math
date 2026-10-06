# Kirby Problem 1.65 and the Legendrian slicing gap

## Result

The full problem remains unresolved in this investigation. One constructive approach, ordinary Morse slicing, stops before the required Lagrangian isotopy. The calculation below proves only that exactness and a regular height function do not automatically make interior slices Legendrian. It is an elementary diagnostic, with no novelty claim and no claimed counterexample to Kirby Problem 1.65.

## Exact target and scope

Problem 1.65 on printed page 63 of the 2026 K3 preliminary book asks whether each exact Lagrangian cobordism whose ambient height has no index-2 critical points admits a Lagrangian isotopy to a decomposable one. This is an authored paraphrase, not a transcription.

Source: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

The ambient setting is the four-dimensional symplectization of standard contact three-space. Write its coordinates as (t,x,y,z), contact form alpha = dz - y dx, Liouville form lambda = exp(t) alpha, and symplectic form omega = d lambda. The cobordism is a two-dimensional embedded Lagrangian surface with cylindrical Legendrian knot or link ends outside a compact region. Exactness means lambda restricted to the surface equals df, with the customary constant-end conditions; for links one must retain the relevant same-end primitive conventions when composing pieces.

The critical-point condition concerns the ambient height t restricted to the surface, not an arbitrary intrinsic Morse function on its abstract topology. Decomposable cobordisms concatenate the standard Lagrangian concordances associated with Legendrian isotopies, isolated standard maximal-tb unknot births, and the allowed oriented Legendrian surgery pieces. A literal Legendrian-isotopy trace generally requires perturbation to become a Lagrangian concordance, as Etnyre and Leverson note in Section 4, footnote 1. Arbitrary smooth bands or tangles have not thereby been certified as these pieces.

We do not identify smooth isotopy, Lagrangian isotopy, exact Lagrangian isotopy, and compactly supported Hamiltonian isotopy. The source states Lagrangian isotopy. Establishing only non-Hamiltonian-isotopy would not by itself refute that conclusion. Conversely, preserving the given ends and exactness would be a sufficient stronger construction, but is not assumed to follow automatically from a smooth isotopy.

## A necessary condition for a height slice to be Legendrian

Let i:L -> R x R^3 be an exact Lagrangian embedding, i*lambda = df. At a regular value c of t|L, let C be a connected component of the one-dimensional slice. Every v tangent to C has dt(v)=0. If pi is projection to R^3, then

alpha(d(pi composed with i)(v)) = exp(-c) df(v).

Therefore pi(i(C)) is Legendrian precisely when f restricted to C is constant. Indeed, projection on a fixed t-level is a diffeomorphism onto R^3, so this vanishing condition is exactly the Legendrian tangent condition. On a connected smooth one-dimensional manifold, df=0 is equivalent to constancy of f.

Exactness supplies a primitive f. It does not supply its constancy on an arbitrary interior slice. Constancy on the cylindrical ends does not add this missing condition at every regular interior height.

## Explicit exact local model

For (s,u) in R^2 define

F(s,u) = (t,x,y,z) = (s,u,s,(s+1)u).

This is a smooth embedding: its projection to (t,x) is the identity, which also proves that its differential has rank two. Pulling back the contact and Liouville forms gives

F*alpha = u ds + du,
F*lambda = exp(s)(u ds + du) = d(exp(s)u).

It follows that F*omega = d(F*lambda) = 0. Since the embedded surface has half the ambient dimension, it is Lagrangian, and the displayed primitive proves exactness. Its height is t composed with F = s, a submersion with no critical points of any index.

For fixed s=c, the slice projects to

u -> (x,y,z) = (u,c,(c+1)u).

The contact form on its tangent is alpha(partial_u) = 1. Thus this slice is not Legendrian, for every c. Equivalently, the primitive exp(c)u is nonconstant on the slice.

This is a local model, or an exact embedded plane if the entire parameter domain is retained. It has no cylindrical compact knot/link ends. It is not submitted as a global cobordism counterexample. Nor does a non-Legendrian slice obstruct the possibility of deforming the surface to have a useful Legendrian movie. Its sole role is to refute the automatic-slicing step in a proposed proof.

## The remaining geometric gap

Morse theory cuts a given surface into smooth products, births, and saddles when no maxima occur. To turn this into a proof of the target, one still needs a theorem producing suitable Legendrian intermediate levels and simultaneously making every critical region an allowed elementary exact Lagrangian piece, with compatible gluings and the required Lagrangian-isotopy conclusion. The local calculation shows why this theorem cannot be replaced by the observation that the height has no index-2 points.

The known smooth realization theorem also stops short. Etnyre and Leverson, Theorem 1.2, realize a smooth ribbon cobordism with nonempty negative end as decomposable after stabilizing its prescribed Legendrian ends. This does not identify an already-given exact Lagrangian embedding with that realization by a Lagrangian isotopy. Their Question 1.8 asks whether an existing Lagrangian ribbon cobordism with both ends nonempty can be stabilized to become decomposable. See https://arxiv.org/abs/2410.06305, pp. 2-3. Removing stabilizations and controlling a prescribed embedding are additional requirements, not consequences established here.

## Verification limits

The accompanying executable checks the displayed local polynomial differential identities using exact rational arithmetic. It checks negative controls and runs identically under Python optimization. It does not certify the existence of a global collaring isotopy, the full source papers, or the original open problem. The separate independent acceptance report reviews this local proof and its scope; it does not certify a global isotopy or settle the original problem.
