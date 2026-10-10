# Source and prior-attempt gate

Checked 4 October 2026 UTC. Rank 567, numeric ID 2302073, code AMR-022-2073.

## Exact target

The requested [catalogue page](https://www.unsolvedmath.com/problems/2302073) could not be opened with the web reader; direct HTTP returned 403. The independently public [UnsolvedMath dataset](https://huggingface.co/datasets/ulamai/UnsolvedMath) supplied the matching numerical and problem-code record. The generated catalogue classification and summary were treated as untrusted discovery aids.

The original question and its complete update were checked in Walter K. Hayman and Eleanor F. Lingham, [*Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed pp. 50–51, PDF pp. 51–52. Both pages were rendered and visually inspected. The question is exactly existence of a jointly entire F with a normal family of z-slices but no entire factorization F(z,a,b)=G(z,H(a,b)). It explicitly asks for genuine two-parameter dependence and states the necessary differential identity for factorization. Update 2.73 reports no communicated progress as of that edition. That historical reporting statement is not a current openness certificate.

The record does not bundle another question or restrict the z-slices to transcendental functions. In particular an affine-in-z construction is admissible. Normality is spherical, allowing the identically infinite limit. No finite-only normality claim is made.

## Prior report and duplicate checks

The selected report in the public research-results corpus, keyed `AMR-022-2073`, was read in full. It says only that the statement was read, a web search found nothing, and the question was treated as open based on the 2018 edition. It contains no mathematical proof attempt or claimed result. The matching catalogue summary says the same. The March 2026 source below supersedes that assessment; the old report is not a mathematical dependency.

The pinned research corpus was checked at revision `372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`. Its complete download was parsed in memory to select the exact record, including its dictionary key; only the selected report and provenance were retained locally. Public files contain neither the report nor the corpus. Checksums and sizes are recorded in SOURCE_MANIFEST.json.

Actual repository checks were made against [AlecKriebel/Math](https://github.com/AlecKriebel/Math), rather than inferring lack of prior work from a queue label:

- The queue row was read and showed rank 567, `queued`, `0/5`, with the matching ID and title.
- All-state PR searches for `2302073` and `2.73` returned no match. A broader `Rubel` search returned PRs 369, 493, 495 and 502, concerning different source questions, and their returned descriptions were inspected.
- Default-branch code searches for `2302073` and `AMR-022-2073` returned no matches. These searches are not assumed exhaustive, particularly because even the known queue row did not appear.
- ID-based branch and commit searches returned no matches; the branch search had no continuation cursor.
- The actual repository root listing was inspected. The recursive `problems/` tree `8f72e77ed517ba2424b4e74b324cda525e6373c3` had 652 entries, `truncated=false`, and no matching ID or two-parameter-normal-family path.
- The actual `unsolved_math_prioritization/attempts` directory listing had 54 entries and no target-ID entry. Two requests for its recursive Git tree failed with a transport-closed error; the successful directory read is the evidence used here.
- `review_v2/related_target_groups.json` was read and contained no occurrence of the target ID or code. No related-group correction is inferred.
- Repository AGENTS.md, the prioritization AGENTS.md and its README were read. The current task's narrower requirements govern disposition and publication: one draft PR only after independent review, no queue.py invocation, no merge, release or external outreach.

These bounded successful checks found no previous repository attempt for this exact target. Untagged or unindexed work cannot be ruled out. There were no remote writes during authoring.

## Current primary resolution and full proof inspection

**Yixin He, Quanyu Tang and Teng Zhang**, [*A Solution to a Problem of Rubel on Two-Parameter Normal Families of Entire Functions*, arXiv:2603.20883v1](https://arxiv.org/abs/2603.20883v1), submitted 21 March 2026. The primary arXiv record and complete ten-page manuscript were read. Theorem 1.2 exactly answers the original existence question affirmatively. Proposition 2.3, Lemma 3.1 and the entire Section 4 proof were checked, including all trapping inequalities, subsequence alternatives, and the sign of the Jacobian obstruction.

This source uses the attracting basin of f(x,y)=(y,(y²−x)/2), a linear coordinate swap/scale and a quadratic shear. The resulting coefficient domain supports a normal family of affine functions and an entire nondegenerate parametrization. These ideas and the affirmative resolution are credited to the authors, without any claim of rediscovery priority. The complete source proof has no apparent unresolved step in this reading. A fresh independent audit of our reconstruction is still required.

The arXiv record retrieved on 4 October 2026 lists version 1 and no journal reference. Searches for the exact title and identifier did not locate a correction or withdrawal. This is a bounded source-status check, not an assurance of exhaustive literature coverage or of human peer review.

**Jean-Pierre Rosay and Walter Rudin**, *Holomorphic maps from C^n to C^n*, Transactions of the American Mathematical Society 310 (1988), 47–86, [DOI](https://doi.org/10.1090/S0002-9947-1988-0929658-4), [primary paper reading copy](https://www.math.stonybrook.edu/~ebedford/PapersForM655/RosayRudin.pdf). The attracting-basin theorem on printed p.49, the complete special-case Theorem 9.1 and proof on pp.73–74, and the complete Appendix on pp.80–86 were read. The specific automorphism here meets the special theorem's spectral inequality: all eigenvalues have modulus 1/√2, so their squared modulus 1/2 is smaller than 1/√2.

PROOF.md supplies the full specialized normalized-iterate argument directly. Its contraction constants are 3/4 and 3/2, giving the summable ratio 27/32. It explicitly proves well-defined global continuation, injectivity, surjectivity and holomorphic inversion; it does not rely on the generally false claim that normalized iterates always converge for every attracting automorphism. The constant Jacobian normalization is classical and is also recorded by Rosay–Rudin Theorem 9.1.

## Disposition and publication boundary

Recommended status: `already_solved`, `1/5`, after a single substantive source-verification/reconstruction turn. The exact original existence question is settled by the prior affirmative construction. Five fresh attempts are unnecessary once that complete prior resolution has been located and verified.

The public packet contains authored mathematical exposition, bibliographic/source-gate notes, a timestamped log, explicit status, an exact supplementary verifier and integrity files. It excludes downloaded papers, rendered pages, extracted source text, dataset rows/corpora, operational receipts and private context. No first-resolution or novel-result claim is authorized. A queue update should change only this row's Status and Turns cells by default and leave all unrelated bytes untouched.
