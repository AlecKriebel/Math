# Function Theory 7.4: audited partial results

**Problem 2307004 / AMR-022-7004, rank 688. Unsolved, 5/5 approaches.**

The sharp all-degree universal constant remains undetermined. This draft preserves
16 frozen author files and all seven independent-audit files byte-for-byte.
Their historical pending-audit and no-remote-write fields describe those stages;
[AUDIT_METADATA.json](independent_audit/AUDIT_METADATA.json) records the later
successful scoped audit. No novelty, full solution, human peer review, or formal
proof-assistant verification is claimed.

## Results and limits

- The full complex two-variable optimum is `R_2 = sqrt(3-sqrt(5))`.
- The known strict bound `M_n > 1/2` is reconstructed. This proof alone supplies
  no uniform positive gap above one-half for the infimum over all degrees.
- Real tuples and exterior-modulus tuples have the sharp restricted constant 1.
- Inverse-moment algebra yields an exact Gaussian-rational `n=32` certificate
  with every measured power sum strictly below `29/40`. This is not optimality.
- The target `inf_n R_n` is not identified with `limsup_n R_n`. Published
  asymptotic results and the 2026 proposed certificate retain their stated
  source and analytic-reduction limitations.

Read the [proof](safe_output/PROOF.md), [limitations](safe_output/LIMITATIONS.md),
[five approaches](safe_output/RESEARCH_LOG.md), and the complete
[independent audit](independent_audit/INDEPENDENT_AUDIT.md).

## Portable replay

From this directory, using Python 3 and only its standard library:

    python3 -B verify_publication.py
    python3 -B verify_negative_controls.py

The publication wrapper uses explicit checks that remain active under `-O`.
It runs the original assertion-based verifier with assertions enabled, verifies
that the original refuses `-O`, and runs the independently implemented exact
checker both normally and under `-O`. Both stored replay outputs must match
byte-for-byte. Strict inventories reject extra files, directories, symlinks,
unsafe or duplicate paths, duplicate JSON keys, and changed frozen identities.
The negative controls also relocate the packet and test scope misstatements.

These finite computational checks do not prove the unresolved all-degree
optimization. Optional floating exploration is never an acceptance mechanism.

## Publication scope

Only authored mathematics, code, certificates, audits, and public verification
metadata are included. No source PDFs, extracted source text, source dataset
records or corpora, or private coordination files are included. On the draft
branch only this problem's queue Status and Turns cells change to `unsolved`
and `5/5`; all other queue bytes and links remain unchanged.
