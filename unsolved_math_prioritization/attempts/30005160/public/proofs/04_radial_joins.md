# Proof 04  Radial test functions and affine joins

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md); [Centered crosses for exponents at least three](03_centered_cross_above_three.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## 1. A common radial test-function class

Let g:R->R be smooth and even with g''''>=0. Define its angular radialization on C by

Phi_g(z)=E_t g(Re(e^(-it)z)),

where t is uniform on the circle. Then Phi_g is radial and bisubharmonic, because

Delta^2 Phi_g(z)=E_t g''''(Re(e^(-it)z))>=0.

Approximation extends the arguments below to continuous even g with fourth distributional derivative a nonnegative measure, including g(x)=|x|^p for p>=3. Such approximation can use even positive mollifiers and uniform convergence on the compact ranges relevant to each finite polynomial.

### Scalar lemma for arbitrary symmetric variables

For independent bounded symmetric real variables X_1,...,X_n, set

G_g(s_0,...,s_n)=E g(sqrt(s_0)+sum sqrt(s_j) X_j).

Then G_g is lattice-supermodular. This gives an alternative elementary proof of the scalar lemma in the centered-cross supplement.

For i!=j>=1, differentiation on the positive orthant gives

G_{s_i s_j}=1/(4 sqrt(s_i s_j)) E[X_i X_j g''(sqrt(s_0)+sum sqrt(s_k)X_k)].

Conditional on all other variables and on |X_i|,|X_j|, pair the four signs. Writing h=g'', which is convex because h''=g''''>=0, the resulting bracket is a positive factor times

h(w+u+v)+h(w-u-v)-h(w+u-v)-h(w-u+v)>=0,

for u,v>=0. The inequality follows because a convex function has increasing finite differences, or because h(w+t)+h(w-t) is nondecreasing for t>=0 and u+v>=|u-v|.

For i=0 and j>=1, the same derivative formula has X_0=1 and denominator 4 sqrt(s_0 s_j). First average h over all random terms except j. The result is even and convex, since h is even and convex and that remaining sum is symmetric. An even convex function is nondecreasing on [0,infinity). Pairing X_j with -X_j then gives a nonnegative expression, as |a+u|>=|a-u| for a,u>=0. Hence every mixed derivative is nonnegative. Boundary coordinates follow by continuity.

### Centered-cross comparison for Phi_g

The centered-cross projection proof applies unchanged with this G_g in place of G_p. Therefore {0,+/-e_1,...,+/-e_n} has sign-majorant comparison for the expectation of Phi_g of its polynomial, whenever g is even and g''''>=0.

### Other positive blocks

The two-layer simplex proof in the earlier circuit chapter applies to any radial continuous bisubharmonic Phi: replace |z|^p by Phi in its circle/disk differentiation argument. The multiradius mean is supermodular because its mixed derivatives are positive convolutions of Delta^2 Phi. It therefore applies to Phi_g.

The center-free cross-polytope has the same coefficient-dependent radial expectation as the two-layer class, by the common-rotation identity, so it also applies to Phi_g. A singleton has sign equality for radial Phi_g.

## 2. Closure under adding independent radial noise

Let Y be any bounded rotationally invariant complex random variable. For smooth even g with g''''>=0, write S=Re(Y). Its law is symmetric and is also the law of Re(e^(-it)Y) for every t. Define

h(x)=E g(x+S).

Then h is even and h''''>=0. Moreover

E_Y Phi_g(z+Y)=E_t h(Re(e^(-it)z))=Phi_h(z).

Thus each positive block comparison above remains valid after adding independent bounded rotationally invariant noise. Approximation proves the same for the distributional test class. In particular g(x)=|x|^p, p>=3, belongs to this class, and

Phi_g(z)=m_p |z|^p,

with m_p=E|cos(t)|^p>0. The positive factor does not affect any comparison.

## 3. Affine joins of the positive blocks

Let Gamma be a finite integer-frequency configuration with a partition into labelled blocks Gamma_b such that its augmented integer relation lattice decomposes as

ker_Z[(1,n) : n in Gamma] = direct_sum_b ker_Z[(1,n) : n in Gamma_b].

This is the usual affine-matroid-component/affine-join relation decomposition. Suppose each block has the same labelled affine relation lattice as a singleton, a two-layer simplex, a center-free cross-polytope, or a centered cross-polytope with its center.

Insert an independent common phase into the original exponential polynomial. Its joint phase distribution is Haar measure on the compact subgroup H of T^Gamma whose annihilator is the displayed relation lattice. The direct-sum relation decomposition implies

H=product_b H_b,

since the product group has exactly the same annihilator. Hence the block polynomial values S_b are independent. Each is rotationally invariant: every affine relation inside a block has coordinate sum zero, so H_b contains the block diagonal circle.

Fix a sign pattern. To replace signs by plus signs in one block, the sum of the other blocks is bounded independent rotationally invariant noise. Section 2 therefore gives the required inequality for that replacement at every p>=3. Repeat through the finite collection of blocks. This proves sign domination for the full affine join. Convexity of the pth moment then gives the full real arbitrary-majorant property.
