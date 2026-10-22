# Independent full mathematical audit of PR #1097

Verdict: **PASS for the complete stated mathematical result, with zero actionable P0–P3 findings.** This is a mathematical verdict only. Priority, present-day openness and preprint publication readiness remain for later audits. This review is AI-assisted and unrefereed.

The audited head is `ad7b0eeef847da65afe1b691705cfa6e832e8201`, for problem 3000016 / AMR-029-0016. All eight submitted files match their actual Git blobs and submitted SHA-256 and byte pins. The report reviewed is the 9,455-byte `MATHEMATICAL_REPORT.md`, SHA-256 `46f0c5c582e5775cd05628fa6dc67ede0a2f550248b84403a51bf621cbc5844c`. No candidate file, shared branch, shared index, queue state, service, publication record or GitHub disposition was changed.

## Independence and evidence

I read the mathematical report first, authenticated all eight actual Git blobs, and froze `INDEPENDENT_DERIVATION_FROZEN.md` before reading the inherited audit, source review, acceptance or status. Its SHA-256 is `41c0b15ad49272ba1642319517fb001572543027050c590dd91d12af2cfa2e0a`. It identifies exact conventions, the gate proof, relay/signed interfaces, complexity bounds and an independently reconstructed coNP certificate. I then read every submitted file in full. I had no sibling contact and did not read sibling review reports.

The fresh checker's principal additional mechanism is exhaustive verification of the reduced-count nonreachability certificate against exact state-graph reachability. It enumerates every partial certificate count in its stated small grid, rather than assuming a prescribed firing schedule. Separate finite exploration checks legal source states, gate-prefix count states, all cleanup order transitions, unrestricted target state graphs, and exact signed threshold conjugacy. All pass/fail checks are explicit exceptions and remain active under `-O`; ordinary and optimized complete result JSON files agree exactly.

There is no original executable among the eight submitted files. The inherited aggregate checks were read as historical reports; no omitted historical checker or output was recovered or replayed. All executable work here is new.

## Exact claim and target

The accepted language consists of ordinary legal reachability on finite nonempty loopless strongly connected directed multigraphs, with an explicit binary-encoded adjacency matrix and nonnegative binary initial and target configurations. The number of vertices varies. A firing is one vertex at a time and requires chips at least equal to the full outgoing degree. Parallel arcs contribute their multiplicity to the threshold and transfers. A zero-length game is permitted; the constructed valid hard instances nevertheless have distinct initial and target configurations.

The reduction proves coNP-hardness under polynomial-time many-one reductions, and the correctly matched prior membership theorem gives coNP-completeness of this language. It is unconditional: no assumption such as P != NP is needed to state a completeness classification. This does not prove hardness for simple graphs, unary edge lists, bounded degree, bounded chip totals, or any of those restrictions combined. It also does not silently extend the cited nonnegative membership theorem to the broader signed-input language.

The immutable imported target asks whether chip-firing reachability is coNP-hard for general digraphs, without a simple-graph qualification. A fresh web-tool cached result for the primary Egres survey explicitly distinguishes simple and multigraph cases and allows signed configurations. The nonnegative multigraph subclass therefore suffices for its general hardness question. Direct fresh retrieval of the exact Egres problem page and survey failed through TLS timeouts; modern alternate Egres paths returned 404. I do not present these as successful live-body reads. `IMPORTED_TARGET_RECORD.json` preserves the read-only existing imported record, and `SOURCE_READ_RECEIPTS.json` distinguishes this from the cached primary survey. The identical general directed problem is also stated in the newly retrieved HKT v4, PDF page 12, Problem 19; its convention on page 2 permits parallel arcs. No present-day open label or priority conclusion follows from any of those historical questions.

## Primary theorem interfaces

I independently retrieved these exact primary preprint bodies:

- Farrell–Levine, arXiv `1502.04690v3`, 218,260 bytes, SHA-256 `efe2b90f98723c10490785e14797ffd9f99dacecc2ac2500a31ed7a6e3f24cb1`.
- Hujter–Kiss–Tóthmérész, arXiv `1507.03209v4`, 211,424 bytes, SHA-256 `6d616809e67cb5b6d68ab1aeb8484c9b29faf1121a7590e7a0c3872f15a2b5b9`.
- Tóthmérész, arXiv `2102.11970v2`, 178,531 bytes, SHA-256 `10d3762f41b1dfdf38c99ad295e52075cd18d7363de7b1ac763ebbf74d01d804`.

These fresh bytes agree with the submitted historical metadata. I read the complete relevant definitions and proof interfaces, including FL pages 2–4 and 10–13, HKT pages 2–6, the complete Theorem 12 on pages 8–9, its period-removal/reduced-count lemmas on page 4, and the original problem on page 12. Tóthmérész's definitions and complete Theorem 2.3/Claims 2.4 and Proposition 2.8 chain on pages 2–7 were read. Fourteen critical PDF pages were rendered and actually visually inspected: FL 2, 10, 11, 12, 13; HKT 2, 3, 4, 8, 9; Tóthmérész 4, 5, 6, 7. The additional HKT problem page 12 was read as extracted text. The visual receipt records which pages were actually viewed.

FL defines its source halting decision for nonnegative configurations on strongly connected adjacency-matrix multigraphs and allows loops. Its Corollary 3.2 is NP-completeness; the immediately preceding proof gives an explicit Karp reduction from nonnegative lattice rank, using a polynomial total-Laplacian construction with strongly connected output. This is a credited source hardness theorem, not a claim that the current report proves its underlying NP-hardness afresh. The lattice representative `sigma_max - sigma` in that chain can be signed. The candidate's exact threshold-preserving normalization supplies the necessary bridge; its validity is established below, so hardness does not rely on an unproved sign property of that representative.

HKT's preprint v4 definitions match the target exactly: loopless directed multigraphs, logarithmic adjacency multiplicities, nonnegative configurations, and ordinary legal firing. Its Theorem 12 establishes coNP membership, not merely a promise about recurrent targets or Eulerian graphs. Its Theorem 1 provides the termination dichotomy; Lemmas 4 and 5 provide period removal and a reduced legal firing count. Restricting this language to strongly connected inputs preserves membership because validity is polynomial-time testable.

Tóthmérész v2 Theorem 2.3 is a distinct earlier barrier: a polynomial reachability algorithm would put recurrence in P, give a coNP certificate scheme for halting, imply NP = coNP, and collapse PH to NP. Its proof does not supply the gate/marker Karp map audited here. The current reduction must be checked on its own, as done below.

The published bibliographic citations were corroborated by primary publisher metadata for FL and arXiv's journal/DOI metadata for HKT and Tóthmérész. Publisher full-body retrieval was not successful here. None of the preprint bodies is asserted byte-identical to its version of record, and theorem numbering is tied explicitly to the inspected preprint versions. The HKT question is Problem 19 in v4; an older indexed account has different numbering, so no cross-version numbering identity is assumed.

## Source preprocessing and totality

For an original signed configuration x, adding `k_v=max(0,-x_v)` chips and the same number of self-loops at v changes its current count and firing threshold by the same constant k_v. Its net firing update does not change because a loop's outgoing loss and incoming return cancel. Induction over every word gives the identical legal-word language, including every later configuration, stability and infinite play. This is a threshold argument: net-Laplacian equality alone is insufficient. The normalized initial vector is nonnegative and the added loop multiplicities have polynomial bit length.

For loop removal, replace all ell_v > 0 loops at v by ell_v arcs each way to a fresh empty relay. The original vertex's threshold stays unchanged. An original legal word lifts by firing that relay immediately after its parent. Conversely, in any expanded legal word, if old and relay counts are t_v and s_v, the relay holds `ell_v(t_v-s_v)`, so `s_v<=t_v`. The projected original state has at v exactly this nonnegative pending-loop amount more than the expanded old state. Every projected old firing is legal, without fairness or immediate-return assumptions. Infinite expanded play has infinitely many old firings because each relay count is bounded by its parent's. Thus existence of infinite play is equivalent in both directions; the abelian halting dichotomy supplies the halting equivalence. Strong connectivity survives, at most one new vertex is used per original vertex, and binary rather than unary packets are written.

A one-vertex source with ell loops has an unchanged state and is nonhalting iff its chip count is at least ell. This includes ell=0: even zero chips then permit the zero-cost unchanged firing forever. It can be classified by a binary comparison and replaced with the directed two-cycle at (1,0) for nonhalting or (0,0) for halting. The reduction can therefore assume n>=2 and every outgoing degree positive. The loop relay construction also independently handles a positive-loop one-vertex graph.

To make the Karp map total on strings, one can define valid-instance NONHALTING with malformed encodings rejected. Parse dimension and signs and test strong connectivity in polynomial time; send rejected inputs to the fixed NO reachability instance consisting of a two-cycle, X=(0,0), Y=(1,0). Its mass mismatch makes it unreachable. If instead using the literal complement of a HALTING language whose malformed strings are rejected, those malformed strings are YES source strings and should be mapped to a fixed YES reachability instance. `DERIVATION_ADDENDUM.md` records both conventions and why valid-instance NONHALTING is coNP-hard. This is a routine total extension of the valid-instance map, not an unresolved promise restriction. The frozen pre-source derivation's provisional malformed-string sentence is clarified in that preserved addendum rather than silently edited.

## Finite cutoff and polynomial output

Let C be the source total, n its vertex count and D its maximum outgoing degree. Every source-legal configuration is nonnegative with total C, so there are at most `(C+1)^n=N` possible states. A legal word with N firings visits N+1 states. A repeated state yields a nonempty legal closed word that can be repeated indefinitely. Conversely a nonhalting game has a length-N prefix. The halting dichotomy equates this existence statement with the complement of stabilizability. No period-vector size or polynomial number of simulated moves is assumed.

At C=0, N=1. With n>=2 and positive outgoing degrees, no source firing is legal; the gate never unlocks. This is a valid NO case. Binary chip counts and edge multiplicities can be arbitrarily large.

The numerical N can be exponential; its bit length is at most `1+n*bit_length(C+1)`. Set `M=N+1` and `B=N(MD+1)`. Their bit lengths, each scaled adjacency entry and each target coordinate are polynomial in the explicit binary source length. For C=0 the bit-length statement includes an additive constant rather than treating log 1=0 as a zero-size integer. Repeated squaring or ordinary integer exponentiation constructs the output with polynomially many polynomial-bit arithmetic operations. Relay preprocessing and n+2 gate construction use polynomial matrix dimension. No arc multiplicity is expanded into a list, no reachability oracle is invoked, and neither a length-N word nor a cleanup trajectory is produced by the reduction algorithm.

## Universal gate/marker proof

Each old vertex has outgoing threshold `M d_v+1`. The gate has threshold `nB+1`, the marker has threshold 1. Old arcs are scaled by M; each old vertex sends one chip to the gate; the gate sends B to every old vertex and one to the marker; the marker sends one to the gate. There are no loops. The gate has direct routes to and from every old vertex and a reciprocal connection with the marker, proving strong connectivity independently of the original strong-connectivity assumption.

The initial vector is `X_v=M x_v+N`, `X_g=nB+1-N`, `X_m=0`. All coordinates are nonnegative; in particular B>=N and n>=2 imply the gate is positive. The prescribed firing vector has each old coordinate N, gate coordinate 1 and marker coordinate 0.

Before the first gate firing the marker cannot fire. At a pre-gate old firing count t, with source-projected state z and individual old counts t_v, direct comparison of updates gives

`H_v=M z_v+N-t_v`, `H_g=nB+1-N+t`, `H_m=0`.

For t<N, every t_v<=N-1. If a source vertex is legal, its target old count is at least `M d_v+1`. If source-illegal, its count is at most `M(d_v-1)+N=M d_v-1`, below the target threshold. Hence legality agrees at every one of the first N projected moves, for every possible order. The gate is illegal until exactly N old firings have occurred; at that point it reaches its threshold. The proof uses no simultaneous firing, scheduler fairness or uniqueness of final counts.

For a nonhalting source, lift any length-N legal source prefix, then fire the gate. Before it fires, every old vertex has `M z_v+N-t_v>=0`; after receiving B it has at least B. Complete each old count to N, in any order. It requires at most N firings at cost `M d_v+1` each, and `B=N(MD+1)` covers this even if all future incoming old transfers are discarded. Gate and marker need not be fired again even when legal; ordinary reachability permits stopping at the chosen target.

The result is exactly

`Y_v=M x_v+MN(i_v-d_v)+B`, `Y_g=(n-1)N`, `Y_m=1`.

Here `i_v` is incoming degree, so the sign and Laplacian orientation agree with the candidate. `Y_v>=B-MND=N`, proving nonnegativity even with extreme degree imbalance. The total is `MC+(n-1)N+nB+1` for both X and Y. The marker ensures X != Y.

For the converse, take any legal word reaching Y, without constraining its count vector k. Marker balance gives `k_g-k_m=1`, hence at least one gate firing. Before that first gate firing, the marker is still zero and cannot have fired. The gate needs at least N prior old firings to reach `nB+1`. The first N of those old firings project legally to the source, by the exact simulation argument. The finite cutoff therefore proves source nonhalting. Delaying the first gate, extra later gate/marker firings, alternate odometers and added kernel periods cannot evade this implication.

Thus `(G,x)` is NONHALTING iff `(H,X,Y)` is REACHABLE, with a polynomial-time total many-one map on the stated encoding.

## Independent reconstruction of membership

For the strongly connected loopless n>=2 case, let p be the positive primitive integer kernel period. Integer image membership for `y-x` is decidable in polynomial time by integer linear algebra. If no integer solution exists, nonreachability is immediately verified by that polynomial decision. Otherwise compute an integer solution h and set

`g=h-min_v floor(h_v/p_v)*p`.

Then g is nonnegative, satisfies `y=x+Lg`, and has a coordinate below the corresponding p coordinate. It is the unique reduced nonnegative solution. Cofactor/matrix-tree bounds and polynomial integer linear algebra bound the bit lengths of p, h and g polynomially, even when their numerical values are exponential.

The period-removal argument can be checked directly. Delete the first p_v occurrences of each vertex from a legal word. At a retained firing of v, all p_v deletions there have happened, while at each other u the deleted count r_u<=p_u. Consequently `(Lr)_v<=0` because Lp=0. The retained execution has at least as many chips at that firing coordinate, and is legal. Removing full periods repeatedly proves that any reachable target has a legal realization with count g. This confirms the exact source interface required by HKT Lemmas 4–5 rather than assuming that linear equivalence implies legal reachability.

A succinct nonreachability certificate is a vector u with `0<=u<=g`, `u!=g`, such that for every v with `u_v<g_v`, the computed coordinate `(x+Lu)_v<d_v`. The vector u need not be legal-realizable. In a hypothetical legal word with count g, consider its first move exceeding u. Its own preceding count at that v equals u_v and every other count is at most u. Nonnegative incoming entries make its available chips at most `(x+Lu)_v`, a contradiction. Conversely, a maximal g-bounded legal word supplies such a certificate whenever the target is unreachable. Verification checks polynomial-bit counts and matrix products, not the exponentially long bounded trajectory. The one-vertex loopless target case is directly decided by x=y. This is the complete membership interface for the accepted restricted language.

## Fresh exact supporting checks

`check_exact.py` is standard-library-only and uses no assert statements for verification. Reproduce with ordinary `python3 -B check_exact.py result.json` and optimized `python3 -O -B check_exact.py result_optimized.json`; the two full output objects agree exactly. It is a finite control program, not a universal proof or a full input parser implementing the reduction as a service.

The actual coverage is:

- 153 source constructions: 81 two-vertex cases with both non-loop arc multiplicities 1–3 and each initial coordinate 0–2; 72 cases on all 18 strongly connected loopless simple three-vertex graphs with zero or one initial chip.
- The reachable source state graphs are completely explored and tested for stable states and cycles. Their dichotomy agrees. Cutoff/simulation explores 911 pre-gate count states and 912 transitions, checking both directions of every candidate old firing legality. There are 39 nonhalting source cases. For one selected valid length-N prefix in each positive case, all remaining cleanup-count order transitions are checked, totaling 8,331 legal transitions.
- Twelve complete unrestricted target state graphs for two-vertex arc multiplicities 1–2 and source configurations (0,0), (1,0), (0,1). Every full exploration terminates without the state cap; Y occurs exactly in the two nonhalting cases, with 820 target states in each positive graph. This test constrains neither gate nor marker nor the designated old count vector.
- An actual legal target-return cycle on the symmetric one-chip source output has period counts `(24,24,1,1)`. Following the designated path `(4,4,1,0)` by that cycle reaches the same target with `(28,28,2,1)`. The stored legal word exercises extra gate and marker firings and explicitly demonstrates why reverse reachability cannot assume a designated odometer.
- 256 signed two-vertex configurations across existing loop multiplicities 0–1, non-loop arc multiplicities 1–2 and initial coordinates -1 through 2. Entire reachable state graphs and all 278 legal transition edges are conjugate under signed normalization; relay nonhalting classifications agree, with 637 expanded states in aggregate. Twenty one-vertex comparisons include ell=0; 18 additional signed one-vertex positive-loop relay controls also agree.
- 1,456 two-vertex source/target pairs with arc multiplicities 1–4 and total chips 0–5. Exact extended-gcd integer solving and period reduction identify 254 nonimage pairs. For the remaining pairs, every candidate partial certificate is checked, totaling 4,344 count vectors; 220 certificates are found. Existence of a certificate agrees exactly with nonreachability from complete state exploration.
- Seven invalid controls expose concrete false conclusions: omit certificate properness; omit reducedness; replace strict obstruction `<d_v` with `<=d_v`; set M=1; lower the gate deficit by one; delete loops naively; add normalization chips without the compensating threshold loops. The final normalization control uses an actual legal one-firing prefix, not an algebraic word assumed legal.
- Five large-binary arithmetic controls with parameters of 1, 8, 64, 512 and 4,096 bits. The largest output integer in the final case has 20,482 bits; formulas, nonnegativity, conservation, graph class and explicit linear test bounds pass. This supplements the general polynomial-bit proof and does not simulate exponentially many firings.

No check hit the exploration cap. Ordinary and optimized results are byte-identical because there are no time-dependent result fields. The invalid variants are genuine controls that fail the intended theorem interface; they are not present in the candidate. These checks are materially independent additional evidence and do not authenticate the old edition's omitted computations.

## Limitations, custody and disposition recommendation

There are no remaining mathematical proof gaps or actionable P0–P3 findings in the claimed result. The exact live Egres page and publisher bodies were not successfully retrieved, but the inspected primary preprints, cached primary survey, full immutable imported target and explicit source proofs establish the mathematical model and target interface. These access limits are recorded rather than erased or turned into claims about priority or publisher/preprint identity. Later priority review remains essential before any novelty or publication framing.

ENOSPC occurred during a later check-result/receipt rewrite after successful initial checks. Only this review's newly generated source-page PNG cache was removed, after all 14 pages had been actually viewed. The attempted first cleanup receipt write also failed; hashes were subsequently reconstructed one page at a time from the identical PDF and render command, and this distinction is recorded. Primary PDFs, submitted blobs and all authored derivations were preserved. Small result files were regenerated successfully in ordinary and optimized modes; final pins bind the successful current bytes. No active sibling input or other research output was removed.

Recommend accepting the mathematics at this exact head and moving to the separate extensive priority audit. A later preprint should keep precise binary-multigraph/nonnegative scope; credit FL source hardness, HKT membership and period removal, and Tóthmérész's earlier barrier; distinguish fresh controls from historical omitted computations; retain AI/unrefereed disclosures; and avoid claiming present-day openness or priority based on these checks. No publication, merge or closure recommendation is made before those later gates.
