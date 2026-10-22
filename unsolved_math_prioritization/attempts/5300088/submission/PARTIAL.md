# Convex-core ball radius versus rank: exact distinctions and five blocked routes

Problem 5300088 / AMR-052-0088. Research date: 2026-10-04.

**Disposition: unsolved, five substantive routes used.** This note does not prove or refute the requested rank-only bound. It records precise reductions, a quantitative negative control for a stronger statement, and the hypotheses of relevant published work. None of these results is claimed as novel. The Schottky mechanism below is a concrete version of the phenomenon in Fan, Remark 5.2.

## 1. Exact target and three different quantities

Let N be a complete hyperbolic 3-manifold of sectional curvature exactly -1, with finitely generated fundamental group. Write C(N) for the quotient of the hyperbolic convex hull of its limit set. Define

    r_C(N) = sup {r >= 0 : a hyperbolic open ball of radius r embeds isometrically in N with image contained in C(N)}.

The target is a finite upper bound r_C(N) <= R(n) for all such N with rank(pi_1 N) <= n. The number of generators need not be minimal: passing from exact rank to rank at most n only requires taking the maximum of finitely many constants. There is no fixed homeomorphism type, thickness hypothesis, finite-volume hypothesis, compactness hypothesis, or prescribed sharp formula. In particular, closed hyperbolic manifolds are included; there C(N)=N. The source's discussion of other dimensions is context, not an additional part of this target.

For x in C(N), put d_C(x)=dist_N(x,N\C(N)), with distance to the empty set interpreted as infinity. Then

    r_C(N) = sup_{x in C(N)} min(inj_N(x), d_C(x)).                 (1)

Indeed, every radius strictly smaller than both terms gives an embedded ball contained in the core. Conversely, an embedded contained ball centered at x has radius no larger than either term. Taking suprema removes any issue at a tangency or an unattained endpoint. This uses open metric balls; changing to closed balls leaves the supremum unchanged. The depth is zero for a lower-dimensional core.

The following statements are therefore different:

- White's global quantity inf_{x in N} inj_N(x).
- The stronger quantity sup_{x in C(N)} inj_N(x).
- The actual quantity r_C(N) in (1).

The second has no rank-only upper bound, even when the convex core is three-dimensional; Section 6 proves this explicitly. A theorem giving a lower bound on an embedded ball, or existence of one large ball, has the opposite quantifiers from the target. The imported earlier report confuses this direction; it cannot be used as resolution evidence.

The original primary statement is Bielefeld's 1990 list, Section 5, printed page 12, based on the November 1989 conference. It credits the question to McMullen and records the quasifuchsian and two-dimensional cases. [Bielefeld](https://arxiv.org/pdf/math/9201271#page=12)

### Orientation and elementary cases

The source uses Kleinian groups, hence the orientable setting. Even if the catalogue is read as allowing nonorientable N, this does not remove the difficult orientable subcase. Conversely, a bound in the orientable case would give one in the nonorientable case: the orientation double cover has rank at most 2n-1 by the index-two Schreier bound; finite-index groups have the same limit set, so the full preimage of C(N) is the cover's convex core; every embedded ball lifts. A monotone orientable bound at rank 2n-1 therefore bounds the original ball. Trivial or elementary groups have cores with no three-dimensional interior under the limit-set hull convention and contribute no positive-radius balls.

## 2. Route 1: carrier graphs and moving a short loop

**Mechanism.** Use a rank-n carrier graph and a short essential loop, then attempt to carry its length bound to every possible ball center.

White's Theorem 4.4 provides a rank-dependent upper bound on the global minimum injectivity radius of a closed hyperbolic 3-manifold, not on its maximum. The convention is stated explicitly in his introduction. [White](https://arxiv.org/pdf/math/0104191#page=1)

Here is the exact elementary loss in this approach. For any x,y in a complete hyperbolic quotient,

    inj_N(x) <= inj_N(y) + d_N(x,y).                              (2)

Choose a path from x to y with length arbitrarily close to their distance, append an essential loop based at y whose length is arbitrarily close to 2 inj_N(y), and return along the path. Conjugation preserves nontriviality, so dividing the new loop length by two proves (2). Reversing x and y proves that inj_N is 1-Lipschitz.

A rank-bound on the length of one essential loop is thus useful at x only if x is uniformly close to a short-loop basepoint. Rank alone does not bound diameter: start with a closed hyperbolic surface bundle with fiber genus g and take its cyclic covers N_m corresponding to powers of the monodromy. A presentation from the mapping torus gives rank(pi_1 N_m) <= 2g+1, whereas vol(N_m)=m vol(N_1). Since a radius-D ball in H^3 maps onto any closed quotient of diameter D,

    vol(N_m) <= pi (sinh(2D_m) - 2D_m),

and consequently D_m tends to infinity. The volume formula follows by integrating 4pi sinh^2(t) from 0 to D_m. A diameter shortcut to (2) is therefore impossible. This does not prove that the distance to the entire short-loop locus is unbounded; it identifies the stronger, missing estimate rather than asserting it.

**Exact gap.** Establish a rank-only coarse density statement for suitable short essential loops throughout the deep core. The existence of a bounded-complexity graph or a single short loop supplies no such statement.

## 3. Route 2: Heegaard sweepouts and area

**Mechanism.** Bound an embedded ball using the area needed for a sweepout surface to separate it, and then control the complexity of that sweepout by rank.

For a closed, connected, orientable hyperbolic 3-manifold of Heegaard genus g, Bachman--Cooper--White prove

    cosh(r) <= 2g                                                (3)

for every isometrically embedded radius-r ball. We use their unconditional Theorem 1.1, not its sharper inequality conditional on the then-unpublished Pitts--Rubinstein hypothesis. Their theorem also treats sectional curvature at most -1, but the target here remains constant curvature -1. [Bachman--Cooper--White](https://arxiv.org/pdf/math/0305290#page=2)

Thus a bound g(N)<=G(n) would give r_C(N)<=arcosh(2G(n)) for the closed case. The readily available inequality is rank(pi_1 N)<=g(N), in the wrong direction: it does not permit replacing g by n in (3). A logical numerical control is n=2, g=100; cosh(r)<=200 does not entail cosh(r)<=4.

Biringer's June 2024 research narrative still poses both the rank-to-Heegaard-genus bound and McMullen's closed-manifold question, and explains that the former would imply the latter. [Biringer, Section 2](https://ianbiringer.net/researchstatement.pdf)

**Exact gap.** A rank-only genus or equivalent sweepout-area bound. Taking this as a lemma merely transfers the unresolved issue to a stronger statement. No assertion is made that the two conjectures are equivalent, or that an arbitrary carrier graph thickens to a Heegaard splitting of the same genus.

## 4. Route 3: topology, boundary area, and filling the core

**Mechanism.** Use the rank-bound on boundary Euler characteristic and the bounded-area geometry of surfaces to fill the core.

For a connected compact orientable core M with nonempty boundary and no spherical boundary components, doubling gives chi(partial M)=2chi(M). With rational Betti numbers, b_0=1 and b_3=0, hence

    -chi(partial M) = 2(b_1-b_2-1) <= 2(n-1).                    (4)

When the boundary components all have nonpositive Euler characteristic, (4) bounds the sum of their negative Euler characteristics. It does not bound the number of torus components, the full topology of M, or the topology/area of an arbitrary Heegaard sweepout.

Fan's Corollary 5.1 obtains a rank-only pointwise injectivity bound for manifolds homotopy equivalent to a book of I-bundles. That topological hypothesis is essential to this cited result. Her Remark 5.2 warns that pointwise injectivity on the core fails in the compressible-boundary setting. [Fan](https://arxiv.org/pdf/math/9907058#page=19)

Bowditch's Theorem 0.1 bounds r_C(N) for fixed compact-core topology, without a thickness or convex-cocompactness restriction in the final theorem. His Theorem 1.1 uses a triangulation-complexity parameter; the proof treats compact cores first and later permits degenerate ends and cusps. A bound depending on the isomorphism class of pi_1 is still not a bound depending only on rank. [Bowditch](https://ems.press/content/serial-article-files/29640)

There is a rigorous obstruction to replacing that triangulation parameter by rank. If a closed hyperbolic 3-manifold has a triangulation with t tetrahedra, straightening its fundamental cycle gives

    vol(N) <= t v_3,

where v_3 is the maximal volume of a hyperbolic tetrahedron. Each straightened simplex contributes at most v_3 in absolute volume; summing proves the inequality. Applied to the cyclic covers in Section 2, t must tend to infinity although rank stays bounded. Thus no universal rank-only upper bound for this triangulation complexity exists.

**Exact gap.** Find filling surfaces or homotopies whose relevant geometry is rank-controlled even when triangulation complexity is not. Boundary area alone does not furnish them. The closed case makes the defect especially clear: it has empty boundary but can contain positive-radius embedded balls.

## 5. Route 4: the thick theorem, excision, and degeneration

**Mechanism.** Apply a complete solution under a global thickness assumption, then try to remove the thin regions or pass to a geometric limit.

Biringer--Souto, arXiv:1708.01774v2, Corollary 14.9, gives a bound F(n,epsilon) for r_C(N) if rank(pi_1 N)<=n and inf_N inj_N>=epsilon>0. The hypotheses and the still-general question occur together on printed page 6; the proof is on page 220. Section 1.1 assumes orientable complete manifolds. No compactness or cocompactness assumption is needed, but a positive global injectivity lower bound excludes cusps. [Biringer--Souto](https://arxiv.org/pdf/1708.01774#page=6)

The following necessary features of a hypothetical counterexample sequence are rigorous consequences.

**Proposition.** Fix n. If orientable complete hyperbolic N_j of rank at most n contain balls B_{r_j}(x_j) in their convex cores, with r_j tending to infinity, then:

(a) inf_{N_j} inj_{N_j} tends to zero;

(b) for each fixed epsilon>0 and the thin locus T_j(epsilon)={y: inj_{N_j}(y)<epsilon},

    dist(x_j,T_j(epsilon)) >= r_j-epsilon;                        (5)

(c) for each fixed s>0, the pointed radius-s neighborhoods around x_j are eventually isometric to B_s in H^3.

**Proof.** If (a) failed, some subsequence would have a common positive thickness lower bound and the cited corollary would bound its r_j, a contradiction. For (b), inj(x_j)>=r_j and (2) give d(x_j,y)>=r_j-inj(y)>r_j-epsilon for each thin y; take an infimum. For (c), choose j with r_j>s and restrict the given embedded ball. This proves local convergence to H^3 without any compactness theorem. QED.

This exposes the obstruction to excision: removing the thin part leaves these large balls intact, but the remaining manifold has boundary and is not complete, so the thick theorem no longer applies. Drilling produces cusps and still has global injectivity infimum zero. Arbitrary replacement/filling would require a separate rank bound and geometric control on the same large ball. A local thickness bound on that ball is already automatic and cannot be silently substituted for the global hypothesis.

**Exact gap.** An epsilon-independent mechanism controlling deep-core balls in the degenerating thin case. The available family of finite F(n,epsilon) does not prove that their supremum as epsilon decreases is finite. Nor is mere pointed convergence to H^3 contradictory: it forgets generators escaping the basepoint.

## 6. Route 5: an explicit rank-two large-injectivity construction

**Mechanism.** Try to refute the desired bound by making all based displacements large in a free group. The construction succeeds for pointwise injectivity but fails to put its large ball inside the core.

The following gives a quantitative version of the phenomenon identified by Fan. Fix q>=3 and L=log(q). In the Lorentz model

    H^3 = {x_0^2-x_1^2-x_2^2-x_3^2=1, x_0>0},  o=(1,0,0,0),

use Klein coordinates u=(x_1,x_2,x_3)/x_0. Put

    t=tanh L=(q^2-1)/(q^2+1),
    c=cosh(2L)=(q^4+1)/(2q^2),
    s=sinh(2L)=(q^4-1)/(2q^2).

Let A and B act linearly by

    A(x_0,x_1,x_2,x_3)=(cx_0+sx_1, sx_0+cx_1, -x_3, x_2),
    B(x_0,x_1,x_2,x_3)=(cx_0+sx_2, x_1, sx_0+cx_2, x_3).

Both are orientation-preserving isometries of H^3. A is a translation along the x_1 axis followed by a quarter-turn about that axis; B is a translation along the x_2 axis. Define the four closed halfspaces

    H_A^+={u_1>=t}, H_A^-={u_1<=-t},
    H_B^+={u_2>=t}, H_B^-={u_2<=-t}.

They have disjoint closures in the closed Klein ball since 2t^2>1. The maps A and A^{-1} pair the two A halfspaces in the standard ping-pong fashion; B and B^{-1} pair the B halfspaces. For example, the transformed u_1 is (s+cu_1)/(c+su_1), an increasing function taking -t to t. Let D be the common open exterior of the four halfspaces.

For a nonempty reduced word w in A^{+/-1},B^{+/-1}, induction from its last letter shows wD lies in the halfspace associated to its first letter. Therefore wD is disjoint from D. The same argument applied to h^{-1}g shows distinct translates of D are disjoint. Also w is not the identity, and all nontrivial w move o outside D, a neighborhood of o. Hence Gamma=<A,B> is discrete and free of rank two. Its action is torsion-free, and N_L=H^3/Gamma is a complete orientable hyperbolic manifold.

The radius-L ball about o lies in D, because its Klein coordinates satisfy |u|<t. It therefore embeds in N_L. Conversely, d(o,Ao)=2L. For p the image of o,

    inj_{N_L}(p)=L.                                               (6)

It remains essential to examine the core, rather than stop at (6). The limit set Lambda is in the union of the four ideal caps associated to these halfspaces: every nontrivial orbit point wo lies in one of the four halfspaces, and the same holds on taking limits. On each such ideal cap, |u_3|<=sqrt(1-t^2)=sech L. The hyperbolic convex hull is the Euclidean convex hull in the Klein model, so it lies in the slab

    |u_3|<=sech L.

The points +/-e_1 and +/-e_2 belong to Lambda as the fixed points of A and B. By Gamma-invariance, A(+/-e_2) also belong to Lambda; their Klein coordinates are

    (s/c,0,+/-1/c).

Combining each of these with -e_1 gives the interior hull points +/-q^{-2} e_3, since 1/(c+s)=q^{-2}. Thus the hull contains the octahedron with vertices +/-e_1, +/-e_2, +/-q^{-2}e_3. This octahedron contains the Euclidean ball of radius 1/sqrt(q^4+2), as its face planes have normal vectors (+/-1,+/-1,+/-q^2). In particular the convex core is genuinely three-dimensional, and p is an interior point.

Along the x_3 axis, hyperbolic distance from o to Klein coordinate z is atanh|z|. Since the preimage of the quotient core is exactly the invariant hull, the depth bounds descend to N_L:

    atanh(1/sqrt(q^4+2)) <= d_C(p)
       <= atanh(sech L) = log((q+1)/(q-1)).                        (7)

The upper bound tends to zero, while (6) tends to infinity. By (1), every ball centered at this p that is wholly in the core has radius at most the right side of (7). Notice that this is a bound at the distinguished point only; it is not an upper bound for r_C(N_L) over all centers.

**Exact gap.** A genuine counterexample must produce large injectivity and large core depth at the same point. This family has the opposite depth behavior. It rigorously refutes the stronger pointwise statement, including a full-dimensional-core version, but does not refute McMullen's question. The elementary ping-pong proof, not finite word enumeration, establishes discreteness and the all-words displacement conclusion.

## 7. Final assessment and next mathematical requirement

The general rank-only convex-core ball bound remains unproved and unrefuted by this attempt. The useful retained results are the exact radius/depth identity, the explicit full-dimensional Schottky control, the necessary thin-degeneration/escape conditions, and proof that a rank bound cannot simply replace triangulation complexity. Known special cases have been kept separate from the full target.

Primary-source searches through 2026-10-04 located the cited 2023 revised thick-case theorem, the 2024 author narrative, and current author publication lists, but no verified theorem removing thickness or replacing topology by rank. This is a dated search result, not proof of the absence of newer or unindexed work. Biringer's current publication list identifies the thick-case work with Memoirs of the AMS (2026); the publisher page was blocked. All theorem numbering and mathematical claims here refer to the inspected arXiv v2 text, without asserting that the final publication has identical pagination. [Author publication list](https://ianbiringer.net/)

The exact missing deliverable is either a uniform rank-only control of both terms in (1) in the degenerating regime, or a bounded-rank sequence with both terms tending to infinity at selected centers. No novelty, formal proof-assistant verification, or external peer review is claimed.
