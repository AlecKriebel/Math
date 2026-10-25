# Independent adversarial review — Zenodo 23431676

**Verdict: PASS at the exact stated binary directed-multigraph scope.** No substantive mathematical defect was found in the six-page published proof, the necessary current mathematical support, or the inspected primary interfaces. This is an independent AI mathematical review, not human peer review, formal certification, a novelty certificate, or a publication approval.

## 1. Immutable subject and independence

The subject is *CoNP-completeness of binary directed chip-firing reachability*, version 1.0, manuscript/metadata date 15 October 2026. The public record was created on 17 October; neither date is used here to infer discovery or deposit priority.

- Public six-page `paper.pdf`: SHA256 `6ae840e0b2e1df73b204c2c293c3fbcfa39206654e775a75261515c693a6187d`, 77,187 bytes.
- `pr1097_support_v1_0.zip`: SHA256 `94280d71c41617198e96f1f4b4aca043ff86c3feda3109e0af9a1a18e1db651d`, 5,658,794 bytes.
- Actual `paper.tex`: SHA256 `daaacbeb3b198a8c13208663a6e49fc417a5b7ec2e7a0bfa62a9a87e42ce7f5f`.

I read every published PDF page and the complete current TeX. I reconstructed the reduction, preprocessing and certificate before reading or executing current published helpers. I then wrote and executed independent exact controls. Only afterward did I read `scripts/run_checks.py` and `scripts/common.py`; I executed the former unmodified in an isolated copy. `scripts/verify.py`, dedicated historical assessment bodies, and sibling mathematical findings remain unread. Historical paths were enumerated or hashed only. The paper's own disclosure/status paragraphs, and current code comments saying historical programs were not replayed, were incidentally encountered and are not treated as review evidence. I did not independently reproduce its claimed historical audit totals or adopt its historical conclusions.

The fresh public receipt and record were checked, both assets were rehashed against that receipt, all ZIP CRCs passed, and every one of the 198 extracted regular files matched its archive bytes. The embedded PDF is identical to the public PDF. Originals were not modified. Exact bindings and primary reading scopes are in `evidence/source-binding.json` and `evidence/primary-imports.json`.

## 2. Claim, success criterion and exclusions

The theorem concerns ordinary sequential legal chip-firing on a finite, nonempty, loopless, strongly connected **directed multigraph**, with binary adjacency entries and nonnegative binary initial and target configurations. The vertex count varies with the input. A firing at v requires at least its full outgoing degree, removes that many chips, and distributes outgoing multiplicities. No sink absorbs chips. A word may be empty and may stop even when further firings are available. Invalid encodings are rejected.

The claim is coNP-completeness under deterministic polynomial-time many-one reductions. I checked a total reduction from the complement of the credited halting problem, both logical directions for arbitrary legal target-reaching words, polynomial **bit** complexity, and an attributed polynomial-size complement certificate. The loopless singleton has degree zero and unchanged state under every firing; reachability is exactly x=y. It is separately handled.

The construction does not prove corresponding hardness for simple graphs, unary encodings, bounded degrees, bounded chips, fixed vertex count, or every signed-configuration formulation. The cutoff can be exponentially large numerically. No polynomial-time trajectory simulation or polynomial witness length is asserted. These restrictions are explicit in the manuscript and remain essential to this verdict.

## 3. Source hardness and preprocessing

I checked Farrell–Levine's model and full relevant Section 3, including the total-Laplacian construction in Theorem 3.1 and Corollary 3.2. It supplies the NP-hard binary strongly connected multigraph halting interface, with loops allowed. A signed lattice representative must not simply be called a nonnegative configuration. The current paper supplies a valid explicit bridge: add k_v=max(0,−x_v) loops and k_v chips at v. The firing matrix remains unchanged, but both the state coordinate and the legal threshold increase by k_v after every word. Thus every legal word corresponds step by step, including stability and infinite play. This checks thresholds, not only equality of Laplacians.

Loop removal also requires more than deleting the diagonal. Replace ℓ_v loops by ℓ_v arcs in each direction between v and one fresh empty relay. An original firing lifts by immediately returning its relay packet. Conversely, for any expanded legal word the relay count s_v and parent count t_v satisfy s_v≤t_v, since its chip count is ℓ_v(t_v−s_v). The projected original state at v exceeds the expanded state there by exactly the pending packet. Every projected parent firing is consequently legal. An infinite expanded word has infinitely many parent firings, because relay counts are bounded by their parent counts. Hence existence of infinite play is preserved both ways, and the halting dichotomy completes the equivalence. Connectivity, polynomial multiplicity bits, and at most one new relay per original vertex are preserved.

A singleton with ℓ loops never changes its chips and is nonhalting iff x≥ℓ, including ℓ=0. The paper classifies this case and substitutes a two-cycle with a fixed halting or nonhalting configuration. Thereafter n≥2 and all source degrees are positive.

I also checked the total-language issue. If a HALTING reduction outputs an invalid NO string, it can instead output a fixed valid nonhalting NO instance; complementing then yields valid NONHALTING outputs. For the valid-instance NONHALTING language with invalid strings rejected, the current reduction sends invalid input to a NO reachability pair of different total mass. Alternatively the literal complement of HALTING includes invalid strings, which must map to a fixed YES pair. The paper states these as distinct conventions, so there is no conflicting promise or hidden partial reduction.

## 4. Gate/marker proof under adversarial firing orders

Let C be total chips, D maximum source outdegree, and i_v incoming degree. Set N=(C+1)^n, M=N+1, B=N(MD+1). At most N nonnegative source states exist by conservation. A legal word of length N visits N+1 states and repeats one, yielding an indefinitely repeatable nonempty legal closed word. Conversely nonhalting supplies such a prefix. The dichotomy connects existence of that infinite play to the source problem's quantifier. C=0 gives N=1 and no legal source move because all degrees are positive.

The gadget scales old arcs by M; adds one old-to-gate arc per vertex, B gate-to-old arcs per vertex, and one arc each way between gate and marker. It remains loopless and strongly connected. Old thresholds are Md_v+1, gate threshold nB+1, marker threshold 1. The stated initial and target vectors have equal total mass and nonnegative coordinates: in particular Y_v≥B−MND=N, and X_g≥1. I expanded the endpoint equation independently; the specified target is exactly X+L_H f for counts f=(N,…,N,1,0).

Before the first gate firing, the marker is empty and cannot fire. After t old moves, with counts t_v and projected source state z, the exact old coordinate is Mz_v+N−t_v, and the gate holds nB+1−N+t. For t<N, t_v≤N−1. A source-legal move has at least Md_v+1 gadget chips, while a source-illegal move has at most M(d_v−1)+N=Md_v−1. This is an induction on every chosen order, including the last prefix move, with a strict margin on both sides. The first gate cannot fire before N old moves and becomes legal at N. Delaying it does not invalidate the argument about the first N moves.

For the forward implication, lift an N-move legal source prefix and fire the gate once. Every old vertex receives B additional chips. Complete each old count to N in any order while leaving gate and marker unused. A vertex needs at most N payments of Md_v+1, funded by B≥N(Md_v+1), even if all future incoming chips are ignored. Immediately before each requested payment, fewer than its allotment have occurred. Thus cleanup is legal. Stopping at the target is permitted; the marker's one chip may make a further firing possible without invalidating reachability.

For the reverse implication, I did not assume the legal target-reaching word has designated count f. If its actual counts are k, marker balance gives k_g−k_m=1. The gate must therefore have fired. Before its first firing, no marker firing occurred, and the gate's initial deficit N could only be filled by at least N old moves. Those first N moves project legally by the strict simulation estimate and force nonhalting. Extra periods, a late first gate, or later marker/gate firings cannot evade this argument. A target recurrence premise and uniqueness of the firing vector are unnecessary.

This is the main strength of the submitted proof: a local endpoint constraint forces the relevant prefix in every possible realization. The fresh complete finite gadget closures corroborate this quantifier rather than checking only the designated word.

## 5. Bit complexity and credited membership

For input length s, n≤s, and C,D have polynomial bit length. The bit length of N is at most 1+n log₂(C+1), including the constant in the C=0 case. M,B and all output entries therefore have polynomial bit length. Preprocessing adds only linearly many vertices; the adjacency matrix has polynomially many entries. Binary exponentiation and the required integer arithmetic take polynomial bit time. The reduction neither writes a length-N word nor expands parallel arcs into unary edge lists. The large numerical reserves thus do not violate Karp reduction size.

For coNP membership, I independently reconstructed the attributed strongly connected argument. The integer kernel of L is generated by a positive primitive integer period p. Directed tree cofactors and their gcd give polynomial-bit p. Polynomial-time integer linear algebra decides whether y−x lies in the integer image and computes h when it does. Subtracting min_v floor(h_v/p_v) copies of p yields a nonnegative solution g with some g_w<p_w. Every other nonnegative solution is g+kp, k≥0; this proves reducedness and uniqueness without a trajectory bound.

The claimed bit bound for g is valid: remove row and column w, use the nonsingular principal minor to solve for g away from w, and bound cofactors and numerators using g_w<p_w. Integer denominators have absolute value at least one. Large numerical firing counts do not imply a large certificate encoding.

Period deletion is the exact Björner–Lovász comparison. In a legal word with counts at least p, delete the first p_v occurrences at every vertex. At a retained firing of v its own deleted count has reached p_v, while every other deleted count is at most its period coordinate. Hence (Lr)_v≤(Lp)_v=0, so the retained word has at least as many chips at its firing vertex. Its endpoint is unchanged. Iterating reduces any reachable realization to g. I checked the complete primary deletion proof as well as the manuscript's specialization.

A complement witness u satisfies 0≤u≤g, u≠g, and (x+Lu)_v<d_v whenever u_v<g_v. It need not itself be legally realizable. In a hypothetical legal g-word, the first move exceeding u has its own preceding count equal to u_v and all other counts bounded by u; nonnegative off-diagonal entries bound its available chips by (x+Lu)_v, contradicting legality. Conversely a maximal legal word with coordinatewise bound g ends at a proper such u if g is impossible. The verifier only checks the short integer vector and inequalities; it does not run that possibly long maximal word. Integer-image failure, invalid encodings and the singleton branch are polynomially decidable. Strict inequality, properness, and reducedness are all material.

## 6. Direct primary interfaces and attribution limits

Five primary PDFs were independently rehashed. The exact URLs, hashes, text-line intervals and reading limits are recorded in `evidence/primary-imports.json`.

- **Björner–Lovász, revised July 1992 author manuscript:** Proposition 4.1 and the full Lemma 4.3 period-deletion argument, printed pp. 12–13. It supports the period mechanism credited here.
- **Farrell–Levine, arXiv 1502.04690v3:** definitions and input model, least-action interface, and complete relevant Section 3 (printed pp. 10–13), including full Theorem 3.1 construction and Corollary 3.2. Its signed lattice interface is bridged by the current threshold-preserving normalization.
- **Hujter–Kiss–Tóthmérész, arXiv 1507.03209v4:** loopless/binary/nonnegative conventions, dichotomy/period statements, full Proposition 8 and Theorems 12 and 14 proofs, and Problem 19 on p. 12. The coNP theorem matches. The recurrent-target theorem genuinely retains a recurrence hypothesis. Problem 19 authenticates the historical general-digraph hardness question.
- **Kiss–Tóthmérész, arXiv 1407.6958v3:** Section 4 setup and complete Claim 4.4 bounded-reserve proof. Large reserves and finite-horizon simulation are prior mechanisms, correctly credited, rather than a fresh general technique established by this paper.
- **Tóthmérész, arXiv 2102.11970v2:** Theorem 2.3 context, complete Claim 2.4 and Proposition 2.8 arguments. Recurrence reduces to return reachability after a chosen legal first firing. Existence of a recurrent representative of a nonhalting class is not a deterministic polynomial-time construction of that representative as a Karp output. The earlier polynomial-hierarchy barrier is not silently substituted for this paper's stronger many-one classification.

The live Egres acquisition timed out; I did not read or rely on its body. HKT v4 suffices to authenticate the historical question. I did not read every passage of every primary paper or conduct an exhaustive literature/priority audit. Standard integer-linear-algebra algorithms and the established cited source hardness are accepted at their inspected interfaces; I did not recursively reprove all underlying complexity literature. Exact-result priority, exact-gadget priority, independent discovery, and current worldwide openness remain unverified. These are not central mathematical gaps in the submitted attributed proof.

## 7. Independent controls and unmodified replay

The fresh standard-library control was authored and executed before helper reading. It uses exact integer/Fraction arithmetic, full finite-state closures where claimed, count-state enumeration and direct certificate enumeration. It contains its own graph routines and no imports from the published kit.

- 27 source graphs: nine two-vertex positive-multiplicity graphs and all 18 strongly connected simple three-vertex digraphs in the tested class.
- 126 source instances; 316 prefix count states with exact legal-set and gate comparisons; 1,878 cleanup count states.
- Twelve complete unrestricted gadget closures containing 1,652 states total, with target reachability equivalent to independently determined source cyclicity. The emergency cap was not reached.
- 400 signed-normalization cases and 216 loop-relay cases, including complete state-graph cycle comparisons.
- 910 reduced target pairs, 44 integer-image failures, and 4,382 blocking-vector candidates compared against full reachability.
- 12,239 explicit period-deletion checks; 20 singleton/zero-degree checks.
- Large binary-output checks for n=2,5,12 and 257-bit total chips, without constructing an enormous trajectory.

Four intentional faults were detected: an insufficient cutoff gives an explicit false-YES word on a halting source; an initially legal gate permits a false YES; insufficient scale permits a source-illegal move; and naive loop deletion changes legality. These controls test mechanisms that could invalidate the proof, rather than merely matching a desired output.

After this independent work, I read and replayed the current standalone `run_checks.py`, byte-for-byte unchanged, in normal, `-O`, and `-OO` modes. All returned PASS with identical stdout. Its `--inject-failure` branch failed as intended in all three modes, so its unconditional checks remain active under optimization. That script also exhibits two target-reaching words with distinct gate/marker counts and detects malformed certificate variants. All six commands, return codes and output hashes are saved. I did not execute the historical-assertion-bearing `verify.py` or claim a replay of omitted historical programs. I did not rebuild the PDF: the actual published PDF/TeX were both read, and their mathematical content agrees in the reviewed proof.

The computations are finite corroboration, not a replacement for the universal estimates and proof above. There is no floating-point tolerance or numerical stability dependence in these controls.

## 8. Final disposition

**Strongest verified result:** the submitted attributed proof establishes coNP-completeness for the precise binary, nonnegative, loopless strongly connected directed-multigraph reachability language, including total encoding conventions and the singleton boundary. The deterministic hardness map handles all target-reaching words, and the prior complement certificate has polynomial encoding length.

**Substantive findings:** none. **Unresolved central proof gaps:** none identified within that scope. The exclusions, source-reading limits, lack of formal/human verification and unknown priority remain as stated above. No repair, publication, website, spreadsheet, Git, deployment, or outreach action was performed. Previously sealed reviews were preserved.
