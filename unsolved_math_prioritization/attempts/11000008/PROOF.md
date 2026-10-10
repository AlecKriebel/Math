# Relative ends of closed-surface mapping class groups: verified partial results

Problem 11000008 / AMR-109-0008 (Farb, Question 2.1).

This AI-assisted manuscript and its independent internal AI audit are unrefereed. “Accepted” refers only to the stated internal partial-theorem assessment; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The full spectrum for g >= 2 remains unresolved by this work, and no novelty or global-openness claim is made.

## Status and scope

This is a partial result, not a determination of the full spectrum and not a novelty claim. Let G_g = Mod(S_g) mean orientation-preserving mapping classes of the closed oriented genus-g surface. Let e(G,H) be the number of ends of a proper cocompact geometric model for G modulo H. Equivalently, use the locally finite Schreier graph H\Cay(G,S). All subgroup witnesses below are finitely generated.

The main conclusions for g >= 2 are:

1. e(G_g,H) = 0 if and only if [G_g:H] is finite.
2. If [G_g:H] is infinite and vcd(H) <= 4g-7, then e(G_g,H) = 1. In particular, a subgroup with at least two relative ends must have vcd(H) in {4g-6,4g-5}.
3. In genus 2 the values 0, 1, 2, and 2^{aleph_0} all occur. The two-ended witness has a generating set of at most ten elements. The continuum-ended witness has a generating set of at most eight elements.

Here vcd(H) means the integral cohomological dimension of a torsion-free finite-index subgroup. Such subgroups exist since G_g is virtually torsion-free; cohomological dimension is unchanged on passage between torsion-free finite-index subgroups of finite cohomological dimension.

No exclusion of finite values >= 3, countably infinite values, or other unresolved possibilities is asserted for g >= 2. The theorem neither replaces relative ends by ordinary subgroup ends nor uses the noncocompact quotient of untruncated Teichmuller space.

For completeness, the familiar low-genus groups give the full spectra {0} for g=0 and {0,2^{aleph_0}} for g=1, with proofs below.

## 1. Elementary facts about the exact subgroup pair

Fix a finite symmetric generating set for a finitely generated group G. Its Cayley graph has right-multiplication edges and the left action of G. The quotient by H has vertices Hg and edges Hg--Hgs. It is connected and locally finite. It is finite exactly when [G:H] is finite. A connected infinite locally finite graph has a ray, hence at least one end. This proves conclusion 1.

### Lemma 1 (finite-index ambient passage)

If H <= K <= G and [G:K] is finite, then e(G,H)=e(K,H).

Proof. Equip K and G with word metrics. The inclusion K -> G is a quasi-isometry, with inequalities uniform on every pair of points of K. It is H-equivariant. Quotient distances satisfy

  d_{H\G}(Hx,Hy) = inf_{h in H} d_G(x,hy).

Taking infima in the quasi-isometry inequalities gives the same inequalities for H\K -> H\G. Choose finitely many right coset representatives G=K T. If g=kt, then d_G(g,k)<=max_{t in T}|t|, so the quotient inclusion is coarsely onto. It is consequently a quasi-isometry of connected locally finite graphs and preserves their spaces of ends. This compares the same subgroup H in two ambient groups; it is not an assertion of unrestricted invariance when H changes. QED.

### Lemma 2 (finite quotient)

If H_0 is normal of finite index in H, the quotient graph H\Cay(G) is the quotient of H_0\Cay(G) by the finite group H/H_0. If the latter graph has one end and is infinite, the former also has one end.

Proof. The preimage of a finite vertex set is finite. In its complement upstairs there is one infinite component. Every infinite component downstairs has an infinite preimage and thus must receive that component. Hence there is just one infinite component downstairs. An infinite graph cannot become finite under a finite-fiber quotient. QED.

More generally, the end space of the finite quotient is the finite-group quotient of the original end space. To see the fiber assertion, exhaust the graph by invariant finite sets. If two ends have the same image, their respective components outside each such set are carried to one another by some element of the finite group. An element occurs for arbitrarily large sets and therefore carries one end to the other. Surjectivity follows by lifting a ray, or by the nested-components description. In particular a continuum-sized end space still has cardinality continuum after a finite quotient.

### Lemma 3 (normal-subgroup quotient)

If N is normal in a finitely generated group K, then e(K,N)=e(K/N). The quotient Schreier graph is exactly a Cayley graph of K/N, allowing redundant generators and loops. In particular a quotient Z gives two ends, while a nonabelian finite-rank free quotient gives 2^{aleph_0} ends. No inference about ordinary ends of N is involved.

## 2. A dimension obstruction for relative ends

### Lemma 4 (a cohomological sufficient condition)

Let K be finitely generated and L <= K of infinite index. If

  H^1(K, Z[K/L]) = 0,

then e(K,L)=1.

Proof. Invert cosets to identify the right Schreier graph L\K with the graph on left cosets K/L having edges xL--sxL. Suppose it has at least two ends. There is a subset A of its vertices with finite edge boundary such that A and its complement are both infinite: take one infinite component after removing a finite separating vertex set.

Let f be the characteristic function of A, regarded in Map(K/L,Z). With the usual left permutation action, define b(g)=g f-f. Finite edge boundary implies b(s) has finite support for every generator s. The cocycle identity then implies b(g) has finite support for every g. Thus b is a 1-cocycle with values in the direct-sum permutation module Z[K/L].

The assumed vanishing makes b(g)=g m-m for some finitely supported m. Consequently f-m is K-invariant. The action on K/L is transitive, so f-m is constant. Outside a finite set f is constant, contradicting that A and its complement are both infinite. The graph is infinite, so it has exactly one end. QED.

### Proposition 5 (duality-group form)

Let K be a duality group of dimension d, and let L <= K have cd_Z(L)<=d-2. Then e(K,L)=1.

Proof. Write D for the right dualizing ZK-module. Duality gives

  H^1(K,Z[K/L]) = H_{d-1}(K,D tensor_Z Z[K/L]).

The right action on the tensor product is (d_0 tensor m)g=d_0 g tensor g^{-1}m. There is a right ZK-module isomorphism

  D tensor_Z Z[K/L] -> (D restricted to L) tensor_{ZL} ZK,
  d_0 tensor gL -> d_0 g tensor g^{-1}.

It is independent of the representative g: replacing g by gl changes the right side to d_0 gl tensor l^{-1}g^{-1}, the same tensor. The inverse sends d_0 tensor g to d_0 g tensor g^{-1}L. Homological Shapiro therefore identifies the displayed homology group with

  H_{d-1}(L,D restricted to L),

which vanishes because cd_Z(L)<=d-2. Here Shapiro follows directly by restricting a free ZK-resolution of Z to ZL and using tensor associativity; the induced-module homology becomes the homology of D tensor_{ZL} that restricted resolution. A projective ZL-resolution of length at most d-2 makes the stated vanishing immediate. The index [K:L] cannot be finite, since a finite-index subgroup of a duality group has cohomological dimension d. Lemma 4 now applies. QED.

The duality identity and its exact dimension for mapping class groups are established by Harer: a torsion-free finite-index subgroup of G_g is a duality group of dimension 4g-5. See [H], Corollary 4.2, printed pages 176-177; the accompanying proof is in Chapter 4, section 1. The needed convention is also stated explicitly in [IJ], Theorem 1.1 and equation (3).

Proof of conclusion 2. Choose a torsion-free normal finite-index subgroup K of G_g and set L=H intersect K. Then L is normal of finite index in H, and cd_Z(L)=vcd(H). Proposition 5 with d=4g-5 gives e(K,L)=1. Lemma 1 gives e(G_g,L)=1. Lemma 2 then gives e(G_g,H)=1. Since L is a subgroup of K, its cohomological dimension is at most 4g-5; this proves the stated two-dimensional range for a possible obstruction. QED.

Examples covered include every finite or virtually free subgroup for every g>=2, every virtually closed-surface subgroup for g>=3, and every virtually Z^r subgroup satisfying r<=4g-7. These are examples of the criterion, not a classification of subgroups. In particular taking H={1} supplies the value 1 in every genus g>=2, and H=G_g supplies 0.

## 3. An elementary finitely generated cyclic kernel

### Lemma 6 (unit-weight commuting generators)

Suppose a group P is generated by y_0,...,y_m, there is a homomorphism chi:P->Z with chi(y_i)=1 for every i, and the commuting graph on these generators is connected. Then

  ker(chi) = < y_i y_0^{-1} : 1<=i<=m >.

Proof. Put t=y_0, k_i=y_i t^{-1}, k_0=1, and N=<k_1,...,k_m>. If y_i and y_j commute, writing alpha(x)=txt^{-1} gives

  k_i alpha(k_j) = k_j alpha(k_i),
  alpha(k_j) = k_i^{-1} k_j alpha(k_i),
  alpha^{-1}(k_j) = alpha^{-1}(k_i) k_j k_i^{-1}.

Root a spanning tree of the commuting graph at 0. Induction along its edges, starting from alpha^{+/-1}(k_0)=1, puts alpha(k_i) and alpha^{-1}(k_i) in N for every i. Hence t normalizes N. The group P is generated by N and t, so N is normal. Since chi kills N and chi(t)=1, the cyclic quotient P/N maps isomorphically onto Z. Thus N=ker(chi). QED.

This proves finite generation directly. It is not the invalid inference that composing a finitely generated-kernel map to a free group with a free-group character preserves finite generation.

## 4. The genus-2 two-ended witness

Write P_5 for the pure braid group on five points placed in convex pentagon position, with swing generators S_ij (1<=i<j<=5). We use the standard facts verified in [KMM], section 2:

- The ten S_ij generate, and their images form a basis of the abelianization.
- Swings supported on disjoint convex hulls commute.
- The full twist z=S_12345 generates the center and its abelianization is the sum of all ten pair-generator classes.

Assign a character chi:P_5->Z by

  chi(S_12)=chi(S_23)=chi(S_34)=chi(S_45)=chi(S_15)=1,
  chi(S_13)=chi(S_14)=chi(S_24)=chi(S_25)=chi(S_35)=-1.

It is an epimorphism and chi(z)=5-5=0. Let y_ij=S_ij on a side and y_ij=S_ij^{-1} on a diagonal. Every y_ij has character value 1 and these ten elements still generate P_5.

Here is a connected subgraph of their commuting graph. The five side generators form the cycle

  12 -- 34 -- 15 -- 23 -- 45 -- 12.

Attach the diagonal vertices by the edges

  13--45, 14--23, 24--15, 25--34, 35--12.

For every listed edge the two convex hulls are disjoint. Inverting a generator preserves commutation. Lemma 6, with t=S_12, proves that ker(chi) is generated by the nine differences y_ij t^{-1} for ij != 12.

Capping the boundary of a disk by a disk with one marked point identifies

  P_5 / <z> = PMod(S_{0,6}) =: Q.

For clarity, this familiar identification can also be obtained without a boundary-framing convention. Normalize the first two points of an ordered five-point configuration in C to 0 and 1. The exact homeomorphism

  Conf_5(C) = C x C^* x Conf_3(C\{0,1})

uses coordinates z_1, z_2-z_1, and (z_i-z_1)/(z_2-z_1) for i=3,4,5. The C^* loop is the full twist z. The last factor is the moduli space of a sphere with six ordered marked points, with three fixed at 0,1,infinity. Its universal marked-structure space is Teichmuller space, which is contractible; fixing the ordered points makes this a genuine covering (an automorphism of the Riemann sphere fixing 0,1,infinity is the identity). Hence its fundamental group is Q. This proves the identification and locates exactly the central factor being killed.

Because chi(z)=0, chi descends to an epimorphism bar-chi:Q->Z. Its kernel is the image of ker(chi), so it is generated by at most nine elements.

The Birman-Hilden theorem gives

  1 -> <iota> -> G_2 --Theta--> Mod(S_{0,6}) -> 1,

where iota has order two. The precise genus-2 statement is [MW], introduction and section 4; the paper supplies proof sketches in section 10. A complete primary proof of the more general fully ramified case is [W], Theorem 1.1 and section 4.2. The hyperelliptic double cover is fully ramified, and its total surface has Euler characteristic -2, so [W] applies. The extra identifications of the symmetric and liftable groups in this genus are verified in [MW], section 4, by the standard twist generators and their lifts. Set Gamma=Theta^{-1}(Q). Since Q is the pure subgroup, [G_2:Gamma]=6!=720. Set

  H_2 = ker(bar-chi composed with Theta|_Gamma).

There is an exact sequence 1-><iota>->H_2->ker(bar-chi)->1. Lift the nine displayed generators and adjoin iota. They generate H_2, so H_2 is finitely generated by at most ten elements. Finally Gamma/H_2=Z. Lemmas 1 and 3 give

  e(G_2,H_2)=e(Gamma,H_2)=e(Z)=2.

Only normality in Gamma is used; no normality in G_2 is asserted.

## 5. The genus-2 continuum-ended witness

Use the same Gamma and map to Q=PMod(S_{0,6}). Forget two ordered marked points to obtain the surjection

  Q -> PMod(S_{0,4}) = F_2.

The last equality also follows from the normalization of three points: the moduli space of four ordered sphere points is C\{0,1}, with free fundamental group of rank two.

The kernel K_infty is finitely generated. Specifically, the one-point forgetful sequences (the Birman sequence [H], printed page 144, applied here with at least four remaining marked points) give

  1 -> F_4 -> PMod(S_{0,6}) -> PMod(S_{0,5}) -> 1,
  1 -> F_3 -> PMod(S_{0,5}) -> PMod(S_{0,4}) -> 1.

Consequently 1->F_4->K_infty->F_3->1, and lifts of three generators together with four fiber generators generate K_infty. In particular it has a generating set of at most seven elements. The same finite-generation conclusion follows from the configuration-space fibration [FN], Theorem 1; these are kernels of forgetting points, not kernels of a character of F_2.

Let H_infty be the preimage of K_infty in Gamma. It is an extension of K_infty by <iota>, so has at most eight generators. The quotient Gamma/H_infty is F_2. A Cayley tree for F_2 has a Cantor end space, of cardinality 2^{aleph_0}. Lemmas 1 and 3 give

  e(G_2,H_infty)=2^{aleph_0}.

Together with H=G_2 and H={1}, this proves conclusion 3. It provides four realized values, not a four-value upper bound.

## 6. Low genus, kept separate

For g=0, G_0 is trivial, so only 0 occurs.

For g=1, G_1=SL(2,Z), and PSL(2,Z)=C_2*C_3. These standard identifications follow from the torus homology action and the modular fundamental domain. Here is an explicit route to the needed virtual-freeness statement. The kernel of C_2*C_3 -> C_2 x C_3 has index six and acts freely on the free-product tree. Its quotient graph has six edges and five vertices, so the kernel is F_2. Its preimage in SL(2,Z) is a central extension of F_2 by C_2. Lifting a free basis splits this extension, giving C_2 x F_2. A free factor therefore has finite index in SL(2,Z); taking its normal core gives a normal finite-index nonabelian free subgroup F of finite rank.

If H<=G_1 is finitely generated and of infinite index, L=H intersect F is finitely generated and of infinite index in F. The covering of a finite rose corresponding to L has finite core: loops for a finite generating set give a finite connected subgraph carrying its whole fundamental group, and the minimal core is contained in it. Outside that core there are trees. Since the covering is infinite there is at least one infinite tree; away from its root every vertex has degree 2 rank(F), so it has a continuum of ends. The countable locally finite graph has no more than continuum many rays, hence exactly continuum many ends.

Lemma 1 gives e(G_1,L)=2^{aleph_0}. The finite quotient in Lemma 2 gives e(G_1,H)=2^{aleph_0}. Finite-index H gives 0. This proves the stated genus-1 spectrum. These low-genus facts do not decide the genus>=2 question.

## 7. What remains unresolved by this attempt

For g>=3, the argument realizes 0 and 1 and confines a putative finitely generated subgroup with e(G_g,H)>=2 to vcd(H)>=4g-6. It does not settle those high-dimensional subgroups. For g=2, it realizes four values but supplies no complete upper classification. In particular the ordinary 0/1/2/infinity theorem for finitely generated groups is not being applied to arbitrary Schreier graphs.

The character example and dimension obstruction are deductions from standard structures, presented with complete proofs of the relative-ends and kernel steps. No assertion is made that these deductions are new in the mathematical literature. This document is suitable for auditing as a partial theorem only.

## References

[F] Benson Farb, Some problems on mapping class groups and moduli space, in Problems on Mapping Class Groups and Related Topics, Chapter 2, Question 2.1, printed page 15. Complete author-hosted book: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf .

[H] John L. Harer, The cohomology of the moduli space of curves, in Theory of Moduli, Lecture Notes in Mathematics 1337, Springer, 1988, pp. 138-221. DOI: https://doi.org/10.1007/BFb0082808 . Complete chapter: https://imag.umontpellier.fr/~calaque/GdT-CGEMC-Harer.pdf . Chapter 1, section 3, printed page 144 (forgetful sequence); Chapter 4, section 1, Corollary 4.2, printed pages 176-177 (duality and dimension). Original duality result: The virtual cohomological dimension of the mapping class group of an orientable surface, Inventiones mathematicae 84 (1986), 157-176, Theorem 4.1, https://doi.org/10.1007/BF01388737 . The complete 1988 author account was inspected; the 1986 article was not separately retrieved.

[IJ] Nikolai V. Ivanov and Lizhen Ji, Infinite topology of curve complexes and non-Poincare duality of Teichmuller modular groups, arXiv:0707.4322v1 (2007), https://arxiv.org/abs/0707.4322 ; complete PDF: https://arxiv.org/pdf/0707.4322 . Theorem 1.1, equation (3), and the end of section 3 corroborate the duality input and distinguish virtual duality from Poincare duality.

[KMM] Nic Koban, Jon McCammond, and John Meier, The BNS-invariant for the pure braid groups, Groups, Geometry, and Dynamics 9 (2015), 665-682, https://doi.org/10.4171/GGD/323 . Complete author manuscript dated January 22, 2014: https://web.math.ucsb.edu/~mccammon/papers/sigma-pure-braids.pdf . Definition 2.4, Lemma 2.5, and Remark 2.6 are the braid inputs. Theorem A is not needed for the elementary kernel proof above.

[MW] Dan Margalit and Rebecca R. Winarski, The Birman-Hilden theory, arXiv:1703.03448v1 (2017), https://arxiv.org/abs/1703.03448 ; complete PDF: https://arxiv.org/pdf/1703.03448 . Published as Braid groups and mapping class groups: The Birman-Hilden theory, Bulletin of the London Mathematical Society 53 (2021), 643-659, https://doi.org/10.1112/blms.12456 . The inspected version is the 2017 manuscript, not the publisher PDF.

[FN] Edward Fadell and Lee Neuwirth, Configuration spaces, Mathematica Scandinavica 10 (1962), 111-118, https://doi.org/10.7146/math.scand.a-10517 . Complete publisher PDF: https://journals.msp.org/mscand/article/download/2674/2673 . Theorem 1 gives the configuration-space fibration.

[W] Rebecca R. Winarski, Symmetry, isotopy, and irregular covers, Geometriae Dedicata 177 (2015), 213-227, https://doi.org/10.1007/s10711-014-9986-y . Inspected complete primary manuscript arXiv:1309.3650v1 (September 14, 2013), https://arxiv.org/pdf/1309.3650 . Theorem 1.1 and section 4.2.
