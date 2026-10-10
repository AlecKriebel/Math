# Reconstruction from balanced cohomology modules

This approach tries to extend the k=2 classification by determining every triple product from its degree and the pairwise cohomology modules. Even granting simultaneous compatible cohomology coordinates, those linear data leave a higher-rank ambiguity.

For a noncrossing perfect matching A of 2k points, every cup joins opposite parities. With the standard alternating change of signs in tautological degree-2 classes, the ring model for a pair is

R_AB=C[z1,...,z_(2k)]/(zi², zi−zj for edges of A or B).

It is a tensor product of c(A,B) copies of C[t]/(t²). Here c(A,B) is the number of components in the union of the two matchings. Put d(A,B)=k−c(A,B); this is the cohomological shift for the Ext-space model.

Suppose candidate composition is balanced over the common polynomial ring R=C[z1,...,z_(2k)], with all pair generators corresponding to 1. It is then determined by the image η of 1⊗1 in R_AC. The relations of R_AB and R_BC imply

(zi−zj)η=0 for each edge ij of B,

since the A- and C-relations already hold in R_AC. Homogeneity forces η to have ordinary cohomology degree

d(A,B)+d(B,C)−d(A,C)=k−c(A,B)−c(B,C)+c(A,C).

Variables zi have degree 2. This condition is only a necessary linear constraint in this simultaneous cohomological model; we do not assume the actual Yoneda algebra already admits that model.

## Dimension of the space of allowed images

Write r=c(A,C) and s for the number of connected components in the union A∪B∪C. The B edges partition the r variables of R_AC into s nonempty groups. For a group of r_j variables, the common annihilator of their differences is spanned by

E_(r_j−1)=the sum of all square-free monomials omitting exactly one variable,
E_(r_j)=the product of all variables.

Both are annihilated by each difference. They span the full annihilator: the quotient by the differences is C[t]/(t²), of dimension two, and the perfect top-coefficient pairing in the square-zero-variable ring identifies the annihilator with the dual of that quotient. Different groups tensor independently.

Let m=(k−c(A,B)−c(B,C)+r)/2 be the required polynomial degree. The minimal annihilator degree is r−s. Therefore the dimension of the allowed degree-m subspace is

binomial(s, m−r+s),

with value zero outside 0≤m−r+s≤s. This is proved for the square-zero-variable model; it is not a classification of global associative Ext algebras.

The exact checker independently forms all difference-multiplication matrices and computes their rational ranks for every ordered triple of matchings for k≤4. It finds dimension one for all triples at k=1,2,3. At k=4, 2696 triples have dimension one and 48 have dimension two.

## An explicit two-dimensional ambiguity

Take k=4 and

A=(12)(36)(45)(78),
B=(14)(23)(56)(78),
C=(16)(25)(34)(78).

Each pair union has two circles: one uses points 1 through 6, the other is the common cup on 7 and 8. The union of all three matchings has the same two components. Thus every pair ring is C[u,v]/(u²,v²), with u on the first six points and v on the final cup. Each pair has d=2, so the image of the two lowest-degree generators must lie in ordinary H2(R_AC). The balance relations permit every

η=αu+βv.

In the usual arc TQFT the six-point part contains a genus-one contribution, producing a nonzero multiple of u, while the untouched common cup contributes the unit. A tensor-factor compatibility statement singles out that direction, but degree and balance alone do not.

This is not a counterexample to the conjecture, nor evidence for a two-parameter family of associative algebras. The missing constraints could be imposed by global associativity, functorial cup factorization, or a coherent system of identifications. The computation pinpoints what a reconstruction proof must add beyond separate pairwise module results.
