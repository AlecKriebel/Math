# Version 2.0.0 release-candidate checks

**Freeze/check date:** 2 August 2026 UTC  
**Scope:** local release assembly and verification only; no publication,
GitHub, Zenodo, browser, or external-communication action was performed here.

## Frozen artifact anchors

```text
fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b  output/pdf/manuscript-v2.0.0.pdf
b7429aed0e5edf572848cbcf856b3da89ff05447967c3dc12d9d386e0270f3d2  audit_packet/specialist_audit_one_page.pdf
e2ac3cf9556eb1bacf53a76dd09963a5a60ca2d47c7fe2c62a0bdfa164dd18db  source/MANUSCRIPT_V2.md
2957ee7486e4a3e16c93c2c0d739ba797d14244e125ff7f58fad76757f3621ec  priority_v2/AUDIT.md
f10a7ed2b66e3f18952bdebbaca90a35aecfaf54c17e5b31a2f1436a4ed7536e  audit_v2/audit_results.json
f7061a40fefd9ca2285f83ba64ce9af63cb76a45a69aca95beb5fbfb17465486  family/remainder_matrix.csv
```

`verify_release_metadata.py` independently checks these anchors on every
replay.  It also verifies that the two copies of `rates.csv`, the frozen-v1
reaction table, both machine-readable rate vectors, and all twenty symbolic
family formulas agree exactly.

## Software environment

The local checks used:

```text
CPython 3.14.6
SymPy 1.14.0
mpmath 1.3.0
macOS-26.5.2-arm64-arm-64bit-Mach-O
pandoc 3.10.1
pdfinfo / pdftoppm 26.05.0
Info-ZIP 3.0
bsdtar 3.5.3 / libarchive 3.7.4
```

The only Python dependencies are pinned exactly in `requirements.lock`.

## Full exact replay

From the release root, the command was:

```sh
./reproduce.sh
```

It created an isolated `.venv-release`, installed the two locked packages,
and returned exit status `0`.  The exact terminal conclusions were:

```text
PASS: Version 2.0.0 package metadata and byte anchors agree
PASS: all exact construction checks succeeded
PASS: all clean-room exact checks 1--17 succeeded
PASS: exact fixed-support family checks succeeded
PASS: exact clean-rate and transverse-stability checks succeeded
PASS: exact complexity-arithmetic checks succeeded
PASS: independent v2 audit succeeded
PASS: all exact v2 manuscript claims succeeded
PASS: all Version 2.0.0 release verifiers succeeded
```

The independent v2 gate additionally reported:

```text
family matrix rank/nullity: 16/4; asserted minor exact
positive cone and both interior rate specializations: exact
original and clean affine/homogenized gcds: 1
fixed-support integer minima: max=10296, sum=52464
original and clean steady ideals: radical conic + 15 points
Sturm counts: roots(T,E,N)=(0,0,2); transition intervals exact
```

## Fresh extraction and reproduction

The standalone verifier archive was built without local environments, caches,
temporary renders, or stale draft PDFs.  Its frozen SHA-256 before extraction
was:

```text
d13d0400afde27bb444133283957aa5b699928549b36b62024c2c07d3ce5e6e1  dist/wr-continuum-v2.0.0-verifiers.zip
```

The exact fresh-run commands were:

```sh
extract=$(mktemp -d /tmp/wr-v2-extract.XXXXXX)
unzip -q dist/wr-continuum-v2.0.0-verifiers.zip -d "$extract"
"$extract/wr-continuum-v2.0.0-verifiers/reproduce.sh"
```

The extracted archive downloaded only the two locked Python wheels (from the
local package cache in this run), recreated its own environment, and again
returned exit status `0` with every `PASS` line listed above.  The extraction
root for this check was
`/tmp/wr-v2-extract.C5SMvs/wr-continuum-v2.0.0-verifiers`.

Before extraction, this command returned no forbidden entry:

```sh
zipinfo -1 dist/wr-continuum-v2.0.0-verifiers.zip |
  rg '(^|/)(\.venv|tmp|__pycache__)(/|$)|manuscript-v2-draft\.pdf|\.pyc$|\.DS_Store$'
```

The final complete archive was separately extracted into a new temporary
directory.  Its root `SHA256SUMS` verified every payload byte, after which its
own `./reproduce.sh` again returned exit status `0` at all eight executable
gates.  Thus the complete archive and the smaller verifier archive were each
tested from fresh extraction roots.

## PDF checks

`pdfinfo` reports:

| Artifact | Pages | Size | Page format | Forms | Encryption |
|---|---:|---:|---|---|---|
| Manuscript | 14 | 108423 bytes | US Letter | none | no |
| Specialist handout | 1 | 5201 bytes | US Letter | none | no |

Both final PDFs were rendered with `pdftoppm`; all fourteen manuscript pages
and the one-page specialist handout were inspected at high/original detail.
No clipped text, overlap, broken table, missing glyph, bad page transition, or
header/footer defect was found.  The temporary PNG render tree was moved out
of the release before checksumming and archiving.

Immediately before packaging, the manuscript PDF was rebuilt successfully
from the frozen source with Pandoc and Tectonic.  The rebuilt byte stream has
the anchored SHA-256 above.  Its exact source, Pandoc metadata, Lua filter,
TeX header, and build scripts are all included in the candidate.

## Metadata and omission checks

The following all succeeded:

```sh
python3 -m json.tool data/release.json
python3 -m json.tool data/rate_vectors.json
python3 -m json.tool data/theorem.json
python3 -m json.tool audit_v2/audit_results.json
```

`CITATION.cff` parsed as YAML.  It has no DOI identifier.  `data/release.json`
has `"doi": null` and the explicit status
`"not_minted_at_release_candidate_freeze"`; no Version 2 DOI is claimed.
The repository-wide concept DOI and Version 1 DOI appear only where their
scope is explained.  The theorem metadata labels the unattained support
values as **proved lower bounds**, not as attained minima.

Immediately before the final checksum pass, the release tree was checked for
and contained none of:

- `.venv-release` or another local environment;
- `tmp/` or rendered PNG intermediates;
- `__pycache__`, `.pyc`, or `.DS_Store` files;
- `manuscript-v2-draft.pdf`; or
- any file from the immutable `releases/v1.0` directory.

The root `SHA256SUMS` covers every non-archive release file except itself.
`dist/SHA256SUMS` covers the three distribution archives.  Archive integrity
is therefore independently checkable without trusting this prose report.
