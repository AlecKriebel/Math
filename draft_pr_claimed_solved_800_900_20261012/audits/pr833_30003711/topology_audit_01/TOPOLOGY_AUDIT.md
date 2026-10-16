# PR833 / problem 30003711: independent geometric and topological audit

Audit date: 2026-10-15 UTC. Decision: **CLEAR for the assigned geometry/topology family, conditional on the spectral/common-fixed-sheet lemma assigned to the separate group family.** No mandatory mathematical repair was found in §§2, 4, 5, or 6 of the supplied proof. This decision is not an independent certification of every group computation or of novelty.

The exact curated target is ordinary, unnormalized section-based Schwarz genus 8 (normalized sectional category 7) for the nine-flex cover over the coefficient space X=CP^9 minus the cubic discriminant. The geometry establishes the required upper bound if the separate group lemma passes. Equality additionally requires a sound lower bound; a late dependency challenge to the inspected preprint is now open, as recorded in LOWER_BOUND_DEPENDENCY_ADDENDUM.md. It does not settle the stronger connected/full-nine-sheet-trivialization interpretation of the original OWR question or an exact branching-complexity invariant.

## 1. Independence and frozen input

I read all of the complete queue JSON and the supplied author PROOF.md, then saved INDEPENDENT_RECONSTRUCTION.md before opening any earlier independent_audit or second_review verdict. Those earlier verdicts remain unread. The geometry/topology argument below was reconstructed directly from the author proof and checked against primary sources, without finite-group tests or old AI verdicts standing in for mathematics.

The supplied PROOF.md has SHA256 c42d7adb46caa0fd5fbaa4ad6006baf711a2a6674a69375671fa9cd86141b965. A read-only extraction of unsolved_math_prioritization/attempts/30003711/author/PROOF.md at frozen commit 0e6e23213494ecb4a7208f920d25d7b49502a5cb has exactly the same hash. The ambient main checkout had advanced to fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9 before this lane began; the frozen proof, rather than ambient changes, was audited. No branch, Git index, queue, PR, or service was changed by this lane, and no outreach occurred.

## 2. Hesse parameterization and the actual pullback

Write a=x^3+y^3+z^3, b=xyz, F_lambda=a-3lambda b. The projective pencil includes the member b=0 at infinity. That is a union of three lines, so removing infinity loses no smooth cubic. For finite lambda, the partial equations are x^2=lambda yz and cyclic permutations. If one coordinate vanishes at a singular point, all three vanish, which is impossible in projective space. Otherwise multiplying gives lambda^3=1. Conversely the familiar three-line factorizations at cube roots of unity are singular. Thus the smooth parameter set is exactly T=C minus {1,omega,omega^2}.

The classical existence of a Hesse form for every smooth plane cubic is the external input. The rest of the quotient identification can be checked without treating exceptional parameter values as generic. Its common nine-point set consists of the solutions of a=b=0, and is the flex set for every smooth member. If a projectivity u maps F_lambda to F_mu, it maps their flex sets, hence preserves S. To see that this preserves the whole pencil, let Q be any cubic through S. On z=0 its restriction is a multiple of x^3+y^3, since it vanishes at the three roots of that polynomial in P^1. This kills x^2y,xy^2 and equates the x^3,y^3 coefficients. Applying the same argument on x=0 and y=0 kills the other four mixed monomials with one zero exponent and equates all pure cube coefficients. Therefore Q=c a+d b. This proves that the cubics through S form exactly the pencil. Consequently u belongs to its Hessian symmetry group Gamma.

Use the point action u.F(x)=F(u^{-1}x), and let u.lambda denote the induced parameter action. The **right** action giving the fibers is

    (g,lambda).gamma=(g gamma,gamma^{-1}.lambda).

Indeed (g gamma).F_(gamma^{-1}.lambda)=g.F_lambda. Conversely, if g.F_lambda=g'.F_mu, then gamma=g^{-1}g' preserves S and lies in Gamma, and mu=gamma^{-1}.lambda. Hence X=(P x T)/Gamma as a topological space, where P=PGL3(C). The action is free because its first-coordinate action is free, even if a parameter has a nontrivial stabilizer. The quotient is a real 18-manifold; the induced continuous bijection to the real 18-manifold X is a homeomorphism by invariance of domain. Only this topological conclusion is required. The same argument with the marked flex p0 replaces Gamma by its stabilizer Gamma_0 and yields Y=(P x T)/Gamma_0.

The finite group acts on the whole projective pencil and permutes the four singular members, so its action preserves T. A nonfaithful parameter action or special j-value introduces no extra identifications beyond the already free diagonal action. The four missing projective parameters must be counted; calling T a punctured affine line is correct precisely because infinity is the fourth singular parameter.

Now let G=PU3. For a matrix representative A of g in P, put U(A)=A(A* A)^(-1/2). Direct functional calculus gives

    U(cA)=(c/|c|)U(A),
    U(AV)=U(A)V     (V unitary).

Thus r(g)=[U(A)] is well-defined modulo C* and satisfies r(g gamma)=r(g)gamma for gamma in Gamma contained in G. In fact A(A*A)^(-t/2), 0<=t<=1, gives a well-defined right-G-equivariant strong deformation on projective matrices; changing A to cA only multiplies it by the scalar c|c|^(-t).

Define f([g,lambda]_Gamma)=r(g)Gamma and F([g,lambda]_Gamma0)=r(g)Gamma_0. These are well-defined continuous maps making the square with p:G/Gamma_0 -> G/Gamma commute. Above x=[g,lambda]_Gamma, the points of Y are

    [g gamma,gamma^{-1}.lambda]_Gamma0,  gamma Gamma_0 in Gamma/Gamma_0.

Their images are r(g)gamma Gamma_0. Right cancellation shows this is a bijection onto p^{-1}(f(x)), including at every exceptional parameter. A morphism of covering spaces that is a fiber bijection is locally an isomorphism of their discrete trivializations. This verifies that Y is the **actual pullback** f*E; a mere commutative square would not have sufficed.

Gamma is finite and acts freely on G by right multiplication, so M=G/Gamma is a compact smooth real 8-manifold. E=G/Gamma_0 is its genuine nine-sheeted covering. Neither M nor X is the coarse moduli space of cubic curves. A section cover on M pulls back to a section cover on X.

## 3. Circle stabilizers and orbit sections

Here is the exact group-theoretic interface required from the other family: every gamma in Gamma with a repeated projective eigenvalue fixes a flex, equivalently the author's Lemma 1. It is enough for this statement to hold in the given faithful projective unitary representation. A representation of the abstract group without this property would not suffice.

The circle H={[diag(1,z,z)]: |z|=1} embeds in PU3: scalar equivalence of two such diagonal representatives forces the scalar to equal 1 by the first entry. At m=gGamma its stabilizer is L_m=H intersect gGamma g^{-1}, a finite subgroup of a circle. Therefore it is cyclic. Under conjugation by g it is J_g=Gamma intersect g^{-1}Hg. If J_g is nontrivial, a generator has eigenvalue multiplicities (1,2); the hypothesis gives a fixed flex, and the entire cyclic subgroup fixes that same flex. For the trivial subgroup any flex works. This is a common fixed point, not the invalid inference from separate fixed points for an arbitrary finite group.

Explicitly identify p^{-1}(m) with Gamma/Gamma_0 by gamma Gamma_0 -> ggamma Gamma_0, and with S by gamma Gamma_0 -> gamma p0. If h in L_m corresponds to j=g^{-1}hg, then h(g gamma Gamma_0)=g(j gamma)Gamma_0. Thus the relevant action on the fiber really is the same flex action as in the group lemma, with no missing inverse. Opposite monodromy conventions replace a subgroup by its inverse and do not alter its common fixed set.

Choose a fixed point e of this action. The map H -> E, h -> he, factors through H/L_m and is continuous. Since H/L_m -> Hm is a continuous bijection from a compact space to a Hausdorff space, it is a homeomorphism. It follows that s_m(hm)=he is a continuous section on the entire orbit. The orbit is an embedded compact circle: proper smooth compact-group actions have embedded orbits, and its dimension is 1 because L_m is finite. There is no zero-dimensional orbit or fixed point of H.

## 4. Extension over saturated neighborhoods, including exceptional orbits

Average any Riemannian metric over compact H. The normal bundle of the compact orbit has an H-equivariant exponential tubular neighborhood W_m. Compactness permits a positive uniform radius, and the resulting disk bundle and its image can be chosen H-invariant. Its radial contraction defines R:W_m x [0,1] -> W_m with R(w,0)=w and R(w,1)=rho(w) in Hm. It fixes the orbit.

The direction of homotopy lifting matters. Put K(w,t)=R(w,1-t), so K(w,0)=rho(w), K(w,1)=w. Start its covering lift at s_m(rho(w)). The covering homotopy property of the genuine covering E->M produces a continuous lift Ktilde with p Ktilde=K. Then s_W(w)=Ktilde(w,1) satisfies p s_W(w)=w. This is a section on **all** of W_m, with the given orbit section as its restriction.

No assertion that E/H -> M/H is a cover enters this argument. The section need not be H-equivariant; ordinary covering homotopy lifting is enough. Exceptional orbit types cause no failure. In slice notation a neighborhood is H x_(L_m) D(V), with finite L_m and a real 7-dimensional normal representation V. Radial contraction is well-defined in that model even as stabilizers of points in D(V) become smaller. The selected orbit sheet extends along normal radial paths. A hypothetical ineffective kernel merely sits inside each finite L_m and is already included in the common-fixed-sheet requirement; effectiveness is not a hypothesis. In this specific PU3 setting the kernel is actually trivial, but that extra fact is unnecessary.

The quotient map q:M->B=H\M is open: for open A, its saturation is q^{-1}q(A)=union_(h in H) hA, which is open. Since W_m is saturated, U_m=q(W_m) is open and q^{-1}(U_m)=W_m. Thus there is an open cover of B with sections on the full inverse images. There is no need to choose neighborhoods with an unchanged orbit type.

## 5. The dimension bound is valid under the actual hypotheses

Left H and right Gamma multiplication commute, so B is homeomorphic to (H\G)/Gamma. The left action of H on G is free and proper. Consequently H\G is a compact smooth real 7-manifold. Right multiplication by Gamma acts smoothly on it, whether or not this action has fixed points.

B is compact metrizable. For example choose a bi-invariant metric on compact G and minimize distance over the compact H x Gamma orbits; disjoint compact orbits have positive distance. The resulting orbit metric induces the quotient topology. This also makes B normal and paracompact.

The exact external triangulation result is Illman 1978, the opening theorem on p.199, existence clause (1), or the more general pair statement Theorem 3.6 on p.216 with N empty. Its hypotheses are a **finite group** acting smoothly on a smooth manifold (with or without boundary). Here the finite group is Gamma and the manifold is H\G. It is not a theorem being applied to the original nonfree circle action.

Moreover Illman's definition of equivariant simplicial complex on p.201 includes the regularity conditions needed for the orbit complex to be an ordinary simplicial complex; that page explicitly identifies its quotient complex and states that simplex dimension is preserved. For a raw simplicial group action, he notes that the second barycentric subdivision has the needed conditions. Thus there is no hidden reliance on a first subdivision merely removing inversions. Compactness and local finiteness give a finite triangulation. Its dimension is 7, and its quotient has dimension at most 7. Therefore B has covering dimension at most 7.

This verifies the author's intended triangulation argument more precisely than the phrase “after subdivision.” It does not use the false general assertion that every finite-to-one continuous image has dimension at most its source. One could also use the finite **open** quotient dimension theorem appearing in Illman's proof, but that alternative is not needed.

## 6. The eight domains and continuity of their sections

Choose a finite subcover U_1,...,U_r of B by the orbit neighborhoods above. Covering dimension <=7 for a compact metric space means this finite open cover has a finite open refinement V_1,...,V_n of multiplicity <=8. For each j select i(j) with V_j contained in U_i(j). A subordinate partition of unity phi_j can be chosen with {phi_j>0} contained in V_j.

Let N be the nerve of the V_j and let f(b)=sum_j phi_j(b)e_j in |N|. Nonzero coordinates give a nonempty intersection of their V_j, so f does take values in the nerve. The multiplicity bound implies dim N<=7. Via the canonical homeomorphism |sd N|=|N|, each subdivision vertex is b_sigma for a nonempty simplex sigma of N. Color it by dim sigma.

An open star consists of points in relative interiors of simplices containing that vertex. Two distinct vertices b_sigma,b_tau of equal color cannot share such a simplex: subdivision simplices are chains of strict inclusions of the original simplices, and equal-dimensional distinct simplices are not comparable. Hence their open stars are disjoint. All open stars cover |N|, and their inverse images W_sigma cover B.

Fix any original vertex j(sigma) of sigma. On the open star of b_sigma its subdivision barycentric coordinate is positive. In original coordinates b_sigma has coordinate 1/|sigma| at j(sigma), while every other contribution is nonnegative. Thus original coordinate j(sigma) is strictly positive throughout that star. Therefore

    W_sigma subset {phi_j(sigma)>0} subset V_j(sigma) subset U_i(j(sigma)).

Restrict the known section over q^{-1}(U_i(j(sigma))) to q^{-1}(W_sigma). For k=0,...,7 define Z_k as the union over dim sigma=k of these inverse images. Each Z_k is open; together they cover M. The pieces in a fixed Z_k are pairwise disjoint and open, so the piecewise section is continuous: the inverse image of any open subset of E is the union of its open inverse images on the pieces. In particular there is no boundary matching condition. There are only finitely many pieces here; even an infinite disjoint open family would give the same continuity conclusion. Unused colors can be omitted or represented by empty open sets, and only improve the bound.

This constructs <=8 open section domains for E->M. Pullback gives <=8 for Y->X. No connectedness or full-sheet labeling property has slipped into the construction. For example a nontrivial cyclic orbit monodromy can fix one flex and move the other eight; its orbit neighborhood then has a section but does not trivialize all sheets. This explains exactly why the stronger invariant cannot be inferred.

## 7. Lower bound and obstruction interfaces

The external lower bound used is Chen–Wan arXiv:2306.17303v2, Theorems 1.2 and 4.1. I read the full ten-page v2 and visually checked its convention and relevant statements. Its X is explicitly the coefficient discriminant complement, and its genus is defined by open section domains. Thus the theorem's hypotheses match this problem, rather than a quotient by coordinate changes. The classifying-cover criterion in Theorem 2.4 applies to the auxiliary regular translation cover, not incorrectly to the nonregular flex cover. The auxiliary subgroup K acts freely and transitively on the nine flexes of the smooth Fermat cubic, giving the needed pullback. Its proof claims degree-7 mod-3 detection for lower bound 8. The theorem statement and its input conventions match, but a late adversarial challenge to that detection argument is open; the theorem is not independently accepted by this lane merely because its statement was read. See LOWER_BOUND_DEPENDENCY_ADDENDUM.md. This lane does not claim an independent reconstruction of Leary's original calculation. See [the inspected v2](https://arxiv.org/pdf/2306.17303v2).

Conditionally on the group lemma, the construction gives g(Y/X)<=8 and g(E/M)<=8. If a sound lower bound 8 is additionally established, equality follows and the normalized value is 7. With the new lower-bound challenge unresolved, this lane does not certify equality.

For completeness the obstruction aside follows directly from the constructed section domains. On the paracompact manifold X, choose a subordinate partition of unity for their pullbacks; use the local sections as the eight join coordinates with those weights. This gives a section of the actual eightfold fiberwise join. For a nine-point set S put I=ker(Z[S]->Z), free of rank 8. The augmented chain complex of a join shows Htilde_7(S^{*8})=I^{tensor 8} and all lower reduced homology vanishes. The join is 6-connected, so Hurewicz identifies pi_7 with this tensor product. Its rank is 8^8=16,777,216. With the factors in fixed order, monodromy acts diagonally by the original sheet permutation; there is no factor-permutation sign. Opposite left/right conventions give the corresponding inverse transport convention, not an untwisted constant system.

Consequently the first obstruction is in H^8(X;I^{tensor 8}), as asserted. An actual global join section forces this canonical primary obstruction to vanish. The argument makes no claim that every arbitrary choice of a partial section has a zero obstruction cocycle, nor does it need to deduce higher obstruction vanishing from a vanishing pullback of an unrelated class.

## 8. Adversarial checks, scope, and remaining gap

The dimension-to-eight-colors step is a general elementary consequence of covering dimension. Orbit-section extension is a standard covering homotopy argument. Their classical nature does not establish an earlier resolution of the specific Hessian problem. No broad priority audit was performed here. Chen–Wan's final remark rules out their freely descending cover method for the larger group because conjugates intersect the circle; the present method expressly tolerates those intersections when they fix a sheet. Thus that remark is not a counterexample or contradiction to this proof, and the stated lower bound 8 would be respected exactly if it is validated.

As a source caution outside the dependencies of the new upper bound, v2 §5 contains an erroneous claim that the Fubini–Study metric is invariant under all PGL3(C). Its invariance group is projective unitary. A diagonal projectivity with unequal positive scale factors changes distances and can bring two distinct points arbitrarily close. This does not occur in the degree-7 classifying-space lower bound of §4, and no algorithmic conclusion in this audit uses §5. The final published text was unavailable, so I do not assert that the same issue occurs in that version.

The author's use of “its projective symmetry group” must be read as the symmetry group of the **pencil**, not the automorphism group of a single generic cubic. Its subsequent quotient formulas and references fix that intended meaning. Making the wording “the pencil's projective symmetry group” would be useful editorial clarification, but is not a central missing argument.

**Strongest verified result in this lane:** conditional on the spectral lemma/common-fixed-sheet conclusion for the actual Hessian action, the full authored geometric construction yields g(Y/X)<=8 in the exact curated convention. Equality still requires the separately challenged lower bound. Every assigned geometric, neighborhood, dimension, coloring, and obstruction interface passes.

**Exact remaining gap for a combined release decision:** the separate group family must certify the spectral lemma for the actual projective representation, and the lower-bound family must resolve the newly identified challenge to the degree-7 detection. This lane checked the group interface and found no obvious defect, but deliberately does not substitute for those independent families. There is no additional topological repair to the upper-bound construction to perform. The original connected/full-trivialization invariant and exact branching complexity remain unaddressed, and no novelty conclusion is supplied.

## 9. Source inspection receipts

SOURCE_LEDGER.json records versions, byte counts, hashes, reading extents and visual checks. All downloaded PDFs, extraction text, OCR, and page renders are ignored private audit material, excluded from the public manifest. The audit does not redistribute these sources.

- [Artebani–Dolgachev, official PDF](https://ems.press/content/serial-article-files/44190), 39 pages: relevant §§2 and 4 read, including Lemma 2.1 and Proposition 4.1. Its parameter has coefficient +lambda xyz, so it is -3 times the author's lambda; its p0 and group letters also differ. These are harmless coordinate/notation changes, not contradictory matrices. Relevant equations were visually checked.
- [Illman 1978, official digitization](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0233/LOG_0044.pdf), 23 PDF pages including digitization cover: image-only mathematical pages. The existence theorem p.199, regular quotient discussion p.201, and Theorem 3.6 p.216 were read visually. The retrieved file is exactly 3,093,991 bytes, SHA256 2b7415001b130e21c5a28b7f5c5d0594e43b7562254ffbf68ad95a428e800ec0. Hash agreement supplements actual reading; it is not a substitute.
- [OWR official report](https://ems.press/content/serial-article-files/46724), 82 PDF pages: Question 5 and surrounding pp.114–115 read and visually checked. Its literal definition requires connected domains and trivial restrictions. The proof's limitation of scope is accurate and material.
- The inspected Chen–Wan body is the **2023 v2 preprint**, ten pages, not the 13-page 2025 journal article. The [author's publication list](https://www.weiyanc.com/research) confirms Proc. AMS 153 (2025), 2255–2267 and DOI 10.1090/proc/17184. Crossref metadata yields the AMS version-of-record PDF link. Three direct official AMS page/PDF attempts returned HTTP403; web opening also failed. I have not read or compared the final published full text.
