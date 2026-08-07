# Author-ready release, version 1.1.1

This directory contains the journal submission and exact computational
supplement for Alec Kriebel's paper *Generic Identifiability of Strongly
Tree-Child Level-2 Jukes--Cantor Networks*.

The theorem covers all binary standard semi-directed `S_TC` level-2 networks
under the open four-state Jukes--Cantor model, modulo ordinary triangle
redirection. A separate graph theorem proves that every binary `W_TC`
level-2 topology automatically has at most one triangle per blob, so no
triangle-count hypothesis remains. The sharpness result gives an all-`n`
non-triangle ambiguity in `W_TC \ S_TC`. The reconstruction theorem returns
a canonical structural class modulo ordinary triangle redirection; it does not
claim that every redirected orientation contains one fixed input distribution.

## Submission files

- `submission/Generic_Identifiability_STC_Level2_JC.pdf`
- `submission/LaTeX_TikZ_Source.zip`
- `submission/STC_JC_Reproducibility.zip`
- journal-specific and generic cover letters
- `submission/Referee_Guide.pdf`

## Verification

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
```

The first is a submission/build check. The second independently rebuilds the complete automatic-triangle rooting universe in Python and C++, and verifies every unchanged statistical/atlas byte against its preserved clean full-adversarial transcript. The optional `verify_regenerate_all.sh` reruns every large algebra generator and directed join from scratch. See `reproducibility/RUNTIME.md` for
resource expectations.

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

Every other file, including all theorem-bearing certificates, the primary
verifier, and both independent reviewers, is present and was independently
rerun before this git mirror was published; see
`reproducibility/GIT_MIRROR_VERIFICATION.txt`.
