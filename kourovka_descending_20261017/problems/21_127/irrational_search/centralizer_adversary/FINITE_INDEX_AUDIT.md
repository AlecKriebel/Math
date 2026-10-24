# Independent audit: explicit finite-index distortion

Completed 2026-10-24T20:51:11.183764+00:00. Assigned-review completion estimate: **100%**. Verdict: **PASS**. This audits a partial research barrier, not a complete solution of 21.127 or an originality claim. No human peer review is asserted.

## Schreier kernel and explicit word

The map F(a,b)->C3 sends a to a generator and b to zero, so its kernel H is normal of index3. The standard Schreier transversal 1,a,a² yields precisely A=a³ and B_i=a^i b a^{-i}, i=0,1,2. The rank is 1+3(2-1)=4. In this free basis w=[A,B0][B1,B2] is the usual single oriented boundary word of a genus-two, one-boundary-component surface Σ. It is a nontrivial reduced word in H and its image in F remains nontrivial by inclusion. Direct free reduction gives an 18-letter nonempty word, recorded in FINITE_INDEX_EXACT_CHECKS.json. There is no confusion between a multi-boundary chain and a single commutator-subgroup element here.

The standard surface-boundary theorem gives scl_H(w)=-χ(Σ)/2=3/2. This is the surface-boundary equality explicitly used in Calegari–Walker Example2.7 and the proof of Proposition2.9, not merely the upper bound supplied by one surface.

## Normal deck action and intersection form

Conjugation by a fixes A and sends B0->B1, B1->B2, B2->A B0 A^{-1}. Thus its homology matrix M fixes [A] and cycles the three [B_i]. The genus-two intersection form Ω pairs A with B0 and B1 with B2. Hence

    Ω(A,B0)=1, but Ω(MA,MB0)=Ω(A,B1)=0.

So M does not preserve Ω. It does not preserve -Ω either; the displayed test is 1 versus0 in both cases. Inner-automorphism ambiguity in the deck action has no effect on H1. If the given marked realization Σ were a cover of a marked oriented surface S inducing H->F, normality of H would realize this outer action by an orientation-preserving deck homeomorphism. Such a homeomorphism preserves algebraic intersection. This gives the required contradiction.

Changing the orientation of Σ replaces Ω everywhere by -Ω and leaves the contradiction. Even permitting an orientation-reversing candidate would not help, since M is neither symplectic nor antisymplectic. The geometry definition in the source uses oriented surfaces; a nonorientable base is not within that definition.

## Independent boundary-degree check

There is also a separate way to rule out a geometric cover, which checks the requested boundary/genus exception directly. A connected compact oriented base S with free fundamental group of rank2 has χ(S)=-1 and is either a once-punctured torus or a pair of pants. A cover of pants has at least one boundary component over each of its three base boundary components, so cannot equal the one-boundary Σ. For a punctured torus, the boundary class is a commutator in F, under every marking. The quotient F/H=C3 is abelian, so its boundary monodromy is the identity. Its three cosets therefore produce three boundary components, each covering the boundary with degree1. In particular a single degree3 boundary component is impossible. Thus allowing arbitrary positive covering degrees on boundary circles creates no exception. Euler characteristic would require genus2 if there were one boundary, but the actual boundary count is three and would instead require genus1.

## Primary theorem application and scope

I independently downloaded the frozen primary arXiv:1101.4055v1 PDF. It agrees byte-for-byte with the parent's cached source (SHA256 95529b0bb086bf296ee429b789c453a6fd9519e57dc65722474a6f7f74e55378). On printed p5, Example2.7 defines the exact notion of geometric realization used here and explicitly states strict decrease of boundary scl for a nongeometric realization. Its Proposition2.9 proof, printed p6, explains the strict inequality through finite-index transfer and distinct faces of the free-group scl ball. This is stronger than the bare existential statement that an inclusion fails to be isometric somewhere; the text specifically identifies the boundary of the chosen nongeometric realization. Since ∂Σ is the single word w here, the conclusion applies to the element itself:

    scl_F(w) < 3/2 = scl_H(w).

No exact ambient value is claimed or independently computed. Its rationality is the known free-group rationality theorem. The example proves failure of automatic scl preservation under a finite-index inclusion of finite RAAGs. It supplies no irrational value, no solution to 21.127, and no novelty claim.

## Verification artifacts

FINITE_INDEX_EXACT_CHECKS.json contains exact integer matrix multiplication, the order-three homology action, and free-word reductions. The proofs above supply the all-case justification, while the source manifest freezes the independent primary downloads. The preserved source statements and all hypotheses match this application.
