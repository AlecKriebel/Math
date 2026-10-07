# Positive factorization minimum lengths: accepted partial audit

**Problem 2769 / KP-2.21, rank 909. Canonical status: unsolved, 5/5 approaches.**

The unchanged six-file author freeze is accepted as a source-qualified partial audit. No repair was needed. The general minimum-length and realizing-word problem remains unresolved by this work; no new minimum, general solution, novelty, or formal proof is claimed.

## Accepted results and limits

- The familiar value m_1,1=12 follows from abelianization and the two-chain relation.
- The known m_2,1=7 and nonempty closed value m_2,0=7 use the stated genus-two obstruction and the published seven-factor construction. If empty words are allowed literally, the closed minimum is zero. The one-boundary capping argument is not asserted for arbitrary boundary count.
- The exact length formula is l = beta_2(X) - 2 beta_1(X) + 4g - 2 + b. Minimizing beta_2 alone needs extra hypotheses.
- The explicit twelve-factor word acts trivially on closed homology but is an interior separating twist, rather than the required boundary multitwist. Matrix equality cannot certify mapping-class equality.
- A lower bound on a restricted monodromy class does not give a lower bound on every admissible word. The October 2026 manuscript claims retain their restricted scopes.

## Read the evidence

- [Original mathematical note](original_author/PROOF.md), [report](original_author/REPORT.md), and [five approaches](original_author/APPROACH_LOG.md)
- [Full independent mathematical audit](independent_audit/audit/FULL_AUDIT.md)
- [Exact acceptance](exact_acceptance/EXACT_ACCEPTANCE.md) and [member pins](exact_acceptance/EXACT_ACCEPTANCE.json)
- [Source inspection and retrieval qualifications](independent_audit/audit/SOURCE_VERIFICATION.json)
- [Historical arithmetic replay](independent_audit/audit/REPLAY_RESULTS.json), [publication validation](PUBLICATION_TEST_RESULTS.json), and [publication metadata](PUBLICATION_METADATA.json)

The three frozen ZIPs and their external manifests are in `archives/`; every member is also unpacked unchanged. The original pending-review fields are historical freeze-time facts. Separate hash-bound acceptance records the completed review without rewriting them.

All three complete corpus inputs and the exact complete record/report pair were checked. The canonical pair is 11,010 bytes; the author's 11,220-byte pretty representation parses identically but has different bytes and a different hash. Seven local PDF pins match, and the independent audit freshly matched six downloads. Stipsicz was checked against the pinned local PDF and readable public content without obtaining a fresh matching download. These are distinct claims. Source files and corpus contents are excluded.

The author and independent arithmetic checks passed normal Python, -O, and -OO. They are diagnostics, not mathematical completeness or mapping-class certificates. The private checker programs are not distributed; this publication contains no executable. Publication-stage fail-closed archive, input-pin, acceptance, inventory, and queue checks are reported separately, including normal/-O hostile-mutation controls.

Only this queue row's Status and Turns change to unsolved and 5/5. Its Findings and every unrelated byte, note, and existing chat link are preserved. This is a draft PR; no merge, auto-merge, release, DOI, or outreach is part of this publication.
