# Nondivisorial canonical Fano degeneration: problem30005079

The current mathematical artifact is `PROOF.md`, identical to the frozen fourth edition in `EDITION_HISTORY.json`. It gives a fivefold example using published theorems and an authored irrational-ratio/product-filtration argument. The frozen proof retains its pre-review candidate label; any subsequent independent acceptance report should identify the exact hash it accepts. No research-novelty claim is made.

`LITERATURE_AND_SCOPE.md` aligns the construction with the original OWR question and distinguishes the prior divisorial examples. `SOURCE_MANIFEST.json` provides only public bibliographic and verification metadata. No copied scholarly PDFs, extracted source text, dataset contents, or private coordination files are included.

To reproduce the optional exact checks with Python and SymPy installed:

    python checks/verify_construction.py

The script checks the two moment identities, rational Taylor root enclosures, toric fan determinants, and coefficient coprimality. Several resultant calculations are additional spot checks; the proof of irrationality handles every positive rational ratio without a bounded search.

`corrections/` contains actual unified diffs. The first corrects a numerical bracket after exact checks; the later diffs make both directions of the stability/soliton citation chain explicit. These amendments are not separate substantive mathematical approaches. Intermediate proof hashes are retained in `EDITION_HISTORY.json`.
