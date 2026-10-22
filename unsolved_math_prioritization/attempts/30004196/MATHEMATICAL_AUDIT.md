# Independent audit: necessary geometry of an ancient oval limit

Problem 30004196 / OWR-17130-012. Audit date: 10 October 2026 UTC.

Public proof-only edition. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## 1. Verdict and exact acceptance boundary

**ACCEPT AS A BOUNDED PARTIAL RESULT.** No mathematical error or acceptance-blocking gap was found in the frozen candidate. Acceptance is conditional on the explicitly imported mean-curvature-flow theorems, whose applicable statements and relevant proof mechanisms were checked against primary sources. It is not a new proof of those deep theorems, a formal proof certificate, an external peer review, or a novelty certification.

The original single-flow, later-time realization question remains **OPEN in this work**. The candidate neither constructs the required flow nor excludes it in the full original class. Its main arrival-time theorem concerns smooth closed embedded **globally mean-convex** initial surfaces in R^3. The original question also allows non-globally-mean-convex initial surfaces. This difference is stated in the candidate and retained here.

Accepted content:

1. The fixed-flow moving-center escape lemma, under its stated compactness and tangent-flow monotonicity assumptions.
2. Spherical-extinction recentering of an oval limit, and distinct spherical extinction points converging to a cylindrical point in the closed mean-convex surface class.
3. Asymptotic axial approach, subquadratic time offsets, smaller oval scale, and the exact operator-norm Hessian gap 1/2.
4. The conditional Hessian-continuity exclusion and the conditional nondegenerate-neck exclusion.
5. The complete infinite scalar bump construction, including global Lipschitz regularity of its gradient and twice differentiability at its accumulation point.
6. The limited construction-route conclusions: the peanut theorem has varying flows; Miura's example has an initially singular point; unchanged shrinking curved patches cannot be implanted in a compact C^2 initial surface.

No author-file correction is required for this acceptance. None of the above is a sufficient condition for realizing an ancient oval, and none justifies replacing a moving center with a fixed tangent center. There is no claim that all cylindrical singularities are nondegenerate or that the arrival-time Hessian is always continuous.

## 2. Distributed proof identity and verification scope

This edition binds the distributed [PROOF.md](PROOF.md): 21,355 bytes, SHA-256 `85a38edad9e22aacefabd36303a5f005ab8c79be048c10fa7f84e60b6d6d17c0`. The complete accepted mathematical proof and all substantive audit findings are preserved. Edition changes are editorial and introduce no new mathematical correction. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit; [MANIFEST.json](MANIFEST.json) hashes the other seven members of this eight-file edition.

The independent audit read the entire original proof and checked its status and README for consistency. During that audit, candidate verification was independently run in ordinary and optimized Python modes with the external original-manifest pin and source checks enabled. Both passed. A complete local before/after inventory verified that the author's tree was not changed during the audit. These are historical verification results, not new mathematical-program executions performed for this edition.

Edition preparation rechecked the frozen accepted authored payload and its external audit seal. It did not rerun the original mathematical programs, rehash source PDFs, retrieve new scholarly sources, inspect source text or conduct a new literature search. The complete analytic arguments stand independently of omitted programs, generated certificates, datasets and raw outputs. Imported PDE theorems remain explicit dependencies.

## 3. Original source and imported hypotheses

During the independent audit, all nine source PDFs listed by the candidate were retrieved from their primary public URLs on 10 October 2026. Every retrieved PDF matched both the candidate's recorded byte count and SHA-256 hash. The historical retrieval times, exact versioned URLs, match results, and precise text and visual inspection locations are retained in [SOURCE_METADATA.json](SOURCE_METADATA.json). Source PDFs, extracted text and rendered pages are not distributed.

### 3.1 Original question

The contribution in [Oberwolfach Report 34/2019](https://ems.press/content/serial-article-files/46813), PDF pages 40–42, begins with smooth closed embedded surfaces in R^3, discusses both mean-convex and general initial surfaces, and places the later-singularity question in the footnote on PDF page 41, printed page 2073. That page was inspected visually. The candidate's broader original-class interpretation is faithful. A full negative answer cannot follow from the mean-convex arrival-time argument alone. Beyond singularities, a legitimate specified continuation is needed; the candidate preserves the canonical outer/inner-flow distinction.

### 3.2 CHH: accumulation and compact component extraction

[Beomjun Choi, Haslhofer, and Hershkovits, arXiv:1910.02341v1](https://arxiv.org/pdf/1910.02341v1), pages 1–4, were checked, with pages 2–3 also inspected visually. Theorem 1.3 and Corollary 1.4 concern a smooth closed embedded mean-convex surface. Proposition 2.2 uses the compact strictly convex oval slice to obtain a genuine convex component and then spherical extinction centers. The proof of the global theorem identifies an accumulation point as cylindrical. Theorem 1.5 is a local result for inward/outward neck singularities with the corresponding outer/inner flow. Its neck and continuation hypotheses must be retained in broader applications. The candidate does so. The relevant first author is Beomjun Choi, distinct from Kyeongsu Choi in the OWR contribution.

### 3.3 CM: arrival time and actual gradient differentiability

[Colding and Minicozzi, arXiv:1501.07899v3](https://arxiv.org/pdf/1501.07899v3), especially Theorem 0.2, Corollary 1.12, and Proposition 2.2, were checked. The setting is a closed smooth mean-convex initial hypersurface and its compact swept-out domain. Corollary 1.12 supplies C^{1,1} regularity and identifies the singular and critical sets. Proposition 2.2 derives gradient difference quotients and the tangent-cylinder Hessian; pages 7–8 were inspected visually. In R^3 the cylinder gives diag(-1,-1,0), up to rotation, while the sphere gives -I/2. The candidate correctly uses surface dimension two, rather than ambient dimension three, in this normalization. No Hessian-continuity conclusion is imported.

### 3.4 SWX: the extra nondegeneracy condition

[Sun, Wang, and Xue, arXiv:2501.16678v1](https://arxiv.org/pdf/2501.16678v1), introduction, Theorem 1.1(i), and Corollary 1.3 were inspected, including a visual check of page 3. The flow in Theorem 1.1 is a unit-regular cyclic mod-2 Brakke flow on a time interval extending to both sides of the point. Nondegeneracy means the full-rank quadratic normal-form condition stated before the theorem. Part (i) gives a two-sided spacetime neighborhood with no other singularity. A cylindrical tangent alone does not establish this condition. The candidate's Corollary 3.3 is valid with the specified hypotheses, not a universal neck-exclusion theorem. Definitions of nondegeneracy from other papers are not silently substituted.

### 3.5 Construction-route and current-scope sources

- [Angenent, Daskalopoulos, and Sesum, arXiv:2512.05077v2](https://arxiv.org/pdf/2512.05077v2), revised 31 August 2026: Theorems 1.3–1.4 and Section 10, PDF pages 52–54, were checked; pages 4 and 53 were inspected visually. The theorem applies to the stated perturbation families of a 4-peanut. The flow varies with the sequence index. Section 10 starts with members whose first singularity is spherical and uses their earlier convexity. It supplies no simultaneous infinitely many episodes in one fixed flow.
- [Miura, arXiv:1411.6249v4](https://arxiv.org/pdf/1411.6249v4), dated 30 January 2016: pages 1–3, including Theorem 2.1, were checked; page 3 was inspected visually. The initial connected compact axisymmetric hypersurface is smooth except at one point. The exhibited singular epochs accumulate toward the initial time. This is not smooth initial data of the original class.
- [Haslhofer's author manuscript](https://www.math.toronto.edu/roberth/papers/haslhofer_icm2026.pdf) is dated 1 October 2025 on its first page. Pages 15–16 retain Problem 5.5 and the oval/accumulation discussion. The [published ICM 2026 chapter](https://epubs.siam.org/doi/10.1137/25M1803383) was independently checked and still presents this selfsimilarity problem as open. Its basic properties and Theorem 1.1 also support the compact convex evolution and enclosing-sphere normalization used here. This is a bounded literature/status check, not proof of absence of every later or unindexed result.
- [Choi, Du, and Zhu, arXiv:2504.09741v1](https://arxiv.org/pdf/2504.09741v1), pages 1–4: the relevant scope is classification of ancient solutions with specified noncollapsing and cylindrical-asymptotic hypotheses. It does not produce one smooth initial surface realizing an oval as a later-time blowup.
- [Sun and Xue, arXiv:2609.19390v1](https://arxiv.org/pdf/2609.19390v1), pages 1–5: stability and perturbation theorems do not make every existing cylindrical singularity nondegenerate. In particular, the denseness theorem has a type-I hypothesis. This manuscript is not a dependency of the candidate's main theorem. Its arXiv version date is 16 September 2026, while the PDF also prints a manuscript date of 18 September 2026; these dates are not interchangeable.

The long external PDE proofs are imported. No claim is made to have independently reproved the entire peanut perturbation analysis, the arrival-time theorem, Brakke regularity theory, or the nondegenerate-neck isolation theorem. An attempted extra opening of Huisken's 1984 DOI failed; no direct inspection of that original paper is claimed. The verified CHH mechanism and Haslhofer exposition suffice to identify the standard convex-flow dependency actually used.

## 4. Mathematical audit of the escape lemma

Proof Section 2 uses the convention M[X,lambda]_s = lambda(M_{t+s/lambda^2}-x). Set

a_i = lambda_i(x_i-x_0),  b_i = lambda_i^2(t_i-t_0).

Direct substitution gives

M[X_0,lambda_i]_s = a_i + M[X_i,lambda_i]_{s-b_i}.

Both signs are correct. If the nonnegative sum lambda_i|x_i-x_0| + lambda_i^2|t_i-t_0| does not tend to infinity, a subsequence has both terms bounded. A further subsequence has a_i→a and b_i→b. For s<min(0,b), the oval time s-b is negative; convergence on compact negative-time intervals identifies the corresponding fixed-center limit as a+O_{s-b}. Compactness supplies the same subsequential tangent flow, and fixed-center monotonicity makes it a backward homothetically shrinking flow on negative times.

On this common past interval its slices are compact and strictly convex. The compact convex shrinker is spherical: equivalently, apply the standard convex-flow round-point theorem to a homothetic compact solution, whose rescaled shape cannot change. Smooth forward uniqueness propagates the spherical solution from a common slice. Because agreement holds on an entire past half-interval, not merely one unanchored slice, the ancient oval cannot have a nonspherical earlier part hidden before that interval. This contradicts its prescribed nonselfsimilarity.

Thus **every bounded subsequence is excluded**, which proves divergence to infinity, not merely unboundedness. Writing A=lambda_i|x_i-x_0| and B=lambda_i sqrt(|t_i-t_0|), boundedness of A+B^2 is equivalent to boundedness of max(A,B). Applying this to subsequences proves the stated parabolic-distance version.

Limits here use one fixed underlying flow. The lemma does not say that Huisken monotonicity makes all moving-center limits shrinkers. It is precisely the obstruction to using that invalid argument.

## 5. Compactness, actual components, and extinction recentering

### 5.1 Why a compact oval slice produces a whole component

The proof's assertion that a compact oval slice produces a whole component is stronger than mere visual resemblance to an oval, but justified by the imported smooth multiplicity-one convergence. Choose a tubular neighborhood of the entire compact limiting oval at time -1. For large i, the approximating sheet is a normal graph over that entire closed surface. Compactness gives a finite covering by regular graph charts. The resulting connected graph is compact, boundaryless, and locally an open subset of the ambient regular slice. It is also closed in that slice. Hence it is an entire connected component; it cannot be an oval-shaped segment joined by an unseen neck elsewhere. Such a neck would require leaving a boundaryless open-and-closed graph component.

The oval has positive principal curvatures with a positive minimum at a fixed compact time slice. C^2 convergence therefore gives strict convexity of the whole approximating component. Compact convex evolution and avoidance allow it to be followed independently to a round extinction. Other components may have unrelated singularities, but they do not destroy this smooth convex evolution. This is the exact mechanism used by CHH Proposition 2.2.

### 5.2 Extinction time and point actually converge

For each fixed small eta>0, smooth spacetime convergence on the compact slab from -1 to -eta tracks the same graph component. Smooth uniqueness identifies it with the component already selected at -1. It survives to -eta and lies inside a sphere of radius R_eta+o_i(1), where R_eta→0 as eta→0. In dimension two the radius obeys d(R^2)/dt=-4. Comparison therefore gives

-eta <= tau_i <= -eta + (R_eta+o_i(1))^2/4.

Its extinction location y_i remains inside that same enclosing ball. For each eta first take liminf/limsup in i, and only then let eta→0. The bounds give tau_i→0 and |y_i|→0. This argument does not assume a general continuity theorem for extinction, and does not illegitimately choose eta depending on i before using compact convergence.

The unscaled centers are z_i=x_i+y_i/lambda_i and s_i=t_i+tau_i/lambda_i^2. They converge to X_0. The second exact identity is

M[Z_i,lambda_i]_s = M[X_i,lambda_i]_{s+tau_i}-y_i.

Its plus sign in time and minus sign in space are correct. On every compact negative-time slab the shift tends to zero, so the recentered sequence converges to the same extinction-normalized oval. The amount of recentering tends to zero in rescaled spacetime, as asserted.

### 5.3 Distinctness and the cylindrical accumulation point

If only finitely many extinction points occurred, convergence would force the sequence eventually to equal X_0. The recentered sequence would then be a fixed-center tangent sequence, contradicting the escape lemma. An infinite sequence therefore has a pairwise distinct subsequence. The standard mean-convex classification and isolation of spherical singularities identify the limiting point as cylindrical, as the candidate states.

There is also an independent arrival-time check that avoids any hidden use of Hessian continuity in the isolation step. Since u is C^1 and ∇u(z_i)=0, continuity gives ∇u(x_0)=0 and u(x_0)=t_0. In the surface case its singular tangent is spherical or cylindrical. If it were spherical, the genuine gradient derivative would imply

∇u(x_0+h) = -h/2 + o(|h|).

This is nonzero for sufficiently small nonzero h, excluding any nearby distinct critical point. Thus a distinct singular accumulation cannot be spherical. Single-valuedness of u prevents two spacetime singular points with the same spatial location and different arrival times. Consequently rho_i=|z_i-x_0| is strictly positive. No continuity of D^2u is needed.

## 6. Arrival-time derivatives and all four conclusions

### 6.1 Directional information is legitimately uniformized

The candidate explicitly closes a potentially serious logical gap: directional derivatives alone need not supply the uniform gradient expansion used at arbitrary moving points. Here C^{1,1} is enough. If q_j=r_j v_j→0 with |v_j|=1, select a subsequence v_j→v. A local Lipschitz constant K for ∇u gives

|∇u(x_0+r_j v_j)-∇u(x_0+r_j v)|/r_j <= K|v_j-v|→0.

CM's directional limit at the fixed direction v is -Pv. Adding the term P(v_j-v), which also tends to zero, proves

|∇u(x_0+q_j)+Pq_j|/|q_j|→0.

The compactness-of-directions argument applies to any sequence that could violate this conclusion, so the remainder is a genuine uniform little-o term. The point lies in the interior of the swept domain; sufficiently short line segments around it remain in that domain. Integrating the gradient expansion along q gives

u(x_0+q)-u(x_0) = -(1/2)|Pq|^2 + o(|q|^2).

More explicitly, if the gradient remainder is bounded by epsilon |h| for |h| sufficiently small, its integral along tq is bounded by epsilon |q|^2/2. This validates the scalar remainder without assuming a continuous Hessian.

### 6.2 Axial displacement and time offset

At q_i=z_i-x_0, the gradient is zero. Hence Pq_i=o(rho_i), proving (3.1). Substitution into the scalar expansion gives s_i-t_0=o(rho_i^2), proving (3.2), including its absolute-value form. No sign of s_i-t_0 is inferred. The result permits approach from either direction along the axis and supplies no specified numerical rate.

### 6.3 Oval scale separation

If lambda_i rho_i had a bounded subsequence, then

lambda_i^2 |s_i-t_0| = (lambda_i rho_i)^2 o(1)→0

there. Both terms in the escape lemma would then be bounded for the recentered sequence, a contradiction. Thus lambda_i rho_i→infinity and r_i/rho_i→0. This uses the full divergence statement of the lemma. It is not deduced just from an unbounded subsequence.

### 6.4 Exact Hessian jump and conditional exclusions

At the selected sphere centers H_s=-I/2; at the cylinder H_c=-P. Thus D=H_s-H_c=P-I/2. Since P is a self-adjoint projection,

D^2 = (P-I/2)^2 = I/4.

Consequently ||D||_op=1/2 in every orthonormal coordinate system. Its eigenvalues are 1/2, 1/2, and -1/2. This is an exact identity at every selected center, not just an asymptotic lower bound.

Hessian continuity at x_0 contradicts the identity. More generally the anchored singular-point oscillation limsup ||D^2u(z)-D^2u(x_0)||_op as singular z→x_0 must be at least 1/2. A hypothesis strictly below 1/2 excludes the oval; equality does not. The candidate's corollary has the necessary strict threshold.

For a neck meeting both the applicable CHH hypotheses and SWX's nondegenerate isolation hypotheses, the recentered distinct spherical singularities contradict the isolation neighborhood. This also validates the broader local outer/inner-flow version with both sets of hypotheses retained. It says nothing about a degenerate cylindrical point. The candidate's mention of global finiteness when all singularities are spherical or nondegenerate is credited to SWX, not offered as a new theorem.

## 7. Full infinite bump construction

The construction is not justified by finitely many sample indices. The following estimates cover the entire infinite series.

Let z_i=2^{-i}, delta_i=2^{-3i}, and p_i=z_i e_3, for i>=1. Define E(a)=exp(-1/a) for a>0 and E(a)=0 otherwise. Put chi(t)=1 for t<=1/16, chi(t)=0 for t>=1/4, and on the intervening interval put

chi(t)=E(1/4-t)/[E(1/4-t)+E(t-1/16)].

Define F(Y)=chi(|Y|^2)[(Y_1^2+Y_2^2-Y_3^2)/4-1], b(x)=sum_i delta_i^2 F((x-p_i)/delta_i), and v(x)=-(x_1^2+x_2^2)/2+b(x). The fixed smooth compactly supported F has support in the closed radius-1/2 ball and agrees with (Y_1^2+Y_2^2-Y_3^2)/4-1 in the radius-1/4 ball. The cutoff extends smoothly and flatly at both transition endpoints, and its denominator is nonzero throughout the intervening interval.

### 7.1 Disjointness and local finiteness

Adjacent center distance is z_i/2. Their support radii sum to (delta_i+delta_{i+1})/2=9 delta_i/16. For every i>=1,

(9 delta_i/16)/z_i = (9/16)4^{-i} <= 9/64 < 1/2.

Thus adjacent closed balls are strictly separated. Their ordered axial projection intervals are disjoint, which also separates every nonadjacent pair. The centers and radii tend to zero, so the only possible accumulation point of supports is 0. At any nonzero point the sum is locally finite, and at any point at most one bump is nonzero. Each boundary glues smoothly to zero.

### 7.2 Differentiability at the accumulation point

For b_i(x)=delta_i^2 F((x-p_i)/delta_i), fixed bounds on F, ∇F, and D^2F give

|b_i|<=C delta_i^2,  |∇b_i|<=C delta_i,  ||D^2b_i||<=C.

On its support, |x|>=z_i-delta_i/2>=z_i/2. Hence

|b(x)|/|x|^2 <= 4C(delta_i/z_i)^2,
|∇b(x)|/|x| <= 2C(delta_i/z_i).

Both tend to zero as supports approach 0, since delta_i/z_i=4^{-i}. Outside the supports both quantities vanish. It follows uniformly that b=o(|x|^2) and ∇b=o(|x|). Define b(0)=0 and ∇b(0)=0. First b is differentiable at 0; next its gradient is differentiable there with derivative zero. These are actual Fréchet statements, not just derivatives along the axis. Adding the cylindrical quadratic establishes the claimed Hessian of v at 0.

### 7.3 Global Lipschitz gradient, including segments crossing infinitely many supports

The derivative of ∇v exists at every point: away from 0 by local smoothness, and at 0 by the previous argument. Its operator norm has one uniform finite bound C_0. For any x,y and any unit vector e, consider

g(t)=e·∇v(x+t(y-x)),  0<=t<=1.

This scalar function is continuous on the interval and differentiable in its interior, even if the segment meets 0 or infinitely many supports. Its derivative is bounded in absolute value by C_0|y-x|. The ordinary mean-value theorem gives |e·(∇v(y)-∇v(x))|<=C_0|y-x|. Taking the supremum over e proves the global gradient Lipschitz bound. No countable partition or unjustified interchange of differentiation and an infinite sum at 0 is used. Continuity of the second derivative is unnecessary.

The notation C^{1,1} here means a continuously differentiable function with globally Lipschitz gradient, as in the candidate proof. It does not assert boundedness of v itself on R^3; the quadratic base is unbounded.

### 7.4 Critical jets and strict maxima

Inside |x-p_i|<delta_i/4, direct cancellation gives

v(x) = -[x_1^2+x_2^2+(x_3-z_i)^2]/4 - delta_i^2.

Therefore ∇v(p_i)=0, v(p_i)=-delta_i^2, and D^2v(p_i)=-I/2. Each is a strict local maximum. The time-like ratio is delta_i^2/z_i^2=16^{-i}→0, and the Hessian jump is exactly 1/2. The construction only matches the selected jets and regularity; it does not claim that every other critical point has a permissible arrival-time singularity model.

### 7.5 Explicit independent PDE-failure certificate

The candidate correctly disclaims an arrival-time solution. This can be checked at a specific regular transition point, rather than left to a generic assertion.

Choose any i and put x=p_i+delta_i w e_3 with w=sqrt(5/32). At t=w^2=5/32 the two cutoff exponents agree, and direct differentiation gives

chi(t)=1/2,  chi'(t)=-512/9,  Q(t)=-1-t/4=-133/128.

Rotational symmetry makes the gradient axial. Its coefficient is

∂_3 v(x) = delta_i w [2 chi'(t)Q(t)-chi(t)/2]
           = delta_i w (4247/36),

which is nonzero. Thus the arrival operator is the transverse Hessian trace, and direct calculation yields

Delta v-D^2v(∇v/|∇v|,∇v/|∇v|)
  = -2+4 chi'(t)Q(t)+chi(t)
  = 4229/18.

The required value is -1, so the residual is 4247/18, not zero. This exact check establishes failure of the displayed PDE at a smooth noncritical point, avoiding any issue about viscosity conventions at a critical point. It reinforces, rather than changes, the candidate's stated scope.

## 8. Construction routes, quantifiers, and curvature obstruction

### 8.1 Varying-flow peanut limit

The candidate keeps M^{(i)} varying in the ADS conclusion, whereas the original question requires the same M for all i. This is a substantive quantifier distinction. Ordinary convergence of initial data cannot be passed through arbitrarily large rescaling without a quantitative error estimate relative to that scale. Even the scalar sequence f_i≡1/i converges smoothly to 0, but i f_i=1 while i·0=0. This countermodel is only a logic check, not an MCF example.

The selected ADS members become convex and disappear at their first spherical singularity. One such member therefore does not have the requested later oval episode. The limiting peanut's own first singularity is degenerate, but that fact does not turn the family's oval limit into a fixed-flow realization. A simultaneous construction would need the additional dynamics and scale-by-scale control explicitly identified in the candidate. No defect in the ADS theorem is alleged.

### 8.2 Miura and restarting time

The missing initial smoothness is not a technicality. If a specific sequence t_i decreases to zero, then for each fixed epsilon>0 all but finitely many of its members lie below epsilon. Restarting after epsilon discards that sequence's accumulation. This does not prove a universal statement about every possible singular epoch of the restarted flow, and the candidate carefully says it does not preserve the same accumulation. Forward existence also does not supply a smooth extension to earlier times.

### 8.3 Directly implanted scaled geometry

Under x↦q+delta x, principal curvatures and the norm of the second fundamental form scale by delta^{-1}. If a fixed patch has |A|=c>0 at a selected point, exact scaled copies have curvature c/delta_i→infinity. Uniformly C^2-close normalized patches retaining a fixed positive curvature lower bound have the same obstruction. A compact C^2 embedded surface has bounded second fundamental form, so it cannot contain this sequence of patches unchanged.

This is only a prohibition of that direct construction. It does not exclude small-amplitude smooth perturbations that later create smaller structures under the PDE. An infinite shrinking-component union also fails to be a smooth compact embedded initial surface at its accumulation. None of these observations proves a negative answer to the original problem.

## 9. Independent checks and negative controls

During the audit, an independent mathematical checker used exact rational arithmetic, independently of the candidate's checker, for:

- The Hessian norm identity for 124 nonzero rational-axis representatives, supplemented by the all-projection identity D^2=I/4 proved above.
- Both spatial and temporal rescaling identities in 729 rational test cases.
- Support separation and flatness ratios through 256 indices, supplemented by the all-index proof above.
- The bump core Hessian and the exact PDE-failure value and residual.

Mathematical negative controls explicitly distinguish:

1. The erroneous spherical Hessian -I from the correct -I/2.
2. The wrong sign in the center-change time shift.
3. Disjointness from flatness: supports with delta_i=z_i/4 are disjoint, yet b(p_i)/|p_i|^2=-1/16, so the required zero second-order bump jet at 0 fails.
4. Smooth convergence before rescaling from convergence on diverging scales.
5. Selected arrival-like critical jets from satisfying the arrival-time PDE.

The audit's historical candidate-integrity testing used only temporary copies. It recorded two unchanged positive controls and 24 negative runs, with each case checked in ordinary and optimized Python. It detected proof-byte mutation, manifest-byte mutation, a coordinated proof-and-manifest reseal against the external pin, a missing proof, duplicate manifest records, duplicate JSON keys, a traversal path, file and ancestor symlinks, and resealed incorrect gap/scale/PDE flags. The semantic-constant cases deliberately omitted the old manifest pin after resealing so they exercised the checker's algebra/scope checks rather than only its hash comparison.

All reported checks passed. These tests are supplementary: finite algebra and integrity tests do not establish geometric compactness, imported PDE theorems, infinite-series regularity, novelty, or existence/nonexistence of the target flow. Those boundaries are explicit in the candidate and in this report.

## 10. Acceptance record and remaining problem

The accepted frozen proof has no required patch. The mathematical contribution is a necessary-condition analysis, two conditional exclusions, a scalar regularity countermodel, and two construction-route limitations. The original result must continue to be labeled partial, with `full_problem_solved=false`.

For the mean-convex subclass, a positive construction would need one smooth initial surface with spherical singularities accumulating at a degenerate cylindrical point and the requisite later-time oval limit. It must satisfy all four audited geometric conclusions. A negative solution needs additional MCF/PDE information excluding the degenerate accumulation. A negative solution for the broader original question must also address the non-globally-mean-convex class and the continuation being used. The scalar example supplies no flow, and ancient-solution classification supplies no fixed-flow realization.

The distributed [ACCEPTANCE.json](ACCEPTANCE.json) records the exact proof and audit byte identities and restricted verdict. The public [MANIFEST.json](MANIFEST.json) records all eight members and hashes the seven non-manifest files; the draft PR body independently pins that manifest. Integrity verification does not replace reading the mathematical reasoning. The complete proof, analytic elaborations and explicit transition-point PDE-failure certificate are retained. The omitted original programs and raw outputs are supplementary, and no theorem depends on them. No copied source documents, source text, source images, generated computational certificates, datasets or private coordination material are distributed. QUEUE.md and unrelated repository content are unchanged.
