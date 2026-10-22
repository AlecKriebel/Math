# Independent structural and source-scope review

Date: 2026-10-21 UTC. Scope: row 1855, adjoint-free matrix approximation. This reviews narrow mathematical claims, not the whole exploratory problem and not priority. No overall resolution is asserted.

## 1. Source theorem and interpretation

Source: Halikias–Hochstenbach–Townsend, *Transpose-free linear algebra*, arXiv:2606.01335v1, Section 5.1, Theorem 5.1 and proof, https://arxiv.org/html/2606.01335v1#S5.SS1 . The locally recovered PDF's printed pages 16–17 were inspected. This is a preprint; journal publication was not established.

The attributed statement is real m-by-n input with n >= m, target 1 <= k <= m, Frobenius relative-best-rank error, finite factor gamma > 1, and success at least 2/3 for every input. Its proof rules out a worst-case query cap q < n. It does not prove expected query cost n, nor n calls in every execution. The Gaussian argument is valid but the adaptive-conditioning sentence requires its usual measurable-algorithm interpretation and an induction over observations. No defect invalidating the bounded-query theorem was found.

The full output matrix must be determined by the completed transcript and randomness. Stored factors qualify; a formula that still invokes the unknown A does not. A basis for the range alone does not recover the row coefficients.

For completeness, the mechanism is as follows. On A = e_1 g^T with g a standard real Gaussian, every rank-k approximation guarantee forces exact recovery because k >= 1. For a fixed random seed, each query asks one adaptive real linear functional of g. Conditional on prior observations, its component in the previously measured span is known; its orthogonal component either vanishes or supplies one new Gaussian scalar. Gaussian conditioning leaves a non-atomic residual on the orthogonal complement until the span has dimension n. A transcript-measurable output therefore has probability zero of exact recovery before n independent measurements. Integrating over the independent seed retains this conclusion. This is a single fixed hard distribution, not an adversarial vector chosen after seeing the seed.

A variable-stopping extension gives P(success and T < n) = 0 on this distribution. Consequently E[T] >= n P(T >= n) >= np if every input succeeds with probability at least p. Averaging over inputs gives sup_A E[T | A] >= np. Randomly reconstructing with n coordinate queries with probability p and otherwise returning zero matches np. This is an elementary consequence requiring its own stopping argument, not the theorem's literal statement. The stopping-time details are given in independent_review.md. The weaker statement that expected cost is at least n is false for p < 1.

Any-aspect-ratio, matching complex-field, spectral-norm, and arbitrary p extensions should be labeled separately proved consequences rather than attributed verbatim to Theorem 5.1. A complex-input proof uses a full proper complex Gaussian and complex-linear queries. A real Gaussian with complex queries does not justify n real-query units, since one complex query can encode two real queries.

## 2. Known row subspace: exact and approximate promises

Let V have d orthonormal columns in F^n, where F is R or C, and let P = VV*. Given the promise A = AP, the d queries forming Y = AV recover A = YV*. An optimal rank-at-most-k approximation is Y_k V*, with k-truncation interpreted as Y itself when k exceeds the available rank. The known subspace is essential information, not something supplied by a range finder. The exact expected-cost lower bound pd follows from the preceding rank-one hard family with g in F^d and row vector g*V*; the deterministic d-query algorithm mixed with zero-query failure matches it. For d = 0 the promise contains only the zero matrix and no lower-bound argument is needed.

Without exact containment, define B = Y_k V*, E = A(I-P), and F_0 = (Y-Y_k)V*. Then A-B = E+F_0 and EF_0* = 0. Thus

- ||A-B||_F^2 = ||A(I-P)||_F^2 + ||Y-Y_k||_F^2 <= ||A(I-P)||_F^2 + ||A-A_k||_F^2;
- ||A-B||_2^2 <= ||A(I-P)||_2^2 + ||Y-Y_k||_2^2 <= ||A(I-P)||_2^2 + ||A-A_k||_2^2.

The last inequalities use Y_k's optimality, testing against A_k V, and right multiplication by the isometry V being contractive. For spectral norm the squared inequality follows from (E+F_0)(E+F_0)* = EE*+F_0F_0*. These bounds do not assert a computable residual certificate from the d observations alone: the row-tail bound is a prior assumption or external certificate.

## 3. Common range and co-range: r queries, not 2r

Suppose A is square, rank r is known, and range(A) = range(A*). This includes normal matrices, but the condition is strictly broader. Let X have r independent standard Gaussian columns in the matching field, query Y = AX, and let Q be an orthonormal basis for range(Y). Then, almost surely,

    A = Y (Q*X)^(-1) Q*.

Proof: Fix an orthonormal basis U of the common range before drawing X. The kernel is its orthogonal complement, so A = U C U*, where C is invertible r-by-r. The square Gaussian U*X is invertible almost surely. Therefore Y has range U, so Q = UR for a unitary R. Then Q*X = R*U*X is invertible, and substituting Y = U C U*X proves the displayed identity. Only the original r oracle calls are used; all remaining matrices are known. This is an upper bound, not an asserted optimality theorem for the normal subclass. It assumes exact arithmetic and exact rank; the inverse can be ill-conditioned. With r = 0 the matrix is zero.

The initial two-batch 2r construction is valid but unnecessarily weak. No normality approximation or stability under noise is supplied by this proof. No novelty is asserted.

## 4. Constant drift: a restricted all-drift operator estimate

Let H = L^2(0,1), let c be real, and set L_c u = -u'' + c u' on D = H^2(0,1) intersect H_0^1(0,1). Let A_c = L_c^(-1). Integration by parts identifies L_c* = L_-c with the same Dirichlet domain. The real part of its weak quadratic form is ||u'||_2^2; Poincare's inequality and Lax–Milgram give invertibility in the weak formulation, while the constant-coefficient equation gives H^2 regularity for L^2 data.

For u = A_c* f, integration against u yields

    ||u'||_2^2 = Re <f,u> <= ||f||_2 ||u||_2 <= ||f||_2 ||u'||_2 / pi.

Hence ||u'||_2 <= ||f||_2/pi and ||u||_2 <= ||f||_2/pi^2. Since -u'' = f+c u',

    ||(-D^2) A_c*|| <= 1+|c|/pi.

Let phi_j(x) = sqrt(2) sin(j pi x) and P_s project onto their first s modes. The rank-at-most-s approximation

    B_s f = sum_{j=1}^s (A_c phi_j) <phi_j,f>

uses s forward function-oracle queries and retains their full output functions; it does not evaluate A_c again when applied to f. By taking adjoints and bounding the sine-series tail,

    ||A_c-B_s|| <= (1+|c|/pi)/(pi^2(s+1)^2).

The first-derivative energy estimate also gives the uniform envelope

    ||A_c-B_s|| <= 1/(pi^2(s+1)).

One may take the minimum of these bounds. Both hold for every real c, with no smallness assumption. This is a special one-dimensional constant-drift estimate, not the general multidimensional or variable-coefficient perturbation conjecture in the source. It is not a finite-precision numerical implementation certificate, and no literature-priority claim is established.

Relevant foundational source: Boullé–Halikias–Otto–Townsend, *Operator learning without the adjoint*, JMLR 25(364), 2024, Theorem 9 and the later perturbation discussion, https://www.jmlr.org/papers/v25/24-0162.html . The displayed constant-drift calculation is independently supplied here rather than attributed to that theorem.

## 5. Rank-one candidate ball and source-parameter caution

For a known unit vector u, let A = u v*, v nonzero, and assume |u*v|/||v|| >= a with 0 < a <= 1. The query Au = alpha u determines v*u = alpha, so v = conjugate(alpha)u+w with w orthogonal to u. The prior is exactly ||w|| <= |alpha|sqrt(a^(-2)-1). Thus the proposed candidate ball, diameter 2|alpha|sqrt(a^(-2)-1), and minimax radius |alpha|sqrt(a^(-2)-1) are correct. The center matrix is alpha uu*, not conjugate(alpha)uu*. When n >= 2, opposite residuals attain the diameter (including the trivial radius-zero case a=1). Operator and Frobenius matrix distances both equal the corresponding v-vector distance.

The source-parameter identification needs care. In the real rank-one case, minimizing distance of the scalar overlap to O(1) = {+1,-1} gives epsilon = 1-a. For complex scalars this equality uses unitary phases, not real O(1). The JMLR text literally uses O(k) and orthogonal terminology even in its complex setup, while its polar-factor calculations use conjugate transposes and appear intended as unitary geometry. This audit does not silently repair that source ambiguity. The safe presentation either restricts the comparison with the paper's parameter to the real case or explicitly defines a separate principal-angle/unitary complex model. Likewise, do not infer a verbatim complex EP reconstruction theorem from the source's zero-angle terminology. The independently proved EP formula above is unaffected.

The known u is part of the assumed information. If it is learned from an additional query, that additional transcript also constrains the candidate set, and the displayed ball is not automatically its exact candidate set. This exact slice does not close the arbitrary-X, higher-rank diameter gap in JMLR Remark 7.

## Draft audit and priority search

Inspected the complete five-approach draft at 2026-10-21 02:53 UTC. All five underlying mathematical arguments pass under the assumptions above; the complex source-parameter comparison required the qualification in Section 5. The final report includes the normal/EP construction, row-prior spectral inequality, and drift-uniform companion. For the known-row-space relative-rank upper bound, the reconstruction branch must output a rank-k truncation, not a possibly rank-d full reconstruction. Singular-value tails beyond the matrix dimensions mean zero.

A targeted search for normal-matrix single-pass low-rank reconstruction, randomized EP matrices, and the JMLR Nyström discussion found the already-inspected JMLR source, which explicitly discusses Nyström approximants in Section 3, Remark 2. This establishes strong reason not to market the elementary structured constructions as novel. The search did not establish exact priority for the EP formula, expected-query refinement, or constant-drift constants. No absence-of-prior-work claim is justified.

## Decision

The narrow constructions above are mathematically sound under the stated assumptions. Preserve the distinctions between source theorem, elementary extension, structured upper bound, and unresolved umbrella. Do not label these results novel, do not assert optimality for the EP/normal algorithm, and do not claim the general elliptic large-perturbation problem is resolved.
