# Independent audit of the global approximate root bound

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance applies only to the stated partial theorem; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and symbolic checks described below occurred in the preceding investigation and audit on 11 October 2026. Editorial preparation authenticated retained bytes without a new scholarly-source inspection or mathematical-program rerun.

## Verdict and exact scope

**Accept as a partial theorem.** For the family

    x^2 - y^2 + a1*x + a2*y + a0 = 0,
    x*y + b1*x + b2*y + b0 = 0,

with all six coefficients unrestricted in R, let N(epsilon) be the least number of open sets covering the whole coefficient space such that each set admits a continuous R^2-valued function at Euclidean distance strictly less than epsilon from at least one actual real common root at every parameter. For every fixed epsilon > 0,

    2 <= N(epsilon) <= 3,

and N(epsilon) is independent of epsilon. The proof includes singular fibers, arbitrarily large coefficients, and the zero parameter. The alternative N = 2 versus N = 3 is not resolved. No novelty, full solution, or present-day literature-status claim is made.

This audit independently reconstructs the candidate argument rather than treating successful algebra or byte checks as mathematical acceptance. No mathematical correction is necessary. Several continuity and closure details that are compressed in the candidate are supplied below. The candidate's metadata still says that it awaits audit; this report records the independent acceptance of its partial result without altering that input.

Audited candidate manifest: SHA256 7a51ec74eeb0005895b9db3b5ae38d12d940b9437fb9233602246be8b1bd5a25, 2216 bytes, 13 listed members. Every listed member's size and SHA256 matched. The proof and dependency statement were read in full. No candidate checker or source-author program was executed.

## Source scope and inspection boundary

The formulation is Problem 2B, with the preceding family and Problem 2A, on printed page 205 of V. A. Vassiliev, [A Few Problems on Monodromy and Discriminants](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf), Arnold Mathematical Journal 1 (2015), 201-209. That page specifies arbitrary affine terms and the entire six-dimensional real parameter space, then permits one fixed positive root-neighborhood tolerance in the approximate question. It does not replace root distance by residual size or explicitly remove singular parameters. The source's exact-selection lower-bound remark does not itself establish the approximate lower bound.

The published PDF is 396737 bytes, SHA256 5d5e81d87118ba8d06685e49dd6619af204956631b1abeb2edd7dfd2d53d3042. The authenticated page-205 image was visually inspected, and the relevant text was checked against the public PDF's web extraction. A web screenshot request failed; the successful visual inspection was of the authenticated local image. No fresh network-byte hash of the PDF was obtained in this audit. No third-party source text or image is copied into this packet.

The remainder of this report is independently authored mathematical analysis. The cited article supplies the problem, not the following upper-bound construction. No unrelated historical or broader literature conclusion is adopted.

## 1 Coordinate reduction preserves precisely the requested problem

Identify R^2 with C isometrically by z = x + i*y. Write

    A = a1 + 2i*b1, B = a2 + 2i*b2, gamma = a0 + 2i*b0,
    alpha = (A - i*B)/2, beta = (A + i*B)/2.

Then the first polynomial plus 2i times the second is

    z^2 + alpha*z + beta*conjugate(z) + gamma.

The inverse linear formulas A = alpha + beta and B = i*(alpha - beta) show that this is a real-linear bijection between R^6 and C^3. Substituting z = u - alpha/2 gives

    H_beta(u) = w,
    H_beta(u) = u^2 + beta*conjugate(u),
    w = alpha^2/4 + beta*conjugate(alpha)/2 - gamma.

For fixed alpha,beta the last formula is an affine bijection in gamma. Thus the parameter change to (alpha,beta,w) is a global homeomorphism, not a local normalization or a discriminant-complement reduction. Translation by -alpha/2 preserves Euclidean distances.

A k-chart approximate cover of C^2 in (beta,w) pulls back to C^3 and gives the selector F(beta,w)-alpha/2. Conversely a k-chart cover in C^3 restricts to the slice alpha=0, producing an open cover relative to that slice, which is homeomorphic to C^2. Empty intersections can be discarded. Consequently the two minimal chart numbers agree for each identical positive tolerance. All following work may therefore be done in C^2 without losing any original parameter.

## 2 Uniform local boundedness and finite fibers

Put b = |beta|. Every actual root satisfies

    |u|^2 <= b*|u| + |w|,
    |u| <= (b + sqrt(b^2 + 4|w|))/2 <= b + sqrt(|w|).

In particular roots are bounded uniformly when parameters vary in any sufficiently small bounded neighborhood. If (beta_n,w_n) tends to (beta_0,w_0) and u_n is a root, every convergent subsequence of u_n limits to a root of the limiting parameter. This local boundedness plus continuity will repeatedly prevent roots from appearing far from the limiting fiber.

For each fixed beta, |H_beta(u)| >= |u|^2-b|u| tends to infinity with |u|, so the map is proper. On a sufficiently large circle the maps

    u -> u^2 + s*beta*conjugate(u) - w, 0 <= s <= 1,

never vanish. Their boundary winding number is the winding number 2 of u^2. The planar Brouwer degree is therefore 2 for every target w, and every fiber is nonempty.

For beta != 0, conjugation of the root equation and substitution give the necessary equation

    (u^2-w)^2 + |beta|^2*beta*u - beta^2*conjugate(w) = 0.

It is a monic polynomial of degree four in u, so there are finitely many actual roots. Sufficiency of this eliminated equation is not needed or assumed. For beta=0 there are the familiar square roots, including the single root at w=0. Hence every fiber is finite, and local degrees at individual roots are defined by sufficiently small isolating disks.

## 3 The central disk is genuinely a Jordan disk

For beta != 0 let D_beta = {u: |u| < b/2}. The real Jacobian determinant is

    J_beta(u) = 4|u|^2 - b^2.

Suppose H_beta(u)=H_beta(v) with |u|,|v| <= b/2. Subtraction yields

    (u-v)(u+v) + beta*conjugate(u-v) = 0.

If u != v, taking absolute values gives |u+v|=b. Equality in

    |u+v| <= |u|+|v| <= b

then forces both radii to equal b/2 and both vectors to have the same direction. This implies u=v, a contradiction. Thus H_beta is injective on the entire closed disk.

A continuous injection from that compact disk into the Hausdorff plane is a homeomorphism onto its image. Invariance of domain makes H_beta(D_beta) open. The image of the boundary circle is a simple closed curve. To spell out the interior assertion, no point of this curve is in H_beta(D_beta), by injectivity. Every limit point of H_beta(D_beta) is in the image of the closed disk, by compactness; a boundary point of the open image cannot be the image of an interior disk point. Therefore its boundary is exactly the circle image. Jordan separation identifies the image with the bounded complementary component: it is a nonempty bounded open and relatively closed subset of that component. Write this Jordan interior as Omega_beta. Its closure is exactly H_beta(closed D_beta), and it contains H_beta(0)=0.

Set Omega_0 empty and

    Omega = {(beta,w): beta != 0 and w in Omega_beta}.

At its unique disk root the Jacobian is strictly negative. The real implicit-function theorem continues that root over a full neighborhood in C^2, and strict membership |u|<|beta|/2 persists on a smaller neighborhood. Thus Omega is open in C^2. These local branches agree by uniqueness, giving a continuous exact section sigma on Omega, with |sigma|<|beta|/2.

No critical target lies in Omega_beta or outside its closure: the full critical locus is the circle |u|=b/2, and its image is the Jordan boundary. Also the injection on the closed disk implies that a given target can have at most one critical root.

## 4 Local critical degrees and all actual root counts

Locally in beta != 0 choose theta continuously so beta=b*exp(3i*theta). The orientation-preserving domain and target changes

    u=b*exp(i*theta)*zeta, w=b^2*exp(2i*theta)*eta

reduce to H(zeta)=zeta^2+conjugate(zeta). A critical point is zeta_0=exp(i*t)/2. For displacement delta=exp(-i*t/2)*(x+i*y), subtract H(zeta_0) and multiply the target by exp(-i*t/2). The resulting germ is

    2*x + k*(x+i*y)^2, k=exp(-3i*t/2)=A+i*B,

whose real and imaginary parts are

    F=2*x + A*(x^2-y^2) - 2*B*x*y,
    G=B*(x^2-y^2) + 2*A*x*y.

All these coordinate changes preserve orientation. Since F_x(0)=2>0, (x,y)->(F,y) is an orientation-preserving local diffeomorphism. The equation F=0 has a unique solution x=h(y) with h(y)=A*y^2/2+O(y^3). In these coordinates, the local planar degree is the one-dimensional local degree of g(y)=G(h(y),y).

If B != 0, then g(y)=-B*y^2+O(y^3), and its one-dimensional local degree at zero is 0. The nonzero second derivative is the fold condition. If B=0, then A=+1 or -1 and

    g(y)=2*A*h(y)*y=y^3+O(y^4).

The local degree is +1. In the coordinates (s,y)=(F,y), the mixed derivative of the second component with respect to s and y is A != 0 at the origin. Together with the nonzero cubic coefficient and the nondegenerate transversal coordinate F, this gives the cusp case. In fact the parameter-free degree calculation, rather than a catastrophe-classification theorem, is all the proof uses. B=0 is equivalent to exp(3i*t)=1, giving exactly three cusps of the critical circle.

At regular roots the sign of J is the local degree: -1 inside D_beta, +1 outside its closure. Additivity of degree over the finite fiber now establishes the counts without numerical sampling:

- If w is inside Omega_beta, it has exactly one negative root in D_beta, no critical root, and therefore exactly three positive roots.
- If w is outside closed Omega_beta, it has no negative or critical roots, and therefore exactly two positive roots.
- At a noncusp boundary target it has one degree-zero critical root and no negative root, and therefore exactly two positive regular roots.
- At a cusp target it has one degree-one critical root and no negative root, and therefore exactly one positive regular root.

The absence of a negative root on the boundary follows from closed-disk injectivity, not a generic-fiber limit argument. The local degrees are topological integers, not polynomial multiplicities. As an optional identity check, the eliminated polynomial at the normalized cusp target w=3/4 factors as (u-1/2)^3*(u+3/2); the triple algebraic root has local topological degree +1.

## 5 The selected exterior roots form a two-sheeted cover

Define

    E = (C^2 \ Omega) \ {(0,0)}.

For beta != 0 and an exterior or fold target, select the two regular positive roots. At a cusp select its degree-one critical root and its regular positive root. For beta=0,w != 0 select both square roots. Each parameter of E consequently has exactly two distinct selected roots, each of local degree +1. This is a specially selected relation, not the full root relation on the caustic: a fold's degree-zero root is deliberately omitted.

Here is a detailed proof that the relation S inside E x C, with its subspace topology, is a two-sheeted covering of E.

**At ordinary exterior points and beta=0,w != 0.** The two roots are simple. Their implicit-function branches over a sufficiently small parameter neighborhood are separated by disjoint root disks. At all nearby E parameters their positive Jacobians make them selected. Since each such fiber has exactly two selected roots, these are all the selected roots.

**At a fold.** The two selected roots at the central parameter are also simple and positive. The same implicit-function argument supplies two separated selected branches and exhausts all selected roots at every nearby E point. It cannot be obstructed by the additional unselected critical root. Thus no branch need cross or continue the fold root itself.

For completeness, the fold's disappearing pair lies on the Omega side. The two selected simple branches remain present on both sides. Nearby interior parameters have exactly four roots, including one negative disk root. As parameters tend to the fold, neither additional root can tend to the two fixed simple roots, by local uniqueness. Both therefore tend to the fold root. Nearby exterior parameters have only the two continuing positive roots. Equivalently, the one-variable reduced quadratic germ creates a pair of opposite degrees on precisely the side containing the negative root. This reasoning also permits beta to vary.

**At a cusp.** Let c be the critical root and r the other, simple root at p_0. Choose disjoint isolating disks around c and r. After shrinking a full parameter neighborhood, every root lies in their union. Indeed a contrary sequence of roots outside the union has a bounded subsequence, whose limit would be a root of p_0 outside the two disks. The branch near r is unique in its disk after a further shrink, by the implicit-function theorem and the same compactness argument, and remains selected and positive. Since an E fiber has exactly two selected roots, exactly one selected root remains in the disk around c.

The latter selected root is continuous at p_0: any sequence approaching p_0 has bounded chosen roots, and every limit in the critical disk must equal c. To verify continuity throughout a local neighborhood, use the ordinary/fold argument at its regular selected points and this cusp argument at any cusp selected points. More explicitly, selected roots cannot converge to an unselected fold root, because the two regular positive roots at that fold already persist and exhaust the selected roots nearby. At an ordinary point or beta=0 all roots are selected; at a cusp both actual roots are selected. Thus the selected relation is sequentially closed over E, and isolating disks identify continuous local branches at all its points. This closes the possible gap between continuity only at the central cusp and a genuine covering trivialization on a neighborhood.

The two graph pieces over each such neighborhood are relatively open in S, as they lie in separated open root disks. Projection restricts to a homeomorphism on each graph. These are the required covering neighborhoods. All neighborhoods above are full neighborhoods in parameter C^2 before intersection with E, and root bounds were uniform there. The assertion therefore includes varying beta and is not merely a fixed-beta slice argument.

## 6 Star-shaped caustics and the exact topology of exterior phase charts

The normalized critical curve is

    q(t)=exp(2i*t)/4+exp(-i*t)/2
        =exp(-i*t)*(2+exp(3i*t))/4.

It never vanishes and 1/4 <= |q(t)| <= 3/4. The factor 2+exp(3i*t) stays in the right half-plane, so a continuous argument lift of q changes by exactly -2*pi in a full period. Direct differentiation gives

    d(arg q)/dt = 2*(cos(3*t)-1)/(5+4*cos(3*t)).

The denominator is at least 1, and the derivative is nonpositive, vanishing only at the isolated cusp parameters. Its integral on every nontrivial interval is strictly negative. Hence the argument lift is strictly decreasing, even though its derivative vanishes at cusps. The induced argument map from the critical circle to the direction circle is a continuous bijection and therefore a homeomorphism. Each ray from zero meets the boundary exactly once.

Since 0 is in the Jordan interior, this unique boundary intersection implies that the interior on each ray is exactly the interval from radius 0 up to that intersection. This establishes star-shapedness rather than assuming it from the visual deltoid shape.

For beta != 0 write the boundary as w=r_beta(v)*v, v in S^1. The inverse direction map above makes r_beta continuous in v. With the local beta normalization from Section 4,

    r_beta(v)=b^2*r_1(exp(-2i*theta)*v).

This proves joint continuity locally in every beta != 0. Different cube-root choices of theta parametrize the same physical critical curve and hence the same uniquely defined radial value. Set r_0(v)=0. The bound

    b^2/4 <= r_beta(v) <= 3*b^2/4

proves joint continuity also as beta tends to zero, uniformly over v. Thus r is a single global continuous function on C x S^1, despite the lack of a global cube-root phase choice.

Let I_1=S^1\{-1}, I_2=S^1\{+1}, and

    O_j={(beta,w): w != 0 and w/|w| in I_j},
    E_j=E intersect O_j.

Each O_j is open in C^2. Since (0,0) is not in O_j,

    E_j=O_j \ Omega,

so E_j is closed relative to the metric space O_j. It need not be closed in C^2, and the proof neither claims nor needs that stronger statement.

All points of E have w != 0: for beta != 0 the target zero lies in Omega_beta, and beta=w=0 was explicitly removed. Consequently E_1 and E_2 cover E.

Define K=(C x [0,infinity))\{(0,0)}. The map

    (v,(beta,t)) -> (beta,(r_beta(v)+t)*v)

is a homeomorphism I_j x K -> E_j. Its inverse is

    (beta,w) -> (w/|w|,(beta,|w|-r_beta(w/|w|))).

Star-shapedness gives nonnegativity of t. When beta != 0, r_beta(v)>0, including at t=0. When beta=0, deleting (0,0) from K enforces t>0. These facts ensure w != 0 throughout, so all formulas are defined and continuous, including the beta=0 boundary behavior.

K is contractible by

    (beta,t) -> ((1-s)*beta,(1-s)*t+s), 0 <= s <= 1.

For s>0 its second coordinate is positive; at s=0 it is the original allowed point. Thus this contraction never hits the removed origin and ends at (0,1). Every point of K has a sufficiently small relative ball avoiding the removed origin; that ball is a convex Euclidean ball or half-ball. Hence K is locally path connected. Each I_j is homeomorphic to R, so E_j is contractible, path connected, and locally path connected.

A covering over a path-connected, locally path-connected, simply connected base is trivial, by the covering homotopy/path-lifting theorem. Contractibility supplies simple connectedness here. Applying this to S restricted to E_j yields a continuous exact section s_j:E_j->C. No compatibility between s_1 and s_2 on their overlap is needed for an open-cover selection problem.

## 7 Why unbounded Tietze extension supplies valid open collars

The following elementary lemma isolates the key approximate step.

Let B be a metric parameter space for a continuous family of maps R^2->R^2, O an open subset of B, and A closed relative to O. Suppose s:A->R^2 is continuous, selects an isolated actual root at every point, and every selected root has nonzero local Brouwer degree. For every fixed epsilon>0 there are an open neighborhood V of A inside O and a continuous epsilon-approximate root selector on V.

Proof: metric spaces are normal, and the unbounded real-valued Tietze extension theorem extends the two coordinate functions of s from A to all of O. Let F:O->R^2 be the resulting continuous extension. Given p_0 in A, choose an isolating root disk centered at s(p_0) with radius rho<epsilon/3. Its boundary has no zero. On this compact boundary the norm of the defining map has a positive minimum, and parameter continuity gives a neighborhood of p_0 on which the straight homotopy from the old map to the new one remains nonzero there. The local degree persists and is nonzero, so every nearby parameter has an actual root inside this disk. Shrink the neighborhood so |F(p)-s(p_0)|<epsilon/3. Then F(p) is at distance less than 2*epsilon/3 from such a root. The union of these open neighborhoods over p_0 in A is the desired V. The same F works on every neighborhood, so there is no patching inconsistency on overlaps.

For the present family, apply the lemma with B=C^2, A=E_j and O=O_j. All selected roots have degree +1, including the critical cusp roots. Thus the exact sections yield continuous F_j on open sets V_j containing E_j with the required strict epsilon bound.

The Tietze theorem used here permits unbounded continuous real-valued functions on a closed subset of a normal space. A bounded-only extension statement would not be enough unless supplemented by its standard unbounded extension corollary. There is no boundedness assumption on s_j, no compactness assumption on E_j, and no assertion of a uniform-width geometric collar. Each p_0 may have its own root-isolation radius and parameter-neighborhood width; the error allowance epsilon is the same fixed number everywhere. The sets V_j are open in C^2 because their constituent neighborhoods were chosen inside the open sets O_j.

This distinction is essential: a degree-zero fold root would not enjoy the same persistence statement. The selected exterior relation was designed to avoid exactly that issue.

## 8 The third chart and continuity across the added origin region

Let R(beta,w)=|beta|+sqrt(|w|). Fix a continuous cutoff chi:[0,infinity)->[0,1], with chi=0 on [0,epsilon/4] and chi=1 on [epsilon/2,infinity). Define the open set

    U_0=Omega union {R<epsilon/4}.

On Omega put s_0=chi(R)*sigma. On the open origin region {R<epsilon/4} put s_0=0. On their overlap the two definitions agree exactly, so the open-set gluing lemma proves continuity on all of U_0. No extension of sigma to an unselected boundary root is being asserted.

On Omega where chi=1 the selector is exact. Where chi != 1, necessarily R<epsilon/2, and

    |s_0-sigma| <= |sigma| < |beta|/2 <= R/2 < epsilon/4.

On the additional small region, every actual root has modulus at most R<epsilon/4 by Section 2, and a root exists by degree. Thus the zero value is also within epsilon/4 of an actual root there. All inequalities needed for the requested strictly-less-than-epsilon convention are strict with room to spare.

Every parameter lies in Omega, in E, or equals (0,0). The first and last types lie in U_0. The second lies in E_1 or E_2 and hence in V_1 or V_2. Thus U_0,V_1,V_2 are three open sets covering C^2, each with a valid continuous approximate selector. Section 1 pulls them back to all R^6 isometrically in the root coordinates.

## 9 A lower obstruction that survives approximation

Assume there were one continuous approximate selector on all parameters. Restrict to alpha=beta=0 and to the circle w=L^2*exp(i*t), with L>epsilon and 0<=t<=2*pi. Let f(t) denote the chosen root-coordinate value. It is continuous and f(2*pi)=f(0). The actual roots are the two values +/-L*exp(i*t/2).

Consequently

    h(t)=f(t)/(L*exp(i*t/2))

lies in the union of the two open disks of radius epsilon/L<1 centered at +1 and -1. These disks are disjoint. Connectedness of the interval forces h to remain in one component, but periodicity of f gives h(2*pi)=-h(0), which lies in the other component. This contradiction proves N(epsilon)>=2.

The strict choice L>epsilon is indispensable: a tolerance covering both small roots could allow a constant selector. This argument neither relies on the source's exact-selection remark nor removes singularities from the domain of the proposed global selector.

## 10 Tolerance independence and quantifier audit

For lambda>0 the parameter dilation

    T_lambda(beta,w)=(lambda*beta,lambda^2*w)

is a global homeomorphism of C^2, and the fiber at T_lambda(p) is exactly lambda times the fiber at p. Given an epsilon_1 cover by U_i with selectors f_i, use T_lambda^{-1}(U_i) with selectors f_i(T_lambda(p))/lambda. The error is strictly less than epsilon_1/lambda. Taking lambda=epsilon_1/epsilon_2 gives N(epsilon_2)<=N(epsilon_1); interchanging the tolerances gives equality.

The result means: for each chosen positive epsilon there exists a cover by at most three open sets. The cover, cutoff, extensions, and neighborhood widths may depend on epsilon. It does not assert one cover and one set of selectors working for all positive epsilons simultaneously, which would force exact selection. It also does not restrict the coefficients to a compact set, require a positive distance from the discriminant, or use an error bound for polynomial residuals.

The quantifiers at a collar point are equally important: for each p_0 in E_j there exists an open parameter neighborhood such that every p in it has some actual root close to the single continuous extended selector F_j(p). The nearby actual root may depend on p and need not itself admit a continuous local branch on the full neighborhood. Nonzero degree, rather than a forbidden local exact branch across a cusp, supplies precisely what approximation needs.

## 11 Literal exact-selection caution

Under the literal all-parameter formulation, an exact continuous section on an open neighborhood of the zero parameter would restrict to a square-root section on a disk about w=0 in the alpha=beta=0 subfamily. Restriction to any sufficiently small nonzero circle gives the same sign contradiction as in Section 9 with zero error. Such a local section cannot exist. Therefore no open exact-section cover of the entire space can exist, even an infinite one, because some member would have to contain zero.

This is an elementary statement about that literal domain. It does not determine the source author's intended modified exact problem, establish a source correction for publication, or decide the approximate optimum. The present accepted partial theorem stands independently of that caution. In particular there is no inference that failure of an exact section at zero or a cusp forces three approximate charts.

## 12 Standard dependencies and what was actually established

The proof depends on the following standard results in their indicated forms:

1. The real implicit-function theorem with continuously varying parameters, at a root with nonzero real Jacobian determinant.
2. Invariance of domain for an injective continuous map between planar open sets, compact-to-Hausdorff embedding, and Jordan curve separation.
3. Planar Brouwer degree: boundary winding, homotopy invariance when the boundary stays nonzero, regular-root signs, finite-fiber additivity, nonzero-degree existence, and invariance under orientation-preserving local coordinates.
4. The covering-space lifting/triviality theorem for a path-connected, locally path-connected, simply connected base. The selected relation was proved to be a covering, including singular boundary targets, before this theorem was used.
5. Unbounded real-valued Tietze extension from a closed subset of a normal space, applied to each real coordinate. Metric normality and the correct relative closedness were checked.
6. Elementary connectedness, compactness, gluing on open sets, and continuity of a homeomorphism's inverse.

The independent checker verifies symbolic identities and selected exact special fibers. It is not a topology prover and is not used to replace Sections 3-8. No numerical sampling, generic-only assertion, catastrophe classification, or inherited exact-cover claim is needed for acceptance.

**Final disposition:** mathematically accepted partial result; no mathematical correction required; full problem unsolved by this packet; exact remaining task is to construct two global approximate charts or prove that every two-chart attempt fails. The original audit included authored checker code and verification metadata; this edition retains the complete mathematical audit and public verification metadata without distributing code or raw outputs. The original audit did not modify a remote repository or research queue.
