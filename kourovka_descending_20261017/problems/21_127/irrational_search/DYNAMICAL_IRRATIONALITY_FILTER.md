# Irrational rotation on a RAAG commutator does not certify irrational scl

2026-10-24 UTC. Elementary diagnostic construction; not a resolution of 21.127 and no originality claim.

Throughout, [x,y]=x y x^{-1} y^{-1}, and products of homeomorphisms use ordinary function composition (the rightmost factor acts first). Let A=F(a,b), the RAAG on two nonadjacent vertices. Set alpha=sqrt(2)/100, and define lifts of circle homeomorphisms

g(x)=x+(1/10)sin(2 pi x), h(x)=g(x)+alpha.

Both commute with x->x+1 and are strictly increasing because their derivatives are at least 1-pi/5>0. The fixed points of g are all integers (repelling) and half-integers (attracting). Since 0<alpha<1/10, h has exactly two fixed points in [0,1): u in (1/2,3/4) and v in (3/4,1). Its displacement is negative on (u,v) and positive on (v,u+1).

There exists an increasing homeomorphism f:R->R, commuting with integer translation, that conjugates g to h. To see this, send each integer n to v+n and each half-integer n+1/2 to u+n+1. On every intervening interval, g and h have the same displacement sign and no interior fixed points. Two increasing fixed-point-free interval homeomorphisms with the same sign are conjugate: choose any increasing map from one fundamental domain [x,g(x)] to [y,h(y)] with matching endpoints and extend equivariantly under g and h. The iterates converge to the interval endpoints, so the extension is a homeomorphism. Apply the same construction to inverses for intervals with negative displacement, and repeat by integer translation. The endpoint maps agree, so the interval conjugacies glue continuously.

Thus f g f^{-1}=h and [f,g]=h g^{-1}=R_alpha, the rigid translation x->x+alpha. The free group has a homomorphism rho sending a to f and b to g. The homogeneous translation-number quasimorphism phi=rot o rho satisfies

phi([a,b])=alpha, an exactly specified irrational number.

If d=D(phi) is the actual pulled-back homogeneous defect, then alpha<=d<=1: the upper bound comes from the universal rotation estimate, and the lower bound is the standard bound |phi([a,b])|<=D(phi). Bavard yields the more precise lower bound alpha/(2d), which need not be irrational. The universal defect estimate D(rot)<=1 also gives a legitimate Bavard lower bound scl_F([a,b])>=alpha/2. Nevertheless scl_F([a,b])=1/2, a standard exact free-group value. Therefore an irrational translation/rotation value on an explicit finite RAAG word is entirely compatible with rational scl. One must establish extremality with the actual defect, or an exact matching surface bound; no such extremality follows from irrationality of phi(g).

For completeness, the upper bound scl([a,b])<=1/2 has a direct covering proof. For every odd n, let a act on Z/n by i->i+1 and b by i->-i. Their permutation commutator is i->i+2, an n-cycle. This defines a connected degree-n cover of a once-punctured torus with a single boundary component mapping with degree n. Its Euler characteristic is -n, and genus is (n+1)/2. Dividing commutator length by n and letting odd n increase gives the upper bound. The lower bound is the classical free-group 1/2 gap (Duncan--Howie), or the usual extremal punctured-torus quasimorphism. The two-generator word is nontrivial and lies in [F,F].

External source dependencies: the universal translation-number defect bound and Bavard duality (Zhuang arXiv:0710.0026v1, Section 2 and appendix, or Calegari's scl monograph); the free-group sharp gap for the exact value. The construction of f is existential but completely specified by the fundamental-domain extension and requires no approximate computation.

This is a route barrier only. It does not rule out an extremal irrational rotation quasimorphism in a different RAAG.
