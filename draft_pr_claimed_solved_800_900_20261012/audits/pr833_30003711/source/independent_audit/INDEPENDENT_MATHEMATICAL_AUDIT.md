# Independent adversarial audit: the flex-point cover

Problem 30003711 / OWR-15987-022; candidate dated 2026-10-06.

## Verdict

**Accept the candidate's theorem for ordinary, unnormalized section-based Schwarz genus: the genus is 8, and normalized sectional category is 7. No mathematical correction to the submitted proof is required.** This is an independent mathematical review with cited classical dependencies, not a formal proof-assistant certification.

The scope qualification is indispensable. The curated question and its explicit Chen–Wan 8-versus-9 target use ordinary section-based genus, and the proof settles that target. The literal definition printed in OWR Question 5 also requires connected domains and triviality of the entire nine-sheeted restriction. The proof does not compute that stronger quantity. An unqualified claim to have solved every literal reading of the OWR formulation is not accepted.

The archive inventory, bytes, and mathematical validity were examined separately. All five submitted files match the external manifest exactly. The full supplied problem record and absent report entry were read; their combined digest matches the specified input. No finite numerical experiment is used as proof.

## 1. The invariant and the actual parameter space

The candidate uses X = CP^9 minus the cubic discriminant. It does not divide X by PGL_3(C). This is exactly the coefficient space in Chen–Wan, Definition on page 1 and Theorem 1.2 on page 2. The nine points over a coefficient vector are the nine distinct flexes of its smooth cubic. The manuscript minimizes the number of open sets admitting one section, and it explicitly permits disconnected sets.

Chen–Wan Theorem 4.1 supplies the lower bound 8 for this precise cover and convention. Its proof pulls back along the Fermat-cubic orbit PU(3)/K, where K is the order-nine translation subgroup, and uses a nonzero degree-seven class for the resulting principal K-cover. I read the reduction and cohomological proof in Sections 2–4, not merely its abstract or theorem statement. The present candidate treats that published theorem as an input; it does not independently reconstruct Leary's underlying cohomology-ring theorem. Neither Chen–Wan's algorithmic-complexity argument in Section 5 nor any claimed invariance of a metric under general projective transformations is needed here.

The candidate makes no equality claim about algorithmic branching complexity. Its use of 8 domains rather than normalized value 7 is consistent throughout.

## 2. Hesse data, the full group, and scalar ambiguity

The relevant group is the projective Hessian group of order 216, not merely its translation subgroup, a chosen matrix lift of order 648, or the full affine group of order 432. Artebani–Dolgachev, Section 4 and Proposition 4.1, identify its action on the nine base flexes as F_3^2 semidirect SL_2(F_3). Their Section 2 and proof of Lemma 2.1 provide the Hesse normal form. Chen–Wan Section 2.2 gives precisely the candidate's coordinates, base flex p0, and generators A, B, C, D. The group lies in PU(3): A, B, and C are unitary, and D is unitary after scalar rescaling. The stabilizer of p0 realizes all SL_2(F_3), so every required linear conjugation really lifts to an element of that stabilizer.

The translation generators commute projectively; their possible scalar commutator in GL_3(C) does not change the projective semidirect-product action. All statements about eigenvalues are statements about their multiplicities or their number of distinct values. Multiplying a representative by a nonzero scalar, or conjugating it projectively, preserves both. Accordingly, the proof never incorrectly assigns an absolute eigenvalue to a projective element.

The smooth Hesse parameter domain is C with the three roots of unity deleted. The omitted point at infinity corresponds to a singular pencil member and is not a missing smooth parameter. Pencil automorphisms preserve smoothness and therefore act on this parameter domain.

## 3. Exhaustive audit of the spectral lemma

Let an element of the full group act as v maps to Lv+t, with L in SL_2(F_3).

1. If I−L is invertible, the equation (I−L)v=t supplies a fixed flex for every translation term. Therefore every fixed-point-free element has eigenvalue 1 in its linear part.
2. Since det L=1, the other eigenvalue is also 1. The characteristic polynomial is (u−1)^2. Cayley–Hamilton gives (L−I)^2=0. This excludes every semisimple or mixed case not explicitly handled in the manuscript.
3. If L=I, a fixed-point-free element is a nonidentity translation. For A^0 B^b with b nonzero, the three diagonal entries are the three different cube roots of unity. For a nonzero, the underlying permutation of A^a B^b is a three-cycle.
4. If L is nonidentity unipotent, N=L−I has rank one and its image equals its kernel. Choose a nonzero u in that kernel, then v so that the ordered basis (v,u) has determinant one. In this basis Nv=cu for c equal to 1 or 2, and Nu=0. Thus L is conjugate within SL_2(F_3), not just GL_2(F_3), to one of the two lower-triangular unipotents in the manuscript. Both conjugacy classes are retained.
5. Direct multiplication with the displayed matrices gives CAC^(−1)=AB and CBC^(−1)=B projectively (the first equality is already exact for the chosen representatives). C fixes p0. Its linear action on translation coordinates is (a,b) maps to (a,b+a). Consequently the conjugated general affine element has form A^a B^b C^c with c in {1,2}.
6. For a=0, the affine fixed-point equations reduce to cx+b=0, with y arbitrary. There are three solutions, so that case is not fixed-point-free.
7. For a nonzero, the representative A^a B^b C^c is a weighted three-cycle with nonzero weights. Its characteristic polynomial is u^3−d for d nonzero. In characteristic zero its derivative is 3u^2, which has no common root with u^3−d. Hence all three eigenvalues are distinct.

These cases exhaust the full group and prove the contrapositive needed by the construction: a projective Hessian element with a repeated eigenvalue fixes a flex. There is no numerical enumeration in this argument and no unstated generalization from K to the full group.

## 4. Common fixed sheet, rather than individual fixed points

H consists of the projective classes of diag(1,z,z), with z on the unit circle. This parameterization is injective in PU(3): a scalar matrix of this form has z=1. Every nonidentity member has one simple and one repeated eigenvalue.

For any g, J_g = Gamma intersect g^(−1)Hg is finite and isomorphic to a finite subgroup of a circle. It is therefore cyclic. If it is nontrivial, apply the spectral lemma to one generator. That generator fixes a flex, and so does every power of it. This produces one flex fixed simultaneously by all of J_g. The proof does not make the invalid inference that separate fixed points for separate elements yield a common fixed point for an arbitrary finite subgroup.

No scalar lift creates extra isotropy: the intersections and the circle are taken inside PU(3), and conjugation is an isomorphism of those actual projective subgroups.

## 5. Orbit sections and nonfree isotropy

Right multiplication by a finite subgroup on G=PU(3) is free. Thus M=G/Gamma and E=G/Gamma0 are smooth compact manifolds, and E to M is a genuine nine-sheeted covering. Left multiplication by H acts smoothly on both and makes the covering H-equivariant.

At m=gGamma the H-stabilizer is L_m = H intersect gGamma g^(−1), a finite group. Identify the fiber with Gamma/Gamma0 and then with the flex set by deltaGamma0 maps to delta p0. The L_m-action on this fiber is exactly the action of g^(−1)L_m g = J_g. The previous step therefore provides a point e over m fixed by the entire stabilizer.

The map H/L_m to E given by hL_m maps to he is continuous and well defined. Its composition with the covering is the orbit identification H/L_m to Hm. This proves a section on the whole orbit, including its fundamental loop. No extra monodromy from the nontrivial fundamental group of PU(3) is omitted: the section is defined using the actual H-action on E, so a loop in H that returns to the identity returns to the same e.

The orbit is an embedded circle because H is compact and its stabilizer is finite. Average a Riemannian metric on M over H. The normal exponential map to this compact orbit is a diffeomorphism from a sufficiently small disk bundle onto an H-invariant open tubular neighborhood W. Its radial retraction r_W onto the orbit is H-equivariant. The homotopy from r_W to the identity lifts through the covering, starting from the orbit section composed with r_W. At its final time the lift is a section over W.

This is a usual covering-homotopy application with a continuous prescribed initial lift. No selection across varying stabilizers is required. Different orbit neighborhoods may choose different sheets; they will later be placed into disjoint pieces before gluing. An equivariant extension is not needed, although uniqueness of covering lifts supplies one for the invariant homotopy and equivariant initial section.

Since W is H-invariant and the orbit projection is an open quotient map, q(W) is open and q^(−1)(q(W))=W. This is the crucial saturation property used later. The candidate never assumes that the induced map between coarse orbit spaces of E and M is a covering.

## 6. The dimension reduction and the eight-color cover

The left action of H on G itself is free. Consequently H\G is a smooth compact manifold of dimension 8−1=7. The finite group Gamma acts smoothly on H\G from the right, and the orbit space B=H\M is its finite quotient. Effectiveness or freeness of that finite action is not necessary for finite-group equivariant triangulation. Subdivision of an equivariant triangulation yields a quotient polyhedron of dimension at most 7. B is compact and metrizable.

This dimension bound applies to the coarse orbit space, including exceptional orbits. It is not an assertion that B is a manifold. Illman's finite-group theorem is used with the smooth Gamma-manifold H\G, where all its hypotheses hold. The actual primary article was recovered from Göttingen's digitized journal archive. I read its equivariant-complex definitions and quotient statement in Section 1 (especially printed p. 201), its approximation and gluing lemmas, and its existence proof in Theorem 3.6 (printed pp. 216–218). The quotient-complex statement explicitly preserves simplex dimension, and the existence theorem does not assume a free action. This verifies the applicable theorem rather than relying only on its title or publisher metadata.

The refinement-and-coloring argument was checked in full:

- Compactness gives finitely many orbit-neighborhood images U_i covering B.
- Covering dimension at most 7 gives a finite open refinement V_j of order at most 8. A subordinate partition of unity defines a continuous map f to its finite nerve N; the nerve has dimension at most 7.
- A vertex of the barycentric subdivision corresponds to a nonempty simplex sigma of N. Color it by dim sigma.
- Two distinct simplices of the same dimension cannot belong to a strictly increasing chain. Thus the corresponding open stars in the barycentric subdivision are disjoint. This proves disjointness of their inverse images, not just a bound on pointwise multiplicity.
- If j is any vertex of sigma, every point of the open star of its barycenter has positive original j-coordinate. Its inverse image under f therefore lies inside V_j and one of the original U_i. A section is available on its full inverse image in M.
- For each of the eight colors, the inverse images are pairwise disjoint open sets. Their sections glue by the elementary pasting property for an open disjoint union. Accumulation on a missing boundary cannot obstruct continuity inside that union.

The resulting at most eight open sets cover M and each has one section. The construction deliberately allows disconnected domains. It has no need to label other sheets, to choose compatible sections on intersecting colors, or to create a global section over B.

## 7. Pullback to coefficient space

Chen–Wan Lemma 3.2 and Proposition 3.3 provide the associated quotients X = (PGL_3(C) × T)/Gamma and Y = (PGL_3(C) × T)/Gamma0, with the diagonal actions that use right multiplication on the first factor and the matching inverse parameter action on the second.

The polar unitary factor r(A)=A(A* A)^(−1/2) is right-unitary-equivariant. Replacing A by cA replaces r(A) by (c/|c|)r(A); hence it is well defined projectively. Also r(AU)=r(A)U for unitary U. These facts establish the quotient map X to G/Gamma and its accompanying map Y to G/Gamma0.

For completeness, fix a representative (g,lambda) of a point of X. The nine fiber elements of Y are represented by (g delta,delta^(−1)lambda), indexed by deltaGamma0 in Gamma/Gamma0. Their images under polar retraction are r(g)deltaGamma0, the nine distinct points in the corresponding fiber of E. Thus the commutative square is a genuine pullback of coverings: the continuous map to the pullback is fiberwise bijective, hence is a covering isomorphism in local trivializations.

This establishes the needed upper-bound transfer directly. It avoids the inadequate assertion that an unspecified homotopy equivalence of bases automatically identifies the particular coverings. Pulling back the eight section domains and their sections proves g(Y/X) at most 8 on the actual coefficient space. The cited lower bound yields equality.

## 8. Join obstruction and limitations

The eight-domain cover and a subordinate partition of unity yield a section of the eightfold fiberwise join. Hence its primary obstruction vanishes with the appropriate monodromy-twisted coefficient system. The join of eight nonempty nine-point sets is 6-connected, with reduced homology in degree 7 of rank 8^8; the coefficient group used by the candidate is consistent with that description. Only the forward implication from an actual section to vanishing of obstruction is asserted. There is no unsupported appeal to pullback injectivity or to vanishing of arbitrary higher obstruction choices.

The accepted proof is dependency-based mathematics. It is not a certified computation of a large obstruction module, and its correct hash does not establish the theorem. No executable verifier is necessary to the logical argument or present in the author archive.

## 9. Exact scope gap

A section of a nonregular cover does not trivialize the full cover. Here the distinction can be exhibited within the very circle action used in the proof. Let C=diag(1,1,omega), and choose the permutation matrix g swapping the first and third coordinates. Then gCg^(−1) is projectively diag(1,omega^2,omega^2), which lies in H. A path in H from the identity to this element gives a closed loop in the orbit of gGamma. Its fiber monodromy is C.

On the affine flex set, C sends (x,y) to (x,y+x). It fixes the three points with x=0 and acts in two nontrivial three-cycles on the six remaining points. Consequently the restricted cover has a section but is not a trivial nine-sheeted cover on that orbit, and no neighborhood containing that entire orbit can make this monodromy trivial. This is a concrete reason the proof's local construction cannot simply be relabeled as simultaneous trivialization.

Additionally, merging disjoint neighborhoods by color does not make their unions connected. Neither issue is repaired by changing from normalized to unnormalized counting. The candidate already discloses both correctly. No numerical value for the stronger connected/full-trivialization invariant follows from this audit.

The proper disposition is therefore:

- Accepted full resolution of the ordinary section-genus theorem and the curated Chen–Wan 8-versus-9 target.
- Qualified resolution when referred back to the literal OWR definition; that stronger target remains outside the proved claim.
- No novelty, priority, formal certification, or exhaustive literature-status claim.

## References

1. W. Chen and Z. Wan, *Topological complexity of finding flex points on cubic plane curves*, arXiv:2306.17303v2, 21 July 2023; journal record Proc. Amer. Math. Soc. 153 (2025), 2255–2267. [Full inspected preprint](https://arxiv.org/pdf/2306.17303v2); [journal DOI](https://doi.org/10.1090/proc/17184).
2. M. Artebani and I. Dolgachev, *The Hesse pencil of plane cubic curves*, Enseign. Math. 55 (2009), 235–273. [Publisher PDF](https://ems.press/content/serial-article-files/44190); [DOI](https://doi.org/10.4171/LEM/55-3-3).
3. *Topology of Arrangements and Representation Stability*, Oberwolfach Reports 15 (2018), 43–123, Question 5 and its definition on printed pp. 114–115. [Publisher PDF](https://ems.press/content/serial-article-files/46724); [DOI](https://doi.org/10.4171/OWR/2018/2).
4. S. Illman, *Smooth equivariant triangulations of G-manifolds for G a finite group*, Math. Ann. 233 (1978), 199–220. [Publisher record](https://link.springer.com/article/10.1007/BF01405351); [digitized primary article locator](https://eudml.org/doc/163108); [inspected Göttingen article PDF](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0233/LOG_0044.pdf).
