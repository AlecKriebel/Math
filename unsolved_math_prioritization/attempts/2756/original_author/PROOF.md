# A planar-to-spherical transfer for wicket intersections

## 1. Conventions and scope

Let P be a set of m = 2n distinct points in the interior of a disk D, with n >= 2. Let B_m be the ordinary planar braid group, identified with the orientation-preserving mapping class group of (D,P) fixing the boundary pointwise. The points of P may be permuted.

Cap the boundary of D by a disk E to obtain a sphere S, and put p in the interior of E. Let

\[
q:B_m\longrightarrow \operatorname{Mod}(S,P)
\]

extend a representative by the identity on E and then forget E and p. This is not merely the quotient of B_m by its center.

Let tau_1 and tau_2 be trivial n-tangles with endpoints P in a 3-ball bounded by S. Their planar representatives lie away from E. Reflect the second tangle into the other ball and write L = tau_1 union reflected(tau_2). The reflection is part of the definition; the union of two upper-half-space tangles alone is not the bridge link.

Let W_i <= B_m be the stabilizer of the isotopy class of tau_i, where tangle isotopies fix the boundary. Let H_i <= Mod(S,P) consist of boundary mapping classes extending over the corresponding tangle ball while preserving its tangle setwise. Reflection identifies both boundary groups with the same Mod(S,P). Set

\[
K=W_1\cap W_2,\qquad G=H_1\cap H_2.
\]

Thus G is the side-preserving bridge Goeritz group. We do not add homeomorphisms exchanging the two balls. Neither endpoints nor individual tangle components are required to be fixed individually by a group element.

## 2. The full-preimage statement

**Lemma 1.** For either tangle, W_i = q^{-1}(H_i). Consequently K = q^{-1}(G), and q maps K onto G.

**Proof.** A braid representative gives a homeomorphism f of D fixing its boundary and preserving P. Extend f by the identity over E to a sphere homeomorphism, also denoted f. The action on a tangle can be described by extending f to the ball and applying that extension to the tangle. Its isotopy class is independent of the chosen extension: two extensions with the same boundary map differ by a boundary-fixing ball homeomorphism, which is isotopic to the identity relative to the boundary by the Alexander trick.

If the braid is in W_i, an isotopy relative to the boundary carries the image tangle back to tau_i. Isotopy extension, followed by composition with the original ball extension, gives a tangle-preserving ball homeomorphism with boundary f. Hence q(f) belongs to H_i.

Conversely, suppose q(f) belongs to H_i. Choose a representative f_0 of the same spherical mapping class that extends to a tangle-preserving ball homeomorphism F_0. There is an isotopy from f_0 to f through maps preserving P. Its endpoint permutation is constant, so after composing with f_0^{-1} it is an isotopy k_t from the identity to f f_0^{-1} fixing every point of P.

This isotopy extends to the ball while fixing the tangle. Here is an explicit local justification. Straighten the tangle near its endpoints so its intersection with a boundary collar consists of radial intervals {x} times [0,epsilon], x in P. Choose a collar cutoff rho that is one on the boundary and zero at the interior collar edge. On the collar use

\[
(x,s)\longmapsto(k_{t\rho(s)}(x),s),
\]

and use the identity outside it. These are homeomorphisms, and the radial tangle intervals are fixed because every k_u fixes P. Compose the time-one extension with F_0. The resulting homeomorphism preserves tau_i and has boundary exactly f. Thus the braid fixes the tangle isotopy class, as required.

The capping and forgetful maps are surjective, so q is surjective. Taking preimages of H_1 and H_2 gives K = q^{-1}(G), and surjectivity of the restricted map follows. This proves the lemma. QED.

## 3. The kernel that must not be dropped

**Lemma 2.** For m >= 3,

\[
N_m:=\ker q\cong F_{m-1}\times\mathbb Z.
\]

The direct-product identification is not asserted to be canonical.

**Proof.** Factor q into capping with a marked disk and forgetting its marked point:

\[
B_m\xrightarrow{c}\operatorname{Mod}(S,P\cup\{p\};p)
\xrightarrow{f}\operatorname{Mod}(S,P).
\]

The semicolon means that p is fixed individually, while P is preserved setwise. The capping exact sequence gives ker(c) = <z> isomorphic to Z, where z is the boundary Dehn twist, or full braid twist. This subgroup is central. The Birman exact sequence gives ker(f) isomorphic to pi_1(S minus P,p). Its hypothesis holds because chi(S minus P) = 2-m < 0. Both sequences, including these puncture conventions, are the standard capping and point-pushing sequences; see Farb-Margalit, Proposition 3.19 and Theorem 4.6 [FM].

Restricting c to N_m therefore gives

\[
1\longrightarrow\langle z\rangle\longrightarrow N_m
\longrightarrow\pi_1(S\setminus P,p)\longrightarrow1.
\]

The punctured sphere has fundamental group F_{m-1}. Choose a free basis and any lifts of its basis elements to N_m. Freeness extends this choice to a homomorphism section. Since the kernel <z> is central, the resulting semidirect product is a direct product. QED.

**Theorem 3.** For any pair of trivial n-tangles with common endpoints, n >= 2, the groups above fit into

\[
1\longrightarrow F_{2n-1}\times\mathbb Z\longrightarrow K
\xrightarrow{q}G\longrightarrow1.
\]

In particular K is infinite, irrespective of whether G is finite.

**Proof.** Lemma 1 places the entire kernel of q inside each W_i and makes q|K surjective. Lemma 2 identifies that kernel. QED.

## 4. Finiteness properties transfer in both directions

**Lemma 4.** In an exact sequence 1 -> N -> E -> Q -> 1 with N finitely presented, E is finitely generated if and only if Q is, and E is finitely presented if and only if Q is.

**Proof.** Finite generation passes to quotients. In the other direction, adjoining a finite generating set of N to chosen lifts of finite generators of Q generates E.

If E is finitely presented, choose finite generators of N as words in the generators of E and impose that they equal the identity. Their normal closure in E is N, since N is normal and those elements generate N as a group. This yields a finite presentation of Q.

Conversely, suppose N and Q have finite presentations. Use their generator sets X and Y, with chosen lifts of Y to E. Take the relators for N; the finitely many conjugation relations for y x y^{-1} and y^{-1} x y, expressed as words in X; and, for each defining relator r of Q, the relation r(Y) = w_r(X) expressing its lifted value in N. These are finitely many relations, all valid in E. To see completeness, first use the conjugation relations to move X letters to one side. If a word maps trivially to E, its Y word is trivial in Q; an expression as a product of conjugates of Q relators reduces it, using the lifted relations, to a word in X. That word is trivial in N and follows from the defining N relators. The presentation therefore defines E. QED.

Applying Lemma 4 to Theorem 3 gives the exact equivalences

\[
K\text{ finitely generated}\iff G\text{ finitely generated},
\qquad
K\text{ finitely presented}\iff G\text{ finitely presented}.
\]

Indeed F_r times Z has the finite presentation with generators x_1,...,x_r,z and relators [x_i,z] = 1. The transfer does not produce unknown generators or relators for G.

## 5. Verified low-bridge consequences

For the unknot with n = 2, HIKK Example 2.8 identifies the spherical group G with C2 times C2. Thus K is finitely presented and has an index-four subgroup F_3 times Z. In particular K itself is not that finite spherical group.

For any 3-bridge decomposition of the unknot, HIKK Example 2.9 supplies finite presentation of G. The preceding theorem therefore supplies finite presentation of the corresponding planar K, with kernel F_5 times Z.

These conclusions recover known low-complexity results through the necessary quotient correction. They are not presented as new solutions. No explicit lift-action table or finite presentation in Artin generators is claimed here.

## 6. Why finite presentations of the two stabilizers do not suffice

The abstract assertion that an intersection of two finitely presented subgroups is finitely generated is false. Here is a complete elementary example; it is not a counterexample involving wicket groups.

Let F = F(a,b), let chi:F -> Z send a to 1 and b to 0, and work in F times Z. The groups

\[
A=F\times\{0\},\qquad C=\{(w,\chi(w)):w\in F\}
\]

are both free of rank two, hence finitely presented. Their intersection is ker(chi) times {0}. The covering graph of the two-loop rose associated to ker(chi) has vertices indexed by integers, an a-edge from k to k+1, and a b-loop at each k. The a-edges form a spanning tree. Collapsing that tree gives one independent loop for every integer. Consequently ker(chi) is free on {a^k b a^{-k}: k in Z}; its abelianization has infinite rank, so it is not finitely generated.

An argument for K must exploit the simultaneous tangle geometry, rather than just finite presentability of its two factors.

## 7. Exact remaining gap

For arbitrary admitted pairs with unknot union and n >= 4, this work proves neither finite generation nor finite presentation of G, and consequently neither property of K. It gives no counterexample. Theorem 3 is a reduction, not an independent explicit classification of the unknown quotient.

A disk- or bridge-complex proof would need a specific G-invariant complex, a proof of its required connectivity, control of the quotient cells, and suitable finiteness of stabilizers. Connectivity or finite presentations available for each separate tangle stabilizer do not establish those simultaneous properties. Those steps are absent here, so that route is stopped rather than promoted to a proof.

## References

[FM] Benson Farb and Dan Margalit, *A Primer on Mapping Class Groups*, inspected version 5.0, Proposition 3.19, Theorem 4.6, and Section 9.1. [University-hosted text](https://pagine.dm.unipi.it/~a019210/Farb%20Magalit_Primer%20on%20Teichmuller%20theory.pdf). [Author's book listing](https://margalit.droppages.net/books.html).

[HIKK] Susumu Hirose, Daiki Iguchi, Eiko Kin, and Yuya Koda, *Goeritz groups of bridge decompositions*, International Mathematics Research Notices 2022, 9308-9356, [DOI](https://doi.org/10.1093/imrn/rnab001). Inspected [arXiv:2004.03098v1](https://arxiv.org/abs/2004.03098v1), Sections 1.6-1.7, Theorem 2.1, Examples 2.8-2.9, Question 2.10.
