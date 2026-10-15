# IM-sharing Theorem H: zero-value counterexamples

Problem 30000700 / OWR-1460-004, queue rank 659.

**Candidate negative answer to the printed universal IM question.** The primary report explicitly allows the shared value to be zero. For any integer k >= 2 and any nonzero complex b, the polynomial f(z) = b z^k/k! shares zero IM with f' and has f^(k) identically b. It cannot be a nonzero exponential. This refutes the asserted universal conclusion, including after correcting the catalogue's incorrectly transcribed additive constant.

The packet includes a classification of all polynomial instances and a transcendental counterexample family for every k >= 3. The latter shows that adding a transcendence assumption does not repair the zero-value case.

**Scope and status:** No novel result is claimed. No conclusion is claimed about a variant requiring a != 0. Independent audit is pending. The elementary counterexamples do not depend on the unavailable full texts listed in SOURCE_VERIFICATION.json. They do not contradict the CM theorem.

Files:
- PROOF.md: self-contained proofs and exact scope.
- verify.py and CONTROL_RESULTS.json: deterministic exact-arithmetic controls.
- SOURCE_VERIFICATION.json: public bibliographic and verification metadata only.
- REPOSITORY_GATE.json: read-only queue and duplication checks.
- RESEARCH_LOG.md and turns.jsonl: approach/status record.
- STATUS.json: machine-readable claim and limitations.
- MANIFEST.json and verify_manifest.py: hash and size validation.

Replay: python3 verify.py; python3 verify_manifest.py.

No scholarly PDF, source text, dataset content, private personal information, or private coordination material is included in this packet.
