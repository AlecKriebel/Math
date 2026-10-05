# Problem 30004169: BLRS Zariski descent

**Outcome: unresolved after five scoped approaches. No full proof or counterexample.**

The target is Question 1 in Maria Yakerson's report, joint work with Tom
Bachmann, *Higher Chow-Witt groups*, printed p.1776 of Oberwolfach Report
29/2019. It concerns the **Bloch–Levine–Rost–Schmid splice**, not just the
ordinary Rost–Schmid resolution.

The source regime is a perfect field of characteristic different from 2,
smooth separated finite-type schemes, integral coefficients, weight q >= 0,
and no additional coefficient line bundle. Determinant twists at residue
fields are part of the construction and must be retained.

The packet supplies:

- the exact complex and comparison map, including cohomological degrees;
- a proof of the already-known weight-zero case;
- an explicit nonflasque lower term, even on the affine line;
- a quadratic-residue obstruction to naive closure without correction;
- a finite Čech reduction isolating the remaining descent defect;
- an orientation check explaining why square twists do not erase the general gap;
- a source/status audit through 2026-10-05 and exact small algebraic controls.

The nonflasque example is **not a counterexample to descent**. In fact its
ambient affine line is inside the published positive comparison theorem.
The formal reductions and elementary examples carry no historical novelty claim.

## Files

- `REPORT.md`: scope, prior-work check, literature and five approaches.
- `PROOFS.md`: full arguments for this packet's scoped statements.
- `controls.py`: standard-library exact checks; no network or source dependency.
- `CHECK_RESULTS.json`: replayable output of the controls.
- `SOURCE_VERIFICATION.json`: source URLs, locations, public hashes and sizes.
- `RESEARCH_LOG.md`: the five attempts and completion estimates.
- `AUTHOR_MANIFEST.json`: hashes of the authored safe files.

Run `python3 controls.py` from this directory. This is an author freeze awaiting
a fresh uninvolved audit. No remote write, publication, release, or outreach
was performed in preparing it. Reading copies of sources and dataset contents
are excluded.
