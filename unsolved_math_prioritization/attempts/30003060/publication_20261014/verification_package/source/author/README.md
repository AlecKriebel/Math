# Higher Koszul homology: characteristic-scope correction

Target: 30003060 / OWR-14218-004; supplied queue rank 865.

## Result

A free associative algebra on two generators is Koszul over every field. In characteristic p>0, a cyclic sum built from x^(p-1)y yields a nonzero higher Koszul homology class in degree one. The smallest example is x tensor y + y tensor x over F_2.

This settles the literal unrestricted-field formulation negatively. It does not settle the characteristic-zero equivalence or its vanishing-to-Koszulness implication. The characteristic-zero research question is **unresolved in this investigation**. Whether the abbreviated OWR statement was intended to inherit characteristic zero cannot be established from the report; its literal text has no such restriction. Queue disposition is deliberately left for independent source-scope review; no queue or remote repository has been changed.

## Files

- PROOF.md: complete elementary proof, every-prime extension, cyclic-orbit formula, and limitations.
- SOURCE_AUDIT.md: exact-source hypotheses, distinction from ordinary Koszul homology, attribution, and bounded literature search.
- SOURCE_METADATA.json: public URLs, versions, hashes, byte counts, and inspection history only.
- SELECTION_REVIEW.json: complete-corpus verification and prior-attempt checks, without any source record contents.
- APPROACHES.json and STATUS.json: one substantive approach; stopped on the literal-scope counterexample, with characteristic-zero target preserved.
- verify_free_algebra.py and RESULTS.json: exact, reproducible finite controls.
- PROVENANCE_RESULT.json: recorded full-corpus and six-PDF byte checks; textual inspection is separate.
- verify_provenance.py: optional complete-corpus and supplied-PDF hash checks; no source texts are bundled.

The immutable safe archive contains only these authored files. An external manifest binds every archive member and the original ZIP byte stream. The external bootstrap verifies its pinned manifest, ZIP hash, exact inventory, names, types, sizes and hashes before extracting or running the checker. The corrected external bootstrap requires isolated, no-site, no-bytecode Python for itself and its child checker; it rejects optimized execution. A successful computational replay must exactly reproduce RESULTS.json.

## Review protocol

Read PROOF.md and SOURCE_AUDIT.md before accepting any disposition. Independently check the coefficient convention, the ordinary versus higher differentials, the absence of incoming boundaries, and the unrestricted-field versus characteristic-zero distinction. The whole Solotar contribution, not a neighboring speaker's field assumptions, is the relevant OWR context.

Run the separately supplied bootstrap with Python's -I -S -B flags, passing the safe ZIP and external manifest. The optional provenance checker accepts explicit corpus/PDF paths; without those inputs, source rehash is not performed. Replaying finite algebra controls does not redo textual source inspection or establish literature exhaustiveness.

No PDFs, source extracts, images, raw corpora, upstream source code, private sources, or private coordination files are included. Existing source results are credited. There is no novelty, first-priority, characteristic-zero solution, formal-certification, or external human-review claim. AI assistance was used throughout. Independent mathematical and source-scope review is recorded separately in the accompanying acceptance; external human review has not been claimed.
