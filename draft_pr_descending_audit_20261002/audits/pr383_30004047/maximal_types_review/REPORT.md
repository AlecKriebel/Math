# PR383 maximal-type and small-support audit

**Verdict: PASS for the explicitly restricted Turn 3-4 theorems and checked deletion stability. No mandatory mathematical repair identified. The original target remains unsolved, 5/5 substantive turns.** This audit does not authorize merge or certify historical novelty.

Frozen head: `967e8e489aa4599f712d5ddcde62e591827f7e38`. All 49 snapshot paths (48 target files and QUEUE) match their recorded lengths and SHA256 values and the exact-head Git blobs; SNAPSHOT_CHECKS.json contains every binding. All writes are confined to this maximal_types_review directory. Git, index, queue, PR and service state were not mutated. There was no outside individual communication.

## Source and verified mathematical scope

The primary question in [OWR 2019/1](https://ems.press/content/serial-article-files/46780), printed pp. 46-47 (physical pp. 42-43), is the mono-constrained universal distinct-endpoint question. The [journal paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v29i2p47), EJC 29(2), 2022, P2.47, DOI 10.37236/8451, defines the tripartition on printed p. 4 and states Conjecture 5.1 on printed p. 21: all real x,y in (0,1], all k>=1, strict x+ky>1 and weak kx+y>=1. The separate psi theorem requires reverse degrees. SOURCE_RECONSTRUCTION.md was saved before candidate proofs or previous verdicts were read; primary pages were rendered and visually inspected.

Strongest verified claim in the assigned family: for every k>=2, strict x,y>1/(k+1), uniform A with n<=5k, and arbitrary positive probability weights on B and C, some C vertex reaches at least n/k distinct A vertices. This is proved by the universal written argument, not inferred from finite samples. In an ordinary diagonal half-reach counterexample x>1/3, A would need at least eleven vertices. Eleven is a lower bound on possible counterexample size, never an upper bound or a support reduction.

Turn 3 validly deduces r=floor((n-1)/k) from below-target uniform reach. Its t counts occurring r-types, not arbitrary inclusion-maximal types. Each r-type owns a disjoint exact-reach C class of weight at least y. The k-class contradiction yields t<=k-1, and nonnegative dual charges yield

    x <= r(r-1)/(rn-|U|) <= (r-1)/(n-t) <= (r-1)/(n-k+1), r>=2.

Denominators are positive; r=0,1 are correctly handled separately. The isolated nine-vertex charge relaxation has no C completion above y=2/7 and is not a tripartite counterexample.

At n=4k+1, Turn 4 forces t=k-1. The residual available C mass is <2y, giving pairwise residual A-union size <=4. Residual triples therefore have a common pair or lie in a four-set. Every charge is feasible for all occurring type sizes, including contained types, pairs and singletons. The exceptional disjoint U,D,w case is complete: any pair containing w must use the common triple intersection; its singleton/empty alternatives justify the revised charges.

The checked deletion theorem assumes an actual exceptional B deletion producing disjoint inclusion-maximal neighborhoods. It renormalizes x to (x-epsilon)/(1-epsilon), preserves y, and correctly uses positive denominators ky and k+y-1. The strict bound epsilon<(x+ky-1)/(ky) and weak bound epsilon<=(kx+y-1)/(k+y-1) preserve signs and endpoints. On kx+y=1, only epsilon=0 is allowed. No universal small-deletion claim is established.

Full reasoning and prerequisites are in PROOF_AUDIT.md. No unsupported universal maximal-neighborhood normalization or type aggregation was found in the candidate's stated proofs. A separate weighted control shows why uniform A is essential: three types of weight 1/10 each can be reached below half in a five-type weighted part, violating the uniform rank bound of two. This refutes a forbidden extrapolation step, not the original conjecture.

## Independent controls and exact replay

All independent code uses standard-library exact rational/integer calculations and no author imports.

- `actual_graph_controls.py`: exhausts all labelled actual two-layer graphs with positive forward minimum degrees in 49 explicit finite boxes, including all A<=5,B<=3,C<=3 boxes and four additional boxes. It checks 15,001,469 graphs and 27,718,085 triggered graph/k instances. Strict-threshold reach checks pass. It finds 1,656 equality-threshold failure instances, first the three disjoint paths at x=y=1/3,k=2, confirming strictness. The listed boxes have zero below-reach cases with strict y, so those necessary-bound assertions are explicitly vacuous there.
- `rank_witness_controls.py`: supplies nonvacuous actual ordinary below-reach witnesses by integer blow-ups for k=2,...,15, n=4k+1. These have y>1/(k+1) but x below the strict threshold; they check the t=k-1 necessary-type structure and 350 residual pair comparisons. It also reconstructs 49 equal-threshold disjoint-path controls. These are not original-conjecture counterexamples.
- `triple_clique_controls.py`: enumerates all 161 maximal cliques in the compatibility graph of 80 eligible residual triples, deduplicates all 4,382 compatible subfamilies, and checks 162,642 exact permitted-neighborhood charge bounds. It includes 25 exceptional disjoint-four-set cases. This does not reduce arbitrary graphs to nine vertices.
- `deletion_boundary_controls.py`: checks 438 exact assertions on adjacent/extreme rational parameters, five zero-deletion weak boundaries, five negative-gap controls, five strict-bound equality rejections, and actual deletion degree renormalization.

After reading the relevant author code, `replay_author.py` copied checkers 3,4,5 into private_B_replay and ran each with bytecode disabled. All full stdout bytes match the respective frozen TURN_3/4/5_CHECKS.json files, all stderr streams are empty, and all exits are zero. These replay 12,569,530 author assertions. AUTHOR_REPLAY.json records checker and stream hashes; the complete streams are retained.

The old frozen review and its checker were read only after the independent mechanism and new clique/deletion controls. PRIOR_REVIEW_COMPARISON.md records agreement without treating the prior PASS as evidence by itself.

## Remaining gap and disposition

Arbitrarily large overlapping higher-rank first-incidence families remain unhandled, as does the full asymmetric wedge outside the proved structural classes. Finite box enumeration, weighted support counts and |A|<=5k cannot be extrapolated to the arbitrary-graph source statement. Original disposition must stay **unsolved, 5/5**. No sixth proof-search turn, original counterexample, historical novelty certification, immutable release or merge authorization is supplied.

AUDIT_MANIFEST.json binds the final report, research log, independent code, outputs, private replay, primary-source artifacts, and frozen snapshot manifest hash. Verification code checks all bindings without modifying the snapshot.
