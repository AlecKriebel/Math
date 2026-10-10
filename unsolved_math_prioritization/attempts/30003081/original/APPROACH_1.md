# Approach 1: product and normal-crossing local models

Status: proved conditional higher-dimensional exactness; broad target unresolved.

Let X be smooth over C, H smooth with local equation z=0, and A have local equation g(x_1,...,x_{n-1}) independent of z. Then
D_X(A)=D_x(g) extended to O_X plus O_X partial_z,
and D_X(A+H)=D_x(g) extended to O_X plus O_X z partial_z.
Restriction sends the first summand onto D_H(A|H) and kills the second; its kernel is z D_X(A). Consequently
0 -> D_X(A)(-H) -> D_X(A+H) -> i_*D_H(A|H) -> 0
is exact wherever this product presentation holds. These identifications follow coefficient by coefficient from divisibility of theta(g) by g and theta(z) by z; the restriction of a logarithmic x-derivation lifts with coefficients independent of z.

In particular the sequence is exact when A+H is a simple normal-crossing divisor: choose coordinates with A=x_1...x_r and H=z, and logarithmic bases x_i partial_i, the remaining partial_i, and z partial_z. This recovers the curve quotient T_H(-R)=O_H(-K_H-R) when dim X=2. In higher dimension the quotient is rank n-1, not the line bundle O_H(-K_H-R); the latter is at most its determinant when logarithmic bundles are locally free.

This proves no statement for arbitrary quasihomogeneous intersections lacking a product description. The method is elementary and classical; no novelty claim is made.
