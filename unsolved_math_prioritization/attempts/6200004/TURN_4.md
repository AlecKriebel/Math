# Turn 4: small-edge splittings and finitely presented subgroup obstructions

## Direction and outcome

We test whether assembling known hyperbolic pieces over small edge groups, or using the recent algebraically fibered examples, can create the missing coefficient gap. A counterexample survives inside a one-ended factor and inside a high-dimensional vertex of every finite cyclic splitting. At the first possible pair(2,4), the rational-dimension-two subgroup theorem excludes the new4-dimensional examples with finitely presented, non-F3 kernels. This does not exclude all high-dimensional fibered examples or finish the original.

## 1. Dimension bounds for a graph of groups

Let G be the fundamental group of a finite graph of groups with injective edge maps. For R=Z or Q set

    a_R=max_v cd_R(G_v),   b_R=max_e cd_R(G_e),

with the edge maximum omitted when there are no edges. Assuming these dimensions are finite, Bass–Serre cohomology gives

    a_R <= cd_R(G) <= max(a_R,b_R+1).           (1)

The lower bound is subgroup monotonicity: RG is free over each subgroup ring by a coset basis, so restriction of a projective resolution remains projective. For the upper bound, the augmented cellular chain complex of the Bass–Serre tree is the exact two-term complex of induced trivial edge and vertex modules. Resolving those modules and using induction/Shapiro gives the usual long exact sequence

    ... → product_e H^{k-1}(G_e;M)
        → H^k(G;M) → product_v H^k(G_v;M) → ...

for every RG-module M. Both exterior groups vanish once k>max(a_R,b_R+1), proving the bound. The finite products cause no exactness issue. This is the standard Bass–Serre argument, not a new theorem.

Suppose G is torsion-free hyperbolic and every edge group is finite or two-ended. Then the edge groups are trivial or infinite cyclic, so b_Z,b_Q<=1. Such edge groups are quasiconvex in G; Bowditch Proposition1.2 ensures that every vertex group is quasiconvex, hence hyperbolic. They inherit torsion-freeness.

If d=cd_Z(G)>=4, (1) forces some vertex v with cd_Z(G_v)=d. Subgroup monotonicity gives cd_Q(G_v)<=cd_Q(G)=q. Therefore

    q/d<2/3  implies  cd_Q(G_v)/cd_Z(G_v)<2/3. (2)

In fact once the vertex maximum over Q is at least2, (1) makes the rational dimension a maximum as well. No such small-edge splitting can be the first source of a ratio violation if all its vertices obey the bound.

## 2. Reduction to one end, and a qualified JSJ consequence

A hyperbolic group is finitely presented. The credited accessibility theorem splits it as a finite graph of finite or one-ended vertex groups over finite edge groups. Bowditch's Section6 recalls this and the quasiconvexity of the vertices. For a torsion-free group the finite edge and vertex groups are trivial. Applying(2) shows:

**If any source counterexample exists, a one-ended torsion-free hyperbolic counterexample exists with the same integral dimension and no larger rational dimension.**

The boundary of that one-ended group is a connected locally connected compactum without a global cut point, by the credited hyperbolic-boundary theorems summarized in Bowditch's introduction. These are extra conditions on a boundary-realization attempt. No assertion of absence of local cut points is made.

For a one-ended candidate, the closed-surface/Fuchsian exception has dimensions(2,2) and cannot apply. Bowditch Theorem0.1 supplies the finite cyclic JSJ splitting. Its two-ended and hanging-Fuchsian vertices have cohomological dimension at most1 in the torsion-free case; the hanging groups here are the bounded, hence virtually free, Fuchsian groups. A vertex carrying d>=4 in(2) must consequently be one of the remaining non-elementary quasiconvex vertices, type(3) in that theorem.

This does not show that this vertex has no cyclic splitting of any kind, or that an arbitrarily iterated splitting process terminates with an absolutely rigid group. Relative JSJ structure and unrestricted splitting are different claims. We retain only the precisely justified one-ended reduction and high-dimensional type(3) vertex consequence.

## 3. A strong obstruction at rational dimension two

Arora–Martínez-Pedroza, Theorem1.1 of the bound arXiv1811.09220v6, proves that every finitely presented subgroup of a hyperbolic group with cd_Q<=2 is hyperbolic. This is a cited external theorem; its statement and introductory deduction from the filling-function results were read, not a fresh recertification of the entire technical filling-function proof.

It follows that any torsion-free hyperbolic group containing a finitely presented nonhyperbolic subgroup has cd_Q>=3. In particular, suppose

    1 → K → G → Z → 1

has G torsion-free hyperbolic and K of type F2 but not F3. F2 means K is finitely presented. If K were hyperbolic, torsion-freeness would give it a finite classifying complex and hence type F3, a contradiction. Thus K is not hyperbolic and cd_Q(G)>=3.

For cd_Z(G)=3 this forces q=d=3. For cd_Z(G)=4 it gives q/d>=3/4. Neither case can answer the source.

The hypotheses apply exactly to CorollariesD and E of Italiano–Migliorini–Ng, arXiv2606.05091, whose statements were read: their dimensions3 and4 examples have kernels F2 but not F3. Finite integral cohomological dimension already forces torsion-freeness. This is a precise exclusion of those two low-dimensional families, not a claim that all algebraically fibered groups have equal rational and integral dimension. For higher d, the lower bound q>=3 alone does not imply q/d>=2/3. Nor is 'not F3' replaced by the distinct assertion 'not FP3 over Q'.

## 4. Source and proof limits

Bowditch's *Cut points and canonical splittings of hyperbolic groups*, ActaMath180(1998),145–186, was read at Theorem0.1, Proposition1.2 and its proof, the introductory boundary conventions, and Section6's accessibility application. These foundational accessibility and boundary results are credited dependencies. The finite-graph dimension inference is proved above from the standard tree cohomology sequence.

No arbitrary subgroup of a hyperbolic group is assumed hyperbolic. The quasiconvexity theorem provides it for the splitting vertices, and the Arora–Martínez theorem provides it only under its rational-dimension and finite-presentation hypotheses.

## 5. Exact controls and next gap

The checker verifies mapping-cone cochain dimension bounds for finite vector-space analogues of the tree long exact sequence, the preservation of a top vertex degree above edge contributions, and all bounded integer dimension profiles used in(2). These controls do not construct or recognize a hyperbolic group, prove accessibility or replace the cited subgroup theorem.

After four turns, all the concrete routes examined still satisfy the2/3 bound or fail an essential hypothesis. The final direction will test the tempting low-rational-dimensional Markov compacta against actual group-boundary conditions, rather than treating their dimension profiles alone as a realization.
