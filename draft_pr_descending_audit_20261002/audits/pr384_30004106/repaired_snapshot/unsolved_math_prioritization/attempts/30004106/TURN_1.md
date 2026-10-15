# Turn 1: scalar-extension reduction and a countable local test

**Scoped reductions; original unresolved, 1/5 substantive author turns.** The standard character/spectral-radius equivalence is credited to Benson, Proposition3.4.2. This turn investigates whether the arbitrary field and the full uncountable indecomposable basis can be removed from a counterexample search. It also isolates why checking growth identities only on positive elements is not an abstract substitute for symmetry.

Write A_k for the dimension-weighted completion in SOURCE_SCOPE. A species means a unital complex character; it is contractive for this norm.

## 1. Algebraic scalar extension is an isometric *-embedding

**Theorem.** For every algebraic extension K/k, extension of scalars induces an isometric unital *-homomorphism

    E:A_k -> A_K.

Its image is closed. If A_K is symmetric then A_k is symmetric. Equivalently, a failure over k remains a failure after algebraic extension. Therefore the universal source question can be reduced to algebraically closed coefficient fields, without claiming a reduction to finite fields or to the algebraic closure of the prime field.

For finite degree d=[K:k], let E be scalar extension on split rings and R restriction of scalars. Both are additive, while E is multiplicative. Decomposing a positive module preserves total vector-space dimension, so for complex linear combinations

    ||E x||_K <= ||x||_k,    ||R y||_k <= d ||y||_K.

As a kG-module, R E M is a direct sum of d copies of M, so R E=d id, also on the complexified split ring. Consequently

    d||x||_k=||R E x||_k <= d||E x||_K <= d||x||_k.

All inequalities are equalities. This argument does not require separability or a normal extension. Natural finite-dimensional duality gives E(M*)=(EM)*, so the involution is preserved.

For an arbitrary algebraic extension, fix a finite-support x. Decompose the finitely many K-extended modules into indecomposables. The matrices for their summands, decomposition isomorphisms, and isomorphisms between repeated isomorphism types involve only finitely many elements of K. They lie in a finite extension K_0/k. The resulting summands over K_0 are indecomposable, since a decomposition there would remain a decomposition over K. Two types distinct over K cannot be isomorphic over K_0, and the chosen isomorphisms make every repeated type already identified over K_0. Thus the exact weighted norm of E x is already its norm over K_0. The finite-extension argument proves equality. Density now gives the claimed isometric *-embedding of completions.

This descent of a finite decomposition uses algebraicity. It is not a specialization theorem for arbitrary families or for infinitely many tensor decompositions.

For the symmetry implication, every power has the same norm before and after E, so the spectral-radius formula gives

    rho_k(x)=rho_K(E x),    rho_k(x*x)=rho_K((E x)*(E x)).

If A_K is symmetric, its identity rho(y*y)=rho(y)^2 therefore holds in A_k. Benson's equivalent characterization proves symmetry of A_k. No extension of every character from a closed subalgebra is assumed, and no general spectral-invariance claim for arbitrary Banach subalgebras is needed.

## 2. Any obstruction lies in one countable tensor-generated subring

Fix one indecomposable kG-module M. Let I_M consist of all indecomposable summands occurring in

    M^(tensor a) tensor (M*)^(tensor b),   a,b>=0,

including the trivial module for a=b=0. Each tensor product has finitely many summands, so I_M is countable. It is closed under duality and under taking summands of products of two of its members: their product is a summand of a larger displayed tensor product.

Let B_M be the closed coordinate subspace of A_k supported on I_M. It is a closed unital *-subalgebra with its inherited norm, exactly the weighted l¹ completion of that tensor-closed split subring.

**Theorem.** A_k is symmetric if and only if B_M is symmetric for every indecomposable M.

If A_k is symmetric, equality of norms on all powers and the radius identity prove symmetry of B_M. Conversely, let s be any character of A_k. Its restriction to every B_M is a character, hence respects duality on M if B_M is symmetric. It then respects duality on every basis element, every finite complex combination, and by continuity every element of A_k. The character criterion proves symmetry.

More explicitly, failure of symmetry supplies a character s and a single basis element M with

    s([M*]) != conjugate(s([M])).

It is enough to test this one module inside its countable B_M. If z=s([M]) and w=s([M*]), then at least one of

    h_1=[M]+[M*],    h_2=i([M]−[M*])                     (1)

has a nonreal value under s. Both are self-adjoint, with Gaussian-integer coefficients supported on at most two basis elements. Indeed if z+w and i(z−w) are both real, then w=conjugate(z). Thus any full obstruction has a finite self-adjoint witness of this particularly simple form. It need not be the class of an actual module: h_2 generally is not.

## 3. An exact compactness criterion for the local species

Enumerate I_M and write d_i=dim M_i and

    [M_i][M_j]=sum_l n_ijl [M_l].

The coefficients are nonnegative integers, and each sum is finite. Consider the compact product

    P=product_(i in I_M) {z in C: |z|<=d_i}.

A point (z_i) defines a dimension-bounded species precisely when

    z_0=1,    z_i z_j=sum_l n_ijl z_l                    (2)

for every i,j. Necessity is immediate. Conversely the assignment extends linearly on the free basis; (2) is multiplicativity, and

    |sum_i c_i z_i|<=sum_i |c_i|d_i

gives a contractive extension to the completion. Thus no additional undisclosed continuity condition is missing.

Fix epsilon>0 and impose also the closed condition

    |z_(M*)−conjugate(z_M)|>=epsilon.                    (3)

**Theorem.** There is a local species satisfying (3) if and only if every finite subsystem of (2), together with the norm bounds, z_0=1 and (3), is feasible.

All equations involve finitely many coordinates and define closed subsets of P. The assertion is exactly the finite-intersection property for compact P. A finite subsystem is a finite real polynomial feasibility problem in real and imaginary coordinates. Its multiplication constants and dimension bounds are integers; epsilon may be chosen rational. Unused coordinates can be set arbitrarily within their disks.

Consequently symmetry is equivalent to the following collection of finite-exclusion assertions: for every M and every positive rational epsilon, some finite subsystem excludes (3). This is not a claim that one finite test suffices for the original problem, or that feasible finite truncations certify a species. Infinite compatibility is essential. Nor is an effective algorithm for all indecomposable decompositions over an arbitrary field assumed.

Together with Section1, this narrows a possible counterexample to an algebraically closed field and a countable tensor-closed family generated by one module. It does not reduce that field to a finite field: matrix entries may be transcendental, and simultaneous preservation of all tensor decompositions under specialization is unproved.

## 4. A precise failed-shortcut control outside the Green-ring class

The source proves that symmetry implies the gamma duality identity for positive module classes in quotient completions. It does not assert its converse. Even the analogous spectral-radius identity for every positive basis combination is insufficient for an arbitrary commutative Banach *-algebra.

Let C=l¹(Z) with convolution, write u for its generator, and give it the nonstandard involution

    (sum_n a_n u^n)*=sum_n conjugate(a_n)u^n.

This is an isometric antilinear involution and an antiautomorphism because convolution is commutative. Every nonnegative real combination x is self-adjoint, so automatically

    rho(x*x)=rho(x²)=rho(x)^2.

Nevertheless C is not symmetric. Evaluation u->i is a contractive character and u is self-adjoint with nonreal value. In fact sigma(u) is the unit circle: ||u||=||u^{-1}||=1 bounds every character value in modulus both ways, and all unit-circle evaluations exist.

For x=1+i u, one has x*x=1+u². Hence

    rho(x)=2,    rho(x*x)=2 <4=rho(x)^2.

This ring with this involution is NOT a modular Green ring: the coefficient-of-unit duality axiom fails for u and u^{-1}. It is not an original-question counterexample. Its role is solely to demonstrate the logical gap in proving full symmetry by checking only positive-growth identities without the extra representation-theoretic input.

## Remaining gap after 1/5

The local compactness criterion has not excluded non-Hermitian species for all actual modules, and it has not produced one. The scalar-extension reduction removes arbitrary algebraic coefficient-field issues but leaves the modular tensor-product problem. Subsequent turns must use actual representation-theoretic constraints to control these species; an abstract nonsymmetric algebra or a positive growth formula is insufficient.
