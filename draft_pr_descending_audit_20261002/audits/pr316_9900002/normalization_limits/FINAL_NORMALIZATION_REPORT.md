# Final independent normalization-family verification

UTC closure: 2026-10-04T14:28:29Z. Best-guess completion of this assigned family audit: 100%. Original substantive author count preserved: 1/5; this audit is not a new search turn.

**Disposition: PASS for the arbitrary-normalization and proper-weak-limit claims.** No mandatory mathematical correction was found in this family's scope. The candidate's concentration input is exactly sufficient, and neither monotonicity nor comparison of a proposed scale with time is needed. This disposition is family-scoped; it is not overall PR, historical-priority, whole-preprint, publication or Git acceptance.

## Independence, inputs and reproducibility

The source-only assessment and proof-only assessment were separately frozen and parent-verified before their respective releases. The four early checkpoint files remain byte-identical with mode 0444. This family read all 18 target-folder files only after those gates. No other fresh family/root mathematical result was read, and no conclusion is inherited from the historical review. The inherited review was compared with an already frozen independent assessment.

The proof remains pinned at SHA256 `996947d8d995699411499b3bbdb781f25ae9a729900fb33074104cbf9e411cab`. `NORMALIZATION_EXECUTION_EVIDENCE.json` pins all 18 target files, verifies all 8 author-manifest, 5 review-manifest and 17 publication-manifest entries, and preserves exact argv, UTC, exit codes, stdout and stderr from all three substantive executions. No actual execution failed.

Both inherited checker outputs reproduced byte-identically: 7,852 author assertions/704 finite renewal cases and 646 historical-independent assertions/168 finite cases. The new `normalization_controls.py` passed 1,773 exact assertions. These checks corroborate finite algebra and test the necessity of hypotheses; none proves the universal all-scale statement. The universal result is proved analytically below and in the frozen first assessments.

Independent control-code SHA256: `6c913d3da277958d20c6b27d7006c45693ae56b3dc20fc415e7cdafce355d8b0`.
Execution-evidence SHA256: `aa9df9fcab81d792ab2a9522905abe0500e416d245f0af958669f877887a37b1`.

## Universal theorem and candidate application

For real finite W_n and deterministic real c_n, assume P(W_n=c_n)->1. If W_n converges weakly to a proper probability law nu on R, tightness puts more than 3/4 of its mass in some compact interval eventually. More than 3/4 of its mass is also at c_n eventually. Therefore c_n lies in that compact interval. Any convergent subsequence c_(n_j)->c has W_(n_j) converging weakly to delta_c, because for every bounded continuous h,

|E h(W_(n_j))-h(c_(n_j))| <= 2 ||h||_infinity P(W_(n_j)!=c_(n_j)) -> 0.

Uniqueness of weak limits makes nu=delta_c. All finite cluster points must agree, so any proper limit is degenerate. This is the candidate's literal lemma, independently reconstructed without relying on its checker or historical review.

The candidate supplies deterministic t_n=a_n/2 tending to infinity and P(D_(t_n)=a_n)>=1-epsilon_n with epsilon_n->0. For **every** deterministic function phi taking finite positive values at all sufficiently large times, including functions depending on this law, set W_n=D_(t_n)/phi(t_n) and c_n=a_n/phi(t_n). Equality on the concentration event gives the lemma's hypothesis. A proper full-time limit would also be the limit along this sequence and must therefore be degenerate. Thus one admissible law excludes all source-allowed nondecreasing scales, and the argument proves the stronger claim for arbitrary positive deterministic scales.

The cases are exhaustive: c_n->0 gives delta_0; c_n->c>0 gives delta_c; c_n->infinity gives escape to infinity in probability. A bounded oscillating c_n has incompatible point-mass sublimits, and an unbounded oscillating c_n has a subsequence that destroys tightness. A nondecreasing phi can still yield oscillating c_n: assign phi(t_n)=a_n for odd n and a_n/2 for even n, which increases because a_(n+1)/a_n>2, and extend by an increasing step function. The proof does not mistake monotonicity of phi for convergence of c_n.

The theorem includes any prospective proper nondegenerate law with an atom at zero. No positivity of such a limit is assumed. The real-valued lemma also validates the candidate's optional extension to finite eventually nonzero signed normalizers.

## Materially different bounded-transform verification

For the nonnegative normalized variables, use f(x)=x/(1+x), with a bounded continuous extension f(x)=0 for x<0. Let e_n=P(W_n!=c_n). Since f takes values in [0,1),

Var(f(W_n)) <= E[(f(W_n)-f(c_n))^2] <= e_n -> 0.

Proper weak convergence implies convergence of both bounded continuous moments E f(W_n) and E f(W_n)^2. Thus Var(f(Y))=0 for any proper limiting Y. Such Y is nonnegative, and f is injective there, so Y must be a finite constant. This independently excludes all proper nondegenerate limits without computing any scale ratio, even when Y has an atom at zero or lacks finite moments.

Properness remains essential: c_n->infinity makes f(W_n)->1, which corresponds to no finite value of Y. The argument does not turn improper escape into a legitimate limit.

## Probability-input and truncated-mean consistency

The literal renewal construction was read in full. Its positive continuous base gives non-lattice support, X>=1 prevents explosion, every X is finite a.s., the masses sum below one, and p_n a_n tending to infinity forces infinite mean. Expanding pre-first-large increments gives E T_n=M_n/q_n and the selected type has probability p_n/q_n. The inclusive T_n<=t_n event is compatible with the strict S_k>t convention even at a renewal epoch. The union/Markov bound and displayed epsilon_n have the correct directions and vanish. No local defect was found in these supporting deductions; this family does not substitute its read for the separate independent renewal-family audit.

The exact identity m(t_n)=M_n+t_n q_n follows because all small increments are below t_n and all large increments exceed it. The displayed upper bound for m(t_n)/a_n tends to zero. Consequently D_(t_n)/m(t_n) tends to infinity in probability on events whose probabilities tend to one. This specific scale is finite positive and nondecreasing and therefore is also excluded by the general theorem. The stronger non-tightness claim for this scale is justified along t_n; no global-time escape assertion is needed or inferred.

## Adversarial controls, scope and remaining gap

Controls deliberately distinguish true hypotheses from nearby false assertions: a fixed atom probability 1/2 allows a nondegenerate mixed zero/one limit; V_n=(1+B)/n tends to zero but division by 1/n restores the nondegenerate law 1+B; tiny exceptional probabilities can conceal enormous outliers and diverging means while leaving a point-mass weak limit; unbounded centers only at sparse indices still defeat full-sequence tightness. Positive concentration in probability without an exact atom was also checked as a strictly weaker sufficient condition through the independently proved source-first lemma. Exact bounded-transform variances are 1/16 for the zero/one mixture and 1/144 for the one/two mixture, exposing the central requirement of concentration probability tending to one.

**Strongest verified result:** the literal concentration hypothesis excludes every law-dependent finite eventually positive deterministic scale giving a proper nondegenerate full weak limit, including atom-at-zero targets and oscillating scales. The candidate meets that hypothesis at the proof-level inspection, and its finite checking claims reproduce honestly.

**Exact remaining gap within this family:** none identified in the normalization/weak-limit deductions. Overall candidate acceptance remains with the root and independent renewal family; their fresh findings were intentionally unread here. Original primary PDF binary/visual access and a preprint-versus-published-text comparison remain unavailable to this family. Source correspondence is checked against the frozen imported target and indexed-primary criteria, not a newly obtained complete primary document. Priority/novelty and any whole-preprint review are outside this assignment. No external individual was contacted and no Git state was changed.
