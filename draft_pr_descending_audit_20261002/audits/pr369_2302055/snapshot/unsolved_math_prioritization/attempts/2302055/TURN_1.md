# Turn 1: finite polynomial pullback equivalence and a transcendental family

## Result and remaining target

Write L(f_1,f_2,f_3) for the source property: every entire F on C^3 bounded on the full hypersurface V_f={sum f_i(z_i)=0} is constant on V_f. All f_i below are nonconstant entire functions.

**Theorem A (exact finite-pullback equivalence).** If P_1,P_2,P_3 are nonconstant one-variable polynomials, then

    L(f_1,f_2,f_3) iff L(f_1 composed with P_1,
                              f_2 composed with P_2,
                              f_3 composed with P_3).

**Theorem B (a positive transcendental family).** L holds whenever

    f_i(z)=R_i(exp(Q_i(z))),  i=1,2,3,

where each Q_i is a nonconstant polynomial and each R_i is a nonconstant Laurent polynomial with complex coefficients. Negative Laurent powers cause no poles after composition with the exponential. In particular, the conclusion holds when each f_i differs by a constant from a nonconstant zero-free finite-order entire function.

These results use credited classical inputs, especially the Rubel–Squires–Taylor irreducibility theorem and the Lin abelian-cover theorem as presented by Lin–Zaidenberg. No novelty is claimed. The proof does not cover arbitrary entire f_i, arbitrary infinite covers of Liouville bases, or a limit of the displayed family. The original target remains unresolved at 1/5.

## 1. Classical inputs and topology

We use the following precise inputs.

1. **Separated-sum irreducibility (Rubel–Squires–Taylor).** For n>=3, the zero hypersurface of a sum of nonconstant one-variable meromorphic functions is irreducible on their pole-free domain. For the entire n=3 case used here, V_f is irreducible and hence connected. Demailly's published 1979 paper, printed p179, explicitly states this theorem and attributes it to Rubel, Squires and Taylor; its final Annals reference is 108 (1978), 553–567. The theorem statement and attribution have been checked in primary sources; the full original Annals proof has not been retrieved. We use this established result as a dependency, not as a new proof.
2. **Abelian covering Liouville theorem (Lin).** A connected regular abelian holomorphic cover of an ultra-Liouville complex manifold is Liouville. Here ultra-Liouville means that every bounded continuous plurisubharmonic function is constant. Lin–Zaidenberg, arXiv:alg-geom/9611020v2, Theorem 1.6, states the stronger hypernilpotent result. Its Sections 1.13–1.19 give the invariant-mean mechanism. The abelian case is the only case used below.
3. **Algebraic base criterion.** A smooth connected quasiprojective complex variety is ultra-Liouville (Lin–Zaidenberg, Section 1.3). Bounded plurisubharmonic functions extend across the boundary of a compactification, and are constant by the maximum principle.
4. Standard local complex-analytic facts: the regular locus of an irreducible complex space is connected and dense; a reduced hypersurface with singular locus of complex codimension at least two is normal. We do not infer Liouville from normality alone.

For completeness, the local singularity conditions in our setting have no hidden growth assumptions. The gradient of sum f_i is (f_1'(z_1),f_2'(z_2),f_3'(z_3)). Each derivative is a nonzero entire function and has a locally finite discrete zero set. Thus the singular set is contained in a locally finite discrete product. Repeated hypersurface factors would make the gradient vanish along a positive-dimensional component, which is impossible. The hypersurface is reduced, of pure dimension two, and normal. In particular its regular locus is connected by input 1 and the standard regular-locus fact. We need connectedness of the full hypersurface for Theorem A; no uniformization or smoothness of that hypersurface is assumed.

## 2. Polynomial push-forward of an ambient entire function

Let P_i have degree d_i and leading coefficient a_i !=0. Put D=d_1 d_2 d_3 and

    p(z_1,z_2,z_3)=(P_1(z_1),P_2(z_2),P_3(z_3)).

For any entire F on C^3, there are entire functions H_1,...,H_D on C^3 such that, for every w in C^3,

    product over p(z)=w, with multiplicities, of (T-F(z))
       = T^D + H_1(w)T^(D-1) + ... + H_D(w).                 (1)

This assertion includes critical values and repeated roots; no globally chosen root branches are needed.

Here is a direct construction. Let C_i(w_i) be a companion matrix for the monic polynomial (P_i(Z)-w_i)/a_i. Its entries are affine or constant functions of w_i. On the D-dimensional tensor product form the three commuting matrices

    A_1=C_1 tensor I tensor I,
    A_2=I tensor C_2 tensor I,
    A_3=I tensor I tensor C_3.

Define M_F(w)=F(A_1,A_2,A_3) by the globally convergent Taylor series of F at zero. On a compact w-set the three matrix norms are bounded by some K. The scalar Taylor series is absolutely convergent on every closed polydisc, so the matrix series converges absolutely and uniformly there. Thus all entries of M_F are entire functions of w.

For each fixed w, triangularize the three companion matrices separately and take the tensor product of those bases. The three A_i become simultaneously upper triangular, with diagonal triples running through all tuples of roots of P_i(Z)=w_i, counted with algebraic multiplicity. Polynomial evaluation and then uniform convergence show that M_F has diagonal entries F(z) for precisely those tuples. Its characteristic polynomial is therefore (1). Taking H_k to be its characteristic coefficients proves global entirety, including at branch collisions.

If |F(z)|<=M on p^{-1}(E) for a set E, the elementary symmetric-polynomial estimate gives

    |H_k(w)| <= binomial(D,k) M^k,  w in E.                (2)

The bound is independent of the sizes or locations of the roots of P_i. This uniformity is essential; a local choice of inverse branches would not by itself justify it.

## 3. Proof of Theorem A

Let V=V_f and W=p^{-1}(V). This W is exactly the separated-sum hypersurface for the three nonconstant entire functions f_i composed with P_i. The map p is surjective, and its restriction W->V is surjective: choose a root of each polynomial equation P_i(z_i)=w_i independently for every w in V.

First assume L(f_1,f_2,f_3), and let F be entire with |F|<=M on W. By (1)–(2), each ambient entire H_k is bounded on V, and hence is constant there, say h_k. Thus every F(z), z in W, is a root of the same fixed monic polynomial

    T^D+h_1 T^(D-1)+...+h_D.

Consequently F(W) is a finite set. Input 1 applies to W, because every f_i composed with P_i is nonconstant entire. Hence W is connected. Its continuous image F(W) is connected and finite, so consists of one point. This proves the forward implication without assuming that the individual inverse branches or generic fibers are connected.

Conversely, suppose L holds on W, and take an ambient entire G bounded on V. The composition G composed with p is entire and bounded on W, so is constant there. Surjectivity of W->V implies G is constant on V. This proves the reverse implication and Theorem A.

This proof is specific enough to preserve the source's ambient-entire quantifier. It does not silently replace it with a stronger holomorphic-extension assertion. The classical finite-cover symmetric-function idea is credited; the matrix construction supplies all multiplicity and ambient-extension details needed here.

## 4. Algebraic torus quotient for the basic family

First take Q_i(z)=z. Define the Laurent polynomial

    H(w)=R_1(w_1)+R_2(w_2)+R_3(w_3)

on (C*)^3 and its zero set S. Define V={H(exp(z_1),exp(z_2),exp(z_3))=0}. All R_i composed with exp are nonconstant entire: the exponential is onto C*, and a nonconstant Laurent polynomial cannot be constant on C*. Therefore V is irreducible by input 1.

The restriction of the coordinate exponential map

    E: V -> S,  E(z)=(exp(z_1),exp(z_2),exp(z_3))

is surjective and is locally biholomorphic as a map of complex spaces. It follows that S is irreducible: a proper decomposition of S into analytic closed subsets would pull back to a proper decomposition of V. The finite algebraic singular locus of S is contained in the product of the finite zero sets of R_i'(w_i) in C*. A derivative can have no zeros, in which case the singular locus is empty; it cannot vanish identically because R_i is nonconstant. Reducedness follows either locally from E or from this discrete-gradient argument.

Let Y=S_reg and X=E^{-1}(Y)=V_reg. These are connected smooth complex manifolds, and Y is a quasiprojective surface. The restriction E:X->Y is a regular unramified holomorphic covering. Its deck transformations are

    z -> z + 2 pi i (k_1,k_2,k_3),  k in Z^3.

All these translations preserve X, and they act freely and transitively on every fiber. The connectedness of X just established matters: it prevents an unjustified passage from a disconnected covering to a global constant. Thus the deck group is Z^3 and input 2 applies because Y is ultra-Liouville by input 3.

It follows that every bounded holomorphic function on X is constant. If F is entire and bounded on V, its restriction to X is such a function. Since X is dense in V, continuity gives the same constant on all of V, including every singular point. Therefore L(R_1 composed with exp,R_2 composed with exp,R_3 composed with exp) holds.

## 5. Polynomial phases and finite-order zero-free inputs

Apply Theorem A to the just-proved basic family with P_i=Q_i. This proves Theorem B for every nonconstant polynomial phase, without assuming the finite polynomial pullback is unramified. Branch collisions are already handled by (1).

As a familiar corollary, let f_i-c_i be zero-free entire of finite order and nonconstant. Hadamard factorization gives f_i-c_i=exp(Q_i) for a nonconstant polynomial Q_i (a nonzero scalar can be absorbed into the constant term of Q_i). Set R_i(w)=w+c_i. Theorem B applies. This uses the classical zero-free finite-order theorem; it does not extend to exp(g_i) with arbitrary transcendental entire g_i.

Examples newly encompassed by this explicitly checked reduction include arbitrary nonconstant Laurent polynomials of exp(z^m+lower terms), in each of the three coordinates, with unrestricted fixed degrees and coefficients. The proof supplies a family of affirmative instances, not a general solution or a claim of historical priority.

## 6. Why the full question is still open in this attempt

An arbitrary entire f_i need not admit a Laurent-polynomial/exponential description with polynomial phase. The coordinate map f_1 x f_2 x f_3 may have infinitely many branch or asymptotic values, is generally not proper, and need not give a regular abelian cover of an algebraic base. The companion construction depends on finite polynomial fibers. Lin–Zaidenberg explicitly exhibits failures for abelian covers of bases that are merely Liouville rather than ultra-Liouville. None of these missing hypotheses is supplied by source boundedness alone.

Polynomial approximation on expanding compact sets also does not pass the result: the assumption bounds F only on the original V, not uniformly on every approximating algebraic hypersurface. No such approximation transfer is asserted.

The next substantive search must address genuinely more general inputs or a mechanism that controls these infinite-fiber and base-geometry obstacles.

## Reproducibility and source qualifications

verify_turn1.py checks the finite companion/symmetric-coefficient mechanism on exact integer matrices, including repeated roots and unequal fiber degrees. Those controls validate algebraic identities; the analytic convergence, connectedness and covering arguments are proved above using the explicit credited dependencies. SOURCE_MANIFEST.json binds the source editions. No numerical test is presented as proof of a universal Liouville theorem.
