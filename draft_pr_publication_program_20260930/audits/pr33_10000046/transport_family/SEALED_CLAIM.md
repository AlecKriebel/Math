# Pre-input transport audit seal

Sealed at 2026-10-02 02:17:51 UTC. This seal follows a fresh literal archived source retrieval, reading the standing SRW definition and section 12 / Q12.33, and then `source_snapshot/PARTIAL.md`. No original code, old review, results, diff, root or sibling mathematical findings have yet been read. Source: https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf; SHA-256 `aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe`; 1,101,523 bytes; 115 PDF pages. Printed and PDF page 104 gives Q12.33. The browser reader failed; curl retrieved the literal PDF. The standing definition is discrete-time graph SRW choosing the next neighbor uniformly. Section 12 describes iid increments for a single marginal walk. The question states no co-adapted or Markovian coupling requirement.

## Exact claim and quantifiers

For every integer d >= 1, all x,y in Z^d and N >= 0, let P_N(x) consist of full vertex words (X_0,...,X_N) starting at x with nearest-neighbor steps. L_N=(2d)^N; each prefix word has probability 1/L_N. Include time 0. Join words only for all-pairs range avoidance: X_i != Y_j for every 0 <= i,j <= N. Let M_N be maximum matching size and a_N=M_N/L_N. Audit the equality

  max over complete-path SRW couplings pi of pi{X_i != Y_j for all i,j >=0}
    = lim_N a_N = inf_N a_N = liminf_N a_N,

including attainment and the normalized maximum Hall-deficiency formula. Each marginal must have its complete SRW path law, including independent increments within that marginal; correct one-time positions are insufficient. Couplings may anticipate the future. No independence between walks is imposed.

The source asks dimensions 3 or 4 and distance-10 starts. PARTIAL fixes graph distance ||x-y||_1=10; this is the exact audited normalization. The source does not explicitly specify a norm. The universal reduction is insensitive to that ambiguity. Bounds using distance 10 below use l1. The full target requires positive infinite range avoidance in the intended dimensions and start configurations. Finite horizons and synchronous avoidance are weaker claims.

## Obligations and success criteria

1. Verify the finite optimum using scaled doubly stochastic matrices and permutations, including completion of a maximum matching. Independently produce matching/cover or capacity certificates. Birkhoff applies to equal word weights only; weighted laws require capacities.
2. Verify compactness of finite-alphabet increment spaces and closedness of the prescribed complete marginal coupling set. Every R_N must be clopen and decrease to R. Check independent SRW-tail extension, restriction monotonicity, fixed-k weak passage before continuity from above, and attainment. Direct passage through varying R_N is invalid.
3. Verify the weighted Hall formula using p(A)-q(N(A)), not cardinality. Infinite extensions require consistent complete laws and their conditional tails. Positive finite mass tending to zero is a mandatory control.
4. Reconstruct a_N=1 for all N<10 via translation at actual l1-distance 10. This improves the universal geometric guarantee 2N<10. Check N=0, shared starts and the N=10 first-hit multinomial count for every displacement with sum absolute coordinates 10.
5. Verify translation gives synchronous avoidance for x!=y but zero infinite full-range avoidance: iid length-10 increment blocks with displacement y-x cause different-time collisions. This obstructs that coupling alone.
6. Derive alpha <= 1-P_x(T_y<infty)<1 for x!=y by the other initial vertex. A finite positive obstruction does not supply a uniform lower bound.

## Precommitted falsifiers

- Synchronous-only avoidance, omission of time 0, and shared-start controls must fail the true target.
- Unequal weights must refute an unweighted-cardinality probability formula.
- A consistent finite-alphabet model with strictly positive a_N tending to zero must refute finite-to-infinite positivity.
- A process with correct one-time distributions but dependent path increments must fail a two-time cylinder check.
- A varying-event weak-limit argument must be rejected; a fixed-k clopen argument must work.
- Check nonattainment against compact prescribed-coupling space and closed R.
- Actual d=3,d=4 bounded horizons are diagnostic only; exponential counts prove no uniform-in-N estimate.

## Promotion boundary

The theorem is a standard transport/compactness reformulation, not a novel solution. The exact remaining d=3 gap is an epsilon>0 such that for every N and every A subset P_N(x), |A|-|N(A)| <= (1-epsilon)(2d)^N, or proof that this is impossible. Prior 4D progress and probabilistic-block dependencies remain conditional to distinct audits. Audit validation costs 0 additional substantive original proof attempts; original remains 1/5. No shared-state, Git, GitHub or queue mutation is permitted in this family.
