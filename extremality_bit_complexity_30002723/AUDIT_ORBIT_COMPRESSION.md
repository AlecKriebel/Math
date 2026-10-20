# Independent audit of the proposed interval-orbit compression

Date: 20 October 2026. Target: queue row 1827, rational sparse-list, possibly discontinuous one-row extremality.

## Status and scope

**PASS for the stated candidate after complete manuscript review.** The first version of this note was provisional because the discontinuous proof was still being assembled. The completed `ATTEMPT_3.md`, `ATTEMPT_4.md`, and `ATTEMPT_5.md` have now been independently reread against all six obligations in Section 8. No remaining mathematical gap or counterexample was identified in this scoped audit. This is an scoped mathematical audit, not external peer review, an implemented compressed solver, or a verification of novelty. Finite checks support the algebraic review but are not the proof.

No publication or queue mutation was performed. The continuous-only candidate is in `structural/CONTINUOUS_AHT_REDUCTION.md`; the general reduction is in `ATTEMPT_3.md` through `ATTEMPT_5.md`. This audit favors compressing the full conceptual `N=4q` system directly, rather than importing a separate coverage argument into the discontinuous case.

## 1. Primary-source interfaces inspected

Basu, Hildebrand, and Köppe, Part I, [arXiv:1206.2079v2](https://arxiv.org/html/1206.2079v2), Section 3.1, Theorems 3.2 and 4.11, were inspected in the primary text. The finite system contains independent interval-affine and breakpoint-point data, with every tight face-specific vertex equation, not just actual point-value additivity. Theorem 4.11 supplies an equivalence with unrestricted extremality at the `1/(4q)` refinement, including discontinuous input. Thus compressing exactly that kernel suffices; restricting competitors to continuous functions would not suffice. The input's rational values and limits are needed for bit-complexity claims, though the source theorem itself allows real values.

Agol, Hass, and Thurston, [arXiv:math/0205057v2](https://arxiv.org/html/math/0205057v2), Theorems 12 and 16 and the Section 6 output definition, were inspected directly. The unweighted algorithm counts orbits in polynomial time in the pairing count and binary interval size. The weighted version permits a polynomial-size piecewise-constant vector-weight description. Its output is a list of weighted integer intervals: the length of an output interval is a multiplicity of distinct orbits sharing that weight. It is not an explicitly expanded list of exponentially many original orbits. Section 6's nonnegative-weight formulation is sufficient here by using separate positive-sheet and negative-sheet counters. The stated complexity depends polynomially on pairing count, weight pieces, weight dimension, and logarithms of the integer bounds.

## 2. Exact trace coordinates and a reconstruction check

Write `s_k` for the slope on `(k/N,(k+1)/N)`, and write

- `J_k = h(k/N+) - h(k/N-)`,
- `P_k = h(k/N) - (h(k/N+) + h(k/N-))/2`.

Indices are periodic modulo `N`. For normalized `h(0)=0`, define

`C = -J_0/2 - P_0`,

`H^-(k) = C + (1/N) sum_{0 <= i < k} s_i + sum_{0 <= i < k} J_i`,

`H^+(k) = H^-(k) + J_k`,

`H^0(k) = H^-(k) + J_k/2 + P_k`.

The single consistency equation is

`(1/N) sum_{0 <= i < N} s_i + sum_{0 <= i < N} J_i = 0`.

It ensures periodic left/right traces. `H^0(fN)=0` is the remaining normalization equation. On an open cell, use `H^+(k)+s_k(x-k/N)`.

This is an invertible linear change of coordinates between normalized periodic piecewise-linear functions and the slope/jump/spike coordinates satisfying the consistency equation. In particular, it does not introduce a hidden extra additive constant. A nonzero coordinate vector satisfying consistency reconstructs a nonzero function. Prefix and singleton orbit counts are enough to evaluate every required trace.

An equivalent initial-right-limit formula is valid, but its jump sum starts at index 1. Mixing the left-limit constant with the right-limit summation convention is an off-by-one error.

## 3. Local sector audit

### 3.1 Genuine additive one-dimensional strata

For a horizontal or vertical actual additive edge, the function relation has the form `h(x)+c-h(x+t)=0`. On each paired cell it gives equal slopes. Taking the two traces at an interior grid crossing gives equal jumps, and comparing actual values with trace averages gives equal spikes.

For a diagonal actual additive edge, the relation is `h(x)+h(t-x)-c=0`. The two differentiation signs cancel, so the slopes are still equal, not opposite. At paired grid points the jumps are equal, while the spikes are opposite.

Thus the local generators are unsigned slope pairings, unsigned jump pairings, and spike pairings whose sign is positive for translation and negative for reflection. In particular the point-index reflection is `k -> Nt-k`, while the cell-index reflection is `k -> Nt-k-1`. These must not be conflated.

### 3.2 A limiting zero edge of a nonadditive two-dimensional stratum

The stronger forced-zero rule is necessary. Consider a horizontal zero boundary `y=b`, with the ambient two-dimensional face lying on the `y>b` side. Let `x=t`, `z=t+b` be an interior grid crossing. Denote the fixed trace `h(b+)` by `B`. The three adjacent fine two-dimensional sectors give

`H^+(t)+B-H^+(z)=0`,

`H^-(t)+B-H^+(z)=0`,

`H^-(t)+B-H^-(z)=0`.

Subtracting gives `J_t=J_z=0`. The fine ray with `x=t` held exactly fixed gives `H^0(t)+B-H^+(z)=0`; the ray with `z` held fixed gives `H^-(t)+B-H^0(z)=0`. Hence `P_t=P_z=0` as well.

The other side and the vertical and diagonal cases follow by the corresponding linear coordinate symmetries. This remains true when the two variable projections overlap or coincide modulo 1. Point-fixed ray equations are essential: using only two-dimensional sector limits would not by itself establish the spike condition.

Within each intervening open fine segment, the two endpoint tight equations give derivative pairing. Therefore the proper generators for a zero limiting edge are equal paired slopes and individually zero jumps and spikes on the interiors of both nonconstant projections. Mere paired jumps/spikes would leave invalid degrees of freedom.

The endpoints of these projection intervals are excluded from the forced-zero ranges. Their one-sided and actual values must instead be handled by residual sector equations.

### 3.3 Fully additive two-dimensional strata

A function in the full fine-grid kernel is additive on every refined stratum in the coarse face interior. The interval lemma then yields one common affine slope on all three open projections, including across fine grid points. Consequently all interior jumps and spikes on these projections vanish.

Conversely, these common-slope and zero-jump/spike conditions make the restriction affine on each whole open projection. The additivity expression is constant on the coarse face interior. An appropriate boundary-sector residual equation sets this constant to zero; retaining all active feasible endpoint sectors is a convenient uniform way to guarantee this and to preserve every boundary trace.

The equality of all cell slopes in a projection is represented by one adjacent-cell shift pairing. One singleton link per projection joins these chains to a common slope component. No dense expansion is needed.

## 4. Residual endpoint sectors and exhaustion

At a fine grid vertex `(u,v)`, the local line arrangement consists of `x=u`, `y=v`, and `x+y=u+v`. There are thirteen relative sectors: one point, six rays, and six open cones. A fixed representative direction set is

`(0,0), (1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1),`

`(1,1), (-1,-1), (2,-1), (1,-2), (-2,1), (-1,2)`.

For each tight coarse-face vertex, retain only directions whose sufficiently small positive step lies in that coarse face's relative interior. The signs of `dx`, `dy`, and `dx+dy` select the actual, right, or left trace in the residual equation. Every feasible fine sector is represented, and impossible sign combinations are excluded.

The coarse arrangement has polynomial size. On each genuine relative stratum the input slack is a nonnegative affine function. Its zero set is empty, the whole face, a boundary edge, or a vertex. The cases in Section 3 and the endpoint residuals are therefore exhaustive. A proof should explicitly assign each tight fine-sector vertex to its containing coarse relative stratum and to the minimal zero face containing the vertex. This is the cleanest way to establish that no fine-sector equation has been lost.

A separate bookkeeping trap: a nonempty closed intersection of interval triples need not have any point simultaneously in their prescribed relative interiors. Such an intersection can encode impossible one-sided data. Enumerate genuine relative strata, or filter by nonempty simultaneous relative interiors. The evolving dense checker correctly applies a centroid relative-interior filter. The manuscript must state this rather than silently treating every closed triple as valid.

## 5. Signed orbit compression

Consider equations `z_j = epsilon z_i`, with `epsilon` in `{+1,-1}`, and forced-zero intervals. Ignore signs to obtain the underlying graph `G`. Form the two-sheet lift with vertices `(i,+)` and `(i,-)`, lifting each signed edge in the standard way. Force zero by pairing the two sheets at that index. On a whole interval this is a single cross-sheet interval pairing.

Each unforced, sign-consistent underlying component gives two lifted components and one real degree of freedom. Each inconsistent or forced-zero component gives one lifted component and no freedom. Thus

`free dimension = components(lift) - components(G)`.

This identity uses the underlying graph before artificial zero flips, whose projected flips are identity maps and do not change its components.

If the total free dimension of the slope, jump, and spike systems exceeds the number `R` of residual scalar equations, non-extremality follows by dimension alone. The trace reconstruction is injective after including its consistency row, so a nonzero residual-kernel vector is a genuine nonzero perturbation direction.

When the dimension is at most `R`, one can recover one original index per free component without expanding the grid. Add a sheet flip on the prefix `[0,m]` and recount lifted components. A decrease occurs precisely when the prefix meets a remaining free component. Binary search finds the least index in such a component. Permanently flip that single index in the search copy, and repeat. There are at most `R` iterations and `O(R log N)` counting queries.

**Important:** weighted reconstruction must use the original graph and original forced zeros, not the modified graph used to kill previously selected representatives during the search.

Place a separate unit marker at the positive sheet of each recovered representative. On its marked lifted component, the difference between positive-sheet and negative-sheet counts over a prefix is exactly the signed coefficient of that component in the prefix sum. Use separate nonnegative counters and subtract their returned sums. Singleton coefficients are obtained similarly or by adjacent-prefix differences.

A nonzero representative marker occurs in exactly one lifted component. Therefore an output multiplicity interval carrying that marker has length one. Only the polynomially many marked components need individual handling; unmarked output multiplicities are never expanded. The labels of AHT's output points need not be original grid indices because the markers supply the necessary identities.

## 6. Bit and output bounds checked

Let `L` be the sparse all-rational input bit length and let `n` be the number of listed breakpoints, including `0`, `1`, and `f`.

- The least common denominator has `log q = O(L)`; replacing it by `N=4q` changes this by a constant.
- A naive enumeration over triples of coarse cells is polynomial in `n`. Every surviving two-dimensional polygon has at most six supporting sides. Geometry and slack evaluations use rational arithmetic of polynomial bit length.
- Each zero face contributes a constant number of interval pairings, adjacent-cell chains, and forced-zero intervals. Periodic reductions and two-sheet lifting split each into only constantly many interval isometries.
- The residual count `R`, the relevant trace coordinates, and the pairing count are polynomial in `n`. All index endpoints have `O(log N)` bits.
- The representative search makes polynomially many AHT calls, each with only polynomially many added flips. It does not make one call per grid index.
- The marker/prefix/singleton weight vectors have polynomial dimension and polynomially many constant pieces. They can be chosen nonnegative with initial entries in `{0,1}`. Every accumulated coordinate is at most `2N`, so its binary length remains `O(log N)`; a bound covering all coordinates is `2N` times their number.
- Weighted AHT is used with compressed multiplicity output, not an expanded orbit listing. The explicit variable count is at most `R` in the branch requiring a rank test.
- After substituting reconstruction, residual matrix entries are signed orbit counts, half-counts, or counts divided by `N`. Multiplication by `2N` gives an integer matrix of polynomial dimensions and polynomial coefficient bit length. Exact rank computation is therefore polynomial in `L`.

A conventional grid-tabulated non-extremality witness may have exponential output size. The proposal is a decision algorithm; it must not promise that expanded witness as a polynomial-size output.

## 7. Independent finite checks

`checks/audit_signed_reconstruction.py` and its JSON result were created independently of the candidate's coarse reduction implementation.

- 204 random finite signed graphs, sizes 1 through 17, compared the lift-minus-base dimension with exact rational matrix rank.
- The same cases tested the prefix-flip binary-search enumeration, the resulting signed basis, and every prefix coefficient against direct summation.
- 230 random rational periodic piecewise-linear trace systems, sizes 1 through 23, checked the normalized reconstruction, its inverse, and the consistency equation.

All passed. These tests validate finite algebraic identities and implementation conventions, not AHT's implementation or the full coarse-face theorem. The independently authored discontinuous coarse-face test in `checks/verify_discontinuous_reduction.py` reports 35 exact full/structured/joint row-space matches, including five inputs discontinuous from both sides at zero. The completed `checks/fourfold_refinement_results.json` reports five genuine `N=4q` comparisons, all passing. Those are separate checks written by the manuscript author, not by this auditor.

## 8. Acceptance obligations and final disposition

1. A complete proof must be available and independently reread, not inferred from messages or these notes.
2. The two directions of exact equality with the `N=4q` active kernel must explicitly cover all thirteen fine sectors and all zero-stratum cases, especially limiting-edge point-fixed rays.
3. The normalized reconstruction and periodicity row must be used consistently, with open projection interiors and projection endpoints treated separately.
4. The signed-dimension threshold must count every residual row, including consistency and normalization, and reconstruction must remain injective on the resulting kernel.
5. The AHT interface must retain grouped output, bounded weight descriptions, and original-graph marker queries. No implicit dense grid or orbit expansion is allowed.
6. The conclusion must be stated for the fixed sparse all-rational encoding and the original unrestricted-competitor extremality notion. A continuous-only result is not the full target.

The completed manuscript satisfies these obligations in the following locations:

1. **Complete proof supplied and reread:** Attempts 3–5 provide the local reduction, signed-orbit algorithm, and assembled theorem. The audit reread the three documents in full, rather than relying on summaries.
2. **Exact active-kernel equivalence:** Attempt 3, cases A–D and its equivalence section, covers full zero faces, genuine zero edges, incident limiting zero edges, isolated zero vertices, and all thirteen feasible fine sectors. The independent derivation in Sections 3–4 of this audit supplies additional detail for the fragile limiting-edge necessity. Each fine face has a unique coarse relative carrier; its active vertex is classified by that carrier's zero face. The generators and residuals enforce precisely the corresponding trace relation, proving both inclusions.
3. **Reconstruction and endpoints:** Attempt 3 gives both origin traces, the correct jump-sum convention, the periodic compatibility row, and the strict-interior restriction for point pairing and forced-zero intervals. Endpoint actual/left/right values are retained through feasible residual sectors.
4. **Dimension and injectivity:** Attempts 4–5 include periodic compatibility and `h(f)=0` among the residual equations and build `h(0)=0` into reconstruction. The change of coordinates in Section 2 is invertible on the periodic normalized space, so the dimension rejection cannot create a spurious perturbation.
5. **Encoded polynomial work:** Attempt 4 explicitly returns to the original graph after representative searches, uses separate nonnegative sheet weights, and identifies only uniquely marked output orbits. Attempt 5 bounds the encoded pairing descriptions, weight pieces, counts, coefficients, and rank computation. No step requires expanding `N` grid positions or an unmarked multiplicity class. The primary AHT proof also explicitly bounds its arithmetic operands by the binary interval size, supporting bit time rather than merely real-arithmetic operation counts.
6. **Full intended target:** Attempt 5 states the sparse all-rational encoding and permits two-sided discontinuity at zero. Its Step 2 imports BHK Theorem 4.11 at `N=4q` to reach unrestricted valid competitors, rather than silently restricting them.

**Final audit disposition:** the proof passes this independent audit for the stated rational sparse-list theorem, subject to the correctness of the cited established BHK and AHT theorems. No additional mathematical assumption was found to be required. The remaining limitations are explicitly scoped: no independent novelty certification, no implementation of compressed AHT-based extremality testing, and no external review. This mathematical audit does not certify priority or external acceptance.
