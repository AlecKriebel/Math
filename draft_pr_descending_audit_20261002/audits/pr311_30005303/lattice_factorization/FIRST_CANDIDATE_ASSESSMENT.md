# First candidate assessment, frozen before candidate code release

UTC checkpoint: 2026-10-04 16:03:11 UTC.
Scope: original snapshot TURN_1.md, TURN_2.md, SOURCE_GATE.md, SOURCE_RECHECK_2.md only, released explicitly by parent after source criteria freeze. No candidate checker code, outputs, inherited review, root conclusions, or other-family findings have been read.

## Verdict and strongest verified result

No mathematical defect found in either bundled candidate answer at prose stage. TURN_1 gives a valid binary MTP2 globally Markov C4 distribution outside clique factorization and its closure. TURN_2 proves the stronger boundary characterization F_2(G)=closure A(G), with unary-and-edge factors, and correctly recovers the literal source edge-only closure. Thus the proposed answers are Conjecture 1 affirmative and Conjecture 2 negative. This verdict rests on direct deductions and this family's independent exact controls, not candidate test success or an author status.

Novelty/priority is not assessed at this gate. SOURCE_GATE and SOURCE_RECHECK_2 are source bindings and limitations, not independent priority certificates. Candidate code claims and recorded assertion counts remain unverified until the next explicit release.

## Turn 1: independent adversarial verification

1. **Normalization/zeros.** Eight support points, seven weights 1 and one weight 2, give total 9. Every coordinate has both values. No strictly positive ambient-support theorem is being invoked.
2. **MTP2.** Duplicating the first coordinate preserves meet and join. The support is a sublattice. The weight 2 occurs only at its top, so the full meet/join inequality holds on every supported pair; outside-support pairs have right side zero. This matches the independently frozen source C6 mechanism.
3. **Global Markov.** For C4 the only nontrivial separators are the two opposite pairs. Each leaves a singleton fixed by the equality X1=X2. These are the full global separation statements because every smaller conditioning set leaves a connected graph and every larger one leaves fewer than two vertices. Degenerate conditional distributions are legitimate; null events impose no conditional assertion.
4. **Factor obstruction.** The even/odd latent cube product has balanced restrictions on every original edge, every singleton, and the empty clique. Substituting any finite real factors gives the same product without division. The two actual products are 1 and 2 in unnormalized weights. Signed or zero potentials cannot escape this invariant.
5. **Closure.** The invariant is a finite polynomial, so the C4 distribution lies outside the closure as well. The candidate correctly does not use this example to refute the different closure claim.
6. **C6 control.** The independently derived C6 equality-block control remains valid, without any dependence on the candidate's implementation.

Independent reconstructed C4 check: 256 MTP2 pairs, 4 ordered nontrivial separations, 256 exact marginal CI minors (this is a deliberately different count from the candidate's pending checker), even weight product 1, odd weight product 2. No candidate code/output was read.

## Turn 2, sections 2-3: support and ferromagnetic approximation

- Equation (4) is valid precisely because p already has a nonnegative local factorization. If every local projected pattern occurs in a positive global atom, the corresponding original factor is positive there; satisfying all such local projection conditions therefore makes their product positive. The candidate does not incorrectly apply this argument to arbitrary globally Markov distributions.
- All active coordinates range from 0 in the support bottom to 1 in its top. An active-edge projection is a sublattice containing 00 and 11, giving exactly the four listed possibilities. Fixed-active edges allow both active values and add no hidden relation.
- Missing 10/01 patterns give directed implications; strongly connected components enforce equal values. Their acyclic quotient and reachability order capture the entire support, because equation (4) excludes unlisted constraints. Its support atoms are exactly upper sets.
- Comparable distinct components have precisely three projected patterns. Restricting an arbitrary log factor to 00,01,11 is affine; any apparent quadratic term is redundant there. Edges within an equality component and fixed-active edges are unary. This is not a positivity assertion about the original individual couplings.
- For incomparable components, the chosen upper set of their strict successors excludes both components, and adding either component alone or both still gives upper sets. The resulting four support atoms differ only at those components. The mixed log difference isolates exactly the aggregated coefficient K_AB, so full MTP2 gives K_AB>=0. There is no leakage from other interactions and no assumption that each original edge coefficient is nonnegative.
- Every nonzero aggregate coefficient has an original edge on which it may be placed; each unary may be placed at a representative original vertex. Thus L is a quadratic polynomial on the original graph with nonnegative interaction coefficients.
- D is integer valued and nonnegative. Its zero set is exactly S by pins and the original missing-pattern implications. Every penalty -t xi(1-xj) contributes nonnegative original-edge interaction +t xi xj and a unary term. A pinned-bit penalty is also unary. Therefore p_t is strictly positive attractive, with the correct normalized limit p. Equality components, a single-point support, and disconnected graphs do not create an omitted case.

Independent exact boundary controls:

- Equality block {1,2}, edges 13 and 23 carrying original couplings -2 and +3 respectively, has aggregate +1 and is MTP2. A lifted +1 interaction reproduces its on-support weights exactly. This control catches any erroneous demand for individually attractive original factors.
- The support x1<=x2<=x3 makes -3 x1x3 equal to -3 x1; a seemingly negative quadratic is correctly absorbed into a unary. All 64 MTP2 pair checks pass.
- Local support reconstruction passes for these examples and for the C4/C6 falsification controls; support reconstruction alone still does not give weight factorization of the latter.

## Turn 2, sections 4-5: independent residual-flow and normalization audit

Starting independently with the oriented energy,
E(x)=sum_(i->j) J_ij xi(1-xj)+sum_i b_i xi,
where b_i=-h_i-sum_(i->j) J_ij,
produces the cut identity C(x)=E(x)+kappa, kappa=sum_(b_i<0)(-b_i). Signs match both terminal cases: i->t costs b_i xi; s->i costs (-b_i)(1-xi).

Use an antisymmetric net flow g_uv=-g_vu as an independent notation. Residual capacity is c_uv-g_uv, equivalently the candidate's c_uv-f_uv+f_vu. Summing conservation on any source side gives net outgoing value v and hence residual cut sum C-v. All residual capacities are nonnegative. Compactness of the finite bounded feasible flow polytope supplies a maximum even for real capacities; a positive residual s-to-t path would permit a finite augmentation, contradiction. The residual reachable set gives a zero-residual cut, so v=min C. This argument uses no possibly nonterminating real-capacity algorithm.

Consequently the residual cut cost is exactly E(x)-min E, and every residual arc that can cross is either terminal-to-vertex (a unary) or between original edge endpoints. Reverse residual arcs introduce no new graph edges. Arcs entering s or leaving t cannot cross a source-side cut. The factor product therefore equals exp(-(E-min E)) exactly.

At a minimizing configuration, residual cut sum is zero; each selected residual factor is exp(0)=1. This proves max_x W(x)=1, and therefore 1<=sum W<=2^|V|. This is the necessary nondegeneracy bound, not an assumption about the unconstrained factor model. It survives parameter convergence.

The local parameter space is a fixed finite compact cube. Each W(x) is a product of selected parameters, with unselected factors interpreted as 1; this avoids an undefined 0^0. Along a convergent parameter subsequence, every weight and the finite normalizer converge, and Z>=1 permits division. The factorizing limit is MTP2 because the finite polynomial inequalities are closed. This proves closure A subset F_2 independently of the support approximation, so there is no circularity.

Independent exact controls use base-2 rational weights and integer capacities, avoiding floating tolerance. Exhaustive graphs/fields/couplings through 3 vertices plus deterministic cases on 4,5,6 vertices, including mixed edge orientations, give 2,068 cases and 25,175 exact energy/cut/factor state identities. Every case satisfies the conservation, residual nonnegativity, min-cut value, factor identity, and normalization bounds. These finite computations supplement the all-real/all-graph proof; they do not supply its quantifiers.

## Global Markov and source boundary recovery

Conditioning on a positive-probability x_C leaves factors within the connected components of G minus C. The normalizing sum splits because the remaining variable sets are disjoint. Thus nonnegative unary/edge factorization implies full global Markov even with zeros. Null assignments require no division or assertion. The theorem concerns precisely the source intersection rather than merely a class called Ising.

For a graph without isolates, all unary factors and the scalar normalization can be absorbed into incident edges. With isolated vertices, a literal edge-only product is independent of them and hence uniform on their coordinates; removing them leaves exactly the same nonisolated model. The MTP2 condition and pointwise closure are preserved by the fixed uniform product. Empty-edge and empty-vertex conventions are addressed correctly in section 6. Conventional arbitrary isolated-vertex unaries are covered by the theorem itself.

## Distinct independently frozen closure mechanism

This family had already frozen a separate mechanism before reading TURN_2:

- Represent any binary lattice support by pins, equality blocks and poset implications.
- Full global Markov forces each equality block to induce a connected G subgraph and each implication cover to have a G edge between its endpoint blocks. A pair of support states differing exactly on the implication interval proves both assertions by conditional rectangularity.
- Hence the support of a Markov lattice law is determined by unary and edge projections.
- On the positive support of an edge-factorizing limiting sequence, restricted log densities lie in the same finite edge-design column space. It is closed, so the limiting log density still has a finite edge representation there; zero forbidden edge cells then recover the complete support. Literal isolated coordinates stay uniform.

This gives an alternative route to the closure conclusion without max-flow. It cannot incorrectly give factorization to every lattice-support Markov law, because the restricted log design-space membership comes from the approximating factorizing sequence. The C4 and C6 controls exhibit exactly the missing membership in the broader refuted statement.

## Artifact bindings, access bounds, and remaining gap

Released prose SHA256:

- TURN_1.md: 909ea0bb5330c037fabda8dfc468bfdc7af5e95809db516d3d20fb303b061374
- TURN_2.md: d2594ebda66841fd57355e4bbc41cc48c0c2a73033a6979a201abb967e69d20b
- SOURCE_GATE.md: 8e1642adcc4c3870e17f8c3780b2df11313a50226fe068f52394f9070c924695
- SOURCE_RECHECK_2.md: c6a2fd7bb6c7e0d97cfbc22e902d87e6855bbe660d754aa499f54f2e25cbb9e0

Own artifacts: source_control_exact.py/source_control_result.json and prose_controls_exact.py/prose_controls_result.json. They do not import or read candidate material. All writes confined to this family folder; no Git/remote mutations or external communication.

Strongest verified result: both exact source mathematical questions have complete, internally valid prose solutions, independently supported by distinct source-first lattice reasoning and exact controls. Remaining gap: candidate implementations and declared reproducibility have not been released/reviewed; priority and full publication packaging remain separate. Completion estimate: 100% of prose mathematical audit, 85% of this family's complete mathematical audit including pending candidate-code reproduction; 0% of priority certification. Freeze at mode 0444 with SHA256 manifest, send parent, then wait for code release.
