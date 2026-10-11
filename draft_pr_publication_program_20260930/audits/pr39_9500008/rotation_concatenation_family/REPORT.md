# Independent rotation and concatenation audit

The frozen PARTIAL.md supports its stated pathwise approximation and diffusive limit. It does not establish the source's exact finite-random-origin claim, and it explicitly leaves that claim unresolved. This audit reconstructed the mechanism before reading the proof or historical verdict. It transfers no historical PASS and claims no solution, novelty, priority, paper, or DOI.

One precision repair is required in the historical review's explanation of reflection: a sign change preserves the *admissibility* of a stopped Brownian pair, not necessarily its joint distribution. This does not invalidate the submitted theorem, whose proof invokes the correct concatenation fact.

## Frozen identity and independence protocol

PR 39, problem 9500008 / AMR-094-0008; head `652b8115080e5e97b2274cb602de3faf8c551f20`, base `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`. The snapshot manifest SHA-256 is `debd6fd2621f401ec927c441da3b54a13ca60ee917698898299ad24faf67616e`. All 16 original attempt artifacts match their frozen sizes and SHA-256 values; the manifest records 17 changed paths. No original, canonical, shared, Git, or remote artifact was changed.

`CLAIM_SEAL.json` was saved at 09:47:07 UTC on 2 October 2026, before PARTIAL, readiness, original review/verdict, or sibling/root interpretations were read. Entire literal source_record.json and prior_report.json were read first as required; their dated triage claims were unavoidable exposure and were not accepted as current evidence. A broad file inventory accidentally disclosed other audits' .gitignore path names, but no sibling contents. `PRE_REVIEW_DERIVATION.md` was saved at 09:48:57 UTC before the submitted proof/code/review reads. Reading order and limitations are recorded separately.

The source claim requires one a.s. finite real random S such that the centered forward and backward halves at S are independent standard Brownian motions. S need not be a stopping time, independent of X, or a join. The input marks are independent, potentially non-iid stopped pairs; zero durations are allowed; both duration sums diverge; one deterministic c bounds every duration strictly. Brownian motion must be Brownian for the filtration in which T is a stopping time. An anticipating enlarged filtration is inadmissible. These are the quantifiers on the [author's Problem 8](https://sites.math.washington.edu/~burdzy/open_mathjax.php).

The [primary paper](https://math.washington.edu/sites/math/files/documents/research/1302.6958.pdf), author-hosted arXiv v4 of 29 March 2013, distinguishes fixed origin and random origin in Definitions 2.1–2.2. Its iid finite-mean theorem uses a stationary renewal shift and a common conditional stopped-path law. Its non-iid uniform-moment counterexample does not obey the common deterministic duration bound. The rotation mechanism occurs in its Theorem 5.2 proof. The supplementary [Pitman–Tang paper](https://www.columbia.edu/~wt2319/Slepian.pdf), printed page 3, confirms the iid/non-iid distinction. No new missing-shift search was conducted; this is no exhaustive literature or novelty certificate.

## Probability law of the comparison path

Write A_0=0, A_j=sum_{i=1}^j T_{-i}, R(t)=X_{-t}. For the j-th negative piece, beginning at a=A_{j-1} and of duration T=T_{-j}, continuity and the source orientation give

    R(a+u)=R(a)+B^{-j}_{T-u}-B^{-j}_T,  0<=u<=T.

Define, on the original stopped marks,

    W(a+u)=-sum_{i<j} B^{-i}_{T_{-i}}-B^{-j}_u.

W and R agree at all joins. The order is -1,-2,..., and the Brownian driving path within each W piece is *not* internally reversed. It is the negative of its original path. This is the crucial distinction from assuming Brownian time reversal of an endogenous stopped segment.

For each original filtration F^k, -B^k is Brownian relative to the same filtration because the transformation is deterministic and preserves independent Gaussian increments. T_k remains an F^k stopping time. Thus (-B^k,T_k) is an admissible stopped Brownian pair. Its law need not equal the law of (B^k,T_k). Independence of the stopped pairs survives deterministic reflection and the prescribed index ordering; identical distributions are unnecessary.

Here is a rigorous law argument that does not presume independence of the full original Brownian paths after they stop. For J finite, use the first J independent stopped negative marks and append an independent fresh Brownian continuation. The stopped mark law determines the law of a Brownian path stopped at its T. By the strong Markov property, concatenating that stopped mark with an independent continuation has Wiener law. Induct backward through the J marks, attaching an already Brownian independent continuation at each step. This finite extended splice has Wiener law. It can be coupled with the explicit infinite W and agrees on [0,A_J]. For any deterministic H, divergence gives P(A_J<=H)->0. Their laws on C([0,H]) differ in total variation by at most that probability, so the explicit W has Wiener law on each compact, hence on the half-line.

This argument keeps all indexed marks, including zero durations. It does not condition on a random subsequence of positive-length marks and then assume those conditional laws retain arbitrary independence. Because A_J tends to infinity, every deterministic finite H is reached by finitely many indexed marks a.s.; no bound on the expected number of marks is required. Repeated zero-time endpoints have the same path value. The source's two divergence assumptions are needed to define both complete half-paths.

The positive half X|[0,infinity) is Brownian by the same finite-splice argument. W is a measurable function of the k<0 stopped marks. The positive half uses only k>=0 marks, so these two *entire path-valued variables* are independent by independence of their generating sigma-fields. This proves more than covariance cancellation or separate Gaussian marginals. Defining Z_t=X_t for t>=0 and Z_t=W_{-t} for t<=0 produces a genuine fixed-origin two-sided Brownian process on the original probability space.

Bounded optional sampling is consistent with the mechanism: E B_T=0 and E B_T^2=E T, with the corresponding exponential martingale identity, hold under the stated filtration. These terminal identities alone would not prove the Brownian law, would not make T independent of B_T, and would not justify reversal. The proof uses the full stopped-path law and strong Markov restarting instead. An anticipating T can fail even the terminal-mean identity, as the exact controls show.

## Exact geometry and almost-sure estimate

The definition above gives the exact identity

    R(a+u)=W(a)+W(a+T)-W(a+T-u).

Consequently

    R(a+u)-W(a+u)
      =[W(a+T)-W(a+T-u)]-[W(a+u)-W(a)].

Both increments have length u<=T<c. If a+u<=H, all four endpoints are in [0,H+c], including a+T when H cuts through the final piece. The triangle inequality yields

    sup_{0<=t<=H}|R(t)-W(t)| <= 2 omega_W(c;H+c).

There is no hidden renewal-rate estimate, iid condition, endpoint independence, or optional sampling at a reverse-time cut in this inequality. It is a deterministic identity for each continuous piece, so the rational finite controls test it meaningfully. The horizon extension H+c matters: a per-index bound cannot be inserted as one common c. A deterministic oversized-piece control shows how the error can see a spike outside the falsely shortened horizon.

c must be positive for any admissible divergent model. At H_m=c*2^m, each increment of length <=c can be included in a block [jc,(j+2)c] for 0<=j<=2^m+1. A difference greater than r implies an absolute displacement greater than r/2 from the left endpoint. The reflection principle over duration 2c and a Gaussian tail bound give a per-block bound 4 exp(-r^2/(16c)). The union bound therefore gives

    P(omega_W(c;H_m+c)>r) <=4(2^m+2) exp(-r^2/(16c)).

No independence of overlapping blocks is needed. With r=8 sqrt(cm), the exponential is exp(-4m), and the sum is finite. Borel–Cantelli, followed by monotonic interpolation between consecutive dyadic horizons, gives the claimed a.s. O(sqrt(log(2+H))) error. Constants may depend on c and the sample. The time units are consistent: Brownian magnitude is proportional to sqrt(time), and the chosen threshold contains sqrt(c).

For each fixed finite L, the uniform discrepancy between r^{-1/2}X_{r t} and r^{-1/2}Z_{r t} on [-L,L] tends to zero a.s. Brownian scaling supplies the latter process's unchanged two-sided Brownian law. Thus the asserted weak convergence in the uniform topology follows. The rescaled Z paths need not converge a.s. to one path. The proof is valid with arbitrarily small durations, external independent time-zero decisions, and different stopping rules at every index.

## Source target, examples, and exact gap

The capped first-hit example uses iid T=min(tau_{-1},1)<2, so it is admissible, positive a.s., has finite positive mean, and has divergent duration sums. On tau_{-1}<1, reversing the terminal piece makes R strictly positive on a nonempty initial interval. A Brownian motion begun at zero has probability zero of this event, by reflection on deterministic intervals and a countable union. This refutes fixed-origin Brownian law only. The known iid theorem gives a different random origin for the same example, so it is no source counterexample.

The periodic-law corollary also checks out when periodicity concerns the complete stopped-pair laws. Grouping a full period gives independent identically distributed Brownian stopped blocks. Successive duration sums are stopping times for the sequential splice filtration; a block's path can be verified by fresh continuation just as above. Its mean duration is finite and positive because divergence excludes an all-zero periodic block. The original half-line divergence survives grouping. Periodic duration marginals alone would not establish this result.

The W construction alters the path within every negative piece. The coupling is exact as a relationship between two different paths; it is not equality of the original path with a single translated Brownian path. The shrinking diffusive error does not provide a finite S, its distribution, or an exact joint law at S. Deterministic observation windows sent to +infinity likewise give finite Brownian windows even in inadmissible-to-the-conclusion models and do not furnish a finite random origin. An iid equilibrium/Palm shift cannot be silently applied to the general non-iid marks, whose conditional path law given duration can depend on the index. The exact gap remains the original finite-random-origin representation or an admissible bounded model ruling out every such S. This audit made no fresh attempt to fill it.

## Executed receipts and falsification sensitivity

All original scripts were copied into the audit's own ignored tmp tree before execution. Using exactly `/usr/bin/python3`, Python 3.9.6 with existing user-site SymPy 1.14.0, both original submitted-verifier copies return 0 and reproduce the 12,288 configurations and 48 prefix-law receipt byte for byte. The original independent checker returns 0 and reproduces its entire result byte for byte: 12 named checks, 144 configurations, 2,256 equalities, and 16 randomized-zero prefix laws. Full stdout, stderr, generated JSON, runtime, script hashes, and comparison status are preserved.

Earlier default Python 3.14.6 and bundled Python 3.12.14 runs could not import SymPy. Those failures are retained rather than erased. An isolated SymPy 1.14.0 installation had already completed in own ignored tmp before the root supplied `/usr/bin/python3`; that private package was not used in the final replay. No existing runtime or package was changed. A supplemental local PDF download received HTTP 403; the web tool successfully exposed the relevant paper paragraph, so no local PDF checksum is claimed for it.

`falsification_controls.py` uses only the standard library. Its final 18 exact rational check groups pass. The first 17-group run is retained with .run1 suffix; the final run adds an explicit reflected-pair-law control. Distinct checks include a six-step fair-prefix law with different stopping rules and time-zero activation probabilities 1/3 and 3/5; 88 rational paths with unequal non-unit slopes, zero pieces, and quarter-grid horizons; 2,304 rotation identities; full finite joint-half independence; legitimate bounded optional sampling; and dyadic cover/series constants.

The adversarial controls detect anticipated T, anticipation at time zero, reversed stopped increments, an endogenous circular stopping-time rotation, reused inputs between halves, and a falsely common time bound. For the cap-two stopped walk, the correctly ordered reflected first increment is fair, while the internally reversed first increment is +1 with probability 3/4. A stopped circular rotation likewise gives probability 3/4 instead of 1/2. The anticipating T has terminal mean 1/2 rather than zero. These are finite invalid-mechanism controls, not Brownian counterexamples to the full target. The finite tests cannot prove infinite Brownian laws, pathwise Borel–Cantelli conclusions, or existence/nonexistence of a source shift; the written arguments are essential.

## Required precision repair and disposition

Historical review/REVIEW.md says, after observing that T stays a stopping time after sign change, that Brownian symmetry preserves each stopped Brownian-pair law. As an equality of paired distributions this is false. Let T=min(first hit of -1,1). The original B_T has a positive atom at -1; -B_T has its corresponding atom at +1 and no atom at -1. Reflection therefore changes the paired law. The exact finite control also finds P(T=1,endpoint=-1)=1/2 before reflection and 0 afterward.

Required replacement: “Because -B^k is Brownian for the same filtration and T_k remains a stopping time, the reflected pair is another admissible stopped Brownian pair. Its joint distribution may differ from the original pair; independence is retained, and the strong Markov concatenation argument applies.” No change is required to the submitted PARTIAL.md theorem/proof on this point. The original review is preserved untouched; the correction is recorded here for later incorporation by the root.

Strongest independently verified result: the displayed coupling bound, a.s. logarithmic error, and two-sided diffusive weak limit for the full stated bounded independent-piece class. Exact full-target gap: one a.s. finite origin with the exact independent Wiener joint law remains unproved. Original authored effort remains 2/5; this audit adds 0 substantive source-research turns. No full-solution or priority claim is supported. Audit completion: 100%; source discovery completion remains uncertain and unchanged by verification.
