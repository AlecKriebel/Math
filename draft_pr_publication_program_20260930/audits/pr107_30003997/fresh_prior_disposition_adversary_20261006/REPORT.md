# Fresh adversarial audit of PR107 prior-work disposition

Audit completed 2026-10-06 UTC. Scope: PR107, problem30003997 / OWR-16633-014, original head `cc2ae01897135b35bee135917819e782a220f2c1`, original attempt1/5, additional central proof-search turns0. This is an audit, not a new research solution or publication.

**Verdict: the bounded `already_solved` classification is defensible when it means “the advertised hardness theorem is an elementary consequence of an inspected published construction; no novel resolution is established.” Closing without merging, with no paper, DOI or publication-tracker row, is proportionate.** No mathematical counterexample, source-access gap or model mismatch remains that requires this disposition gate to stay pending. This does not establish earliest priority or a global absence of possible further results.

## Independent source and mechanism

Before reading root's theorem comparison, root's prior checker/results or other prior-family final reports, I pinned and read the original source record/manifest, full Kaibel contribution at printed3014-3015 / PDF46-47, repaired v1 proof/checkers/actual results and mathematical gate, and the full-primary Chapoullie-Szigeti Theorem13 construction, Figure2 and both proof directions at printed11-12. `INITIAL_MECHANISM_FROZEN.md` and its receipt record the independent reconstruction. The first display timestamp was corrected to its already recorded actual receipt time before root comparison; the mechanism text was unchanged.

The original Kaibel Problem2 uses one fixed root, one common spanning out-arborescence, and a distinct arc-cost vector for each nonroot destination, summed along that destination's root path. The literal source permits real costs; rational binary-encoded coefficients give a computational decision model, and the binary restricted family suffices for hardness of the source optimization. The source's Problem1 and Wong's polyhedral motivation are separate from the theorem audited here. The curation's generic “open” label and background sentence are not priority evidence.

The decisive primary is Romain Chapoullie and Zoltan Szigeti, *On packing time-respecting arborescences*, Discrete Optimization45(2022),100702, [DOI10.1016/j.disopt.2022.100702](https://doi.org/10.1016/j.disopt.2022.100702), [author-hosted primary](https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf). The exact local PDF is793145bytes, SHA256 `cd4fc5328ec4ae96f895767a172367cc4eac2b7cc7c87b4da0d393fc0519c7a8`; root's retrieval receipt is independently pinned. No third-party PDF or long extract is copied into this audit. Four rendered pages were inspected, hashed, then deleted; their hashes/disposition remain recorded.

## Checkable proof-level containment

For a3-regular3-uniform exact-cover instance with h elements and h hyperedges H_i, the published graph has selectors u_i, element sinks v_j, and conflict sinks w_ij for distinct unordered intersecting pairs i<j. Each u_i has two distinguishable parallel root arcs, black and gray. Exits to elements are black and exits to conflict sinks are gray. A monochromatic spanning arborescence selects a color for each u_i: each element requires a black-selected parent and each conflict requires a gray-selected parent. The black-selected hyperedges thus cover all elements and are pairwise disjoint. Conversely an exact cover gives those choices.

Subdivide each original root arc separately, obtaining s->b_i->u_i and s->g_i->u_i. Both arcs s->b_i and s->g_i are forced, since their heads have indegree1. Each u_i chooses exactly one of its two remaining incoming arcs. Unused intermediate vertices are forced root leaves. Each sink still chooses one original incoming arc. Therefore *all ordinary feasible trees*, not only monochromatic or zero-cost ones, have a bijective correspondence with the original parallel-arc parent choices. The inverse compresses the selected u_i path and deletes the unused forced leaf. Acyclicity and root reachability exclude hidden noncanonical trees.

For each element destination, charge every gray first root arc1; for each conflict destination, charge every black first root arc1. All other entries, including all coefficients for intermediate and selector destinations, are0. Its actual path sum is exactly the indicator that the selected first color disagrees with its fixed exit color. Consequently total cost0 is equivalent to the published monochromatic condition. This is a destination-specific sum over a single common tree; it does not replace the objective by a common arc vector, capacities, max-cost constraints or independent paths.

The expanded graph is simple with four consecutive layers, every arc goes to the next layer, every root path has depth at most3, and all vertices are reachable. The new intermediate, selector, element and conflict indegrees are1,2,3 and2 respectively. With m=h+|W|, there are1+3h+m vertices and7h+2|W| arcs. Each hypergraph vertex generates at most three distinct pairs, so |W|<=3h. Even a full dense destination-by-arc table has polynomial size. The finite integer-input certificate is polynomially checkable; binary cost0 has no cancellation, so existence of a zero-cost tree, optimum0 and threshold<=0 agree on this subclass. Bounded numbers establish strong optimization hardness.

Adding1 to **every** destination-by-arc entry, including formerly zero vectors and entries unused by particular paths, adds the fixed path-length total2h+2h+3m=4h+3m for every feasible tree. This recovers all-positive coefficients{1,2} and the same decision answer at threshold4h+3m. It is not valid to infer this constant shift for arbitrary graphs with variable root-path lengths; the consecutive layers are essential.

This supplies every advertised restriction of the candidate's hardness bundle. The 2022 theorem statement alone does not print that bundle: the proof-level graph and the explicit transformation supply it. The prior paper does not literally state Kaibel's cost-table formulation.

## Attempts to falsify the containment

| Challenge | Audit result |
|---|---|
| Subdivision adds spanned unused vertices | Harmless forced root leaves; all costs for these destinations are0 and the full ordinary-tree inverse is checked. |
| Hidden trees or disconnected selections | All original/expanded trees have one parent per nonroot vertex; layers imply reachability. Small unfiltered edge-subset enumeration additionally finds exactly all16 mapped trees. |
| Destination-cost sum differs from monochromatic paths | Dense path summation agrees with an independent original arc-color calculation for every tested tree. A deliberately corrupted destination price is rejected. |
| Full table, empty cases, infeasibility | Dense entries are explicitly constructed; nonempty RXC3 sinks always have a parent. Empty direct input is root-only feasible; candidate preprocessing uses fixed promised yes/no instances when needed. No encoding blowup or feasibility loophole arises. |
| Depth/degree/positive alphabet | All expanded arcs and indegrees are checked. Universal1-2 offset holds for all ordinary trees, including positive binary-cost trees. |
| Literal published W display | Self-pairs break the proof. A positive six-element instance has3 exact covers, but adding diagonal conflict sinks raises the binary minimum to2. This defect is explicit, not ignored. |
| Ordered duplicate pairs | Duplicating distinct pairs preserves zero feasibility but doubles pair counts and changes positive optimum accounting. The intended family uses distinct unordered pairs. |
| Published root-set intersection notation | Displayed nonroot reachability sets omit s despite an intersection written s. Adding the root to both, or using disjoint nonroot sets, fixes the display. The direct parent-choice argument avoids reliance on it. |
| Generic signed exact-zero inference | Rejected outside the nonnegative subclass: a sole feasible tree of cost `-1` meets threshold<=0 but supplies no exact-zero witness. This generic distinction does not invalidate the binary reduction. |

The omitted i<j condition is compelled by Figure2, the |W|<=3h counting bound and the converse's explicit j<k. A reader taking diagonal pairs literally would see a broken yes-construction; the local convention must be stated. Neither notation correction invents a new hardness mechanism or transfers the central problem to an unsupported claim.

## Fresh computational evidence and its limits

`fresh_checks.py` uses distinguishable original arc identities, independently builds the expanded dense table, reconstructs root paths, and checks ordinary-tree inverse mapping, original monochromaticity and destination sums with explicit exceptions. `replay_checks.py` records all actual subprocesses, stdout/stderr hashes and expected failures. Normal and optimized runs yield identical semantic fresh results:4,648,994 explicit checks per run.

- A small generic positive graph: all16 ordinary trees mapped, with2 zero trees; an unfiltered expanded edge-subset census independently finds the same16 trees.
- All four triples on four elements: all82,944 ordinary trees mapped; optimum1 and no exact cover. This is a3-regular3-uniform boundary control, **outside** the divisible-by-three RXC3 universe-size promise. It is not used as the hardness premise.
- Consecutive cyclic triples on six elements: all64 selector assignments and all3 exact covers checked; optimum0 and positive threshold78. Two thousand complete ordinary trees are sampled, then each exact cover is used to construct and cost an actual zero tree.
- Cyclic triples with offsets{0,1,3} on six elements: all64 selector assignments checked, no exact cover and optimum2; positive threshold87. Two thousand complete ordinary trees are sampled.

The last two controls meet the usual universe-size divisibility promise. Exact per-assignment minima are computed through exhaustive independent terminal marginal choices and an arbitrary-size separability argument; sampled tree absence is never used as evidence of no cover. Full trees for the six-element families are not exhaustively enumerated (191102976 and1528823808 possibilities). Finite checks support the universal proof above and do not replace it.

The effective candidate v2 author and independent checkers reproduce their actual receipts exactly in both normal and -O modes:449 formulas/12696 trees and114 formulas/1674 trees/222114 examined edge subsets respectively. Four deliberate false candidate guards fail nonzero, as do both fresh RuntimeError guards, under normal and optimized Python. The latest replay bundle contains12 actual runs. The guards are explicit raises, so optimization does not erase them.

## Exact-optimum identity and possible surviving novelty

The candidate's identity

`min_T C(T) = min_assignment number of unsatisfied clauses`

is correct for the ordinary cleaned-formula construction and is formally stronger than satisfiability equivalence. Duplicate signed literals and tautological clauses are harmless for unsatisfied counts; the fixed trivial branches preserve the decision answer rather than promising the raw formula's exact count. The identity is an objective-preserving reduction property for general mixed-literal3SAT, not merely an equality for the RXC3 family.

**I do not claim that this all-formula identity is printed in, or logically follows solely from, the 2022 decision theorem. Its precise historical priority remains unresolved.** For a fixed assignment, however, every clause independently chooses one witness literal. The minimum false-witness indicator is0 for a satisfied clause and1 for an unsatisfied clause. Thus the identity is immediate objective accounting once the candidate gadget is fixed. The transformed prior graph has analogous accounting for uncovered elements plus overlapping selected pairs.

The candidate establishes no additional approximation threshold, parameter boundary, counting result, exact algorithm or independently consequential optimization theorem. The exact correspondence and direct SAT exposition have legitimate explanatory and reproducibility value, but their presence does not establish a new resolution of a target whose entire advertised hardness bundle is already contained in a prior published construction. This is a bounded novelty assessment, not a proof that every possible useful extension is known. A separately stated consequential theorem would warrant its own claim and source-bound audit; none is promoted here.

## Current package and final closure text

After the initial mechanism was frozen, I read/pinned root's comparison/checker/results and the final reports of the exact-question, classical-network and Wong-formulation families. These are labeled **post-freeze supplemental comparisons**. Their broader history and unread older sources are not proof premises of this fresh containment argument. They agree with the bounded disposition and preserve the exact-identity uncertainty.

The original mathematical gate remains a dated v1 snapshot. Current `repaired_diagnostics_v2` changes only the review header and old negative priority-search paragraph; both checker files are byte-identical to v1 and the mathematical reduction is unchanged. V2 proof SHA256 is `27968a88187710ac83fc68c96cfda1edbdeda1eae6fc7da80929f4def6477436`. It now cites the verified prior corollary and labels the identity's priority unresolved. I read the complete proof, metadata diff, notes, effective artifact pins and current receipts. No stale “search found no prior proof” assertion is relied upon as a current conclusion.

I also reviewed the unposted closure comment. An optional clarity correction was adopted: its description of gray overlap arcs explicitly states distinct unordered intersecting pairs i<j, with figure/count/converse support. The old and final body hashes/bytes are pinned separately in `FINAL_CLOSURE_BODY_PIN.json`; no mathematical inference or disposition changed. The final closure body SHA256 is `ac74e0fd61258c54ece26cdea76f1b1b8673d4b63e5031c798d14ce079ccbdc5` (3159bytes).

The final text distinguishes a published corollary from identical printed wording, rejects earliest-priority/global-refinement claims, preserves the exact identity and archived original1/5 attempt, and says closure concerns priority rather than a counterexample. It is defensible as written.

## Final bounds and recommendation

Strongest verified result: the full binary/zero-threshold/simple/reachable/consecutive-layer/depth-three/indegree<=3 hardness theorem and positive1-2 variant are elementary consequences of the inspected2022 published construction, with the published pair convention made explicit. The candidate itself is mathematically sound after its minor repairs.

Unresolved: earliest historical priority; precise earlier wording/priority for the all-formula SAT optimum correspondence; other potential separately formulated consequences. These are not access or model gaps blocking the bounded `already_solved` disposition.

Recommended action: close PR107 without merging, record `already_solved` with the explicit corollary qualification, retain the audit and original attempt, and create no paper, DOI, Zenodo deposit or publication-tracker row for this disposition. This agent performed no service action, Git/index mutation, commit, outreach or outreach preparation. All writes stay inside this assigned audit directory; the original candidate and turn ledger are unchanged. Main branch was checked. Assigned bounded audit completion:100%; new-discovery completion is not estimated as a probability or claimed.
