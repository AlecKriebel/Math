# PR33 original-stage transport/compactness adversarial audit

**Verdict: PASS_PARTIAL within this family's scope.** The frozen finite-transport proposition, Hall-deficiency identity, infinite compactness/attainment argument and elementary bounds are correct. They establish a universal equivalence, not a positive three-dimensional avoidance bound. No mathematical correction to those portions of frozen PARTIAL.md is required. The prior four-dimensional source argument, later literature status and novelty assessment remain conditional dependencies assigned to another audit family.

## Frozen target and provenance

- PR33 head: `de5877c38bf3604f0a8e074af7a9c55fca334522`.
- Actual base equals metadata base: `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`.
- Frozen exact diff: 55,852 bytes, SHA-256 `7ef73671ccd579fbb59d73588b861a9acb5f60bb0d03b3563ccb036975039f6a`, 14 sections. All 13 numeric-attempt added bodies equal their frozen files exactly. The other section changes the queue row from queued 0/5 to unsolved 1/5 and adds a qualified reviewed-partial note.
- All 13 original numeric files, both actual programs, their results and the entire old review were read. The exact diff was read completely in contiguous blocks covering lines 1-1267 and independently checked against the originals.
- Original substantive proof budget remains **1/5**. This verification costs **0 additional attempts**. This family changed only its exclusive folder; no Git, GitHub, queue, status or shared research artifacts were mutated.

Before old code, old reviews, results, exact diff, root or sibling mathematical findings, I freshly retrieved the literal archived notes, read the SRW convention and section-12 / printed-PDF page-104 question, read PARTIAL.md only, and sealed exact claims, assumptions and falsifiers. The unmodified seal SHA-256 is `38b28b94489bcc8b420edf8b8c205bec20953dd2c5aa06f7cddb038dc43f4c33`. The archive PDF SHA-256 is `aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe`, matching the frozen original source receipt. Its time-0 interpretation and unrestricted complete-path coupling model are consistent with the source.

The initial seal conservatively noted that Q12.33 itself does not specify a norm. A later complete extract and visual check of standing page 5 independently confirmed the notes define graph distance as shortest-path length. Thus the graph-distance/l1 normalization in PARTIAL is supported. The seal is preserved rather than silently rewritten. Setup failures and this clarification are recorded in RESEARCH_LOG.md. Source: [archived Benjamini notes](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf).

## Independently reconstructed universal theorem

PROOF.md gives a full derivation for all d>=1, all starts x,y in Z^d and all N>=0, including shared starts. Finite words are labeled increment sequences, not range-equivalence classes. Every SRW word has weight 1/(2d)^N. A coupling matrix scaled by (2d)^N is doubly stochastic. A finite alternating-path proof establishes the needed Hall identity, and a support-matching subtraction proof establishes the permutation decomposition. Completing a maximum safe matching to a permutation retains both full finite path marginals and its exact safe count.

For the infinite conclusion, the finite-alphabet increment pair space is compact. The set of couplings with both entire marginal laws fixed is compact and closed. Every finite optimizer extends by independently sampled iid SRW tails. Finite full-range avoidance is clopen and decreases with N. The proof takes a weak subsequence, holds k fixed, passes the R_k mass inequality through the limit, and only then takes k to infinity. This proves

  max_pi pi{X_i!=Y_j for all i,j>=0}
    = lim_N a_N = inf_N a_N = liminf_N a_N,

and proves the maximum is attained. Projective consistency of the selected finite optimizers is unnecessary. Closedness of the infinite event also gives upper semicontinuity, ruling out a nonattainment objection. The original proof makes the correct fixed-k passage; it contains no illicit moving-event weak-limit step.

The weighted generalization is proved independently using a finite capacity network with real weights and exact max-flow/min-cut reasoning. Its optimum is

  1 - max_A [p(A)-q(N(A))].

The empty subset makes the maximum nonnegative. A maximum safe subcoupling extends to a full coupling by a residual product matrix. Unequal weights, zero weights and unequal support cardinalities are allowed. Cardinality matching is valid for the original equal-weight SRW words, and does not automatically apply to unequal-weight range groups. Conditional complete tail laws replace independent uniform tails for arbitrary fixed complete laws on finite-alphabet path spaces.

## Boundary and falsification results

| Challenge | Verified result and scope |
|---|---|
| Full versus synchronous range | At d=1, displacement 2, N=2, full optimum is 3/4 and synchronous optimum is 1. The stronger target is essential. |
| Time 0 | Shared starts have every full optimum 0, including N=0. Deleting time 0 produces a false N=0 optimum 1. |
| Complete path marginals | A nearest-neighbor three-step process has every correct one-time SRW law but assigns individual words probabilities 0, 1/8 or 1/4. Appending ordinary independent tails preserves every later one-time law, while the complete marginal law remains wrong. |
| Unequal weights | A diagonal graph with weights p=(3/4,1/4), q=(1/4,3/4) has unweighted perfect matching but weighted optimum 1/2. A single allowed edge has optimum 1/4, rather than cardinality value 1/2. |
| Finite positive masses | Fixed iid fair-bit complete laws and a decreasing prefix event have exact finite optima 2^(-N)>0 and infinite optimum 0. The same phenomenon for the SRW full-range event is proved in d=1 using a bounded gambler's-ruin argument. |
| Moving weak-limit events | Flip only bit N in an iid fair-bit coupling. Both full marginals remain iid fair, fixed-prefix laws converge to the diagonal, and the N-prefix equality event has mass 0 while its infinite event under the limit has mass 1. Weak continuity cannot be used with a varying event. |
| Distance 10 | Translation proves a_N=1 for all N<=9, every d and every signed/non-axis l1-distance-10 start. The proof is universal; enumerations below are only finite diagnostics. |
| Translation tails | A specified displacement word occurs in iid length-10 blocks with positive probability. The translation coupling has infinite full-range avoidance probability 0 although it never collides synchronously. This excludes only that coupling. |
| Elementary upper obstruction | Visiting the other initial vertex forces a range collision under every coupling. Thus alpha<=1-P_x(T_y<infty)<1 for distinct starts. The horizon-10 multinomial count is correct for all displacement types, signs and zero coordinates. This is an upper bound, not a positive lower bound. |

No attempted falsifier invalidated the original theorem. The falsifiers reject stronger interpretations and substitutions, which the original artifact already excludes.

## Actual computations and reproducibility

The original author program and old independent reviewer program were copied unchanged into an ignored private directory and executed successfully. Their result receipts were reproduced byte for byte. ORIGINAL_REPLAY.json records the original code equality and result hashes. The author result hash is `2d47b2a6c68671b3a5691308c22d6fbce8742690f616b791879a415f6a20b197`; the reviewer result hash is `e3af17200b82e16ccb317a7d0c193ea03468d8237a75066bc726c7365df901d9`.

This family's controls import neither old implementation. They keep every labeled word and solve integer-scaled rational transport by Edmonds-Karp, rather than the author's recursive matcher or the old review's grouped-range Dinic solver. certificates.json contains literal optimal permutations and Hall sets for 24 finite graphs (22 true-event controls and 2 substituted-event controls), and rational full couplings plus Hall sets for 9 weighted graphs. The independent checker decodes word labels arithmetically, rederives every allowed-edge neighborhood, checks complete finite marginals, and equates the primal certificate with its Hall upper bound. It passed 921 substantive certificate checks. The solver also performs exhaustive permutation and Hall-subset enumeration in the smallest cases.

The actual distance-ten first-hit checks cover all 66 nonnegative 3D coordinate compositions, all 286 nonnegative 4D compositions, and two signed examples: 354 counts total. They use a separate absorbing recursion in the endpoint box. Its confinement is valid because any shortest endpoint word is coordinate monotone; at total distance ten, no word with a backward step can hit by time ten. No infinite-time inference is drawn from those counts.

Representative certificates include full mass 210/216=35/36 for d=3, displacement (2,0,0), N=3; 34/36=17/18 for d=3, displacement (1,1,0), N=2; perfect finite matchings at actual distance ten in d=3 and d=4; and 1023/1024 in d=1 at displacement 10, N=10. Exact certificate bytes are retained for direct inspection.

Eight tampered in-memory copies were tested against the independent verifier and rejected: duplicate marginal labels, erased Hall deficiency, inflated optimum, synchronous substitution, deleted time zero, unweighted interpretation of weighted mass, corrupted weighted row mass and an invented uniform lower bound for the vanishing-prefix example. MUTATION_RESULTS.json preserves every rejection reason. Earlier setup/illustration failures remain in RESEARCH_LOG.md, and the earlier control receipts remain in ignored tmp/.

Run `python3 reproduce.py` from this folder to replay the three new programs in ignored private copies and verify all 13 original SHA-256 hashes, sizes and Git blob identities, plus the exact original diff. REPRODUCIBILITY.json records deterministic byte equality for certificates.json, controls_results.json and MUTATION_RESULTS.json. No package installation or network is needed for computations. References and scratch copies are ignored; the final manifest excludes itself and lists every first-party deliverable exactly.

## Exact remaining gap and disposition

For every intended fixed pair x,y in Z^3 at graph distance 10, the unresolved positive claim is precisely the existence of epsilon(x,y)>0 satisfying, **for every N and every subset A of complete length-N SRW words from x**,

  |A|-|N(A)| <= (1-epsilon(x,y)) 6^N.

Its negation requires deficiency arbitrarily close to 6^N. Neither the reduction nor these certificates prove either side. Finitely many distance-ten displacement types mean positivity for every type would imply a common positive bound over those types, but none has been established. The route remains blocked at this equivalent central estimate. Do not reopen it without materially new mechanism or evidence.

No full 3D solution, no independent certification of the cited 4D proof, no Markovian-coupling result, no novelty priority claim and no publication promotion follow from this audit. Audit completion is 100%; progress toward the remaining 3D uniform bound is 0% from this verification; original budget remains 1/5.
