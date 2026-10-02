# Turn 1: coefficient profiles and the first possible dimensions

## Direction and outcome

We first test whether coefficient change alone forces the proposed2/3 lower bound. It does not: elementary finite cochain models can display arbitrarily large rational/integral gaps, but they are not group resolutions or admissible boundaries. For actual torsion-free hyperbolic groups we obtain a precise finite-prime obstruction and isolate the first possible pair as(cd_Q,cd_Z)=(2,4). These are necessary conditions, not a solution.

The prime-field detection theorem below is explicitly credited to Dicks–Leary, Proposition9, whose complete proof on the downloaded page13 was read. The finite-denominator argument is a standard reconstruction; no novelty is claimed.

## 1. Boundary shift and low dimensions

Write d=cd_Z(G) and q=cd_Q(G) for a nontrivial torsion-free hyperbolic G. Such a group is infinite and admits a finite classifying complex, for instance the quotient of a sufficiently large contractible Rips complex. In particular d is finite and q<=d by flat rational base change.

Also q>=1. If q=0, the augmentation QG→Q would split as a QG-module map. The image of1 under a splitting would be a finitely supported, left-G-invariant element of QG with augmentation1. No such nonzero element exists for infinite G.

The credited Bestvina–Mess formula gives

    r=dim_Q(boundary G)=q-1,
    n=dim_Z(boundary G)=d-1.

These are relative Čech cohomological dimensions. For finite-dimensional compact metric spaces integral dimension equals covering dimension. Therefore the strict target is

    3q<2d, equivalently 3r+1<2n.                (1)

There is an essential shift: comparing r/n directly with2/3 is a different inequality.

If q=1, the boundary has rational cohomological dimension0 and hence covering dimension0. Here is the elementary coefficient-independent point: for any two distinct points x,y, the degree0 restriction to the closed set{x,y} is surjective because the next relative rational cohomology group vanishes. A locally constant rational-valued function taking different values at x,y therefore exists, so clopen sets separate any two points. Compactness upgrades this to a clopen neighborhood basis. Thus the boundary is zero-dimensional, and its integral cohomological dimension is0. Bestvina–Mess now gives d=1.

Consequently no group with d<=3 can beat2/3. Every witness has q>=2 and

    d>=floor(3q/2)+1.

The smallest possible integral dimension is4, with rational dimension2. Its boundary would have covering dimension3 and rational cohomological dimension1. Existing(2,3) groups attain equality, as the source states.

## 2. Group-ring coefficient change

Let G have a finite classifying complex. Its finite free ZG cellular resolution C_* gives, for every degree k,

    H^k(G;QG) = H^k(G;ZG) tensor_Z Q.           (2)

Indeed Hom over ZG from a finitely generated free module commutes with localization; the corresponding finite cochain complex over QG is the localization of the integral one. Localization is exact, so it commutes with cohomology. The same argument works for Z[1/N]. Left modules in the resolution produce right group-ring modules in these cohomology groups; none of the arguments assumes a trivial action.

For type FP groups of finite cohomological dimension, the top nonzero group-ring cohomology detects that dimension. Briefly, a finite projective resolution of minimal length d has nonzero top cohomology with group-ring coefficients: if its dual last differential were onto, finite-projective duality would split the original last inclusion and shorten the resolution. Conversely no cohomology exists above d. This is also the standard input in Dicks–Leary Proposition9.

It follows from(2) that if q<d, all A^k=H^k(G;ZG), k>q, are torsion abelian groups, while A^q has a nonzero rationalization. This is not a statement about ordinary H^k(G;Z).

## 3. The top discrepancy is seen by a prime field

A finite projective resolution of length d exists with finitely generated terms: truncate a finite free resolution at its projective dth syzygy. Thus

    A^d = coker(Hom(P_{d-1},ZG)→Hom(P_d,ZG))

is finitely generated as a right ZG-module. If q<d it is a nonzero torsion abelian group. Choose finitely many ZG-module generators; their finite additive orders have a common multiple M. Since integers are central, M annihilates the entire module. This uniform annihilator is established for the **top** module, not by assuming lower cohomology modules are finitely generated.

Some prime p dividing M has a nonzero p-primary component of A^d. A nonzero abelian p-group of bounded exponent cannot equal p times itself: iterating such a surjection would annihilate it. Hence A^d/pA^d is nonzero for some p. Top-degree base change, or the cochain universal coefficient sequence with zero next cohomology, gives

    H^d(G;F_p G) = A^d tensor_Z F_p !=0.

The integral projective resolution base-changes to an F_p G projective resolution, so cd_Fp(G)<=d. Consequently

    cd_Fp(G)=d for at least one prime p          (3)

whenever q<d. This is the torsion case of the credited Dicks–Leary prime-field detection theorem.

Their preceding example with integral dimension3 and dimension2 over **every** field does not contradict(3): the original Coxeter example is infinitely generated, and the two-generator modification is not asserted to be of type FP. Finite generation alone is insufficient. This distinction was checked directly in that primary text.

## 4. Only finitely many primes can exceed the rational dimension

There exists a nonzero integer N such that

    cd_{Z[1/N]}(G)=q,
    cd_{F_p}(G)<=q for every prime p not dividing N. (4)

To see this, tensor the finite free integral resolution C_* with Q. Since cd_Q(G)=q, the qth syzygy is projective and the surjection C_q⊗Q onto it splits. Let e be the resulting projection of C_q⊗Q onto a copy of that syzygy. Then

    e²=e, d_q e=d_q, e d_{q+1}=0.

All entries of the finite matrix e involve only finitely many rational denominators and finitely many group elements. Choose N clearing those denominators. The same identities hold over R=Z[1/N]. The original localized complex is exact. Its differential d_q embeds im(e) into C_{q-1}⊗R: an element of im(e) in its kernel lies in im(d_{q+1}), where e vanishes, and hence is zero. The image is all of im(d_q), by d_q e=d_q. Thus replacing C_q by the finitely generated projective module im(e) gives an R G projective resolution of length q. Rational base change provides the reverse inequality, proving the equality in(4).

For p not dividing N, tensor this resolution with F_p over R. It remains exact: its augmented exact sequence is split as a sequence of R-modules, since its terms are R-projective and its final module R is R-projective; split successively from the augmentation. Its terms become projective F_p G-modules. This proves the field upper bound. No flatness of F_p over R is falsely assumed.

Additionally(2) over R shows that every class in A^k for k>q is killed by some power of N. A common exponent for all classes in those lower torsion degrees has not been proved. Equations(3),(4) say a candidate's integral dimension must be detected by one of a finite exceptional set of primes.

## 5. Why this does not yield the desired ratio bound

For any2<=q<d and prime p, take a finite free **abelian cochain complex** consisting of a free Z class in degree q and the two-term block

    Z in degree d-1 --times p--> Z in degree d.

Its cohomology is Z in degree q and Z/p in degree d, with the evident direct sum convention when q=d-1. Rationally only degree q survives; modulo p there are extra classes in degrees d-1 and d. Inverting p contracts the upper block. Thus every coefficient restriction above is compatible with q/d arbitrarily small at the level of a finite cochain complex.

This complex is not claimed to be Hom of a group resolution, compactly supported cochains of a cocompact contractible space, or the relative Čech data of a hyperbolic boundary. Even a finite polyhedron realizing those **global** cohomology groups has rational relative dimension d: an open ball in the interior of a top-dimensional simplex has nonzero compactly supported rational cohomology in degree d. Low global rational cohomology alone therefore cannot provide the required boundary.

## 6. Controls and next direction

The checker applies deterministic integral unimodular changes of basis and adds acyclic summands to the model complexes. Exact rational and prime-field ranks verify the coefficient profiles, chain identities, finite exceptional-prime behavior and contraction of the upper block. It also checks the arithmetic boundary shift and strict dimension threshold. Finite linear algebra does not construct the required group.

The next turn must use geometric group constraints beyond these algebraic profiles, especially the Coxeter nerve and its deleted-simplex cohomology. The full source question remains unresolved after this first turn.
