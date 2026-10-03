# Attempt 2: polynomial images in nilpotent groups

Date: 2026-10-03 UTC. Second substantive proof attempt.

## Goal and scope

Try to collapse the finitely many value directions using polynomial dependence on coordinates. This gives an affirmative answer for locally nilpotent ambient groups. It applies to arbitrary group words in this special class; it does not prove the general multilinear-commutator question.

## Polynomial-image lemma

Let F: Q^d -> Q^e be a polynomial map. If F(Z^d) is contained in a finite union of rational linear subspaces L_1,...,L_m, then the whole image F(Q^d) is contained in a single L_i.

Proof. Suppose no L_i contains the whole image. For each i choose a rational linear functional ell_i vanishing on L_i but with ell_i composed with F not identically zero. This is possible because L_i is a proper subspace and F(Q^d) is not contained in it. The nonzero polynomial product_i ell_i(F(t)) vanishes at every integral point, since each F(t) lies in some L_i. A rational polynomial vanishing on Z^d is zero: induct on d, using infinitely many integer roots in its last variable. This contradicts the fact that a polynomial ring over Q is an integral domain. The zero-subspace case is covered by the same argument; a subspace equal to Q^e makes the conclusion immediate.

This is a finite-union statement for a genuinely polynomial image on one integral lattice. It makes no assertion about arbitrary sets contained in finitely many lines.

## Standard nilpotent input, explicitly credited

For a finitely generated torsion-free nilpotent group N, Mal'cev's rational completion and Hall's coordinate theorem give:

1. A rational nilpotent Lie algebra with its finite Baker–Campbell–Hausdorff group, into which N embeds.
2. An ordered Mal'cev basis a_1,...,a_d with every element of N written uniquely as a_1^{n_1}...a_d^{n_d}, n_i in Z.
3. The logarithm of this coordinate expression, and multiplication, inversion, and every fixed word map in these coordinates, are rational polynomials. This follows from the truncated BCH formula; the logarithm of a power c^k is k log(c).

These are standard structural inputs, not results newly proved here. Hall's polynomial theorem is also recalled and used in A. Cant and B. Eick, “Polynomials describing the multiplication in finitely generated torsion-free nilpotent groups,” arXiv:1801.02932, subsequently J. Symbolic Computation 92 (2019), 203–210, DOI 10.1016/j.jsc.2018.04.014.

## Proposition: torsion-free nilpotent case

Assume N is finitely generated, torsion-free and nilpotent, and the values of an arbitrary word v are covered by cyclic subgroups C_i=<c_i> of N. In logarithmic coordinates, all values lie in the finite union of rational lines Q log(c_i).

By the standard input above, the map taking the integral coordinate tuple of the arguments to log(v(g_1,...,g_n)) is polynomial. The polynomial-image lemma puts its image in a single rational line L. Therefore all v-values belong to exp(L).

A one-dimensional Lie subspace is abelian and its BCH law is addition. Consequently exp(L) is an abelian subgroup, so v(N) is abelian and all its elements have logarithms in L. By Attempt 1, Lemma 1, v(N) is finitely generated. Its image under log is therefore a finitely generated subgroup of a one-dimensional rational vector space, which is cyclic (clear denominators for finitely many rational generators). Since exp/log are inverse and N is torsion-free, v(N) is cyclic or trivial.

Notice that we do not assert that an arbitrary subgroup of Q is cyclic. Finite generation is essential to the last step.

## Proposition: all locally nilpotent ambient groups

Let G be locally nilpotent and suppose its v-values have a finite cyclic cover. Attempt 1 gives finitely many v-values generating H=v(G). Put all the arguments of these values in a finitely generated subgroup K. Then v(K)=H, and local nilpotence makes K nilpotent.

The torsion subgroup U of a finitely generated nilpotent group is finite and characteristic, and K/U is torsion-free nilpotent. The cover descends to this quotient. The previous proposition makes v(K/U) cyclic. The natural map H -> v(K/U) has kernel H intersect U, which is finite and normal in H. Thus H is finite-by-cyclic.

This also covers finite groups within the nilpotent class, and the zero-image case produces a finite H.

## Why this does not finish the original question

Attempt 1 reduces a general counterexample to a solvable ambient group with an abelian verbal subgroup, not a nilpotent ambient group. A finitely generated solvable group need not admit one global nilpotent Hall-polynomial coordinate model. Replacing its word map by a polynomial map on a single irreducible affine space is unsupported.

Even a finite disjoint union of polynomial domains does not suffice: different components can map to different lines. The elementary set map from two copies of Q to Q^2, taking t to (t,0) on one component and to (0,t) on the other, has polynomial restrictions, finite line cover and rank-two generated image. This is a counterexample only to that proposed inference, not a realization as a group word map.

## Outcome

Affirmative special case: locally nilpotent G, for every word. General obstacle: a mechanism joining the different value directions in the solvable, nonnilpotent reduction. No full proof or counterexample to KOU-21.98.

Best-guess completion: 25%, heuristic and nonmonotonic. No novelty claim for the special case.
