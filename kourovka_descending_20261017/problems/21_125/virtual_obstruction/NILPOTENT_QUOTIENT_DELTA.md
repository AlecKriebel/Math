# Sharpness of the nilpotent-quotient filter

October24,2026. This is a consequence of the uniform finite action in `CENTRALIZER_COSET_FILTER.md`, not a RAAG embedding theorem.

Write \(d=m-1\ge1\), let \(N\) be the least power of2 at least \(d\), and identify the cyclic shift module with
\[
R=\mathbb F_2[x]/(x^N-1)=\mathbb F_2[\epsilon]/(\epsilon^N),\qquad \epsilon=x+1.
\]
The shifts of \(v=\epsilon^{N-d}\) span the ideal \(V'=\epsilon^{N-d}R\), of dimension \(d\). The image of the explicit uniform permutation representation is therefore exactly
\[
Q=V'\rtimes C_N,
\qquad |Q|=2^d N.
\]
Indeed the top fiber generator maps to \(v\), the stable letter to the cyclic shift, and these generate the full shift span and cyclic factor. The degree-\(2N\) permutation action is faithful on this image: a nontrivial shift changes a first coordinate, and any nonzero flip vector changes a second coordinate somewhere.

Commutators with the cyclic factor multiply the base module by \(\epsilon\); the base module is abelian. Consequently
\[
\gamma_k(Q)=\epsilon^{k-1}V'\quad(k\ge2),
\qquad \gamma_d(Q)\ne1,\quad \gamma_{d+1}(Q)=1
\]
for \(d\ge2\). If \(d=1\), the quotient is \(C_2\), of class1. Thus the nilpotency class is **exactly \(m-1\)** in every case. The image of \(a_2\) is the nonzero vector \(\epsilon^{N-1}\).

The main filter proved that a normal RAAG-embedding cover cannot have nilpotent quotient of class below \(m-1\). This explicit quotient reaches that threshold and passes the full centralizer-coset filter: the image of \(C_{G_m}(t)\) lies in the cyclic shift subgroup, while the image of \(a_2\) is a nontrivial global flip. In the regular action of \(Q\), no element of that coset has a fixed point, since none is the identity. Thus the **normal kernel** is also a finite cover passing this filter. This establishes sharpness for the obstruction criterion, with no implication that this kernel is special.

The nilpotent-quotient route is therefore blocked even when arbitrary finite covers are restricted to normal covers and finite2-group quotients. A stronger ingredient, beyond the known short Engel pairs and their centralizer cosets, is necessary for a negative solution.
