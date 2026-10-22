# Classical priority audit research log

Scope: PR212 / 30005310 / OWR-11695865-009. All authored artifacts stay in this folder. No Git, tracker, database, publication, provider, or external communication actions are authorized here.

## 2026-10-15 09:51:31 UTC — source-first reasoning freeze

Completion estimate for this audit: **65%**. This is an audit-completion estimate, not progress toward a new mathematical discovery.

Read the frozen native source_record.json and submitted PROOF.md before any inherited reviews. Verified all three supplied PDF SHA256 values. Read complete Homs/Kuznetsova contribution, printed pp. 3146–3149, Gross–Sullivant Section 5 (and definitions in its introduction), and Blekherman–Sinn Definitions 1.1/1.4, Propositions 1.2/1.5, Section 2 through Theorem 2.7 and Corollary 2.11. Visually inspected the existing private page renders for OWR pp. 3146–3149, GS p. 14, and BS pp. 13–18. These are source images, not inherited reviews.

Frozen independent finding before inherited-review access: Gross–Sullivant Corollary 5.3 and its following sentence already state WMLT=2 for every bipartite graph with an edge. Blekherman–Sinn Theorems 2.1 and 2.7, with the explicit m=4 discussion following Corollary 2.11, already give GCR=MLT=4 for K4,4. These combine to the exact singleton triple needed to contradict the printed full numerical threshold scenarios at rank index n=3, once the elementary elimination-ideal bridge is checked. GCR=4 directly gives I4=0 by density, and det(cross block) belongs to I3 directly; no radical-ideal identification is needed for this example. This strongly favors a credited already-covered source correction, not a new threshold theorem.

Exact source-target distinction: the printed Proposition 3 second conclusion has n=WMLT≤MLT=n+1; the frozen clean question strengthens ≤ to <, but this difference does not matter for K4,4. Printed Conjecture 4 literally refers to the two cases. If interpreted only as antecedents (strict signed-SOS versus positive-definite intersection), the construction satisfies the second antecedent and does not refute that repaired question. Surrounding examples are 4-cycles, but the general definitions and Proposition 3 carry no explicit four-vertex restriction.

Remaining checks: independently reconstruct useful finite certificates; inspect the GS Definition 5.1 source page for its open-set argument; look for an authoritative erratum or explicit earlier recognition of the 2022 numerical error, without treating negative search as proof; produce coverage map and sealed authored manifest. No inherited review or sibling priority report has been read.

## 2026-10-15 09:55:19 UTC — exact specialization independently checked

Completion estimate for this audit: **85%**. No discovery percentage is asserted.

Read and visually checked GS Definition 5.1 on p. 13 by one small private render. Found a reversed inequality in the following explanatory sentence (printed wmlt≥n where the definition requires wmlt≤n). Its definition, splitting proof, Corollary 5.3, and explicit bipartite statement are consistent and suffice. BS Remark 2.2 calls treewidth m+1; under the GS convention treewidth is m. That typo does not enter the K4,4 specialization, which is on the n≤binom(m,2) branch proved by their explicit independent-generators construction. Read the complete requested BS proof chain through Lemmas 2.8–2.10.

Built check_certificates.py using only exact rational arithmetic. It verifies full Gram-statistic Jacobian minors 256 (singleton) and 128 (tied), the rank-two success witness, an exact-rank-three positive-definite-intersection witness, and a concrete rank-three open-failure mechanism modeled on BS: a rational orthogonal Householder matrix gives matching frame Grams and a 6×6 coefficient minor 1148/3375 with positive all-ones kernel. The analytic neighborhood argument will be in REPORT.md. This also independently verifies MLT=4 for the singleton specialization, avoiding reliance on a delicate real-density step in the general BS proof.

Authoritative browsing: opened arXiv version-history pages (GS v3 2015-09-16, BS v2 2017-05-23), the official EMS report page (published 2023-07-27 for workshop 2022), and the MFO repository record. Narrow erratum/correction searches found no primary recognition. This is only a bounded negative search, not evidence of first recognition. The recent Homs/Kuznetsova/Stolz paper remains deliberately unread here because a separate priority family owns that review. No inherited reviews or sibling reports read.

## 2026-10-15 09:58:12 UTC — report complete and sealing checkpoint

Completion estimate for this assigned classical-priority audit: **100%**. The wider research/promotion goal is **not** marked complete; no new-discovery percentage is asserted.

Completed REPORT.md with exact old-source coverage map, source-target distinction, proof-chain challenges, full finite-certificate interpretation, singleton-versus-tied separation, and access/search limits. Re-ran the exact checker and compared stdout with certificates.json byte-for-byte; it reproduces exactly. Rechecked the open-failure argument: the invertible 6-column coefficient minor gives a continuous strictly positive kernel vector under perturbation, and equal weighted frame Grams yield the PSD sparse annihilator. Rechecked the four-observation upper bound: the nonzero Jacobian minor gives interior sufficient statistics almost everywhere, hence PD completions. These are separate from the historical coverage inference.

Disposition: the full literal numerical counterexample is valid but already covered by the combined 2015/2017 primary results, so recommend a credited source correction. Explicit prior recognition of the report's mistake remains unverified, and the antecedents-only question is untouched. The genuinely tied variant's WMLT and ideal assertions follow by projection; no tied MLT equality is claimed.

Final authored manifest and SHA256 seal cover only the authored report, log, exact checker, captured certificate, and manifest chain. All source PDFs, full source texts, and page renders remain private and excluded. No Git, index, ref, tracker, provider, publication, database, PR, or queue mutation; no external communication or outreach; no sibling priority report read. Parent retains promotion authority.
