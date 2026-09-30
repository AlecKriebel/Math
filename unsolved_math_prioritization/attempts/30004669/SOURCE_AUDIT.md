# Source and scope audit

Checked 2026-09-30. The target remains unresolved by this package.

## Original question and model

The full contribution *Relativized depth* in OWR21/2021, printed pp.1162–1164, defines depth using prefix-free K and ordinary computable time bounds. The exact alternatives on p.1164 were visually checked. “A-depth is stronger” means D^A is a smaller class, not a larger one. Computable oracles give equality; the uncertain cases concern noncomputable K-trivial oracles.

The full published article by Bienvenu, Delle Rose and Merkle, TCS949 (2023), 113694, was downloaded. Definitions2.1,2.10,3.1, Lemma2.2 and the proofs around Theorems3.3–3.4 and6.3 were checked. Section3 explicitly rejects fully relativizing the time bounds. Its Section6 leaves the exact K-trivial question open. The last page and its quantifiers were visually inspected.

Its time convention measures time as a function of output length. Universal-machine simulations require an ordinary computable enlarged time bound. The proof artifact retains that enlargement instead of asserting identical deadlines for different machines. The target is strong logical depth of infinite binary sequences, not plain-complexity depth, polynomial-time depth, infinitely-often conditional depth, or depth of circuit families.

## Imported theorems and the new deductions' limits

Nies, *Lowness properties and randomness*, Advances in Mathematics197 (2005),274–305, was downloaded in full. Theorems6.1–6.2 supply downward closure and low-for-K equivalence. Theorem7.4, printedp301, supplies a **truth-table** c.e. K-trivial cover; its exact statement and change-record proof were visually and textually checked. The earlier cost-function and golden-run theorems remain credited inputs, not independently reproved here.

The full primary preprint of *Solovay functions and their applications in algorithmic randomness* was checked in Section4.4. It explicitly says its elementary proof yields only a Turing cover and cites Nies for the stronger truth-table cover. Our transfer requires the latter; no substitution of Turing reducibility is made.

Moser–Stephan, *Depth, highness and DNR degrees*, DMTCS19(4) (2017), was downloaded from the journal. Its Section4.4, Theorem4.6 and proof assert that every K-trivial set is shallow for the prefix-free constant-significance notion, matching BDRM's cited input. This is used only to exclude witnesses X computable from A. It does not characterize all A-shallow sequences.

The transfer lemma adapts BDRM's simulation argument using equal unbounded K-complexities. Its c.e. consequence and the elementary compiler obstruction are not claimed to be novel. Neither is a classification of the noncomputable K-trivial oracles.

## Current literature check

Primary searches used the exact title, K-triviality, time-bounded complexity, relativized depth, and the author publication page. The 2024 CIRM lecture by Delle Rose repeats the same open alternatives; this was checked through its indexed primary text, while a direct local PDF request returned403. The 2026 publication *Bridging Computational Notions of Depth* by Bienvenu and Porter is listed on the author's publication page. Its full arXiv2403.04045v1 was read for its scope and searched for oracle/lowness statements: it compares strong/weak depth and deep effective closed classes, and does not furnish the K-trivial oracle classification. No final-journal comparison is claimed.

No exact resolution was located. A bounded search cannot certify the absence of later results; the package's unresolved status means its own full target is unproved.

## Gates and provenance

The selected record was read from the authorized pinned full dataset because the UnsolvedMath landing page was unavailable. Its source-code keyed prior-report value is null. The imported record has a dated literature assessment, not a previous proof. The local desk review likewise identifies the unbounded-versus-time-bounded gap without resolving it.

At base c6975ca76f9f667f1250ba403d0e6da2aafe14d0 the queue row was rank165, queued0/5. Current state/history, all-ref target history, related-target groups, complete-record related-title searches and140 all-state PRs produced no previous problem-specific attempt. The new branch is dot/math-30004669. No queue or shared state file is edited by this package.

The actual research runtime is gpt-6-astra at xhigh. The queue's general ultra-budget description is not presented as the runtime used. Two substantive approaches are recorded; no additional approach is hidden in source triage. Source PDF hashes and URLs are in `source_manifest.json`; downloaded PDFs remain outside the public package.
