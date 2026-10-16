# Operative literal-source qualification for PR52

The original nineteen files are preserved unchanged at pinned head d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a. This qualification supersedes only ambiguous descriptions of the prior report's storage, not the historical bytes or the mathematical theorem.

- The raw research_results.json dictionary has no OWR-1452-008 key at immutable revision 37e53eabe540fb458758e198be61634bd02ee008. This is absence, not a present JSON-null value.
- Original prior_report.json is exactly `null\n`, hence its decoded value is JSON null. It records the author's absence display convention.
- The selected SQLite records.report cell is non-NULL text exactly `'{}'`, decoded as an empty object. queue.py's import uses reports.get(problem_number, {}) for this unambiguous absent key. Calling the SQL join “null” is not literally correct.

SELECTED_LITERAL_SOURCE.json retains the exact SQL payload/report strings, full decoded upstream problem, raw key-presence flag and full original prior-report bytes. DATED_NATIVE_SELECTION.json gives dated mutable native identities without future acceptance authority. No SQL, raw cache, original PR artifact, native queue/state or historical review is rewritten.

The final ledger remains zero substantive fresh search attempts plus one credited known-theorem validation activity. The older research-log wording is retained rather than erased. This qualification creates no additional proof-search response and no separate invented original-response field.
