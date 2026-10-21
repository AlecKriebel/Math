# Final eligibility reconciliation, PRs 700–800

Independent read-only screen, captured **16 October 2026, 19:17:28–19:17:40 UTC**.

Every one of the **101 integer PR numbers** was queried directly through five GraphQL alias batches, rather than repository search or a capped connection. A second complete 101-number inventory agreed exactly with the first. The captured responses are included.

The result is **nine merged**, **two closed without merge** (#734 and #767), and **90 open drafts**. Only each open draft's own problem row in the exact immutable-head `unsolved_math_prioritization/QUEUE.md` was inspected. Their statuses are **80 `unsolved`, nine `already_solved`, and one `claimed_solved`**.

The only eligible current draft is **#799**, problem **30002364**, head **cc45ec9dc93515593c3b2a228def86c3a562e13f**, status exactly **`claimed_solved`**, turns **5/5**. It was already the parent's active case. **There are no newly eligible PRs outside that known current case.**

The nine merged numbers are #718, #742, #764, #765, #778, #781, #786, #788, and #789. These were accounted for by metadata only. Their mathematics was not reread. No mathematical files or claims of any skipped PR were inspected.

For every one of the 90 open drafts, an authenticated GitHub GraphQL `object(expression:"<immutable-head>:<queue-path>")` query supplied the queue blob's Git OID and byte length. Existing local immutable Git blob bytes reproduced that OID and length before the script extracted only the own problem row. The certificate records the full blob SHA-256, the own row and its SHA-256, timestamp, exact head, and status. All 90 sources were available locally; no fetch or raw-download fallback was needed.

This is a point-in-time eligibility certificate. GitHub API responses are evidence obtained through authenticated transport, not independently signed attestations. Later edits require another check. In particular, the parent must read back #799 after its final disposition. The screen makes no mathematical or priority judgment.

No GitHub mutation, native queue/index/ref/object write, sheet write, Zenodo action, external message, or program-wide document edit was made. Only this dedicated screen directory was written.

Completion estimate for this metadata reconciliation: **100%**. Completion of the research/publication goal remains the parent's responsibility.
