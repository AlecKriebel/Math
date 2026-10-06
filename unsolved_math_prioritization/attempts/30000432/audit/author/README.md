# 30000432: exact cycle-bipyramid partial and proof-route obstructions

**Status: unsolved, 5/5 substantive approaches.** The general Ziegler question
is not settled. The main authored partial classifies every equal-area drawing
of a labeled cycle bipyramid with a fixed triangular exterior: there are
exactly m−2, and all have explicit rational coordinates. The proof is valid
for every m≥4. The verifier's finite sample is supplementary.

Read `PROOFS.md`, then `SOURCE_REVIEW.md`. `CERTIFICATES.json` contains small
exact witnesses. `SOURCE_METADATA.json` records only public source metadata
and corpus verification hashes; no source PDFs, extracts, or datasets are
included. `MANIFEST.json` covers every other file recursively.

Python 3, standard library only:

    python verify.py
    python -O verify.py
    python run_checks.py

The first two commands verify the mandatory manifest and exact rational
controls. The last also checks relocation and rejects integrity and semantic
mutations in both Python modes. It uses temporary copies and leaves the
packet unchanged. Run commands from any working directory by supplying the
script's absolute path. Do not place output files inside the frozen packet:
the integrity gate rejects unlisted files.

No general-graph enumeration, formal proof certification, historical novelty,
human peer review, or remote publication is claimed. This packet is ready for
a fresh independent mathematical/source audit; it does not itself contain an
independent audit verdict. Existing literature is credited explicitly.
