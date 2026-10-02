# Independent adversarial review: 30005936

**Verdict: PASS for all five scoped mathematical results. No mandatory correction. Original broad source bundle remains unresolved5/5.**

Reviewed frozen FINAL_AUTHOR_MANIFEST.json SHA256 `d2e1df9dbe1ca6d60ed45bc9c67fa0fad31299778f53eb89703220b158dbcca7`, binding42files,43includingitself. In particular TURN_5.md SHA256 `99446e5409e160a3722419e36a3f5fbc2a7385d7520c45c57b67def9a0b616ee`. The verdict is an independent AI-assisted analytic/source audit, not a human peer-review, formal proof-assistant or novelty certification.

## 1. Exact source and prior-work scope

The complete Cohen contribution in [official OWR26/2024](https://ems.press/content/serial-article-files/49484), printed1495–1498, was checked, including visual inspection of printed1497. Its second setting is the Dirichlet space-time-white-noise equation and the frozen geometric-Brownian splitting formula with its old-state multiplier and independent sqrt(N)-scaled spatial Brownian cells. The superlinear example is explicitly exponent1.25. Thus the fixed-midpoint negative theorem addresses a substantive source question; it does not exploit a missing multiplier or replace white noise with a common Brownian driver.

The [published Bréhier–Cohen–Ulander paper](https://research.chalmers.se/publication/542281/file/542281_Fulltext.pdf), Assumption3, Proposition5, Theorem6 and Corollary7 were checked. Printed1326 was visually inspected. Its τ^(1/4) estimate is temporal against the semidiscrete solution; the continuum estimate is h^(1/2) under the one-sided restriction. The packet preserves this distinction. The negative result uses τ=h² and therefore survives either reading.

[Anton–Cohen–Quer-Sardanyons](https://arxiv.org/abs/1711.08340), Theorem2.1 and the following smooth-data paragraph, explicitly state the uniform h^(1/2) spatial estimate used in the additive/noiseless kernel reductions. The original Gyöngy source was not independently retrieved; that limitation and the intervening primary citation are accurately disclosed. [Mueller1999](https://arxiv.org/abs/math/9902126) confirms historical subcritical nonexplosion credit; the packet supplies its own quantitative cutoff argument instead of importing an unverified exit rate. [Ulander](https://arxiv.org/abs/2412.10800v3) uses a different exact-simulation LTE method with bounded invariant interval and smooth coefficient hypotheses. It does not establish the present frozen-coefficient unbounded-state claim. Related PR317 has a distinct common-noise setting and is appropriately credited without silently transferring its theorem.

## 2. Turns1–2: nonsmooth extension and quantitative high moments

The centered moving-average approximation is C1, preserves g(0)=0, has the same Lipschitz constant and uniform error≤Lε. The old-state-multiplied exponential is continuous through zero even if f=g/x is not. For a fixed mesh its Gaussian dominating variable has all finite moments; no mesh-uniform domination is needed. BCU's coefficient estimates use the common Lipschitz bound and bounded f. Passing the coefficient limit separately at each mesh preserves their uniform constant. The exact-solution stability convolution and positivity argument through a countable dense set are valid.

For turn2, the BDG/Minkowski inequality does not assume an independent random integrand. The killed discrete heat kernel has the stated eigenvalue and increment estimates; the time-integrated mode sums admit both sqrt(τ) and Nτ bounds. The spatial kernel comparison is imported only through fixed additive/noiseless coefficients, which avoids concealing a dependence on the variable L. Exponential weighting of the decreasing singular-convolution sum yields exp(C(1+L^4)); the numerical substep requires NL²τ≤1 and that hypothesis is retained.

The four-term error decomposition, integrable last-step singularity, and continuous spatial-error decomposition give the displayed high-p estimates. The finite grid maximum costs (MN)^(1/p); balanced refinement gives h^(−3/p), requiring p>6. The cap has L_R=(5/4)R^(1/4), so exp(CL_R^4) is exp(CR). These details justify the later growing cutoff rather than merely asserting favorable constants.

## 3. Turns3–4: exact exits and bounded-test convergence

For each bounded cutoff the conditional heat identity is integrable. Integrating against1 and using the killed semigroup makes unweighted mass a continuous nonnegative supermartingale, without assuming a spatial boundary derivative. Optional stopping gives its maximal tail.

Parabolic chaining counts O(2^(3j)) edges and yields a spatial exponent a<1/2−3/p, with amplitude-only factor R^(5/4). Its full deterministic-time-interval seminorm is measured before evaluating at the stopping time. Zero boundary values ensure that a height-R point has an entire two-sided interval on which the solution is at least R/2. The resulting mass estimate, Markov bound and parameter optimization give every q<1/2, and consistent cutoff stopping times yield nonexplosion. The proof does not infer second moments from this weak supremum tail.

The good-event induction for numerical cutoff agreement is valid because coefficients are frozen at old grid states; intermediate stochastic-substep overshoots are immaterial. Bilinear interpolation is a sup contraction and exact cutoff Hölder regularity adds only R^(5/4)h^(3/8). A sufficiently small logarithmic cutoff controls exp(CR)h^alpha, and its variance condition follows from h sqrt(log(1/h))→0. The final coupling gives uniform space-time convergence in probability and a logarithmic bounded-Lipschitz path-law rate on the explicitly bounded test class. It does not cover arbitrary one-sided mesh refinement or unbounded observables.

## 4. Turn5: full negative mean-square subquestion

The normalized first eigenfunction phi=(π/2)sin(πx) has integral1. Localized stochastic Fubini gives V=e^(π²t)∫phi u as a continuous nonnegative local martingale with bracket density e^(2π²t)∫phi²u^(5/2). The integral of the square, rather than the square of an integral, is essential for white noise and is correct. Weighted Hölder and ∫phi^(1/3)≤1 give sigma²≥e^(−π²t/2)V^(5/2).

The explicit barrier F(s,v)=v[1−(1+b)e^(−b)], b=8/(s sqrt(v)), satisfies F_s=(1/2)v^(5/2)F_vv, with F_vv=−b³e^(−b)/(4v). Its first two spatial derivatives extend correctly at zero. These identities and all needed endpoint limits were independently verified symbolically. With the decreasing deterministic clock c(t)=∫_t^t0 e^(−π²r/2)dr, the Itô drift has the sign
( sigma²−e^(−π²t/2)V^(5/2) )F_vv/2≤0.
Stopping both V and its bracket gives a true stopped stochastic integral. Removing the stops at each t<t0 and then taking t↑t0 uses nonnegative Fatou twice. No uniform integrability or unbounded random-clock sampling is invoked. The resulting strict loss E V_t0<V_0 is valid for every positive deterministic t0.

Conditional cutoff expectations yield killed-heat domination for the uncut field: eventual pathwise equality on compact rectangles and conditional Fatou justify the passage, including the almost-sure limit of the random initial heat term. Thus the nonnegative mean deficit propagates by the heat semigroup. The sine-series estimate uses |sin(jθ)|≤j sinθ and the exact geometric sum977/3375<1/2. It transfers the positive weighted deficit at1/2 to the specified midpoint at time1, rather than merely proving a deficit at an unspecified point.

For every finite numerical mesh, frozen Gaussian integration preserves the old-state first moment. Nonnegativity and induction justify Tonelli even if higher moments are infinite. Sampled sine initial data are a discrete eigenvector with lambda_N≤π². Hence every even N and every M have the same strictly positive lower bound δ_* on the midpoint first-moment error. The extended Cauchy–Schwarz inequality gives the stated lower bound on mean-square error under any coupling. Along M=N² it decisively refutes the quarter-order continuum mean-square extension for the exact source's power5/4 example.

This is compatible with turn4: rare large values prevent uniform integrability, while bounded tests still converge. The proof does not establish infinite coupled second-moment error, failure for bounded smooth tests, optimality of the logarithmic rate, or failure of other schemes.

## 5. Verification and disposition

All172 historical/final manifest entries and seven primary PDF hash bindings verify. All five author scripts replay byte-exactly:99,505 assertions. Separate controls give15,075 exact parameter/Gaussian/killed-semigroup/localization assertions and eight SymPy1.14.0 symbolic barrier checks. These finite checks supplement the analytic audit; they do not certify SPDE limit arguments by computation.

No mandatory author change is required. Publish, if authorized, as **unsolved5/5 for the full rough-coefficient/unspecified-weak-test bundle**, prominently preserving the complete negative fixed-midpoint mean-square subquestion and the positive bounded-test theorem. Classical and prior campaign ingredients should retain their existing attribution. No new discovery claim is warranted from this review.
