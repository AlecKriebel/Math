# An elementary rotation-only lower bound for pyjama coverings

## Status and exact scope

This is a partial quantitative result for the original whole-plane problem, not a solution of its asymptotic-order question. The main proof below is self-contained. It uses no existence theorem, dynamical theorem, translation, or dilation. The elementary bound was derived in this work; no occurrence was located in the bounded literature check described in [SOURCE_METADATA.json](SOURCE_METADATA.json). That is not a global novelty certificate.

For a unit vector \(u\in\mathbb R^2\), put
\[
 P_u(\varepsilon)=\{x:\operatorname{dist}(u\cdot x,\mathbb Z)\leq\varepsilon\}.
\]
Let \(N(\varepsilon)\) be the least number of such sets covering all of \(\mathbb R^2\). This is exactly rotation about the origin of the closed vertical-strip set in Green's Problem 41 (dataset 171 / GREEN-083). Replacing \(u\) by \(-u\) leaves the set unchanged.

### Theorem 1 (first-circle obstruction)

For every \(0<\varepsilon<1/2\), every covering by \(n\) rotations satisfies
\[
 n\geq\frac{\pi}{2\arcsin(\varepsilon/(1-\varepsilon))}.
 \tag{1}
\]
Consequently,
\[
 N(\varepsilon)\geq\left\lceil\frac{\pi}{2\arcsin(\varepsilon/(1-\varepsilon))}\right\rceil,
 \qquad
 \liminf_{\varepsilon\downarrow0}\varepsilon N(\varepsilon)\geq\frac\pi2.
 \tag{2}
\]
Equivalently, a covering with \(n\geq2\) rotations requires
\[
 \varepsilon\geq\frac{\sin(\pi/(2n))}{1+\sin(\pi/(2n))}.
 \tag{3}
\]

**Proof.** Fix \(r\) with \(\varepsilon<r<1-\varepsilon\). If \(|x|=r\), then \(|u\cdot x|\leq r<1-\varepsilon\). Thus for every nonzero integer \(k\),
\[
 |u\cdot x-k|\geq |k|-|u\cdot x|>\varepsilon.
\]
It follows that on this circle the periodic set \(P_u(\varepsilon)\) agrees exactly with its central strip \(\{|u\cdot x|\leq\varepsilon\}\).

Parameterize the circle by \(x=r(\cos t,\sin t)\), \(0\leq t<2\pi\), and write \(u=(\cos\theta,\sin\theta)\). Membership becomes
\[
 |\cos(t-\theta)|\leq\varepsilon/r.
\]
This set of angles consists of two closed arcs, each of angular length \(2\arcsin(\varepsilon/r)\). Its total angular measure is therefore \(4\arcsin(\varepsilon/r)\), independently of \(u\).

If \(n\) rotated pyjama sets cover the whole plane, these \(n\) pairs of arcs cover the entire circle. Finite subadditivity of angular measure gives
\[
 2\pi\leq4n\arcsin(\varepsilon/r).
\]
Let \(r\uparrow1-\varepsilon\). Continuity of \(\arcsin\) gives (1); integrality gives the first part of (2). Since \(\arcsin t/t\to1\) as \(t\to0\), the right-hand side of (1), multiplied by \(\varepsilon\), tends to \(\pi/2\). This proves the liminf assertion.

For \(n\geq2\), (1) is equivalent to \(\arcsin(\varepsilon/(1-\varepsilon))\geq\pi/(2n)\). Monotonicity of sine on \([0,\pi/2]\) gives (3). All steps preserve weak inequalities, as required for the closed-strip problem. \(\square\)

**Endpoint check.** One can also work directly on \(|x|=1-\varepsilon\). A noncentral strip can meet this circle only where \(u\cdot x=\pm(1-\varepsilon)\), at at most two isolated tangency points. These have zero angular measure. The limiting-radius proof avoids needing even this observation.

**Comparison with the cited volume bound.** The usual bound is \(N(\varepsilon)\geq1/(2\varepsilon)\). The real-valued right-hand side of (1) divided by \(1/(2\varepsilon)\) tends to \(\pi\). Thus (1) improves that explicit lower bound by an asymptotic constant factor \(\pi\). It does not improve the order \(\varepsilon^{-1}\). In particular it proves neither \(\varepsilon N(\varepsilon)\to\infty\) nor a polynomial upper bound.

### Proposition 2 (exact strength of the first-circle test)

For \(0<\varepsilon<1/2\), let \(m\) be the number of distinct strip axes modulo \(\pi\), represented cyclically by \(0\leq\alpha_1<\cdots<\alpha_m<\pi\). Set \(\alpha_{m+1}=\alpha_1+\pi\), and let \(g=\max_j(\alpha_{j+1}-\alpha_j)\). A necessary condition for a whole-plane cover is
\[
 g\leq2\arcsin(\varepsilon/(1-\varepsilon)).
 \tag{4}
\]
This condition is also necessary and sufficient for the corresponding central strips to cover the closed disk of radius \(1-\varepsilon\).

**Proof.** Work in the circle of directions modulo \(\pi\). At radius \(r>\varepsilon\), a central strip covers precisely the directions at distance at most \(a_r=\arcsin(\varepsilon/r)\) from its axis. Such intervals cover the directional circle if and only if every successive gap has length at most \(2a_r\): a larger gap leaves its midpoint uncovered; conversely every point between successive axes is within half their separation of one of them. Coverage at the outer radius implies coverage at each smaller radius, since central strips are radially star-shaped; the disk of radius \(\varepsilon\) is in every central strip. Apply this with outer radius \(1-\varepsilon\). For a whole-plane cover, use radii below \(1-\varepsilon\) and take the limit as in Theorem 1. \(\square\)

Since the gaps sum to \(\pi\), (4) implies (1) with \(m\leq n\). Conversely, equally spaced axes have all gaps \(\pi/m\). They achieve the best possible disk coverage, proving that this local-disk method alone cannot give a larger necessary lower bound. This converse concerns only the disk. It is not a whole-plane upper bound. In fact equally spaced directions fail for every \(\varepsilon<1/3\), by the credited roots-of-unity result discussed in [SOURCE_METADATA.json](SOURCE_METADATA.json).

### Proposition 3 (an independent second-moment obstruction)

For \(0<\varepsilon<1/2\), every whole-plane cover satisfies
\[
 n\geq1+\frac1{2\varepsilon}.
 \tag{5}
\]

**Proof.** Discard repeated unoriented directions and write the remaining number as \(m\leq n\). If \(m=1\), a point with \(u\cdot x=1/2\) is uncovered, so a cover has \(m\geq2\). Set \(p=2\varepsilon\), and let \(I_j(x)\) be the indicator of \(P_{u_j}(\varepsilon)\). Put \(M(x)=\sum_{j=1}^m I_j(x)\).

We first justify the exact asymptotic densities used here. Let \(B_R\) be the radius-\(R\) disk, and write \(\langle f\rangle_R=(\pi R^2)^{-1}\int_{B_R}f\). In orthogonal coordinates whose first axis is \(u_j\), the set \(P_{u_j}(\varepsilon)\) is periodic with period lattice \(\mathbb Z^2\), and its indicator has mean \(p\) on a unit fundamental square. For \(i\ne j\), the linear map \(A:x\mapsto(u_i\cdot x,u_j\cdot x)\) is invertible, because the two directions are not parallel. In those coordinates, \(I_iI_j\) is the indicator of \((\mathbb Z+[-\varepsilon,\varepsilon])^2\), with mean \(p^2\) on \([0,1)^2\). Pulling back the integer lattice through \(A\) yields a fixed lattice in the original plane, with the same fundamental-cell proportion \(p^2\).

For completeness, the average over growing disks of any bounded measurable function periodic under a fixed full-rank lattice converges to its fundamental-cell mean: tile by one bounded fundamental parallelogram. Cells completely inside the disk contribute their exact mean. Cells meeting its boundary are contained in an annulus of fixed width, hence have total area \(O(R)\). The discrepancy between their actual integrals and mean-times-area is also \(O(R)\). Dividing by \(\pi R^2\) proves convergence. Cell boundaries have area zero. This proves
\[
 \lim_R\langle I_j\rangle_R=p,
 \qquad
 \lim_R\langle I_iI_j\rangle_R=p^2.
\]
Only individual and pairwise periodicity was used; no common lattice for all the rotations was assumed.

A cover has \(1\leq M(x)\leq m\) everywhere. Therefore \((M(x)-1)(M(x)-m)\leq0\). Integrate and let \(R\to\infty\), using \(M^2=\sum_j I_j+2\sum_{i<j}I_iI_j\), to obtain
\[
 mp+m(m-1)p^2-(m+1)mp+m
 =m(1-p)\bigl(1-(m-1)p\bigr)\leq0.
\]
Since \(m>0\) and \(0<p<1\), it follows that \((m-1)p\geq1\). Thus \(n\geq m\geq1+1/p\), proving (5). \(\square\)

The two independent bounds can be combined as
\[
 N(\varepsilon)\geq\left\lceil\max\left\{
 \frac{\pi}{2\arcsin(\varepsilon/(1-\varepsilon))},
 1+\frac1{2\varepsilon}\right\}\right\rceil.
\]
The first-circle bound is the asymptotically stronger one. The second-moment bound remains useful near \(\varepsilon=1/2\).

## Boundary examples, credited rather than new

For \(\varepsilon\geq1/2\), the unrotated closed set already equals the plane, so \(N(\varepsilon)=1\). For \(1/3\leq\varepsilon<1/2\), \(N(\varepsilon)=3\). To see the upper bound, choose unit normals \(u_1,u_2,u_3\) at angles \(0,2\pi/3,4\pi/3\), so \(u_1+u_2+u_3=0\). If some point missed all three strips at width \(1/3\), the fractional parts of \(u_j\cdot x\) would all lie in \((1/3,2/3)\). Their sum would then lie strictly between 1 and 2, yet it is an integer because the three unrounded coordinates sum to zero. This is impossible. Monotonicity gives coverage at every larger width. The lower bound of three follows from (5), or directly by solving two independent dot-product equations with right sides \(1/2\).

For \(0<\varepsilon<1/3\), Theorem 1 gives \(N(\varepsilon)\geq4\). The equilateral three-rotation construction is already explicit in Malikiosis–Matolcsi–Ruzsa (2012/2013), p.2, and is not claimed as new here.

## Exact remaining gap

The established quantitative upper bound is the prior Kravitz–Leng theorem: some universal \(C>0\) gives a whole-plane cover with at most \(\exp\exp\exp(\varepsilon^{-C})\) rotations for \(0<\varepsilon<1/10\). Their theorem is stated for open strips and therefore also yields the closed-strip cover considered here. The theorem is credited, not re-proved or independently audited in this attempt.

Our lower bound and that prior upper bound do not determine the order of \(N(\varepsilon)\). A claimed solution would still need substantially smaller upper bounds and/or a lower bound of a genuinely larger order, with matching estimates if asserting the asymptotic order. The sharp disk example is expressly insufficient for this purpose.
