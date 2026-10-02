# Separate read-only adversary: explicit mapping-torus diagnostic

Verifier: `/root/pr32_hprinciple_formal_geometry_adversary/mapping_torus_control_verifier`. Assigned only the diagnostic in AUDIT §8; no full-target proof search, original/sibling-family review, file modification, Git/GitHub action, or outreach.

**PASS.** No counterexample or missing premise in the explicit mapping-torus diagnostic. Verification of this assigned control is complete. The all-index immersion realization depends on AUDIT §7 and was outside this subordinate verifier's scope.

The Klein-bottle deck action is free and properly discontinuous. Every element has form a^m b^n; a fixed point forces m=0 and then n=0. A compact rectangular fundamental region establishes compactness. Direct composition gives a b a^-1=b^-1, h a h^-1=a^-1 b, h b h^-1=b, and h²=b^-1. In addition h^-1(X,Y)=(-X,Y+1/2)=b h(X,Y), h^-1 a h=a^-1 b^-1, and h^-1 b h=b. Thus both h and its inverse normalize the deck group, proving f is a genuine smooth diffeomorphism of K.

For the convention (p,1)~(f(p),0), take T(X,Y,z)=(h(X,Y),z-1). Its conjugation action is the stated action of h. Normal forms g T^k are distinct because their vertical translations differ. Consequently the fundamental-group presentation has precisely the Klein relation and the two conjugation relations. T²(X,Y,z)=(b^-1(X,Y),z-2), so h²=b^-1 adds no relation T²=b^-1.

Abelianization gives 2b=0 and 2a=b, with no relation on T. Therefore H_1(M_f;Z)=Z<T> direct sum Z/4<a>. Exact independent affine-matrix and Smith-form checks passed. Choosing the positive vertical deck T^-1 changes 2a=b to 2a=-b, producing the same abelianization.

The mapping torus is compact, connected, smooth and boundaryless. Its fiber has a trivial normal line, so w1(TM_f) restricts to the nonzero w1(TK); the source is nonorientable. For the explicit deck generators, the total Jacobian signs give w1(a)=1, w1(b)=0, w1(T)=1. Replacing the free homology generator T by T+a changes its orientation value to zero and changes its nonabelian conjugation presentation.

Compactness supplies finite generation. With chi(M_f)=0, b1=1 and b3=0, we obtain b2=0. Hence Hom(H_2,Z)=0. Integral universal coefficients give H^2(M_f;Z)=Ext(H_1,Z)=Z/4. This is cohomology H^2, not homology H_2.

Every integral character kills torsion a, whereas w1(a)=1. Thus w1 has no integral lift. Exactness for 0→Z --2→ Z→Z/2→0 implies beta(w1) is nonzero and killed by two. In Z/4 it is the unique nonzero order-two element, 2. It is divisible by two and has zero coefficient reduction.

Independently, rho2 beta(u)=u² for a degree-one mod-two cocycle. Choose its integer edge values in {0,1}; its half-coboundary on an ordered triangle is one precisely when both consecutive edge values are one, exactly the cup-square formula. Thus w1²=0. The character a↦1, b↦2, T↦1 also verifies an explicit mod-four lift.

Finally -4x-2y=2 in Z/4 has exactly eight solutions: arbitrary x and odd y. The subordinate verifier makes no independent claim about their immersion representatives beyond the assigned geometric diagnostic.
