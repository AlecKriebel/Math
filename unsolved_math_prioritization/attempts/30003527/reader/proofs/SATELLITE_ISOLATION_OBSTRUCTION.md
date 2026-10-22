# A finite-entry-surface obstruction to isolated satellite families

Problem 30003527 / OWR-15575-006, queue row 1767. Authored 13 October 2026 UTC within shared substantive pass 2. This rules out the isolated realization of the explicit pass-1 satellite compactum; it does not resolve the unrestricted invariant-enlargement question. Independent audit is pending at the time of this draft.

## Result

Let O be an open subset of R³, let φ be a continuous full flow on R³, and let K⊂O be an isolated invariant compactum. Suppose {C_n} is a family of pairwise distinct clopen components of K, each homeomorphic to a circle. Let u∈H¹(O;Z). Write

u|C_n = w_n c_n,

where c_n is either generator of H¹(C_n;Z), so |w_n| is independent of that choice. Then the set of distinct integers {|w_n|: n≥1} is finite.

The result does not assume a smooth flow, nonvanishing dynamics, periodic motion on C_n, or connectedness of K. The circles may consist of equilibria or have any other invariant circle dynamics. The conclusion is about the winding magnitude of the circle as a subset of O.

Apply this with O=int T₀ and with the compactum X=Σ∪⋃_{n≥1}C_n from pass 1. Its circles C_n are clopen components of X, and their winding magnitudes in O are 3·2ⁿ. These are all different. Consequently:

**There is no continuous full flow on R³ for which that X is an isolated invariant compactum.**

In particular no choice of dynamics on the already constructed X, and no field gluing in its complement, can make X the isolated maximal invariant set sought in the pass-1 candidate. The conclusion is stronger than ruling out only standard odometer suspensions.

## Imported topological-flow inputs

J. J. Sánchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1, 27 March 2024:

- https://arxiv.org/abs/2403.18805
- https://arxiv.org/html/2403.18805v1

The inputs are:

1. Section 5.4: K has arbitrarily small tame compact 3-manifold isolating blocks N. In particular choose N⊂O. Write E=N^i for the compact orientable entry surface, D=N⁺ for the compact forward-invariant set, and L=n⁺=D∩E. The entry trace L is contained in the interior of E.
2. Proposition 5(ii): Ȟ^q(D,L;Z)≅H^q(N,E;Z). Thus these relative groups are finitely generated for every q. This is the relative pair (N,N^i), not (N,K); the latter need not have finite cohomology.
3. Theorem 13: a compact subset Y of the interior of a compact orientable surface, with finitely generated integral Ȟ⁰ and Ȟ¹, has a compact surface neighborhood P with Y→P inducing cohomology isomorphisms. Applying the result inside an arbitrarily small compact surface neighborhood gives the same conclusion there. In particular, if Ȟ⁰(Y)=Ȟ¹(Y)=Z, such a neighborhood P is a connected annulus.

The final implication in input 3 follows from the classification of compact connected orientable surfaces. The isomorphism in degree zero forces P to be connected; rank H¹(P)=1 then forces genus zero and exactly two boundary components. No assertion about singular H₁(Y) is needed.

These inputs apply to merely continuous flows. The following deductions are written out and do not invoke a theorem asserting movability of an arbitrary isolated set.

## 1. Stable clopen pieces corresponding to the circles

First D·[0,∞)⊂D, the compact sets D·t decrease with t, and their intersection is K. Hence, for every neighborhood V of K relative to D, there is a T such that D·[T,∞)⊂V. This is a compactness argument for nested compact sets.

For each n, decompose K=C_n ⊔ (K\C_n), a disjoint union of compact invariant sets. Choose disjoint closed neighborhoods U_n and U'_n of these two sets relative to D, whose union contains a relative neighborhood of K. For some T_n,

D·[T_n,∞) ⊂ U_n ∪ U'_n.

Set D_n={p∈D: p·T_n∈U_n}. Its complementary piece is {p∈D:p·T_n∈U'_n}. These two pieces are disjoint closed subsets covering D, so D_n is compact and clopen in D. A forward semiorbit after T_n is connected and remains in U_n∪U'_n, so it cannot switch pieces. Equivalently,

D_n={p∈D: ω(p)⊂C_n}.

Here ω(p) is nonempty, compact, and connected because the forward semiorbit remains in compact D. This characterization shows that D_n is independent of the chosen neighborhoods and time, is positively invariant, and satisfies D_n∩K=C_n. It also shows that different D_n are disjoint.

Put L_n=D_n∩L. For every finite collection J of indices,

(D,L) = ⨿_{n∈J}(D_n,L_n) ⊔ (D_J',L_J'),

where D_J'=D\⋃_{n∈J}D_n and L_J'=L∩D_J'. This is a finite disjoint decomposition into compact clopen pairs.

The inclusion C_n→D_n induces an isomorphism on integral Čech cohomology. To check this directly, set Y_k=D_n·k. These are nested positively invariant compacta whose intersection is C_n. Every inclusion Y_{k+1}→Y_k is a homotopy equivalence: the time-one map provides an inverse up to the time-[0,1] flow homotopies, confined respectively to Y_k and Y_{k+1}. Čech continuity now gives the asserted isomorphism induced by inclusion. In particular

Ȟ⁰(D_n;Z)=Z and Ȟ¹(D_n;Z)=Z.

No actual retraction D_n→C_n is asserted.

## 2. All but finitely many relative pieces are acyclic in the needed degrees

Fix q∈{0,1,2} and let R_q=Ȟ^q(D,L;Z), a finitely generated abelian group by input 2. Finite additivity for compact clopen pairs gives, for every finite J,

R_q ≅ (⊕_{n∈J} Ȟ^q(D_n,L_n;Z)) ⊕ Ȟ^q(D_J',L_J';Z).

Consequently there are only finitely many n with Ȟ^q(D_n,L_n;Z)≠0. Here is the elementary algebra, including torsion: write R_q≅Z^r⊕T with T finite. In any finite direct-sum decomposition of R_q, at most r nonzero summands have positive rank. Every remaining nonzero summand is a nontrivial finite group. The product of the orders of their torsion groups divides |T|, so there are at most log₂|T| of those. If arbitrarily many indices had nonzero groups, a sufficiently large finite J would violate this bound.

Take the union of these three finite exceptional sets and call it F. For n∉F, the exact cohomology sequence of (D_n,L_n) gives isomorphisms, induced by inclusion,

Ȟ⁰(D_n;Z) ≅ Ȟ⁰(L_n;Z),
Ȟ¹(D_n;Z) ≅ Ȟ¹(L_n;Z).

Therefore L_n is a nonempty connected compact subset of the interior of E and Ȟ⁰(L_n)=Ȟ¹(L_n)=Z. By input 3 it has arbitrarily small annular neighborhoods in E.

The argument does not split off the non-clopen limiting solenoid component, and does not assume that component is isolated. Only the genuinely clopen circle components are used.

## 3. Entry annuli reproduce the ambient winding

Take any finite J disjoint from F. The compact sets L_n, n∈J, are pairwise disjoint, so choose pairwise disjoint compact surface neighborhoods around them inside int E. Apply input 3 separately inside those neighborhoods. This gives pairwise disjoint annuli P_n⊂int E, with inclusion L_n→P_n inducing a Čech H¹ isomorphism. Let τ_n be a core circle of P_n.

Restrict the ambient class u along the inclusions into O. The diagram consists of

C_n → D_n ← L_n → P_n ← τ_n.

Every indicated arrow induces an isomorphism on integral first cohomology. The first isomorphism was proved in Section 1; the second comes from the relative vanishing in Section 2; the third comes from input 3; the fourth is the usual core equivalence of an annulus. The restrictions of u agree after pullback because all these are actual subspace inclusions into O. Thus u|τ_n has coefficient ±w_n with respect to a generator of H¹(τ_n;Z).

This uses Čech cohomology of L_n throughout. It does not replace Čech cohomology by singular homology for a possibly wild entry trace.

## 4. A fixed compact surface bounds distinct winding magnitudes

A compact orientable surface E has a finite bound b(E) on the size of a collection of pairwise disjoint, pairwise nonisotopic essential simple closed curves, allowing boundary-parallel curves. This is the elementary multicurve bound from the classification of compact surfaces: a pants decomposition bounds the non-boundary-parallel classes, and there are at most as many boundary-parallel classes as boundary components. Disks, spheres, annuli, and tori are checked separately. For example, the deliberately loose finite bound

b(E)=Σ_i max(1,3g_i+2b_i)

suffices, where g_i and b_i are the genus and number of boundary components of each component E_i.

If w_n≠0, then τ_n is essential in E: a curve nullhomotopic in E has zero restriction of every class pulled back from O. If |w_n| and |w_m| are distinct, τ_n and τ_m cannot be isotopic in E, even after orientation reversal, because isotopic curves have the same absolute evaluation of u.

If infinitely many different nonzero |w_n| occurred for n∉F, choose b(E)+1 such indices. Section 3 produces disjoint essential curves in E with pairwise distinct magnitudes, hence pairwise nonisotopic. This contradicts the surface bound. The indices in F contribute only finitely many extra values, and zero contributes at most one. The theorem follows.

## 5. Application and exact scope

In the explicit satellite construction, every C_n is separated by positive distance from the compact remainder X\C_n. It is therefore a clopen component of X. The open torus O=int T₀ has H¹(O;Z)=Z; a generator restricts with absolute degree 3·2ⁿ to C_n. The theorem proves that X cannot be isolated under any continuous full flow.

This does not rule out simultaneous invariance of Σ and the C_n under a flow that has additional invariant structure nearby. It also does not show that every larger invariant set must be movable. In particular the obstruction does not solve the full target, which permits an arbitrary compact invariant A, arbitrary open U⊃A, and any compact invariant movable B with A⊆B⊆U.

The next realization attempt must either use a different nonmovable compactum, abandon isolation and nevertheless exclude all admissible invariant supersets, or produce a general enlargement theorem. Merely preserving the same X and trying a more elaborate continuous vector field cannot repair the isolated-X route.

## Source and inspection note

The cited arXiv HTML was inspected in this pass for Proposition 5(ii), the proof of Theorem 14 describing the stable clopen decomposition, Theorem 13, and the block-existence argument in Section 5.4. The pass-1 PDF verification metadata remains applicable. No remote mutation, external communication, or source-body publication was made.
