# Independent early mechanism seal

UTC: 2026-10-03T01:50:23.147222+00:00

## Exposure and scope
Read actual root AGENTS.md and unsolved_math_prioritization/AGENTS.md. Before this seal I have read no candidate PARTIAL, historical review, helper, results, ledger, source_record, or original diff. I saw filenames while inventorying and the parent supplied literal target and head/base identifiers. The original target supplied is weak shift convergence θ_n X ⇒ X′ on a separable metric product path space and seeks a characterization by a construction of only X and X′ (example synchronous metric distance →0). The literal excerpt supplies no convergence mode, ergodicity, adaptedness, or homogeneity. This is a mathematical audit, not another proof-attempt response or a solution of the whole target. No remote/index/native source writes, commit, branch change, or outreach authorized for this family.

## Independent mechanism from the literal target
Use path space S={{0,1}}^N with product topology and left shift θ. Partition time into consecutive blocks of lengths 2L_j, with L_j→∞. In each block put L_j fresh independent fair bits into the first half and repeat those bits in the second half. All fresh bits across blocks are independent. Let X be this process and X′ have the fair iid product law Q.

Any fixed finite shifted window of X has independent fair coordinates for all sufficiently late starting times: the only duplicate indices in a block have separation L_j; different blocks use disjoint bits. Thus θ_n X ⇒ Q in product topology. Q is stationary and genuinely iid/ergodic. Weak convergence follows by exact eventual cylinder laws and compactness/uniform approximation of continuous functions by cylinders.

For any joint law of X and X′, let p_k=P(X_k≠X′_k). For a duplicated pair a_j,b_j in a block, X_a_j=X_b_j a.s., while Q gives P(X′_a_j≠X′_b_j)=1/2. The triangle/union bound therefore yields p_a_j+p_b_j≥1/2. Both indices go to infinity; hence limsup p_k≥1/4. For the usual product metric d(x,y)=Σ_{r≥0}2^{-(r+1)}1[x_r≠y_r], P(d(θ_k X,θ_k X′)≥1/2)≥p_k. Consequently synchronous convergence in probability fails for every coupling, hence also almost-sure convergence and expected-distance convergence. The quantifier is ∀ joint laws with the stipulated marginals; for each one there is an infinite deterministic subsequence with discrepancy probability ≥1/4 (the subsequence may depend on the joint law).

This obstruction survives every metric compatible with binary product topology: the first-coordinate 0 and 1 cylinders are disjoint compact sets, so their mutual distance is some δ_d>0. The scale is metric-dependent, but the lower probability bound 1/4 is not. It does not automatically assert an identical threshold on a noncompact generic path space without this compact binary embedding.

The coordinate constant 1/4 is sharp: start with iid Y and independent auxiliary fair bits. For each duplicated pair, select W=Y_a when Y_a=Y_b, and on disagreement choose Y_a or Y_b equally. W is fair and independent across disjoint pairs; each endpoint disagrees with W with probability 1/4. This establishes sharpness only of the single-coordinate limsup bound, not an optimal complete-path distance distribution.

## Fixed random offsets: independent derivation and precise boundary
If T,S are integer-valued almost surely finite variables on the joint space (arbitrarily dependent on X and X′), simultaneous comparison θ_{n+T}X against θ_{n+S}X′ still cannot tend to zero in probability. With D=S−T, far duplicated X pairs give X_a=X_b; for fixed d, the iid pair (X′_{a+d},X′_{b+d}) becomes asymptotically independent of each fixed positive-probability event {{T=t,S=s}} as a,b→∞, since any event can be approximated in probability by a cylinder event and the relevant iid coordinates eventually lie outside that cylinder. Summing over a finite truncation of (T,S), then letting its probability tend to one, gives P(X′_{a+D}≠X′_{b+D})→1/2. Convergence at deterministic n would imply convergence at the finitely shifted times a−T,b−T by truncation and a finite union, contradicting the duplicated-pair inequality.

I have not sealed a claim for n-dependent offsets T_n,S_n merely tight in law. The offsets at the paired times can choose different X coordinates and destroy the exact repeated-coordinate equation; an additional argument or obstruction is required. I also have not sealed a claim for convergence in distribution of distances, weak convergence on more general path topologies, generic stationary limits, or continuous time.

## Verdict anticipated before candidate exposure
The construction proves that weak shift convergence alone cannot imply existence of a synchronous coupling with metric distance tending to zero in probability or almost surely, even with a stationary iid limit. It rules out one illustrative coupling characterization. It does not rule out some other characterization using only X and X′; that literal full target remains unresolved. Nothing here supplies novelty certification or a full solution.

Audit completion estimate: 20%. Discovery completion estimate for full literal characterization: 0% from this audit; obstruction-route evidence is established subject to later adversarial verification.
