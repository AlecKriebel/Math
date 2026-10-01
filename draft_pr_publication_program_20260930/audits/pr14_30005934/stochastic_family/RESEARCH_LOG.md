# Independent stochastic-analysis audit log

## 2026-10-01 13:52 UTC — scope checkpoint (10% complete)

Target: exact PR14 snapshot `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`, candidate proposition for problem 30005934 / OWR-14298374-003. Work is confined to this audit folder. No canonical or Git changes, outreach, or paper creation.

Reviewed `CANDIDATE.md` as a hypothesis. Historical `independent_review` files and sibling audit findings are excluded from this independent analysis. The source metadata was inspected only for target identification; any included historical verdict is not used as evidence.

Audit success criteria: independently derive covariance positivity, finite-rank moving-test Itô identity, bracket normalization, bounded martingale and conditional-transform claims under the exact weak-solution assumptions; identify any counterexample or exact unresolved analytic gap. Scope excludes construction of solutions, full rank classification, and the earlier candidate's wider claims.

Initial algebraic checks: Riccati signs and factor four are consistent with the stated real Hilbert–Schmidt cylindrical Brownian normalization. Main outstanding checks are graph-domain approximation, random-initial stopping, original weak-solution definition compatibility, and external finite-dimensional theorem normalization.

Completion estimate: 10% toward a finished independent stochastic-family audit, not toward a novel discovery.

## 2026-10-01 13:58 UTC — analytic derivation checkpoint (50% complete)

Independently derived: (i) positivity of the bounded form covariance comes from continuity at zero, not positive-time injectivity; (ii) density of D(A²) follows using squared resolvents; (iii) D(A²) columns give C¹ paths in the D(A) graph norm; (iv) finite-span graph-C¹ approximations produce the moving-test rule by stopped Itô isometry and deterministic drift estimates; (v) scalar trace-noise integrand is `2 sqrt(X) v sqrt(Q)`, yielding bracket `4 tr(X v Q v) dt`.

Primary source consulted directly: the final Cox–Cuchiero–Khedher EJP paper, original OWR report, and Graczyk–Małecki–Mayerhofer arXiv manuscript. Their weak equation uses the same real Hilbert–Schmidt Brownian normalization and continuous trace-class paths. The candidate's weaker no-moment assumption does not impair stopped moving tests or the bounded exponential martingale.

Adversarial checks outstanding: concrete unbounded/noninjective models, non-trace-class covariance, heavy-tailed random initial data, simultaneous conditional transform versions, and clean reporting of the exact scope. No contradiction or central analytic gap found so far.

Completion estimate: 50% toward independent audit.

## 2026-10-01 14:04 UTC — adversarial models and alternate mechanism checkpoint (85% complete)

All eleven independently written exact-rational checks pass, including noise coordinate sums, nonsymmetric A with noncommuting Q, Riccati and log-determinant derivatives, negative-alpha exponential drift cancellation, and singular/nonsingular resolvent identities. These are finite algebra checks only.

Explicit hostile analytic model: H=L²(0,1), S(t)f(x)=f(x+t) with killing beyond 1, A=f' with f(1)=0, Q=I. The semigroup is noninjective at every positive time and nilpotent after time 1. Its covariance is multiplication by min(t,x), hence strictly positive in quadratic-form sense and non-trace-class. The candidate's finite-rank mechanism remains valid.

Found an additional independent necessity mechanism: whiten a finite positive-scale transform, exponentially tilt and rescale, then take a tight limit to its central determinant transform. A central transform's positive weighted determinant moment equals `2^-n alpha(alpha-1)...(alpha-n+1) (1+s)^(-n alpha/2-n)`. This identity can be derived by polynomial interpolation of its derivative expression from integer Gaussian Gram matrices. Choosing n=floor(alpha)+2 rules out every noninteger alpha>=0. This route does not need the imported theorem's rank classification or construction direction.

A fresh child adversary is checking conditional kernels/version continuity and the alternate tilting/determinant route. Report and verdict are being prepared; completion is not yet final pending that review.

Completion estimate: 85% toward independent audit.

## 2026-10-01 14:14 UTC — final checkpoint (100% complete)

Verdict: PASS for the exact narrow necessity claim. No central stochastic-analytic gap or counterexample was found under the candidate's continuous positive trace-class weak-solution assumptions. The checkable derivation in `REPORT.md` supplies the stopped graph-C¹ moving-test limit, noise bracket factor four, Riccati exponential martingale, and arbitrary random-initial conditional transform.

The fresh conditional/positivity adversary passes its entire assigned slice. Its independent determinant reviewer reconstructed the weighted determinant identity, with 144 exact rational Taylor-jet checks. This agent reran all 144 successfully and separately reran its own 11 exact-rational finite algebra checks successfully. The report clearly separates these computations from the analytic proof.

Additional verified necessity route: exponential tilting and rescaling produces a central finite matrix transform; the positive weighted determinant moment rules out every noninteger nonnegative alpha. The child report also verifies an unconditional random-initial tilt ratio that removes disintegration from this alternative. Neither route proves a solution construction or the broader rank classification.

Exact remaining gap in the narrow audited argument: none identified. Standard Brownian-with-respect-to-filtration meaning is required; stating it explicitly is optional clarification. Alpha=0 is correctly included, and a zero solution is not excluded through natural-number notation. Priority and publication classification remain outside this family.

Completion estimate: 100% of the independent stochastic-family audit. No outside individual contacted, no canonical source modified, and no Git operation performed.
