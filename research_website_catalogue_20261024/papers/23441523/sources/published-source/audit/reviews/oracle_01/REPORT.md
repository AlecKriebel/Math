# Independent adversarial audit: adaptive oracle lower bound and exact problem model

Audit completed 2026-10-17 UTC. Scope: PR 1119, claimed head `786fff9ba06951209e8c1e3bc6114efbfa2c9d16`, frozen `inputs/PROOF.md`, 25,005 bytes, SHA-256 `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`. The local proof bytes match that pin; I did not independently inspect remote Git state.

## Verdict

**No blocking mathematical defect found in the adaptive lower bound, its prerequisites, or its alignment with the original question.** In particular, the lower bound applies to unrestricted two-sided adaptive adjacency access with a worst-case bound on the total number of sampling and adjacency calls. This is the complexity counted in the primary problem statement. The comparison is therefore an answer to the original problem, rather than a claim confined to canonical sampled-vertex testers.

The strongest verified quantitative conclusion is

\[
 s+2e\ge\left(\frac{n^3}{12T}\right)^{1/3},\qquad
 Q\ge\left(\frac{n^3}{96T}\right)^{1/3}\ge m^{1/3},
\]

for the manuscript's family and success probability at least two thirds, where `n=6m` counts tail vertices, `T=mK`, `Q` bounds total oracle calls, and `s,e` are separate worst-case sampling and adjacency bounds. Together with the polynomial classical upper bound, this rules out every fixed polynomial comparison of the two complexities, even after constant proximity rescaling. All weights are positive rational numbers.

This is a mathematical audit of the pinned manuscript, not a priority determination or external peer review. I independently reconstructed the proof before reading `inputs/MATHEMATICAL_AUDIT.md`; after completing that reconstruction and the first finite checks, I read that prior audit as a comparison. Its conclusions were not used as premises.

## Exact target and primary-source ledger

The original publisher PDF is [Oberwolfach Report 19/2019](https://ems.press/content/serial-article-files/46798), physical PDF page 27, printed page 1139, Problem 5. Its model on the preceding page defines the complexity by counting sampling and adjacency calls together. The distribution is unknown and graph size is not supplied. Its weighted distance counts each unordered changed pair once. The question ranges over hereditary extendable graph properties. The manuscript preserves each condition; its classical tester also works without receiving graph size.

The actual current [arXiv record](https://arxiv.org/abs/1905.09903), retrieved 2026-10-17, still lists v5, submitted 2021-09-28, as latest. The downloaded unversioned [current PDF](https://arxiv.org/pdf/1905.09903) identifies itself as v5. Page 2 again counts both call types; Problem 5.6 is on physical page 22. Proposition 5.7 separately discusses canonical vertex-sample counts, with adjacency inspection understood. Footnote 24 allows a constant proximity relaxation for irrational distributions in that positive transfer. The present proof does not use that transfer.

[Goldreich's author manuscript](https://www.wisdom.weizmann.ac.il/~oded/R3/vdf.pdf), dense model pp.10–12, likewise counts graph and sampling queries together. Proposition 2.2 converts to sampled-endpoint access under its stated hypotheses; this lower bound does not depend on it. Goldreich's ordered-pair distance is twice the present unordered-pair normalization. That convention change cannot remove a superpolynomial separation, and no numerical constant is imported from it.

These are model-consistency checks, not an extensive novelty search. Complete retrieval URLs, sizes, timestamps and hashes are in `SOURCE_LEDGER.json`. Primary source bodies and text extracts were retained locally for audit use, not authored as new research results.

| Retrieved body | Bytes | SHA-256 |
|---|---:|---|
| Original OWR publisher PDF | 718945 | `f88f89375b4b427312169552c106d6395dd249cacc6040b8eb8b23726a95d8de` |
| Current unversioned arXiv PDF | 506856 | `6ddba2d03267d367dffb8dd3ce23f6f5f6afb36496ee68142c02119d398c2b4d` |
| Current arXiv abstract/history HTML | 40865 | `05b86c8d0d22309f0a3c971e6046162eab86d0754edeaa034b589dfe4b4de4ed` |
| Goldreich author PDF | 677203 | `d5758b714c936a7e1d215ed24a61a1bc4d6f9aa22edbdc5e5873d64ac56afbad` |

## Independent reconstruction of the lower-bound mechanism

### Deterministic prerequisites

Let the fixed property be `P = K4-free ∩ A3`, where `A3` means deletion of at most one vertex permits a 3-coloring. Deleting a vertex, adding an isolated vertex, and deleting edges preserve the relevant conditions. Every 3-colorable graph belongs to P. Thus the property is hereditary, extendable, and edge-monotone, with no parameter dependence.

For a 3-colorable tail H, adjoin a universal apex of mass `1/2`, and give each tail vertex mass `1/(2n)`. I independently checked the distance identity

\[
 \operatorname{dist}_D(J(H),P)=\tfrac14\operatorname{dist}_{U_n}(H,\text{triangle-free}).
\]

The upper bound deletes a minimum triangle edge-hitting set; the remaining tail remains 3-colorable. For the reverse bound, any repair F in P, including additions, must have a triangle-free subgraph on the tail vertices whose apex edge survives. If S is the set losing that edge, isolate S in the repaired tail. Off S, use F's tail edits; original edges incident with S contribute at most `n|S|`. Dividing by `n²` gives at most four times F's total weighted cost, since one apex-edge removal costs `1/(4n)`. This argument does not restrict the permitted repairs to deletions.

The explicit host R has exactly T designated edge-disjoint triangles and no other triangle. The arithmetic check is important: every edge determines its `(x,a)` index, while a purported triangle has part-differences `a,b,2c`, hence `a+b=2c`. The no-progression set forces `a=b=c`. Equal sphere norms and the no-carry digit representation prove that set's stated property. These give a 3-partite host and all deterministic hypotheses used below.

### Pattern distributions and farness

On each triangle, GOOD is a uniform even-parity three-bit vector and BAD a uniform odd-parity vector; triangle patterns are independent. Every restriction to fewer than three edge coordinates is uniformly distributed under both laws. This is a joint-coordinate statement, stronger than equality of individual edge marginals.

GOOD has no full triangle and is always in P after adjoining the apex. For BAD, the number Z of full retained triangles is `Bin(T,1/4)`. Exactly Z original edges must be removed to make the tail triangle-free, because its full triangles are edge-disjoint; adding edges cannot remove an existing triangle. Therefore the weighted distance is exactly `Z/(4n²)`.

The exponential-moment calculation with parameter `log 2` yields

\[
 \Pr[Z<T/8]\le e^{-T/32}=:p.
\]

Thus at least `1-p` of unconditional BAD is `epsilon_d`-far for `epsilon_d=T/(32n²)`. There is no need to condition the hard distribution on farness, an operation that would introduce correlations into the pattern coordinates. This avoidance is essential, and the proof handles it correctly.

### Deferred labels with arbitrary adaptive query endpoints

The tester receives n, the apex name, the entire weight vector, and the n tail names. A secret uniform bijection assigns those tail names to the fixed host vertices. All tail weights are equal, so the weight vector reveals no information about that bijection. A name counts as exposed only when it appears in an actual sample or adjacency call; knowing the name set in advance does not expose its graph incidences.

Enlarge the tester's observations by supplying the full graph induced on the exposed labels. An execution with s sample calls and e adjacency calls exposes at most `s+2e` tail names. Querying the apex is uninformative. Two fresh endpoints of one adjacency call may be exposed sequentially; allowing observation after the first exposure would only give still more power.

The symmetry assertion needed here is precise. Condition on:

1. the exact host image of every exposed tail name;
2. the full public transcript and algorithm coins used so far; and
3. all pattern-coordinate restrictions revealed on those names.

The remaining part of the bijection is uniform over all bijections between unused names and unused host vertices. Indeed, every observation concerned only already assigned names. Given their exact images, each observation restricts pattern bits and leaves the unused-name permutation independent. A new name chosen as any function of the transcript consequently has a uniform image among the remaining host vertices. This remains true after many negative adjacency answers, and does not assert that the tester's posterior on the *exposed* host images is uniform.

Sampling returns the apex with probability `1/2`, otherwise a uniformly random tail name. This can be coupled with the same sample-name random tape in both worlds. Repetitions reveal no additional image; whether a returned name is repeated is identical while the public transcripts coincide.

This conditioning argument defeats the potential adaptive attack: observations can identify likely host geometry of already seen vertices, but they cannot select an unused *name* whose host image is preferentially the desired third vertex. The unused names remain exchangeable. If the entire secret mapping were provided, that attack would work; the finite negative control below verifies this boundary.

### Joint GOOD/BAD coupling

Use common private coins, sampled names, and newly assigned host images. For every designated triangle, defer pattern choices until its observed coordinates are needed. Before the first time that all three vertices of any designated triangle have been exposed, each observed coordinate subset is proper, so its GOOD and BAD laws agree. Independence across triangles permits a simultaneous common coupling. Non-host edges are always zero.

If one exposure completes a designated triangle, stop the common-transcript coupling before supplying its possibly different full-pattern answer. Both marginals can subsequently be completed with their proper conditional laws. Until that event, the common transcript makes the adaptive tester take the same actions in both worlds.

An occasionally misleading shortcut would be to claim uniformity *after conditioning merely on having avoided a triangle*. That conditional set is generally biased. The valid argument instead uses the full sequential experiment. Continue either designated world after coupling failure, and pad after algorithm termination by drawing fresh uniform remaining images until k images exist. Conditional on all previous images and the full actual history, every next image is uniform unused. By induction the **unconditional padded sequence** is a uniform ordered k-sample without replacement. The event that a real exposure causes coupling failure is contained in the event that the padded prefix contains a designated triangle.

For each fixed triangle, that probability is `(k)_3/(n)_3`. The union bound therefore proves

\[
 \operatorname{TV}(\mathcal T_{GOOD},\mathcal T_{BAD})
 \le \min\{1,T(k)_3/(n)_3\}.
\]

When `k<n` and `n≥6`, `(n)_3≥n³/2` gives the coarse bound `2Tk³/n³`. When `k≥n`, the same coarse bound is at least one and is trivially valid. Stopping early cannot violate the bound; it can only reduce actual exposures relative to the padded sequence.

### Error quantifiers and the total-cost bound

A randomized tester valid for each fixed weighted input rejects any GOOD input with probability at most `1/3`. Averaging its pointwise soundness over unconditional BAD gives rejection probability at least `(2/3)(1-p)`. Thus the rejection-probability gap is at least `1/3-2p/3`, and is at least `1/6` when `p≤1/4`. Actual d≥4 parameters have T far above `32 log 4`.

A decision event's probability gap cannot exceed transcript TV, so the exposure bound forces the displayed inequality for `s+2e`. This argument already includes the algorithm's random coins in the coupling; no unproved deterministic-tester reduction or informal invocation of Yao is needed. For a total worst-case call budget Q, apply the same reasoning directly with `k=2Q`, allowing the sample/query split to vary across executions. Since `s+2e≤2(s+e)`, the constant 96 follows.

If all adjacency endpoints must be sampled labels, use `k=s` instead, even if all their pairwise adjacencies are free. Conversely, a sample-only lower bound with *arbitrarily many free queries to arbitrary known names* would be false: a tester could retrieve the entire finite graph with zero sample calls. The theorem does not claim that false stronger statement. The original problem's total-cost convention is why this distinction does not leave a gap.

### Quantitative separation and boundaries

The parameters give `T=mK`, `n=6m`, and `K≤m`, hence

\[
 \frac{n^3}{96T}=\frac{216m^2}{96K}\ge m.
\]

The floor loses at most a factor of two for d≥4, giving the manuscript's bounds

\[
 \frac1{2304d2^{3d}}\le\epsilon_d\le\frac1{1152d2^{3d}}.
\]

Thus `log(1/epsilon_d)=Theta(d)` and `log(m^(1/3))=(log 2)d(d+1)/3`. Both sides use fixed P. A sequence of such lower bounds already contradicts any fixed polynomial upper comparison required for every small epsilon. Positive rational weights give direct exact instances; irrational approximation is unnecessary. Replacing classical epsilon by any constant multiple preserves its polynomial upper bound.

The conclusion concerns worst-case oracle cost as stated. It does not claim polynomial computation time or identify a sharp optimal lower-bound constant.

## Classical upper bound cross-check

For completeness, I checked the logical direction needed to compare with the lower bound. Farness from P implies farness from 3-colorability because `C3⊆P`. In the list-coloring lemma, the repair inequality bounds monochromatic edges by `n|U|+sum delta(v)`; counting an edge twice is harmless. It forces an epsilon fraction of empty-list or high-delta vertices. Coloring a high-delta vertex with *any* permitted color decreases total list size by at least `epsilon n/2`. The tree has fewer than `3^h` addresses, and each address's next independent block misses with conditional probability at most `1/(12·3^h)`. A union bound over addresses requires no independence between nodes.

For large n, two disjoint sampled non-3-colorable witnesses survive deletion of any single vertex. Cross-block collisions are bounded by `r²/n`, even with repetitions within each block. For small n, `M≥N log(3N)` samples collect every vertex with probability at least two thirds. Both cases use the same size-oblivious algorithm. Repeated samples do not create duplicated graph vertices. Thus the polynomial classical cost is sufficient for the exact total-complexity comparison.

## Independent exact finite adversarial controls

`oracle_checker.py` is an independently authored, standard-library-only checker. It imports neither the prior audit's checker nor candidate code. It uses exact integers and rational probabilities, with explicit exceptions that remain active under Python optimization.

The test host has six tail vertices, two designated edge-disjoint triangles `(0,1,2)` and `(0,3,4)` sharing one vertex, and one isolated vertex. There are 720 permutations and 16 pattern assignments per world, so **11,520 exact latent configurations per distribution**. The shared vertex matters: it tests overlapping triangle vertex sets, not merely independent disjoint components.

| Distinct exposed tail names | Exact induced-graph TV | Exact probability of a designated triangle | Union bound |
|---:|---:|---:|---:|
| 0, 1, 2 | 0 | 0 | 0 |
| 3 | 1/10 | 1/10 | 1/10 |
| 4 | 3/10 | 2/5 | 2/5 |
| 5 | 13/24 | 5/6 | 1 |
| 6 | 3/4 | 1 | 2 |

The checker also performs Bellman optimization over **every deterministic adaptive adjacency-query tree through four calls**, allowing every one of the 15 named vertex pairs at each node. Randomized policies cannot improve the optimum because they mix deterministic trees. The value is the maximal total variation obtained by the tree, calculated as half the sum of absolute signed leaf masses.

| Worst-case adjacency calls | Optimal adaptive TV | Optimal nonadaptive TV |
|---:|---:|---:|
| 0, 1, 2 | 0 | 0 |
| 3 | 1/10 | 1/10 |
| 4 | **19/120** | **1/10** |

The computation visits 30,505 Bellman states and 25,931 marginal states. Its explicit optimal four-query decision tree is included in `oracle_checker_results.json`. The strict adaptive improvement is a meaningful adversarial control: this computation would expose an argument that silently replaced adaptive queries with a fixed query set.

Additional checks:

- Every proper subset of the three parity coordinates has TV zero, while the full triple has TV one.
- **2,064 exact conditional checks** verify that each unused name has a uniform unused host image, conditioning on exact exposed images and their observed induced graph. These include histories after a full triangle is already exposed, so the permutation-independence control is stronger than the pre-failure assertion used in the proof.
- A transcript-dependent early stopping rule has TV `1/20`, below the three-name exposure bound `1/10`.
- Exact repeated-label occupancy calculations with apex probability `1/2` check 1, 2, 3, 4, 6 and 10 sample calls. For example, three calls give TV `1/144`; four give `13/576`. The transcript includes the actual sampled names and repetitions. These values average the exact induced TV over the graph-independent distinct-tail occupancy distribution.
- A negative control gives the tester the secret host mapping. Three adjacency queries on a known designated triangle then have TV **one**. Therefore hiding only pattern bits while revealing the entire mapping would invalidate the lower bound; the actual model does not make that gift.
- Exact parameter inequalities are verified for every d from 4 through 128, including the floor, positivity, denominator bound and both cost inequalities.

Normal and optimized executions produce identical byte-for-byte output; the result is not dependent on optimization-removable assertions. These finite controls are supplementary evidence. The uniform-label induction and coupling above establish the infinite-family lower bound.

## Findings, proposed repair, and remaining gap

No mathematical repair is required in Sections 6–8. The strongest potential objections—posterior bias from negative edges, dependence caused by shared triangle vertices, conditioning BAD on farness, adaptively chosen unused names, repeated samples, changing sample/query splits, and the meaning of sample complexity—are addressed by checkable arguments above.

One exposition improvement would be to spell out the unconditional continuation-and-padding argument and explicitly distinguish it from conditioning on nonfailure. The manuscript already supplies the correct conditional-uniformity mechanism, so this is clarification, not a missing lemma. Its hypothesis that secret host identities are not supplied should remain explicit.

No unsupported equivalent problem was substituted for the central oracle claim. No unresolved mathematical gap remains in this focused audit. Priority and comprehensive literature novelty remain outside its scope. I took no Git, tracker, PR, Zenodo or external-person communication actions.

## Reproducible artifact receipt

Run `python3 oracle_checker.py` from this review directory. `python3 -O oracle_checker.py` gives the same result. The full per-artifact receipt is `ARTIFACT_MANIFEST.json`.

| Authored artifact | SHA-256 |
|---|---|
| `oracle_checker.py` | `d2415bcfbd1e9ed48861f7d3feb54b98252e4b4a98eec4f2a1202e305d17f88e` |
| `oracle_checker_results.json` | `f90fb8768bdf3b2e0e33180559b731e251c86af509833cd0ef0bfd3a56a67ee4` |
| `checker_stdout.json` | `f90fb8768bdf3b2e0e33180559b731e251c86af509833cd0ef0bfd3a56a67ee4` |
| `checker_optimized_stdout.json` | `f90fb8768bdf3b2e0e33180559b731e251c86af509833cd0ef0bfd3a56a67ee4` |
