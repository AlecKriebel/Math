# Fresh PR14 source-integrity and priority challenge

**Verdict: PASS for this challenge, with explicit scope qualifications. No mandatory repair found.** This is an independent source/attribution and artifact-integrity determination, not a mathematical certification based on older reviews. The parent agent's independently recorded mathematical conclusion was neither modified nor used as evidence.

The reviewed objects are original PR14 head `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`, its frozen `source_snapshot/`, and the current `reviewed_candidate/` manifest SHA-256 `1c73083e7d1a0df3c4ff45c31cb98ca1546e58f6d73e139ecb74598a2ca8d064`. The family manifest SHA-256 is `b873942e9a21d3fcc9153d0e5ee51561c952dd5b47306b8b1f56b75576314f10`. These hashes bound the verdict. Any subsequent modification requires reconciliation.

## 1. Exact original and current artifact identities

`verify_integrity.py` read the original Git objects directly. All 12 frozen source files match the actual original-head bytes, SHA-256, Git blob SHA-1, mode, and length. The source path sets match exactly, and the original base-to-head changed-path list matches the 13 entries in `snapshot_manifest.json`. This includes the historical queue change; the captured old PR-body statement about an unchanged queue is therefore historical contradictory metadata, not an accurate description of that original diff. The current candidate does not rely on that statement.

All 16 current candidate entries and all 24 family entries match their respective manifests. There are no extra current candidate files or unlisted family files outside ignored temporary caches. The actual current candidate SHA-256 is `20afe8e57f91c5f6483d54389d70fc7d19fce27114549b83461289f760ac1229`; the frozen original candidate has SHA-256 `bf8d8a5dda2bfe36cd0c28b4a2d0fe9ee1d2ff0365f286de8cc4bd4daa4ccf1d`. The current README correctly distinguishes historical review/provenance evidence from the modified candidate. These checks establish identity and do not validate a family's substantive reasoning.

The audit made no Git mutation. The branch remained `main`; other work advanced its head during this read-only challenge. The verdict concerns the frozen original head and manifest-pinned current candidate, not a mutable branch name.

## 2. Exact primary source and zero boundary

The [OWR original](https://ems.press/content/serial-article-files/49484), Open problem 1 on printed p. 1480, and [final EJP paper](https://pure.uva.nl/ws/files/234720765/Infinite-dimensional_Wishart_processes.pdf), Open problem 1.2 on printed p. 5, ask the injective-noise, unbounded-generator existence question using alpha outside N. The neighboring degenerate-noise question is distinct. Visual inspection confirms both problem labels and printed pages; the EJP PDF includes an extra repository cover, so printed p. 5 is physical PDF page 6.

No explicit definition of N was located. EJP uses N0 in the Corollary 4.11 proof on printed p. 29, while that corollary's statement uses N intersected with [0,rank(Q)); this contextual evidence does not explicitly define the convention. The candidate accurately records the ambiguity. If zero is excluded from N, alpha=0 and the zero process give an affirmative exception even with an unbounded noninjective semigroup. The negative claim must remain alpha outside N0.

The EJP weak-solution setting matches the candidate's equation and state space; its transform theorem has additional integrability hypotheses. The candidate derives its finite-rank transform separately, without silently importing that theorem outside its hypotheses.

## 3. One-fixed-law GMM normalization

Freshly downloaded [GMM primary source](https://arxiv.org/pdf/1607.00206), Definition 1.1 (printed p. 2) and Theorem 1.3 (printed p. 4), gives the required distributional criterion. The candidate map is dimension p=n, shape beta=alpha/2, scale Sigma=2C, and noncentrality omega=b. Cyclicity of finite-dimensional trace matches the exponent's factor order. The scale is positive definite, not a singular-scale extension.

Theorem 1.3 (ii) equivalent to (iii) is a criterion for existence of one law. Applying it to a conditional fixed-time compression does not assume its process is Markov. The scalar restriction is alpha in {0,...,n-2} or alpha >= n-1, with rank(b)<=alpha in the discrete range. The theorem explicitly covers alpha>=0 even though Definition 1.1 initially describes a positive shape. At n=1, alpha=0 lies on the unrestricted boundary; no rank restriction follows there. Negative alpha is excluded separately by scalar transform growth. These source uses match the current candidate.

## 4. Earlier exact public claim and identity

The freshly retrieved [immutable manuscript](https://github.com/ipitchford/wishart-reachable-noise/blob/73dd242a4450400e2f8f16b65929cb77fee76be1/paper.md) at commit `73dd242a4450400e2f8f16b65929cb77fee76be1` already contains the finite-rank conditional transform in Lemma 3 (raw lines 227-282), the injective-noise obstruction in Corollary 2 (130-140), and the random-initial necessity extension in its scope paragraph (755-763). Its real Hilbert, bounded positive noise, continuous trace-class weak-solution setting and arbitrary-generator necessity subsume the current narrow claim. The extension is explicitly necessity; the general random-initial existence classification is excluded. The current attribution accurately credits this mechanism and makes no novelty claim.

The manuscript author field declares Anonymous, as does the creator metadata for [Zenodo version DOI 10.5281/zenodo.22892681](https://doi.org/10.5281/zenodo.22892681). Git author and committer metadata instead name Ian Pitchford. Neither a repository account nor Git metadata establishes manuscript authorship or authenticated human authorship. Anonymous (2026) is the supported citation.

Zenodo's public API records creation on `2026-09-22T07:29:24.820191+00:00`, version `0.1.0-candidate`, preceding the 30 September attempt. This deposit is a stronger public-availability anchor than author-controlled Git dates. The versions endpoint returned one version. This proves an earlier exact archived claim, not historical first priority or external review.

## 5. Fresh archive challenge and reproducibility

`retrieve_primary.py` independently fetches original PDFs, immutable Git raw content/blob/commit metadata, and the exact Zenodo record and deposited files. It does not consume old primary downloads. The prior manuscript SHA-256 is `8ac4fe3bf81f4ec70cf17fcd4e3413b13271cf61524dacd7209119a3ae86b184`, and computed Git blob identity is `54ff9ccf53045aa22230e8f03c4127f54bb98902`, also the `paper.md` blob in exact commit metadata. All four deposit MD5s, all three advertised SHA-256s, both ZIP manuscript copies versus immutable raw content, and both ZIP PDF copies versus the standalone deposited PDF pass.

Run `python3 verify_integrity.py`, then `python3 retrieve_primary.py`, then optionally `python3 replay_pdf_inspection.py` from this report's directory. The first two scripts write compact receipts here; external material and rendered pages stay solely in ignored `tmp/`. The PDF inspection uses the already installed Poppler utilities. No installation or environment mutation is needed. Public API response hashes can change if service formatting changes; advertised archive checksums and exact bytes are the material identity tests.

The dated three-query web check found the exact Evidence Press source release. It supplies bounded corroboration only. It is not an exhaustive literature or retraction search. No outside individual was contacted; no foreign paper or archive is included in the deliverable.

## 6. Strongest result and exact remaining gap

Source integrity, narrow subsumption including random initial values, correct Anonymous attribution, GMM fixed-law use, and the zero-convention qualification pass independently. There is no remaining required source/hash repair for the manifest-pinned reviewed candidate. The full stochastic proof still requires the parent's independent mathematical verdict; a manifest cannot supply it. Worldwide priority, authenticated outside peer review, and the earlier manuscript's broad existence/singular-noise/Gaussian-continuity claims remain unverified and unclaimed.
