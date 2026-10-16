# Adversarial review of PR #1097: gate reduction

Review date: 2026-10-14 UTC. Reviewer family: gate and firing-order falsification. Exact PR head: ad7b0eeef847da65afe1b691705cfa6e832e8201. Problem 3000016 / AMR-029-0016.

## Verdict and limits

**PASS for the complete mathematical claim as expressly stated. No actionable P0–P3 defect was found in the eight submitted files.** The proof gives a deterministic polynomial-time many-one reduction from NONHALTING to legal REACHABILITY on finite loopless strongly connected directed multigraphs with binary adjacency entries and nonnegative binary initial/target configurations. Credited prior coNP membership makes that exact language coNP-complete.

The source theorem contracts were independently authenticated from full primary PDF bodies. There is one source-access limitation, not a discovered mathematical defect: today's standalone Egres problem page could not be retrieved. The primary Egres survey was read through its full indexed text and supports the multigraph hardness branch; I have not certified the standalone page's exact full wording. The parent must preserve this limit until its own original-target reconciliation. No novelty, present-day openness, first-in-literature, simple-graph, unary, bounded-degree, or signed-language membership conclusion is certified. A later dedicated priority audit remains necessary.

The review is AI assisted and unrefereed. It is neither external human peer review nor formal proof-assistant certification.

## Independence and custody

All eight original submitted files were compared byte-for-byte against git show at the exact head and their actual Git blob IDs were independently obtained. INPUT_PINS.json records sizes and SHA-256 hashes; the submitted manifest agrees. The full MATHEMATICAL_REPORT was read first. INDEPENDENT_DERIVATION_BEFORE_LABELS.md was frozen at 05:17:18 UTC with hash b2a7c2553e43a3f6244aac7af9abf1d4597fe4fb9b0905e8c0b3c039db8f5fac before reading MATHEMATICAL_AUDIT, ACCEPTANCE, STATUS, or any sibling report. Source bibliographic metadata and the manifest were used only for retrieval/custody. Inherited accepted labels in the report were ignored as evidence. After the new derivation and fresh tests, I read the entire inherited audit, source review, README and status/acceptance declarations to test consistency. No sibling family report was consulted.

No candidate byte was changed. No Git/index/branch/service operation, publication or outreach occurred. The original eight-file edition contains no executable; all computations here are newly authored tests, not replay of omitted historical code. Historical aggregate counts in the original audit were not independently rerun and are not substituted for today's results.

## Exact claim and mechanism

The source is a conserved nonnegative loopless strongly connected system with n>=2, positive degrees, adjacency a_uv, maximum degree D and total chips C. Set

N=(C+1)^n, M=N+1, B=N(MD+1).

The number N can be exponential in numeric value; only its binary bit length and construction time must be polynomial. Every source state lies in {0,...,C}^n. A length-N legal word visits N+1 states and repeats a state. The nonempty intervening word can be repeated indefinitely; the abelian dichotomy excludes a terminating alternative. Conversely, a nonhalting game has such a prefix. The cutoff needs no period-vector bound, fairness assumption or guessed firing vector.

In H, old arc multiplicities are multiplied by M. Each old vertex sends one chip to g; g sends B to each old vertex and one to m; m returns one to g. The resulting degrees are Md_v+1, nB+1 and 1. The gate directly reaches and is reached from every old vertex, and the gate-marker cycle includes m, so H is strongly connected and loopless. All multiplicities are binary integers; no arc list is expanded.

The initial old coordinate is Mx_v+N; the gate is nB+1-N and the marker is zero. For t old firings before the first gate, individual counts t_v and projected source state z give exact identities

H_v=Mz_v+N-t_v, H_g=nB+1-N+t, H_m=0.

For t<N, t_v<=N-1. If z_v>=d_v, H_v>=Md_v+1, so its firing is legal. If z_v<=d_v-1, H_v<=M(d_v-1)+N=Md_v-1, so it is illegal. This is an inductive, all-orders equivalence for precisely the first N old moves. The first gate is unavailable before N old moves and becomes legal at N; the empty marker cannot contribute anything before that gate. The integer margins include the C=0/N=1 case and the Nth move: the condition is checked just before the move, at total t=N-1.

## Forward implication and every cleanup order

From a legal N-move source prefix, fire g once. Immediately before g, source nonnegativity and t_v<=N make every old H coordinate nonnegative. Each receives B. Finish old counts to N, requesting exactly N-t_v additional moves per vertex, and fire neither g nor m again.

Each vertex can pay for its entire remaining block using at most N(Md_v+1)<=B. Before any requested firing it has made at most N-1 of these moves, so that firing is legal even if all incoming old transfers are ignored. The same inequality covers every interleaving, including extreme block orders, vertices with zero remaining moves, unequal old degrees, and large imbalances. A legal game may stop at Y even if more moves are possible; no stabilization or recurrent-target condition is imposed.

The final odometer is f_old=N, f_g=1, f_m=0. Independently multiplying the incoming/negative-diagonal Laplacian gives

Y_v=Mx_v+MN(i_v-d_v)+B, Y_g=(n-1)N, Y_m=1.

Since i_v,x_v>=0 and d_v<=D, Y_v>=B-MND=N. The gate initial count is at least one; all other nonnegativity is explicit. X and Y have equal total MC+(n-1)N+nB+1, and differ because the marker changes from zero to one. Thus all output coordinates are valid regardless of source halting behavior.

## Reverse implication under arbitrary schedules and odometers

Let k be the actual nonnegative firing-count vector of any target-reaching legal word, without constraining it to f. The marker coordinate yields k_g-k_m=1, hence k_g>=1. Take the first gate firing. No marker has previously fired, because the marker starts empty and receives only from the gate. Therefore the gate must have received at least N old-to-g chips, one per old firing. Its preceding old subsequence has at least N moves. Their first N moves are legal on the source by the prefix induction above. The finite cutoff implies NONHALTING.

This argument survives delayed first gates, multiple gate firings, arbitrarily many marker returns, extra old cycles, alternative target-reaching counts, and additions of whole period vectors. It needs neither uniqueness of the final odometer nor equality to the prescribed vector. Simultaneous firing is never assumed. Later old firings may cease to simulate the source, which is harmless because the reverse implication uses only the first N preceding moves.

## Preprocessing and edge cases

For a loop group of multiplicity ell at v, replace it by ell arcs v-to-r and ell arcs r-to-v with a fresh empty relay. Old degree/threshold is unchanged. The relay holds ell(t_v-s_v), so its firings cannot outnumber its owner's. The original projected state exceeds the expanded old state by exactly the pending relay chips at that owner. Every projected old move is legal. Original words lift by immediate relay returns; an infinite expanded word has infinitely many old moves. This proves both nonhalting directions, and halting follows by dichotomy. Strong connectivity persists; there are at most twice as many vertices and polynomial-bit integers.

A one-vertex graph with ell loops never changes its chip count; its game is nonhalting exactly when count>=ell, including ell=0. The fixed two-cycle with (1,0) supplies YES and with (0,0) supplies NO. This constant preprocessing keeps the hard source restriction n>=2 and D>=1. The main construction never divides by a zero degree.

Adding k_v=max(0,-x_v) self-loops and k_v chips at v leaves the net update unchanged and shifts both threshold and current coordinate by k_v for every word. Thus signed intermediate source configurations become nonnegative without changing any legal word, finite stable endpoint, or nonhalting outcome. This normalization also handles existing loops; the subsequent relay removal gives the actual loopless source required by the gadget. It closes the signed intermediate issue in the Farrell–Levine lattice proof rather than silently assuming a stronger source theorem convention.

## Complexity and credited membership

For binary input size s, n<=s, bitlength(C+1) and bitlength(D) are polynomial in s, and bitlength(N)<=1+n log_2(C+1). M and B have polynomial bit length. Polynomial-bit integer powers, products, sums, and the n+2 adjacency matrix entries/coordinates can be computed in polynomial bit time. Preprocessing adds at most linearly many vertices and polynomial-bit chips/loops. No simulation of the length-N legal word is part of the reduction algorithm. Existence of an exponentially long witness does not undermine Karp reduction time.

[Farrell–Levine Corollary 3.2](https://arxiv.org/pdf/1502.04690v3) supplies credited NP-complete HALTING; its complement has the needed coNP hardness. [Hujter–Kiss–Tóthmérész Theorem 12](https://arxiv.org/pdf/1507.03209v4) supplies membership for the exact nonnegative binary loopless model. Restriction to strongly connected well-formed inputs preserves membership since that restriction is polynomial-time decidable. SOURCE_INTERFACE_DERIVATION.md adds an independent polynomial-bit check of reduced odometers using cofactors and a deleted Laplacian inverse. [Tóthmérész Theorem 2.3](https://arxiv.org/pdf/2102.11970v2) is a credited earlier hierarchy barrier, with a different recurrence/certificate interface; the comparison is not a priority clearance.

## Fresh computational falsification

check_gate_reduction.py is a self-contained fresh exact-integer program with unconditional exceptions, not assert-dependent validation. Normal Python and optimized Python both passed with identical JSON after removing the timestamp. Both deliberately invalid self-test runs exited nonzero. COMMAND_RECEIPTS.json records actual commands.

The fresh instance universe is 144 two-vertex cases (each directed multiplicity 1..3, each chip coordinate 0..3), plus 144 three-vertex cases (all 18 strongly connected loopless simple graphs, each chip coordinate 0 or 1): 288 total, 148 nonhalting and 140 halting. Source status comes from complete reachable state graphs and an independent Kahn cycle test. Every legal pre-gate odometer layer up to N is explored, checking exact state identities and legal-move equality, gate availability, and marker emptiness: 7,458 states and 9,944 old transitions. N ranges up to 64. Boundary odometers are tested with opposing block cleanup orders. All 140 halting augmented reachable state graphs are independently exhausted (218 total states), with no target and no reachable cycle.

Additional checks cover 324 relay instances (767 expanded states and 704 edges), 400 signed-offset instances (626 source states), and 20 one-vertex threshold/replacement cases. They test complete state spaces and projected legal moves, not only an intended lifted word.

For the two-cycle with source (1,1), N=9 and B=99, an unrestricted H state-space search exhausts all 12,614 reachable configurations. The fresh explicit direct witness has counts (9,9,1,0); appending a legal complete period gives another target-reaching word with counts (108,108,2,1). A separate direct target word deliberately delays the first gate until N+1 old moves. These controls demonstrate the relevance of the arbitrary-count and delayed-gate proofs.

Four further constructions use 2, 3, 5 and 8 vertices with adjacency values through 1+2^1024 and initial coordinates through 2^263+7. The largest output integer has 5,251 bits. These checks verify strong connectivity, nonnegative coordinates, conservation and conservative bit bounds without simulating a firing word or expanding arc lists.

Four deliberately invalid variants are detected: adding one initial gate chip creates a false target from the empty halting source; setting N=1 creates a false target from a source with one legal move then stabilization; setting M=N-1 permits an augmented move illegal on the source; changing the marker target breaks conservation. These are controls only and do not modify the candidate. Finite tests support falsification; the universal classification is established by the written argument, not these finite enumerations.

## Source inspection, residual access limit and final custody

The three freshly downloaded primary PDFs match the submitted recorded SHA-256/byte identities exactly. Relevant proof pages were fully extracted/read and nine complete pages were actually inspected as rendered images, as recorded in SOURCE_RETRIEVAL, SOURCE_INTERFACE_DERIVATION and SOURCE_VISUAL_INSPECTION. Copyright source bodies remain in ignored raw_private storage. After the nine page views completed, a tiny heredoc hit ENOSPC; only those own derivative PNGs were removed (3,109,548 bytes). Their hash/size receipt is retained, and the PDFs/text remain. No source image is claimed to remain locally available after that cleanup.

The original standalone Egres page access limit is explicit. Its survey distinguishes simple and multigraph rows, so the manuscript must retain its binary-multigraph qualification; a separate simple-graph hardness question is not settled. No candidate repair is currently needed. Priority, original-page reconciliation, paper preparation and whole-package reviews remain parent tasks; this mathematical review alone does not authorize publication readiness.
