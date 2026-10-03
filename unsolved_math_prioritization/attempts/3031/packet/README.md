# Exact-coloring graphs3031: five-turn partial research packet

Original target: Erickson's exact-coloring classification for countably infinite complete graphs. Source3031 / OPG-57824, rank425; source alias3114 / OPG-37229 is identical and reserved against duplication.

**Status: original target UNSOLVED; local author budget EXHAUSTED5/5. No remote changes.** This packet is ready for an uninvolved audit. Passing an audit of the partial theorems does not settle the conjecture or establish novelty.

## Main results to review
1. `FINITE_MODELS.md`: complete finite rooted models with explicit2(c−1) core bound, bounded target verification and crossing-core constraints. General equivalence is credited to Stacey–Weidl; originality of refinements unclaimed.
2. `TURN_1.md`: properly colored K5 block family and explicit(112,43) certificate.
3. `TURN_2.md`: finite four-gadget theorem for the full normalized deficit-difference-six subfamily. This is the strongest construction theorem in the packet; its novelty remains unverified.
4. `TURN_3.md`: proper-clique numerical-semigroup families for every fixed larger gap d=6r, with exact conductor certificates for d=12,...,48.
5. `TURN_4.md`: exact (217,43) construction and a compact-padding obstruction, including explicit failure for (262,64).
6. `TURN_5.md`: failed arbitrary-palette extension and exact sumset obstruction.

`SOURCE_GATE.md` documents checked sources, provenance, prior-attempt search, and the no-fabricated-alias-row rule. `turns.json` records exactly five substantive author turns. Remote QUEUE remains unchanged by this worker and is not silently represented as synchronized.

## Reproduction
Run in this directory with Python 3 standard library:

python check_examples.py
python deficit_blocks.py
python gap_six_gadgets.py
python large_gap_gadgets.py
python padding_obstruction.py
python extension_failure.py

No packages, network, external state or solver are needed. Every script writes only its checked local output files. `rooted_c112_m43.json` is also a standalone certificate accepted by:

python rooted_verify.py rooted_c112_m43.json --full-spectrum

`failed_extension_c113_m43.json` is deliberately a negative control and must be rejected with exit1 because it contains a43-color subset.

## Scope cautions
The full infinite target is not equivalent to testing ordinary finite edge-only cliques. A rooted certificate needs both spoke labels and edge labels. A finite search miss is not proof of impossibility unless the complete bound is exhausted. A gadget's missing local deficit does not automatically exclude the desired infinite palette at larger subset sizes. Current literature is credited, including Ranđelović's2025 sufficiently-large-m preprint, without claiming a new independent recertification of its entire proof. Searches were scoped, not global novelty proofs.

Do not upload the separate raw source corpus or source PDFs; they are not part of this research packet.
