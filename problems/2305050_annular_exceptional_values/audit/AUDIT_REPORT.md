# Independent audit: Function Theory Problem 5.50

Problem identifier: **2305050 / AMR-022-5050**. Review date: **2026-10-03 UTC**.

## Verdict

**Accept the proposed disposition `already_solved`, at substantive turn `1/5`.** F. W. Carroll's 1979 Theorem 2 answers the precise question affirmatively. The answer is not a new resolution. The existing attribution note correctly distinguishes the relevant exceptional values from singularities of an inverse function.

No mathematical correction to the note's theorem application is required. This report makes several suppressed construction details explicit, including the role of the possibly unbounded cap, the order of approximation choices, and the boundary interpretation in Lemma A. The classification rests on the published theorem and the exact definition match, not on the finite verification program. This is an AI-assisted mathematical audit, not a claim of human peer review or formal proof verification.

The seven reviewed public files and their unchanged comparison copies match the frozen SHA-256 records. The reviewed freeze digest is `d9f59c9b1fd51a7f925af09fe94f34f005b4b50db3ab62d1e4fee45245035bd2`. A separate public-safe manifest identifies the reviewed artifacts and audit outputs by relative filename and hash.

## 1. Exact target and attribution

The primary problem is Hayman and Lingham, *Research Problems in Function Theory (New Edition)*, Problem 5.50, printed p. 104. It asks for an analytic function on the unit disk with nested Jordan curves approaching the unit circle, with minimum modulus tending to infinity, and with countably infinitely many values whose preimages do not accumulate on the entire unit circle. Its Update 5.50 already credits Carroll with the requested strongly annular example. Reference [145] identifies the 1979 paper. The problem and update were checked against the page image, not merely extracted text.

Carroll's complete five-page paper was read against its page images. On p. 330 he defines, for finite complex (a),

\[
 Z'(f,a)=\mathbb T\cap\overline{\{z\in\mathbb D:f(z)=a\}},
 \qquad
 S(f)=\{a\in\mathbb C:Z'(f,a)\ne\mathbb T\}.
\]

Here the closure is taken in the plane; since the preimages lie in the disk, its intersection with the unit circle is exactly their boundary accumulation set. This is the problem's (Z'(f-a)). It has no relation, by definition, to counting critical values or finite asymptotic values. Confusing those meanings would invalidate the application; no such confusion occurs in the reviewed note.

Carroll's Theorem 2 explicitly asserts a strongly annular function with countably infinite (S(f)). His strong annularity uses (0<r_1<r_2<\cdots\uparrow1). The circles (J_n=\{|z|=r_n\}) satisfy all three conditions of the original problem: each lies inside the next, they eventually lie in any prescribed outer annulus, and their minimum moduli tend to infinity. Thus there is neither a domain mismatch nor an annularity mismatch.

The attribution is to Carroll throughout. Osada's earlier construction has two exceptional values; it is not being credited with the countably infinite example. No uniqueness of the example, prescription of its exact exceptional set, or new priority claim is needed or asserted.

## 2. Audit of the geometry and induction invariants

Carroll sets

\[
 \zeta_j=\exp(2\pi i(1-2^{-j})).
\]

The fixed cap (G_j) has the nonempty circular boundary arc from \(\zeta_j\) to \(\zeta_{j+1}\), of angular width \(2\pi 2^{-j-1}\). The remaining cap (G'_n) is split into (G_n), (G'_{n+1}), and intervening polygonal area at the next stage. Its chord has distance \(\cos(\pi/2^n)\) from the origin.

The radius choices

\[
 \cos(\pi/2^{n+1})<r_n<\cos(\pi/2^{n+2})
\]

are compatible with the initial radii, force strict increase and convergence to 1, and leave nonempty choices after avoiding all zeros of the finitely many (f_{n-1}-a_j). A nonzero holomorphic function has a discrete, hence countable, zero set in the disk; the corresponding excluded radii cannot exhaust an interval. In fact only finitely many zeros occur in a compact subannulus containing the choice interval.

For each (n), the small regions (T_{n,j}) lie inside the polygon, outside the previous circle, and are mutually disjoint. They avoid all caps to be protected. Their intersections (B_{n,j}) with the new circle provide the gaps. Lemma A chooses the smaller gaps \(\sigma_{n,j}\) independently of the eventual size and smallness tolerances. This independence matters: the large arcs (A_{n,j}) can be fixed before the Runge approximations are chosen.

The five induction properties have distinct uses:

1. \(\|f_n-f_{n-1}\|_{\{|z|\le r_{n-1}\}}<2^{-n}\) gives convergence and preserves previously established circular lower bounds in the limit.
2. \(|f_n|>2^n\) on the new circle gives strong annularity after passage to the limit.
3. (f_n-a_j) stays bounded away from zero on every fixed (G_j) already introduced.
4. (f_n-a_n) stays bounded away from zero on the remaining (G'_n).
5. (f_n) is bounded on (G'_n\cup\bigcup_{j=1}^{n-1}G_j). The omission of (G_0) from this boundedness condition is deliberate and must not be overlooked.

The base (a_0=0,a_1=1,a_2=2), (f_1=f_2=5), satisfies the required properties at (n=2). At the next stage, boundedness on the previous remaining cap permits a real (a_n>a_{n-1}) chosen outside its range with a positive distance margin. The inherited omission of (a_{n-1}) holds on the new fixed (G_{n-1}\subset G'_{n-1}); omission of the newly chosen (a_n) holds on (G'_n\subset G'_{n-1}).

## 3. Polynomial algebra and the uniform-estimate issue

The matrix in Carroll's p. 332 coefficient system is (M=J-I), of size (n+1), where (J) is the all-ones matrix. It acts as multiplication by (n) on the constant vector and by (-1) on the sum-zero subspace. Therefore

\[
 \det M=n(-1)^n\ne0,
 \quad A=\frac1n\sum_{i=0}^{n}a_i,
 \quad \alpha_j=A-a_j,
 \quad \sum_i\alpha_i=A,
 \quad \sum_{i\ne j}\alpha_i=a_j.
\]

These identities hold for every (n\ge1) and every complex right-hand side. They are not conclusions from a finite sample.

Carroll's combination is

\[
 g=(f_{n-1}-A)\exp\!\left(\sum_i P_i\right)
       +\sum_i\alpha_i e^{P_i}.
\]

If all (e^{P_i}) except (e^{P_j}=t) equal 1 exactly, it reduces exactly to

\[
 (f_{n-1}-a_j)t+a_j.
\]

The displayed algebra is correct. The actual construction only makes the inactive polynomials small, rather than identically zero. Thus the algebra by itself does not certify the following uniform separation claims. In particular, one must not infer a uniformly small additive error from a small multiplier on (G_0), where (f_{n-1}) need not be bounded. The paper uses qualitative approximation tolerances; the supplied program neither tests nor proves that analytic step.

For a fully explicit check of the finite construction principle, the same Runge step can be organized by successive affine-exponential changes. This is an audit reconstruction using Carroll's cap geometry and Lemma A, not a claim that the paper literally uses this order of operations or a claim of a new theorem.

### An explicit ordering of the finite Runge step

Let the protected caps at stage (n) be (C_j=G_j) for (j<n) and (C_n=G'_n), with their respective values (a_j). Start with (F=f_{n-1}). Process (j=0,\ldots,n) using

\[
 F_{\mathrm{new}}=(F-a_j)e^{P_j}+a_j.
\]

On (A_{n,j}), choose (P_j) close to a holomorphic branch of

\[
 \log\!\frac{R-a_j}{F-a_j},
\]

where (R>\max_j a_j) is also well above (2^n). On the inner disk, all other caps, and all other large arcs, choose (P_j) close to zero. The active arc is compact and simple; its denominator is nonzero. It consequently has a thin simply connected neighborhood with a holomorphic logarithm. Earlier steps can preserve this nonvanishing on every as-yet unprocessed arc by sufficiently small changes on that compact arc.

The Runge compact consists of the closed zero-target pieces and the disjoint active arc. Filling bounded complementary components of the zero-target pieces adds only zero-target regions. The active cap gives access to the exterior, and the positive gaps in the triangles separate the active arc from the filled zero set. The resulting compact has connected complement, as in the paper's Runge geometry. All cap closures may be used for the zero target, even where they meet the unit circle: that target is the entire function zero, so no extension of (F) across the circle is being assumed there.

Here are the required preservation estimates, which also explain why (G_0) needs separate treatment.

- On the active cap, (F_{\mathrm{new}}-a_j=(F-a_j)e^{P_j}). A polynomial is bounded on the closed unit disk, so its exponential has a strictly positive modulus lower bound there. The existing separation margin therefore stays positive.
- On any other bounded cap (C_i), use
  \(F_{\mathrm{new}}-F=(F-a_j)(e^{P_j}-1)\).
  Its first factor is bounded and its second can be made arbitrarily small. This preserves the positive distance from (a_i).
- On (G_0) during a step (j\ne0), write (m_0=\inf_{G_0}|F|>0). Then
  \[
  |F_{\mathrm{new}}-F|
  \le |F|\left(1+\frac{|a_j|}{m_0}\right)|e^{P_j}-1|.
  \]
  Choosing the last factor sufficiently small gives \(|F_{\mathrm{new}}|\ge |F|/2\ge m_0/2\). This relative estimate does not require boundedness on (G_0). During step (j=0), (a_0=0) and the active-cap multiplication preserves omission of zero directly.
- On the compact inner disk, choose the change smaller than \(2^{-n}/(2(n+1))\). On all other large arcs, make it small enough to preserve the existing positive real-part margins and the unprocessed denominators' nonzero margins.
- Every bounded cap remains bounded, because the operations involve only a bounded (F), constants, and exponentials of polynomials.

There are finitely many conditions at each stage. At each successive step the relevant constants and positive margins are already fixed, so the next tolerance can be chosen without circular dependence. The result is a holomorphic (g), separated from the prescribed cap values, bounded on the required caps, within (2^{-n}/2) of (f_{n-1}) on the inner disk, and with \(\operatorname{Re}g>2^n+1\) on all the large arcs. This confirms the finite construction principle without treating the published approximation signs as exact identities.

### Closing the gaps

Choose the total smallness allowance \(\sum_j\varepsilon_j\) less than each of:

- half the smallest cap-omission margin for (g);
- (2^{-n}/2), for the inner-disk budget;
- (1/2), for the real-part margin on the large arcs.

All caps and the inner disk lie outside every (T_{n,j}), so Lemma A bounds every perturbation there by its allowance. On \(\sigma_{n,j}\), the other perturbations are small; choose (M_j) above \(\max_{|z|=r_n}|g(z)|+2^n+1\). Then the (j)-th perturbation dominates (g) and the others. On a protrusion of a large arc into (T_{n,j}), its real part is positive by Lemma A and all other perturbations are small. Thus

\[
 f_n=g+\sum_{j=0}^{n}h_j
\]

has modulus (>2^n) on the entire circle, preserves all omission margins and boundedness requirements, and meets the approximation budget. This checks all five induction invariants, including the bookkeeping suppressed in the printed conclusion.

## 4. Lemma A: analytic and boundary checks

The full supplied proof on pp. 333-334 was read. Its analytic input is Arakelian's uniform approximation theorem, explicitly cited by Carroll. It is not an application of ordinary Runge approximation to an arbitrary noncompact set.

The slit complement \(\widehat{\mathbb C}\setminus B_{n,j}\) is conformally mapped to the complement of the closed unit disk with the real whiskers \([-2,-1]\cup[1,2]\). Boundary correspondence is interpreted in prime ends. Symmetry selects the subarc \(\sigma_{n,j}\) whose two sides map to the two unit semicircles. The other pieces map to the real whiskers. The triangular boundary maps strictly outside the unit circle, allowing (1<\rho<2) below its minimum modulus. These choices depend on the geometry, not on (M_j,\varepsilon_j).

For sufficiently large integer (m), Carroll uses

\[
 \Psi(z)=\left(\frac{\rho}{\varphi(z)}\right)^{2m}.
\]

The even exponent is essential: on both real whiskers the boundary value is positive, including the negative whisker. On the central subarc its modulus is \(\rho^{2m}\); off the triangle it decays geometrically, by the modulus bound on the conformal image and the maximum principle. On the remaining parts of (B_{n,j}), its positive real value has the uniform lower bound \((\rho/2)^{2m}>0\).

A potential boundary confusion is avoided as follows. Remove only the part of the triangle exterior to the new circle, and call the remaining relatively closed subset of the disk (E). The central slit arc is now part of the boundary of (E), with the trace from the retained side. The two generally different traces on the unit semicircles need not be identified with each other. The resulting function is continuous on (E) and holomorphic in its interior, exactly what the approximation theorem requires.

The removed region has an escape to its single unit-circle vertex and has the uniform near-boundary escape property described by Carroll. Thus (E) is in the required Arakelian class. Approximate \(\Psi\) uniformly with error smaller than the off-triangle smallness margin, the gap-modulus margin, and half \((\rho/2)^{2m}\). The resulting holomorphic (h_j) has all three strict properties in Lemma A. In particular, uniform approximation really does preserve the positivity assertion; mere pointwise positivity would not have been enough.

The original proof of Arakelian's theorem is an external dependency, not independently re-proved here. The conformal mapping and boundary-correspondence facts are standard analytic inputs. The audit checks the way they are used and does not represent them as consequences of the finite computation.

## 5. Limit, Hurwitz, and cardinality

For every fixed compact subdisk, all sufficiently late estimates in (2.1) hold on that subdisk. Summability therefore makes \(f_k\) locally uniformly Cauchy, and its limit (f) is holomorphic. For (k\ge2),

\[
 \sup_{|z|\le r_k}|f-f_k|
 \le\sum_{m=k+1}^{\infty}2^{-m}=2^{-k}.
\]

It follows that

\[
 \min_{|z|=r_k}|f|
 \ge\min_{|z|=r_k}|f_k|-2^{-k}
 >2^k-2^{-k}\longrightarrow\infty.
\]

This proves strong annularity and, in particular, rules out a constant limit. The strict inequality is valid because each circle is compact and the corresponding pointwise lower bound for (f_k) is strict.

For fixed (j), the functions (f_k-a_j) are zero-free on the connected open cap (G_j) for all sufficiently large (k). Hurwitz gives either a zero-free limit or an identically zero limit on that cap. The identity theorem would turn the second alternative into (f\equiv a_j) throughout the disk, contradicting the circular lower bounds. Thus (f-a_j) is zero-free on (G_j). No uniform positive omission margin as (k\to\infty) is needed here.

Each interior point of the circular arc bounding (G_j) has a sufficiently small disk-relative neighborhood contained in (G_j). Consequently that entire open arc is excluded from (Z'(f,a_j)), and (a_j\in S(f)). Since the (a_j) are distinct, (S(f)) is infinite.

For the upper bound, Osada p. 491 states, for annular functions and (a\ne b), that the open sets

\[
 U_a=\mathbb T\setminus Z'(f,a),\qquad
 U_b=\mathbb T\setminus Z'(f,b)
\]

are disjoint, and attributes this consequence to the Koebe-Gross theorem. Carroll p. 330 invokes the same fact. The complete Osada mathematical paper was read; its later two-value construction is not required for this upper bound. The Koebe-Gross theorem itself remains an expressly identified classical dependency.

Fix a countable dense sequence \((q_m)\) on \(\mathbb T\). Each nonempty open (U_a) contains some (q_m). Map (a\in S(f)) to the least such (m). Disjointness makes this map injective. Thus (S(f)) is at most countable; together with the infinitely many (a_j), it has cardinality exactly \(\aleph_0\).

This argument does not assert (S(f)=\{a_j:j\ge0\}); additional exceptional values would not affect the required cardinality.

## 6. Exact computation, independently checked

The supplied `verify.py` was run unchanged. Its output is byte-for-byte identical to `verification.json`, with SHA-256 `0c2774eab500052d3bb5331bbdd6b5d0e27aefce07f229dd596c5635d84319f6`.

The claimed 29,774 assertions were independently counted:

- determinant checks: 20;
- right-hand-side vectors: \(\sum_{n=1}^{32}(n+2)=592\);
- linear-system equations and single-active-factor identities: \(\sum_{n=1}^{32}(n+1)(n+2)=13088\) each;
- finite geometric-tail checks: \(127\cdot20=2540\);
- lower-bound and monotonicity checks: 127 each;
- arc widths, nonempty arcs, and partial sums: 64 each.

Their sum is exactly 29,774. No category counts were inferred merely from the program's printed total.

The independent program also:

- recomputes the 20 determinants by fraction-free Bareiss elimination, rather than the supplied determinant routine;
- solves all 592 systems directly by Gauss-Jordan elimination before comparing their solutions with the coefficient formula;
- checks the resulting 13,088 equations;
- checks the single-active-factor formula on three additional pairs, totaling 39,264 additional evaluations;
- checks the geometric and angular arithmetic from separate closed forms.

The general identities follow algebraically: the matrix decomposition above proves the coefficient result for all (n\ge1); the geometric tail is a convergent geometric series; and the angular increments telescope. The extra finite evaluations are redundancy, not a substitute for these arguments.

The computation does not construct an infinite holomorphic function, choose Runge or Arakelian approximants, verify the topology of approximation sets, prove Hurwitz or Koebe-Gross, or establish an analytic existence theorem by testing examples. The reviewed files accurately state this limitation.

## 7. Scope and final disposition

The exact question, published solution, and transfer to the requested definition agree. The induction's geometric and analytic roles, the limiting deductions, and the countability argument withstand the checks above. The nontrivial historical approximation and boundary-distribution results remain credited theorem inputs.

Accept **`already_solved`, `1/5`**, with Carroll's 1979 Theorem 2 as the resolving result and no novelty claim. The artifact's existing `independent_review: pending` describes its pre-review state; the result of this audit may now be recorded separately or incorporated without changing the mathematical attribution. Original materials were preserved and no remote changes were made.

## References

1. F. W. Carroll, *A strongly annular function with countably many singular values*, Mathematica Scandinavica **44** (1979), 330-334. [DOI](https://doi.org/10.7146/math.scand.a-11814). [Publisher PDF](https://journals.msp.org/mscand/article/download/1834/1833).
2. A. Osada, *On the distribution of a-points of a strongly annular function*, Pacific Journal of Mathematics **68** (1977), 491-496. [Publisher PDF](https://msp.org/pjm/1977/68-2/pjm-v68-n2-p17-s.pdf).
3. W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, 2018, Problem and Update 5.50, printed p. 104, reference [145]. [arXiv record](https://arxiv.org/abs/1809.07200).
4. N. Arakelian, *Uniform and tangential approximation by holomorphic functions*, Izv. Akad. Nauk Armjan. SSR Ser. Mat. **3** (1968), 273-286. Cited as the external approximation theorem used in Carroll's Lemma A; its original proof was not independently reviewed.
