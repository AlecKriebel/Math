# Independent adversarial audit: AMR-011-0005

## Verdict

**PASS, restricted to the frozen packet's stated partial results.** The full Abért–Virág shortest-law problem remains unresolved by this investigation after five approaches. There is no complete candidate, verified asymptotic determination, historical novelty certification, formal proof-assistant verification, or external human peer review.

No mathematically necessary correction was found. In particular, the exact depth-four claim is **L_(4,2) = 16**, not an all-variable claim. The all-variable exact claims remain L_1 = 2, L_2 = 4, L_3 = 8. The retained general estimate is n < L_n <= 2^n.

The audit is bound to author manifest SHA-256 `7945b043809987bd5e6af09ee2bd279aaca7855698d9d556cd17a0c081b85aa5` and the 21,562-byte author ZIP with SHA-256 `6a4403908dcf263fe30c005e94078c116cbb4a6e14db6009b3ac865576a68fb0`. All ten archive members match the frozen files byte for byte. No author file was edited.

## 1. Target and literature scope

The primary source is [Abért, Some questions](https://www.renyi.hu/~abert/questions.pdf), dated November 2, 2010, Question 5. The source asks the shortest-law length for the n-fold binary wreath tower and proposes the power word of length 2^n. Its tree interpretation establishes the imprimitive action. No fixed variable rank is specified there. The imported asymptotic formulation is therefore weaker than the precise primary question.

[Bradford's author manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/fd15be02-36ce-4a0d-8a47-2653cd3c8715/content), June 14, 2023, uses W_0 = C2 and thus n+1 factors for W_n. Proposition 6.4 applies to every fixed finite free rank and excludes laws of length at most n+1 in that indexing. Replacing its index by n-1 gives exactly the packet's n < L_n. Question 10.3 asks the finite shortest-law question and its continuation discusses the power word. The relevant pages were independently read, and the question/continuation visually checked. No finitely generated infinite-group word-metric estimate is substituted for the finite-law length here.

The inspected 2025/2026 [Fariña-Asategui paper](https://arxiv.org/html/2505.23142v1) concerns Hausdorff dimensions and qualitative lawlessness. Its Question 1, Theorems A and C, and Corollary 5 do not determine this finite minimum. The arXiv record's 2026 online-first journal statement was confirmed. [Bradford–Willis, version 2](https://arxiv.org/html/2503.23582v2), concerns lawlessness growth of infinite finitely generated groups; its Lemma 2.6 packages existing nonlaw evaluations into a direct product and supplies no missing bound for this tower. Neither similarly related title resolves the target.

The inspected [Abért–Virág manuscript](https://www.math.toronto.edu/~balint/tg14.pdf), Proposition 4.1 and Theorem 4.4, supplies infinite-tree/random-action context, not the asserted finite optimum. [Thom, Propositions 3.1–3.2](https://arxiv.org/pdf/1508.07730v2), bounds laws by group order. With M = 2^(2^n-1), the quoted bounds become O(2^(3n/2)) and O(2^(9n/2)); the packet correctly declines to treat them as improved guarantees or lower bounds on every output of those methods.

All six local PDF byte counts and SHA-256 values were independently recomputed and match the source metadata. Publicly accessible versions and the stated relevant results were independently inspected. This does not claim fresh network-byte equality for all six PDFs or an audit of every cited paper's dependency proofs.

Both complete public corpus files were independently hashed and compared with the independently retrieved [immutable repository manifest](https://github.com/AlecKriebel/Math/blob/6144d964777214c6963a915288c18fcf97b42026/unsolved_math_prioritization/manifest.json). The target numeric ID and problem code each occur once. The complete selected record and report were read; the report matches its entry in the bound full corpus. The catalog byte count, SHA-256 and Git blob hash also match the author's pinned metadata. No source text or dataset contents are redistributed in this audit.

Fresh GitHub searches for the exact ID and exact problem code returned no PR matches. The packet's wider repository searches remain bounded historical observations at its stated snapshot, rather than proof of universal absence. Independent public searches found no verified resolution within the inspected results; no worldwide current-open-status claim follows.

## 2. General proof audit

### Word length and rank reductions

The definition counts generator letters, with powers expanded, and excludes coefficients and the empty reduced word. Assigning an element of exact order 2^n to one variable and identity to the others proves the exponent-sum divisibility claim. Below length 2^n, each exponent sum must be zero. Hence the total length is even, and each used variable occurs at least twice, once with each sign.

Every nontrivial free-group element has a nonempty cyclically reduced conjugate. Conjugacy preserves universal lawhood, while deleting a conjugating prefix and inverse suffix cannot increase length. The enumeration need not divide further by cyclic rotations: it retains all signed-renaming representatives with no inverse first/last pair. Retaining cyclic duplicates is harmless. Variable renaming and independent inversion are bijective changes of assignments and preserve length and lawhood. Word inversion does also.

Consequently, depths one and two reduce as claimed. At depth three a hypothetical shorter law leaves only lengths four and six with at most three variables. This proves the all-rank reduction without asserting a length-preserving arbitrary-rank embedding into F_2. At depth four, words shorter than sixteen may use up to seven variables; those ranks are outside the two-variable computation.

### Order, exponent, and linear lower bound

The order recurrence gives 2^(2^n-1). The exponent induction and root-swapping maximal-order element establish exponent exactly 2^n and the power-law upper bound. The embedding preserving an additional final bit proves monotonicity.

The separated-prefix proof works for every freely reduced nonempty word, including words whose last letter is negative or introduces a new variable. Inverting that variable reduces the negative case to the positive one. The bottom sibling swap is inserted before the last positive action at the penultimate projected vertex. An earlier positive edge cannot start there because prefix vertices are distinct. An earlier inverse edge can be affected only if its terminal vertex is there, which would have to be the immediately preceding edge; free reduction forbids it. Thus all previous prefix images remain on last-bit zero, while the final image acquires last-bit one. This argument allows the old final image to repeat any earlier image; it does not require a return to the initial image specifically.

The construction yields a counterevaluation at depth equal to word length; embedding supplies the statement for all shorter words at depth n. It does not justify using only logarithmically many levels. Its source attribution and indexing are correct.

### Section criterion and composition

Under the chosen right action, positive letters use the section at the input child and then toggle the root state. For an inverse letter, the root toggle must occur first to determine which original input section to invert. The displayed transitions satisfy this requirement. Every pair of child sections is independently assignable in W_(n-1). The necessity and sufficiency proof is therefore valid, and the depth recursion terminates even when section word length does not decrease.

The commutator's eight formal sections really have reduced length four. This defeats the stated literal universal half-length-section claim only; it does not prohibit more sophisticated specializations.

### Central powers and alternative laws

The bottom flip is central by induction on sections and invariance under the root swap. In the non-root-fixing case, the two squared sections are ab and ba, which are conjugate. Their central half-powers must agree, giving either identity or the common bottom flip. The base case and root-fixing case are valid. The resulting commutator expands to 2^n+2 letters and is freely reduced; it does not improve 2^n. The disjoint-variable derived-word construction has length 4^n and is likewise only a weaker upper bound.

## 3. Independent computation and coverage

The principal independent checker was written afresh. Its core does not import the author's enumerator, recursive law test, witness constructor, inverse routine, or permutation evaluator.

- It enumerates full fixed-alphabet reduced strings, filters balance and cyclic reduction only afterward, and canonicalizes signed variable names.
- At depth three, a second Cartesian-product enumeration on all six signed F_3 letters reproduces the one length-four and seven length-six candidates.
- At depth four, candidate counts at lengths 4, 6, 8, 10, 12, 14 are 1, 3, 27, 190, 1510, 11851. The total is 13,582.
- A separate forward dynamic program over all four possible first letters gives 8, 24, 216, 1520, 12080, 94808. Division by eight is valid because a nonempty balanced reduced two-variable word uses both variables, so signed permutations act freely.
- The independent group encoding numbers internal vertices in breadth-first order, rather than the author's recursive preorder. Each leaf is acted on directly using its input-prefix bits. Permutation membership is checked by bijectivity and preservation of every binary prefix block.
- A fixed SHA-256-derived assignment bank supplies a checked moved leaf for every candidate. All eight depth-three candidates need at most two bank trials; every depth-four candidate needs at most seventeen. No successful sampling or probability estimate is used to certify a law. Each nonlaw has an explicit exact counterevaluation.

This gives 13,590 fresh counterevaluations. The deterministic independent certificate stream hashes to `e9f3ebc893a505d507ea914325c86f6771e29d623c964ac93518947acfb0ea91`.

Only after that independent proof does the checker import author code for cross-checks. It compares exact candidate sets, rejects duplicates, reconstructs every author certificate using the independent tree action, and checks the full evaluated permutation. Both author certificate-stream hashes match, including all 13,582 depth-four certificates. The eight printed proof-table rows are separately checked for completeness and for moving leaf zero to one.

Further controls independently check:

- all 32,906 portraits at depths one through four, their tree actions, inverse actions, orders, and central half-powers;
- 1,456 reduced F_2 words through length six against direct W_2 evaluations and the author's recursive criterion;
- all 1,456 corresponding separated-prefix witnesses, including tree membership and every prefix position;
- 54,328 depth-four transformed-word membership checks covering cyclic rotation, word inversion, individual generator inversion, and generator exchange;
- rejection of identity assignments as a purported commutator counterevaluation;
- byte-identical author offline replay.

The checker uses explicit exceptions for its independent assertions. The author's required offline replay still intentionally rejects Python's optimized mode because the original controls use assertions. See `INDEPENDENT_RESULTS.json` for exact counts and hashes.

## 4. Publication and stopping conditions

The author freeze is preserved. Its pending-audit field is historical; a publication wrapper may record this separate scoped PASS without altering frozen author bytes. Publication must retain `unsolved`, five of five approaches, no full candidate, and the depth-four rank-two qualification.

This audit folder contains only authored review, source-identification metadata, hashes/counts, and verification code/results. It contains no PDFs, extracted source pages, raw imported records, private-source contents, or private coordination. No remote write, PR change, merge, release, or third-party communication was performed.
