# Independent LP / polytope analytic assessment

Analytic checkpoint: 2026-10-03 19:55:12 UTC. Written after fully reading all 41 target files, including all four programs, every certificate, nested manifest, historical state and prior review claim. No candidate program was executed, and no root or sibling mechanism or mathematical assessment was read before this checkpoint. The prior review's PASS was treated as a hypothesis.

## Conclusion before execution

The three mathematical turns pass in their stated scopes. In particular, TURN_3's boundary quantization proof establishes the absolute gap `|psi(13/27,14/27)-psi(14/27,13/27)| >= 1/108`. No mandatory mathematical correction has been identified. The exact two values, their ordering, optimal integer invariants, historical priority and novelty remain unestablished by this audit. Integrity and program replay are separate pending work and cannot prove the universal result by assertion counts.

## Independent boundary derivation as a packing LP

Take any finite `(1-theta,theta)` biconstrained graph with `0<theta<1`. If a C vertex reaches all A vertices, its maximum reach is1 and every proposed lower bound below1 holds. Otherwise each C vertex misses an A vertex. Their B-neighborhoods are disjoint and their minimum sizes sum to |B|; hence every C neighborhood has exactly theta|B| vertices. Summing B–C edges and using each B→C lower bound forces all B vertices to have exactly theta|C| C-neighbors. This derives exact regularity from the universal finite-graph hypotheses without a duality theorem or limiting witness.

Group C vertices into their distinct B-neighborhoods T_i. Their class frequencies q_i and the uniform B frequencies b_v are strictly positive rational probabilities. The incidence matrix M satisfies `Mq=theta 1`, `M^T b=theta 1`. A vertex missed by a C type i must have B-neighborhood exactly the complement of T_i. Thus the missed sets A_i are pairwise disjoint and nonempty. Define their masses p_i. Any A vertices outside these classes remain present. For every B vertex v, the B→A constraint bounds its total nonneighbor mass by theta, giving `M p<=theta 1`. If t is the smallest missed mass then `p_i>=t`, so `F=1-t` and `Delta(M)t<=theta`. This applies to every admissible graph in the nonfull case.

The polytope controlling the missed masses is

`p_i>=t>=0`, `Mp<=theta 1`, `sum p_i<=1`.

Choose a row of degree Delta. Sum its incident lower bounds `p_i>=t` and compare with its packing constraint: this is an exact elementary dual certificate `t<=theta/Delta`. Normalization also gives `t<=1/n`. Regularity gives `n theta=sum_v b_v deg(v)<=Delta`, so the row certificate is at least as strong as normalization. Constant masses `p_i=theta/Delta` attain it; leftover mass `1-n theta/Delta` can occupy a universal A type. This independently explains the candidate's upper construction as an exact primal matching the row dual.

Strictly positive b and equal column b-weight theta imply incomparable distinct column supports: strict inclusion would add positive mass. Therefore C_i reaches every special A_j with j!=i and misses exactly A_i. It reaches the universal residual type when that type has positive mass because theta>0 forces every T_i nonempty. The universal type is omitted at residual0. This proves exact reach `1-theta/Delta`, all four degree constraints and normalization.

For rational theta, the candidate's regular template class is nonempty via a cyclic matrix. The possible Deltas form a nonempty set of positive integers, whose smallest member is realized by its defining finite template. Thus no unbounded-graph compactness or global infimum attainment is being assumed. Both the lower and upper deductions yield

`psi(1-theta,theta)=1-theta/d(theta)`.

Every retained weight is rational and positive. A separate positive integer denominator for each part makes every type present in an ordinary finite graph. Degree fractions survive exactly. Boolean paths survive because all retained middle types receive at least one copy. This construction proves boundary attainment as a consequence. Rationalizing a positive real regular template is also justified here: the two exact affine systems have rational coefficients and theta rational, so rational free variables inside their solution spaces preserve strict positivity. It does not invoke generic rounding at an irrational boundary.

At irrational theta, no integer B-neighborhood can have size theta|B|. Hence the nonfull case is impossible and `psi(1-theta,theta)=1`. This separate boundary statement is consistent with the source and is not needed for the rational counterexample.

## Source seed and integer separation

Fresh source Figure1, published printed6, was visually read after candidate reading. The top row frequencies are `(5,5,3,3,3,4,4)/27`, the lower row frequencies `(4,4,3,3,3,5,5)/27`. Independently traced top-row neighbor sets are

`{1,3,4,5}`, `{2,3,4,5}`, `{3,6,7}`, `{4,6,7}`, `{5,6,7}`, `{1,2,6}`, `{1,2,7}`

using one-based lower-row labels. This agrees with the candidate M; all weighted sums are13/27. Its maximum row degree is4. The complement preserves positive weights, makes every weighted degree14/27, keeps distinct columns and has maximum row degree4. These are credited source objects; no new source theorem is needed.

Let d=d(13/27), e=d(14/27), both integers1–4. Equality of the boundary values would require `13e=14d`; coprimality forces d>=13 and e>=14, impossible. If d=e, the gap is `1/(27d)>=1/108`. If e>d, `13(e-d)-d>=10`; if d>e, `14(d-e)+e>=15`. The unequal case has de<=12, so either gap exceeds1/108. This is an exact unordered separation. Setting d=e=4 to infer exact psi values would be unsupported.

The explicit two162-vertex constructions yield only upper bounds95/108 and47/54. Those bounds alone would not show asymmetry. The universal packing argument and finite integer invariant are what exclude equality.

## Earlier-turn LP and sampling audit

TURN_2 matches the independent matrix formulation sealed earlier. The B-polytope contains both constraints `Pb>=x1` and `Q^T b>=y1`. Fixed-topology forward and reverse objective LPs optimize different outside-part probabilities. Their compact closed optima exist, but mixing with strictly positive feasible points is necessary to obtain the infimum over positive retained support. For rational x,y, rational vertex optima and rational positive feasible points exist in their respective rational polytopes; rational mixtures and exact blowups preserve all paths.

The forward certificate has u a C probability, v>=0 on B and `Ru-Pv>=lambda1`; multiply by p to get `max(R^T p)>=x sum(v)+lambda`. The reverse certificate uses an A probability and `R^T u-Q^T v>=lambda1`, so `max(Rq)>=y sum(v)+lambda`. Nonnegative v and normalized u are essential, and the candidate's displayed certificates meet those requirements. The positive family has f=1/2, g=2y. Universal values remain1/2 in both orders by the credited max-degree lower bound and two disjoint components. The support deletion is a change of graph that removes individual constraints, exactly as acknowledged. No fixed-template dual is promoted to a universal lower certificate.

TURN_1's cofinal rational formula uses actual finite degree minima and near-minimizers. It handles possible nonattainment directly. Monotonicity and exchanging actual rational parameter minima preserve the gap direction. Right continuity is claimed only when both coordinates are irrational, where any chosen finite graph has strictly larger rational minima; no threshold continuity is inferred.

For sampling, conditional independence holds separately for every chosen endpoint's n opposite-part draws. Four directed degree families and two original-reach-set domination families yield6n events. Sampled B can delete original paths, which only improves the upper reach bound. Copies of repeated selections are ordinary twins. The tilted-Bernoulli variance bound1/4 proves the exponent, and the ceiling estimate gives failure probability at most0.24<1. The finite table sandwich keeps its parameter shifts and the sufficient gap certificate requires an exact global reversed table lower bound. No such table is claimed computed. These are valid scoped deductions and do not prove symmetry or supply the final pair.

## Source-duality and boundary concerns resolved for this candidate

The source2.2 support, source2.3 attainment and simultaneous-reweighting concerns in the independent seal remain valid cautions about those routes. TURN_3 avoids them: elementary finite counting replaces transposition duality; integer minimum replaces unbounded graph minimization; rational theta affine systems and explicit positive blowups replace generic boundary approximation. Starred rotation is not used in the decisive proof. The source's omitted12.2 proof is credited but is not required to obtain the new boundary formula or gap.

## Frozen program inspection and proof/computation consistency

All four source programs use only standard-library rational arithmetic, finite enumeration and JSON printing; two read adjacent certificate JSON files. There are no network calls or writes to the candidate namespace. Replay must use byte-identical private copies with their certificate files adjacent.

`verify_turn1.py` tests finite reach domination and envelope arithmetic; it does not execute the analytic concentration proof or enumerate a global optimization table. `verify_turn2.py` samples572 rational family parameters and checks both fixed-template dual matches and the120-vertex graph. `verify_turn3.py` validates the seed, complement, two ordinary graphs, cyclic templates and finite3+3+3 boundary cases; it does not compute d(theta). `review/check_independent.py` adds set-based reach controls, repeated C types and additional A vertices. Their scopes agree with the proof; replayed PASS and count totals will remain finite computational evidence.

Historical source-gate searches, branch/ref totals, number of genuine author turns, review independence and remote exactness are provenance assertions to validate separately. A target's public self-description or nested hash is not evidence that every earlier search or private read actually occurred. Existing historical snapshots and wrapper states are not inconsistent merely because the later disposition changes their status.

Audit completion estimate: 55%. Mathematical analytic assessment complete; executions, fresh artifact bindings, actual Git history and public replay policy pending. Strongest verified mathematical result is the claimed unordered absolute gap, subject to independent source-seed arithmetic replay. No later-literature priority conclusion is claimed.
