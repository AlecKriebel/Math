# Problem 30001522: a Wu-manifold witness

The authored proof answers the literal free-action question affirmatively using one fixed classical manifold, SU(3)/SO(3). It has free cyclic actions of every odd order and no free continuous involution, hence no free torus action. It is simply connected, finite, and rationally equivalent to S^5.

Status: **author-prepared complete proof, awaiting fresh independent mathematical audit**. No novelty or publication-priority claim is made. No exact prior publication explicitly tying this witness to Hanke's OWR question was located in the bounded source search. The ingredients and homogeneous space are classical and are credited in PROOF.md.

Read PROOF.md for the mathematics, LITERATURE_STATUS.md for source scope, and SOURCE_METADATA.json and PROVENANCE.json for public verification metadata.

## Reproduction

From any working directory, run `python3 -I -B /path/to/VERIFY.py`, then `python3 -I -B -O /path/to/VERIFY.py`. Run the damage controls with `python3 -I -B /path/to/TEST_CONTROLS.py`. Isolated mode prevents local modules from shadowing the standard library; `-B` disables bytecode writing. No third-party package, network request, write inside the packet, source PDF, or original corpus is needed. A trusted archive/manifest digest must be checked separately before trusting any verifier shipped with an archive.

VERIFY.py rejects missing or extra members, cache directories, symlinks and other nonregular members; verifies every manifest-listed byte; then compiles CHECKS.py directly from its just-verified bytes. It does not import a local source file or execute bytecode caches. The arithmetic result is compared to EXPECTED_RESULTS.json.

The finite diagnostics do not formally verify topology or prove an infinite family. Their role is to catch arithmetic and packaging mistakes. Fresh mathematical review is required before acceptance. SOURCE_METADATA.json describes historical source inspection; public replay does not re-fetch or authenticate the omitted source documents or corpora.

The safe package contains only original mathematical exposition, authored code/results, and public metadata. Source PDFs, extracted source text, corpus records, and private coordination material are excluded.
