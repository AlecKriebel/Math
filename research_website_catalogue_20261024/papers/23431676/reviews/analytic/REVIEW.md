# Independent analytic review — Zenodo 23431676

**Disposition: PASS for the exact stated mathematical theorem.** This is an AI analytic review of the authenticated version below, not human peer review, formal proof certification, a novelty determination, or publication approval. No substantive mathematical defect or unresolved load-bearing gap was found.

## Identity, coverage and independence

- **Work:** *CoNP-completeness of binary directed chip-firing reachability*, Alec Kriebel, version 1.0, six published PDF pages. Printed date and Zenodo publication metadata: **15 October 2026**. Record creation: **17 October 2026, 05:45:36 UTC**. These dates do not establish first deposit or priority.
- PDF SHA-256: `6ae840e0b2e1df73b204c2c293c3fbcfa39206654e775a75261515c693a6187d`.
- Public support ZIP SHA-256: `94280d71c41617198e96f1f4b4aca043ff86c3feda3109e0af9a1a18e1db651d`.
- Fresh acquisition receipt SHA-256: `c4ecaf95a88e3cf418f6587396cdb1ad05f191cbe96c6546c990e523f29cb548`; record JSON: `f345ad9f30afd61b753a56a05b714b20a41c76ab42a73fdcb46afc6c7edbfc04`.
- Read the complete current TeX and all six actual published PDF pages, including definitions, all proofs, limitations, disclosure and references. Visually inspected the displayed construction/proof/certificate on PDF pp.3–5. The embedded PDF equals the public PDF. ZIP CRC and all **198 regular extracted members** were independently checked against the archive without modifying source bytes.
- Read the mandatory programme objective. Read only raw primary-source acquisition receipts and raw primary bodies from the scope cache, not its report or conclusions. No sibling or historical assessment body was read. The manuscript's own reported historical audit counts/priority language were necessarily encountered; they were treated as author statements and were not adopted as fresh evidence.
- Before inspecting any submitted helper, independently reconstructed the universal proof and wrote/executed exact controls. `evidence/pre_helper_seal.json` binds that reconstruction, implementation and result with timestamp **2026-10-25T02:52:05.425307+00:00**. The seal was rechecked unchanged at completion.
- Afterwards read all 356 lines of current `scripts/run_checks.py` and 162 lines of `scripts/common.py`. The latter exposes provenance-file paths but their bodies were not opened or executed. `verify.py`, historical provenance, administrative status/repair records, `SOURCE_AUDIT.md`, and expected-result declarations were deliberately excluded as mathematical authority. Current mathematics is completely given in the manuscript and the standalone current check program.

## Exact strongest supported claim

For nonempty finite **loopless strongly connected directed multigraphs**, encoded by **binary adjacency entries**, with **nonnegative binary** initial and target configurations, ordinary sequential legal chip-firing reachability is **coNP-complete under deterministic polynomial-time many-one (Karp) reductions**. The vertex count is part of the input. A legal word may stop while further moves remain enabled, and the empty word is allowed. Invalid encodings are rejected. The singleton loopless case is decidable by equality.

The hardness construction uses large parallel-edge multiplicities, degrees and chip counts. It does not prove the same classification for simple graphs, unary input, bounded degrees or bounded chip totals. The membership result being applied is the nonnegative configuration model; no assertion about every signed reachability formulation is needed. Signed states appear only in a source-normalization interface that is explicitly proved.

## Universal proof reconstruction

### 1. Source problem and preprocessing

Farrell–Levine's exact source edition states NP-completeness of halting for strongly connected directed multigraphs with adjacency-matrix input. Its total-Laplacian construction is polynomial in the binary description, not the number of expanded arcs. The reduction from nonnegative lattice rank uses a possibly signed intermediate configuration `sigma_max - sigma`. The current manuscript supplies the needed explicit normalization: add `k_v=max(0,-x_v)` loops and chips at vertex v. The firing matrix is unchanged, while the threshold and current coordinate are both translated by `k_v` after every word. Hence legality, stability and infinite play are preserved. This is stronger than merely saying that the Laplacian is unchanged.

Replacing all loops at a vertex by one aggregated relay preserves the old threshold and introduces only one new vertex per original vertex. Every old word lifts by returning its packet immediately. In any expanded word, the relay count cannot exceed its parent count, and the projected original coordinate exceeds the expanded old coordinate by the pending returned packet. Therefore every projected old move is legal; infinitely many relay moves cannot occur with finitely many parent moves. The source halting equivalence follows. Strong connectivity, binary size and nonnegativity are preserved.

Singletons, including zero outgoing degree, are explicitly classified before using positive-degree assumptions. Zero-degree singleton firings are legal and change nothing, so they are nonhalting but have reachability only to the same configuration. The paper treats these two questions separately and correctly.

The language-totalization discussion is sound: validity is polynomially decidable, invalid outputs of a halting reduction can be replaced by a fixed valid NO-halting instance, and invalid source strings can be mapped to the stated fixed YES/NO reachability instance according to which complement convention is chosen. No promise-problem reduction is silently substituted for a Karp reduction.

### 2. Finite-state cutoff and exact prefix simulation

For a preprocessed source on n>=2 vertices with total C chips, conservation and nonnegativity put every reachable state in `{0,...,C}^n`. Thus `N=(C+1)^n` bounds the number of states. A legal word of length N visits N+1 states and contains a nonempty closed legal subword. Repetition gives infinite play; the halting dichotomy rules out an alternative terminating maximal game. The converse is immediate. This is a finite-state bound, not an asserted polynomial firing-time bound.

With `M=N+1`, scaling old arcs and adding one arc from each old vertex to the gate gives, before any gate firing,
`h_v=M z_v+N-t_v`, `h_g=nB+1-N+t`, and `h_m=0`.
For t<N the count t_v is at most N-1. A legal source vertex has enough chips for the enlarged threshold `M d_v+1`; an illegal one has at most `M(d_v-1)+N=M d_v-1`. Both directions hold at every prefix, regardless of firing order. The gate is unavailable until exactly N old moves have occurred; the marker is unavailable until the first gate.

### 3. Forward completion and reverse implication for arbitrary words

After N simulated moves and one gate firing, every old vertex has at least `B=N(MD+1)` chips. Completing each old firing count to N costs that vertex at most `N(Md_v+1)<=B`, even if all future incoming chips are ignored. This proves legality for **every** ordering of remaining old moves, not only a convenient schedule. The resulting count `(N,...,N,1,0)` gives exactly the displayed target by column-Laplacian multiplication.

The reverse implication does not assume this particular count vector. For any target-reaching word, marker balance is `k_g-k_m=1`, forcing a first gate firing. Before that first gate the marker cannot fire, and the gate must have received at least N old contributions. Their first N moves are therefore genuine source moves by the prefix invariant. Delayed gate firing, additional complete periods, and later gate/marker firings do not undermine the argument.

Initial and target coordinates are nonnegative: `X_g>=1` and `Y_v>=B-MND=N`. Totals agree, the marker makes X and Y distinct, and the gadget is loopless and strongly connected. The `C=0,N=1` case is included: every old vertex has positive threshold, so the gate never opens.

### 4. Binary complexity

The integers N, M and B may be exponentially large in value but have polynomial bit length: `log N=n log(C+1)`, with a constant retained at C=0. Preprocessing at most doubles the vertex count; the gadget adds two vertices. Polynomially many arithmetic operations on polynomial-bit integers construct the matrix and vectors. No length-N word or unary-expanded edge list is output. The source-to-target map is deterministic and polynomial in the intended encoding.

### 5. Credited coNP membership

For n>=2, the integer kernel of L is generated by a positive primitive period p, with polynomial-bit tree cofactors. Given an integer solution h of `Lh=y-x`, subtracting `min_v floor(h_v/p_v)` multiples of p gives the unique nonnegative reduced g. Every other nonnegative integer solution is `g+kp`, k>=0. A coordinate `g_w<p_w`, together with a nonsingular deleted minor, gives the stated polynomial bit bound on g.

The integer-image computation is a standard polynomial integer-linear-algebra step, not an integer-programming oracle. It also admits a direct reconstruction recorded in `evidence/integer_image_derivation.md`: solve rationally with one coordinate fixed to zero, use Bezout coefficients for primitive p to determine the only possible fractional shift along p, and check integrality. This explains the exact interface without depending on a newly acquired complete GLS textbook body.

Period deletion is valid: at a retained firing v, its first p_v deleted occurrences are complete, while other deletion counts are at most p_u. Hence `(Lr)_v<=0`, so the retained sequence has at least as many chips at its active coordinate. Repeated deletion reduces any successful count to g while preserving legality and endpoint.

For a certificate `0<=u<=g`, `u!=g`, with `(x+Lu)_v<d_v` whenever u_v<g_v, consider the first attempted move exceeding u in a hypothetical g-word. Its own prior count equals u_v and all other prior counts are bounded by u, so its available chips cannot exceed the obstructing coordinate. This contradicts legality. Conversely any maximal g-bounded game that fails to realize g gives such a proper u. Neither u's realizability nor nonnegativity of x+Lu is required. The certificate has polynomial binary length; no verifier must execute its potentially long game. The invalid-input, no-integer-image and singleton branches are polynomially decidable.

## Primary interfaces checked

The exact paths, URLs, SHA-256 values and reading scopes are in `evidence/source-custody.json`. These were inspections of original author/preprint bodies, not title-only citations.

1. **Farrell–Levine, arXiv v3:** definitions and nonnegative halting input; least-action/kernel/tree interfaces; complete Section 3 hardness construction, Theorem 3.1 and Corollary 3.2. The strong-connectivity, total-Laplacian and binary-size conditions match. The signed intermediate issue is handled by the manuscript's proved normalization. [Source](https://arxiv.org/abs/1502.04690v3)
2. **Hujter–Kiss–Tóthmérész, arXiv v4:** binary adjacency and nonnegative loopless definitions; halting/bounded-game and period statements; Proposition 8; full Theorem 12 certificate; Theorem 14 and its recurrence hypothesis; original Problem 19. This authenticates the historical general-digraph question without needing the unavailable Egres body. [Source](https://arxiv.org/abs/1507.03209v4)
3. **Björner–Lovász, July 1992 author manuscript:** halting/bounded-game interfaces, primitive period Proposition 4.1, full period-deletion Lemma 4.3, and reduced-uniqueness Lemma 5.2. Its loop convention includes the firing threshold, agreeing with the preprocessing issue. The paper correctly credits this machinery. [Source](https://lovasz.web.elte.hu//morepapers/abacus.pdf)
4. **Kiss–Tóthmérész, arXiv v3, full Section 4:** reserve-based finite-horizon simulation for an Eulerian source in a distance-to-nontermination/divisor-rank reduction. The current manuscript cites this as related method attribution; it does not import its Eulerian-only simulation as a theorem for arbitrary directed inputs. [Source](https://arxiv.org/pdf/1407.6958v3)
5. **Tóthmérész, arXiv v2, full chip-firing Section 2:** signed configurations, Theorem 2.3, Claim 2.4, Proposition 2.8 and their proofs. One chosen legal firing gives recurrence-to-reachability, whereas the recurrent representative in Proposition 2.8 is existential. These inspected statements do not themselves construct the target required by the present Karp reduction. This comparison is not an exhaustive antecedent search. [Source](https://arxiv.org/abs/2102.11970v2)

## Fresh controls and supplied replay

The universal arguments above determine the verdict. Computation is supplementary and finite.

- Fresh exact implementation, completed before helper inspection: 27 strongly connected two/three-vertex models; **234** source/configuration cases, **2,917** prefix states, **110** complete-prefix count states and **220** cleanup words. Whole gadget reachability was explored for four selected cases, including a positive case with **820** reachable states and halting cases with one/two states, allowing arbitrary subsequent gate/marker moves.
- Exact independent membership/certificate comparisons covered **2,898** pairs and **17,746** candidate box vectors, including **22** valid obstruction vectors whose algebraic intermediate configuration has a negative coordinate. Period deletion checked **6,130** legal words.
- Loop-relay tests covered **360** cases, with delayed-return projection checked through depth six. Signed normalization checked **626** legal prefixes. Singleton thresholds 0–3 with initial counts 0–4 were checked. Very large binary inputs constructed the output and exact target without traversing an exponential trajectory.
- Fresh deliberate faults were detected: setting M=1 admits a source-illegal move; releasing the gate one chip early enables it from the zero-chip source; an insufficient reserve breaks cleanup legality; replacing the strict obstruction inequality with a nonstrict one falsely rejects a legal one-step move.
- After helper inspection, a further independently derived exact integer-image control checked **220** seeded cases and large periods with **65, 513 and 2,049** bits. Its timing is explicitly separate from the pre-helper seal.
- Current submitted `run_checks.py` was replayed normally and under `python -O`; both succeeded with identical output. Its finite coverage reports 87 source instances, 785 prefix states, 852 transitions, 7,668 cleanup-order transitions, unrestricted target-state cases, distinct successful target count vectors, certificate, signed/loop and binary-size controls. An explicit injected failure exited nonzero under `-O`, so correctness guards remain active under optimization.
- No historical omitted executable or old aggregate result was represented as replayed. No PDF rebuild, dependency installation, source repair or public mutation was performed.

## Remaining limits and disposition

No unresolved defect remains in the stated mathematical theorem after this review. This does **not** certify exact-result/gadget/method priority, independence of discovery, current worldwide openness, journal suitability, or the manuscript's historical audit census. Egres was not available in the raw acquisition; original HKT Problem 19 is sufficient for the historical question actually used. The full GLS monograph and all recursive antecedents of established primary theorems were not re-audited; the applied interfaces and the direct integer-image reconstruction above suffice for this scope.

The proof's encoding and model restrictions should remain visible in any eventual public explanation. The complete abstract's AI/unrefereed and priority limitations should remain intact. There is no basis here to claim simple-graph hardness or an impossibility theorem for polynomial algorithms. **Analytic gate: PASS at the exact scope above.** Root retains the combined review and publication decision.
