# Independent reproduction and adversarial audit: PR 458 / 20000693

Reviewer `/root/pr458_reproduction`. Frozen head `87a39f7b4e5ef81aacf98464f86586cc95684d7f`. Review completed 2026-10-12T18:01:29.279824+00:00. Author source bytes remain untouched. This family performed no original proof-search attempts, remote writes, status actions, publication, index or checkout operations, or external communication.

**Finding: the scoped heuristic's analytic bookkeeping is sound, but its current verification entrypoints have one publication-blocking defect.** All 19 deliberately invalid historical executions per mode are rejected normally and accepted under inherited `PYTHONOPTIMIZE=1`. Current publication also needs two presentation/citation correction groups. Raw findings are retained; fresh checks do not upgrade historical controls to valid ones.

## Scope and independence

The AIM primary section page was freshly retrieved by HTTP, 33,521 bytes, SHA-256 `e61d05b854171b45265d2f316e6d08702cb210a3e4f8a3ad2d87b79360df5484`, exactly matching historical provenance. The selected object is Problem 5.3, attributed to C. Turnage-Butterbaugh. It asks to develop a heuristic for imprimitive/product L-function moments and gives an unshifted Dirichlet-product example. It supplies no demand for a proved general high-moment asymptotic. Fixed finite moduli and weights, a t-aspect interval and nonnegative powers are the candidate's explicit scope choices. They must remain visible.

`INDEPENDENT_RECONSTRUCTION.md` was written before reading the historical `REVIEW.md` or `DISPOSITION.json`. The author candidate and verification source were inspected before reconstruction: this is independent mechanism and judgment, not a blind replication. After that checkpoint the entire historical review, all manifests, all mathematical verifier source and documentation were read. The historical author's verifier and review copy were checked for exact byte equality. No present sibling-family verdict influenced this family's reconstruction. Root primary citation evidence was read only after the independent numerical and analytic mechanism had been implemented.

Acceptance here means a coherent leading model for fixed, finite unshifted Dirichlet products with fixed nonnegative real weights. It does not certify actual L-function high moments, distinct-factor zero independence, prime/zero splitting, growing-cutoff exchanges, uniform growing conductors or weights, shifts, negative powers, all lower-order terms, general higher-degree products, or first mathematical priority. Those exclusions match the candidate's disclosure. Deep priority and operational disposition are not this family's tasks.

## Frozen inputs and manifest coverage

All 27 frozen objects match `SOURCE_RECEIPT.json` at entry and final recheck. The author script and its review copy are byte-identical; author report and both retained replays are byte-identical; reviewer report and stdout are byte-identical. The three overlapping public/author/review manifest groups contain 46 extant file records, all verified. Counting overlapping records does not imply 46 distinct files.

Nineteen historical records are absent from the public packet: seven author source records, eleven review source-input records and the explicitly excluded review source-text extraction. These are marked **unavailable and not currently verified from the packet**, not silently accepted from historical `matched:true`. Separately the historical input-integrity ledger has ten extant currently verified author files and seven absent source objects. The freshly fetched AIM page verifies one historical foreign source independently; this family did not fetch the other historical PDFs or extractions. The referenced final-packet manifest with hash beginning `62bb3afa` is absent as an object and is not re-certified. These deliberate omissions are not source corruption.

The root separately retrieved and inspected literature; `ROOT_CITATION_EVIDENCE_READBACK.json` records which entire root receipts this family read and their hashes at reading time. Their primary-PDF visual assertions remain root provenance, not this family's independent source-image inspection. No foreign full text, extraction or image is in this family's positive public list.

## Independent analytic reconstruction

For actual local character values c_i=chi_i(p), the analytic branch at zero of B(z)=product(1-c_i z)^(-a_i) has logarithmic derivative

    B'(z)/B(z) = sum_{k>=1}(sum_i a_i c_i^k) z^(k-1).
    n b_n = sum_{k=1}^n (sum_i a_i c_i^k) b_{n-k}.

The fresh implementation uses pairs of exact `Fraction` values for Gaussian rationals. A separate binomial-convolution implementation agrees through degree twelve in 100 input/prime cases. These finite agreements supplement the displayed general generating-function derivation. For A=sum a_i, the coefficients satisfy |b_n| <= d_n=(A)_n/n!, because nonnegative weights give a coefficientwise majorant `(1-z)^(-A)`. This proves absolute local convergence on |z|=p^(-1/2), permits Parseval and yields the positive local phase mean J_p. The n=1 term is |sum a_i chi_i(p)|^2/p. Since p>=2, the remaining series is uniformly O_a(p^-2), with bound sum_{n>=2} d_n^2 2^{-(n-2)}, a finite fixed-weight constant. This does not make an assertion about moments on the critical line.

Equality of primitive inducers is the correct grouping. Their weights add before squaring, E=sum M_psi^2. Different labels and different deleted Euler factors do not imply distinct primitive zeros. Nonreal conjugate primitives remain distinct unless equal. A quotient character on the lcm of their conductors is nonprincipal by uniqueness of the primitive inducer; finite character witnesses only corroborate, rather than prove, that general fact.

The common-modulus lift must restore **inverse** Euler factors at primes dividing the auxiliary Q but not the original q_i. The original local coefficient series and restored common-modulus series coincide exactly. Deleted prime factors share the same phase: two local values 1 and -1 have mean 1/(1-x^2), not 1/(1-x)^2. The zeta/principal-mod-2 example has E=4 and local ratio1/6. Conjugate classes cannot be merged to force exponent4 in the equal-weight example. Zero weights can be omitted, including at zeros; all-zero input has integral exactlyT and both constants1.

At good primes the p^-1 term in J_p consists of diagonal E plus cross terms. The positive real factors (1-1/p)^E and |1-rho(p)/p|^(2M_psi M_phi) cancel these terms. Each H_p is positive and1+O_a(p^-2), so its product converges absolutely to a positive finite value. The remaining increasing-prime Euler limits at1 require the standard fixed-modulus prime number theorem in arithmetic progressions, not just an unsupported inference from L(1,rho) nonvanishing. It supplies convergence of the first-prime sums; higher powers converge absolutely. Isolating the finitely many nonzero partial L-values gives the submitted positive arithmetic constant. Its finite bad-prime ratio to the primitive-core constant is an identity of the defined constants, not a theorem transporting actual asymptotics.

The CUE finite product rewrites exactly by the Barnes recurrence as

    C_N(m) = [G(1+m)^2/G(1+2m)]
             G(N+1)G(N+1+2m)/G(N+1+m)^2.

The known Barnes asymptotic supplies N^(m^2). There is one such factor per positive-weight primitive class. The cutoff powers from the prime and zero models cancel to E. Fixed conductor logarithms are leading equivalents of logT; they do not determine lower-order coefficients or justify growing-conductor extrapolation. These are analytic/model normalizations. The correspondence of actual primitive zeros to independent matrices and the weighted prime/zero splitting remain assumptions, openly declared by the candidate. The final clarification layer correctly distinguishes Sahay's intermediate GRH premise from its formal conditional hypotheses.

## Historical positive replays

An isolated environment uses Python3.14.6, SymPy1.14.0 and mpmath1.3.0, the actual recorded mathematical-library versions. Scripts that write their own reports were copied to private directories, never executed against frozen paths. Environment inheritance supplies `PYTHONOPTIMIZE=1`; it is not replaced with an untested merely advertised mode.

Eight actual baselines were executed: author, reviewer, publication hash check and publication `--replay`, each in normal and optimized mode. All exit0. Author output and generated report are exactly the frozen2,570-byte report, SHA-256 `e3965d19d1aeb0e013c0aacb3cc2a6704082b9f51302a8a5e079b6b0fb5e9f8c`, reporting966 checks. Reviewer output and generated report are exactly the frozen4,132-byte report, SHA-256 `227ebf38aa91492fb468680d44daa36324629e568d6a5ca8b4faafc677d89af2`, reporting380 cases. Both publication outputs also match across modes; ordinary publication output SHA begins `ddb394b0`, replay output `473fe0ae`. These positive passes do not show that the predicates remained operative.

The author966 count includes coefficient-level increments, whereas reviewer380 counts one input/prime or matrix case. They must not be added as a uniform theorem certificate. Both disclaim L-function moment verification, accurately. The historical suite records twenty fractional CUE Toeplitz cases and eighteen local phase cases; their finite numerical tolerances have no rigorous floating-error enclosure.

## V1: actual false acceptance under optimization

AST inspection finds13 `assert` nodes in executed author code,24 in reviewer code and12 in the publication verifier. The identical unused review copy has another13 physically duplicated assertions. Optimization removes the operative predicates, while status and counts remain `PASS`.

The initial18-case batch executed36 actual subprocesses. Eight mathematical variants deliberately impose wrong deletion ratios, omit modulus restoration, merge primitive or conjugate classes, use the wrong Barnes constant, or substitute independent local expectations. Ten packet variants alter a same-size source byte, a byte count, an unlisted file, rehashed theorem/novelty/status/turn-budget fields, a frozen manifest, a forbidden source extraction sentinel, or a frozen expected report. Every case is rejected normally and accepted with `PASS` under optimization. All eight invalid mathematical scripts emit exactly the original frozen PASS report.

The initial expected-report mutation was originally labeled a replay-mismatch probe, but normal rejection occurred earlier at the frozen author verification digest. That label is not evidence for reaching the generated-report comparator. A refined additional probe therefore preserves source bindings, corrupts the **actual isolated subprocess-generated report** and reaches the comparator: normal stderr ends `author/verify.py: replay report differs`, while optimization returnsPASS. The complete initial artifact, refined one-case artifact and an aggregate retain this history and the corrected mechanism label. Total actual negative executions are19 per mode: normal19 rejected, optimized0 rejected and19 falsePASS. The public recipe includes both distinct mechanisms. Private fixtures contain only authored sentinel data or modified public target scripts; no foreign extracted source text was copied into a fixture.

Required repair: replace publication and mathematical `assert` predicates with explicit fail-closed guards, or reject optimized mode before successful output. Require actual normal/optimized subprocess negatives for both mathematical claims and hash/scope/report-integrity controls. A fresh passing mathematical audit does not repair the historical publication verifier, and positive byte equality does not resolve V1.

## Fresh checkable audit

`verify_independent.py` uses explicit `require` guards and reports673 cases in each mode. Both complete JSON outputs are byte-identical,40,017 bytes, SHA-256 `2b39e563cd5030eb4ad9aceb5e66b0b4c6f62fc22e09f18ccf238c2a3b87c796`. The nine actual mutated subprocesses per mode all reject in both modes, covering primitive/conjugate collisions, deletion, local correlations, Barnes normalization, a false theorem flag, missing inverse restoration, wrong regularization sign and negative weights.

The673 case families are:100 recurrence-versus-binomial comparisons,100 lift identities,100 primitive aggregations,100 zero-omission identities,77 good-prime regularizations,76 complete table multiplicativity checks,10 finite distinct-primitive witnesses,7 boundary/normalization cases,18 local tail/quadrature cases,40 exact integer CUE Toeplitz cases,18 fractional Fourier cases,18 fractional determinant cases and9 finite Barnes-quotient cases. These are independently defined case counts, not author966 units and not theorem counts.

Each local numerical case uses exact rational coefficients through degree224 and an exact positive tail bound. With d_n=(A)_n/n!, the first omitted term is d_(N+1)^2/p^(N+1); the successive ratio is bounded by

    R=max(1/p, ((A+N+1)/(N+2))^2/p)<1.
    remaining tail <= first_omitted/(1-R).

The ratio bound follows by monotonicity when A>=1 and by its limiting bound1/p when0<A<1. A=0 gives tail0. The1,024-node periodic trapezoid rule has a separate exact analytic bound. On the Laurent annulus with radii5/4 and4/5, p>=2 gives1/sqrt(p)<3/4 and |F(w)|<=40^ceil(A). Cauchy coefficient estimates and aliasing give error <=2*40^ceil(A)/((5/4)^1024-1). The report includes these exact rational bounds. The mpmath evaluations and their rounding are **not interval-certified**. Maximum observed phase discrepancy is4.80929004518e-67; it is corroborative agreement, not a claim of a validated floating enclosure.

Integer CUE weights0 through4 and sizes1 through8 use exact Fraction Toeplitz determinants and factorial products. Fractional weights1/4,1/2 and7/4 use numerical Fourier integrals versus the closed reciprocal-Gamma Fourier coefficients, determinant versus finite Gamma product, and finite Gamma versus Barnes quotient. Maximum observed fractional determinant relative discrepancy is1.17723828025e-70. No actual Dirichlet L-function high moment is evaluated or certified.

## P2 and C3: publication presentation corrections

P2: the current README requiresSymPy1.13.1 although both frozen reports actually record1.14.0. Strict report-byte comparison binds the version field, so the prescribed version is inconsistent with the frozen expected outputs. Use SymPy1.14.0 and mpmath1.3.0 in current replay instructions. The addendum references absent `START_HERE.md`; the current entrypoint is `README.md`. Correct that reference if a publication proceeds.

C3: root independently retrieved the official Keating–Snaith PDF,289,778 bytes, SHA-256 `097f78ed43e8427864a4566b5448a92eecca901b73a64c0d970c296aa90a42c8`, and visually read printed59–60. Its reported citation correction is finite CUE equation6 and Barnes leading equation15; historical SOURCE_GATE equations10–12 concern cumulants. This family read the entire root receipt/reconstruction and independently verified finite CUE/Barnes identities, but did not visually inspect that PDF or independently certify printed numbering. Correct the citation in a current publication and retain the historical peer report's explicit source-cache limitation. Neither presentation group changes the submitted mathematical formula.

## Disposition and exact gap

`RESULT.json` retains integer blocking_issues1, required_repairs3 and unresolved_mathematical_gaps0 **within the openly heuristic target**. Required corrections are V1 explicit verification guards, P2 dependency/entrypoint instructions and C3 root-established citation numbering. The model's unproved assumptions and general moment asymptotic are not silently counted as proved or as resolved theorem gaps: they are intentionally outside a heuristic-level theorem claim and remain disclosed conjectures.

No new mathematical priority, literature exhaustiveness or first solver is certified. No operational helper, status correction, merge, paper or Zenodo/tracker action is approved by this family. A narrow classification based on sound analytic bookkeeping and independently verified prior coverage would not rely on the broken verifier; its scope must be reviewed separately and raw V1 retained. If the problem becomes excluded by the user's queue rule, this report does not request additional source repairs or processing afterward.

Reproduce with the pinned environment by running `replay_historical.py`, `test_historical_negative_controls.py`, and `run_independent_controls.py`. They write only this reviewer's outputs and ignored private cases. Historical negative semantic outcomes reproduce; diagnostic paths and refined-probe history are not advertised as byte-stable. Fresh normal/optimized mathematical JSON outputs are byte-stable in the pinned mpmath version. The final positive public manifest enumerates only authored safe artifacts and excludes its own self-hash, private fixtures, environment, caches and foreign sources.
