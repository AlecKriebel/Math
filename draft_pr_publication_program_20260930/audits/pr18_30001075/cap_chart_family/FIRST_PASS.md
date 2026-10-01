# Independent first-pass cap-chart audit

Prepared 2026-10-01 UTC. Frozen PR 18 / problem 30001075, head `99e403e85d38d92b021198c4a57bbad3cd8775ba`.

## Verdict and independence

**Universal cap-chart mechanism: passes independent analytic reconstruction. No central mathematical gap or counterexample was found.** The finite controls are corroborative only. The universal verdict is based on the derivations below, including the explicit bracket/self-map argument omitted from the candidate's abbreviated prose.

I read the frozen `CANDIDATE.md` and `source_record.json` first. Before this first-pass report and its seal, I did not read any historical review, historical verification code/results, root reconstruction, root verdict, or sibling conclusion. New exact controls were written from scratch using only Python's standard library and rational arithmetic. No author/reviewer implementation was imported. All work is confined to `cap_chart_family/`; no Git, canonical proof/queue edit, environment change, outreach, or paper action was performed. This is validation and does not consume the central attempt ledger.

The audited candidate has SHA-256 `b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252`; its source record has SHA-256 `b90fc595a14ea6522ec5d01bbb04fd3d0445362bc0a3257e2cc927f350f3afb5`. Line locators below refer to this exact `source_snapshot/CANDIDATE.md`, not the canonical working proof. The source file is 19,580 bytes.

## Exact claim and success criteria

For arbitrary pairwise disjoint convex subsets of R^3, a common tangent line must actually intersect each set and lie in a plane bounding a closed halfspace containing that set. The target is that the union of all such complete affine lines has Lebesgue outer measure zero. There is no smoothness, strict convexity, unique-contact, dimension-three, compactness, or closedness assumption in the final statement. The compact-case reductions must therefore preserve tangency and cover every lower-dimensional boundary case.

Lemma 1 is the primary target: after discarding lines contained in a planar body's affine plane, common tangent lines to two disjoint compact sets of affine dimension at least two must be covered by countably many Lipschitz images of open subsets of R^2 in line space. Individual images may contain extra lines. A merely finite, generic, smooth, or fixed-contact calculation would not establish this assertion.

I independently inspected the [OWR original](https://ems.press/content/serial-article-files/46191), printed p. 2552 / PDF page 76. Its tangency definition and Conjecture 4 match the audited claim. Conjecture 3 asks for containment in countably many 2-manifolds, which this audit does not assert. I inspected the complete contraction theorem in [Lebl, Basic Analysis, Theorem 7.6.2](https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/mit18_100af20_basic_analysis.pdf), printed p. 267, and the equal-dimensional Lipschitz image inequality in [the Stanford area-formula text, Theorem 1.2.2 and Corollary 1.2.3](https://math.stanford.edu/~ryzhik/STANFORD/STANF272-17/book-splitchap1.pdf), printed pp. 13–14. Cached PDF hashes and locators are in `primary_source_manifest.json`; the caches are ignored under `tmp/`. The thesis URL returned a retrieval error and is not used as evidence for this mechanism.

## Mechanism audit

| Route / mechanism | Independent evidence | Status | Exact remaining gap |
|---|---|---|---|
| Four-dimensional line coordinates and normalized gap | Direct support/projection derivation; exact support-difference controls | Verified | None |
| Strict hemisphere for all contact normals | Interior disk forces positive common direction | Verified even at corners | None |
| Tiny caps preserve normal cone and affine span | Convex-segment and affine-basis arguments | Verified | None |
| Own/cross motions are independent and diagonally dominant | Height interpolation and signed support differences; exact tiny-gap bases | Verified | None |
| Uniform nearby active normals | Compactness plus a strict support-gap margin | Verified | None |
| Roots, square self-map, contraction, parameter Lipschitz bound | Explicit brackets and comparison estimates below | Verified | Candidate could spell these out for readability |
| Countable cover when contacts move | Fixed-cap zero sets and second countability; a cap-miss control | Verified | Candidate could name the fixed-cap subset explicitly |
| Composition with rank restriction and area formula | Reconstructed density/contact argument and all dimensions | Consistent | Not a novelty/priority clearance |

### 1. Support gap, tangency, and signs

Candidate lines 35–73. Lines whose direction has nonzero z component are uniquely `(u+zv,z)`. Such charts cover affine line space with three ambient-axis choices; hence the space is second countable. Around one line an orthonormal change aligns its direction with z.

For fixed compact C, put `Z=max_C |z|`. For every unit n,

`|psi_n(u+du,v+dv)-psi_n(u,v)| <= |du| + Z |dv|`.

Thus the maximum over n is Lipschitz with constant at most `sqrt(1+Z^2)` in the Euclidean product norm. Existence of maxima and continuity in n follow from compactness, independently of support-function differentiability.

The projection `Q_v={x-zv:(x,z) in C}` is compact convex. Its support function is exactly `h_C(n,-n·v)`. If Q_v has interior, its normalized support-gap maximum is negative inside, zero on its boundary, and positive outside. The outside assertion follows from strict separation; inside, a disk about u gives a uniform strictly negative bound. At a boundary point a support line exists and attains zero. A support line of Q_v lifts to a plane containing the whole affine line, and membership `u in Q_v` supplies an actual contact. Conversely, a supporting plane containing `(u+zv,z)` has normal `(n,-n·v)` with transverse n nonzero, so normalizing n yields the gap zero condition.

The support-difference sign in (4) is correct. If the support summand at `(x,z)` changes by `-z n·dv`, the maximum's difference lies between its minimum and maximum changes. Subtracting this difference reverses those bounds, and adding `n·du` gives exactly the source's min/max of `n·(du+z dv)`. This holds for arbitrary increments and arbitrary affine dimension. A point at height 1 provides a negative control: reversing this sign gives -1 when the exact gap increment is +1.

### 2. Normal hemisphere and caps

Candidate lines 79–102. After aligning L_0, both projections have interior: this follows from affine dimension three, or from transversality when the set is planar. Since the line is tangent, 0 is a boundary point. Choose a disk with center w and radius r inside the projection. Every unit supporting normal n at 0 has `n·w+r <= 0`. Therefore `e=-w/|w|` and `alpha=r/|w|>0` give `n·e>=alpha` for **every** supporting normal, not just an arbitrarily selected one. Corners and nonsmooth contact sets are included. There need not be a uniform alpha across all lines; none is required.

Pairwise disjointness makes the selected contacts distinct. Reversing the z axis if needed gives heights s<t and d=t-s>0. Positive d need not be uniform across the global family. Pick a rational closed ambient ball D with contact a strictly in its interior and arbitrarily small diameter. Rational centers/radii are chosen in one fixed original Cartesian system. If `|c-a|<rho/4` and `rho/2<R<3rho/4`, the rational ball centered at c of radius R contains a in its interior and lies inside the ball of radius rho about a. Orthogonal rotation does not change this containment, so any desired height width follows. There are only countably many such choices; rotated-coordinate rationality is unnecessary.

For the cap C'=C intersect D, the supporting-normal cone at the entire aligned line is unchanged. One inclusion follows from C' subset C. For the reverse inclusion, a functional supporting C' at the line vanishes at a. If it is positive at p in C, it is positive at `(1-lambda)a+lambda p`; for small positive lambda that point lies in the interior ball neighborhood of a and hence in C', a contradiction. This works when L_0 intersects C in a segment, when a is at the endpoint of that segment, and when C is planar.

Affine dimension is also unchanged: choose an affine basis `a,p_1,...,p_k` in C. Short positive portions of all segments `[a,p_j]` lie in D and remain affinely independent with a. Thus the cap's affine hull equals that of C, and its planar projection is still transverse with interior. The ball must contain a **strictly** inside it. The exact negative control `C=conv{(0,0),(1,1),(-1,1)}` with ball centered at `(1,0)` of radius 1 puts a at the ball boundary: its cap has the additional -x support normal which the original set does not have.

### 3. Motions and nearby maximizers

Candidate lines 104–134. Evaluation at heights s and t is an invertible linear map from (u,v) to the pair of transverse displacements; its determinant has absolute value d^2. V_A evaluates to `(e_A,0)` and V_B to `(0,e_B)`, so they are independent even when e_A=e_B or e_A=-e_B. Adding perpendicular own directions at the two heights supplies a full four-coordinate basis. Its determinant has absolute value `1/d^2`, checked independently for equal, opposite, orthogonal, nearly parallel directions and tiny rational d. Small d worsens constants but does not invalidate a chart.

There is a uniform nearby-active-normal assertion for each fixed cap. To make its compactness argument quantitative, on the compact set of normals with `n·e <= alpha/2`, the gap summand at zero has maximum `-gamma<0`: none is a contact supporting normal. Uniform Lipschitz continuity makes their nearby values at most `-3gamma/4`, while any original contact normal has nearby value at least `-gamma/4`, after shrinking the parameter neighborhood. Hence every maximizer is in the good hemisphere. Planar transversality is an open condition and can be imposed on the same neighborhood.

For the A cap's heights `z in [s-epsilon d,s+epsilon d]`, its own coefficient `(t-z)/d` is at least `1-epsilon>1/2`. At an initial maximizing normal, `n·e_A>=alpha_A/2`, so (4) gives the positive own increment lower bound `m_A h`, where `m_A=alpha_A/4`. No derivative, unique normal, or continuous selection of normals is used. For the cross motion, `|(z-s)/d|<=epsilon` and `|n·e_B|<=1` for all normals, so each summand changes by at most `epsilon |h|`, and its maximum satisfies the same bound. The B estimate follows identically. The strict choice `epsilon<alpha_i/16` gives `epsilon/m_i<1/4`.

A long contact segment can destroy the own bound **without** localization: for a height z beyond t, `(t-z)/d` is negative. Clipping the entire set to a short height range around the selected contact is exactly what removes this obstruction. No assumption of point contact is hidden in the argument.

### 4. Explicit root domain and square contraction

Candidate lines 136–143. Let K_i be finite Lipschitz bounds for the residual parameters r in the chosen linear coordinates. Select delta>0 so the closed product square in a,b lies inside the good coordinate box. Then choose eta>0 so the residual ball is inside the box and

`K_i eta < (m_i-epsilon) delta/2` for i=A,B.

For `|b|<=delta, |r|<eta`, the source estimates give

`g_A(delta,b,r) >= (m_A-epsilon)delta-K_A eta > 0`,

`g_A(-delta,b,r) <= -(m_A-epsilon)delta+K_A eta < 0`.

Strict monotonicity in a and continuity give a unique root throughout that complete parameter domain, not merely an assumed branch. The analogous B brackets hold. Comparison at roots gives

`|rho_A(b,r)-rho_A(b',r')| <= (epsilon/m_A)|b-b'|+(K_A/m_A)|r-r'|`,

with the analogous inequality for rho_B. In particular, roots at `(0,0)` are zero and

`|rho_A(b,r)| <= (epsilon/m_A)delta+(K_A/m_A)eta < ((1+epsilon/m_A)/2)delta < 5delta/8`.

Therefore the square map is well defined and maps the closed square strictly into its interior. It is a contraction in the max norm with `kappa=max_i epsilon/m_i<1/4`. The square is a nonempty complete metric space, satisfying all hypotheses of the contraction theorem. Its unique fixed point p(r) obeys

`|p(r)-p(r')|_infinity <= max_i(K_i/m_i)/(1-kappa) |r-r'|`.

The resulting graph is Lipschitz on an open residual ball. Within a suitably shrunk open product neighborhood, every simultaneous zero is this unique fixed point; by the projection criterion these are exactly the common tangent lines to the fixed caps there. This is a routine rigorous expansion of the source paragraph. No nonsmooth implicit-function theorem or unverified differentiability is substituted.

### 5. Countability with moving contacts

Candidate line 145. A covering of the **original** tangents by arbitrary neighborhoods would be insufficient if the associated graph only represents cap tangencies. This danger is real: for `C=[0,1]x[-1,1]x[0,10]`, L_0 is the vertical x=y=0 line and has an entire contact segment. The lines `L_theta=(theta(z-10),0,z)`, theta>0, converge to L_0 and are tangent at height 10. They miss every sufficiently small cap selected near height 0.

The candidate uses the correct different quantifiers. For a fixed rational cap pair P, let T_P be the common tangent lines to those **same** caps at which the good-height/good-normal construction is available for them. For each L in T_P, let U_L be its open line-space neighborhood and Gamma_L its graph of the zero equations of these same caps, with `T_P intersect U_L subset Gamma_L`. Second countability gives a countable subcover of T_P by the U_L. Any point of T_P in a selected neighborhood is a tangent of the same caps, so belongs to that selected graph even if its own contacts differ. Taking the union over countably many rational cap pairs yields a countable graph cover. Every original retained tangent belongs to at least one T_P by the earlier contact-localization construction. Thus the proof does not apply Lindelof to unrelated zero sets. Naming T_P and its zero-set inclusion explicitly would improve readability, but the required content is already present in line 145.

## Composition with the rest of the proof

Candidate lines 21–29 and 147–243. Closing arbitrary convex sets can destroy pairwise disjointness, but the preliminary choice of pairwise disjoint rational balls makes the resulting closure caps compact and disjoint regardless of overlap of original closures. Every original supporting plane remains supporting for the closure and for the cap containing its selected contact. Hence the original locus is covered by countably many compact-case loci. Empty original sets give no common lines and are vacuous.

In each Lipschitz two-parameter graph, the selected tritangent parameter set is Borel: compact contact points and unit supporting-plane normals have subsequential limits witnessing limiting tangency. The excluded planar-contained and identical interval-support-line conditions are closed. At a density point which is also a differentiability point of the graph map, every parameter direction h can be approximated by points of E at `q_0+tau h+o(tau)`. A proportional-radius hole would contradict density one.

If `Du+z_i Dv` had rank two at a full-dimensional contact, move in a parameter direction whose first-order transverse displacement points toward an interior-ball center. Convexity supplies an interior ball of radius proportional to tau around the corresponding convex combination with the contact. A nearby tangent line would pass through its interior, a contradiction. For a planar set and transverse line, its smooth intersection with the affine plane has the analogous relative-interior displacement and gives the same contradiction; any supporting plane through a relative interior point must equal that affine plane. For an interval, the intersection equation implies the derivative image is parallel to its transverse direction; its denominator remains nonzero near the nonidentical intersecting line. For a point, its incidence equation makes the derivative zero.

The three heights are distinct because the sets are disjoint. Hence the degree-at-most-two polynomial `det(Du+z Dv)` vanishes identically. On bounded graph and height patches the sweep `(q,z) -> (u(q)+zv(q),z)` is Lipschitz and its absolute three-dimensional Jacobian is zero almost everywhere on `E x [-M,M]`. The exceptional q set has zero product measure. The inspected area-formula image inequality applies to measurable subsets; it requires no injectivity and no open tritangent set. Bounded patches and then countable unions produce outer measure zero. The point and interval chart cases are elementary two-parameter incidence families with the same rank argument. This composition is consistent with the verified Lemma 1 and does not require all three bodies to be full dimensional.

The deduction yields a null set, not a countable smooth-manifold cover. No inference about worldwide priority is justified by this audit.

## Fresh finite controls and deliberate falsifications

`independent_controls.py` completed at 2026-10-01T16:57:19.736445+00:00. All **34,489 exact assertions in 25 categories** passed. Results are in `independent_results.json`. These include 4,200 signed support-difference assertions, 2,352 full-basis determinant assertions, 6,384 own-motion inequalities, 18,816 cross-motion inequalities, exact nonsmooth prism roots, tiny contact gaps down to 10^-12, aperture alpha down to 10^-12 in the bracket tests, and fixed ambient rational balls after rotation with d=10^-15.

The nonsmooth examples include prisms with opposite exposed faces, whose nearby gap functions are `a-h|a+b|` and `b-h|a+b|`, and orthogonal prisms with residual root `h r/(1+h)` for r>=0 and `-h r/(1-h)` for r<0. These examples exhibit actual contact segments and nondifferentiable root dependence. Deliberate negative controls detect reversed support signs, contacts on a cap-ball boundary, unlocalized distant heights, missing projection interior, and changing original contacts which miss a selected cap. The exact direct-function tests do not establish that an arbitrary continuum of maximizing normals satisfies the good hemisphere; that assertion was proved analytically above.

## Must-fix versus optional changes

**Must fix before a clean publication of this exact text: two notation defects, with no effect on the mathematical mechanism.** Line 57 prints `u:=u` where simply `u` is intended. More seriously, line 190 uses `u(q):=u(q)+z_i v(q)` while line 194 refers to undefined `nu(q)`. Introduce a distinct `nu(q)=u(q)+z_i v(q)` in (13) and use it consistently. This restores the intended interval argument and prevents accidental overwriting of the original intercept function.

**Optional exposition:** spell out the root sign brackets/self-map estimates above; name the fixed-cap set T_P and the inclusion into each selected graph; clarify that no global uniform lower bound on alpha or d is needed. None of these optional changes transfers the central difficulty to another unsupported claim.

**Strongest verified result:** the universal Lemma 1 mechanism is analytically justified under precisely the compact/disjoint/dimension/transversality hypotheses stated, and it composes correctly with the density/rank/area-formula steps to the arbitrary-convex-set outer-null conclusion. **Exact remaining gap:** no central proof gap found; notation cleanup remains in the frozen text, and external novelty/priority clearance remains outside this audit phase.
