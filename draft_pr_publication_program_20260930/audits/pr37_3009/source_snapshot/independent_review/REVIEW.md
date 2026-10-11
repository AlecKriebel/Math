# Independent review of the planar recurrence partial result

**Verdict: PASS for the stated low-dimensional consequence of established theorems.** No mandatory mathematical correction was found. This is not a solution of the complete KP-5.2 target: dimensions at least three, including the stated stronger smooth-recurrence variant, remain unresolved in the submitted package. No novelty or priority is certified.

Reviewed on 30 September 2026 by a separate gpt-6-astra, xhigh reviewer. The reviewed artifact is PARTIAL.md for problem 3009, SHA-256 **c24cf9578f26202c2af4e25d017a5e44d7047ad32e7f35ebac0604275399f00f**. The author artifact was not edited. The review checks its arguments against the original question and the actual hypotheses of the imported theorems.

## Source and category

The full pinned record agrees with [K3, Problem 5.2](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pages 302–303. The relevant pages were read, and page 302 was rendered and visually checked. Part (a) concerns homeomorphisms or diffeomorphisms of the entire Euclidean space, one common bound on the diameters of all full orbits, and a subsequence of powers tending to the identity in the compact-open topology. Part (b) concerns a closed ball with its boundary fixed pointwise. The general-dimension formulation must be retained. The source's informal remarks about other manifolds and local smallness are not separate theorems proved by this package.

The [Kolev–Pérouème primary preprint](https://arxiv.org/abs/math/0303258v3), pages 1–2, defines recurrence by one sequence of positive iterates converging uniformly on a compact metric space. Its Theorem 1.1 states that a nonidentity orientation-preserving recurrent sphere homeomorphism has exactly two fixed points. The boundary-fixed disk consequence is explicitly given immediately afterward. I read these statements, the recurrence discussion, and the proof in Sections 2–3; page 2 was also rendered. The arXiv metadata and [publisher record](https://doi.org/10.1017/S0305004197002272) identify the publication as Mathematical Proceedings of the Cambridge Philosophical Society 124 (1998), 161–168. The downloaded text was the March 2009 v3, not a claimed byte-identical journal PDF: the publisher PDF endpoint returned HTML in this review.

The Cartwright–Littlewood statement in [Boroński, Theorem A, page 1](https://arxiv.org/abs/1510.06663) has exactly the orientation, compactness, connectedness, nonseparation, and invariance assumptions used below. I also read its Section 3 explanation of Brown's covering-space proof. That source calls a continuum nondegenerate; the constructed set contains an open disk, so this convention causes no issue. Neither the author nor this review represents the original 1951 or Brown 1977 PDF as independently inspected.

## Audit of the reduction

### The uniform bound and orientation

The equivalence between a common full-orbit diameter bound and

\[
 |h^k(x)-x|\le D\quad\text{for every }x\in\mathbb R^2,\ k\in\mathbb Z
\]

is correct with the same constant. To compare any two orbit points, apply the displayed inequality at the second point with the difference of the exponents. Merely assuming that each orbit is individually bounded would be insufficient.

For the straight-line homotopy \(H(x,t)=x+t(h(x)-x)\), the estimate
\(|H(x,t)|\ge |x|-D\) is uniform in \(t\in[0,1]\). More explicitly, the preimage of a compact subset of a radius-\(M\) disk is closed and lies in the compact product \(\overline B(0,M+D)\times[0,1]\). Thus this is a proper homotopy of maps of the plane. Its extension fixes the added point at infinity and is continuous jointly in \(x,t\). Degree is therefore unchanged from the identity, and the homeomorphism has degree \(+1\). This suffices for orientation preservation; an isotopy through homeomorphisms was never required.

### Uniform recurrence on the sphere

The chordal distance formula and estimate (2) are correct, including the factor 2. For \(|x|\ge R>D\), the lower bounds on the two denominator factors follow respectively from \(|x|\ge R\) and \(|h^k(x)|\ge |x|-D\). They hold for all iterates with the same constant.

Given a spherical error tolerance, choose \(R\) so the exterior bound is smaller than that tolerance. Compact-open recurrence then makes the chordal error on the radius-\(R\) disk small along the given sequence; one may use \(q(x,y)\le 2|x-y|\) there. Infinity has zero error. This proves the precise uniform recurrence needed by Kolev–Pérouème. No uniform Euclidean recurrence on the whole plane is inferred.

### Connected invariant neighborhoods

For \(D>0\), each \(h^k(B(a,2D))\) is connected and contains \(h^k(a)\). That point belongs to the original ball because its distance from \(a\) is at most \(D<2D\). Every member of the union therefore meets the connected central member. The union \(U_a\) is connected and open.

The index set is all of \(\mathbb Z\), so reindexing gives \(h(U_a)=U_a\), not just one-sided invariance. If \(x=h^k(y)\) with \(|y-a|<2D\), then \(|x-a|\le |x-y|+|y-a|<3D\). Its closure \(C_a\) is consequently compact, connected, nonempty, and invariant under both \(h\) and its inverse. Taking the closure of just one orbit instead would not justify connectedness; the submitted construction correctly avoids that shortcut.

### Filling and the fixed-point theorem

Let \(V_\infty\) be the unbounded component of \(\mathbb R^2\setminus C_a\). It is unique because the entire exterior of a disk containing \(C_a\) is connected. The filled set is

\[
 K_a=\mathbb R^2\setminus V_\infty.
\]

It is closed and bounded. Every bounded complementary component of \(C_a\) has nonempty boundary contained in \(C_a\); its closure is connected and meets \(C_a\). Adding all these components thus preserves connectedness. The complement of \(K_a\) is connected by definition. No local connectivity, smooth boundary, or Jordan-domain assumption is needed.

A plane homeomorphism is proper and permutes the complementary components of an invariant compact set. It sends an escaping sequence to an escaping sequence, so it preserves the unique unbounded component. Consequently \(h(K_a)=K_a\). Every point exterior to the closed radius-\(3D\) disk is connected to infinity in the complement of \(C_a\), so \(K_a\) stays in that closed disk.

All Cartwright–Littlewood hypotheses now hold, yielding a fixed point in each such disk. Choose centers at distance \(7D\), for example; the two closed radius-\(3D\) disks are disjoint. Their finite fixed points together with infinity give at least three distinct sphere fixed points. Orientation and recurrence were established above. The sphere theorem forces the identity. The separate \(D=0\) case is immediate.

### Closed disks, intervals, and smooth maps

Pointwise boundary fixation makes the piecewise extension by the exterior identity a continuous bijection with a continuous piecewise inverse. It is a plane homeomorphism. Interior points cannot move to the boundary, because a boundary point is already its own unique preimage. All full orbits therefore remain inside the closed disk or are singleton exterior orbits. A diameter bound of 2 applies to the unit disk, and compact-open convergence on the compact closed disk is uniform. The extension has the required recurrence.

No differentiability across the glued boundary is needed: a diffeomorphism is in particular a homeomorphism, and stronger smooth recurrence implies the required compact-open recurrence. The warning against claiming a smooth extension is appropriate.

On the line, a decreasing surjective homeomorphism has unbounded displacement at positive infinity. An increasing homeomorphism that moves a point right has all positive iterates at least as far right as the first image, contradicting recurrence at that point; the left-moving case is identical. Boundary fixation on a closed interval ensures increasing orientation. These arguments establish both one-dimensional conclusions.

## Adversarial controls and remaining scope

Two explicit controls illustrate why the hypotheses cannot be silently weakened.

1. An irrational rotation of the plane is compact-open recurrent and every individual orbit is bounded, but no common orbit-diameter bound exists. Its first nonzero angular displacement grows linearly with radius. It does not refute the submitted theorem.
2. On the unit disk, the radial twist \(h(re^{i\theta})=re^{i(\theta+2\pi r)}\), extended by the identity outside, fixes the boundary and has full-orbit diameters at most 2. For every integer \(m\ge1\), the radius \(r_m=1-1/(2m)\) is moved by angle \(\pi\) modulo \(2\pi\) under \(h^m\), giving displacement \(2r_m\ge1\). Thus no sequence of iterates converges uniformly to the identity on the disk. Bounded orbits alone do not imply the submitted conclusion.

For a dimension control, \(\operatorname{diag}(-1,-1,1,1)\) restricts to a nonidentity orientation-preserving period-two map of \(S^3\) fixing a whole circle. Hence the sphere fixed-point count used here has no dimension-independent extension. This is a countercontrol to that proof step, not a counterexample to KP-5.2.

The 1990 Oversteegen–Tymchatyn theorem concerns uniform recurrence in the Euclidean metric on the whole plane. The metric warning is independently explicit on page 2 of Kolev–Pérouème; the correct [AMS bibliographic record](https://www.ams.org/journals/proc/1990-110-04/home.html) was checked, but the primary AMS PDF returned HTTP 403. The submitted proof does not depend on substituting that theorem for compact-open recurrence.

Likewise, [Pardon's theorem](https://arxiv.org/abs/1112.2324v3) assumes a locally compact faithfully acting group. It cannot be applied by declaring the closure of the powers compact or locally compact without proof. The source and package explicitly retain this gap. The recurrence-versus-equicontinuity warning is supported by the nonregular recurrent examples discussed in the primary sphere paper.

## Reproduction and verdict

The author's check program was copied to a separate review directory and rerun unchanged: all **31 assertions passed**, and its JSON output matches the submitted output. The independently written control program passes **8,462 exact assertions**, including 1,404 chordal-bound vector cases, 7,020 proper-homotopy vector cases, symbolic stereographic identities, and explicit hypothesis/dimension controls. These computations are algebraic diagnostics only. They neither prove the imported global topological theorems nor resolve the remaining dimensions.

**Publication disposition:** suitable for a draft PR as a credited low-dimensional consequence with the full target marked **unsolved**. Preserve the frozen artifact hash, the established-theorem attribution, and the lack of a novelty claim. No mandatory revision remains after this independent audit.
