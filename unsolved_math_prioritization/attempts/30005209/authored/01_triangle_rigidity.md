# Approach 1: rigidity of a triangular normal fan

## Objective

Test the proposed side-transitive symmetry class against the smallest possible number of facets. In dimension two, three support numbers minus two translations minus one area constraint leave no shape parameter.

## Setup and known reduction

Let (P\subset\mathbb R^2\) be a nondegenerate, unit-area triangle containing 0, and let \(\psi=h_P\) be its support function. Let its distinct outer unit normals be \(\nu_1,\nu_2,\nu_3\), and write
\[
P=\{x:x\cdot\nu_i<h_i,\ i=1,2,3\}.
\]
For (0<\alpha<2\), minimizers of (P_\psi+\gamma V_\alpha\) exist when γ is small. Their nonlocal term is uniformly Lipschitz with respect to symmetric difference, so they are (O(\gamma)\)-quasiminimizers of the crystalline perimeter. The planar Figalli–Maggi rigidity theorem then says that they are convex polygons whose sides have normals among those of (P\). They converge, modulo translations, to (P\). These are precisely the first steps in the proof of Bonacini–Cristoferi–Topaloglu (2021), Theorem 2.5; those steps do not use the side-transitive symmetry hypothesis. The symmetry is used later for the energy comparison.

With only these three permitted normals, a bounded convex set with nonempty interior must have all three supporting sides. Thus any such minimizer is a triangle with the same oriented normals.

## Exact geometry

Let (N\) be the (3\times2\) matrix with rows \(\nu_i^T\), and let \(\ell=(\ell_1,\ell_2,\ell_3)\) be the side-length vector. The divergence theorem gives
\[
N^T\ell=0,\qquad \ell\cdot h=2|P|=2.
\]
The normals span \(\mathbb R^2\), so \(N\) has rank 2. Consequently the three columns of \([N\ h]\) are linearly independent: if (Na+ch=0\), multiplication by \(\ell^T\) gives (2c=0\), hence (a=0\).

Every support vector \(h'\in\mathbb R^3\) therefore has the unique form
\[
h'=Na+ch.
\]
Whenever \(h'\) defines a nondegenerate bounded triangle with these oriented normals, (c>0\), and the triangle is exactly (a+cP\). Its area is (c^2\). Under the unit-area constraint, (c=1\).

It follows that every small-γ global minimizer is a translate of (P\). Since a minimizer exists, (P\) itself is a global minimizer and is unique modulo translations.

## Independent first-variation check

Write
\[
B_i=\int_{L_i}v_P(x)\,d\mathcal H^1(x),\qquad
v_P(x)=\int_P|x-y|^{-\alpha}\,dy.
\]
Translation invariance of (V_\alpha\) implies
\[
\sum_{i=1}^3 B_i\nu_i=0.
\]
The nullspace of \(N^T\) is one dimensional and contains \(\ell\); hence (B_i=A\ell_i\) for some (A\). Thus every triangle has the same average potential on each of its sides, without requiring any reflection symmetry.

The boundary first-variation formula used here is justified for every \(\alpha<2\) in Approach 2; it is also the sliding formula in the cited primary papers. No nonintegrable boundary-to-boundary Hessian is used.

## Attribution and scope

The automatic sliding stationarity is explicitly stated in Bonacini–Cristoferi–Topaloglu, *Riesz-type inequalities and overdetermined problems for triangles and quadrilaterals* (2022), Remark 4.1. Their equilateral-triangle rigidity theorem assumes **tilting** stationarity, a stronger condition. It therefore does not contradict this result.

The argument already disproves an interpretation of the classification problem asserting that the 2021 side-transitive class is exhaustive. For example, an area-one scalene triangle is admissible under the actual source assumptions. It does not classify polygons with four or more sides. If one imposes the additional condition \(\psi(-\nu)=\psi(\nu)\), triangles are excluded; that additional convention is not part of the source definition.
