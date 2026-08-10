# Repair branch — submission withheld

This directory is undergoing a fail-closed mathematical and reproducibility
repair.  The former version 1.1.1 positive-classification release is
**withdrawn**: its bridge chart and finite-atlas promotion were not certified
at the strength required by the manuscript.  The global standard
strongly-tree-child level-2 Jukes--Cantor theorem is presently **unresolved**,
not refuted.

The currently established result is the all-`n` sharpness theorem for the
explicit Theta family in `W_TC \ S_TC`, together with its exact stochastic
and rank certificates.  It is not a counterexample in the standard `S_TC`
class.

The authoritative repair status and gate ledger are:

- `repair/STATUS.md`
- `repair/DEPENDENCY_GATES.md`
- `repair/RESEARCH_LOG.md`

Nothing under `submission/`, `source/paper/`, or
`reproducibility/exact_release/` should be submitted or cited as a completed
positive theorem until every repair gate is independently verified and this
notice is replaced by a coherent release.

## Historical withdrawn files

- `submission/Generic_Identifiability_STC_Level2_JC.pdf`
- `submission/LaTeX_TikZ_Source.zip`
- `submission/STC_JC_Reproducibility.zip`
- journal-specific and generic cover letters
- `submission/Referee_Guide.pdf`

## Historical verification commands

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
```

These commands belong to the withdrawn version 1.1.1 bundle.  A successful
run is not evidence for the global theorem: parts of that bundle attest frozen
bytes or conditional status records.  Replacement fail-closed commands will
be published only after the mathematical repair closes.

Licenses: manuscript text and figures are CC BY 4.0; code is MIT. No persistent
archive identifier is claimed in this local release; the author should insert one
after depositing the final bytes. The
`MANIFEST.sha256` file is an integrity control, not a mathematical proof.

## Note on this Git mirror

Three files from the original author-ready release are intentionally omitted
here because they exceed practical Git hosting limits or duplicate bytes
already present unpacked elsewhere in this directory:

- `submission/LaTeX_TikZ_Source.zip` and `submission/STC_JC_Reproducibility.zip`
  are zipped copies of `source/paper/` and `reproducibility/`, which are
  already present unpacked; both zips are covered by `MANIFEST.sha256` and can
  be regenerated with `reproducibility/build_component_archives.py`.
- `reproducibility/publication/certificates/theta_k6_weak_signatures.bin`
  (SHA-256 `92db30fa49ee4603ff27256d10898f785c42a252b4180503391ec09b175bb711`,
  recorded in `MANIFEST.sha256`) is a 175&nbsp;MB exhaustive signature dump used
  only by the optional `reproducibility/verify_regenerate_all.sh` full
  regeneration path, not by `verify_quick.sh` or `verify_full.sh`. It can be
  regenerated from `reproducibility/publication/src/regenerate_signature_relation.cpp`.

The omissions listed above remain relevant to reconstructing the historical
bundle, but the historical manifest and verifier hierarchy are not an
authoritative proof ledger for the repaired project.
