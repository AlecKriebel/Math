# Independent adversarial audit: prescribed block-code extension

## Disposition

**PASS: the frozen proof gives a complete effective criterion for the specified map in Boyle Problem 16.3, conditional only on the expressly cited published PRZ separation theorem.** No correction to the frozen mathematical argument is required. This is an independent AI mathematical audit, not formal verification or human peer review. Novelty, publication priority, and a present-day consensus that the original problem is open are not established.

The target is a nonempty two-sided mixing sofic shift T and a specified surjective sliding block map f:T→T. The criterion decides whether f extends to a block map from some SFT containing T into T. It does not decide whether an arbitrary given shift admits some suitable map, nor does it characterize stable cellular-automaton limit sets. Equality of the SFT and T is permitted by the original source's wording. Irreducibility suffices in place of mixing.

Audit date: 2026-10-06. The reviewed author archive and all extracted author files are unchanged; its frozen status file correctly continues to record that audit was pending when the author packet was created.

## Source and identity verification

The complete catalog, problem corpus, and research-report corpus match the author's pinned byte counts and SHA-256 values. Independently selected record 4600024 / AMR-045-0024 is ranked 820. Re-encoding the entire selected problem record and its entire associated report using the stated default Python JSON convention reproduces the 3,101-byte review hash. The statement hash also matches. The corpus report is a historical triage record, not authoritative evidence of current openness.

Fresh public downloads reproduce both decisive PDF hashes and sizes. Boyle's printed page 17 was freshly rendered and visually inspected; Problem 16.3 concerns the given surjective self-code, and includes neither a receptive-fixed-point hypothesis nor strict containment. PRZ's printed page 8 was freshly rendered and visually inspected; its Theorem 4.2 uses a common finite recognizing **monoid** and gives exactly k=4(|M|+1). Definitions on printed pages 4–6 establish the finite-word, empty-word, and profile conventions. The theorem is used as published, not independently reproved here.

Sources:
- Mike Boyle, *Open Problems in Symbolic Dynamics* (2008), Problem 16.3, printed p.17: https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf
- Thomas Place, Lorijn van Rooijen, Marc Zeitoun, *On Separation by Locally Testable and Locally Threshold Testable Languages*, LMCS 10(3:24), 2014, Theorem 4.2: https://lmcs.episciences.org/1163/pdf ; DOI https://doi.org/10.2168/LMCS-10(3:24)2014

## Mathematical review, including attempted failure modes

### A. Finite words versus bi-infinite points

After removing graph vertices without both an infinite past and an infinite future, and retaining their connecting edges, every surviving finite graph path extends on both sides. This justifies using every surviving vertex as initial and final to recognize L(T). It does not require the supplied presentation itself to be strongly connected. The subset construction has an initial state equal to the entire vertex set; acceptance is nonemptiness. The empty word is accepted because T is nonempty.

For n≥2, the overlap graph with vertices L_(n−1)(T) and edges L_n(T) is strongly connected. To connect vertices u and v, use irreducibility to obtain a word ucv in L(T), then read its successive overlaps. Thus every path extends to a bi-infinite path. Every length-n word of T occurs in T[n], and every length-n word of T[n] was allowed by construction. These facts give the claimed equality of n-block languages.

For a word of length at least n, local n-admissibility gives a finite overlap path and hence extendability. For a word shorter than n, membership is **not** vacuous local admissibility: it is membership in L(T). This is exactly the convention stated explicitly in proof Section 2. Conversely, any such short word in T[n] lies inside an n-block of a point and hence lies in L(T). No dead-end finite paths or spurious short words enter the intersection test.

Labelling each overlap edge by its last symbol does recognize the entire finite-word language, including short words: a graph path extends backward to supply the initially omitted n−1 symbols, and every finite point block can be read as edge labels starting n−1 coordinates earlier.

### B. Regular bad-word language and its ideal property

For local window length ell, the transducer retains at most ell−1 input symbols and feeds one output letter to a complete DFA for L(T) exactly when a full window is available. For |w|<ell, no output letter is fed, so F_*(w)=epsilon and w is not bad. A word is accepted by the bad DFA precisely when its complete output word is outside L(T).

If w is bad, its output F_*(w) is a contiguous output factor of F_*(uwv), independent of memory/anticipation offsets. Factoriality of L(T) therefore makes B a two-sided ideal. It is immaterial whether a generic DFA uses a visibly absorbing rejection state: acceptance/rejection is checked for the entire output, and factoriality proves the semantic property. Since f maps T into T, L(T) and B are disjoint.

For any bi-infinite x, F(x) lies outside T exactly when a finite output block lies outside L(T). The corresponding finite input window is a bad word. Conversely, every bad input word occurring in x produces such a forbidden output block. This verifies the all-length language-intersection equivalence, without a bounded witness-length assumption.

### C. Fixed completion versus arbitrary extension radius

An SFT S containing T has a finite forbidden list. Choose n at least every forbidden length; if each n-word of a point belongs to T, none of those forbidden words occurs. Thus T[n]⊆S. The same argument works after intersecting a larger-alphabet S with A^Z.

If a different block map G extends f, enlarge G's and F's windows to a common contiguous interval. Their output rules coincide on every T-word in that interval. Increasing n to cover its length makes F and G identical on T[n]. Consequently arbitrary radii and different choices on words outside T confer no extra existence power. There is no unsupported assumption that equal maps on T have globally equal local rules.

Surjectivity is used only at the last step: T=f(T)⊆F(T[n]); hence inclusion in T becomes equality. Without surjectivity the same existence test still works but the equality conclusion must be removed. The automorphism argument is valid because the local identity gF=id can be extended to a sufficiently fine neighborhood, while F's image there is already in the domain of g.

### D. SFT witness to locally testable separator

Strong connectivity makes L(T[n]) equal to the language of words whose n-factors are allowed, with the expressly specified finitely many short-word exceptions. Excluding finitely many factors is locally testable; finite languages are locally testable; this supplies an LT separator. There is no conflation of an arbitrary sofic language with an LT language, and there is no need to assume that languages of arbitrary graph presentations are LT.

### E. Critical saturation lemma

This is the key new reduction and survives adversarial review.

1. Irreducibility concatenates a finite list of all n-words into one U∈L(T). Further allowed extension can make U arbitrarily long.
2. If w∈B occurs in T[n], irreducibility of the overlap graph produces a single word W=UcwdU in L(T[n]). To justify simultaneous concatenation, first join U to w, then join that entire allowed word to the second U. The two-sided ideal property gives W∈B.
3. Independently join U to itself inside T to obtain V=UeU∈L(T).
4. Both V and W have exactly L_n(T) as their n-factor sets. Every k-word of T extends to an n-word when k≤n, so both have precisely L_k(T) as their k-factor sets. Every short factor of either long word also sits inside some n-factor; endpoint factors are not exceptions.
5. Both words start and end with the same long U. A full k-profile is a length-k factor split after floor(k/2) symbols. Left-truncated and right-truncated profiles depend only on the corresponding first or last k−1 symbols. Since each word has length at least 2k, no profile is truncated at both ends. Therefore their published k-profile **sets** coincide, with no counting assumption.
6. Any LT[k] separator containing L(T) must accept V and hence W, a contradiction.

Padding is necessary: an arbitrary bad word need not have the same profile set as an allowed word. The proof does not omit that step, does not assume the separator is factorial, and does not replace profile equality by factor-set equality alone.

### F. Imported bound and recognition map

The complete DFAs for L(T) and B can be placed on disjoint state sets with block-diagonal letter transitions. The transformation monoid generated by those letters and the identity recognizes both languages by evaluation at their respective initial states. It is finite; a closure computation enumerates it. This is one common morphism A*→M, as required by PRZ. The theorem does not require a minimal monoid, a faithful graph presentation, a semigroup in place of a monoid, or an independent bound depending on alphabet rank. Empty words and the identity element are included.

The published theorem supplies an LT[k] separator with k=4(|M|+1). Taking N=max(2,ell,k) meets the saturation lemma's hypotheses. No off-by-one conversion to another definition of LT[k] is used: the proof directly compares the source's profiles. The unused extra restriction N≥ell is harmless.

### G. Actual decision procedure and witnesses

This criterion is more than a restatement of the original existence question. All its parameters are calculated from the input graph and local rule before the final test.

- Subset construction produces a complete language DFA; the finite buffer/output construction produces a complete bad-word DFA.
- On a disjoint union with d states, at most d^d transformations exist, so enumerating the generated monoid terminates. It may be large; no efficient complexity claim is made.
- Compute N, enumerate the finite set A^N, retain the words accepted by the language DFA, and construct the finite overlap graph.
- The product of this graph with the bad-word DFA has finitely many states. Reachability from every overlap vertex paired with the bad DFA's initial state decides the intersection exactly.
- An accepting state yields a finite bad input witness by predecessor traceback. Strong connectivity extends it to a point of T[N]. Combined with the imported bound and saturation argument, this certifies nonexistence at every radius, not merely failure at this N.
- If no accepting state is reachable, output the finite forbidden list A^N minus L_N(T), together with the completed local rule. These specify T[N] and the desired extension. Onto follows from f(T)=T.

Thus both outcomes terminate and the positive outcome constructively gives the requested SFT and map. The executable packet is explicitly a finite-control suite, not a general-purpose implementation of the enormous universal algorithm.

## Executable and integrity review

The author's original suite replays exactly in isolated ordinary and optimized modes, including direct optimized execution of the mathematical source. Its 3,456 checks and 768 local-rule/domain cases are correctly described as finite controls.

The auditor's independently authored source performs 221,468 checks, including:
- All 144 strongly connected binary-labelled graphs on two vertices, allowing nondeterministic edges
- Canonical orders 2, 3, 4, with language tests on every binary word through length 7, including epsilon and words shorter than n
- 28 identity-obstruction padding constructions and exact published profiles at every scale 1 through n
- All 256 binary width-three local rules: direct bad-language comparisons and two-sided-ideal controls
- Exact self-map and surjectivity checks on the even shift, with 36 bad-word padding controls for valid self-maps
- Periodic irreducible controls, including a one-symbol shift with an unused alphabet letter

The width-three even-shift search finds no non-SFT surjective positive control; this is reported as a bounded observation, not a theorem about larger radii or other shifts. The universal acceptance rests on the written argument plus PRZ, not these experiments.

Tamper controls separately test changed proof, changed results, changed mathematical source, missing files, extra files, malformed manifests, extra directories, empty and populated bytecode directories, raw unlisted bytecode, symlinks, and FIFOs. Clean copies replay from a different working directory. Checks use explicit exceptions, not removable Python assertions. All execution is from source with isolation and bytecode writing disabled. An externally pinned archive or manifest remains the trust anchor: a coordinated adversarial rewrite of all files and metadata is outside an unkeyed local hash manifest's guarantees.

## Publication boundary

This packet contains only authored proof/audit/code/results and public hashes, sizes, titles, URLs, and verification metadata. Source PDFs, source text extracts, screenshots, corpus contents, private notes, and coordination records are excluded. Nothing was committed, pushed, posted, or otherwise published during the audit.

Accepted wording: “Independent audit passed for the complete effective criterion for the prescribed-map problem, using the credited published LT-separation theorem.” Avoid claims of formal verification, human peer review, proved novelty, an efficient implemented general solver, or resolution of the separate existential-over-map problem.
