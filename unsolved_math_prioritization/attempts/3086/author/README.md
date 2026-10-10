# Unit-square covering: exact partial results and a local-lemma counterexample

Problem: UnsolvedMath 3086 / Open Problem Garden OPG-37327.

**Status: the original all-integer conjecture is unresolved in this work.**
No covering counterexample, all-integer proof, novelty claim, or journal-acceptance
claim is made.

The principal checkable result is an exact counterexample to the unrestricted
single-tile grid-length estimate in Lemma 2 of Sira Sriswasdi's
[arXiv:2609.15876v1](https://arxiv.org/abs/2609.15876v1).
The tile has positive-length contact with precisely one boundary side. It is not
a boundary-tangency artifact. Its grid-intersection length exceeds the stated
upper bound. The paper uses that estimate in its proposed n=4 proof; that argument
therefore requires a repair. This finding does not show that the n=4 conclusion is
false.

Other proved observations: the axis-parallel version; the n=1 case; an all-n lower
bound of 2n on the number of non-axis-parallel tiles in any hypothetical cover;
and an elementary two-parallel-line chord bound. No novelty is asserted for these.

## Reproduce

Run `python3 verify.py` using Python 3.9 or newer, without optimization flags.
It uses only the standard library and compares its output with `results.json`.
All certificate geometry and comparisons use exact rational arithmetic in
Q(sqrt(2)); there is no numerical optimizer in the proof or replay dependency.

`PROOF.md` supplies the arguments and precise limitations. `sources.json` records
public-source verification metadata. `RESEARCH_LOG.md` records four substantive
approaches, their outcomes and remaining gaps. `manifest.json` freezes the files
in this directory other than itself. `check_manifest.py` verifies that file list
and each byte count and SHA-256 digest.

The safe package intentionally contains no source PDFs, copied source extracts,
images, raw datasets, private correspondence, or coordination records.
Independent audit is still required before promotion or publication.
