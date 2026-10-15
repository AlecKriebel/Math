# Independent adversarial audit: entropy family

**Verdict: PASS for the complete mathematical claim at the pinned head. No P0, P1, P2 or P3 actionable defect found in the submitted proof or its stated mathematical/source scope.**

Target: PR 1064; problem 30001073 / OWR-2090-026. Head: `bdefe31b9d226c8f27008d13f57775d5de8df3d7`. Full Git tree: `7f13a55b639ad35fc752603486c8b4168433c71a`. Review folder: `reviews/entropy_01`.

This is an independent reconstruction and attempted falsification of the submitted entropy/Gibbs mechanism, followed by a full downstream audit. It does not certify novelty, priority, a sharp constant, external human peer review, proof-assistant verification, or current worldwide open status.

## Custody and independence

Read root `AGENTS.md`, then submitted `PROOF.md` before other inherited conclusions. Immediately pinned all nine snapshots, the exact `SUBMITTED_PINS.json`, the actual commit object and full recursive Git tree. Each snapshot matches both its declared SHA-256/byte count and the actual blob at the head. These checks are in `INPUT_CUSTODY.json`; the original commit and tree records are `HEAD_COMMIT_OBJECT.txt` and `HEAD_FULL_TREE.zlist`.

The exact primary original problem was freshly retrieved and read in full before reconstruction. `INDEPENDENT_DERIVATION.md` was frozen at 2026-10-14T03:34:28.886925+00:00 with SHA-256 `0f83f15fd13f4c48c6921f991bf544d5ba6ddb5607ee6cf8a10c03834a7792cb`. No other submitted document contents or full prior-method paper had been read at that freeze. The arXiv abstract metadata alone had been opened. The frozen deduction has not been altered. All nine actual submitted files were subsequently read for consistency. No other approach-family results were read or requested.

All work and new files are confined to this review folder. No original file was repaired. No branch, index, Git mutation, publication, service configuration, outreach, other-worker contact or subagent action was performed. Full third-party PDFs, copied text and source images are private under ignored `sources/raw/`; source receipts and source-interface analysis contain safe authored metadata.

## Exact original target and accepted result

Fresh inspection of the [official original report](https://ems.press/content/serial-article-files/46191), printed pp. 2549-2550 (PDF pp. 73-74), confirms a fixed gamma>=1 and an **unnormalized** sum of squares bound on a nonnegative doubly stochastic matrix. The source asks for exp(-n) up to a polynomial factor and already gives the van der Waerden lower bound. It expressly distinguishes an entrywise gamma/n assumption.

The submission proves, for every nonnegative row-stochastic n by n matrix of positive integer order, with S=sum a_ij^2,

    per(A) <= exp(-n+e^4 sum a_ij^2 log(e/a_ij))
           <= exp(-n+e^4 S(1+log n)).

At zero entries the summand is its continuous value zero. For S<=gamma and n>=2, this yields

    per(A) <= n^(3e^4 gamma) exp(-n).

The original doubly stochastic target follows together with its already-known lower bound. The stronger upper theorem does not need column stochasticity. There is no lower-bound assertion for merely row-stochastic matrices. At n=1 the pure-power expression fails and the stated constant-prefactor bound is used correctly.

## Adversarial reconstruction of the central mechanism

1. **Actual joint law and chain rule.** An arbitrary finite law on permutations is paired with independent iid continuous uniform row priorities. For each fixed order, the conditional law q is considered only at histories of positive probability. The finite entropy chain rule then averages over the independent order without changing the marginal cross terms.
2. **Support and zero entries.** Every positive q_j has positive b_ij and lies in an unused column. Restricted marginal mass Z is positive, so r_j=b_ij/Z is a valid probability distribution on the unused columns with support containing that of q. KL(q||r)>=0 gives H(q)+sum q_j log b_ij<=log Z. Zero q and zero r entries cause no positive-coefficient log(0).
3. **Priority conditioning and Jensen.** Given a positive-support full permutation X and T_i=t, other priorities stay independent uniforms. Bijectivity of X and the row sum of B give E[Z_i|X,T_i=t]=b_i,X_i+(1-t)(1-b_i,X_i). Finite positive marginal support bounds log Z_i and justifies all averages. Concavity of log is applied in the upper direction. The integral is -1-b log b/(1-b); averaging the sampled marginal value contributes the second factor b. Thus g(b)=-b^2 log b/(1-b), with g(0)=0 and g(1)=1, yields the claimed entropy lemma. A deterministic permutation is an equality check.
4. **Gibbs identity and singular cases.** If per(A)=0 the positive exponential bound is immediate and no Gibbs law is used. Otherwise products normalized by per(A) define a genuine probability distribution. Positive Gibbs marginal b forces positive input a. Direct entropy substitution gives log per=H+sum b log a and hence log per<=-n+sum g(b)-D(B||A).
5. **Mass cancellation.** Both A and B have total mass n, so D(B||A)=sum d(b,a), d=b log(b/a)-b+a. This is a sum of nonnegative scalar divergences. In particular d(0,a)=a when a>0 must be retained; omitting marginal-zero/input-positive entries would break the exact identity. d(0,0)=0 is the only a=0 case that occurs. Column stochasticity is required only for B, where it follows from the permutation law.

The proof does not assume a sequential greedy sampler is well-defined on all sparse histories. A three-cycle-support example can lead a greedy marginal sampler to a dead end after individually permissible choices. That partial history has zero Gibbs probability, and the submitted conditional proof correctly excludes it. This is a source-interface subtlety handled by the candidate, not a defect in the candidate theorem.

## Complete downstream audit

The scalar bound g(b)-d(b,a)<=e^4 a^2 log(e/a) is valid for every permitted pair 0<=a,b<=1. The inequalities g(b)<=b and g(b)<=h(b)=b^2 log(e/b) follow from b log(1/b)<=1-b. If b>=e^2a, d>=b+a>=g. Otherwise nonnegative d can be discarded, and monotonicity of h plus b<e^2a gives the bound. The two regimes cover their switch line; b=0, b=1, a=0 and a=1 all have the stated values. Summation establishes the first permanent bound.

Row Cauchy-Schwarz gives 1<=S<=n. The exact normalized-square identity sum a^2 log(1/a)=(S/2)(H(p)-log S), p=a^2/S, and H(p)<=2 log n give the second bound. For n>=2, 1+log n<=3 log n. No stronger entrywise hypothesis or unsupported optimization is used.

The equal-uniform-block example is correct: for k blocks of order m, n=km, S=k and per=(m!/m^m)^k. Its Stirling asymptotic forces a polynomial power at least k/2 at gamma=k in the asymptotic sense and rules out a gamma-only constant prefactor. The candidate does not claim optimality of its displayed exponent.

## Prior-work interface and all-document consistency

Fresh version-bound [Anari-Rezaei arXiv:1811.02933v2](https://arxiv.org/pdf/1811.02933v2), complete section 4, equation (6), p. 12, gives the exact Gibbs-marginal/random-order precursor. The conditional Jensen integral in the submission turns that expression into its displayed entropy/KL bound. Therefore sections 2-3 are a self-contained derivation of a prior mechanism; the attribution is necessary and correct. The candidate appropriately locates its possible contribution in scalar absorption and the norm consequence without certifying novelty. Detailed safe receipts, version identities and the original-source mapping are in `SOURCE_INTERFACES.md`.

All nine submitted files are consistent with this accepted mathematical scope, the n=1 caveat, established-method credit, and the explicit novelty/priority limitations. The manifest's eight member identities and the audit manifest's proof/report identities match actual distributed bytes. `CONSISTENCY_CHECK.json` records these bindings. Their historical editing and removed-diagnostic statements were not replayed against unavailable original programs or pre-edition originals; this review supplies a fresh analytic verification of the pinned edition. Internal consistency is not authentication of every historical process claim.

## Fresh finite corroboration

Newly authored `finite_checks.py` uses exact rational matrix weights, Gibbs probabilities, marginal support and positive histories, with 120-digit Decimal evaluation of logarithmic expressions. It passed 11 matrix cases (orders 1-4, including per=0, non-column-stochastic inputs, positive-input/zero-marginal edges, sparse cycles, uniform blocks and near-deterministic inputs), 2 arbitrary permutation laws, 1,573 positive conditional histories and 201 scalar endpoint/switch-line probes. It checks chain identities, local KL support, the random-order inequality, the Jensen correction, total-mass divergence splitting and downstream bounds. Numerical tolerance is 1e-95; tiny negative roundoff slacks around 1e-118 are retained in the output.

`FINITE_CHECKS.json` binds the new executable hash and outputs. These are finite numerical corroboration with exact combinatorial probabilities, not an interval proof, universal extrapolation, proof-assistant certificate or replay of historical diagnostics. The universal acceptance rests on the frozen deductive reconstruction.

## Severity verdict and exact remaining gaps

| Severity | Findings |
| --- | --- |
| P0 | None. |
| P1 | None. |
| P2 | None. |
| P3 | None actionable in the submitted mathematical/source scope. |

No proof gap remains for the asserted bound or the exact original asymptotic target. The constant is loose but explicitly not optimized. Novelty, first-solution status, exhaustive literature coverage and present worldwide open status remain unestablished. No claim should promote this audit into certification of those matters. No change to the original files is requested by this family.

Audit goal completion: **100%** for independent verification of this head and assigned mechanism. Mathematical target proof completion: **100%** within the stated scope; novelty is **not assessed** as a completed discovery goal.
