# Independent audit of the literal dense cycle assertion

## Decision

Accept the classical-theorem-based refutation of the unrestricted H2 assertion associated with ID 2193, EP-584, rank 898. The refutation also defeats the joint unrestricted H1-and-H2 assertion. It is an already publicly documented obstruction, not a new solution. Do not mark the intended sparsity-qualified internal strong-C6 problem generally resolved. The exact accepted payload and exclusions are recorded separately in EXACT_ACCEPTANCE.json and EXACT_ACCEPTANCE.md.

The original five authored files have no blocking mathematical defect. A separately frozen clarified derivative corrects the distinction between an absent research-report key and an existing empty report, makes the background-versus-statement-field distinction explicit, and spells out the H1 limitation. CLARIFICATIONS.patch is an actual unified patch; replay against freshly extracted original files reproduces all five derivative files byte for byte. The original archive, manifest and files remain unchanged.

## Complete inherited input check

All three complete corpus byte counts and SHA-256 digests match the supplied pins. The catalog identifies precisely ID 2193 / EP-584 / rank 898. A unique complete problem record is present. Its statement digest matches b28737a9849838c6181d10b15f85a2d8e4eadce8040f8c437d8dbd8b06db485b. Serializing [complete_record, reports.get(problem_number, {})] with json.dumps(sort_keys=True), retaining all other defaults, yields e1601693f7c82888489d082791d70f661cbeb1cdb3bf38c03ebc0927279b48d7. The EP-584 report key is absent; its effective value is {}. The entire record, including all background and dated literature triage, was read. No substantive inherited authored proof or computation was present.

The unqualified statement field asks for a lower bound proportional to delta^2 n^2 for H2, with every distinct pair of its edges on a simple cycle of length at most eight. The entire inherited background is more informative: it distinguishes fixed positive density from polynomial sparsity, records the Fox–Sudakov restricted range, and treats the intended sparse problem as unresolved in a dated assessment. Its prose and status labels are not proofs. It would be a scope error to discard this background and advertise the literal wording issue as resolution of the intended research problem. No dataset text is republished in this audit.

## Mathematical verification

Use the density convention explicitly present in the target: delta=e(G)/n^2, not e(G)/binomial(n,2). The lower-bound constant for the rejected assertion must be positive and uniform in both n and delta. Distinct H1 and H2 may be chosen, and disproving H2 alone suffices for the conjunction.

The invoked external theorem is Lazebnik–Ustimenko–Woldar, Proposition 2.1(i),(iii), in [LUW]. Its hypotheses permit every prime power q and every positive integer k; its girth bound requires k odd. At k=5 it gives a simple bipartite q-regular graph D(5,q) with n=2q^5 and girth at least 10. Prime q≥2 is a sufficient subfamily. The q-congruence in part (iv) is needed only for equality of the girth, not for the lower bound used here. The exceptional order formula at k=1 is irrelevant. No large-q qualification or connectivity assumption is silently imported.

The finite-coordinate definition independently confirms the vertex and degree counts: the two vertex classes each have q^5 coordinate vectors; for each point, the line's first coordinate can be chosen in q ways, and the remaining four incidence equations determine the rest successively. The reverse calculation similarly gives q neighbors for each line. Thus the handshake identity gives m=nq/2=q^6. Consequently

- delta = 1/(4q^4)
- delta^2 n^2 = q^2/4
- delta^3 n^2 = 1/(16q^2)
- delta = 2^(-6/5) n^(-4/5)

There is no cycle of length at most eight anywhere in G. If a proposed H2 has two distinct edges, those edges are either adjacent or disjoint. In either case its defining property would require a forbidden cycle in G. Allowing the cycle to use edges outside H2 does not help. Internal cycles, being ambient cycles too, are also excluded. Hence e(H2)≤1, with a single-edge subgraph satisfying the pairwise property vacuously under either convention.

For an arbitrary proposed uniform c2>0, take a prime q>2/sqrt(c2). Then c2 delta^2 n^2=c2 q^2/4>1. Primes are unbounded, so q can also satisfy any fixed global lower bound on n. The claimed H2 size is impossible on arbitrarily large graphs. This is an infinite-family argument conditional on the named published theorem; the arithmetic replay is only a consistency check, not a finite-computation substitute for that theorem.

The H1 quantity instead tends to zero. A single edge satisfies H1's pairwise conditions vacuously, so this family alone does not refute a bound c1 delta^3 n^2 for fixed c1 at large q. No such H1-only negative is accepted. Likewise the argument does not refute an assertion for each fixed delta with an n-threshold depending on delta. The dependency on the published LUW girth theorem is explicit; its underlying proof is not independently reproduced here.

## Prior attribution and witness conventions

The currently accessible [ULAM] note, carrying the printed date April 21, 2026, states the same high-girth obstruction in Theorem 1 and Corollary 2. It uses a component CD(5,q); the accepted derivation uses all of D(5,q), whose order is exact. Both yield the same obstruction. For the component proof, q-regularity and simplicity imply its order grows at least as q+1, supplying the unbounded-order step. The original date of online publication is not independently established by an archive; the document's printed date and current availability are verified. Its separate Proposition 4 is outside this acceptance and unnecessary.

[FS] defines cycle-connectedness internally. Problem 1.1 quantifies a positive small exponent bound; Theorem 1.2 gives a strongly C8-connected subgraph of at least n^(2-2 beta)/64 edges for each fixed 0<beta<1/5 and sufficiently large n. Adjacent pairs have cycles of length at most six. The proof uses n>2^20 k^5 with k=n^beta. This is not silently extended to every n and every variable density just above a bare threshold. The accepted counterexample has exponent 4/5, outside that range. The concluding discussion identifies the stronger internal C6 question as a distinct historical gap.

[Duke–Erdős] Corollary 1 fixes a positive density parameter and allows the resulting constant and large-n threshold to depend on it. Its witness cycles lie in the selected subgraph. The final graph discussion already recognizes large-girth obstructions to unrestricted short-cycle requirements. Neither this result nor its quantifiers can be replaced by an arbitrary density-sequence conclusion. The original packet's failed 1984 full-PDF retrieval remains disclosed and is not counted as full-source inspection.

## Current manuscript is not certified

[Li] is arXiv:2606.06522v1, submitted June 2, 2026. Its definitions and theorem statements distinguish internal weak-C6 and internal C8 cores through density n^(-1/3), an ambient strong-C6 selection when k=o(n^(1/2)), and a claimed internal strong-C6 obstruction for fixed beta in [1/3,1/2). The weak-C6 positive statement does not impose adjacent-edge C4 witnesses. The ambient theorem allows extra witness edges. Neither can be substituted for the internal strong-C6 target. The full manuscript proofs were not audited, and no new correctness or peer-review claim is made. The accepted negative does not use this manuscript.

## Retrieval and integrity limits

Five source PDFs were freshly retrieved during this audit; every byte count and SHA-256 matches the original packet's public source metadata. Relevant pages were textually inspected, and LUW Proposition 2.1, Fox–Sudakov's theorem page, the prior note's theorem/corollary page, Li's definitions/theorems, and Duke–Erdős Corollary 1 were also rendered and visually checked. SOURCE_AUDIT.json distinguishes the exact scopes.

Fresh web-tool attempts on both exact live problem pages returned Internal Error without content. The original packet separately reports historical HTTP 403 and browser blocking. No fresh live-page contents, live status, or live identity match is asserted. The acceptance is anchored to the complete supplied record/report pair. Bounded repository-search claims in the author's log were not independently repeated and do not establish novelty or exhaustive absence of other work.

Both original and clarified safe archives contain five authored files only. The audit package adds authored analysis, the actual clarification patch, a replay program, exact acceptance, and public verification metadata. It includes no raw PDFs, image renders, source extracts, dataset records, private-source contents or private coordination. No publication, repository change, queue change, merge, or new mathematical search was performed by this audit. Original source-stage STATUS.json is preserved in the derivative; this separate acceptance is the later independent review record.

## References

- [LUW] F. Lazebnik, V. A. Ustimenko and A. J. Woldar, A new series of dense graphs of high girth, Bulletin of the AMS 32 (1995), 73–79, Proposition 2.1. https://arxiv.org/pdf/math/9501231
- [ULAM] A note on the formulation of Erdős Problem #584, printed date April 21, 2026, Theorem 1 and Corollary 2. https://www.ulam.ai/research/erdos584.pdf
- [FS] J. Fox and B. Sudakov, On a problem of Duke–Erdős–Rödl on cycle-connected subgraphs, JCTB 98 (2008), 1056–1062. https://people.math.ethz.ch/~sudakovb/cycle-connected.pdf
- [Duke–Erdős] R. Duke and P. Erdős, Subgraphs in which each pair of edges lies in a short common cycle, Congressus Numerantium 35 (1982), 253–260. https://users.renyi.hu/~p_erdos/1982-35.pdf
- [Li] Eric Li, On the Duke–Erdős–Rödl Problem at the One-Third Threshold, arXiv:2606.06522v1. https://arxiv.org/abs/2606.06522v1
