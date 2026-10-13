# Laurent-series descent: reviewed partial results

**Original 30004320 remains unsolved after five substantive author turns.**
This draft contains positive descent theorems under explicit stabilizer
hypotheses and precise obstructions to attempted proof methods. It contains
no counterexample to the original homogeneous-space question.

Read [the current reviewed status](REVIEWED_STATUS.md), [the final author
result](FINAL_RESULT.md), [the source map](FINAL_SOURCE_MAP.md), and the
[full independent review](review/ADVERSARIAL_REVIEW.md). All five proofs and
all historical manifests are preserved without edits.

The new homogeneous-space results explicitly assume a **smooth affine acting
group and a smooth schematic/fppf homogeneous variety**. Their positive
classes include tame finite stabilizers; arbitrary finite étale stabilizers
when H1(k,G)=1; all multiplicative-type stabilizers, including non-smooth
ones; and smooth stabilizers with reductive identity and prime-to-p Weyl and
component orders. Known perfect-field descent is credited to Florence;
constant-torsor descent over arbitrary fields is credited to Florence–Gille.
Historical novelty of the partial results is unverified.

The final cyclic-algebra example is a nonconstant torsor over a Laurent field
and obstructs full-Puiseux object-surjectivity. It does not disprove descent
of a point on a constant homogeneous space.

## Verification

Run `python verify_publication.py` with Python 3 and SymPy. It verifies the
public manifests and repeats all five author checkers and the independent
controls: 128,694 author assertions plus 8,664 independent assertions. These
finite controls support the analytic review; they are not a formal proof
assistant certificate. To additionally check the eleven separately obtained
primary PDFs, pass `--source-dir /path/to/sources`. Without that argument,
source hashes are explicitly reported as not rechecked. Raw PDFs, images
and imported records are excluded from publication.

AI-assisted research with separate AI-assisted source/proof review; no human
peer-review, historical-priority, merge or release claim.
