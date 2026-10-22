# Boyle's Pingree problem 2: audited partial investigation

UnsolvedMath **4400008**, AMR-043-0008, selection rank **701**.
Disposition: **unsolved, 5/5 documented approaches**. This packet supplies neither
a proof nor a counterexample to the original question.

## Exact scope and remaining gap

The question concerns finite-alphabet, two-sided, one-dimensional subshifts and
a homeomorphism mapping each complete integer orbit onto a complete integer
orbit. The source is a mixing shift of finite type (SFT). No continuous or
bounded integer cocycle is assumed. The unproved step is that the target must
be finite type. Mixing then follows from the preserved orbit data.

The preserved [author packet](author/README.md) and [independent audit](independent_audit/audit.md)
retain eleven lemmas: orbit and measure invariants, the conditional mixing
reduction, cocycle regularity limits, an explicit continuous orbit involution
with unbounded jumps, shadowing and finite-language reformulations, limits of
positive-speed constructions, and finite-graph return/roof constructions.
Target shadowing and source-target flow equivalence are equivalent closing
goals in this setting; neither has been established here. The unbounded-jump
example is a self-orbit-equivalence of a full shift and is not a counterexample
to the original problem.

Five distinct approaches are recorded in [five_approaches.md](author/five_approaches.md).
The audit accepts them as documented approaches; it does not independently
certify historical interaction counts. No material correction was required.
No novelty, present global-openness, or publication-ready resolution is claimed.

## Frozen inputs and audit boundary

- `author/`: 8 original files, 56,661 bytes; manifest SHA-256
  `0d9b8a4ad752b292c4d59b262b08090478df48a303959c2de41d612387f045b6`.
- `independent_audit/`: 9 original files, 45,526 bytes; manifest SHA-256
  `9e9c5001c3c568a1dad07e7cda8cce9f334d6649273c5b8fcca2cbceb26b85c3`.

Both packets are byte-preserved. Statements such as "not yet performed" in the
frozen author status or "no remote writes" in the original author/audit files
describe those earlier stages. The separate audit and this publication wrapper
supplement that history without rewriting it.

The audit records freshly matching six scholarly PDFs and inspecting the
relevant text/pages. Only public bibliographic and verification metadata is
included. The exact catalog page returned HTTP 403 and its full research notes
remain uninspected. Original raw AI-result corpora were not inspected and no
raw-record match is claimed. The available selection catalog is not a substitute
for those corpora. Salo's result addresses the neighboring free-part conjugacy
question; Matsumoto's cited preservation result has different continuous,
one-sided hypotheses. Neither is treated as resolving this question.

## Reproduction

Use Python 3.10+ with its standard library. From this directory run:

```sh
python3 -B verify_publication.py
python3 -B -O verify_publication.py
python3 -B test_corruption.py
```

The first two commands strictly verify the inventory, frozen manifest pins and
audit-to-author byte bindings, then reproduce all three saved control outputs
byte for byte. The original controls always execute in isolated, unoptimized
Python so their assertions remain active, even when the outer verifier uses
`-O` or the environment sets `PYTHONOPTIMIZE`. Counts are 9,198 author assertions,
165,565 independent assertions and five deliberate mathematical faults rejected.
These finite controls do not prove the infinite mathematical claims.

The last command creates twenty actual disposable corruption variants across
normal and optimized verifier modes. Its output must equal
`CORRUPTION_RESULTS.json`. It checks content changes, missing/extra files,
symlinks, unsafe/duplicate manifest paths, duplicate JSON keys, and resealed
changes to the frozen packets. These are integrity tests, not security claims
against an adversary replacing both verifier and publication manifest.

The publication gate also requires replay after relocation and from remotely
retrieved bytes; the draft PR records those outcomes. No source PDFs, extracts,
page images, raw records, or private
coordination files are included. The queue change is limited to this row's
Status (`unsolved`) and Turns (`5/5`); every other queue byte is preserved.
