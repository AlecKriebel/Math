# Independent full review request: induced-C4 profiles

Problem30005116 / OWR-10252930-028. Five substantive author turns are frozen. Recommended disposition: **original unsolved5/5**, with the stated scoped results. Please bind the final review to the final manifest and subsequently verified WIP head; preserve frozen author files and keep review artifacts separate. No additional author search is requested.

## Packet and source paths

Public packet: `/workspace/shared/math-30005116-final`.
Source inputs: `/workspace/shared/math-30005116/sources`.
Read `SOURCE_GATE.md`, `FINAL_RESULT.md`, all five proofs, checkers, receipts, states and manifests. Source hashes are in `SOURCE_HASHES.json` and the turn2/turn4 additive source records. The historical gate and states remain unchanged.

- `owr2022-22.pdf/.txt`, `printed1227.png`: exact Mubayi Problem10, Conjecture11, Theorem12 on1227, reference1228. The nearby “no longer open” sentence belongs to the preceding problem. Report2022 versus publication14April2023.
- `lmr-feasible.pdf/.txt`, `lmr-page10.png`: Liu–Mubayi–Reiher definitions, Construction1.9, Theorems1.16/1.18, Proposition6.1, Section3 symmetrization and Section6 proof. The source's density is induced vertex-set density, not labeled embedding or ordinary cycle density. Source conjecture1.17 remains open in the paper.
- `semi2026.pdf/.txt`: Balogh–Lidický–Mubayi–Pfender–Volec, dated8January2026. Its AC4 leaves two pairs unspecified and is not inducedC4 or induced2K2. Its stronger related conjecture is credited, not substituted for our target. No numerical flag bound is used as an exact result.
- `pikhurko-razborov2017.pdf/.txt`, `pr-page140.png`: construction H_{a,n} on139; visually checked Theorem1.1 on140. The theorem assumes triangle density at most g3(a)+δ at the graph's actual edge density a and grants an ε binom(n,2) edit into H_{a,n}. This published theorem is a credited external input, not reproved. Print2017 and online4May2016 differ.
- `cograph-terminology2024.pdf/.txt`: Coudert–Coulomb–Ducoffe, Section6.2 on18 supplies the standard recursive definition and P4-free terminology with earlier credit. Our theorem is proved from the recursion and does not require a general graphon characterization or removal lemma.

## Highest-risk points

1. **Moment optimization:** compact fixed-dimensional constraint set; deleting zero coordinates; independent constraint gradients; at most two positive cubic roots; the constrained Hessian rules out two small coordinates. Check the reciprocal-integer exception, endpoint choices, finite-size factor24 and the unbounded-part-count limit. Merely locating stationary points is insufficient.
2. **Graphon normalization:** c(W) is the probability the sampled unlabeled four-vertex graph is C4, equal to three times one fixed induced edge-pattern integral. Perfect matching counting gives c≤3p²/2. All six edge/nonedge factors matter. Complements turn C4 into2K2, not C4.
3. **Join and triangle-stability step:** formula(4) of turn2 includes only occupancy4 and2+2; replacement preserves density exactly for block densities≤1/2. For finite graphs the adjacency kernel has edge density2e/n², whereas the source uses e/binom(n,2). Collision error is≤6/n. Published triangle stability is applied only to sequences whose triangle excess tends to0; no inference that arbitrary C4 extrema minimize triangles is made. The induced-C4 edit constant is6.
4. **Ties and locality:** the paw family attains the candidate value, not a verified unrestricted maximum. Check the one-edge-triple count, edit-distance bound, fixed-space tying path and L∞ versus L1 distinction. The multilinear remainder is bounded by171||h||∞||h||1, not by a false O(||h||1²) bound for strip edits.
5. **Full cograph closure:** check the coupled density at a union node: x=∑w_i²p_i, largest mass w≥x, and its internal density p≥x when x>1/2. Use the monotonicity of F only in its correct interval. Verify the explicit union gap, low-density case, join endpoint p_i=1 approximation, and cotree induction for arbitrary masses and depth. The finite scan through6 is supplementary. No almost-P4-free theorem is presumed.
6. **Rank-one direction:** factorization3(m2²−m3²)², Cauchy bridge m3m1≥m2², z=m2²/p∈[p,1], nonnegative squaring, both equality branches and p=0,1/2,1. Check the vertical feasible interval, deterministic graph-sequence attainability and explicit strict gaps from F. The rank-one maximum is not the source-wide maximum.

## Replay

Run `python verify_turn1.py` through `python verify_turn5.py` in the author directory and compare stdout byte-for-byte with their corresponding `TURN_n_CHECKS.json`. All use the standard library. Counts are38,829;611;502;44,939;8,624, totaling93,505. The source theorem hypotheses and universal written proofs require independent audit in addition to these finite controls.

Report any defect promptly. The full original remains unresolved unless the exact all-graph source target is actually addressed; none of the restricted theorems is a silent substitute.
