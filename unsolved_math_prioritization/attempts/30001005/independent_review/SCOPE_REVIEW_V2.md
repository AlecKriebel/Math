# Narrow source disposition review of release 2

Reviewed 3 October 2026 UTC for problem 30001005 / OWR-2045-001.

## Decision

**PASS for publication as a source correction and verified classical obstruction, with the original target unresolved, queue status `blocked_pending_source_repair` (or `blocked` with that reason), and substantive attempts retained at 0/5.**

This is not approval to mark the original problem `already_solved`, to claim a new result, or to declare a replacement problem open. The earlier HOLD on an unqualified original-problem resolution remains in force. The revised disposition respects it.

## Frozen release

Reviewed directory: `rank445-30001005/release_v2`.

MANIFEST.json SHA-256:

`244cda56551a5f5019d37f46e112c621f88e30305c733f4503b461397cd83fd5`

All ten manifest payload entries exist and match their hashes. The verifier reran successfully and agrees with the stored result. The analytical proof in sections 2–4 is unchanged from the independently audited first release. No release file was changed by this review.

## Required points verified

1. **Quantifier repaired.** SOURCE_CERTIFICATE.md now describes an initial hypersurface and a given flow. It no longer replaces this with existence of some smoothing evolution. SCOPE_DISPOSITION.md explicitly distinguishes given-flow universality from existential construction and explains why one nonsmoothing flow does not refute the latter.
2. **Counterexample scope retained.** The headline names locally finite integral Brakke flows, noncompact data, and hypersurface dimension seven. It does not assert a counterexample to self-expanding asymptotics separately, a compact-data counterexample, or uniqueness of the stationary flow.
3. **Original unresolved status retained.** The manifest contains `original_selected_flow_problem_resolved: false`, `new_open_target_authenticated: false`, `new_discovery_claim: false`, and `turns_used: 0`. README, GATE_REPORT, SCOPE_DISPOSITION, and the turn log consistently recommend a source-repair hold.
4. **Source-gate conclusion is defensible and bounded.** The OWR abstract's smoothing announcement is qualified by construction in its Theorem 2 and dimension at most six. It supplies no explicit modern weak-flow class and does not explicitly formulate an n ≥ 7 open conjecture. The catalogue's dimension cutoff and unspecified flow class do not authenticate a precise current open selected-flow conjunction. This is a conclusion about the record's evidentiary sufficiency, not a global claim that no open problem exists.
5. **Proved regimes remain excluded from a manufactured residual.** The revised assessment distinguishes the 2024 outermost-flow results in dimensions two through six and their smooth-outermost-expander extension to higher dimensions. It does not use methodological difficulties with forward monotonicity as proof that an asserted theorem is open.
6. **Attempt accounting is appropriate.** Zero substantive attempts is consistent with verifying a classical counterexample and failing the source-readiness gate. There is no authenticated new target on which five attempts should be padded. If a genuine, precisely sourced open target is subsequently supplied, it requires a new readiness decision and substantive work.

The decisive source anchors are [Ilmanen's OWR contribution, printed p.1937](https://ems.press/content/serial-article-files/46179) and [Chodosh–Daniels-Holgate–Schulze, Theorems 1.2–1.4 and the paragraph after Theorem 1.2](https://link.springer.com/article/10.1007/s00222-024-01296-8). These were inspected in the first audit. Their implications support this source-repair disposition without any assumption about exhaustive literature search.

## Suggested explicit Findings text

Source-scope ambiguity. The stationary Simons cone in hypersurface dimension seven disproves universal short-time smoothing for unrestricted locally finite integral Brakke flows with noncompact data. This does not settle an existential or specified selected-flow formulation, or the asymptotic-expander clause separately. The original OWR announcement does not specify the weak-flow class and restricts its smoothing theorem to constructed flows in dimensions at most six; the cited modern outermost-flow regimes are proved. No precise current open n ≥ 7 selected-flow conjunction is authenticated by this catalogue entry. Hold for source repair; original target unresolved; 0/5 substantive attempts.

## Review boundary

This was the requested narrow review of quantifiers, disposition, and consistency with the already inspected decisive sources. It is not a fresh proof search or independent full-text audit of every additional literature summary in SCOPE_DISPOSITION sections C and F. Those supplementary summaries disclose their access limits and are not needed for the PASS above. The PASS must not be described as an exhaustive current-status review of all related literature.

No remote write, queue mutation, new proof attempt, cancelled-download retry, or invented target was performed.
