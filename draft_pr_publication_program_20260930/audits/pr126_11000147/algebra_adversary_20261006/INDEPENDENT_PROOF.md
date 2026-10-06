# Independent mathematical audit of PR126

Initial independent proof checkpoint: 2026-10-06 21:50 UTC. Mathematical validation estimate 70%; original budget 1/5, new central proof-search turns 0. No prior review or submitted verifier was read to obtain this proof.

## Exact claim and assumptions

Conditional on the source allowing nonsingular Anosov maps on the closed oriented torus, the submitted matrices define three distinct orientation-preserving diffeomorphisms, each Anosov, such that every pair satisfies a length-three braid relation and no pair commutes. No prescribed higher genus, boundary fixed pointwise, nonconjugacy, minimal generating set, or faithful Artin representation is part of this theorem. The source-category decision and historical priority are separate gates.

## Independent group proof

Let `a b a = b a b` in an arbitrary group, with `a != b`. Set `c = a b a^-1`. Multiplying the braid equality on the left by `b^-1` and the right by `a^-1` gives `b^-1 a b = c`. Conjugation by `a` sends the braid pair `(a,b)` to `(a,c)`. Conjugation by `b^-1` sends it to `(c,b)`. These operations are automorphisms of the group, so all three unordered pairs satisfy their braid relation.

If `c=a`, multiplying `a b a^-1=a` on the left by `a^-1` and right by `a` gives `b=a`. If `c=b`, then `a b=b a`. For any commuting braid pair `(u,v)`, the braid equality reduces to `u^2 v=u v^2`; multiplication by `u^-1` and `v^-1` gives `u=v`. Thus `c=b` is also impossible, and the same observation proves noncommutation of each distinct pair. Nothing assumes torsion freedom or a faithful representation. This works even in finite groups (for example the three transpositions of the symmetric group of degree three).

If the conjugacy-invariant class under consideration contains `a,b`, it also contains `c`. An odd braid relation also makes `a,b` conjugate: conjugation by `ab` takes `a` to `b`. Accordingly, conjugacy of the three elements cannot invalidate this particular existential claim.

## Integer matrices and actual maps

Direct integer multiplication gives determinant one and trace four for each submitted matrix. The fresh script checks both integral two-sided inverses, `C=A B A^-1=B^-1 A B`, and all three common braid products. Their exact values are:

```
A B A = B A B = [[0,-1],[1,0]]
A C A = C A C = [[7,-10],[5,-7]]
B C B = C B C = [[5,-13],[2,-5]]
```

For an integer matrix of determinant one, `f_M([v])=[Mv]` is independent of the representative because `M Z^2=Z^2`. Its inverse is `f_(M^-1)`, so it is a smooth diffeomorphism with positive Jacobian determinant. Under column-vector coordinates, actual composition is `f_M o f_N=f_(MN)`. Thus these are exact relations between actual maps, not merely relations in a quotient by isotopy. Distinct integer matrices induce distinct homology actions. In particular, the three maps and their mapping classes are distinct. The three pairwise products do not commute. Braid lengths one and two would imply equality and commutation, respectively, so their smallest positive braid length is three.

## Exact Anosov and foliation proof

For every matrix the characteristic polynomial is `t^2-4t+1`; its roots are `lambda=2+sqrt(3)>1` and `lambda^-1=2-sqrt(3)` strictly between zero and one. The real eigenlines are distinct. Since the matrix is constant, the associated translation-invariant tangent line fields give a globally invariant splitting of the torus tangent bundle. On one-dimensional stable and unstable eigenspaces the derivative scales Euclidean length exactly by `lambda^-1` and `lambda`, respectively. Hence the Anosov inequalities hold uniformly for all iterates, without a limiting or empirical argument.

For `M=[[a,b],[c,d]]` in this example (`b != 0`), eigenvectors `(b,lambda-a)` and `(b,lambda^-1-a)` are nonzero and transverse. Irrationality of both eigenvalues excludes a rational eigenline: if a nonzero rational vector is an eigenvector, a nonzero coordinate expresses the eigenvalue as a rational quotient. The corresponding translation-invariant foliations descend to the torus and have no singularities. A constant covector annihilating one line supplies its transverse measure. The covectors

```
ell_s=(lambda^-1-a,-b),  ell_s M=lambda ell_s;
ell_u=(lambda-a,-b),     ell_u M=lambda^-1 ell_u
```

are independently checked in the exact ring `Z[sqrt(3)]`. Integrating the absolute covector along transverse paths yields measured foliations. Under pullback by `f_M` their transverse measures scale by the displayed reciprocal factors. The pushforward convention swaps which reciprocal factor is assigned, without changing the invariant-foliation condition. This distinction is not a mathematical defect in the submitted claim.

The measured-foliation argument proves the nonsingular torus analogue of pseudo-Anosov behavior. Some literature restricts the word pseudo-Anosov to negative Euler characteristic surfaces; this proof does not settle that terminology. The primary source's explicit surface conventions must determine whether this theorem meets its question.

## Falsification checks and limits

The independent script uses explicit runtime guards, not Python assertions. It checks perturbed-matrix controls that must fail determinant and braid identities, exact covectors, the source's `X^2=-I`, `Y^3=I`, `XY=A`, `YX=B` example, and finite torus coordinates. Exhaustive checks of distinct braid pairs in `SL(2,F_p)` for `p=2,3,5` corroborate the general lemma, including finite-characteristic degeneracies. These finite computations are not the proof of the universal lemma or the dynamics.

No mathematical gap has been found in the precisely scoped conditional theorem. It does not prove any higher-genus, boundary-fixed, or faithful triangular-Artin statement. The triangle representation has the explicit additional relation `C=A B A^-1`; it therefore cannot be used as evidence of independent third generation or automatic Artin faithfulness. Nothing here certifies novelty or priority.
