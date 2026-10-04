# A connected symplectic surface with a non-Weinstein complement

**Candidate counterexample; independent adversarial review pending.**
This addresses Kirby Problem 4.109, record 2985. The construction uses
Auroux's disconnected hyperplane-section example, as presented by Giroux,
and an explicit free quotient that makes the surface connected. Historical
novelty has not been established.

## 1. Statement and scope

There exist a closed connected symplectic four-manifold ((X,\Omega)) and a
closed connected embedded symplectic surface \(\Sigma\subset X\) such that

\[
\operatorname{PD}_X[\Sigma]=[\Omega],
\tag{1}
\]

but \(X\setminus\Sigma\) does not have the homotopy type of a two-dimensional
CW complex. In particular its given symplectic form cannot support a
Weinstein structure. In fact, its underlying manifold admits no Weinstein
structure for any symplectic form.

Here \([\Omega]\) is an integral real cohomology class; if an integral lift is
required, take \(\operatorname{PD}_X[\Sigma]\). Thus this gives the degree
\(k=1\) instance of the class condition in the original question. The surface
has genus three and self-intersection four.

The original question, including its two remarks, is on printed p.281 of
[*K3: A New Problem List in Low-Dimensional Topology*](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
The result concerns the prescribed surface in that question. It does not
assert that this symplectic manifold has no other surface in this class with
Weinstein complement. It does not settle the separate effective-degree
question in the remarks or the special case of \(\mathbb{CP}^2\).

## 2. Four affine tori and a free involution

Work in \(T^4=\mathbb R^4/\mathbb Z^4\), with coordinates \(x_1,\ldots,x_4\)
modulo one and symplectic form

\[
\omega_0=dx_1\wedge dx_2+dx_3\wedge dx_4.
\]

Define the affine tori

\[
A=\{x_1=0,\ x_2-x_3=0\},\qquad
B=\{x_2+x_3=\tfrac14,\ x_4=\tfrac14\}.
\tag{2}
\]

All equations for the tori are equations modulo one. Parametrizations are

\[
(u,v)\longmapsto(0,u,u,v),\qquad
(u,v)\longmapsto(u,v,\tfrac14-v,\tfrac14).
\]

For both parametrizations the pullback of \(\omega_0\) is \(du\wedge dv\),
so both tori are symplectic with these orientations. They meet at exactly
the two points

\[
(0,\tfrac18,\tfrac18,\tfrac14),\qquad
(0,\tfrac58,\tfrac58,\tfrac14).
\tag{3}
\]

These intersections are transverse and positive. For example, the Jacobian
of the ordered normal equations
\((x_1,x_2-x_3,x_2+x_3,x_4)\) has determinant \(2>0\).

Consider the affine involution

\[
\tau(x_1,x_2,x_3,x_4)
  =(x_1+\tfrac12,x_2,-x_3,-x_4).
\tag{4}
\]

Its square is the identity on \(T^4\), it has no fixed point because of
the first coordinate, and \(\tau^*\omega_0=\omega_0\). Its images are

\[
A'=\tau A=\{x_1=\tfrac12,\ x_2+x_3=0\},\qquad
B'=\tau B=\{x_2-x_3=\tfrac14,\ x_4=\tfrac34\}.
\tag{5}
\]

The two nodal unions \(A\cup B\) and \(A'\cup B'\) are disjoint:

- \(A\cap A'=\varnothing\) because their \(x_1\) coordinates differ;
- \(B\cap B'=\varnothing\) because their \(x_4\) coordinates differ;
- \(A\cap B'=\varnothing\) because \(x_2-x_3\) would be both zero and \(1/4\);
- \(B\cap A'=\varnothing\) because \(x_2+x_3\) would be both \(1/4\) and zero.

In particular, one can choose an open neighborhood \(U\) of \(A\cup B\)
such that \(U\cap\tau U=\varnothing\).

## 3. Symplectic smoothing and its homology class

Set

\[
\begin{aligned}
\alpha&=dx_1\wedge(dx_2-dx_3)+(dx_2+dx_3)\wedge dx_4,\\
\beta&=dx_1\wedge(dx_2+dx_3)+(dx_3-dx_2)\wedge dx_4.
\end{aligned}
\tag{6}
\]

With the symplectic orientations specified above, the Poincaré duals of
\(A\) and \(B\) are the two respective terms of \(\alpha\). This follows
also by regarding each torus as an oriented regular fiber of its indicated
map to \(T^2\). Thus

\[
\operatorname{PD}_{T^4}([A]+[B])=[\alpha],\qquad
\tau^*\alpha=\beta,\qquad \alpha+\beta=2\omega_0.
\tag{7}
\]

Smooth the two positive double points of \(A\cup B\), within \(U\), to
obtain a connected embedded symplectic surface \(S\). This is the same
local symplectic smoothing used in
[Giroux, Proposition 9 (Auroux)](https://arxiv.org/abs/1803.05929).
For completeness, the required smoothing can be checked directly here.

Near either double point use real affine coordinates

\[
s_1=x_1,quad s_2=x_2-x_3,quad
s_3=x_2+x_3-\tfrac14,quad s_4=x_4-\tfrac14,
\]

choosing the appropriate local lifts so that all four vanish at that point.
Then \(A=\{s_1=s_2=0\}\), \(B=\{s_3=s_4=0\}\), and

\[
\alpha=ds_1\wedge ds_2+ds_3\wedge ds_4,\qquad
\beta=ds_1\wedge ds_3-ds_2\wedge ds_4.
\tag{8}
\]

Put \(z=s_1+i s_2\) and \(w=s_3+i s_4\). The form \(\alpha\) is the
standard positive Kähler form, while \(\beta=\operatorname{Re}(dz\wedge dw)\).
On the complex smoothing \(zw=\varepsilon\), with \(\varepsilon\ne0\),
the form \(\beta\) vanishes and \(\alpha\) is positive. Therefore
\(\omega_0=(\alpha+\beta)/2\) restricts positively to the smoothing.

One can make this modification agree exactly with the original axes outside
a fixed small neighborhood. Use \(w=\varepsilon\chi(|z|)/z\) on the
outer \(z\)-annulus and \(z=\varepsilon\chi(|w|)/w\) on the outer
\(w\)-annulus, where \(\chi\) equals one near the inner edge and zero
near the outer edge. Keep \(zw=\varepsilon\) in the intervening region.
On each fixed outer annulus the graph and its first derivatives approach
the corresponding axis as \(\varepsilon\to0\), so positivity of
\(\omega_0\) persists there. For sufficiently small \(\varepsilon\),
the two transition regions are disjoint, the central piece is an embedded
annulus, and the resulting surface is smooth and equals the axes near the
outer boundary. This gives the required compactly supported local
smoothing. It is homologous to the original nodal union, since the
replacement agrees at the boundary of a ball and the ball has no second
homology.

Performing this at both points gives

\[
\operatorname{PD}_{T^4}[S]=[\alpha].
\tag{9}
\]

The smoothing connects the two tori. Removing the four disks at the two
nodes and inserting two annuli gives Euler characteristic \(-4\), hence
genus three. Since \(S\subset U\), the surface \(S'=\tau S\) is disjoint
from \(S\), is symplectic, and has Poincaré dual \([\beta]\).
No independent smoothing choice on \(S'\) is needed: it is defined as
the image under \(\tau\).

The cohomological checks are

\[
\alpha^2=\beta^2=4\,dx_1\wedge dx_2\wedge dx_3\wedge dx_4,
\quad \alpha\wedge\beta=0,
\quad \operatorname{PD}_{T^4}[S\sqcup S']=2[\omega_0].
\tag{10}
\]

## 4. The connected quotient surface

Let

\[
X=T^4/\langle\tau\rangle,qquad p:T^4\longrightarrow X.
\]

The free symplectic involution makes \(X\) a closed connected smooth
symplectic four-manifold. Let \(\bar\omega\) be the descended form, so
\(p^*\bar\omega=\omega_0\), and set \(\Omega=2\bar\omega\).

Define \(\Sigma=p(S)\). Because \(S\cap\tau S=\varnothing\), the map
\(p|_S:S\to\Sigma\) is an injective immersion and hence a diffeomorphism
onto an embedded compact surface. Thus \(\Sigma\) is connected, smooth,
symplectic, and of genus three. Its full inverse image is \(S\sqcup S'\).
Naturality of Poincaré duality under the covering gives

\[
p^*\operatorname{PD}_X[\Sigma]
=\operatorname{PD}_{T^4}[S\sqcup S']
=2[\omega_0]=p^*[\Omega].
\tag{11}
\]

Pullback by a finite covering is injective on real cohomology: the transfer
composed with pullback is multiplication by its degree, here two.
Equation (11) therefore proves (1). In particular \(\Omega\) has integral
periods, since its real cohomology class has the integral lift
\(\operatorname{PD}_X[\Sigma]\). The construction does not infer
injectivity on integral cohomology or discard possible torsion.

Also \(\int_X\Omega^2=\tfrac12\int_{T^4}(2\omega_0)^2=4\),
so \([\Sigma]^2=4\), as asserted.

## 5. A covering-space obstruction to every Weinstein structure

Write \(N=X\setminus\Sigma\). Its connected double cover is

\[
\widetilde N=T^4\setminus(S\sqcup S').
\tag{12}
\]

The complement is connected: paths in a connected four-manifold can be
perturbed off a closed embedded codimension-two submanifold. Choose
disjoint tubular neighborhoods of \(S\) and \(S'\), and let \(M\) be
the compact exterior. Then \(\widetilde N\) deformation retracts onto
\(M\).

The long exact sequence of \((T^4,M)\), excision, and the oriented Thom
isomorphism give the segment

\[
H_4(T^4;\mathbb Z)\longrightarrow
H_4(T^4,M;\mathbb Z)
\cong H_2(S\sqcup S';\mathbb Z)
\longrightarrow H_3(M;\mathbb Z).
\tag{13}
\]

The first map is \(\mathbb Z\to\mathbb Z^2\), \(1\mapsto(1,1)\):
the fundamental class restricts to the oriented fundamental class of each
surface under the Thom identification. Exactness consequently gives an
injection

\[
\mathbb Z^2/\langle(1,1)\rangle\cong\mathbb Z
\lhook\joinrel\longrightarrow H_3(M;\mathbb Z)
\cong H_3(\widetilde N;\mathbb Z).
\tag{14}
\]

In particular the double cover has nonzero ordinary third homology.

A Weinstein four-manifold has the homotopy type of a CW complex of
dimension at most two: its exhausting Weinstein Morse function has only
critical points of index at most two. Every covering space of such a
manifold also has the homotopy type of a two-dimensional CW complex,
by lifting a CW homotopy model. Its third homology must vanish.
Equivalently, a Weinstein structure would lift to the finite cover,
where the same Morse-index obstruction applies.

Equation (14) contradicts this necessary condition. Hence \(N\) is not
homotopy equivalent to any two-dimensional CW complex and admits no
Weinstein structure. This proves the stated counterexample. \(\square\)

## 6. Attribution and verification boundary

The two orthogonal integral classes and the smoothing of two pairs of
affine tori are the Auroux construction presented in Giroux's Proposition 9.
Disconnected counterexamples themselves are therefore prior work. The
explicit offsets above verify every required disjointness condition
directly. The step examined here is the free quotient exchanging the two
components, together with the obstruction in its connected double cover.

The homological obstruction is independent of choices of primitive,
Liouville compactification, completion, or symplectic deformation. It also
does not confuse disconnectedness of the *lifted* surface with
disconnectedness of the quotient surface: the latter is connected.

Exact algebraic checks can verify the affine equations, orientations,
exterior products and covering-class calculations. They supplement the
written smoothing and homology arguments; they do not replace them.
Independent adversarial review is required before this candidate is
presented as a reviewed result. Historical priority remains unconfirmed.
