# Turn 4: a monodromy criterion and the double-exponential barrier

## Outcome

A further sufficient condition is proved for one source input, with the other two still arbitrary. The condition is on the full inverse monodromy, not merely on the number of singular values. An explicit computation for exp(exp z) shows why finite singular-value data do not automatically meet it.

**Theorem.** Let f be nonconstant entire. Suppose there is a finite set S in C such that

    f: C minus f^{-1}(S) -> C minus S

is a surjective unramified covering. Let G be its monodromy permutation group on one fiber. If G is virtually nilpotent, then the source property holds for (f,g,h) for every pair of nonconstant entire g,h.

Here virtually nilpotent means that G has a nilpotent subgroup of finite index. The monodromy group is the image of the fundamental group in the permutation group of the fiber; it is not assumed to equal the deck group of the original possibly nonnormal covering.

This theorem is a credited application of the classical nilpotent-cover Liouville theorem combined with a checked pullback and normal-cover argument. It does not establish virtually nilpotent monodromy for arbitrary entire functions, or even for all functions with finitely many singular values. The original target remains unresolved at 4/5.

## 1. Ultra-Liouville finite covers

We first record a finite-cover consequence, valid for complex manifolds. If Y is ultra-Liouville and X->Y is a connected finite unramified holomorphic cover, then X is ultra-Liouville. Given a bounded continuous plurisubharmonic function v on X, its finite fiber maximum is a bounded continuous plurisubharmonic function on Y, hence constant. The maximum is achieved at some point of X, and the maximum principle gives constancy of v on connected X.

Consequently, a connected regular cover X->Y with virtually nilpotent deck group K is Liouville whenever Y is ultra-Liouville. Choose a nilpotent normal finite-index subgroup N of K: starting with a nilpotent finite-index subgroup, take the intersection of its finitely many conjugates. This core remains nilpotent as a subgroup of the original nilpotent group. The intermediate cover X/N->Y is finite and hence ultra-Liouville. The cover X->X/N has nilpotent deck group N, so Lin's theorem (Lin–Zaidenberg Theorem 1.6) makes X Liouville.

We use no theorem saying that every amenable or every solvable cover of a noncompact ultra-Liouville base is Liouville. Such a replacement is not justified by the source theorem.

## 2. The normal closure and its pullback

Put B=C minus S and X_f=C minus f^{-1}(S). Both are connected: the removed sets are finite or locally finite discrete, respectively. Fix basepoints and let

    rho:pi_1(B)->G

be the monodromy homomorphism of the covering X_f->B. Its kernel defines a connected regular covering B_hat->B with deck group G. The point stabilizer in the original monodromy action contains this kernel, so there is a covering B_hat->X_f over B. This is the topological normal closure; no algebraic Galois closure of an infinite-degree map is assumed.

For arbitrary nonconstant entire g,h, set

    H(y,z)=-g(y)-h(z),
    U={(y,z) in C^2:H(y,z) not in S}.

The excluded set is a proper analytic subset, a finite union of level hypersurfaces of the nonconstant entire H. Its complement U is connected and ultra-Liouville. Indeed every bounded continuous plurisubharmonic function on U extends plurisubharmonically across the analytic subset to C^2, and bounded-above plurisubharmonic functions on C^2 are constant.

Pull B_hat->B back by H:U->B. Any connected component Z of this pullback is a regular cover of U whose deck group G' is a subgroup of G, namely the monodromy image of pi_1(U) in G after a basepoint choice. It is not necessary that this image equal G. A subgroup of a virtually nilpotent group is virtually nilpotent: intersect it with the finite-index nilpotent core. Therefore Section 1 makes Z Liouville.

The corresponding pullback of X_f->B is

    V^0={(x,y,z):f(x)+g(y)+h(z)=0, f(x) not in S}.

It is a smooth covering of U. The full hypersurface V is irreducible by the credited Rubel–Squires–Taylor theorem. Removing the proper analytic subset {f(x) in S} leaves V^0 connected and dense. Properness of that subset follows as before: a fixed f(x) allows only a discrete set of x and one equation in y,z, so cannot contain an open part of the two-dimensional hypersurface.

The map from the full pullback of B_hat to V^0 is a covering, and its restriction from each connected component Z surjects onto connected V^0 by path lifting. Thus a bounded holomorphic function on V^0 pulls back to a bounded holomorphic function on Z, is constant there, and is constant on V^0 by surjectivity. Every ambient entire F bounded on V therefore is constant on V^0 and, by density, on V. This proves the theorem.

## 3. Relation to the earlier explicit family

For f(z)=R(exp z), with R a nonconstant Laurent polynomial, remove a finite set containing the rational map's finite branch values and its finite values at 0 and infinity. Each generic inverse is obtained by first choosing one of d rational inverse roots u_j(w), and then a logarithm. Label the fiber by (j,n), 1<=j<=d, n in Z. A continued loop permutes j and changes the logarithm by an integer depending on j. Hence its monodromy embeds in

    Z^d semidirect S_d.

This group is virtually abelian, so the criterion recovers the basic case of turn 3. The arbitrary polynomial phase still follows from turn 1. The reasoning here does not claim that every polynomial precomposition has virtually nilpotent inverse monodromy; that separate finite-pullback theorem is what permits those phases.

Finite singular values alone are not enough, as the next exact example shows.

## 4. Exact inverse monodromy of exp(exp z)

Let f(z)=exp(exp z). Over B=C minus {0,1}, the inverse branches have the form

    z=Log(L(w)+2 pi i k)+2 pi i n,   (k,n) in Z^2,          (1)

where L is a local logarithm of w. On a sufficiently small simply connected neighborhood avoiding 0 and 1, none of L(w)+2 pi i k vanishes, and all logarithms in (1) exist. These branches account for every preimage and give a surjective covering over B. In particular the finite branch-exclusion hypothesis is satisfied with S={0,1}; f has no critical points, but those two omitted/asymptotic values matter.

Choose generators of pi_1(B) given by positive loops around 0 and 1. The loop around 0 increases the inner logarithm index k by one. Its possible additional n-shifts can be removed by relabeling n separately at each k, since the k-orbits are infinite with no cycle. Thus its action may be written

    a(k,n)=(k+1,n).

For a small loop about 1, exactly one inner logarithm branch vanishes at the enclosed point. Its outer logarithm gains 2 pi i; every other branch is locally nonzero across that disc. After a basepoint path and index choice this generator is

    b(k,n)=(k,n+1 if k=0, otherwise n).

The relabeling that makes a pure shift does not change this unit translation on its single k-fiber. Conjugates a^j b a^{-j} translate n independently on the fiber k=j. They commute, each has infinite order, and a finite product of their powers is the identity only if every exponent is zero. Therefore

    G = (direct sum over j in Z of Z) semidirect Z
      = Z wreath Z,                                       (2)

where the last Z shifts the lamp positions. This is an equality of faithful permutation groups generated by the two puncture loops, not merely a quotient or a group containing some computed finite pattern.

The group (2) is not virtually nilpotent. If a finite-index subgroup K were nilpotent, it would contain some a^r and b^s with positive integers r,s. Write delta_j for the lamp with value one at j. The commutator

    a^r b^s a^{-r} b^{-s}

has lamp vector s(delta_r-delta_0). Iterating commutators with a^r gives the k-th finite-difference vector

    s(shift_r-I)^k delta_0.

For every k>=1 its coefficient at position kr is s, so it is nonzero. All these arbitrarily deep commutators lie in K, contradicting nilpotence. This proves that no finite-index nilpotent subgroup exists.

## 5. What has and has not been excluded

The criterion offers another rigorously stated sufficient condition for arbitrary other inputs. The explicit double-exponential calculation shows that replacing it by 'f has finitely many singular values' is a genuine missing implication, not a theorem proved by the present argument.

This is not a counterexample to the original function-theory problem. For instance, exp(exp x)+exp y+exp z=0 is already affirmative by turn 3 using its second input. Even for a triple of double exponentials, non-virtually-nilpotent inverse monodromy by itself neither constructs a bounded holomorphic function nor proves failure of Liouville. Amenability or metabelian structure also does not supply the absent conclusion of the quoted cover theorem.

The fifth and final search will examine the natural double-exponential stress test without confusing a failed sufficient criterion with an actual negative answer.

## Sources and controls

The covering formulation of singular values is checked against Rempe-Gillen and Sixsmith, arXiv:1502.00492v2, Section 2, especially Definitions 2.1 and Remark 2.2. The theorem above assumes a surjective covering explicitly, so it does not rely on conventions about values omitted from a general analytic map. Nilpotent Liouville covering input remains Lin–Zaidenberg Theorem 1.6. SOURCE_ADDITION_T4.json binds the added primary source.

Exact controls implement the infinite wreath product through finite-support integer lamp vectors, verify the action and conjugation laws on finite samples, and check the finite-difference endpoint certificates. These supplement the universal group proof and do not assert a bounded-function counterexample.
