# A negative answer to the random generalized-lattice moment comparison

Problem 30000052 / OWR-723-005 is **resolved negatively**, with a complete standalone elementary proof accepted by a separately tasked independent internal AI-assisted mathematical audit.

At n = 3, d = 1, p = 4, independently continuous uniform generator and shift give expected normalized anchored fourth moment 19/1620, exceeding the iid value 4/405 = 16/1620. The strict excess is 1/540 and the ratio is 19/16. A second standalone geometric argument gives, at n = 4, lattice moment at least 2/315 > 11/1920 iid, with lower-bound margin 5/8064.

The proof retains all-n,d second-moment equality (2^(-d)-3^(-d))/n and all-dimension equality of ensemble laws for n <= 2. Thus three is the smallest possible point count for a counterexample. All points are indexed and weighted by 1/n; collisions and endpoint conventions are null-set issues, not conditioning events.

## Complete authored documents

- [PROOF.md](PROOF.md): full accepted elementary proof, with only eight inline-TeX delimiter repairs
- [AUDIT.md](AUDIT.md): full substantive independent mathematical reconstruction, hidden-assumption checks, exact recomputation reasoning and acceptance scope
- [ACCEPTANCE.md](ACCEPTANCE.md): accepted full-negative decision and review limitations
- [ACCEPTANCE.json](ACCEPTANCE.json): precise accepted scope and distinct original/distributed document identities
- [STATUS.json](STATUS.json): accepted internal-audit status and exact scope
- [VERIFICATION.md](VERIFICATION.md): authored analytic explanation of the supplementary chamber calculation
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): attribution and bounded literature/retrieval review
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source PDF identity, inspection history and verification summaries
- [MANIFEST.json](MANIFEST.json): exact ten-file inventory, hashing the other nine members

## Attribution and limitations

The original question is Erich Novak's *New bounds for the star discrepancy*, reporting joint work with Aicke Hinrichs, in *Discrepancy Theory and Its Applications*, Oberwolfach Report 13/2004, printed pp. 696–699, especially pp. 697–698: https://doi.org/10.4171/OWR/2004/13.

The manuscript, audit and edition are AI-assisted and unrefereed. Internal mathematical acceptance is not external human peer review, journal acceptance or proof-assistant certification. No novelty or priority is claimed. The literature review is bounded; lack of a located earlier resolution is not exhaustive status clearance.

The result concerns the expectation of the p-th power under the displayed continuous-generator average. It does not settle the expectation of the norm rather than its p-th power, refute the existence of well-chosen lattice generators, or answer the separate existence/upper-bound problem. The exact n = 4 value 139/17280 in the audit is supplementary: the geometric bound already proves failure.

Every proof argument and all substantive independent audit reasoning are retained. The original audited files remain unchanged and have identities distinct from this edition. Wrapper edits remove private accounting and update acceptance/formatting status; the audit's norm-versus-p-th-power wording is clarified explicitly. Programs, raw outputs, generated certificates, datasets, copied source documents/text/images and private coordination material are excluded. The accepted proof stands without omitted software.

Preparation rechecked frozen identities and replayed the independent exact calculation in normal, -O and -OO Python, without new scholarly retrieval, source-text inspection or literature research. QUEUE.md and unrelated repository content are unchanged. No merge, release, DOI, journal submission or outreach is implied.
