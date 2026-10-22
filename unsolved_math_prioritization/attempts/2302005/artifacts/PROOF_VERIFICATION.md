# Verification of Gol’dberg's known affirmative answer

This note checks the implication for Rényi's concrete question and the mechanism of the original published construction. The construction and its resolution credit are Gol’dberg's. Standard complex-analysis theorems, including the classical Keldysh approximation theorem explicitly invoked in that paper, are used as external theorems. This is not a formal proof-assistant certificate or a claim to reprove those foundational results.

## 1. Exact question and definition equivalence

Let \(G\) be nonconstant and entire. Write
\[
 E(G)=\{a:\ \forall\alpha<\beta<\alpha+2\pi,\ \forall R>0,\
 \exists z\ (|z|>R,\ \alpha<\arg z<\beta,\ G(z)=a)\},
\]
where angular intervals are interpreted on the circle. This is equivalent to the catalogue's infinitely-many-distinct-preimages formulation because the zeros of \(G-a\) are discrete and every compact disc has only finitely many.

Gol’dberg defines \(D(G)\) by requiring the arguments of nonzero solutions of \(G(z)=a\) to be dense on the angular circle. Then \(D(G)=E(G)\):

- Membership in \(E(G)\) immediately implies angular density.
- If a nonempty angular interval contained only finitely many a-points, remove their finitely many arguments and choose a smaller nonempty open subinterval. Angular density would require another a-point there, a contradiction. Thus every angle has infinitely many a-points. Discreteness then makes their moduli unbounded.

A solution at zero has no argument and is omitted from this angular set. Adding or removing that one point cannot change either property. Counting multiplicities cannot turn finitely many zeros of a nonzero entire function into infinitely many. No uniform radius over all sectors or all values is required.

## 2. Published theorem and immediate consequence

The theorem on original p.191 is:

> For every bounded closed at-most-countable set \(A\subset\mathbb C\), an entire function \(G\) exists with \(D(G)=A\).

Take \(A=\{0,1\}\). It meets all hypotheses, and the preceding equivalence gives \(E(G)=\{0,1\}\). Such a function cannot be constant and cannot be a polynomial: it has infinitely many zeros and infinitely many 1-points. This proves the claimed transcendental-entire existence statement.

For arbitrary distinct \(a,b\), either apply the theorem directly to \(\{a,b\}\), or put \(F=a+(b-a)G\). Solving \(F(z)=w\) is equivalent to solving \(G(z)=(w-a)/(b-a)\), so \(E(F)=\{a,b\}\). This change imposes no extra normalization or growth hypothesis.

## 3. Two inclusions in the original construction

The following is a proof check specialized in its application to finite \(A\); the published theorem permits compact countable \(A\).

### 3.1 Target-plane domains

The construction chooses bounded simply connected domains \(D_n\) containing \(A\), with
\[
 \bigcap_{n\ge1}D_n=A.
\]
These domains are not asserted to be nested. For a finite set, surround its points by pairwise disjoint arbitrarily small polygonal neighborhoods. A simple arc traversing the neighborhoods divides a large disc into two sides. Adjoin the neighborhood interiors to each side. The resulting two simply connected domains intersect just in the small neighborhoods. Repeating at successively smaller scales gives the displayed intersection. This is the finite-set case of the construction on p.192.

Let \(P_n:\mathbb D\to D_n\) be a conformal map with \(P_n(0)\notin A\). Such a base point exists since \(D_n\) is open and \(A\) is finite (or countable). Its inverse image \(T_n=P_n^{-1}(A)\) is compact and avoids both zero and the unit circle. Hence a number \(d_n>0\) can be chosen so that
\[
 d_n\le |t|\le1-d_n\quad(t\in T_n),\qquad d_n<1/2.
\]
The exclusion \(P_n(0)\notin A\), sometimes lost in OCR, is important for the positive lower bound.

### 3.2 Bounded interpolation in the upper half-plane

The lemma on pp.191–192 constructs a function \(f_n\), holomorphic above the real line and continuous on its closure, with
\[
 |f_n|<1-d_n/2.
\]
For each \(t\in T_n\), it supplies t-points \(\zeta_j(t)\), with \(\operatorname{Im}\zeta_j(t)\ge2\), whose arguments are dense in \([0,\pi]\), and on their unit circles it gives
\[
 |f_n(\zeta)-t|\ge c_n|\zeta_j(t)|^{-5/4}
\]
for all sufficiently large indices. The unit discs lie strictly inside the upper half-plane. Section 4 below checks the interpolation estimates; the lower bound is what allows approximation without destroying the desired a-points.

### 3.3 Domain-plane sectors and approximation

The original construction places one closed half-plane below \(\operatorname{Im}z=-1\), then translated disjoint dyadic sectors in the upper half-plane. In its notation,
\[
 G_1=\{\operatorname{Im}z\le-1\},\qquad L_1(z)=-z-i,
\]
and for \(n\ge2\),
\[
 p_n=n2^n e^{i\pi2^{2-n}},\quad
 G_n=p_n+\{re^{i\theta}:r\ge0,\ \pi2^{1-n}\le\theta\le\pi2^{2-n}\},
\]
\[
 L_n(z)=-(z-p_n)^{2^{n-1}}.
\]
On the appropriate branch, each \(L_n\) maps the sector interior conformally to the upper half-plane. Put
\[
 F_n=P_n\circ f_n\circ L_n.
\]
The sectors are connected by the polygonal arc through their successive vertices, starting at \(-i\), to form the closed continuum used in the paper. Its complement has the escape geometry specified there: complementary points can be joined to infinity by a half-ray. Define \(F\) to agree with \(F_n\) on each sector and extend continuously along the joining arc.

At this precise step, p.193 invokes Keldysh's entire-approximation theorem, citing the 1945 announcement and Mergelyan's 1952 exposition. It gives an entire \(G\) with
\[
 |G(z)-F(z)|<\exp(-|z|^{1/4})
\]
on that continuum. This is the external approximation theorem used here; mere Runge approximation on compact sets, without the tail control, would not justify this step.

### 3.4 Inclusion of the desired values

Fix \(a\in A\) and a sector index \(n\). The preimages under \(L_n\) of the interpolation circles are closed contours inside \(G_n\). Their angular widths tend to zero; their angular locations have dense tails in the dyadic angular interval assigned to \(n\).

On the compact disc \(|t|\le1-d_n/2\), univalence gives a constant \(\mu_n>0\) with
\[
 |P_n(t)-P_n(s)|\ge\mu_n|t-s|.
\]
Indeed, the difference quotient extends continuously across the diagonal by the nonvanishing derivative and is nowhere zero on that compact product. Thus the interpolation lower bound transfers to the contours:
\[
 |F_n(z)-a|\ge C_n|z|^{-(5/4)2^{n-1}}
 \ge C'_n|z|^{-2^n}
\]
for sufficiently large contours, with \(n\) fixed. For \(n=1\), the affine map gives the same harmless weaker polynomial bound.

The approximation error \(e^{-|z|^{1/4}}\) is eventually smaller than this polynomial lower bound. Rouché's theorem therefore preserves at least one a-point inside each sufficiently distant contour. The dyadic intervals together with the lower half-plane cover all directions apart from endpoints; every nonempty angle contains a smaller interval in one of their interiors. This yields infinitely many a-points in every angle and proves \(A\subseteq E(G)\).

### 3.5 Exclusion of every other value

Fix \(b\notin A\). Because \(\bigcap D_n=A\), some \(D_{n_0}\) excludes \(b\). The image of \(G_{n_0}\) under \(F_{n_0}\) lies in the compact set
\[
 K_{n_0}=P_{n_0}(\{|t|\le1-d_{n_0}/2\})\Subset D_{n_0}.
\]
Its distance to the complement of \(D_{n_0}\) is positive. The approximation error tends to zero, so sufficiently far out in \(G_{n_0}\), the entire function \(G\) still takes values in \(D_{n_0}\), and in particular never equals \(b\).

Every fixed closed angular subinterval strictly inside the unshifted sector lies in its translated sector outside a sufficiently large disc. Choose one such open angle. It has no b-points sufficiently far out and only finitely many in the remaining compact portion. Consequently \(b\notin E(G)\), proving \(E(G)\subseteq A\). The radius and chosen angle may depend on \(b\), exactly as the negation of the problem's definition allows.

## 4. Check of the lemma's analytic estimates

The original proof on pp.194–198 uses widely separated interpolation points \(\zeta_j=r_je^{i\theta_j}\). For each target value the assigned directions have dense tails. Choose radii sufficiently large that \(\operatorname{Im}\zeta_j\ge2\), \(\theta_j>r_j^{-1/4}\), and
\[
 r_{j+1}>r_j^{1+2/\delta},\qquad r_{j+1}/r_j\ge B,
 \quad 0<\delta<1/4.
\]
These conditions are compatible with any prescribed recurrent dense list of angles in \((0,\pi)\). The literal small initial radius in the original display is immaterial: begin sufficiently far out to meet the height condition. No estimate depends on retaining an impossible first point of modulus one and height at least two.

For the upper half-plane, form the Blaschke products omitting the j-th zero,
\[
 \phi_j(\zeta)=\prod_{k\ne j}\frac{\overline\zeta_k}{\zeta_k}
                  \frac{\zeta-\zeta_k}{\zeta-\overline\zeta_k},
\]
and localized factors
\[
 \Phi_j(\zeta)=(\zeta/r_j)^\delta\exp[-(\zeta/r_j)^\delta],
 \qquad 0\le\arg\zeta\le\pi.
\]
The rapid growth of the radii ensures local convergence of the products. They satisfy \(|\phi_j|\le1\), and radial separation gives the positive uniform lower bound
\[
 |\phi_j(\zeta_j)|\ge
 \Psi(B):=\left[\prod_{k\ge1}\frac{1-B^{-k}}{1+B^{-k}}\right]^2,
 \qquad\Psi(B)\longrightarrow1.
\]
Normalize \(h_j=\Phi_j\phi_j/(\Phi_j(\zeta_j)\phi_j(\zeta_j))\). Then \(h_j(\zeta_k)=\delta_{jk}\). Also \(|\Phi_j(\zeta_j)|\ge e^{-1}\). Splitting the sum at the radius nearest \(|\zeta|\), and using geometric-series bounds on each tail, gives
\[
 \sum_j|h_j(\zeta)|\le\Psi_1(B)/\Psi(B),\qquad
 \Psi_1(B)\longrightarrow1,
\]
with the original choice \(\delta=(\log\log B)^{-1}\). Choose \(B\) so large that this ratio is less than \((1-d/2)/(1-d)\). Then
\[
 f(\zeta)=\sum_j t_jh_j(\zeta),\qquad d\le|t_j|\le1-d,
\]
is locally uniformly convergent, continuous on the closed half-plane, interpolates \(t_j\), and has modulus below \(1-d/2\).

The nonvanishing bound on the unit circle around \(\zeta_j\) requires more than interpolation. There,
\[
 \log h_j(\zeta)
 =\delta(1-e^{i\delta\theta_j})\frac{\zeta-\zeta_j}{\zeta_j}
   +O(r_j^{-5/3}).
\]
The \(O(r_j^{-5/3})\) term, visible in the original p.197 image, includes the logarithmic derivative of the Blaschke factor; OCR can misread this exponent. Since \(\theta_j>r_j^{-1/4}\), the magnitude of the displayed leading term is at least
\[
 (2\delta^2/\pi)r_j^{-5/4}.
\]
The exponent comparison \(5/3>5/4\) makes the error negligible. Hence \(|h_j-1|\ge c r_j^{-5/4}\) eventually. The remaining localized factors contribute
\[
 \sum_{k\ne j}|h_k(\zeta)|=O(r_j^{-2}),
\]
as checked in equation (18) on p.198, using \(r_{j-1}<r_j^{1/3}\) and \((r_j/r_{j+1})^\delta=O(r_j^{-2})\). Therefore
\[
 |f(\zeta)-t_j|
 \ge d|h_j(\zeta)-1|-\sum_{k\ne j}|h_k(\zeta)|
 \ge c' r_j^{-5/4}
\]
for all sufficiently large j. This is the exact lower bound required by Rouché's theorem above.

## 5. Boundaries of the conclusion

The construction is analytic and existential. It does not provide a finite formula, a certified numerical sample, a finite growth order, or an exact classification of all possible \(E(G)\). The original paper's bounded countable extension and the later summary are not needed for the two-point case. The known affirmative result is complete for the specific existence question, and its credit remains with Gol’dberg.
