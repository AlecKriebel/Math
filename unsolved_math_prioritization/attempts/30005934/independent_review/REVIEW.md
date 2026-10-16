# Independent review of the noninteger Wishart obstruction

**Verdict: PASS for the narrow mathematical claim and its match to the original question.** No substantive proof gap was found. The reviewed argument excludes every noninteger real parameter for continuous positive trace-class weak solutions with bounded positive injective noise, without assuming that the semigroup is injective. This is an independent AI mathematical review, not formal verification or human peer review.

**Reviewed document:** `CANDIDATE.md`, target 30005934 / OWR-14298374-003.  
**Reviewed SHA-256:** `bf8d8a5dda2bfe36cd0c28b4a2d0fe9ee1d2ff0365f286de8cc4bd4daa4ccf1d`.  
**Review date:** 30 September 2026. **Reviewer model:** gpt-6-astra, xhigh.

The conclusion was already explicitly claimed in an earlier unrefereed manuscript dated 22 September 2026. The candidate properly credits that source. This review supports neither a novelty claim nor the earlier manuscript's wider existence classification.

## Source and scope verification

The original [Oberwolfach report](https://ems.press/content/serial-article-files/49484), printed pp. 1478–1480, asks whether injective noise can allow a noninteger parameter for some unbounded generator. The same question is Open Problem 1.2, printed p. 5, in the [published Cox–Cuchiero–Khedher paper](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf). Its weak equation and continuous positive trace-class state space match those in the candidate. The latter does not impose the paper's extra moment and smoothing assumptions; the finite-rank proof supplies its own localization instead. The distinct degenerate-noise question is outside the reviewed claim.

The necessary finite-dimensional restriction is correctly imported from [Graczyk–Małecki–Mayerhofer, Definition 1.1 and Theorem 1.3](https://arxiv.org/pdf/1607.00206), published in *Stochastic Processes and their Applications* **128** (2018), 1386–1404. The positive-scale hypothesis is essential and is proved before application. The theorem applies to existence of a single probability distribution, so no Markov property of the compressed process is required. I checked the theorem statement, transform definition, scale discussion, and relevant necessity argument; this review does not formally reverify that paper's full proof.

The prior [versioned manuscript](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md), Lemma 3 and Corollary 2, contains the same finite-rank mechanism and narrow conclusion. Its [release page](https://evidencepress.org/releases/wishart-reachable-noise/) labels it unrefereed. The candidate's attribution and refusal to claim new priority are appropriate.

## Covariance positivity survives noninjective semigroups

For each nonzero fixed vector \(h\), positivity and injectivity of \(Q\) give \(\|\sqrt Qh\|>0\). Strong continuity at zero gives an interval of positive length on which \(\|\sqrt Q S(s)h\|\) remains bounded away from zero. Consequently

\[
\langle C_t h,h\rangle=\int_0^t\|\sqrt Q S(s)h\|^2\,ds>0
\]

for every \(t>0\). The interval and lower bound may depend on \(h\), which causes no problem. This asserts strict positivity of the quadratic form, not a uniform coercive bound on all of \(H\). On each finite-dimensional subspace, compactness of its unit sphere then gives a positive-definite compression.

There is no hidden use of injectivity of \(S(t)\). As an adversarial diagnostic, take the left shift on \(L^2(0,1)\) with \(Q=I\). This semigroup has a nonzero kernel at every positive time and vanishes entirely for \(t\ge1\). Nevertheless, \(C_t\) is multiplication by \(\min(t,r)\), which is positive almost everywhere. Exact interval-compression checks in the accompanying script confirm positive diagonal entries, including times at which the terminal semigroup is zero. This diagnostic is not asserted to provide a Wishart solution.

## Finite-rank Riccati calculation

Write \(B_s=S(s)L\), \(R_s=D_s^{-1}\). Finite-dimensional differentiation gives

\[
B_s'=AB_s,\quad D_s'=2B_s^*QB_s,\quad
R_s'=-2R_s B_s^*Q B_sR_s.
\]

The product rule for \(\psi_s=B_sR_sB_s^*\) yields exactly

\[
\psi_s'=A\psi_s+\psi_sA^*-2\psi_sQ\psi_s,
\qquad \phi_s'=\alpha\operatorname{tr}(Q\psi_s).
\]

All products involving the unbounded generator have the finite-rank bounded extensions stated in the candidate. No inverse of the semigroup appears. Since \(D_s\ge I\), none of these formulas becomes singular when a semigroup column is killed. The initial conditions are \(\psi_0=LL^*\), \(\phi_0=0\).

## Moving tests and localization

The use of \(D(A^2)\) is sufficient. This domain is dense for a strongly continuous semigroup generator; for example, squared resolvent approximations have range in \(D(A^2)\) and converge strongly to the identity. Semigroup invariance of the domain gives, for each column \(f(s)=S(s)l\), a continuously differentiable path in the graph-norm space \(D(A)\), with derivative \(Af(s)\).

Here is a precise version of the approximation underlying the candidate. Uniformly approximate the continuous graph-norm-valued derivative \(f'\) on the compact time interval by finite-span continuous functions, and integrate them with the exact initial value. The resulting paths \(f_k\) and their derivatives converge uniformly in graph norm. Together with the continuously differentiable finite matrix coefficients \(R_s\), they give finite-span tests \(v_k(s)\) for which the ordinary product rule follows from finitely many scalar weak equations. The quantities \(v_k\), \(v_k'\), and \(Av_k\) converge uniformly in operator norm to the required limits. The same holds for their adjoints.

Stop at the first trace-norm exit above \(m\), as in the candidate. On this stopped interval, drift errors are bounded by \(m\) times the operator-norm errors. For a self-adjoint test error \(w\), its scalar noise coefficient satisfies

\[
\|2\sqrt{X_s}\,w\sqrt Q\|_{\mathrm{HS}}^2
\le4m\|Q\|\,\|w\|^2.
\]

The Itô isometry, or its maximal inequality, therefore gives convergence of the noise terms. On the event that the initial trace exceeds \(m\), the stopped identity is trivial; alternatively one may first multiply by its complementary time-zero indicator. This handles random initial values without an integrable initial trace assumption. For every path and finite time horizon, trace-norm continuity bounds the trace, so localization exhausts the horizon almost surely. Thus the moving-test rule is justified and does not silently require a trace-class-valued semimartingale decomposition of the whole process.

## Quadratic variation and bounded martingale

For a self-adjoint test \(v\), the two Brownian terms combine into the scalar functional

\[
E\longmapsto2\operatorname{tr}(\sqrt Q\,v\sqrt X\,E).
\]

With Hilbert–Schmidt pairing \(\langle K,E\rangle=\operatorname{tr}(K^*E)\), its representative is \(2\sqrt X\,v\sqrt Q\). Therefore the quadratic variation is \(4\operatorname{tr}(XvQv)\,ds\), with the factor four and operator order used in the proof. An earlier draft named the adjoint as the representing integrand. That notational error did not affect the norm or the proof, and the reviewed hash corrects it explicitly.

For the exponent of \(F_s\), differentiating the backward time parameter gives drift \(-2\operatorname{tr}(X_s\psi_{T-s}Q\psi_{T-s})\). Half its quadratic variation is the positive opposite quantity. This checks both the sign and the factor in the cancellation.

On the fixed compact interval, \(\phi\) is deterministic and bounded. Positivity of \(X_s\) and \(\psi_{T-s}\) makes the exponential uniformly bounded even for negative \(\alpha\). The local martingale is consequently a true martingale. No unproved first-moment estimate or integrability of a global operator determinant is used.

## Conditional laws and theorem matching

The endpoint martingale identity first conditions on \(\mathcal F_0\). Its right-hand side depends on the time-zero information only through \(X_0\), so the tower property gives conditioning on \(X_0\). The positive trace-class cone is a closed subset of a separable Banach space and is standard Borel. The joint law of \((X_0,Y)\), with \(Y\) finite-dimensional, therefore admits a regular conditional law of \(Y\) given \(X_0\).

For one fixed dimension and horizon, intersect the probability-one sets for a countable dense collection of positive tests. On that event, the conditional Laplace transform and the displayed deterministic expression are continuous in the test, so equality extends to the full positive cone. This step does not condition Brownian motion on an individual initial realization or assume that such conditioning preserves a weak solution. It only conditions the already established fixed-time transform.

The determinant and resolvent identities remain valid for singular positive tests. With the notation of the candidate, the parameter match is

\[
\beta=\alpha/2,\qquad\Sigma=2C,\qquad\omega=b.
\]

Here \(C\) is positive definite and \(b\) is positive semidefinite. The imported theorem places no full-rank requirement on \(b\). Its extra rank condition in the discrete parameter range cannot admit a noninteger parameter outside the scalar set. The transpose-free order \(v(I+2Cv)^{-1}\) agrees with the source transform; it is also equal to the symmetric positive expression using \(\sqrt v\).

Negative \(\alpha\) is correctly eliminated before invoking the theorem: in dimension one, the power factor diverges as the test tends to infinity, while the noncentral exponential tends to a strictly positive finite limit. Such a function cannot be a probability Laplace transform. For a nonnegative noninteger \(\alpha\), any integer \(n>\alpha+1\) places it below \(n-1\) but outside the discrete integers, contradicting the theorem. There is no need to choose the same conditional null set for all dimensions, since a single obstructing dimension suffices.

## Independent exact checks

The accompanying `independent_checks.py` was written independently of the author's check script. All **19** diagnostics passed using exact rational and symbolic arithmetic:

- Three Riccati, determinant-derivative, and initial-condition examples, including nonnormal generators and a rectangular finite-rank test
- Three coordinate-by-coordinate Brownian coefficient and quadratic-variation checks
- Three resolvent and determinant identities with zero, singular, and full-rank positive tests
- Four left-shift covariance examples, including a zero terminal semigroup
- One Gaussian completion-of-squares normalization check
- Five noninteger parameter exclusions with exact obstructing dimensions

Reproduce from this directory with `python independent_checks.py`. The tested environment used Python 3 and SymPy 1.14.0. Results are in `independent_results.json`. These calculations can catch algebraic errors but do not replace the analytic argument or the imported distribution theorem.

## Final disposition

The reviewed candidate provides a complete negative answer to the narrow noninteger existence question under its explicitly stated weak-solution assumptions, which cover the original source setting. It is suitable for a draft research pull request together with its source and priority qualifications. No additional mathematical repair is required for this conclusion.

Do not describe this review as verification of the prior manuscript's general reachable-noise classification, an existence construction, strong uniqueness, a formal proof certificate, or a novel first resolution. The zero parameter is left in \(\mathbb N_0\), consistently with the zero solution and the explicit convention in the candidate.
