# Independent geometric adversarial audit of PR 28

Exact head: `90a81313f3f65a7914fb6d5a9950fa087ea7467e`. Target: 7000019 / Ghomi Problem 4.3. This audit was reconstructed independently and sealed in `EARLY_SEAL.md` before reading the author's proof, old review, old checkers, or old receipts. All work created by this family is confined to this directory. No external communication, Git mutation, candidate write, queue write, PR write, publication write, package installation, or foreign-source redistribution occurred.

**PASS for the stated smooth convex partial theorem, with no mathematical correction required.** The verified result requires a compact convex body with nonempty interior, boundary class C²,α with 0<α<1, a single strip area constant across every admissible orientation and position, and 0<h<2rin. It is a consequence of an elementary orientation average and Reichel's classical electrostatic rigidity theorem. This audit certifies neither novelty nor full solution of the intended fixed-width problem. The gaps are the range h≥2rin and nonsmooth convex boundaries.

## Source target and exact assumptions

[Ghomi's survey](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), revised September 2, 2019, places Problem 4.3 on printed p.12 under the heading on area and volume of convex surfaces. Its displayed wording says closed surface, a fixed distance h below the diameter, and a constant area whenever the two planes intersect the surface. It does not explicitly put convexity or h>0 into that display. Parallelism follows from a positive distance between entire planes; nonparallel planes have distance zero. The positive-width convex intended target is independently established by [Ghomi's own 2017 formulation](https://mathoverflow.net/questions/283109/converse-of-the-archimedean-property-of-the-sphere): its definition is the boundary of a compact convex set with interior points, the diameter is extrinsic, and 0<h<d is explicit. Tangent intersection is allowed. The early seal records the literal displayed target before interpreting it.

The distinction is substantive. Allowing h=0 in the abbreviated display creates a trivial degeneration on ordinary smooth surfaces; allowing disconnected nonconvex surfaces creates the nested-sphere example proved below. Neither supplies a solution to the intended convex, positive-width target. The source's historical open description is not evidence of current worldwide status. The original package correctly makes no priority claim and keeps the queue unsolved with two of five original attempts used.

[Kim–Kim, arXiv:1208.5361](https://arxiv.org/pdf/1208.5361), pp.1–4 and Proposition 2/Theorem 3, defines cap-area hypotheses for all sufficiently small positive heights. Its curvature mechanism, Lemma 8 and proof on pp.5–7, uses a limit as the height tends to zero. No such family of heights follows from a single fixed h. This primary body was read as a quantifier control, not substituted into the proof.

## Universal geometric admissibility and positive caps

Write S=∂K, σ=H² restricted to S, M=σ(S), and for a unit vector u let

\[
 a(u)=\min_{x\in K}u\cdot x,\qquad b(u)=\max_{x\in K}u\cdot x,
 \qquad w(u)=b(u)-a(u).
\]

A plane u·x=s intersects S exactly when a(u)≤s≤b(u). At a support value this is the nonempty support face. At an interior value its section with K contains a relative interior point; a boundary point of the bounded planar section belongs to S. Such an interior point can be obtained by taking an appropriate strict convex combination of an extreme point and an interior point of K. Therefore two h-separated planes are admissible exactly for t∈[a(u),b(u)−h]. The interval is empty for w(u)<h, a singleton for w(u)=h, and has positive length for w(u)>h. This characterization includes both endpoints and tangent planes.

Every cap {y∈S:u·y>s} with a(u)<s<b(u), and its lower counterpart, has positive H² measure. To justify the measure step, choose c with B(c,r)⊂int K. Radial projection from c is a homeomorphism of S to the unit sphere, with Lipschitz constant at most 2/r on S. A nonempty cap is relatively open; its projected image is a nonempty open part of the unit sphere and has positive area. The Lipschitz area inequality then forces the original cap to have positive H². Convex boundaries also have finite area, for example by their finite local Lipschitz atlas. This prevents replacing positive-area caps with merely nonempty sets.

w is continuous because the compact body's support functions are Lipschitz in u. It obeys max w=d: projection distances are at most d, and the direction of a pair of diameter-realizing points gives equality. If some w≤h while d>h, a path in S² from that direction to a direction with width d crosses a direction v with w(v)=h. Its sole closed strip contains S, so the global constant C equals M. In a direction u with w(u)>h, choose t=a(u)+(w(u)−h)/2. The strip is strictly within the support planes and omits nonempty open caps of positive area, so its area is less than M. Contradiction. Hence

\[
 0<h<d\quad\hbox{and the global strip identity}\quad\Longrightarrow\quad
 \min_{u\in S^2}w(u)>h.
\]

The global constant and tangent-inclusive intersection convention are exact premises. This proof is universal over all orientations and all admissible offsets; no sampling supplies it.

An additional endpoint control is useful. A plane strictly between support levels cannot contain a positive-area patch of S: its intersection with S is contained in the boundary of a planar convex section, which has planar area zero. A support plane can contain a positive-area face. If the strip condition holds and w>h, let t decrease to a(u) through interior values. Dominated convergence loses exactly the lower support-face area while the upper level a(u)+h has zero area. Equality of all closed-strip areas therefore forces that support-face area to vanish. Apply the reflected argument at the upper support face. This endpoint deduction does not assume all convex surfaces have area-free support faces; it follows from the strip hypothesis.

The exact cube control in the new script catches the false area-free endpoint shortcut. For K=[−1,1]³ and h=1, four vertical faces contribute area 8. At t=−1 the lower support face adds 4, and at t=0 the upper support face adds 4; the strictly interior strip t=−1/2 has area 8. Thus the closed-strip areas are 12, 12, and 8 respectively. For h=2 the single support strip has total area 24. This cube is a control, not a claimed constant-strip surface.

## Tetrahedron: exact all-direction obstruction to the inradius shortcut

Let T have vertices v₁=(1,1,1), v₂=(1,−1,−1), v₃=(−1,1,−1), v₄=(−1,−1,1). Its complete edge-difference set is 2(±eᵢ±eⱼ), i<j. Therefore for every direction u, if a≥b≥c≥0 are the sorted absolute coordinates of u,

\[
 w_T(u)=\max_{i,j}u\cdot(v_i-v_j)=2(a+b).
\]

If |u|=1, then (a+b)²−(a²+b²+c²)=2ab−c²≥0, since a≥b≥c. Thus w≥2, and u=e₁ attains equality. The exact minimum width is 2. Every pair of distinct vertices has squared distance 8, so d=2√2.

The halfspaces are vᵢ·x≥−1, because each face opposite vᵢ has that equation, its other three vertices lie in it, and vᵢ lies on the correct side. All |vᵢ|=√3 and Σᵢvᵢ=0. At the origin all four face distances equal 1/√3. At any possible center x the average signed face distance is

\[
 \frac14\sum_i\frac{1+v_i\cdot x}{\sqrt3}=\frac1{\sqrt3}.
\]

The minimum face distance is at most this average; an inscribed ball cannot have larger radius than that minimum. The origin achieves it, so rin=1/√3. Hence h=3/2 satisfies h<2=min w<d but h²=9/4>4/3=(2rin)². This refutes the proposed general implication min w>h⇒h<2rin. It does not show a tetrahedron satisfies the strip property.

Boundary regularity and this numerical geometric gap are separate issues. The tetrahedron refutes a shortcut formulated for general convex bodies; it is outside the C²,α partial theorem. There is no claim that nonsmoothness itself explains every possible large-width gap, and no exact-identity-preserving smooth approximation is assumed.

## Centered strips, kernel average, and threshold

Put δ=h/2. The set of centers at which every orientation yields an admissible centered strip is

\[
 F_\delta=\{x:a(u)+\delta\le u\cdot x\le b(u)-\delta\ \forall u\in S^2\}
 =K\ominus\overline B_\delta.
\]

The equality follows from the support-halfspace representation of K: x+\overline Bδ⊂K holds exactly when u·x+δ≤b(u) for every u, with the lower inequality supplied by −u. For x in the open set E={dist(x,S)>δ}, a slightly larger ball around x lies in K. Both centered planes cut the body at strict interior levels and hence intersect S. This checks the surface-intersection requirement, not merely solid intersection.

For fixed z≠0, the signed cosine u·z/|z| has uniform distribution on [−1,1] when u is uniform on S². Thus the fraction of directions with |u·z|≤δ is

\[
 \min\{1,\delta/|z|\}.
\]

At |z|=δ the fraction is exactly one; for |z|<δ it remains one rather than the invalid value δ/|z|>1. Ordinary direction-area measure has total 4π, so its integral is 4π times this fraction. For x∈E every y∈S satisfies |x−y|>δ. Tonelli gives

\[
 C=\delta\int_S\frac{d\sigma(y)}{|x-y|}=\delta U(x).
\]

There is no signed or conditionally convergent integral. The kernel and all local derivatives are uniformly bounded on each compact subset of int K separated from S. U is harmonic there, and int K is connected. h<2rin gives a center with distance >δ and hence a nonempty open E. Harmonic real analyticity then extends U=C/δ from E to the entire interior.

At h=2rin, Fδ can collapse to one point or a lower-dimensional set; E is empty. For the unit ball, h=2 gives F₁={0}. If h>2rin even Fδ is empty. A harmonic function may be constant on a plane without being constant in its domain: x↦x₁ is zero on x₁=0. Therefore an arbitrary lower-dimensional center set cannot replace the open starting set. The exact kernel outside E is the truncated kernel min(1,δ/r), and treating it as δ/r everywhere is false. These two rejected mutants identify the precise route failures. This does not prove the large-width target false.

## Primary Reichel mapping and nonsmooth separation

[Reichel 1996](https://ems.press/content/serial-article-files/34877), DOI 10.4171/ZAA/719, printed p.622, was inspected as pixels as well as extracted text. It assumes a bounded C²,α domain G with connected exterior and defines equilibrium distribution by constancy inside G of the single-layer potential. For dimension three its fundamental solution is 1/(4πr). The electrostatic conclusion states that only a ball can carry a constant equilibrium surface density. The reduction and exterior proof were read through §§2 and 4, printed pp.622–630. Theorem 1 on p.625 supplies radial symmetry under its regularity, elliptic, boundary, and exterior conditions.

Take G=int K. Convexity gives boundedness and connected exterior: from a point c in int K every exterior point can be moved radially away from c to a surrounding sphere while remaining exterior; the sphere connects all such rays. The boundary is the assumed C²,α surface. The density is identically one and positive; Ψ=U/(4π) is constant in G. In the exterior, Ψ is harmonic, positive, tends to zero at infinity, and is less than its boundary value by the maximum principle. The constant interior derivative is zero, so the single-layer jump relation gives exterior normal derivative −1 when the normal points out of G. Reichel's g=1, f=0 case has the required ellipticity and monotonicity; the stated regularity supplies the boundary traces. This is an exact hypothesis match, not a theorem about arbitrary Radon measures or arbitrary disconnected shells.

The averaging and harmonic interior calculation themselves only require the finite boundary measure and the geometric open center set, so they do not manufacture smoothness. Removing C²,α would require an appropriate extension of the imported rigidity statement or another argument. Approximation alone does not preserve the exact strip identity. No such extension is supplied by the original package or this audit.

## Sphere converse: all orientations, positions, endpoints, and limits

On a radius-R sphere centered at c, rotate any u into the vertical axis. Parametrizing by longitude θ and height s gives the surface area element R dθ ds. Consequently the pushforward density is 2πR on [u·c−R,u·c+R], with no endpoint atoms. Every admissible t in [u·c−R,u·c+R−h] has strip area C=2πRh, including both tangent endpoint choices. M=4πR², so C/M=h/(2R). Spherical symmetry makes the interior Newton potential radial and harmonic; regularity at the center forces it constant, and at the center U=4πR. This agrees with C/δ=4πR.

As h tends to zero through positive admissible values, C/h=2πR stays fixed. As h increases to 2R, C approaches the total sphere area and the admissible interval contracts to the support strip. h=2R itself is excluded by the strict source h<d, though the limiting formula remains consistent. Neither limit licenses replacing a single fixed-width hypothesis by all widths.

## Nested spheres: whole-interval classification including inner tangencies

For two concentric spheres R>r>0, any plane intersecting the union has offset in [−R,R] relative to the common center; the outer sphere meets every such plane. Hence both h-separated planes meet exactly when 0<h≤2R and t∈[−R,R−h]. Rotation invariance handles every orientation. The area divided by π is

\[
 2Rh+2rL_r(t),\qquad L_r(t)=\max(0,\min(r,t+h)-\max(-r,t)).
\]

The max/min switches occur only at t=−r, r, −r−h, r−h, and the outer-domain endpoints. Between successive switches Lr is affine; at a switch the formula is continuous. This is a complete all-region description, including inner tangency points. The new checker records every exact affine cell for six rational configurations and confirms the endpoint formulas.

For R+r≤h<2R, every admissible strip includes [−r,r]: t≤R−h≤−r and t+h≥−R+h≥r. Then Lr=2r and total area is 2πRh+4πr². At the threshold h=R+r, the t=−R strip touches the inner sphere at its upper pole, and t=−r=R−h touches at its lower pole. A sphere has zero-area tangent points, so these endpoint choices still contribute the full inner area. The fresh R=2,r=1,h=3 example has area 16π at every admissible offset, including these two touches.

This is also the exact threshold for constancy. If h≤R−r, t=−R has zero inner overlap while the centered strip t=−h/2 has overlap min(h,2r)>0. If R−r<h<R+r, the first overlap is h−R+r, strictly below min(h,2r): when h≤2r its difference from h is R−r>0; when h>2r its difference from 2r is R+r−h>0. Thus the areas differ in both remaining regions. Equality h=R−r has zero support overlap and positive central overlap. This proof covers all h, not merely a grid.

The author's R=2,r=1/2,h=3 configuration falls inside the constant region. Its total area is 12π+π=13π, h<d=4, and every t∈[−2,−1] contains the inner sphere. The union is a smooth disconnected closed surface, but not the boundary of a convex body. It diagnoses the abbreviated PDF wording and is excluded by the primary intended convex target. No target counterexample credit is appropriate.

## Projection density: the remaining quantifier gap

For any direction u where the area pushforward has an integrable density fu on interior support levels, define Fu(t)=∫t^(t+h)fu(s)ds. Its almost-everywhere derivative is fu(t+h)−fu(t). Thus constant strips imply fu(t+h)=fu(t) for almost every t∈(a(u),b(u)−h), independently for every u. The constant area is shared across all u. This is finite-support sliding-window periodicity; it is not global periodicity past the support or pointwise equality at atoms. The author's qualified density statement is correct.

One h-period does not force a density constant. The author's cosine density is positive and gives every contained h-window area h. A materially different fresh control uses the continuous periodic quadratic spline

\[
 g(s)=1+\tfrac12(s^2-s+1/6),\quad 0\le s\le1,
 \qquad f(t)=g(\{t/h\})\ \text{on }[0,3h].
\]

The values match at period endpoints, its minimum is 23/24 and endpoint value 13/12, and its primitive is G(s)=13s/12−s²/4+s³/6. For every phase s∈[0,1], the unit-period integral is G(1)−G(s)+G(s)−G(0)=1. Therefore every contained length-h window has area h. Yet two half-width windows have areas h/2 and 31h/64. This rejects both constant-density and freely-variable-width substitutions. Such a one-dimensional density is not asserted to be the compatible family of area pushforwards of any convex surface; that missing all-direction condition remains substantive.

## Exact source binding, replay, and disposition

`INPUT_AND_REPLAY_RECEIPT.json` binds all 17 original snapshot bodies byte-for-byte to their exact-head Git blobs and declared SHA-256 values. It also checks the complete 18-path diff against the manifest, including the sole queue transition from queued 0/5 to unsolved 2/5. All proof, review, scope, provenance, attempt, old receipt, and script bodies were read after sealing. Original and sealed files were never modified.

The original `verify.py` and old `review/submitted_verify.py` replayed unchanged with 1,056 assertions each. Old `review/independent_checks.py` replayed unchanged with 266 controls. Every full generated receipt equals its saved original receipt. All scripts were copied into ignored `tmp/original_replay`, and the existing explicit `/usr/bin/python3` with SymPy 1.14.0 was used; no dependency was installed. `geometric_controls.py` imports no original code and passes 40 fresh exact controls while rejecting 11 false mutants. Its finite and cell computations supplement the universal arguments above; they do not prove Reichel's external theorem or solve the unresolved full problem.

Downloaded PDF/HTML, extracted text, renders, and replay byproducts remain only in ignored tmp. Primary PDF bytes independently match the original provenance hashes. The self-exclusion manifest binds every first-party file in this audit directory except the manifest itself, with an explicit ignored-foreign-material rule.

The package's mathematical scope is accurately partial. Preserve the strict inradius threshold, C²,α boundary, convex-body definition, global strip constant, tangent-inclusive convention, two original attempts, unsolved queue state, and no priority credit. Root integration and a fresh complete gate are outside this family's write authority.
