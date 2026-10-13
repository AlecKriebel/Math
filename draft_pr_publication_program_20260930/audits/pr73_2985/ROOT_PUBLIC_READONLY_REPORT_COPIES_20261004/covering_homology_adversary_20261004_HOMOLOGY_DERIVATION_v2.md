# Independent covering-homology derivation (format-corrected v2)

Set $Y=T^4$ and $D=S\sqcup S'$. Choose disjoint closed oriented normal disk bundles $V=V_1\sqcup V_2$ and let $M=Y\setminus\operatorname{int}V$. Symplectic orientations on the ambient manifold and surfaces orient the normal bundles. Their triviality is not assumed.

In each punctured normal disk of radius $\epsilon$, replace $0<r\leq\epsilon$ by $r_t=(1-t)r+t\epsilon$, fixing angular and base coordinates. Extend by the identity outside the bundles. This is a strong deformation retraction $Y\setminus D\to M$; continuity across the removed zero section is unnecessary. A path can be perturbed relative its endpoints to be transverse to $D$. The intersection dimension $1+2-4$ is negative, so the path misses $D$. Hence $Y\setminus D$ and $M$ are connected.

## Pair cohomology and ordinary third homology

Poincare-Lefschetz duality and collared excision give

$$
H_3(M;\mathbb Z)
\cong H^1(M,\partial M;\mathbb Z)
\cong H^1(Y,V;\mathbb Z).
$$

For excision, remove a smaller disk bundle from the interior of $V$; the remaining pair retracts to $(M,\partial M)$. These groups also identify with $H_c^1(Y\setminus D;\mathbb Z)$. Thus compact support is on the cohomology side, while the homology used for the obstruction is ordinary singular homology.

The pair sequence contains

$$
\mathbb Z=H^0(Y)
\xrightarrow{1\mapsto(1,1)}H^0(V)=\mathbb Z^2
\xrightarrow{\delta}H^1(Y,V)
\longrightarrow H^1(Y)\longrightarrow H^1(V).
$$

It injects $\mathbb Z^2/\langle(1,1)\rangle\cong\mathbb Z$ into the relative degree-one group. Geometrically either oriented normal circle bundle represents the resulting ordinary third-homology class; their sum bounds the exterior.

This verifies the candidate's alternative Thom map $H_4(Y)\to H_4(Y,M)\cong H_2(D)$. The ambient fundamental class restricts to each surface fundamental class with coefficient one. Self-intersection and the Euler class of the oriented normal bundle do not enter that local restriction coefficient. Reversing a basis orientation changes the diagonal to $(1,-1)$ without changing its primitive image or cokernel.

The injected copy of $\mathbb Z$ is a direct summand here: its quotient in the pair sequence is a subgroup of the free abelian group $H^1(Y)$ and is therefore free abelian, so the short exact sequence splits. The argument does not assume that an arbitrary copy of $\mathbb Z$ in an abelian group splits.

## Exact upstairs group and vanishing downstairs

The restriction $i^*:H^1(Y;\mathbb Z)\to H^1(S;\mathbb Z)$ is injective. If $i^*a=0$, the defining Poincare-duality identity gives, for every $b\in H^1(Y;\mathbb Z)$,

$$
\langle a\smile b\smile[\alpha],[Y]\rangle
=\langle i^*a\smile i^*b,[S]\rangle=0.
$$

This bilinear pairing is nondegenerate over $\mathbb Q$. Equivalently, exterior multiplication by $\alpha$ from degree one to degree three is invertible over $\mathbb Q$. In coordinate bases its matrix is

$$
L_\alpha=
\begin{pmatrix}
0&1&1&0\\
1&0&0&1\\
1&0&0&-1\\
0&1&-1&0
\end{pmatrix},
\qquad \det L_\alpha=4.
$$

The retained independent exact-algebra script checks this without importing any original checker. Consequently $a=0$ rationally and integrally, since $H^1(T^4;\mathbb Z)$ is torsion-free. The kernel of $H^1(Y)\to H^1(V)$ vanishes, so

$$
H_3\!\left(T^4\setminus(S\sqcup S');\mathbb Z\right)\cong\mathbb Z.
$$

The deck involution exchanges the two components of $V$. On the quotient by the diagonal it sends $[(a,b)]$ to $[(b,a)]=-[(a,b)]$. It preserves ambient orientation, so duality identifies this with action $-1$ on upstairs $H_3$.

Now set $N=X\setminus\Sigma$. If $c\in H^1(X;\mathbb Z)$ restricts to zero on $\Sigma$, then $p^*c$ restricts to zero on $S$ and hence is zero. Transfer gives $2c=0$, and degree-one integral cohomology is torsion-free, so $c=0$. Thus $H^1(X)\to H^1(\Sigma)$ is injective. Since $X$ and $\Sigma$ are connected, their degree-zero cohomology map is an isomorphism. The pair sequence gives $H^1(X,\Sigma;\mathbb Z)=0$. The corresponding exterior duality implies

$$
H_3(N;\mathbb Z)=0.
$$

A proof relying on nonzero ordinary third homology downstairs would fail. The candidate instead uses the cover. The anti-invariant generator explains why rational transfer does not supply a downstairs generator.

## Finite-cover lifting and the Weinstein CW bound

For a conventional open Weinstein structure $(N,d\lambda,Z,\phi)$, pull back the form and primitive, lift $Z$, pull back the metric, and use $\phi\circ p$. A finite covering is proper, preserving compact sublevels of the proper bounded-below function. Its local diffeomorphism property preserves critical indices and nondegeneracy. Gradient inequalities pull back unchanged. Complete flow trajectories lift for all time, preserving completeness whenever this is required.

A Liouville flow expands the symplectic form by $e^t$. Along a stable manifold of a nondegenerate critical point, tangent vectors contract in forward time. The restriction of the symplectic form to that stable manifold therefore vanishes. Its dimension is the Morse index, so the index is at most half the ambient dimension, here two.

Choose increasing regular values of an exhausting Morse function. Compact intervals contain finitely many critical points. The Morse normal form gives a handle at each crossing, with core dimension equal to the index. Retraction to the cores gives CW attachments. The exhaustion produces a possibly infinite CW homotopy model of dimension at most two, without any finite-type hypothesis. Generalized Morse structures in the standard definition admit Morse perturbations with the same necessary bound.

The target literature also uses compact Weinstein domains and their interiors or Liouville compactifications. A compact Weinstein domain has the same index bound, and its interior and completion have its homotopy type. A finite cover of such a domain is a compact Weinstein domain with lifted data. This proves the obstruction in that convention too, without invoking completeness for the inherited finite-volume form. K3 section 4.9, printed p.263, was read in full after sealing for this exact convention; the complete-flow convention is separately checked in Cieliebak-Eliashberg.

For the stronger purely topological claim, suppose $N\simeq K$ for a two-dimensional CW complex $K$. Pull the double cover back along a homotopy equivalence $K\to N$. Its cells lift cells of $K$, so the pulled-back cover has a CW structure of dimension at most two. Lifting the equivalence and homotopies makes it homotopy equivalent to the original cover. Its ordinary third homology must vanish, contradicting the established $\mathbb Z$.

Thus $N$ has no two-dimensional CW homotopy model and admits no Weinstein structure, for any form, under either convention above.

Primary background read in full at the relevant locations: [Hatcher, Algebraic Topology, Section 3.3](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf), printed pp.242-243 and 253-255, for compact-support cohomology and duality; [Cieliebak-Eliashberg, Flexible Weinstein manifolds, pp.1-4](https://library.slmath.org/books/Book62/files/eliashberg.pdf), for definitions, Morse perturbation and the index bound; and [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp.263 and 281, for the target conventions and full question with remarks. The specific deductions above are independent applications to the authenticated candidate.
