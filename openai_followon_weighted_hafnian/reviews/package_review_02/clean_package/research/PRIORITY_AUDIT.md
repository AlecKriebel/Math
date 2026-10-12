# Priority and attribution audit

Audit completed: 2026-10-07 05:20 UTC (2026-10-06 22:20 PDT). This is a literature and scope audit, not certification of the unreviewed upstream proof. The mathematics and final package must pass their separate reviews before publication.

## Decision

**There is no defensible novelty claim for converting binary nonnegative rational weighted perfect matchings to simple unweighted perfect matchings, or for obtaining the corresponding FPRAS conditionally on an unweighted general-graph FPRAS.** The logarithmic integer gadget is established machinery. The exact binary rational reduction is also explicitly public. An attributed consequence and implementation note is compatible with the requested framing; a preprint advertised as a new reduction, independent solution of the base conjecture, or first general weighted FPRAS is not.

The audit did not locate an identical public package combining the October 2026 upstream result, this particular Horner implementation, a complete bounded-bit sampler analysis, and the present reproducibility artifacts. This limited observation is **not evidence of first priority**, and does not turn old machinery into a new mathematical result. No previously unresolved statement distinct from the newly available base FPRAS has been established by this project. The defensible contribution is a transparent derivation, implementation, and verification of its weighted consequence.

If independent examination finds that the exact current note and its proof are already public, the user's no-duplicate-publication condition applies. Absence from these searches alone cannot settle that question affirmatively. On the evidence below, the classical reduction is duplicated and must be credited, while the same complete current implementation note has not been identified. This audit therefore permits only the consequence/exposition framing, subject to mathematical and final-package validation; it gives no unconditional publication clearance.

## Exact target and equivalent formulations

For a symmetric matrix of even order with binary nonnegative rational off-diagonal entries, its hafnian is precisely the partition function of perfect matchings of its support, with product edge weights. Diagonal entries never enter. Clearing denominators gives positive integer edge weights on the support and a known scalar factor. A zero hafnian is equivalent to failure of the support to have a perfect matching. Thus rational hafnian approximation, weighted perfect-matching partition-function approximation, and weighted perfect-matching sampling are the relevant formulations; keyword searches only for “hafnian” miss prior reductions stated as `#FugacityWeightedPM`, `#PerfMatch`, Holant, and permanent gadgets.

The central implication is old: an exact polynomial-size reduction with a known positive scalar preserves relative approximation. Exact uniform sampling on a lifted graph pushes forward to its weighted matching law when fiber sizes equal weight products; approximate sampling loses no additional total variation under deterministic pushforward. These are deductions, not new algorithmic breakthroughs. The only newly available algorithmic input here is the upstream all-simple-graphs unweighted FPRAS, if independently valid.

## Priority findings and required credit

| Item | Verified prior disclosure | Consequence for this project |
|---|---|---|
| Positive integer weight removal with logarithmic graph size | Dell–Husfeldt–Wahlén, ECCC TR10-078 (27 April 2010), §3, Fig. 3; expanded Dell–Husfeldt–Marx–Taslaman–Wahlén, arXiv:1206.1775v1 (8 June 2012), §3, Fig. 3 | A binary DAG/path implementation is a realization of established machinery. Directed path gadgets with off-path loops translate to the split-vertex matching form. No “first compact/logarithmic gadget” claim. |
| Uniform binary rational weighted-to-unweighted reduction | McQuillan, arXiv:1301.2880v1 (14 January 2013), §7.2, Lemmas 25–27 | The full exact counting reduction is already explicit, including binary rational input and a simple output graph. Cite this as the strongest directly applicable antecedent. |
| Earlier rational two-terminal gadget | Goldberg–Jerrum, arXiv:cs/0605140v1 (30 May 2006), §4.5, Lemma 7 | Fixed rational weights can be simulated by parallel-edge bundles. Its unary size is not a binary-input bound; do not use it alone to justify the target complexity. McQuillan cites and strengthens this mechanism. |
| Later literature acknowledging the equivalence | Cai–Liu, arXiv:1904.10493v1 (23 April 2019), explanation of Theorem 1.2; ICALP 2020 | Explicitly cites McQuillan Proposition 5 when observing that nonnegative edge weights add no approximation power. This is independent confirmation of the established equivalence. |
| Width-preserving integer gadgets | Curticapean–Marx, SODA 2016, §4, Method 2 | An O(log² W) undirected gadget with pathwidth 2 serves a structural-width purpose and cites Dell et al. It does not imply that our unrestricted O(log W) construction improves prior weight removal. |
| Counting-to-sampling | Jerrum–Valiant–Vazirani (1986), §6, Theorem 6.3 | Classical self-reducibility machinery. Its particular almost-uniform generator definition allows failure; our always-feasible, bounded-bit sampler requires its own quantitative proof or the precisely applicable upstream sampling lemma. |

Detailed statements and bibliography are in [SOURCE_STATEMENTS.md](priority_sources/SOURCE_STATEMENTS.md) and [references.bib](priority_sources/references.bib). Search history and version dates are in [SEARCH_LOG.md](priority_sources/SEARCH_LOG.md).

## The family 113 manuscripts

Pinned input: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The selected source archive and hashes are recorded by the project's `sources/SOURCE_MANIFEST.json`. The source clone was read only. A GitHub main check and a read-only remote-ref check found the same commit; no newer correction was observed and the pin was not changed.

The main manuscript is *A Fully Polynomial Randomized Approximation Scheme for Perfect Matchings in General Graphs*, supplied author **OpenAI**, supplied year **2026**. Its stated applications expressly exclude compressed weights/multiplicities (`build/main.tex`, lines 3126–3127 at the pin). Its deletion sampler lemma begins around lines 3198–3210 and gives TV accuracy with polynomial dependence on the full finite graph encoding and the inverse tolerance. Its source citation metadata must be used, together with the exact commit and file path. The project has not independently invented its base approximation algorithm.

The entropy companion, *Entropy and Face Dimension of the Perfect-Matching Polytope*, is also supplied as OpenAI (2026). Its binary-integer result is a deterministic multiplicative factor $512^n$ approximation with exact zero detection, not a relative-error FPRAS. Its weighted log-partition section proves an entropy/optimization bracket for finite real log weights. Full text, section files, appendices and references were searched; no arbitrary-input relative-error weighted FPRAS or TV sampler was found there. It is relevant comparison and must be cited, but it does not duplicate the claimed FPRAS guarantee by itself.

The filenames and manuscript labels say **23 September 2026**. This is a manuscript date, not established public disclosure. The pinned initial commit has author/committer timestamp **6 October 2026 21:58:50 UTC**. The official OpenAI release announcement is dated **6 October 2026** and announces publication of the repository. The earliest public release evidenced in this audit is therefore **6 October 2026**, not 23 September. A commit timestamp alone does not establish the instant of public visibility. The API response and its retrieval timestamp are preserved in `priority_sources/upstream_main_github_commit.json`.

Source-specific citations are supplied by each preprint's README. For reproducibility, use pinned GitHub paths rather than implying that a moving `main` URL is immutable. Relevant links: [official release](https://openai.com/index/sharing-ai-progress-in-mathematics/), [main manuscript at the pin](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/main.pdf), [entropy companion at the pin](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026/main.pdf).

## Mandatory and current restricted comparators

| Source | Actual restriction and approximation | Why it does not cover the target |
|---|---|---|
| Rudelson–Samorodnitsky–Zeitouni, arXiv:1409.3905v2, Theorems 1.2 and 1.9 (Annals of Probability 2016) | Gaussian determinant estimator; strong expansion, dense degree and/or stochastic scaling hypotheses; high-probability sublinear logarithmic error bounds | Gives subexponential multiplicative factors under structural hypotheses, not arbitrary relative epsilon accuracy on all binary rational supports. |
| Barvinok, arXiv:1601.07518v5, Theorem 2.1 (Discrete Analysis 2017:2) | Entries in a fixed interval [d,1], d>0; approximates log hafnian within epsilon; quasi-polynomial time $n^{O_d(\log n-\log\epsilon)}$ | Fixed bounded ratio and no arbitrary support zeros; not an FPRAS in the unrestricted input bit model. |
| Yi, arXiv:2609.04079v1, Theorem 1.1(a), Corollary 1.3 | Fixed gamma>0 and theta>0; positive entries in [theta,1], support minimum degree at least (1/2+gamma)n; deterministic exp(±epsilon) approximation with polynomial bit time for fixed parameters | A recent restricted FPTAS. Sparse supports and input-dependent very small positive entries are outside its theorem. |

No signed/complex hafnian or unrestricted Gaussian-boson-sampling claim follows from the nonnegative reduction. The comparator results are independently public prior art, not certified here by checking their complete proofs. The exact statements actually used for comparison were inspected.

## Historically unresolved statement and present status

Qi Ge's 2011 thesis, Question 7.6 (printed p. 147), asks about an FPRAS for positive-weight perfect matchings in general graphs and contrasts the bipartite result. This records historical problem provenance. It does not establish that this question remained independently unresolved after a general unweighted FPRAS became available: the exact weighted-to-unweighted equivalence was public well before this project.

The strongest justified description is: **a self-contained weighted consequence of the OpenAI unweighted theorem, with established weight-removal and sampling mechanisms credited, plus transparent implementation and checks.** In particular, the paper should state that the general weighted consequence already follows from the previously established reduction once the cited unweighted theorem is accepted. An exact newly released theorem is a new available premise; applying an old equivalence to it does not establish separate priority for the weighted theorem.

Recommended title/abstract language is “an exact reduction and sampling consequence” or “implementing the weighted consequence”; avoid “we solve the conjecture,” “we introduce logarithmic weight removal,” “the first FPRAS,” and claiming conventional peer review. The Horner realization, explicit constants, boundary-case coverage and bounded-bit implementation can be accurately described as this note's presentation/artifacts. They must not be described as new mathematical mechanisms without further independent evidence.

## Audit coverage and remaining conditions

Completed: primary-source comparison for both mandatory arXiv papers; current September 2026 comparator; citation chains for binary rational reduction; exact integer gadget antecedents; JVV sampler scope; family 113 companion inspection; supplied source citation metadata; source pin/correction check; public-versus-manuscript chronology; equivalent formulations.

Limits: searches cannot prove universal absence of an identical note; the source release is extremely recent; public indexing can lag; no external individuals were contacted. The upstream proof's soundness, local construction proof, always-terminating sampler, artifact correctness, and final package claims are separate conditions checked by the other project reviewers. A later source correction or discovered duplicate requires reopening the corresponding gate.

Local priority audit completion estimate: 100% of the assigned audit scope, with the explicit epistemic limits above. Overall mathematical-resolution and publication-package percentages belong in the root research log and are not inferred from a favorable priority review.

## Evidence custody

The small owned Markdown/BibTeX/JSON notes are publication-safe evidence. Downloaded third-party PDFs and extracted text in `priority_sources` are local reading copies; they are **not part of the publication payload** absent redistribution rights. `DOWNLOAD_MANIFEST.json` records checked URLs, content hashes and retrieval times. Expendable figure renders were removed after the shared disk became full; the underlying PDFs/text and inspected statement notes remain. No source clone, branch, index, commit or external correspondence was modified by this audit agent.
