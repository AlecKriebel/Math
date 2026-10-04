# First source-only assessment: arbitrary normalization and weak limits

Frozen UTC: 2026-10-04T14:14:57Z
Audit completion estimate: 20%. The target quantifiers and a sufficient universal-normalization lemma are established; no candidate has been read or evaluated.

## Intake and source manifest

Only the two files below were read. No candidate, snapshot, inherited proof/review/code, other family artifact, or root result was read. The indexed primary text is represented by the source criteria; the original primary PDF binary has not been acquired or inspected by this family. Its stated current binary-retrieval limitation remains unresolved. This is a source-defined target, not an independent current priority finding. The imported partial-progress assertions are not accepted as deductions.

| Source | SHA256 |
|---|---|
| `../SOURCE_FIRST_CRITERIA.md` | `90d01e6d5640945b009cc12d383a34ef1bec9e6ae0f9e2450d4ccf27d98d90f2` |
| `../source_inputs/problem_payload.json` | `5287ae163a93ef07ad9b962436f41d79525fdad5df82971fca240317c9d49f1e` |

## Exact claim to be verified or falsified

The admissible model has independent nonnegative delay S_0 and i.i.d. recurrence lengths X_i that are strictly positive and finite almost surely, non-lattice (not supported on dZ for any d>0), with E[X_1]=infinity. For a counterexample, S_0=0 is sufficient. Set S_n=sum_{i=1}^n X_i and N_t=inf{n>=0:S_n>t}; then D_t=X_{N_t} is the interval covering t using the strict endpoint convention. The required recurrence law must actually produce an unbounded renewal sequence, and all selected times must tend to infinity.

The general affirmative target has the logical form: for every admissible recurrence law there exists a law-dependent, deterministic, eventually finite positive, nondecreasing function phi and a proper finite nondegenerate random variable Y such that D_t/phi(t) converges weakly to Y as real t tends to infinity. Refutation needs one admissible law and delay for which every such phi fails. Proving failure for every eventually finite positive deterministic phi, with no monotonicity requirement, is a stronger sufficient statement.

Nondecreasing means phi(s)<=phi(t) whenever s<=t in its eventual domain; it does not imply strict increase, divergence, continuity, differentiability, or regular variation. The target includes bounded, diverging, and discontinuous scales. Even a nondecreasing phi can have highly oscillatory ratios relative to a separate deterministic comparison scale.

Proper finite weak convergence means weak convergence to a probability law on the finite real line; normalized variables are nonnegative, so a limiting law has support in [0,infinity). Delta_0 and delta_c for positive c are degenerate. Escape to infinity is improper. A mixed law with an atom at zero and positive mass elsewhere is nondegenerate and must be excluded, not omitted by requiring positivity of the limit.

## Independently proved sufficient obstruction

**Concentration-subsequence lemma.** Let V_t be nonnegative finite random variables. Suppose there are deterministic times t_k tending to infinity and positive deterministic numbers a_k such that Z_k=V_{t_k}/a_k tends to 1 in probability. Then no eventually finite positive deterministic scale phi(t) can give a proper nondegenerate full weak limit of V_t/phi(t). No monotonicity or divergence of either scale is needed.

Proof. Assume a proper full limit Y exists. Along t_k, W_k=V_{t_k}/phi(t_k)=r_k Z_k, where r_k=a_k/phi(t_k)>0, must converge weakly to Y and hence is tight. To see what tightness forces, choose M so that P(W_k>M)<1/2 eventually, while P(Z_k>1/2)>3/4 eventually. If r_k>2M for infinitely many k these bounds contradict one another. Thus r_k is eventually bounded. Take any subsequence on which r_k converges to a finite r>=0. Boundedness and Z_k tending to 1 imply |r_k Z_k-r| <= r_k|Z_k-1|+|r_k-r| tends to zero in probability. Hence W_k on that subsequence has limit delta_r, and uniqueness of the assumed full weak limit forces Y=delta_r. Therefore Y is degenerate. All finite cluster points must agree, so if a proper limit exists r_k actually converges to that same r. QED.

The equivalent extended-ratio cases are useful adversarial checks: r_k tending to zero gives delta_0; r_k tending to r in (0,infinity) gives delta_r; r_k tending to infinity makes W_k tend to infinity in probability because P(Z_k>1/2) tends to 1. An oscillating ratio either has incompatible finite point-mass subsequential limits or has an unbounded subsequence that destroys tightness. This exhausts all deterministic scales through compact subsequences of [0,infinity]. It also excludes mixed atom-at-zero limits: along the concentration subsequence every proper limit is a single point mass.

## Attack plan and boundary controls after explicit release

1. Require the candidate to supply a fully admissible law and a genuine diverging time sequence. Do not infer the universal claim from failure of time scaling or truncated-mean scaling alone.
2. If a concentration subsequence is claimed, check a_k>0, exact probability convergence to a positive constant, error bounds uniform enough to tend to zero, and the strict renewal endpoint convention. One such subsequence suffices for the lemma; multiple sequences or simulations are unnecessary for the universal normalization step.
3. If instead only proper nondegenerate subsequential limits are supplied, prove the needed convergence-of-types statement rather than assume scales are comparable. For V_{t_k}/a_k converging to Z with P(Z>0)>0, a ratio tending to zero gives delta_0 by tightness. A ratio tending to infinity violates tightness, even when Z has an atom at zero: choose epsilon>0 with P(Z>epsilon)>0 and obtain a fixed positive escaping mass. Finite positive ratios rescale Z. Distinct subsequential shapes must be shown incompatible up to any positive multiplicative constant. Merely different moments or apparent shapes are insufficient.
4. Do not mistake bounded normalization ratios for convergence of those ratios, or extract only one favorable subsequence while leaving others untreated. Proper convergence must agree along every deterministic time sequence.
5. The suggested phi(t)=E[min(X_1,t)] is finite and positive for t>0, nondecreasing, and diverges to infinity for the admissible infinite-mean law by monotone convergence. Therefore it falls within the universal exclusion if established. Any separate argument about its order must be derived from the actual law; the imported regular-variation assertion is not evidence.
6. Check that no claimed stronger theorem silently excludes mixed limiting laws, assumes phi tends to infinity, or relies on an atom at infinity in the recurrence distribution. Finite computations can check formulas or expose a counterexample but cannot quantify over all phi.

Strongest verified result at this checkpoint: the abstract concentration-subsequence obstruction above, with exact coverage of all deterministic positive normalizations and mixed finite limiting laws. Exact remaining gap: whether the unread candidate constructs and proves its required concentration subsequence for an admissible renewal law, and whether its written all-normalization argument matches the independently proved lemma.
