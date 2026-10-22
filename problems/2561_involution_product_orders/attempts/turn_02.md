# Attempt 2: a complete characteristic-two symplectic transvection family

Date: 2026-10-03. Second substantive proof attempt, extending the previous ternary-reconstruction route by reconstructing affine geometry. This proves a family, not the universal Kourovka claim. No novelty is asserted.

## Statement

Let F=F_q have characteristic two, let V have even dimension 2n>=2, and let B be a nondegenerate alternating F-bilinear form. For v!=0 put

    T_v(x)=x+B(x,v)v.

Let D={T_v:v!=0} and color distinct vertices by the order of their product in Sp(V,B). Then every color-preserving permutation of D is induced by conjugation by a semilinear symplectic map. In fact preservation of color3 alone suffices. This answers 21.52 for the transvection class of every simple Sp(2n,q) in characteristic two (excluding nonsimple Sp(2,2), Sp(4,2)). In particular it covers the unique involution class of PSL(2,2^f), f>=2.

## Matrix-order calculation

Each T_v is a nonidentity involution. The map v -> T_v is injective: equality forces identical image lines of T_v-I; if w=cv, equality forces c^2=1, hence c=1. Sp(V,B) is transitive on nonzero vectors, and M T_v M^{-1}=T_{Mv}. These transvections therefore form one conjugacy class.

For v!=w with B(v,w)=0, the two transvections commute, and their product is a nonidentity involution. If d=B(v,w)!=0, U=<v,w> is nondegenerate and V=U orthogonal-direct-sum U-perp; the product acts trivially on U-perp. In the basis v,w of U, it has determinant1 and trace d^2. It therefore has order3 precisely when d=1: if d=1 its polynomial is X^2+X+1, and conversely a nonidentity order3 determinant1 matrix in characteristic2 has this characteristic polynomial. Thus

    |T_v T_w|=3 iff B(v,w)=1.

This equivalence also accounts for all pairs; v=w has product1 and B(v,v)=0.

## Reconstructing every affine hyperplane

Identify D with V minus {0}. A permutation f preserving color3 satisfies

    f(N(v))=N(f(v)),   N(v)={w:B(v,w)=1}.

The sets N(v), v!=0, are exactly all affine hyperplanes not containing0. Extend f by f(0)=0. Two distinct N(v),N(w) are disjoint exactly when v,w are proportional: nonproportional linear functionals take prescribed values (1,1), whereas w=cv with c!=1 makes those equations inconsistent. Hence f permutes the parallel classes of hyperplanes not containing0. The missing hyperplane through0 in each parallel class is the complement of their union in V, so f preserves these as well. Consequently f maps every affine hyperplane to an affine hyperplane, and preserves incidence and intersections. It maps all affine subspaces, including lines and planes, to affine subspaces of the same dimension.

For q=2 there is an even shorter conclusion: preservation of color3 is preservation of every value of B, since the only other value is0. For all x,y,z,

    B(f(x+y),f(z))=B(x+y,z)
                  =B(f(x)+f(y),f(z)).

Surjectivity and nondegeneracy imply f(x+y)=f(x)+f(y), so f is symplectic-linear. The following affine argument treats q>2.

## Elementary affine-geometric lemma

An origin-fixing bijection of F^m, m>=2, mapping every affine hyperplane to an affine hyperplane is semilinear (for q>2). Here are sufficient details rather than an unexplained reconstruction invocation.

Intersections reconstruct all affine subspaces and their dimensions. The images of a coordinate basis form a basis, as spans and dimensions are preserved. Compose with the inverse linear basis map so that g fixes0 and every basis vector. Within each affine plane, disjoint lines are parallel; therefore parallelism is preserved. Coordinate grids give

    g(sum_i a_i e_i)=sum_i phi_i(a_i)e_i,

where phi_i:F->F are bijections fixing0,1. The diagonal line in every coordinate plane is fixed, forcing all phi_i to be the same map phi. The lines y=x+b, which are parallel to the fixed diagonal, force phi(x+b)=phi(x)+phi(b). The lines y=ax through0 and the point (1,a) force phi(ax)=phi(a)phi(x). Hence phi is a field automorphism and f=M phi with M invertible and phi applied coordinatewise. (A symplectic basis may be chosen initially, so B has coefficients0,1.)

## Recovering the form and extending to the group

Write f=M phi as above. For u,v in V, preservation of B(u,v)=1 becomes preservation of the value1 for the two nonzero linear functionals, as v varies,

    v -> B(u,v),    v -> phi^{-1}(B(M phi(u),M phi(v))).

Their value1 hyperplanes coincide. Two nonzero linear functionals with the same value1 hyperplane are equal: their kernels are the translation spaces of that hyperplane, so one is a scalar multiple of the other, and evaluating at a point of value1 makes that scalar1. Therefore

    B(f(u),f(v))=phi(B(u,v)).

Thus f is semilinear symplectic. Its conjugation action on linear transformations normalizes Sp(V,B), and a direct calculation gives f T_v f^{-1}=T_{f(v)}. Consequently the original vertex permutation extends to a group automorphism. Conversely such maps preserve all product orders.

## Scope and obstruction to further extension

For n=1 in characteristic2, every nonidentity involution in SL2(q) has rank-one nilpotent part and is some T_v: the determinant-one unipotent calculation and existence of unique square roots in F suffice. Also Z(SL2(q))=1, so SL2(q)=PSL2(q). For higher n this proof covers only the transvection class. Other involutions have higher-rank nilpotent parts; their color3 neighborhoods are not the full affine hyperplanes of V. Odd-characteristic involutions also have a different parameter space. No step above controls those remaining cases.

The next attempt will test the broader simple-group cases with a reproducible exact colored-matrix automorphism procedure and then try to extract a general structural invariant from the verified small examples.
