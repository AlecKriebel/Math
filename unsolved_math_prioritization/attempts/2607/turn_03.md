# Attempt 3: affine variation in the abelian verbal subgroup

Date: 2026-10-03 UTC. Third substantive proof attempt.

## Reduced setting

Use Attempt 1 to quotient the finite torsion kernel of H=w(G). Thus H is a free abelian group of finite rank, normal in G, and conjugation by G induces a finite group of automorphisms of H. Write V=H tensor Q. All w-values lie in a fixed finite union of rational lines in V. We test whether varying arguments inside H forces these lines to coincide.

## An elementary affine-lattice lemma

Suppose an affine subset x+L, where L is a subgroup of V, is contained in finitely many one-dimensional rational vector subspaces. Then either L=0, or QL is one-dimensional and x belongs to QL.

Indeed, choose nonzero a in L. If x and a are linearly independent, the points x+n a, n in Z, lie on infinitely many different lines through 0: proportionality for two different integers would force the proportionality factor to be 1 by comparing coefficients of x, and then force the integers equal. Thus x belongs to Qa. If b in L is independent of a, take x+b in the same affine set and apply the argument to (x+b)+Z a; it is again impossible. Hence L is contained in Qa.

## Word expansion over an abelian normal subgroup

Fix an arbitrary group word v on n variables and a base tuple g=(g_1,...,g_n). For h_i in H, substitute g_i h_i for its i-th argument. Expanding a word as a sequence of letters and their inverses, move each h_i factor to the right, conjugating it by the fixed suffix of the base word. Because H is abelian, the H corrections commute, and conjugation on H depends only on the quotient element of the conjugating suffix in G/H. Corrections made by other h_j therefore do not alter these conjugation operators.

Consequently there are integral linear endomorphisms D_i(g) of H, each a finite signed sum of conjugation operators, for which

  v(g_1 h_1,...,g_n h_n) = v(g_1,...,g_n) · (sum_i D_i(g)(h_i)).

Here the last factor is written additively inside H; its order relative to the base factor is fixed by having moved corrections to the right. The identity holds when the base value is outside H as well, but for v=w both factors are in H, so it is an ordinary affine expression in V. This is an explicit elementary version of the Fox-derivative expansion for an abelian kernel.

Let L_g=sum_i D_i(g)(H). Every element of the affine lattice w(g)+L_g is an actual w-value, because the h_i vary independently. The preceding lemma therefore proves:

- Either L_g=0 and all H-perturbations of this base tuple leave its value unchanged;
- Or L_g has rank one, and its rational span contains w(g).

In particular any single fixed base tuple whose derivative images span rank two would refute the finite cyclic-cover hypothesis. This is a useful obstruction to proposed examples, not a construction of an example satisfying the hypothesis.

## Explicit commutator control

In a split semidirect product V semidirect Q, write elements as (v,A), with product (v,A)(u,B)=(v+A u,AB). With [x,y]=x^{-1}y^{-1}xy, direct multiplication gives translation part

  A^{-1}(B^{-1}-I)v + A^{-1}B^{-1}(A-I)u.

This follows from the four successive factors (-A^{-1}v,A^{-1}), (-B^{-1}u,B^{-1}), (v,A), (u,B). It supplies an exact check on the two leaf derivatives, including their signs and order. For deeper word trees the same rule recursively computes all leaf coefficient blocks alongside the quotient word value.

For instance A=B=-I on Q^2 gives translation 2v-2u, a rank-two image. The semidirect product Z^2 semidirect C_2 with inversion therefore cannot provide a counterexample even for the simple commutator word: its commutator values contain 2Z^2 and need infinitely many cyclic subgroups.

## The central obstruction

If H <= Z(G) and w is a commutator word, all the D_i are zero. Conjugation on H is trivial, so D_i is multiplication by the exponent sum of the i-th variable in w; each exponent sum is zero. Thus varying a tuple inside H gives no new values at all:

  w(g_1 h_1,...,g_n h_n)=w(g_1,...,g_n).

The finite-line condition cannot by this method join different values arising from distinct tuples of G/H. Assuming that some derivative must be nonzero would therefore be circular or false. The remaining central case is not removed by the finite conjugation action from Attempt 1.

## A bound on the conjugation image

Let s be the number of distinct nonzero rational lines that actually contain w-values in V. These lines span V. Conjugation permutes them. In the kernel of the permutation action, an automorphism acts as multiplication by +1 or -1 on each line: its restriction preserves the rank-one lattice H intersect L and is a lattice automorphism. The signs determine the automorphism because the lines span V. Hence the conjugation image has order at most 2^s s!, with s <= m. This does not bound the rank by one; the coordinate-axis action on Z^r shows why.

## Outcome

Proved: each coset tuple modulo H has either a singleton value image or one affine lattice on one line, and the finite conjugation group admits an explicit signed-permutation bound. Derived an exact rank test for split lattice extensions. The general question remains open because different coset tuples, especially with central H, have not been linked.

Best-guess completion: 25%. The attempt gives a concrete obstruction but leaves the central rank-collapse problem untouched.
