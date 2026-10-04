# Function Theory 6.80 known resolution

- Target: 2306080 / AMR-022-6080, original queue rank 588.
- Classification: **already_solved**, negatively by Lappan (1981).
- Substantive turns: **1/5**. One complete reconstruction of the known
  counterexample was obtained; no five-turn exhaustion is claimed.
- Main artifact: PROOF.md, a self-contained proof of global univalence
  of the derivative and nonnormality of its based primitive.
- Source audit: PROVENANCE.md, including a corrected exponent and
  bibliographic citation in the published version of Gröhn's paper.
- Reproduce finite controls: `python3 verify.py` (Python 3.10+;
  standard library only). Output is compared with CHECKS.json by default.
- APPROACH_LOG.md and turns.jsonl record the single substantive response.
- MANIFEST.json binds the public files by SHA-256, excluding itself.

The proof, rather than finite sampling, establishes the infinite-domain
claim. Controls verify exact rational margins and symbolic coefficient
identities and provide explicitly noncertifying numerical diagnostics.
No downloaded source PDFs, source corpora, or private coordination
materials are included. This is a verification of known mathematics,
with no claim of novelty or expert peer review.
