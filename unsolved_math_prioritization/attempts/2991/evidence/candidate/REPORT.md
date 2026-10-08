# Kirby 4.115: a complete part-(a) candidate and four part-(b) routes

## Result and scope

The file `PART_A_PROOF.md` gives a complete candidate proof of the first existence question: the untwisted spin of L(8,3) has diffeomorphic but non-isotopic balanced minimal-genus (3,1)-trisections. The proof excludes isotopy even after arbitrary sector permutations. It is a proof of unstabilized inequivalence, and the manifold has fundamental group C_8.

The second question asks for two non-diffeomorphic balanced equal-genus trisections of one closed simply connected smooth 4-manifold. No such pair is proved here. Four further, mathematically distinct attempts below establish partial constructions and obstructions without replacing this target by a weaker one. The bundled target has used five substantive approaches in total. Literature checks, arithmetic tests and independent reviews are not extra proof approaches.

No priority or novelty claim is made. The 2026 K3 list retains both questions, but an unsuccessful literature search cannot exclude an earlier or unindexed answer. The main candidate is a short consequence of existing spun-trisection existence theory plus an elementary homology argument; Islambouli's Nielsen-class framework is explicitly credited.

## Exact equivalences and parameters

A trisection is an ordered decomposition T=(X_1,X_2,X_3), with X_i a smooth 4-dimensional 1-handlebody, pairwise intersections 3-dimensional handlebodies, and central surface Sigma of genus g. A balanced (g,k)-trisection has all three sector ranks k. Diffeomorphism equivalence uses an orientation-preserving ambient diffeomorphism taking each specified sector to its counterpart. Ambient isotopy equivalence requires the ambient diffeomorphism to be connected to the identity by a smooth isotopy. Our part-(a) proof also excludes an isotopy carrying sectors through any permutation.

The ambient manifold, smooth structure, and genus must be fixed in the second question. Different smooth manifolds with equal intersection forms, different genera, relative trisections, marked decompositions, and stable equivalence do not meet that question.

For a fixed closed simply connected X, chi(X)=2+b_2(X), whereas a balanced trisection has chi(X)=2+g-3k. Thus

    g = b_2(X)+3k.

Equal genus on that fixed manifold automatically fixes k. Balanced stabilization changes (g,k) to (g+3,k+1). Gay-Kirby's uniqueness theorem allows eventual isotopy after stabilization; no construction here contradicts or evades it.

## Approach 1. A rank-one torsion marking moved by a lens-space symmetry

This is the complete candidate in `PART_A_PROOF.md`. The mechanism has four essential ingredients:

1. The coordinate swap of the quotient S^3/<(z_1,z_2)->(zeta z_1,zeta^3 z_2)> induces multiplication by 3 on C_8 and is orientation preserving.
2. A local radial rotation makes the map the identity near a ball without changing its homology action. It then extends to the untwisted spin X.
3. Meier's spun-trisection theorem gives a (3,1)-trisection of X. Each sector's infinite cyclic H_1 maps onto H_1(X)=C_8, so the image of a generator, up to sign, is an ambient-isotopy invariant of that sector.
4. Multiplication by 3 exchanges the two classes of units modulo sign. A multiset of three such classes cannot be invariant under that exchange.

The proof includes every topological reduction; the finite arithmetic check is supplementary, not a substitute for the proof. The distinction is between isotopy classes inside one diffeomorphism orbit. That same fact prevents it from directly answering part (b).

## Approach 2. Kill the cyclic fundamental group by surgery

### Construction

Let X and F be as in Approach 1. Choose a smooth embedded loop gamma representing a generator of pi_1(X)=C_8, with a framing of its oriented rank-three normal bundle. Such a framing exists because every oriented rank-three vector bundle over S^1 is trivial. Perform ordinary framed circle surgery:

    Y_gamma = (X minus int(S^1 x D^3)) union (D^2 x S^2).

Then Y_gamma is closed, smooth, oriented and simply connected, and chi(Y_gamma)=4. In particular b_2(Y_gamma)=2.

### Proof of these claims

The inclusion of the loop exterior into X is an isomorphism on fundamental groups. Surjectivity follows by perturbing loops off gamma; injectivity follows by perturbing null-homotopies off gamma, since 2+1<4. Replacing the punctured normal fibers by their radial deformation retraction identifies the complement of gamma with the compact exterior up to homotopy. Van Kampen for surgery quotients pi_1(X) by the normal closure of gamma. Since gamma generates C_8, the result is the trivial group. Euler characteristic increases by chi(D^2 x S^2)-chi(S^1 x D^3)=2, since their common boundary has Euler characteristic zero. Finally, Poincare duality and simple connectivity give chi=2+b_2.

### The obstruction to using this as part (b)

Carry the loop and its framing through F. The map F on the exteriors extends by the product-coordinate identification over the surgery pieces, giving an orientation-preserving diffeomorphism

    Y_gamma -> Y_{F(gamma)}.

Any trisection construction whose second output is obtained by carrying the first construction through that diffeomorphism necessarily gives diffeomorphic trisections. Furthermore, all sector Nielsen tuples now map to the trivial group, so the distinguishing invariant of Approach 1 becomes constant. Thus simply killing the group in a diffeomorphism-equivariant way cannot turn this isotopy-only distinction into a diffeomorphism distinction.

Exact remaining gap: construct compatible surgery choices not carried to one another and prove the resulting same-manifold, same-genus trisections inequivalent by another invariant. There is no such certificate here. We do not identify Y_gamma with a particular standard b_2=2 manifold; that identification is not implied merely by its group and Euler characteristic.

## Approach 3. Double a pair of inequivalent relative trisections

### Source inputs, used with their full hypotheses

Takahashi's Theorem 4.3 supplies two non-diffeomorphic relative trisections R_0,R_1 of W=S^2 x D^2, both of type (2,1;0,2), with equivalent induced boundary open books. They are distinguished there by capping their diagrams: the resulting closed 4-manifolds have respectively even and odd intersection forms. This is a relative result.

Castro-Ozbagci's Corollary 2.8 doubles a (g,k;p,b)-relative trisection, by gluing to its oppositely oriented copy through the identity boundary map, to obtain a balanced

    (2g+b-1, 2k-2p-b+1)

trisection of the ordinary double.

### Derived closed candidates and a rigorous marked distinction

Apply the doubling theorem separately to R_0 and R_1. Both ordinary doubles are

    D(W) = S^2 x (D^2 union_boundary D^2) = S^2 x S^2,

and both trisections have parameters (5,1). The numerical check is 2+5-3=4=chi(S^2 x S^2).

Retain as additional marking the equatorial copy of boundary W and the designation of the positive W-half. No orientation-preserving diffeomorphism can identify the two doubled trisections while preserving that marked half and the sector labels. Indeed, restriction to the marked half would give a diffeomorphism R_0 -> R_1, contradicting the input theorem. This is a proof of inequivalence of these marked doubled decompositions.

Exact remaining gap: an unmarked trisection diffeomorphism need not preserve the equatorial hypersurface or either half. Nothing proved here makes that seam intrinsic to the closed trisection. Therefore marked inequivalence cannot be promoted to inequivalence in part (b). Capping the original relative diagrams is not a substitute: those caps change the ambient manifold, producing S^2 x S^2 and CP^2#(-CP^2), rather than two decompositions of the same manifold.

## Approach 4. Classify the integral homological triple in the efficient case

This approach tries to distinguish genus-22 efficient K3 trisections through the integral homology of their three disk systems. The following linear-algebra theorem shows exactly what this test can and cannot retain.

### Algebraic theorem

Let H be a rank-2g free abelian group with a unimodular alternating form omega. Suppose A,B,C are rank-g Lagrangian direct summands, each pair complementary over Z. Then a symplectic basis identifies

    H = Z^g_a direct_sum Z^g_b,
    A = Z^g_a,  B = Z^g_b,
    C = { (Sx,x) : x in Z^g },

where S is a symmetric unimodular integer matrix. Two ordered triples of this type are symplectically isomorphic if and only if their matrices are integrally congruent.

### Proof

Choose dual integral bases a_i of A and b_i of B with omega(a_i,b_j)=delta_ij; their existence follows from unimodularity and H=A direct_sum B. Since C is complementary to A, projection C->B is an integral isomorphism, so C is the graph of an integral matrix S. The equation omega((Sx,x),(Sy,y))=0 for all x,y says S^t=S. Complementarity to B says S is an integral automorphism, hence det(S)=+1 or -1.

An automorphism preserving both A and B has block form diag(P,P^{-t}), P in GL(g,Z), and it is symplectic. It takes the graph of S to the graph of P S P^t. Conversely any congruence is implemented by this block matrix. This proves both directions, including integrality rather than merely rational equivalence.

### Application and exact gap

For a (g,0)-trisection, each pair of disk-system Lagrangians is integrally complementary: the associated Heegaard 3-manifold is S^3, and its first homology is H divided by their sum. The usual trisection intersection-form formula identifies the graph form, with a fixed overall sign convention, with the ambient intersection form. Therefore on a fixed oriented X all efficient (g,0) trisections give the same ordered integral homological triple up to symplectic change of basis. For the genus-22 K3 candidates this entire algebraic layer cannot distinguish them.

We used the intersection-form identification from Feller-Klug-Schirmer-Zemke. The graph-classification proof above is independent of geometric classification of diagrams. Its no-extra-homological-information conclusion is consistent with, and already covered in greater scope by, Feller-Klug-Schirmer-Zemke Theorem 4.4; it is not claimed as new. It does not assert that symplectically equivalent homological triples are equivalent trisection diagrams. That would discard the crucial nonabelian curve and mapping-class information.

Exact remaining gap: detect geometric disk-system or Torelli information that survives all allowed surface diffeomorphisms and same-color handleslides, while keeping the smooth ambient manifold fixed. A homologically trivial regluing need not preserve the required pairwise S^3 boundaries and need not preserve the smooth 4-manifold. Neither assertion is assumed here. No classification of non-efficient (g,k), k>0, triples is claimed.

## Approach 5. Try the topology of the central-surface exterior

A diffeomorphism of trisections carries the central surface to the central surface, so its exterior with peripheral data is a possible invariant stronger than the ordinary group of X. We compute its integral homology exactly in the simply connected case, rather than presuming it varies.

### Exterior homology theorem

Let Sigma be the genus-g central surface of any trisection of a closed simply connected oriented smooth X, and let E = X minus int(nu Sigma). Then

    H_0(E;Z) = Z,
    H_1(E;Z) = Z, generated by an oriented meridian,
    H_2(E;Z) = H_2(X;Z) direct_sum Z^(2g), noncanonically,
    H_3(E;Z) = H_4(E;Z) = 0.

### Proof

Sigma is the oriented boundary of each of the embedded pairwise 3-dimensional handlebodies, so its class in H_2(X;Z) is zero. Its oriented normal bundle has Euler number zero and is trivial; equivalently, the collar in a bounding handlebody supplies a nonzero normal section. The exterior is connected by general position.

Excision and the Thom isomorphism give H_j(X,E;Z)=H_{j-2}(Sigma;Z). In the long exact sequence of the pair, the map H_2(X)->H_2(X,E)=Z is intersection with [Sigma], hence zero. Since H_1(X)=0, it follows that the boundary meridian generates H_1(E)=Z.

Since H_3(X)=0 by Poincare duality, the same exact sequence gives

    0 -> H_1(Sigma) -> H_2(E) -> H_2(X) -> 0.

The last term is free abelian because X is simply connected and closed oriented. The sequence splits as abelian groups, though no preferred splitting is provided. The map H_4(X)=Z -> H_4(X,E)=H_2(Sigma)=Z takes the ambient fundamental class to the surface fundamental class and is an isomorphism. Exactness then gives H_3(E)=0. Finally H_4(E)=0 for a compact connected 4-manifold with nonempty boundary. This proves the formulas.

For the (5,1) double candidates above, H_2(E)=Z^12. For an efficient genus-22 K3 trisection, it is Z^66. Thus ordinary integral homology of this exterior gives no distinction at fixed X and g.

Exact remaining gap: compute and distinguish the nonabelian exterior group or suitably marked peripheral structure for an actual pair, and show that distinction is invariant under all sector-preserving diffeomorphisms. The homology calculation does not claim the exterior group is infinite cyclic. Nor does it establish any pair with different exterior groups.

## Verification and limitations

The executable checks enumerate the unit/sign obstruction, all triples and all sector permutations, positive and negative controls for that obstruction, the graph-matrix identities for representative unimodular forms, and the exact parameter/homology arithmetic. They contain always-active checks, work without source documents or datasets, and emit JSON to stdout by default. Optimization modes do not disable them. These are finite algebraic consistency checks, not computer proofs of the smooth constructions or an exhaustive diagram search.

The specialized geometric existence and doubling results are identified by exact theorem numbers and primary URLs in `SOURCE_METADATA.json`. The candidate proof does not invoke lens-space mapping-class classification, a naturality theorem for spinning trisections, or a simply connected manifold-classification theorem. No source text, PDF, dataset content, or private coordination material is included in this source-free candidate directory.

## Public references

- Actual 2026 K3 list, Problem 4.115, p.286: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- J. Meier, *Trisections and spun 4-manifolds*, Theorem 1.2: https://arxiv.org/abs/1708.01214 ; https://doi.org/10.4310/MRL.2018.v25.n5.a7
- D. Gay and R. Kirby, *Trisecting 4-manifolds*, Theorem 11 and Lemma 13: https://arxiv.org/abs/1205.1565 ; https://doi.org/10.2140/gt.2016.20.3097
- G. Islambouli, *Nielsen equivalence and trisections*, Proposition 4.5: https://arxiv.org/abs/1804.06978 ; https://doi.org/10.1007/s10711-021-00617-y
- N. Takahashi, *Non-diffeomorphic minimal genus relative trisections of the same 4-manifold*, Theorem 4.3: https://arxiv.org/abs/2406.03113
- N. A. Castro and B. Ozbagci, *Trisections of 4-manifolds via Lefschetz fibrations*, Corollary 2.8: https://arxiv.org/abs/1705.09854
- P. Feller, M. Klug, T. Schirmer and D. Zemke, *Calculating the homology and intersection form of a 4-manifold from a trisection diagram*: https://arxiv.org/abs/1711.04762
- P. Lambert-Cole, *Trisections, intersection forms and the Torelli group*, contextual caution about homology versus valid geometric regluing: https://arxiv.org/abs/1901.10834 ; https://doi.org/10.2140/agt.2020.20.1015
