# Research log: family-list mixed \(P_4\) hostile review

## 2026-07-28 12:26 PDT — frozen input and dependency audit

- Froze the seven candidate artifacts at aggregate tree SHA-256
  `1e4a808e1eb45d9f03f8f74ed199e30cd20c51bd3d7c566fea4d73869329fae4`.
- Verified every artifact and accepted-dependency digest in the frozen
  manifest.
- Read the candidate note, manifest, observed summary, research log, all
  three source scripts, accepted C-148, accepted C-070, and the accepted
  C-148 hostile review.
- Kept the candidate directory read only.

## 2026-07-28 12:26 PDT — symbolic theorem audit

- Reconstructed the left-endpoint defect argument from the exact family
  lists and checked all seven exclusions for the missed vertex.
- Re-derived \(L_S(d)=\{c\}\), the \(14/9/5\) pair ledger, and the
  external-state closure argument.
- Checked that the path reflection is a hypothesis-preserving relabeling
  and does not assert an automorphism.
- Replayed the accepted packed and clean-room C-148 checks: all 32
  completions have empty terminal local kernels.
- Audited the synchronous rank indexing, including rank-zero successors,
  same-round deletion, and greatest-family survival.
- Searched every proof and encoding use of a missing family role.  None
  is converted into graph nonadjacency.

## 2026-07-28 12:26 PDT — SAT scope and replay

- Audited the graph, family, domination, one-guard response, independence,
  and nondominating-pair clauses directly from `synthesize.py`.
- Derived independent closed forms for the variable and clause counts and
  matched all eleven rows.
- Reconstructed and solved fresh formulas for orders 12 through 22 with
  the pinned CaDiCaL 3.0.1 binary.  Every run returned code 20 and
  `UNSAT`, with the reported size.
- Did not treat this generator replay as a proof: no DRAT/LRAT
  certificate, independent CNF implementation, or proof-checker package
  exists.
- Recorded two nonblocking metadata edits: “possibly proper” is the exact
  family scope, and literal command strings are not present in the
  observed JSON.

## 2026-07-28 12:26 PDT — verdict

- **PASS.**  Theorem 1, Theorem 2, the family/static guardrail, and the
  OBSERVED-only claim boundary are sound at the frozen hash.

## 2026-07-28 12:31 PDT — manifest-v2 revision confirmation

- Received revised candidate tree SHA-256
  `33a7dfb07261dff1d3ec4442269600c09e3e2b4566254710d4cc1dbab7c6897d`.
- Reversed the revised `NOTE.md` paragraph in memory and recovered the
  original audited SHA-256 exactly.
- Reversed the revised `OBSERVED_RESULTS.json` scope phrase in memory and
  recovered the original audited SHA-256 exactly.
- Reversed only the manifest schema, the two revised classification
  labels, and the two changed artifact hashes; this recovered the
  original manifest SHA-256 exactly.
- Confirmed that the candidate research log and all three Python sources
  retain their original audited hashes.
- Confirmed every v2 manifest binding, all three accepted dependency
  hashes, the solver hash, and the revised seven-file tree hash.
- The two original metadata findings are resolved.  No theorem, code,
  run row, dependency, or proof byte changed.
- **PASS CONFIRMED for manifest v2.**  The original audit remains recorded
  above.
