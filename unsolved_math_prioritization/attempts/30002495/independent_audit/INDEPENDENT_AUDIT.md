# Independent audit: real-variable Nyman criterion approaches

## Verdict and exact audited object

The mathematical propositions in the supplied packet are accepted as stated. No mathematical correction is required. The packet is a five-approach partial-results investigation of a methodological equivalence, not a proof of RH, a disproof of RH, or a solution of the requested equivalence. The appropriate disposition remains **unsolved, 5/5 approaches**. Work on RH itself remains outside this audit's scope.

A required, narrowly scoped software correction is supplied: the finite arithmetic checker used removable Python `assert` statements. Optimization can suppress every mathematical check while preserving the same `PASS` output and the same reported 23,767 groups. The corrected checker replaces all 16 assertion sites with explicit, always-executed checks. Its positive output is unchanged. The original unoptimized checks were replayed successfully; this defect does not invalidate the proofs or that particular recorded execution.

Input: problem 30002495 / OWR-12866-002, queue rank 986. The exact input manifest has SHA-256:

`6c41bb59af46e93ffdc169484847271bbec0a6fc178673d491cf8ec9e41244ea`

The input consists of the manifest and its ten inventoried files. All eleven original files were preserved byte-for-byte. This report is a fresh, AI-assisted independent audit, separate from the author's self-check. It is not human peer review or machine-checked formal mathematics. No helper reviewer was used and nothing was published by this audit.

## 1. Original question, conventions, and source scope

The primary source is Michel Balazard's contribution in [Oberwolfach Report 06/2014](https://ems.press/journals/owr/articles/12866), printed pp. 348–352. I read the surrounding survey and visually inspected printed pp. 349–350 in the publisher PDF. The question on p. 350 asks for a real-variable proof connecting formula (2), the all-positive-epsilon prime-counting error, with formula (3), weighted square-norm approximation by fractional parts. It is explicitly methodological. The source's index is a >= 1, and its target is the indicator of [1,infinity). The surrounding text identifies the half-line measure dt/t^2 and linear combinations. There is no stated coefficient-sum constraint and no axiomatic list of permitted real-variable tools.

The packet's exact formulation is therefore faithful. The supplied interpretation of “real variable” is clearly identified as a working interpretation, not falsely attributed to the source. Proving the two individual RH-equivalent assertions unconditionally would be a different task; none is claimed.

The convention repairs are valid:

- For p > 1, the bound min(t/a0,1)^p is integrable against dt/t^2. For a convergent parameter sequence, fractional parts converge away from a countable set of breakpoints. Dominated convergence proves norm continuity of a -> e_a. Consequently allowing or excluding a = 1 does not change the closed span.
- The choice of the target value at t = 1 has zero measure and no norm effect.
- Taking real parts does not increase approximation error to a real target, so real and complex coefficient versions have the same target membership.
- Below 1, any admissible finite combination f equals t C, with C = sum c_a/a. Its squared error norm on (0,1) is exactly |C|^2. Replacing f by f-Ce_1 imposes the coefficient constraint, and the stated triangle-inequality error bound follows. Conversely, constrained sums are already admissible sums. Under x = 1/t, the measure becomes dx and the corrected sums vanish for x > 1, giving the ordinary constrained formulation on (0,1).

Literature scope is also accurately limited. [Báez-Duarte, arXiv:math/0011254v1](https://arxiv.org/abs/math/0011254v1) contains the credited real integral implication, its subcritical converse, and the endpoint divergence statement. I inspected the introduction, definitions, Section 2's relevant lemmas/propositions, Section 3's proof, and the pertinent qualifications; this is not a full-paper referee review. [The seven-page strengthening preprint](https://arxiv.org/abs/math/0202141v2) was read in full: the finite damped family is classical, and its norm-convergence argument explicitly uses complex-variable machinery. The packet correctly credits the family and does not use that proof to fill its real-variable gap.

The [2025 Gallardo-Gutiérrez–Seco paper](https://link.springer.com/article/10.1007/s11785-025-01661-2) was checked through the abstract, introduction, Theorem 2.1 and its proof. These passages concern analytic spaces, Mellin-type testing against complex powers, and zeta zero-free regions. They do not supply the requested real-variable equivalence. No judgment about the correctness of the rest of that paper is made. Targeted later-literature searches did not locate a verified solution of the exact methodological question; this is a bounded search result, not a theorem of nonexistence. The Bdim catalogue fetch again returned HTTP 502; neither its inaccessible contents nor its search snippet was relied on as full-text evidence.

All three available source PDFs match the public metadata's byte counts and SHA-256 digests. Audit source metadata is in SOURCE_REVIEW.json. No third-party PDFs, screenshots, extracted text, or dataset contents are included in this audit folder.

## 2. Proposition 1 and the smoothed consequence

Accepted. The lower-end constants are correct, including x = 2:

1. Partial summation gives theta(x) = pi(x) log x - integral_2^x pi(t) dt/t. The Li_2 contribution is x-2. A prime-counting error O(x^(1/2+eta)) contributes O(x^(1/2+eta) log x), which is absorbed into the requested epsilon exponent by choosing eta < epsilon.
2. The reverse identity is pi(x) = theta(x)/log x + integral_2^x theta(t) dt/(t log^2 t). Substituting theta(t)=t yields Li_2(x)+2/log 2. Bounding the logarithmic denominators from below gives the claimed error estimate for any positive fixed exponent.
3. Prime powers of exponent >= 2 contribute at most floor(log_2 x) sqrt(x) log x. This elementary overestimate suffices because every positive power absorbs log^2 x.

The family quantifier “for every epsilon > 0” is essential and is handled correctly. The argument does not assert identical constants across epsilon or across changing test functions.

For the smoothed identity, apply Stieltjes integration by parts to integral phi(t/x) d(psi(t)-t). Compact support inside (1,2) kills the boundary terms; substituting t=xu removes the factor 1/x. This gives exactly the sign and derivative norm stated in the packet. The estimate is valid for a fixed compactly supported C^1 test function and sufficiently large x. It supplies no uniform bound for sharp cutoffs with growing derivative norms. This is a reduction of (P), not a bridge to closure.

## 3. Proposition 2: signed inversion and the absolute-value loss

Accepted, including signs and endpoints. The logarithmic derivation satisfies D(a*b) = (Da)*b+a*(Db). Applying it to mu*1=delta and using 1*Lambda=log gives Dmu=-mu*Lambda. Summing this finite divisor identity through x and partial summation produces

M(x) log x - integral_1^x M(t)dt/t = -sum_(n<=x) mu(n)psi(x/n).

The finite identity x integral_n^x t^(-2)dt=x/n-1 gives the exact second integral in (2.1). With R(y)=psi(y)-(y-1), the displayed signs agree. At integer endpoints the finite sums use <= and the single integration endpoints have no effect; x=1 also gives zero on both sides.

For 1/2 < beta < 1, absolute summation yields x^beta sum_(n<=x)n^(-beta), hence an O(x) bound. This does not imply the desired square-root-plus-epsilon cancellation. The packet properly describes a failure of this estimate, not an impossibility theorem for every real-variable method. Neither (P) nor the exact identity has been used to assume the missing Möbius estimate.

## 4. Proposition 3: full operator proof and endpoint qualification

Accepted for every 1 < p < infinity. I checked each transition independently.

### Operator and integrability

With t=exp(v), W_p f(v)=exp(-v/p)f(exp(v)) is an isometry, since dt/t^2=exp(-v)dv. Applying the same substitution to the integration variable gives convolution with k_p(v)=exp(-v/p){exp(v)}. The negative half-line integral is p/(p-1); the positive half-line integral is at most p. Young/Minkowski therefore gives precisely the stated norm bound p+p/(p-1).

For the actual summatory function M, local boundedness handles the integral over a finite u interval. Under (3.1), Hölder on the finite measure space ([1,infinity),du/u^2) gives integral |M(u)|du/u^2 < infinity. The large-u portion of the pointwise operator integral is therefore absolutely convergent. Compact truncations converge both in the input H_p norm and pointwise after application of the integral formula, identifying the bounded extension almost everywhere. No assumption about M at infinity has been slipped into the operator argument.

### Arithmetic identity and the constant I

For real s > 1 both Dirichlet series are absolutely convergent, so their product is 1 by finite divisor cancellation. The positive denominator sum tends to infinity as s decreases to 1. Partial summation of the Möbius series and domination by 2|M(u)|/u^2 then show I=integral M(u)du/u^2=0. This does not require analytic continuation or the prime number theorem.

For real v >= 1, sum_(n<=v)M(v/n)=1 follows by regrouping a finite divisor sum. Integrating against dv/v and changing variables gives integral_1^t M(u)floor(t/u)du/u=log t. Thus SM(t)=-log t for t>=1 and zero below 1, with the sign in (3.3) correct.

### Closed-span conclusion

For fixed R, norm continuity of u -> e_u on [1,R] permits finite-sum approximation to the H_p-valued integral against M(u)du/u. Its error is bounded by the uniform continuity modulus times a finite integral. Hence SM_R lies in B_p; boundedness and input truncation give L=-chi log t in B_p.

D_a has norm a^(-1/p) and maps e_u to e_(au), preserving B_p when a>1. The difference quotient (D_aL-L)/log a is exactly the stated ramp. It is bounded by chi in absolute value and converges pointwise away from the endpoint to chi as a decreases to 1. Since chi is in H_p, dominated convergence proves the final closure statement.

### Subcritical and endpoint scope

Assuming the additional Möbius bounds, choose eta>0 with p(1/2+eta)<1. This makes the power integral finite for p<2. It does not make the p=2 integral finite. Divergence of that majorant alone would not prove divergence of the actual moment, and the packet explicitly avoids this fallacy.

The escaping-mass example has exact moment (1/2)N^(p/2-1), so the claimed contrast between every fixed p<2 and p=2 is correct. It is an auxiliary sequence, not a claimed Möbius approximation.

The actual endpoint divergence is correctly cited. One small typographical trap exists in the 2000 source itself: the proof of its Proposition 2.2 writes a little-o assertion about F where the primitive of F is needed. Visual inspection confirms this is in the PDF, not merely the text extraction. The source's definition of its auxiliary H_p, Corollary 2.1, and Lemma 2.3 give the intended valid argument. If F(x)=M(x)x^(-2/p) belonged to unweighted L^p, splitting its primitive at a fixed A and applying Hölder on [A,x] would give integral_1^x F(t)dt=o(x^(1/q)). The cited critical-line-zero input contradicts that primitive estimate when p=2. Thus the citation's endpoint statement remains sound; the packet does not reproduce the source's typo.

Here the source's auxiliary function named H_p is distinct from the packet's weighted function space H_p. Critical-line zero information is credited background only. It is not an input to any claimed real-variable proposition or a completion of either missing implication. Since the actual M is not in the endpoint space, the p=2 conditional implication diagnoses a nonviable sufficient hypothesis for M. It is not a viable RH proof strategy as written.

## 5. Proposition 4.1: finite-tail annihilators

Accepted. Under W_2 the exact scalar is a^(-1/2), and the translation parameter is log a>=0; the span is genuinely unilateral. All dual pairings converge by Cauchy–Schwarz. Real Hilbert-space orthogonal projection gives the asserted target-membership test.

For the support proposition, C=integral_0^R f(t)dt/t exists because the second Cauchy–Schwarz factor is sqrt(R). Taking a>max(R,1) gives C=0. For a>=1, expanding floor(t/a) as a finite sum of indicators gives (4.2). On max(1,R/2)<a<R only the first tail can contribute. The tail integral is absolutely continuous there because the interval is bounded away from 0. Its identically zero value forces f=0 almost everywhere there. The reduced support bound can then be used again. After finitely many halvings there is no support above 1.

If R<=1 the conclusion is immediate. Nonzero below-one annihilators exist, as the packet notes; they have zero target pairing and are not separating witnesses. A genuine separator, if any, must have unbounded upper support. Truncating a putative separator is not legitimate because its infinite family of orthogonality conditions is not preserved.

## 6. Proposition 4.2: unilateral versus bilateral translation

Accepted. The given real exponential kernel is in L^1 and L^2. Its pairing with v after a nonnegative shift s is exp(-s)(1/2-(3/2)(1/3))=0. The target pairing is 2/3. At s=-log 2 the pairing is 1/8. The signs and constants are exact.

For the full-group argument, Cauchy–Schwarz makes each F_j(s) finite. Its convolution kernel has L^1 norm 1/j, so F_j is in L^2(R). The local absolutely continuous representation yields F_j'=jF_j-w almost everywhere. The equation F_1=(3/2)F_2 then gives w=3F_2, hence F_2'=-F_2. A locally absolutely continuous solution on the whole line is C exp(-s), which lies in L^2(R) only when C=0. Therefore the full translation orbit has zero orthogonal complement and is dense.

This is a genuine counterexample to a group-to-semigroup inference. It is not the Nyman kernel, is not a counterexample to the classical criterion, and provides no prime-error estimate controlling actual infinite-tail annihilators.

## 7. Proposition 5.1: unconditional local approximation

Accepted. For epsilon>0 the real inverse-series identity gives 0<A_epsilon<=epsilon by integral comparison for the denominator. Absolute summation from N+1 onwards gives the tail bound N^(-epsilon)/epsilon. These are bounds on an infinite, absolutely convergent sum; no interchange with the epsilon limit is assumed.

For N>=R>=1, expanding the finite fractional parts gives exactly (5.2). The floor identity follows by finite divisor inversion. The coefficient inequality 0<=1-n^(-epsilon)<=epsilon log n produces the stated uniform error on [1,R]. On (0,1), the squared weighted error integral is exactly |A_(epsilon,N)|^2, which is important because the measure itself is infinite near 0. The [1,R] measure is at most 1, so the triangle inequality yields (5.3). The condition N_j^(-epsilon_j)/epsilon_j -> 0 is sufficient, and restriction handles R<1.

For epsilon_j=1/j and N_j=ceil(exp(j^2)), the expression is at most j exp(-j). The rounding direction helps rather than hurts. This construction proves local convergence without assuming (P). It does not compute these cutoffs or establish a global norm bound. Attribution to the sign-changed reciprocal-coordinate classical family is accurate.

## 8. Proposition 5.2 and the final norm estimate

Accepted. Since ||chi||_(H_2)=1, the tail pairing is bounded by (C+1)||w 1_(R,infinity)||. Letting j increase for fixed R and then letting R increase proves weak convergence. A norm-closed linear subspace of a real Hilbert space is weakly closed, equivalently (B_2-perp)-perp=B_2, so membership follows. An infinite uniformly bounded subsequence retains the same local convergence; “subsequence” here must have indices tending to infinity, as usual.

For the explicit averages, weak convergence lets one choose each later index to make finitely many pairings at most 1/m in absolute value. The diagonal terms contribute at most (C+1)^2/m. The off-diagonal terms contribute at most 2/m. The bound ((C+1)^2+2)/m is therefore correct. The averages remain finite linear combinations of admissible generators. No algorithm for locating the subsequence is claimed.

Finally, scaling yields ||e_n||=n^(-1/2)||e_1||. Splitting its squared norm at 1 gives ||e_1||<=sqrt(2). Integral comparison of n^(-1/2-epsilon), for 0<epsilon<1/2, gives exactly (5.4). This bound grows along the stated diagonal and proves no uniformly bounded subsequence. The proposition is sufficient only; the packet does not assert that this particular diagonal must be bounded whenever (N) holds.

## 9. What remains unproved

The substantive gaps are correctly separated:

1. A real-variable prime-error-to-closure bridge.
2. The necessary signed Möbius convolution cancellation, or a different inversion avoiding the O(x) loss.
3. An endpoint argument that does not require the actually divergent Möbius H_2 moment.
4. Control of infinite-tail annihilators for the actual one-sided orbit.
5. A global H_2 bounded subsequence for the displayed locally convergent finite damped sums, if that route is to be used.
6. A real-variable proof of the reverse implication from closure to the prime-counting error.

No hidden RH assumption or complex-zero input repairs any of these. The source-based divergence diagnosis is compatible with the packet remaining unresolved. The five-approach count is a research-ledger count, not a count of five successful implications. Source checking and auditing are not extra approaches. No claim of mathematical novelty is established or needed.

## 10. Verification findings and precise correction

### V1: optimization removes the arithmetic checks

The original checker has 16 Python `assert` sites inside loops and at exact constant checks. Under `-O`, `-OO`, or an optimized interpreter selected through PYTHONOPTIMIZE, these expressions are not evaluated. Count increments and JSON output still run. A deliberately false exponential-kernel equality then emits output byte-identical to CONTROL_RESULTS.json, including its PASS and 23,767 groups.

There is an important distinction in the wrapper:

- Running `python -O verify_packet.py --replay` alone does not pass `-O` to its subprocess. Its arithmetic child uses the default optimization level unless the environment sets otherwise.
- Setting PYTHONOPTIMIZE=1 or 2 propagates to that child, so the original wrapper can report a byte-identical replay with all checker assertions disabled.
- Inventory rejection is implemented with explicit conditionals and survives optimization.

The supplied patch replaces each assert expression by `require(expression, label)` and defines require to raise AssertionError explicitly on false conditions. No proposition, coefficient, loop range, expected output, or arithmetic operation is changed. The corrected file is provided as check_controls_hardened.py; OPTIMIZATION_SAFETY.patch targets the original check_controls.py. Applying it changes a hashed file, so a derived packet must regenerate its manifest and obtain a new external digest. Do not overwrite the frozen original manifest or silently treat a changed file as the original audited input.

### V2: external manifest binding is a necessary trust boundary

The original verifier checks complete flat inventory, lengths, hashes, entry fields, path safety and regular-file status. It does not compare the manifest's own digest with an expected external value; it prints that digest. This is consistent with the manifest's declared scope, not an undisclosed proof guarantee. A coherently changed file plus a coherently rehashed manifest passes an unanchored verifier. The audit runner first enforces the exact external input pin and rejects that coordinated mutation. Hash consistency alone is not mathematical correctness or authenticity.

The separate rehashed false-check test intentionally leaves the external pin to isolate the optimization defect; it does not demonstrate a bypass of the pinned original packet. Ordinary single-file tampering is rejected by the original inventory checker before replay.

### Reproducible controls and their limits

AUDIT_CONTROL_RESULTS.json records full-domain output comparison for the corrected checker in normal, -O, -OO, PYTHONOPTIMIZE=1 and =2 modes; every output matches the original unoptimized 23,767-group result. The audit also forces each of all 16 checking sites false, individually, at optimization levels 0, 1 and 2. All 48 corrected mutations reject. The original rejects its 16 normal-mode mutations and accepts its 32 optimized mutations. Only the semantic-mutation runs use reduced positive loop domains for speed; every site is reached. Full unchanged-domain positive replays are separate.

The corrected checker was also installed in a temporary derived packet and tested through the original wrapper with PYTHONOPTIMIZE=2: full replay matched, all eight original inventory selftests passed, and a coherently rehashed false arithmetic condition was rejected. The full audit runner itself also completed under -O.

Twenty inventory mutation classes are tested at all three optimization levels, including the original eight classes plus manifest symlinks, directories, a FIFO, absolute paths, invalid byte types, malformed digest/schema/JSON and reserved manifest entries. All are rejected. The original eleven input files are rehashed at the end and must be unchanged.

INDEPENDENT_MATH_RESULTS.json records 2,068 separately implemented exact finite control groups, using a prime sieve for Möbius values, rational endpoint/floor and damping identities, escaping-mass moments, an actual nonseparating below-one annihilator, and exponential-kernel pairings. Their output was checked under normal, -O and -OO execution. These are supplementary finite controls, not substitutes for the analytic proofs above.

The original checks, corrected checks, independent finite checks, byte manifests and mutation tests cannot certify an asymptotic, an infinite-dimensional closure statement, RH, or the desired methodological equivalence. Acceptance is confined to the authored partial propositions, their accurately stated limitations, and the demonstrated correction to reproducibility.
