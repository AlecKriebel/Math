# Necessary geometry of an ancient oval limit

Problem 30004196 / OWR-17130-012. 10 October 2026.

Accepted bounded partial, with the complete [mathematical audit](MATHEMATICAL_AUDIT.md). This AI-assisted manuscript and audit are unrefereed. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The original realization question remains open.

## Result and exact scope

The original realization question remains unresolved. This report proves a bounded necessary-condition theorem in the closed mean-convex surface class, an exclusion criterion under an additional continuity hypothesis, and an explicit scalar example showing why a regularity-only proof stops short. It also checks two plausible construction routes against their precise hypotheses. It does not construct an ancient oval limit of one smooth closed initial surface and does not exclude such limits in the original class.

The source question concerns mean curvature flow starting at a smooth, closed, embedded surface in R^3, continued through singularities, and asks whether an ancient oval can occur as a limit at a time strictly after the first singular time. Where a choice of weak continuation matters, outer and inner level-set flows are the relevant canonical continuations. The original question is not restricted to globally mean-convex initial surfaces. The arrival-time theorem below **is** so restricted. The separate moving-center lemma applies whenever the stated tangent-flow monotonicity and convergence properties hold.

The contribution by Kyeongsu Choi, Robert Haslhofer and Or Hershkovits in Oberwolfach Report 34/2019, PDF pages 40–42, supplies the original context; its page 41 footnote leaves later-time occurrence open. The equivalence between oval limits and accumulating spherical singularities is due to **Beomjun** Choi, Robert Haslhofer and Or Hershkovits (CHH), not to this report. The arrival-time differentiability theorem and Hessian identification are due to Tobias Colding and William Minicozzi II (CM). The deductions assembled here have no established novelty claim.

## 1. Conventions and precise imported results

For a spacetime point X=(x,t), write

M[X,lambda]_s = lambda (M_(t+s/lambda^2) - x).

An ancient oval O is the compact, strictly convex, non-selfsimilar ancient solution under consideration, normalized to become extinct at spatial origin and time 0. It is smooth for s<0. A limit flow at X_0 allows X_i→X_0 and lambda_i→infinity. A tangent flow fixes X_i=X_0. These are different quantifiers.

The arguments use the following established results. They are dependencies, not newly proved claims.

1. **Tangent-flow monotonicity.** For a fixed Brakke flow in this setting, a tangent flow at X_0 is backward selfsimilar on negative times, by Huisken's monotonicity formula. Subsequential compactness holds for its parabolic rescalings.
2. **Compact convex limit extraction.** In a mean-convex flow, convergence to a smooth multiplicity-one oval is smooth on compact subsets before its extinction. A compact oval slice is therefore approximated by an actual closed strictly convex component of the rescaled flow. The component evolves smoothly to a round extinction. This is the mechanism in CHH, Proposition 2.2.
3. **CHH accumulation criterion.** In the flow of a smooth closed embedded mean-convex surface in R^3, oval limits are equivalent to spherical singularities accumulating at a cylindrical singularity. The proof localizes the conclusion at the point supporting the oval limit. In the broader original class, CHH Theorem 1.5 instead assumes an inward or outward neck singularity and uses the corresponding outer or inner flow. Those local hypotheses are not omitted here.
4. **CM arrival time.** If M_0 bounds a compact mean-convex domain, its arrival time u is C^{1,1}, twice differentiable, with gradient zero at singular points. At a cylindrical singularity x_0 with axis L through x_0,

   D^2u(x_0) = -P,

   where P is orthogonal projection onto L-perpendicular. At a spherical singularity z,

   D^2u(z) = -(1/2)I_3.

   These are CM, Theorem 0.2 and Proposition 2.2, in arXiv:1501.07899v3. The gradient differentiability used below is justified explicitly in Section 3.
5. **Nondegenerate neck isolation.** Sun–Wang–Xue, arXiv:2501.16678v1, Theorem 1.1(i), proves spacetime isolation of a nondegenerate cylindrical singularity for a unit-regular cyclic mod-2 Brakke flow. Their nondegeneracy is the full-rank quadratic normal-form condition defined immediately before the theorem. It is not an assumption automatically satisfied by every cylindrical tangent flow.

## 2. Bounded motion of centers cannot produce an oval

**Lemma 2.1.** Suppose a fixed flow M has an oval limit

M[X_i,lambda_i] → O,

where X_i=(x_i,t_i)→X_0=(x_0,t_0) and lambda_i→infinity. Assume the compactness and tangent-flow monotonicity stated above. Then

lambda_i |x_i-x_0| + lambda_i^2 |t_i-t_0| → infinity.     (2.1)

Equivalently, with d_P(X,Y)=max(|x-y|,sqrt(|t-s|)),

lambda_i d_P(X_i,X_0) → infinity.                         (2.2)

**Proof.** If (2.1) failed, there would be a subsequence on which the two terms are bounded. Pass to a further subsequence with

a_i=lambda_i(x_i-x_0)→a,
b_i=lambda_i^2(t_i-t_0)→b.

Set N_i=M[X_0,lambda_i]. The exact relation between slices is

N_i(s)=a_i+M[X_i,lambda_i](s-b_i).

For every sufficiently negative s, namely s<min(0,b), the right side converges to a+O_(s-b). Compactness and fixed-center monotonicity say that this same limiting flow is backward selfsimilar for s<0. Hence a time-translated and spatially translated ancient oval would agree with a homothetically shrinking flow on a whole past time interval. A compact convex homothetically shrinking solution is a round sphere; forward uniqueness of compact smooth MCF would then make the oval spherical. This contradicts the choice of a non-selfsimilar oval. Every bounded subsequence is therefore impossible. The equivalence with (2.2) follows because A+B^2 is bounded exactly when max(A,B) is bounded, for A,B≥0. ∎

This lemma does not prohibit moving-center limits. It proves precisely why replacing moving centers by the limiting center is invalid in the remaining case: the replacement is unbounded at the blowup scale.

## 3. Geometry forced by a single-flow oval limit

**Theorem 3.1.** Let M be the mean curvature flow of a smooth closed embedded mean-convex surface in R^3. Suppose M has an ancient oval as a limit flow at X_0=(x_0,t_0). Let u be the arrival time. After taking a subsequence and recentering by an amount tending to zero in rescaled spacetime, there are pairwise distinct spherical extinction points Z_i=(z_i,s_i), with Z_i→X_0, and scales lambda_i→infinity such that

M[Z_i,lambda_i] → O.

The point X_0 is cylindrical. Let L be its tangent-cylinder axis, P projection onto L-perpendicular, rho_i=|z_i-x_0|, and r_i=1/lambda_i. Then rho_i>0 and

|P(z_i-x_0)|/rho_i → 0,                                  (3.1)
|s_i-t_0|/rho_i^2 → 0,                                   (3.2)
r_i/rho_i → 0.                                           (3.3)

Moreover, at every one of these points,

||D^2u(z_i)-D^2u(x_0)||_op = 1/2.                         (3.4)

Thus spherical extinction centers must approach the axis to first order, their time offsets must be smaller than quadratic spatial separation, and the oval's spatial scale must be smaller still than that separation. The arrival-time Hessian has a fixed-size discontinuity along this sequence.

### Proof of extinction recentering

Take the convergent oval blowup sequence and normalize its limiting extinction to (0,0). At rescaled time -1, smooth multiplicity-one convergence around the entire compact oval gives, for all sufficiently large i, a closed strictly convex component C_i. It is a component, rather than just a long capped piece, because the normal graph over the compact oval is itself a compact boundaryless surface and is relatively open in the smooth ambient slice. Convex MCF evolves it smoothly to a spherical extinction, say at (y_i,tau_i) in rescaled coordinates.

We verify y_i→0 and tau_i→0, rather than assume continuity of extinction. For every small eta>0, the limiting oval at time -eta lies in a ball B_(R_eta)(0), with R_eta→0 as eta↓0. For large i its corresponding component exists at -eta and is contained in B_(R_eta+o(1))(0). It cannot disappear before -eta. Comparison with the shrinking enclosing sphere, whose extinction delay in R^3 is radius squared divided by 4, gives

-eta ≤ tau_i ≤ -eta+(R_eta+o(1))^2/4.

The convex component and its extinction point remain in that enclosing ball. Taking limits in i and then eta↓0 proves tau_i→0 and y_i→0. In unscaled coordinates set

z_i=x_i+lambda_i^(-1)y_i,
s_i=t_i+lambda_i^(-2)tau_i.

Then Z_i→X_0 and

M[Z_i,lambda_i]_s = M[X_i,lambda_i]_(s+tau_i)-y_i → O_s.

If only finitely many Z_i occurred, a convergent subsequence would be eventually centered at X_0 itself. Lemma 2.1 would rule out the oval. We may therefore take a subsequence of pairwise distinct Z_i. The CHH criterion and its proof identify X_0 as cylindrical; equivalently, the accumulation is singular, and the mean-convex tangent classification and isolation of spherical singularities leave the cylinder.

### Proof of the arrival-time estimates

Write q_i=z_i-x_0. Both endpoints are critical points, and u(z_i)=s_i, u(x_0)=t_0. The CM result gives the first-order expansion of the gradient

∇u(x_0+q)= -Pq + o(|q|),                                 (3.5)

and the scalar expansion

u(x_0+q)=t_0-(1/2)|Pq|^2+o(|q|^2).                       (3.6)

For completeness, even if CM Proposition 2.2 is read initially as directional convergence of difference quotients, (3.5) follows from that convergence and the C^{1,1} bound. Given q_j→0, pass to a subsequence q_j/|q_j|→v. Lipschitz continuity of ∇u makes the difference between its normalized values at q_j and at |q_j|v tend to zero. The directional limit at v is -Pv. Every such subsequence has the required limit. Integrating (3.5) along the straight segment proves (3.6), with a uniform little-o remainder.

If z_i=x_0, the single-valuedness of arrival time would give Z_i=X_0. Since the selected spherical points are distinct from the cylindrical point, rho_i>0. Substitute ∇u(z_i)=0 in (3.5):

Pq_i=o(rho_i).

This proves (3.1). Substitute that result in (3.6) to obtain s_i-t_0=o(rho_i^2), proving (3.2).

Apply Lemma 2.1 to the recentered sequence. If lambda_i rho_i had a bounded subsequence, then (3.2) would also give

lambda_i^2 |s_i-t_0| = (lambda_i rho_i)^2 o(1) →0

along it, contradicting the lemma. Thus lambda_i rho_i→infinity, which is (3.3).

Finally,

D^2u(z_i)-D^2u(x_0)=P-(1/2)I_3.

Projection P has eigenvalues 1,1,0, so this difference has eigenvalues 1/2,1/2,-1/2. Its operator norm is exactly 1/2. This proves (3.4). ∎

**Corollary 3.2.** In the closed mean-convex surface class, an oval limit is impossible at a point where the arrival-time Hessian is continuous. It is enough that the Hessian oscillation along nearby singular points have limsup strictly less than 1/2 in operator norm.

**Proof.** The sequence in (3.4) violates either condition. ∎

No assertion that the required continuity holds for every flow is made. C^{1,1} and twice differentiability do not imply it.

**Corollary 3.3.** An oval limit cannot occur at a nondegenerate neck satisfying the Sun–Wang–Xue hypotheses. This local conclusion also applies to the broader outer/inner-flow setting wherever CHH's corresponding neck hypotheses and the cited isolation theorem apply.

**Proof.** CHH would produce distinct spherical singularities accumulating at the neck, contradicting spacetime isolation. ∎

This is a direct combination of credited prior results. It is not an exclusion of degenerate cylindrical singularities. Sun–Wang–Xue already give finiteness when all singularities are spherical or nondegenerate cylindrical (their Corollary 1.3).

## 4. A rigorous obstruction to a regularity-only exclusion

A potential exclusion proof would try to derive a contradiction from the two critical-point Hessians and the C^{1,1}, twice-differentiable regularity of u. The following explicit example shows those properties alone cannot do so. It is a scalar example, not a mean curvature flow or an arrival-time solution.

Choose a smooth cutoff chi:[0,infinity)→[0,1] equal to 1 on [0,1/16] and 0 on [1/4,infinity). One explicit choice on the intervening interval is

chi(t)=E(1/4-t)/(E(1/4-t)+E(t-1/16)),

where E(a)=exp(-1/a) for a>0 and E(a)=0 for a≤0. Define

F(Y)=chi(|Y|^2)((Y_1^2+Y_2^2-Y_3^2)/4-1),
z_i=2^(-i), delta_i=2^(-3i), p_i=(0,0,z_i), i≥1,

v(x)=-(x_1^2+x_2^2)/2 + sum_(i≥1) delta_i^2 F((x-p_i)/delta_i).   (4.1)

**Proposition 4.1.** The function v is C^{1,1} and twice differentiable on R^3, smooth away from 0. It has

v(0)=0, ∇v(0)=0, D^2v(0)=diag(-1,-1,0),

and at each p_i,

v(p_i)=-delta_i^2, ∇v(p_i)=0, D^2v(p_i)=-(1/2)I_3.

The p_i are strict local maxima, accumulate along the third coordinate axis, and satisfy |v(p_i)-v(0)|/|p_i|^2→0. The Hessian jump is exactly 1/2 in operator norm.

**Proof.** The support of the i-th summand lies in the ball B_(delta_i/2)(p_i). These balls have disjoint closures: the separation of adjacent centers is z_i/2, whereas the sum of their radii is (9/16)delta_i<z_i/2 for i≥1. They accumulate only at 0. Thus the sum is locally finite away from 0, and at most one term is nonzero anywhere.

Let b denote the sum of bumps. On its i-th support,

|b|≤C delta_i^2, |∇b|≤C delta_i, ||D^2b||≤C,

with a constant independent of i, since F is one fixed compactly supported smooth function. Points on that support satisfy |x|≥z_i-delta_i/2≥z_i/2. Because delta_i/z_i=2^(-2i)→0, we have b(x)=o(|x|^2) and ∇b(x)=o(|x|) at 0. Extending b and ∇b by zero at 0 makes b differentiable there with gradient zero, and makes ∇b differentiable there with derivative zero. Thus v is twice differentiable at 0 with the stated Hessian. Elsewhere it is smooth. Its second derivative is bounded everywhere. The mean-value theorem applied to each component of its gradient along any segment gives a global Lipschitz bound for ∇v, proving C^{1,1}.

For |x-p_i|<delta_i/4, the cutoff is 1 and all other bumps vanish. Hence

v(x)=-(x_1^2+x_2^2+(x_3-z_i)^2)/4-delta_i^2.

This formula proves the critical-point, strict-maximum and Hessian claims. The time-like ratio is delta_i^2/z_i^2=2^(-4i)→0. The final norm computation is the same as (3.4). ∎

The example preserves exactly the finite-jet obstruction used in Theorem 3.1. It does **not** satisfy, or purport to satisfy, the arrival-time equation

-1=∆v-D^2v(∇v/|∇v|,∇v/|∇v|)

throughout its transition regions. It does not satisfy all the other structural results for a genuine arrival time. Therefore it cannot serve as a counterexample to the original problem. It proves that a successful exclusion must use further MCF/PDE information, rather than silently upgrade twice differentiability to continuity of the Hessian.

## 5. Why two construction routes do not yet give one original-class flow

### 5.1 Perturbing a peanut solution

Angenent–Daskalopoulos–Sesum, arXiv:2512.05077v2 (31 August 2026), Theorem 1.4 and Section 10, obtain an ancient oval after rescaling a sequence of *different* flows in specified perturbation families of a 4-peanut solution. Section 10 selects members that become convex before their first spherical singularity.

In symbols, the relevant conclusion has the form

D_(lambda_i)(M^(i)-X_i) → O,

with M^(i) varying. The original problem requires

D_(lambda_i)(M-X_i) → O

for a single M. Convergence of the unrescaled initial surfaces does not justify substituting their limit M for each M^(i) on diverging scales. The limiting peanut has its own degenerate first singularity; a spherical perturbation member becomes convex and then vanishes at its first singularity. The oval from the parameter sequence is not a later-time blowup of any one of those individual spherical members.

To make this route work, one would need a single-flow construction retaining an unbounded sequence of oval-producing episodes, with quantitative error control after rescaling at every episode, and smooth compact embedded initial data. The cited theorem supplies no such simultaneous realization. This is a quantifier gap, not a defect claimed in that theorem. Its long perturbation analysis is not independently re-proved here; its statement and the varying-flow proof mechanism were inspected.

### 5.2 Infinite small components or necks

Miura's arXiv:1411.6249v4, Theorem 2.1, constructs a compact connected axisymmetric hypersurface smooth except at one initial point, whose flow has singular times tending to 0. The missing smoothness hypothesis is essential to its relevance here. Starting at a positive time does not preserve the same accumulation: if t_i↓0, then only finitely many terms of that sequence lie above any fixed epsilon>0. Nor does forward existence produce a smooth negative-time extension.

A direct implantation of geometrically similar shrinking building blocks into the initial surface also has a concrete obstruction. If a fixed smooth curved patch Sigma has |A_Sigma|(p)=c>0 and copies q_i+delta_i Sigma with delta_i↓0 are included unchanged in one initial surface, then their corresponding curvatures are c/delta_i→infinity. A compact C^2 embedded initial surface has bounded curvature. Therefore that particular rescaled-patch construction cannot be smooth. The same obstruction applies to uniformly C^2-close normalized copies retaining curvature at least c/2.

This is only a no-go result for that direct implantation. It does not rule out a smooth low-amplitude initial perturbation generating increasingly small structures later. Proving that evolution would require a new dynamical construction. Neither Miura's initial singularity nor an infinite disjoint union of shrinking components meets the original smooth closed embedded initial-surface requirement.

## 6. Exact remaining gap

For globally mean-convex closed surfaces, the unresolved step is existence or impossibility of a single smooth initial surface whose spherical singularities accumulate at a degenerate cylindrical singularity. Such a realization would settle the original existence question positively, because it is already within the original class. CHH converts that event to an oval limit, but does not realize the event.

A negative solution to the **full original question** must additionally cover the original non-globally-mean-convex scope and a legitimate through-singularity continuation; the mean-convex arrival-time theorem here does not do that. At inward/outward necks one has the local CHH equivalence with its exact hypotheses, but this still leaves the accumulation mechanism unresolved.

A future positive construction must verify, for one fixed smooth closed embedded initial surface, a sequence of moving centers and diverging scales converging to the entire ancient oval on every compact negative-time interval, at a limiting spacetime point after the first singular time. In the mean-convex subclass it must also meet (3.1)–(3.4). A future negative proof needs a new exclusion of the degenerate accumulation, not classification of ancient solutions alone.

## References and credit

- Kyeongsu Choi, joint work with Robert Haslhofer and Or Hershkovits. Ancient mean curvature flow of low entropy. Oberwolfach Report 34/2019, PDF pp. 40–42, especially p. 41 footnote. https://ems.press/content/serial-article-files/46813
- Beomjun Choi, Robert Haslhofer, Or Hershkovits. A note on the selfsimilarity of limit flows. arXiv:1910.02341v1; Theorem 1.3, Corollary 1.4, Theorem 1.5, Proposition 2.2. https://arxiv.org/abs/1910.02341
- Tobias H. Colding, William P. Minicozzi II. Differentiability of the arrival time. arXiv:1501.07899v3; Theorem 0.2, Corollary 1.12, Proposition 2.2. https://arxiv.org/abs/1501.07899
- Ao Sun, Zhihan Wang, Jinxin Xue. Passing through nondegenerate singularities in mean curvature flows. arXiv:2501.16678v1; Theorem 1.1(i), Corollary 1.3. https://arxiv.org/abs/2501.16678
- S. B. Angenent, P. Daskalopoulos, N. Sesum. Mean curvature flow near a peanut solution. arXiv:2512.05077v2; Theorems 1.3–1.4 and Section 10. https://arxiv.org/abs/2512.05077
- Tatsuya Miura. An example of a mean-convex mean curvature flow developing infinitely many singular epochs. arXiv:1411.6249v4; Theorem 2.1. https://arxiv.org/abs/1411.6249
- Robert Haslhofer. Mean curvature flow through singularities. Author PDF dated 1 October 2025; Problem 5.5, PDF pp. 15–16. https://www.math.toronto.edu/roberth/papers/haslhofer_icm2026.pdf
- Beomjun Choi, Wenkui Du, Jingze Zhu. Rigidity of ancient ovals in higher dimensional mean curvature flow. arXiv:2504.09741v1. Classification under specified ancient-flow hypotheses, not single-flow realization. https://arxiv.org/abs/2504.09741

This is an AI-assisted, unrefereed mathematical report. The elementary deductions above are supplied with proofs; imported deep theorems retain their original credit. No claim of external peer review, full-problem resolution, or priority is made.
