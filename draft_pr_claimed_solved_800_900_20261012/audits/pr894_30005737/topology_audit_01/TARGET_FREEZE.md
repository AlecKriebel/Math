# Frozen target and provenance

Frozen UTC: 2026-10-16T07:02:15.364383+00:00
Completion estimate: 10% of this independent audit.

Eligible target: PR 894; problem 30005737, Post-Lie Structures with Semisimple Target. Original draft head 401f86e018e8cc5075e37a29bae9350eb9f89c36. Original research effort recorded as claimed_solved, 1/5; this is validation only.

Exact mathematical target: for a finite-dimensional complex perfect nonsemisimple Lie algebra g and a semisimple complex Lie algebra n on the same vector space, prove that no post-Lie product on (g,n) exists. Perfect means [g,g]=g. Nonsemisimple means its solvable radical is nonzero. A post-Lie product must satisfy its three standard compatibility identities for the two brackets.

Native background was read completely before the authored proof or old audits: the source is Oberwolfach Report 46/2023, DOI 10.4171/owr/2023/46, pp. 2681–2715, problem discussion p. 2689. The frozen background labels this a conjectural extension from sl3(C) to arbitrary semisimple n. Dated upstream open status is provenance, not an assumption that a proof fails.

Boundary cases: n=0 forces g=0 on the common vector space, contrary to nonsemisimplicity; multiple simple factors must be included; the complex field and finite dimensionality are necessary for the contemplated group topology route. Nonclosed images of integrated homomorphisms and global stabilizers cannot be ignored.

Authentication: SOURCE_MANIFEST.json SHA256 1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c; all 18 external source blobs authenticated by bytes, SHA256, and Git blob SHA1. Native canonical pair: 3524 bytes, SHA256 b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298. Complete catalog record and root native receipt also read. Authentication receipt records the real process start/end, return code, and raw output hashes.

Success criterion: independently verify the global topology implications and identify their exact hypotheses; reject any claim that silently replaces local transitivity by global transitivity, Lie algebra Levi decomposition by a global product, or a compact-form rank by the required dimension. No broad priority search is within this audit.
