# PR 952 / 10400145 — independent computational route review

The first-jet obstruction and the polynomial-series arithmetic withstand this review. No correction to that finite algebra was found. The actual quantum-topological identification and printed source conventions remain inputs to a separate source/mathematical review; this report is not full-paper acceptance or a priority audit. The original whole-filesystem read-only replay was **not reproduced** on this macOS host.

The bound submitted head is `989a532ae1d50894190d010a0a02ba8c3d71ee05`, exactly the `claimed_solved` object in the eligibility gate. START.json and END.json authenticate all 33 original files against ORIGINAL_FILE_RECORDS.json, ORIGINAL_SNAPSHOT.json, their byte counts, SHA-256, disk modes, Git blob identities/modes, and bytes read from the immutable Git commit. Only copies inside this review's own tmp directory were executed. No original file, Git state, corpus, source PDF, or historical receipt was rewritten.

The exact question was read privately before candidate intake; INITIAL_ATTACK.md was saved and reread first. Its first paragraph discloses the mathematical hints already present in the assignment. Candidate code/manifests were then read before execution. Later reading of original audit reports was used to check scope statements; their acceptance grades were not adopted as evidence for this route.

## Independently checked mathematics

Let J_m(q)=product from j=1 to m of (1-q^j), and let R be the inverse limit of Z[q,q^-1]/J_m. Let E_N(t)=product from j=1 to N of (t-q^j), and S be the inverse limit of R[t]/E_N. These are the candidate's stated rings; their match to the primary source is outside this computational route.

Put D=Z[e]/e^2. The Laurent substitution q=1+e, q^-1=1-e kills J_2, so the projection to the second finite quotient of R gives a ring map T:R->D. It does not factor through the first quotient, because 1-q maps to -e, which is nonzero. No inversion of e, cancellation by e, or injectivity of a Taylor map is used. The same finite-level reasoning works after reduction to any commutative base ring, including rings with torsion. It also shows why localizing at q-1 destroys this argument: a unit cannot map to a nilpotent in a nonzero ring.

For any fixed N, monic division supplies a degree-below-N representative P(t)=sum a_j t^j for the Nth component of F in S. For n<=N, E_N(q^n)=0. Changing representatives and passing to a later coordinate therefore preserves evaluation exactly. Write T(a_j)=alpha_j+beta_j e. Since (1+e)^(jn)=1+jn e,

T(P(q^n)) = A+(B+nC)e,

where A=sum alpha_j, B=sum beta_j, C=sum j alpha_j. Hence the constant coefficient is independent of n and the linear coefficient is affine. This proof holds for arbitrary polynomial degree and does not approximate an infinite F by a polynomial globally. For any finite set of ranks choose one coordinate containing them all. For ranks 1,2,3 the second difference is zero. If F(q)=1, the linear values must be 0,C,2C.

The independently authored checker verifies this mechanism through 1,400 polynomial-in-n coefficient identities in rational polynomial arithmetic, 2,000 finite-characteristic monomial second differences (moduli 2,3,4,5,6,7,12,25), and 144 monic-node kernel tests. These are finite controls accompanying the general proof above. Extra higher-jet computations are diagnostic checks, not a separate claimed research result.

For the supplied Poincare expression define

s_k(q)=q^k (1+q+...+q^k) product from j=k+2 to 2k+1 of (1-q^j).

This polynomial is exactly the stated expression after cancelling its single denominator 1-q. The k=0 term is 1. For every k>=1 the remaining product has exactly k factors, each divisible by x=q-1. Its coefficient of x^k is

(-1)^k (k+1) product from j=k+2 to 2k+1 of j = (-1)^k (2k+1)!/k!,

which is nonzero over Z. Thus ord_x(s_k)=k for every k, including all omitted summands, without numerical sampling. In particular s_1=q(1+q)(1-q^3) has linear coefficient -6, and every k>=2 contributes zero to the first jet.

There is also a direct Habiro-ideal justification for passing to the inverse limit. With the Gaussian binomial polynomial,

s_k(q)=q^k (1+q+...+q^k) [2k+1 choose k]_q J_k(q).

The product formula for the Gaussian binomial gives this equality by cancellation; its polynomial character follows from the usual recurrence, which is also independently implemented in the checker. For each fixed m, all terms k>=m lie in J_m. The sum consequently defines an element of R, and the map T through R/J_2 receives no contribution from the infinite tail k>=2. This closes the distinction between a proved all-tail statement and a finite list of zeros. The program checks leading order through k=18 and the exact Habiro factorization through k=12 as controls, not as the proof for all k.

The resulting jet through degree six, independently calculated by finite polynomial arithmetic justified by that tail bound, is

1 - 6x + 45x^2 - 464x^3 + 6224x^4 - 102816x^5 + 2015237x^6.

It is a jet of the supplied series; identifying that series with the actual quantum invariant remains a topological input.

For the proposed coefficient formula f(n)=n(n^2-1)lambda, an exact polynomial calculation gives

f(r+2)-2f(r+1)+f(r)=6(r+1)lambda.

The supplied series gives the rank-two coefficient -6. Conditional on the topological bridge using this same parameter and normalization, lambda=-1, so ranks 1,2,3,4 give 0,-6,-24,-60. The first three have residual -12, contradicting the necessary zero; ranks 2,3,4 have residual -18. This agrees with the candidate's claimed contradiction.

Boundary tests distinguish genuine changes of hypotheses. Two nodes alone can be fit by P(t)=1+C(t-q); no three-node obstruction follows from only two values. Lambda=0 removes this first-order test but does not establish an interpolating invariant. A uniform nonzero rational parameter scale preserves a nonzero residual; changing q-1 to log(q) preserves the first coefficient. A rank-dependent scale 1/[n(n+1)] changes the cubic coefficients into the affine sequence n-1, and changes the question. Modulo a divisor of 12 the ranks-1/2/3 residual may vanish; modulo 4 or 12 a later triple can still detect failure. In characteristics 2 and 3 the integer n(n^2-1) vanishes for every integer n. The characteristic-zero obstruction is not asserted over all coefficient rings. None of these boundaries falsifies the stated Z-valued first-jet argument.

## Actual execution and trust checks

All original Python files use explicit checks, with zero assertion statements. Original author direct checks/bootstrap, algebra-audit runner, bridge finite algebra, and outer integrity mode succeed in isolated normal, -O and -OO Python. The original outer mutation harness independently reports 105 rejected negative controls and six successful positive controls. The raw fresh results, including each actual error and elapsed subprocess time, are in RUNTIME_RESULTS.json.

There are 118 recorded initial cases: **115 parent subprocess launches plus three external-pin rejections before execution**. An earlier progress message called these all launches; the correction is recorded in RESEARCH_LOG.md and REPLAY_SUMMARY.json. Initial summed subprocess time is 23.326670 seconds. Nested original harness launches are not added to that parent-launch count.

The cold matrix initially ran independent_math.py at SHA-256 a3bfaa513ad3c00d8a362c493943f16cf145b354faf0fb0e9412ccf899fd8c06. The checker was then enhanced with the Habiro Gaussian-binomial factorization controls. MATH_RESULTS_INITIAL.json preserves the earlier successful output. The final checker hash is ff44cdce74d36b40995843f7bc450e31fcac532163f3a411da51f3244ea82601. MATH_ADVERSARY_RESULTS.json records its fresh normal/-O/-OO reruns, five altered-mechanism mutations in all three modes, and the separately named profile tests: 52 further parent launches, 13.831193 seconds total. No historical receipt was substituted for a fresh result, and no failure was silently erased.

The five independent mechanism mutations remove a tail factor, change the cubic's linear part, omit the first nonconstant summand, rescale q incorrectly, and corrupt the Gaussian recurrence exponent. All are detected under all three optimization settings. Direct original-checker mutations also test cubic data, residual, rank offset, boolean/float confusion, vanishing/sign-changed Casson value, parameter, ring localization, quotient level, schema additions/deletions and malformed/duplicate/nonfinite JSON. Semantic tests bypass the manifest deliberately so rejection is not merely a stale hash. In contrast, stale-file, missing/extra namespace, FIFO, symlink and changed-verifier tests retain their original external anchors.

The original TEST_MUTATIONS.py intentionally refreshes disposable wrapper pins to reach malformed-manifest schemas. Those controls test parser behavior; they are not claims that attackers can alter trusted initial pins. Its receipt labels that distinction. The external initial original bootstrap anchors were checked before execution and changed outer-bootstrap copies were rejected without running them. The original nested checker inherits the requested optimization via its authenticated bootstrap. The original algebra audit also runs all three child modes itself; its direct semantic negatives do not inherit the outer optimization flag, so this review's separate all-mode direct negative matrix supplies that coverage.

Hostile working-directory modules and PYTHONPATH/PYTHONSTARTUP/PYTHONHOME settings did not execute the sentinel under isolated launches. No fake bwrap, package installation, symbolic-runtime borrowing, chmod surrogate for EROFS, or production publication step was used.

## Findings and exact remaining gap

**REQ-COMP-01 — unreplicated full Linux replay.** This host is macOS 26.6.2, CPython 3.14.6, uid 501; bwrap is absent. All three outer full-replay attempts and all three direct source-bridge attempts actually failed with FileNotFoundError for bwrap (errno 2). Therefore the original 72-control source-bridge run, its whole-filesystem read-only result, and errno-30 write probe were not freshly reproduced here. A real supported Linux environment with working bubblewrap, an unprivileged user, and its installed interpreter/stdlib trust roots is required before anyone claims a fresh original full-replay PASS. This is a required condition on such a claim, not evidence that the original program falsely passes on macOS: it fails closed as documented. Separately running the supported finite stages is valid and is labeled as such.

**REQ-COMP-02 — source/topology boundary.** Computation does not prove that the supplied Poincare series, n(n^2-1)lambda theorem, common quantum parameter and proposed inverse-limit ring are the exact ones in the primary sources and target conjecture. Those identifications must be independently source-checked before promotion of the full result. The original proof and reviews explicitly state that cited topological theorems are external mathematical inputs. This is a required boundary for interpreting this route's output, not a discovered error in those inputs. This route fetched no primary PDFs and made no literature/priority determination.

**OPT-COMP-01 — Unix modes.** Original integrity mode accepts a proof changed from 0644 to 0755 and a checker changed from 0644 to 0666, because its authenticated manifests bind bytes, not permission bits. This does not violate its advertised inventory/byte/hash promises, nor invalidate a historical unchanged-mode receipt. Exact mode binding is extra hardening, implemented in the new prototype and tested to reject both changes. Mode binding still is not a read-only filesystem.

**OPT-COMP-02 — ancestor symlinks.** Original integrity rejects a directly symlinked root and symlink members, but accepts an otherwise exact tree reached through a symlinked ancestor. Its code promises a nonsymlink root/member inventory, not complete ancestor rejection. The separately authored prototype chooses the stricter rule and has a direct rejection control. This is extra hardening, not a mathematical defect or a violation of a stated original trust guarantee.

**OPT-COMP-03 — precise platform documentation.** For a new package, identify the legacy full profile explicitly as Linux/bubblewrap and expose the supported portable profile under a distinct name/status. The prototype demonstrates this separation and never reports EROFS, source inspection or full-paper acceptance as passed. It is an own-folder prototype pending independent package-level review, not a replacement for the immutable submission.

The strongest supported result is the exact finite algebraic obstruction plus an all-tail derivation of the first coefficient of the supplied polynomial series, and successful supported replay/negative controls with externally anchored original bytes. The mathematical conclusion about actual invariants is conditional on the separate primary-source bridge. No computational route gap beyond that declared external input was found. The remaining portability gap is exact Linux/bwrap whole-filesystem read-only replay, which remains NOT_RUN here.
