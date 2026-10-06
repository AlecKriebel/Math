# Final independent adversarial priority report: Conjecture 1 / PR311

Finalized: 2026-10-04T17:17:34.397970+00:00. Approach family: exponential-family boundary/support geometry and hypothesis-preserving theorem specialization.

## Verdict and bounded recommendation

The released proof supports the exact source-literal closure conclusion, including zeros, finite real original-edge factors, normalization, global Markov semantics, isolates, and empty cases. I found no proof defect in the released TURN_2 or the allowed alternative derivation. No inspected prior body states the full all-support Conjecture 1 or TURN_2's stronger equality F_2(G)=closure A(G).

There is nevertheless substantial and previously omitted primary overlap: Kahle–Sullivant (2024), Theorem 5.5, already proves factorization for factorizing limits with natural lattice support. Its Proposition 4.1 and Lemma 5.4 give the cover-edge mechanism. The full original-edge closure assertion has a short, independently derived extension using facial-support geometry and deterministic equality classes. Calling it simply a new solution of an untouched 2022 problem without this comparison would misstate the inspected history. Calling it an already-published full theorem would also exceed the evidence.

Recommendation: retain the mathematically correct closure result and the stronger attractive-approximation characterization in a revised, fully attributed research note; hold any claim of historical novelty, first resolution, or immutable result snapshot. The note should identify the exact extension beyond natural supports and separately state the stronger characterization. The closure result alone has a modest contribution profile because its residual bridge is short and elementary; the stronger zero-permitting characterization is a better candidate contribution. Its historical priority remains unresolved within the bounded search. This is a recommendation about framing and promotion, not authorization to publish or make a release.

## Independence and access gates

Original PDF independently fetched and visually read printed3125–3127 before candidate access. Frozen criteria: 2026-10-04T16:59:16.924019Z, SHA256 5e986af08048e9bc8c9e052b2d8666c468fd000c0b3a657133c26f9d5eee04af, mode0444.
First independent historical conclusion: 2026-10-04T17:04:59.442846Z, SHA256 f2218f1f3e4f55b382cccd96973bcbb8ee81e958ac90e615591b6193da581e4a, mode0444. This early conclusion remains unchanged; later evidence added the KS2024 overlap.
Independent facial-support bridge: 2026-10-04T17:07:57.136397Z, SHA256 a60b708fa9a4481c44670d177e516bc6d49bbb207644ebe59fabe2689d7816a8, mode0444. It was developed and frozen while candidate-blind.
KS2024 was independently retrieved at 2026-10-04T17:09:04.413252Z and its relevant full bodies read before candidate access.
Named release gate from root: 2026-10-04T17:10:32.826356Z. Actual five allowed full reads: 2026-10-04T17:11:07.246203Z through .247265Z. Exact paths, hashes, modes, sizes are retained in streams/released_candidate_inputs.json. Only TURN_1.md, TURN_2.md, SOURCE_GATE.md, SOURCE_RECHECK_2.md, and lattice_factorization/ALTERNATIVE_SUPPORT_CLOSURE_DERIVATION.md were read. No other candidate code, root/sibling reports, or inherited reports were read. No Git/index/queue/main-history mutation, outreach, other-chat messaging, or publishing occurred.

## Exact prior comparison

| Source/body location | Prior result actually read | What it does and does not discharge |
|---|---|---|
| [GMS2006](https://arxiv.org/abs/math/0608054), Theorems3.1–3.2, PDFpp8–9; Appendix LemmaA.2, pp29–30 | Nonnegative monomial image is toric membership plus A-feasible support; toric membership describes completion; completion support is facial | Applies exactly to original-edge configuration indicators. Supplies finite values once support feasibility is proved. Does not by itself make lattice supports feasible. |
| [LUZ2021](https://web.math.ku.dk/~lauritzen/papers/AOS2007.pdf), Theorem3.2 p1438, Proposition3.6 p1440, Lemma4.9 p1449 | Canonical MTP2 cone; positive quadratic coupling sign condition; all-pair support reconstruction | Parameter closedness permits parameters to diverge. All-pair reconstruction requires a further original-edge reduction. |
| [Fallat et al.2017](https://research.chalmers.se/publication/251020/file/251020_Fulltext.pdf), Theorem7.5 p1173 | Positive edge potentials yield MTP2 iff each potential is MTP2 | Explicit positivity excludes boundary zero cells. TURN_2's aggregation over equality classes is additional work. |
| [KS2024](https://arxiv.org/abs/2411.03139v1), Definition2.4 p3; Proposition4.1 pp5–6; Lemma5.4/Theorem5.5 p7 | Natural lattice support makes cover relations appear as graph edges; natural-support limits factor over maximal cliques | Natural means empty/full support extremes and rank=cardinality. Equality blocks and pins are excluded. Its support argument uses only pair covers, so it specializes to the original-edge indicator design. Full all-support closure is not its literal statement. |
| [KZ2004](https://www.cs.cornell.edu/~rdz/Papers/KZ-PAMI04.pdf), Theorem4.1/Section4.1 pp150–151; [PQ1979](https://publications.polymtl.ca/5993/1/EP-R-79-15_Picard.pdf), TheoremI reportp4/PDFp9 | Submodular binary pairwise energies use no auxiliary variable vertices; all minimizing cuts obey residual implications | Gives a routine prior ground-state support result. Does not establish that every arbitrary MTP2 edge law has positive attractive approximants. |
| [KR2007](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/01/PAMI07-QPBO.pdf), Section2.1–2.2 manuscriptpp5–7 | Nonnegative normal form and residual-capacity energy reparameterization | TURN_2 Section4's finite max-flow mechanism is classical. Exponentiating its nonnegative costs and ensuring a shared maximizing assignment gives the compact normalized deduction. That deduction is a short application, not a new flow theorem. |

KS current arXiv listing inspected on the audit date shows v1 submitted 5November2024, and the body is dated 6November2024. The author's publication page lists the paper as to appear in Proceedings of the AMS (2025). The priority conclusion uses the actual 2024 body, not the publication-page title or journal status.

## Full hypothesis-preserving closure derivation and its novelty boundary

This derivation was independently completed before release and is in public/independent_boundary_bridge.md. It is not copied from the released alternative.

1. For E nonempty let A have four indicator rows per original edge. Any real-factor p_n can be represented by absolute-value factors without changing it, because p_n is nonnegative. Thus p_n belongs to the nonnegative monomial image for exactly that A. Continuous binomials put the limit p in X_A.
2. S=supp(p) is a Boolean sublattice by MTP2. GMS LemmaA.2 makes it a facial support: a finite energy H(x)=c dot A_x is zero exactly on S and strictly positive outside. H contains only original-edge pair terms; no submodularity is required.
3. Delete pins and identify coordinates forced equal in S. Boolean-lattice reconstruction (equivalently apply LUZ Lemma4.9 to the uniform law on S) represents S by the downsets of the quotient poset. This reduction is standard, but naturality now holds only on quotient coordinates.
4. Every equality class C is connected in G: choose two support states differing exactly in C. If C splits into D,F without a cross edge, the pairwise form gives H(10)+H(01)=H(00)+H(11)=0 under the common exterior. Nonnegativity forces split zero-energy states, contradicting deterministic equality. This is an elementary additional lemma not stated in the inspected KS body.
5. Every quotient cover C<D has some original cross edge. The cover context I=downarrow D minus {C,D} makes class patterns 00,10,11 feasible and 01 forbidden. Without a cross edge H(01)=H(00)+H(11)-H(10)=0, contradiction. For singleton classes this is the same cover-square mechanism as KS Proposition4.1. Extending it to blocks uses the facial pairwise energy.
6. Connected equality edges enforce each block. An edge for each quotient cover enforces its implication. Nonisolated pins are encoded in incident edges. Isolates cannot be pinned or related by a facial original-edge energy. Hence S is exactly the intersection of its original-edge projection cylinders, which is A-feasibility.
7. GMS Theorem3.1 gives finite nonnegative original-edge factors reproducing p exactly. Closed simplex, MTP2 inequalities, and polynomial global CI relations preserve normalization and membership in M_2.
8. E empty,V nonempty gives an empty literal factorizing family, hence vacuous closure. V empty gives the sole law. For E nonempty, literal isolates remain independent uniform coordinates; scalar normalization is absorbed into an existing edge.

Classification: prior explicit ingredients plus an unstated elementary support bridge give a short full corollary/extension. This is not a routine specialization of Theorem5.5 alone, because equality-class connectivity and original-edge lifting are missing from its stated hypotheses. Nor is it evidence of a major new method: the proof is brief after the correct facial-lattice formulation is identified. Whether this extension meets the research program's novelty bar is a contribution judgment, distinct from historical absence.

## Stronger released characterization

TURN_2 states F_2(G)=closure A(G), with unary factors allowed. Its Section2 starts from actual factorization, so original-edge support reconstruction is already available. Section3 removes comparable-class pair interactions into unary terms and aggregates coefficients between equality blocks. The four-upper-set square makes each remaining incomparable-class aggregate nonnegative. The implication/pin penalties then give positive ferromagnetic approximants on ORIGINAL edges. This supplies the precise positive-approximation bridge that was missing from the inspected positive-only statements.

The same argument also yields an explicit finite factorization with MTP2 edge factors: multiply exp(L) by the implication/equality support indicators and unary pins. Each indicator is MTP2, and the nonnegative couplings in L give MTP2 edge factors. This observation is a deduction from the released proof, not a new independently certified historical theorem.

The reverse inclusion follows using the classical residual reparameterization and compact parameters with an unnormalized maximizing weight equal to1. The lower bound Z>=1 is essential; naive factorwise compactness without it would be invalid. All limiting factors are finite in [0,1], so zeros cause no divergent-factor claim. The source-literal isolate and empty conventions are explicitly reduced in TURN_2 Section6.

Classification: the zero-permitting aggregation/attractive approximation is a mathematically distinct bridge beyond the inspected prior statements and beyond KS natural-support closure. I did not locate an equivalent prior full theorem. The flow mechanism and the final compactness inference are classical/application components. A claim that the stronger equality is already published would require an exact additional body theorem, which this audit does not have. A claim of historical novelty would likewise exceed this bounded search.

## Boundary stress tests and related overlap

- Natural-support test: on a triangle, any natural lattice limit support has implication zeros on original edges by KS's covers, while GMS supplies pair-factor values using the ORIGINAL-edge design. No clique-to-edge value reduction is silently assumed.
- Equality/pin test: on edges12,23,14 with an additional isolated vertex5, take support x1=x2, x3<=x2, x4=1, x5 free. This is an unnatural sublattice. Equality edge12, implication edge23 and pin on edge14 reproduce all support zeros with finite factors; vertex5 stays unrestricted and literal uniform. The facial bridge preserves exactly these features, which KS Definition2.4 excludes on original coordinates.
- Failed shortcut: a lattice support plus global Markov does not imply pairwise weight factorization. KS Example6.5 uses the C4 equality support {empty,12,3,4,34,123,124,1234} and violates a toric quartic. Its stated weights (bottom mass1/2, remaining seven1/14) are themselves MTP2: log weights differ by a positive multiple of the bottom indicator, a supermodular function on the three-block cube. Thus the candidate TURN_1 top-boost counterexample lies in an already-published structural family, with a changed boost ratio and order reversal. It is outside completion and cannot refute Conjecture1. This overlap is material to the bundled publication framing, although the assigned verdict is about closure.
- Positive-only shortcut: positive canonical cone closedness does not bound h,J in a sequence, so it cannot replace the support bridge.
- Clique shortcut: Theorem5.5's clique conclusion alone does not imply original-edge factors on triangles or larger cliques. The proof's cover-edge support construction and GMS original-edge design are what make the specialization exact.

## Search scope, body-read scope, and audit limits

Thirteen dated web batches are retained as exact query arguments and full result streams in streams/web_results_01.json through web_results_13.json. Query families included source conjecture names, MTP2/Ising closure, boundary/support factorization, facial sublattices, binary submodular ground states, graph-cut reparameterization, and log-supermodular zero-potential factorization. The first batch's exact query arguments are separately in web_queries_01.json. Search results merely identified candidate sources; every mathematical overlap above was checked against primary body text. No titles/abstracts/metadata alone are treated as theorem evidence. Secondary summaries only served as search leads.

Private original bodies, text extraction, retrieval headers, executable command arguments, full retrieval streams, selected body-read streams, and visual render commands are retained in private_sources/, streams/, and tmp/pdfs/. Copyrighted bodies are not in public/. Exact body-read scope:

- Original: visually full printed3125–3127.
- LUZ2021: textSections3.1–3.3,4.3–4.4,5/5.1 and relevant references; visually pp1438,1439,1449. Scope does not assert reading all24pages.
- GMS2006: textdefinitions/modelmatrix,Theorems3.1–3.2 and Appendix proofs; visually PDFpp8–9. Relevant exact proofs retained in selected streams; not a full-paper read.
- Fallat2017: textSection7.3–7.5 surroundings; visually printed1173.
- KZ2004: visually full printed150–151, including Theorem4.1 and its no-auxiliary construction.
- PQ1979: source theorem/proof visually read reportp4/PDFp9; web extraction also covered definitions/propositions nearby. OCR errors are resolved by the visual page.
- KS2024: textSections1–2,4–5,6.5; visually PDFpp3,5,7,13. The natural restriction and theorem are actually body-read. Theorem6.1 body statement/proof was inspected in extracted search scope, but it is not needed for the closure deduction.
- KR2007: textSection2.1–2.2 manuscriptpp5–7, including normal form, source/sink network and flow reparameterization; page6–7 renders retained.

No exhaustive database review or universal negative historical certificate is claimed. No candidate code was read or run. This audit verifies prose deductions, exact source specialization, and boundary cases; finite implementation reproducibility is outside its released input scope. Nothing here approves external publication.

## Strongest result and exact remaining gap

Strongest verified result: exact finite-binary original-edge closure has two consistent prose proofs and a separately frozen candidate-blind facial-support derivation; the stronger attractive-approximation characterization has a checkable zero-case bridge beyond inspected positive-only statements. Exact remaining gap: historical priority of the all-support extension and stronger characterization, and whether their modest/stronger respective contributions meet the intended publication novelty standard. That gap is not a mathematical closure gap.

Completion estimate:100% of this bounded independent priority audit; mathematical correctness substantially supported, historical absence deliberately unverified.
