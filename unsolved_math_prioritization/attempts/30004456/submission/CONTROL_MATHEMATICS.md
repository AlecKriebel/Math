# Mathematics of the bounded controls

These are elementary consistency checks; none searches for, or proves, the general optimal splitting.

For G=F_n×Z write a character as φ(w,z)=a(w)+qz, where a(x_i)=a_i and q≠0. Projection to F_n identifies ker φ with

L={w∈F_n : a(w)≡0 mod q}.

Indeed, z=−a(w)/q is the unique possible lift. If d=gcd(a_1,…,a_n,q), L has index m=|q|/d. The connected Schreier graph on the reachable residues of Z/|q| has m vertices and nm positively oriented labelled edges. Hence L is free of rank 1+m(n−1), and

−χ⁽²⁾(ker φ)=m(n−1)

when n≥1. This agrees with the obvious fibred HNN splitting whose base is ker φ. It also shows explicitly why a nonprimitive character must be normalized: using |q|(n−1) would overcount by d. Scaling all character values by a nonzero integer preserves m and the kernel rank. The controls actually build the connected Schreier graph and a spanning tree rather than only compare two copies of the rank formula.

For q=0 and the standard primitive character a_1=1, a_i=0 (i>1), there is an explicit splitting

F_n×Z = (F_{n−1}×Z) *_{Z}

with stable letter x_1 and both edge maps into the central Z-factor. When n=1 the base and edge are both Z. The base Euler characteristic is zero. For n≥2 the kernel is an infinite-rank free group times Z; all its L²-Betti numbers vanish because of the infinite amenable direct factor. The script only checks the finite product-cell Euler arithmetic for this family; it does not compute L²-homology of an infinite complex.

For n=0, G=Z and nonzero φ has trivial kernel. The Euler target is −1, while b₁⁽²⁾ of the trivial group is zero. This is a negative control against dropping b₀.

The script also checks the finite arithmetic implications used in the squeeze and graph-of-spaces Euler translation, and rejects normalization of the zero character. Such checks verify sign/convention arithmetic; they are not evidence for the truth of the referenced infinite-dimensional theorems.

Bounds are deliberately fixed: n=1,…,4; |q|=1,…,6; every residue vector 0≤a_i<|q|; both signs of q; scaling factors 2,3,5; and n=1,…,8 for the q=0 cell arithmetic. Python's arbitrary-precision integer arithmetic is used throughout. No floating-point approximation, randomized sampling, network requests, or external packages are involved.
