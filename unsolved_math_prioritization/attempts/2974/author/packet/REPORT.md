# Inequivalent pencils on a fixed symplectic four manifold

Problem 2974, KP-4.98, queue rank 1051. Research date: 2026-10-08.

## Result and scope

The universal multiplicity question is **not resolved here**. Five mathematical approaches give a concrete special-case construction, an exact conditional monodromy criterion, and obstructions to three proposed general constructions. No new universal theorem, counterexample, novelty, peer review, or formal certification is claimed.

The question concerns two, and more ambitiously infinitely many, inequivalent Lefschetz pencils of a common sufficiently high genus on each fixed closed symplectic four-manifold. The finite base set must be nonempty. Passing to a blowup or to a homeomorphic manifold does not establish the fixed-manifold conclusion. We use the usual oriented smooth equivalence: an orientation-preserving diffeomorphism of the total spaces takes base sets to base sets and intertwines the maps after an orientation-preserving diffeomorphism of the base sphere. No symplectomorphism is demanded. This convention is explicit in [B16, Introduction] and [LS26, Section 2.1]; [K3, p. 271] gives a shorter formulation. Varying critical values by reparametrizing the base therefore supplies no examples.

There is a quantifier issue worth making explicit, without using it as a purported solution. On standard symplectic CP2 a positive fiber class is dH and adjunction forces genus (d-1)(d-2)/2. Consequently not every sufficiently large integer is even an admissible genus. We address the intended multiplicity problem at a common large admissible genus; the literal all-integers reading already fails the existence requirement. We also distinguish a common compatible symplectic form from a theorem for every prescribed symplectic form.

For a pencil on X with fiber class F, genus h, b base points and r critical points, the basic identities are

    b = F.F > 0,
    2h - 2 = F.F + K.F,
    r = e(X) + b + 4h - 4.

The first uses transverse intersections at the base points; the second is symplectic adjunction; the third follows by blowing up the b points and counting the Euler contribution of each Lefschetz singularity.

## Current sources and inherited work

Lee and Servan's 2026 preprint gives an infinite fixed-genus family on either S2-bundle over a surface of genus q at least two. Its fiber genus is 2q, it has four base points and a constant fiber class, and one symplectic form works for the family. Its Section 7 gives other infinite families with homeomorphic total spaces, without identifying all their smooth structures. The stated ruled-surface theorem is a substantial special case, not a theorem for arbitrary X or every large admissible genus. [LS26, Theorems 1.2-1.3 and Section 7.]

Baykur's earlier constructions give multiplicity after blowups. Their exceptional-data mechanism and the distinction between Hurwitz equivalence and partial-conjugation equivalence were already analyzed in the supporting problem 11000156 packet. That work is credited and is not counted again. In the present problem partial conjugation is a construction to try, not an equivalence move that the resulting pencils must survive. [B16; B19; supporting audit linked in SOURCES.json.]

The present source check found no universal resolution. This is a bounded research finding, not proof that no unindexed result exists. The inspected arXiv history for [LS26] listed v1 only; the preprint's own general question remains unresolved there. Literature retrieval, normalization, gate screening, and arithmetic tests consume zero mathematical approaches.

## Approach 1  Change the integral fiber class without changing genus

The first construction attempts to find positive classes with equal adjunction genus but different divisibilities. Divisibility in the free part of H2 is preserved by every diffeomorphism, so it distinguishes pencils without computing their monodromy.

Let X=E1 x E2 be a fixed product of elliptic curves with a fixed product Kahler form. Write U=[E1 x {point}] and V=[{point} x E2]. These are members of a primitive integral basis in H2(X;Z), with U.U=V.V=0 and U.V=1. For integers a,b at least three, the class aU+bV is the Chern class, under Poincare duality, of a product line bundle. A degree-at-least-three line bundle embeds an elliptic curve: Riemann-Roch shows that removing any subscheme of length two lowers the section dimension by two. Taking the two embeddings and then the Segre embedding proves that the product line bundle is very ample.

A generic pencil in this linear system is Lefschetz. This is the standard generic-hyperplane theorem, not an asserted new existence theorem. Its regular fibers are connected by connectedness of ample hyperplane sections. Explicitly, if a smooth ample divisor split into disjoint nonzero effective divisors D1 and D2, ampleness would give D1.D1>0 and D2.D2>0 while D1.D2=0, contradicting the Hodge index theorem. All these pencils have holomorphic fibers for the same complex structure and hence symplectic fibers for the same chosen Kahler form. [AS04, Proposition 2.5.]

Since K_X=0, the numerical data and divisibility are

    h = ab + 1,    b_base = 2ab,    r = 6ab,
    div(aU+bV) = gcd(a,b).

For example, (a,b)=(3,12) and (4,9) give genus 37, 72 base points and 216 critical points, while their fiber divisibilities are 3 and 1. They are inequivalent pencils on the same symplectic T4.

This amplifies to arbitrarily many at a common genus. Take M to be the product of k distinct odd primes. For every divisor a of M with a>1, put b=M^2/a. Then a and b are at least three, a divides b, and their product is M^2. The 2^k-1 resulting pencils all have genus M^2+1 and 2M^2 base points. Their divisibilities are the distinct integers a. Thus a single fixed product symplectic T4 admits arbitrarily large finite sets of inequivalent equal-genus pencils, with the common genus allowed to grow.

This is an elementary special-case deduction using standard algebraic geometry, not a novelty claim. It does not produce an infinite family at one fixed genus. Nor does it extend to all X: on standard CP2 the class dH, its square d^2, and its divisibility d are determined by the genus once h>=1. Even the number r=3(d-1)^2 of critical points is then fixed. An arbitrary-manifold solution cannot rely only on these arithmetic distinctions.

## Approach 2  Move the pencil inside algebraic parameter spaces

The next idea holds a line bundle L fixed and varies the two-dimensional space of sections defining a pencil, hoping that different coefficients yield inequivalent maps. Let U_L be the locus of Lefschetz pencils in Gr(2,H0(X,L)), for a very ample L on a fixed connected projective surface. Transverse base intersections, ordinary nondegenerate critical points, and pairwise distinct critical values define a nonempty Zariski-open locus. The complex Grassmannian is irreducible, so this open set is connected and path connected in its analytic topology.

Here connectedness really gives smooth equivalence, rather than just an equality of numerical data. Choose a smooth path in U_L and trivialize the rank-two tautological bundle over the interval. The base points move in disjoint smooth paths. Blowing them up fiberwise gives a smooth family of compact total spaces with marked exceptional sections. The critical points and their images move without collisions. An isotopy of S2 identifies the critical-value sets; the parameter-dependent complex Morse lemma trivializes neighborhoods of the critical points. Away from those neighborhoods the maps are proper submersions, so horizontal lifts trivialize the family. Compatible lifts can be joined with a partition of unity, fixed in the chosen local neighborhoods. Blowing down the matched marked sections yields a smooth equivalence of the endpoint pencils on X.

Thus this coefficient-variation construction remains in one equivalence class. In particular every generic holomorphic plane pencil of a fixed degree belongs to the same class. This says nothing comparable about all symplectic pencils in that homology class.

There is a stronger obstruction conditional on the published classification statement [HH18, Theorem 1.1], which identifies holomorphic pencils of genus greater than five by genus and fiber divisibility, allowing different complex structures. For a genus-h pencil on T4, write F=dA. Its even intersection form gives A.A=2m for an integer m, and adjunction gives h-1=d^2 m. Hence d^2 divides h-1. There are only finitely many such d at any fixed h. Together with the cited classification, this gives finiteness of holomorphic equivalence classes at each h>5. In particular if h-1 is prime, every holomorphic pencil has divisibility one and the classification permits at most one equivalence class. The separate source-reading caveat below explains why this packet keeps this stronger conclusion source-conditional rather than claiming to have certified the published proof.

Under that classification, an infinite fixed-genus family on T4 in this range must contain infinitely many pencils that are not holomorphic for any complex structure. Independently of it, Approach 1 is intrinsically finite at a fixed genus because ab=h-1 has only finitely many positive factor pairs. The proved connected-linear-system obstruction also does not depend on the classification. The missing ingredient is a genuinely different construction, not more variation within a connected linear system.

## Approach 3  A general lattice criterion for partial conjugation

We attempt to extend the Johnson-homomorphism mechanism used in [LS26, Section 4]. The following abstract calculation is proved here in full; its use of partial conjugation is credited to that work. The extension keeps the original kernel image and isolates precisely when it can be removed without destroying an ambient conjugacy invariant.

Let Gamma be a group, N a normal subgroup, L a finite-rank free abelian Gamma-module, and tau:N -> L a Gamma-equivariant homomorphism. Let S be a finite subset of Gamma, G0=<S>, and f in N. For n>=0 define

    Gn = < S, f^n S f^(-n) >,
    Lambda0 = tau(G0 intersect N),
    v = tau(f),
    M = span_Z { g . (s^(-1) . v - v) : g in G0, s in S }.

Then the exact equality is

    tau(Gn intersect N) = Lambda0 + nM.                 (1)

Proof. Put a_s=s^(-1) f^n s f^(-n). Each a_s belongs to N and f^n s f^(-n)=s a_s. Let D be the subgroup generated by all g a_s g^(-1), with g in G0 and s in S. It is stable under conjugation by G0, contains every a_s, and is normal in <G0,D>. Thus Gn=D G0. Since D is contained in N, an element dx of Gn lies in N exactly when x belongs to G0 intersect N. Consequently

    Gn intersect N = D (G0 intersect N).

Equivariance and additivity give

    tau(a_s) = n(s^(-1) . v - v),
    tau(g a_s g^(-1)) = n g . (s^(-1) . v - v).

These generate tau(D)=nM, proving (1).

For a conjugacy-invariant quotient, suppose C is a **Gamma-invariant saturated** subgroup of L containing Lambda0. Saturated means L/C has no torsion. Let Q=L/C, and let Mbar be the image of M in Q. If Mbar is nonzero, all Gn are pairwise nonconjugate in Gamma.

Proof. In any integral basis of Q, define the content c(A) of a nonzero subgroup A to be the greatest common divisor of all coordinates of its elements, equivalently the largest positive integer c for which A is contained in cQ. Set c(0)=0. This definition is invariant under every integral automorphism of Q. Equation (1) implies that the image of tau(Gn intersect N) in Q is nMbar, with content n c(Mbar) for n>0 and content zero for n=0. Conjugation by Gamma induces integral automorphisms of Q, so two different n cannot have conjugate groups.

Both qualifications on C matter. Quotienting by an arbitrary initial image that is only G0-invariant does not give an invariant under unknown Gamma-conjugators. Quotienting by a nonsaturated subgroup can introduce torsion, where multiplication by n does not have the claimed content behavior. A canonical admissible choice is the saturation of the subgroup generated by all Gamma-translates of Lambda0; however, this may be all of L and leave no information.

A transparent nongeometric example shows the criterion can retain information even with Lambda0 nonzero. Take Gamma=Z^2 semidirect C2, with the involution sending (x,y) to (-x,y); N=Z^2 and tau the identity. Generate G0 by the involution and translation by e2, and let f be translation by e1. Then Lambda0=Ze2, M=2Ze1, and C=Ze2 is invariant and saturated. The kernel lattice is Ze2+2nZe1, and its quotient content is 2n. This example verifies the mechanism only; it is not a mapping-class factorization. If G0 already also contains translation by e1, the kernel is all of Z^2 for every n and the proposed distinction disappears.

For the pencil problem in genus at least three, take Gamma to be the closed mapping class group, N the Torelli group, and tau the Johnson homomorphism to (wedge^3 H)/H. A duplicated-block factorization whose unchanged and changed blocks each generate G0 can have precisely the groups Gn above. Positivity is retained by conjugation, but the construction must also establish all of the following:

1. The conjugator centralizes the product of the changed block in the mapping class group with the required boundary components, so the boundary multitwist relation is unchanged.
2. The relation still has nonempty base set, represented by disjoint sections of square -1 after blowing up.
3. Blowing those sections down gives the same smooth X for every n, not just equal Euler characteristic, signature, fundamental group or intersection form.
4. An admissible quotient C leaves Mbar nonzero; if a prescribed symplectic form is required, compatibility with that form must also be established.

Nonconjugacy of the resulting closed monodromy groups implies inequivalence of fibrations and hence of the pencils. This proves a sufficient criterion, not the existence of the required blocks or diffeomorphisms for every X. The ruled-surface preprint supplies geometry of this kind for its particular manifolds; the general case still lacks it.

## Approach 4  Transplant the known infinite family by fiber sum

One natural universal construction is to combine an arbitrary pencil with a known infinite family of genus-matched fibrations, and then try to recover the original X by blowing down exceptional spheres. Euler characteristic together with signature obstructs this construction in the relevant example.

Start with a genus-h pencil on X with b base points, and write Y=X#b CPbar2 for its associated fibration. Let Z be a genus-h fibration over S2 with r_Z critical points. The fiber sum W=Y#_F Z satisfies

    e(W) = e(X) + b + r_Z,
    sigma(W) = sigma(X) - b + sigma(Z).

Indeed e(Z)=4-4h+r_Z, removing the two fiber neighborhoods subtracts twice e(F), and signature is additive under this closed-boundary gluing. If k exceptional spheres are blown down, the resulting numbers are e(W)-k and sigma(W)+k. Equality with X would require simultaneously

    k = b + r_Z,    k = b - sigma(Z),
    hence r_Z + sigma(Z) = 0.                           (2)

Allowing extra ordinary blowups does not help: e+sigma is unchanged by either an ordinary blowup or blowdown, and its defect after the fiber sum is r_Z+sigma(Z).

The ruled-surface family in [LS26] has h=2q, e(Z)=8-4q, sigma(Z)=-4, and therefore r_Z=4q+4. The defect in (2) is 4q, which is positive. Even when an input pencil has the required matching genus, no sequence consisting only of ordinary blowups and blowdowns can turn this fiber sum back into the original oriented X. This is an obstruction to the proposed transplantation, not to other surgeries or to inequivalent pencils on X.

This argument does not reuse the earlier stable-classification cancellation attempt: it tests existence on a fixed X through the blowup-invariant number e+sigma. The missing alternative would be a gadget of zero defect, together with smooth-type and monodromy control, or a different operation changing the defect in a controlled way.

## Approach 5  Amplify at fixed genus by branched base change

Another way to retain the fiber genus is to pull back a fibration along a degree-d map from S2 to S2, with d>1 and all branch values regular for the original fibration. Starting again with Y=X#b CPbar2, denote the pullback by Y_d. Every original critical point has d unramified preimages, so r_d=d r and the fiber genus remains h.

The Euler formula gives

    e(Y_d) = d e(Y) + 4(d-1)(h-1).

For clarity one may take the cyclic map z -> z^d after choosing its two branch values away from the original critical values. The covering Y_d -> Y is branched along two disjoint regular fibers; the ramification surfaces upstairs are also fibers with normal Euler number zero. The branched-cover signature formula therefore has zero correction and yields sigma(Y_d)=d sigma(Y). [GKS21, Theorem 1.] More general branched base changes are unnecessary for this obstruction.

It follows that the defect of e+sigma relative to X is

    (e+sigma)(Y_d) - (e+sigma)(X)
       = (d-1) [ e(X)+sigma(X)+4h-4 ].                   (3)

Any sequence of ordinary blowups and blowdowns preserves this defect. Thus the proposed procedure can return to the oriented smooth X only if the bracket in (3) vanishes. It does not vanish for CP2 with h>=1, T4 with h>=2, or K3 with h>=1: the brackets are respectively 4h, 4h-4 and 4h+4.

There is also a separate section obstruction. The inverse image of each original (-1)-section is a section over the new base, but its normal line bundle is pulled back by a map of degree d. Its self-intersection is consequently -d. For d>1 these particular sections cannot be blown down as ordinary exceptional spheres to create the original pencil base points. Other exceptional spheres might exist; the numerical obstruction (3) already excludes a repair by ordinary blowups and blowdowns in the examples listed.

Thus increasing the covering degree provides more critical fibers on other four-manifolds, not a universal infinite family on the original X. No conclusion is claimed in the exceptional zero-bracket cases, and no statement about arbitrary rational blowdowns or other surgeries is implied.

## Exact remaining problem

The strongest concrete positive deduction here is finite multiplicity on one fixed product T4. The strongest structural deduction is the conditional lattice criterion (1), with a quotient that remains invariant under all ambient conjugators. Neither proves two pencils, much less infinitely many, on every fixed symplectic X at a common high admissible genus.

The missing universal construction must create a positive boundary-multitwist factorization with an effective inequivalence invariant while controlling the smooth total space after its (-1)-sections are blown down. Equal characteristic numbers, stabilization, homeomorphism, coefficient variation, fiber summing with the ruled example, and branched base change do not supply that control. Status: unsolved here, five substantive approaches completed.

## Reproducibility and limits

The source-free packet contains authored arguments, exact finite algebra and arithmetic checks, and public bibliographic and hash metadata. It contains no copied source bodies, dataset records, screenshots, or coordination material. The checker tests numerical identities, explicit T4 families, lattice content, and finite semidirect-product models of (1). It does not certify the general group-theoretic proof, mapping-class realizability, symplectic existence theorems, smooth classification, or the universal problem. External hashes are integrity pins, not signatures or a proof certificate.

## Source reading caveat

The proof of [HH18, Lemma 3.5, displayed p. 1527] treats a polarization of type (1,d) on an underlying product of elliptic curves as a product of degree-one and degree-d line bundles. That implication is not valid for an arbitrary polarization on the product. For the very ample degree-(4,9) product bundle used above, the alternating integral form is the direct sum of 4J and 9J, where J is the unimodular two-dimensional symplectic form. Its first elementary divisor is gcd(4,9)=1 and their product is 36, so its polarization type is (1,36). Both factor bundles nevertheless have degree greater than one, and its generic pencil is Lefschetz by the very-ample construction.

Thus the lemma's literal product exclusion needs a qualification, such as an appropriate decomposable-polarization hypothesis. This observation does **not** refute Theorem 1.1 or determine whether its proof is repairable; no such conclusion is used. The published theorem remains credited as a published statement, and all new unconditional deductions above avoid the problematic lemma. The bounded erratum search found no correction resolving this wording. This check is source auditing and adds no sixth mathematical approach.

## References

- [K3] R. Inanc Baykur, Robion C. Kirby, and Daniel Ruberman, K3 A New Problem List in Low-Dimensional Topology, 2026 preliminary version, Problem 4.98, PDF and displayed p. 271. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- [LS26] Seraphina Eun Bi Lee and Carlos A. Servan, Infinitely many Lefschetz pencils on ruled surfaces, arXiv:2602.10051v1, 2026. https://arxiv.org/abs/2602.10051
- [B16] R. Inanc Baykur, Inequivalent Lefschetz fibrations and surgery equivalence of symplectic 4-manifolds, Journal of Symplectic Geometry 14 (2016), 671-686. https://arxiv.org/abs/1408.4869 ; https://doi.org/10.4310/JSG.2016.v14.n3.a2
- [B19] R. Inanc Baykur, Inequivalent Lefschetz fibrations on rational and ruled surfaces, 2019. https://arxiv.org/abs/1806.00375 ; https://doi.org/10.1090/pspum/102/02
- [HH18] Noriyuki Hamada and Kenta Hayano, Topology of holomorphic Lefschetz pencils on the four-torus, Algebraic and Geometric Topology 18 (2018), 1515-1572. https://arxiv.org/abs/1603.08284 ; https://doi.org/10.2140/agt.2018.18.1515
- [AS04] Denis Auroux and Ivan Smith, Lefschetz pencils, branched covers and symplectic invariants, 2004 lecture notes. https://arxiv.org/abs/math/0401021
- [GKS21] Christian Geske, Alexandra Kjuchukova, and Julius L. Shaneson, Signatures of Topological Branched Covers, International Mathematics Research Notices 2021, 4605-4624. https://doi.org/10.1093/imrn/rnaa184 ; https://academic.oup.com/imrn/article/2021/6/4605/5880468
