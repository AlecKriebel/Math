# Independent review:30005042 branching-process partials

## Verdict and binding

**PASS_SCOPED_PARTIALS. Original target remains unsolved after five substantive author turns. No mandatory mathematical correction identified.**

This report binds the43 author artifacts listed in FROZEN_MANIFEST.json SHA-2568362e7215e8afb2fd5922f66b61ba3dc457039c61235f4030c17c50e55bb8c36. RESULT.md has SHA-2565313b4b00a0a2db70209b54c9480d96cb35ce4ea79bb2c7f167f9de2eb113ad9; PROOF_COLLECTION.md has SHA-2567e1c3119d59b44857739cb9c5e5cecfe35a0827909943b346290b3162e1ed913.

The reviewer did not contribute to the author's proof route. The full five written proofs, original source context, exact coupled model and the cited classical inputs were audited. This verdict certifies the stated restricted arguments, not historical novelty, the exact-endpoint J1 theorem, or a complete description of the source limit processes.

## 1. Original target and source scope

The original OWR12/2022 contribution, printed592–593, was inspected visually. It asks for a weakening of the moment hypothesis in a functional convergence theorem and for a description of the limiting process law. The inspected full Mailler–Marckert arXiv2106.01426v1 fixes independent copies of one nondecreasing integer-valued càdlàg offspring process with mean parameter lambda. The generation recursion couples all parameters through the same offspring copies. The relevant topology is local Skorokhod J1 on compacts strictly above1, with convergence in probability. Scalar Kesten–Stigum and finite-dimensional convergence do not alone settle this.

The manuscript already contains finite-variance smoothing uniqueness, scalar geometric laws and the process fixed-point equation. These are credited. Open question1 on printed15 asks for simple binary/geometric/Poisson process descriptions. The packet's integrable uniqueness and bivariate geometric formula are substantive scoped results, but do not automatically close that request.

The three mathematical PDFs hash-match. The fourth, excluded Bath download, really has a target bibliographic cover and an unrelated *The Stable Graph* body. It was not used as mathematical evidence. The absence of an inspected final2022 mathematical edition remains disclosed. No claim of exhaustive current openness is certified.

## 2. Turn1: integrable smoothing laws and integrated convergence

The nested Ulam construction preserves the actual joint recursion, not merely the separate parameter marginals. At any generation, ordering active vertices by their first ancestral appearance gives nested initial segments; the unused offspring-process copies are independent of that ancestry-measurable ordering. Conditional exchangeability then gives the same transition kernel as the original generation array. Finite parameter laws and càdlàg measurability justify the process-level identification used later.

The terminal-mark averaging estimate is valid with only an integrable seed: after centered truncation atK, conditional Cauchy–Schwarz uses E sqrt(Z)<=sqrt(EZ), and the discarded part uses EZ=m^n. No second population moment is introduced. Applying this to each coordinate yields the claimed W1 approximation to the normalized population vector.

For a fixed mean-one integrable law, every iterate has the same law. Its closeness to the martingale population law forces that constant law to be the scalar-limit vector law, and hence forces mean one. Classical Kesten–Stigum supplies the necessary and sufficient XlogX condition. Conversely, under that condition the finite-child root decomposition and L1 convergence prove existence and uniqueness. The arbitrary finite nonnegative mean-profile classification correctly removes zero coordinates and rescales only positive ones. It does not claim arbitrary profiles preserve càdlàg paths.

The expected L1-function convergence follows by joint measurability, scalar L1 convergence and the uniform bound2 on expected absolute error. The random L1 element is legitimate by Fubini and separability. Its distinction from J1 convergence is correctly demonstrated by the shrinking-spike control, which is not misrepresented as an offspring counterexample.

## 3. Turn2: the monotone-process maximal inequality

The threshold argument is sound. After fixing deterministic nonnegative monotone curves and their endpoint weights, independent threshold indices represent their cumulative values. Conditional Jensen applies to the maximum norm to the powerp. Sorting thresholds independently of the signs converts the threshold sum into partial sums of a finite Rademacher martingale, including ties. Doob's Lp inequality and, for1<p<=2, the pointwise inequality (sum w_i²)^(p/2)<=sum w_i^p give the stated bound. Averaging afterwards requires only p-th endpoint moments; no hidden second moment of the random envelope is used.

The symmetrization factor2^p, and hence C_p=(2p/(p-1))^p, is valid. Passing through dense finite grids is justified because the processes and their dominated mean functions are càdlàg.

At generationn, conditioning on the past makes the activation thresholds deterministic, while the next offspring copies stay independent. The random number of active parents is finite; averaging the conditional inequality uses only EZ_n(b)=b^n. The ratio b/a^p yields absolute summability on sufficiently short intervals. A finite partition works because a>1 andp>1; a countable compact exhaustion gives the claimed local uniform convergence and expected-supremum convergence.

The bounded two-jump example is source-admissible. Both locations are uniform, so its mean is exactlylambda; the specified event places one jump in each adjacent interval without wraparound. Its lower bound is delta/[n(n+1)], which rules out every source exponentkappa>1/2. The example establishes coverage outside the original increment condition, not failure of the weak-moment conjecture.

## 4. Turn3: moving truncation and logarithmic thresholds

The generation-dependent partition is essential and correctly used: beta^n<=2alpha^n prevents the fixed-interval exponential loss. The large-active-envelope union bound sums geometrically in the interval index; the number of eligible generations contributes only a logarithm. Tonelli and Borel–Cantelli therefore give the simultaneous active-family maximum statement under XlogX.

The cutoff X(lambda)1_{X(b)<=lambda^n} is nondecreasing and càdlàg. Dependence between the cutoff and the same offspring copy is allowed; independence between copies survives. Applying the Turn2 lemma atp=2 after truncation gives the displayed variance bound. The geometric-tail inequality controls its full moving-grid sum by B_n=E[Y min(Y/a^n,1)], and sum B_n is finite under XlogX.

After sufficiently large generations, the actual discarded sum vanishes simultaneously across the compact. The remaining deterministic tail bias is nonnegative. Thus M_(n+1)<=M_n+d_n, and square summability ofd_n implies M_n²=O(n) pathwise. The nonincreasing summable bias sequence satisfies sum n b_n²<infinity. This proves almost-sure square summability of the actual supremum increments without asserting finite expected squares of untruncated heavy-tail increments.

Under the stronger log^(2+epsilon) moment, weighted Cauchy–Schwarz proves sum sqrt(B_n)<infinity. The discarded centered terms are bounded by a two-index tail count requiring a second logarithm. The resulting expected absolute sum of supremum increments is finite, so almost-sure locally uniform and expected-supremum convergence follow. The logarithmic exponent above two is explicit, rather than being described as the exact XlogX endpoint.

The Cantor-coordinate martingale control is valid: finite sign patterns attain all favorable factors, giving supremumH_n and increment norm1/n exactly, while fixed-coordinate second moments remain uniformly bounded. It is a generic obstruction to a functional-martingale shortcut, not a branching-process counterexample.

## 5. Turn4: scalar maxima and the true geometric joint law

For each fixed parameter, the centered truncated contributions are square-integrable martingale differences. Their variance sum is bounded by the exact geometric tail at the firstk withlambda^k>=y. Replacinglambda by the compact left endpoint yields the stated B_n/[a(a-1)] bound. Doob is applied only to this single parameter's generation filtration. The discarded centered contribution is summable in expectation under XlogX. Consequently the scalar temporal-maximal estimate is valid uniformly in the parameter with the supremum **outside** expectation.

The subsequent uniform-integrability argument uses an integrable finite-generation envelope and uniform L1 approximation. The first-moment equicontinuity follows from monotonicity ofZ_N and its known mean; no random parameter is inserted into the scalar maximal estimate there. These facts are not promoted to path tightness.

I independently checked the geometric coupling against Section2.2. At successive thresholds, the additional geometric waiting length is independent of the previous count, so the source's independent-increment offspring formula is correct. Its inverse-threshold display needs the right-continuous version at random ties; the author's strict comparison supplies that version without changing deterministic finite-dimensional laws.

The common descendant pairs in the root decomposition are retained. Expanding the UUV indices by their coincidences gives the claimed third mixed-moment recurrence and formula. The scaled independent-increment candidate has the same marginals and covariance, but its U²V moment differs by the stated strictly negative rational quantity. This excludes precisely that candidate; it does not prove non-Markovianity.

The bivariate Laplace recursion, factorC(t), monotonicity ofM_t and derivative boundlambda all check. The linear mean-corrected terminal has a second-moment error that remains geometrically decaying after the lambda^n amplification. I independently reconstructed the exact n=8 rational interval atlambda2,mu3,s=t=1; its lower endpoint is strictly above1/2. No numerical approximation is needed for this separation.

## 6. Turn5: common jump envelope and l2 alignment

This is the highest-risk part, and its conditioning is valid.

- A single monotone integer-valued copy has finitely many jumps on a compact. Continuity of its mean gives E Delta X(theta)=0 at each deterministictheta. Independence of different copies and a countable union exclude coincident intrinsic jump times throughout the Ulam tree.
- The presence of a depthk parent at a specified parameter depends only on its ancestors. Its own marked jump process and all child-subtree copies are independent of those ancestors. Selecting a random interval of child labels using the parent process preserves independence and identical distribution of the selected descendant subtrees.
- At an active parent event, the new subtree batch gives exactly Delta W_n(theta)=theta^(-k-1)sum_i W_(n-k-1)^(i)(theta). Descendants activated by the same ancestral event are included in that batch, rather than counted as new intrinsic events at the same time.
- The birth parameter is independent of those new subtree copies. Therefore the uniformly bounded **fixed-parameter** expected generation maximum from Turn4 may be integrated at that random parameter. No expected supremum over parameters is introduced.
- The marked mean measure satisfies integral J nu(dtheta,dJ)=dtheta. The expected number of active parents on the left atdepthk is theta^k; deterministic jump atoms vanish, so the left-limit expectation is the same. Conditional independence and Tonelli justify the exact depthk count formula.
- The subtree-batch law is independent ofdepth. Summing the geometric prefix in the count formula yields E#{events:B_e>eta}<=C(b-a)/[eta(a-1)]. It counts each intrinsic event once together with its entire future sequence of inherited jumps; there is no missing extra sum over generations.

Integrating this bound against2eta on(0,1) proves finite expected capped-square sum. There are then only finitely many envelopes above1, each finite almost surely, so the uncapped square sum is finite almost surely. No finite expectation is claimed for that uncapped sum. Scalar martingale convergence at each independent random birth parameter extends to the countable event set. Dominated convergence with the square-summable envelope proves l2 convergence of the full jump-size vectors.

The conditional J1-limit assertion is also correct. Under time changes tending to the identity, a nonvanishing jump of a uniform transformed limit must match a prelimit jump. Above any fixed size threshold there are only finitely many possible locations; a converging matching location is eventually the same one. Conversely, a positivej_theta cannot disappear. Negative jumps cannot arise in such a J1 limit. This identifies possible jumps but does not establish that a J1 limit exists.

The remaining cumulative small-jump/continuous-drift issue is real and is not hidden by the envelope theorem. A square-summable jump envelope is not a total-variation bound, and the between-jump drift has factorn. The packet does not claim otherwise.

## 7. Checks and disposition

All43 manifest-bound author files and four reading PDF hashes were verified; only three PDFs are mathematical inputs. The five author scripts were replayed in separate copies and their receipts match byte-for-byte, totaling40,502 exact assertions. A separately authored checker passes5,849 exact controls, including ancestry-measurable relabellings, threshold Jensen bounds, geometric tails, inactive/batch event identities, marked-depth sums, independent mixed-moment expansions and a fresh rational transform enclosure.

These controls supplement the preceding analytic audit. They are not an exhaustive search, proof of general process existence, endpoint tightness or historical novelty.

Recommended publication scope: **unsolved5/5, with the reviewed partial results exactly as frozen**. Retain the local-supercritical domain, every moment threshold, the original/final-edition access distinction, and the separation among scalar, finite-dimensional, integrated, jump-vector and J1 convergence. No further author proof route is supplied by this review.
