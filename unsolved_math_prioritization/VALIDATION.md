# Validation record

Final check: 2026-09-22T05:24:16+00:00. Source revision: `37e53eabe540fb458758e198be61634bd02ee008`.

- All **15,458** source IDs have one individual short review in the six historical ledgers. All 15,458 original notes are distinct; all 15,458 effective notes are also distinct. Every merged assessment hash matches its complete pinned problem and joined prior report.
- The raw source files' checksums and all 15,458 indexed payload/report pairs were checked for equality. See [source integrity](review_v2/source_integrity.json).
- **90** source or calibration overrides are stored separately from original judgments. The merge manifest binds each ledger, the overrides and activated assessments by SHA-256. Original notes remain available after later corrections.
- **1,951** eligible candidates: 1,798 proof routes and 153 routes combining reasoning with modest checks. All start `queued`, at `0/5`; there are no ready, active or solved local research claims. The remaining 13,507 records carry holds.
- All **886** records with an explicit upstream resolution claim are excluded. Additional source checks exclude later resolutions and hold unsupported solution claims, ambiguous statements, huge searches and insufficient proof routes. This does not certify that every remaining candidate is currently open.
- All **34 regression tests pass**. They cover source changes/cache loss, retained retired records, review and status persistence, exact hold clearance, full-review merge coverage and source matching, override validation, preservation of later assessment edits, five-turn exhaustion and candidate verification. Independent workflow retesting reproduced and then verified fixes for seven defects.
- Three full exports, including different process hash seeds, were byte-identical for catalog, CSV, queue, shortlist and summary. [Machine-readable results and hashes](review_v2/final_validation.json).
- Raw downloads and SQLite remain ignored. The review ledgers, effective assessments, all-record ranking, status workflow, source provenance and logs are committed. No mathematical attempt, outreach, GitHub release or Zenodo deposit was made.

## Independent challenges

[Cross-domain ranking](review_v2/FINAL_RANKING_AUDIT.md), [final leaders](review_v2/FINAL_LEADER_AUDIT.md), [analysis/eigenvalues](review_v2/FINAL_SOURCE_AUDIT_2.md), [dynamics/probability](review_v2/FINAL_SOURCE_AUDIT_3.md), [algebra/topology](review_v2/FINAL_SOURCE_AUDIT_4.md), [CPWL algorithm scope](review_v2/FINAL_CPWL_AUDIT.md), and [workflow audit with retests](review_v2/FINAL_WORKFLOW_AUDIT.md). These preserve initial findings and explain their limits; effective changes are in [overrides](review_v2/adversarial_overrides.json).

## Reproduce

Restore the pinned source using the README instructions, then run:

```sh
python3 -m unittest discover -s unsolved_math_prioritization -p 'test_*.py'
python3 unsolved_math_prioritization/queue.py rank
```

The completed historical merge is already activated. Do not replay it over later assessments; the checksum guard rejects that loss of work. Use `assess` for subsequent judgments and `sync` to ingest a new dataset version. Source changes retain old reviews and statuses but invalidate clearance.

## Remaining limits

These are short semantic desk reviews, with targeted primary-source checks of selected candidates, not 15,458 exhaustive literature reviews. Probabilities and impact are subjective and uncalibrated. No method can certify the unique highest expected-value order or guarantee a five-turn solution from this evidence. Full-target novelty, proof validity, exceptional cases and source conventions still require verification before and during each attempt. Related and semantically duplicate problems may remain.

Evidence fields enforce documentation, not mathematical truth. Commands assume a single writer. Staged file replacement is sequential, not a transaction across all files; abrupt interruption or disk failure was not fault-injected. Future reused upstream IDs require identity review. Raw import uses memory proportional to the approximately 149 MB pinned inputs. No partial proof has been promoted as a full solution.
