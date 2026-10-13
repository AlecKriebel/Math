# Independent flow audit of frozen PR #521

Reviewer: flow01. Scope: the scalar probability-normalized relative flow, its analytic foundation, exact second-base-derivative identity, and finite-time loss of total-space positivity. No prior audit is used as evidence. No branch, shared index, original source, publication, or external communication is changed.

## 2026-10-13 03:10 UTC — checkpoint 1 (25%)

Read the workspace AGENTS.md and the frozen public/PROOF.md. The target is treated as a hypothesis: a smooth positive metric on O(2,2) over P1 x P1 loses horizontal positivity under the precise flow d_t phi = log(MA(phi)/mu_phi), with both fiber measures normalized to probability.

The independent first derivation gives scalar right hand side log(g) + phi + log integral(e^-phi) - log integral(g). Its gauge behavior under adding a base function is consistent, and the central stationary fiber appears to close the true second variation into a linear nonlocal equation. These are provisional algebraic deductions, not yet an analytic validation.

Primary-source search: the publisher PDF URL in the proof returned HTTP 403 through the web tool. ArXiv Naumann 1710.10034 and Berman 1002.3717 are accessible. Berman explicitly separates normalized volume-density flow from the positivity-preserving non-normalized anticanonical flow. Next: read the exact Naumann definitions and finite-time regularity assertions, verify the normalized chart transformation, and construct independently checkable calculations.

## 2026-10-13 03:13 UTC — checkpoint 2 (75%)

Obtained and read the published Naumann paper directly from the publisher (the command-line download succeeded although the web tool returned 403). Verified probability normalization in equations (8), (10), (13), and the finite-time smoothness statement in Theorem 5. The P1 automorphism issue is only relevant to convergence assertions and does not obstruct finite-time wellposedness.

Independent deduction: represent the actual nonlinear solution as B(s) + F(z) + q(t, delta*p(s), z), where q(t,k) is the normalized fiber solution starting at k*x^2. Then the actual second-base jet is epsilon + delta*(partial_k q)|_(k=0). This reduces to an exact derivative equation with generator Delta_F + 1 - mean. Solving it in monomials, without using the draft's eigenfunction basis, gives w(0,t)=epsilon-delta*(1-exp(-2t))/6.

Adversarial source check: a product stationary Fubini–Study family plus a base weight contradicts the literal +r*c coefficient in Naumann's printed Proposition 4, eq. (14), for r=2. The defining flow gives +c. The draft avoids the source formula and remains correct. Parent notified of this source diagnostic, without transmitting it to any other agent or individual.

## 2026-10-13 03:19 UTC — final checkpoint (100%)

Completed INDEPENDENT_FLOW_REVIEW.md, including global determinant/frame/coordinate normalization; independently factored strict initial-positivity bounds; an explicit construction of normalized weights from the classical fiber curvature flow; finite-time parameter regularity and uniqueness; the exact nonlinear-family derivative; and the monomial solution with threshold exp(-2t)=3/4.

Ran the dependency-free check_exact.py. All 17 exact rational polynomial checks passed, with horizontal coefficient -1/96 at t=(log 2)/2 and initial pole derivative -1/12. The machine check explicitly does not claim to establish parabolic existence.

Verdict: no analytic blocker found. The strongest verified result is the full finite-time counterexample conditional only on established fiber Kähler–Ricci flow wellposedness. Exact remaining analytic gap: none found. Optional repairs: explain the printed source's scaling discrepancy with the pure-base diagnostic, and replace the isolated displayed nu/u inconsistency in the draft.

The parent supplied effort-local primary source receipts while this audit was under way. Temporary duplicate publisher PDF/text made by this reviewer were removed; only original review prose, the independent check, and its result are retained here. Original proof SHA-256 remained 4deb64c3b249dcf26a87ccdd222bad837e61f107b5304ed0e3ad2c6f1e444b36. No branches, original files, shared index, commits, pushes, releases, or external communications were changed.
