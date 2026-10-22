# Function Theory 2.42: credited reconstruction and literature correction

Problem 2302042 / AMR-022-2042, queue rank 675. Disposition:
**already_solved, 1/5, as an attributed literature-status correction**.

For each integer n >= 2, the reconstructed Gol'dberg-Eremenko example has
2n distinct listed finite asymptotic values whose ray/total point-count ratios
are 1/(2n). The fresh independent audit found no blocking gap in this positive
construction. This is credited prior work, not a novel solution.

Hayman-Lingham's **2018 draft**, Update 2.42, reports Barsegyan's entire-function
bound sum(b_k) <= 1, which rules out simultaneous density one for two or more
distinct values. **Barsegyan's original proof and any hypotheses omitted by
that draft were not inspected.** A bibliographic venue discrepancy remains.
The full upstream problem/report corpora and original selected-record bytes
were not freshly retrieved or matched. The status is therefore an attributed
literature correction, not verification of that complete original proof.

## Preserved evidence

- `freeze/`: the unchanged new recovery freeze, all 8 files and its original ZIP
- `independent_audit/`: the unchanged fresh independent audit, all 7 files and ZIP
- `PUBLIC_SOURCE_ADDITION.json`: separate public catalog metadata that
  corroborates the venue discrepancy, without modifying either frozen packet
- `RESEARCH_LOG.md`: publication-scope checkpoint and completion estimate
- `verify_publication.py`, `PUBLICATION_MANIFEST.json`: portable strict replay

The author freeze's statements that a fresh audit is required describe its
state at freezing. That requirement is now met by the adjacent **fresh** audit,
whose verdict is **PASS WITH EXPLICIT LIMITATIONS**. No historical audit pass
was inherited. The immutable freeze is not edited to restate later events.

## Replay

From this directory, run `python3 verify_publication.py` and
`python3 -O verify_publication.py`. The standard-library-only wrapper checks
the exact file inventory, both frozen ZIPs, all frozen manifest hashes and
member bytes, and replays the independent audit in ordinary and optimized
Python. Its replay includes 2,480 algebraic/scope checks, 8 rejected scope
mutants, 9 extra consistency checks, 2,000 exact flux checks, and four kinds
of rejected manifest mutation in each Python mode.

The frozen audit also contains 290 previously run, uncertified floating-point
diagnostics. The wrapper preserves and hashes those results but does not rerun
them; their optional script requires mpmath. Neither finite exact tests nor
floating-point diagnostics are a formalization of the analytic proof.

Only this attempt packet and this row's Status, Turns and Findings are changed.
The queue's existing header, unrelated rows, Chat and DOI cells remain intact.
Source PDFs/text dumps, raw datasets and private coordination files are excluded.
No merge, release, DOI, external outreach or journal-readiness claim is made.

Provisional AI-assisted research for Alec Kriebel; qualified expert review
remains necessary. See the full [independent audit](independent_audit/safe_audit/AUDIT.md)
and [reconstructed proof](freeze/safe_output/PROOF.md).
