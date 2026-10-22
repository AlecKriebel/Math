# Quantitative lattice squares in polyomino boundaries: audited partial record

ID 30001694 / OWR-4798-010, supplied queue rank 706. Publication date: 2026-10-05 UTC.
Outcome: **unsolved, 5/5 bounded approaches consumed**. The universal conjecture remains unresolved by this work. No novelty or globally certified openness claim is made. The retained author's subjective completion estimate is 20%, not a probability or a full-resolution claim.

## Controlling release guide

Read [the complete independent audit](audit/FULL_AUDIT.md) before the historical author README. The audit accepts the exact original mathematical partial record and its 9,349-row certificate **only under the independent strict validator**. The author and audit directories and ZIPs are preserved byte-for-byte. Historical pending-audit fields are historical, not the current verdict.

Two historical validation claims are explicitly superseded:

1. `author/verify.py` silently accepts appended rows with out-of-domain masks 0 or 65536. Its claim to reject every extra row is false. The actual frozen certificate has exactly 9,349 correct rows.
2. `author/verify_manifest.py` exempts every file named MANIFEST.json, including nested paths, so it accepts `extra/MANIFEST.json`. Its claimed exact allowlist is false. The original ZIP itself has exactly the intended entries and no hidden extra member.

Use `audit/strict_release_validator.py --controls` for certificate and archive acceptance, never either historical verifier alone. It independently enforces canonical integer fields, mask domain, exact row count, uniqueness, the complete admissible-mask set, all maxima and witnesses, exact member and manifest allowlists, duplicate-key rejection, and immutable hash/size anchors. All 17 attacks are rejected under normal Python and `python -O`. This script does not import or run either historical verifier. The historical defects are preserved and disclosed, not silently patched.

## Exact scope and retained results

The domain is a finite nonempty union of unit lattice cells whose boundary is one Jordan curve. If s is the largest side of an open axis-parallel interior square and M is the largest side of a square whose four vertices are boundary lattice points, the target is 2 M² >= s². The boundary square may be rotated; its edges and interior need not lie inside the polyomino. The original even/odd constants and source attributions are retained in [PROOFS.md](author/PROOFS.md).

Five bounded approach families retain integer-block, lattice-rounding, unit-chord reduction, rectangle, quarter-turn symmetry, and conditional compactness arguments. None supplies the missing unbounded quantitative guarantee for arbitrary chordless grid cycles. The exact missing statements are recorded with the proofs.

Three independently implemented admissibility methods agree on all 65,536 masks, including the empty mask. All 65,535 nonempty 4-by-4 cell masks yield 9,349 admissible objects; the certificate's maxima and witnesses match. The minimum M²/s² is 8/9, first at mask 16366. There is no symmetry quotient. Extended bounded controls cover 53,072 chord surgeries and 32,500 rounding cases; these support the proofs and do not prove the universal conjecture.

The seven-cell mask 886 has no axis-aligned boundary lattice square, but a rotated boundary square has M²=5. It defeats an axis-only strategy, not the target conjecture.

Pettersson, Tverberg and Östergård's [2014 paper](https://link.springer.com/article/10.1007/s00454-014-9578-5) supplies the credited reductions and reports the bounding-box bound n <= 13 (cell-box side length; an (n+1)-by-(n+1) vertex grid). Our 4-by-4 computation is smaller and is a reproducibility exercise, not a new frontier or a replay of that published search. The original statement is Tverberg's [OWR 08/2011, printed pages 362–363](https://ems.press/content/serial-article-files/46323).

## Reproduce offline

Python 3.10+ standard library only. From this directory:

    python -B verify_publication.py
    python -O -B verify_publication.py

Each command checks the exact publication inventory, immutable author/audit ZIP and manifest anchors, every file's bytes, the extracted-to-archive correspondence, and strict validation with all 17 attacks under both normal and optimized Python. It does not alter any retained file.

Direct controlling command:

    python -B audit/strict_release_validator.py archives/polyomino_30001694_FROZEN_PUBLIC_PACKET.zip --controls

Optional extended geometric replay (use a new output directory outside this publication):

    python -B audit/independent_controls.py --original author --out /path/to/new-results

Run this extended script without `-O`: its supporting geometric stress tests use Python assertions. The controlling strict validator and publication integrity checks use explicit exceptions, so their mandatory checks remain active with `-O`. The extended script deliberately records historical acceptance of attacks as defects, not passes.

## Source and publication limits

The primary OWR source was inspected. Publisher-indexed 2014 article text was inspected; the publisher PDF body remains uninspected. Its download was denied twice and stopped, with no alternate route. The exact problem webpage and raw prior AI/dataset records remain uninspected. Catalog hashes are inherited identifiers, not newly established raw-source matches. Public source hashes and inspection history are metadata only.

Only authored proofs, code, computational certificates, audits, and public verification metadata are included. Scholarly PDFs, source extracts/images, raw external records, private sources, and private coordination files are excluded. A computation certificate authored for this finite check is not an imported dataset record.

The queue change sets only this row's Status to unsolved and Turns to 5/5. Findings, Chat, DOI, all other rows, and the existing embedded header are preserved exactly. No merge, release, DOI, or outreach is part of this publication.
