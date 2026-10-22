# Independent source and identity review

Inspection date: 2026-10-05 UTC. This is a bounded audit record.

## Frozen identity and full local corpus verification

The original 20,203-byte author archive and every file in its manifest were rehashed, matching the recorded freeze identity. No author file was modified. The independent source identity check read and hashed all bytes of the three complete local corpus files, then parsed their complete JSON structures:

- catalog.json: 21,735,099 bytes; 15,458 records
- problems.json: 68,931,837 bytes; 15,458 records
- research_results.json: 80,334,822 bytes; 6,701 records

Their SHA-256 values agree exactly with the author's public metadata; they are recorded in PUBLIC_METADATA.json. There is exactly one problem with numeric ID 30006060 and exactly one record with problem number OWR-14298592-014. The catalog rank is 804. Rank is queue metadata, not mathematical evidence.

The UTF-8 statement hash is `3c062a84a1760d6c102cd840c55082a885e929feff4841eb7a6a4987f3b80043`, matching the catalog.

The research corpus has no key for this problem number. The prescribed empty-object fallback therefore applies. Independently hashing Python's default sorted-key JSON serialization of [problem, {}] gives review hash `974c2823b16c272d74df92feabb871ed7f4dcf3bcb5f2e0d84a990d348a14760`, matching the catalog. A missing separate research entry is not evidence of an earlier proof attempt or evidence that no earlier proof exists. The supplied problem's dated literature-triage prose was read but not treated as a proof or current status certification. No source record or dataset content is included in this package.

## Scholarly sources inspected

All ten source PDFs listed by the author were rehashed and their PDF magic checked, matching the listed byte counts and hashes. The audit independently read each load-bearing statement and checked its hypotheses. Full PDF byte identity does not mean every line of every paper was reviewed. PUBLIC_METADATA.json records the exact file identities and scopes.

1. [Oberwolfach Report 43/2024](https://ems.press/content/serial-article-files/50050), DOI 10.4171/OWR/2024/43: the complete relevant contribution, printed pages 2543–2546, including references. The two words on page 2545 were visually inspected. A fresh web request to the publisher route without the query string succeeded. The query-string route timed out; a web screenshot request had a cache miss. The existing matching local PDF supplied the successful visual inspection. The workshop dates are September 22–27, 2024; the report's publication is 2025.
2. [Collins, Seifert-matrix algorithm](https://webhomes.maths.ed.ac.uk/~v1ranick/julia/SeifertMatrix.pdf): corrected July 30, 2013 manuscript; Sections 3.1–3.3 and local diagrams on printed pages 11–12. Local rendering was inspected. A fresh web PDF read also succeeded.
3. [Baader, Positive braids of maximal signature](https://ems.press/content/serial-article-files/44257?nt=1): Section 2's surface/basis/linking-tree description. Its signature convention is opposite to the convention used in the packet; the trefoil calibration and global sign were checked.
4. [Truöl, The upsilon invariant at 1 of 3-braid knots, v2](https://arxiv.org/abs/2108.03674v2): Proposition 3.2(C), Lemma 4.11, positive-braid tau/genus discussion, and minimal-block corollary. All inequalities on the block exponents and the knot hypothesis hold for both inputs.
5. [Baker, A note on the concordance of fibered knots](https://arxiv.org/abs/1409.7646): revised manuscript, Lemma 2, Theorem 3 and proof, including its homotopy-ribbon definition. No smooth nonsliceness conclusion is asserted.
6. [Ozsváth–Stipsicz–Szabó, Concordance homomorphisms from knot Floer homology, v3](https://arxiv.org/abs/1407.1795v3): initial slope, Theorem 1.14, and the L-space discussion in Section 2.
7. [Conway, The Levine–Tristram signature: a survey](https://arxiv.org/abs/1903.04477): Section 2.4 and its precise concordance-invariance qualification. The inspected PDF is the actual arXiv PDF, not the author's failed HTML download.
8. [Rasmussen, Khovanov homology and the slice genus](https://arxiv.org/abs/math/0402131): Theorem 4 and the positive-knot argument in Section 5.2.
9. [Cheng–Hedden, Knot Floer homology of positive braids, v2](https://arxiv.org/abs/2504.13005v2): July 14, 2026 version; abstract, Theorem 1.1 and surrounding scope. It is not a full filtered-complex determination.
10. [Borodzik–Truöl, Non-complex cobordisms between quasipositive knots, v3](https://arxiv.org/abs/2504.04894v3): December 24, 2025 accepted version; Proposition 1.3, Question 1.5 and the explicit nonfibered qualification.

The independent proof uses the standard Burau formula, Seifert-form Alexander polynomial, genus-degree bound, Fox–Milnor condition, Arf/determinant rule, and branched-double-cover presentation/linking form as established background, not original theorems proved by the verifier.

The [requested problem page](https://www.unsolvedmath.com/problems/30006060) was attempted again but was not accessible through the web tool. Its current live contents were not certified.

## Bounded current-literature check

Fresh web checks visited [Truöl's research page](https://paulatruoel.github.io/research.html), the versioned Truöl, Baker, Conway, Ozsváth–Stipsicz–Szabó, Rasmussen, Cheng–Hedden and Borodzik–Truöl arXiv records, and the publisher reports. Targeted searches included the positive-three-braid concordance topic, the explicit exponent pattern and numeric target. Returned related publications and presentations supplied no resolution of this particular pair. Irrelevant numeric-ID search hits were discarded. This is a negative search result with bounded coverage, not proof of historical openness or originality.

## Independent bounded prior-artifact check

Fresh read-only connector searches were run in [AlecKriebel/Math](https://github.com/AlecKriebel/Math):

- default-branch code search: 30006060 and concordance, no returned results
- all-state PR search: 30006060 and exact report label, no returned results
- commit search: 30006060, no returned results
- branch search: 30006060 and concordance, no returned results
- braid branch search: both pages inspected through terminal cursor; four unrelated surface-braid / braided-Thompson branches
- broader all-state positive-braid PR search: one unrelated positive-link signature bound, [PR #266](https://github.com/AlecKriebel/Math/pull/266)

No actual previous target artifact was located within this scope. Generic catalog presence or literature triage was not counted as mathematical work. This audit did not inspect every unrelated branch, recover all historical branch contents, or reattempt a full recursive tree traversal. It does not inherit an exhaustive search claim from the author. There were no repository writes, comments, publication, or third-party outreach.

## Package boundary

This audit package contains authored proof/review text, authored computation and correction code, calculated certificates and public verification metadata. It contains no third-party PDFs, text extracts, screenshots, raw source corpora, private sources or private coordination. The source files remain outside the package. No publication or remote mutation was performed by this audit.
