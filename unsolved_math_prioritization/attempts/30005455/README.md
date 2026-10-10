# Finite WARM: sharp forest threshold and a whisker improvement

Problem 30005455 / OWR-12697708-008. The bundled two-clause target remains **OPEN**.

For a finite simple undirected loopless graph, unit initial edge counts and arbitrary positive vertex firing rates, [Theorem A](PROOF.md) proves almost-sure forest support for alpha>4/3. Its cycle-specific statement excludes even cycles for every alpha>1 and odd m-cycles for alpha>sec^2(pi/(2m)), including nonuniform weights, unequal rates, chords and attachments. The known equal-rate triangle is strictly stable and positively attainable for 1<alpha<4/3, establishing the sharp lower obstruction. No stochastic claim is made at alpha=4/3.

For equal positive rates, [Theorem C](PROOF.md) improves the prior >25 bound to alpha>=17/4: surviving components are trees of diameter at most three. The entire finite algebra is written out, including the five closed exponent intervals, exact rational margins, fractional-power comparisons and the analytic tail. No omitted generated certificate or program is needed.

The equal-rate whisker assertion for 4/3<alpha<17/4 remains unresolved. The exact, strictly stable unequal-rate diameter-four path at alpha=2 is a scope control, outside that equal-rate assertion. It is not a counterexample to the unresolved target. No infinite-graph or loop/multigraph extension is claimed.

## Included documents

- [PROOF.md](PROOF.md): complete accepted mathematical manuscript, with only the opening problem-label sentence edited
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): all independent reconstruction, exact controls, scope and limitations
- [ACCEPTANCE.json](ACCEPTANCE.json): accepted claims and exact distributed proof/audit/source-review identities
- [STATUS.json](STATUS.json): precise partial result and remaining OPEN interval
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): primary attribution, imported theorem and bounded historical status
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source PDF hashes/sizes, retrieval/inspection history and supplementary verification summary
- [MANIFEST.json](MANIFEST.json): exact eight-file inventory, hashing the other seven members

## Credit and review limits

Hirsch, Holmes and Kleptsyn's published 2023 Theorem 1 and Proposition 1 supply the stochastic convergence, strict-stability attainability and support bridge. They are imported, not re-proved. Holmes and Kleptsyn's 2017 work supplies the prior bounds, the credited least-weight argument and the known unequal-rate warning. Oberwolfach Reports 12/2023 states the original two questions and the triangle obstruction. Full public citations and source locators are retained in the proof and source review.

The manuscript and audit are AI-assisted and unrefereed. Mathematical acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. No novelty or priority is claimed; the bounded historical source search is not exhaustive literature clearance.

Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. Historical finite computations are supplementary. Publication preparation rechecked frozen input bytes, editorial preservation and local publication integrity; it did not rerun the original mathematical programs, retrieve new scholarly sources or conduct a new literature search. QUEUE.md and unrelated repository content are unchanged. No merge, release, DOI, journal submission or outreach is implied.
