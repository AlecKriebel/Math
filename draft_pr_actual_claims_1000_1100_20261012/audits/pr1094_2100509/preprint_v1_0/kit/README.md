# Real-spectrum compact-support classification: portable supporting kit

This kit accompanies Alec Kriebel's *A torus-collar proof of the real-spectrum compact-support classification for Nijenhuis operators*, version 1.0, prepared 15 October 2026. ORCID: https://orcid.org/0009-0001-9320-500X.

The paper supplies a complete proof of the historical Problem 5.11 as printed in arXiv:1804.03737v2 (p. 29; v1 Problem 4.10 p. 37, originally posed in 2018). In every dimension n >= 1, every prescribed numerical real Jordan matrix is realized in a commuting local frame on a nonempty open Euclidean domain by a globally smooth compactly supported real Nijenhuis tensor. Nonreal spectrum is impossible. Type, rank and eigenvalues can change elsewhere; fixed Cartesian matrix, global regularity and analytic compact support are outside the theorem.

The nonreal obstruction, real semisimple/two-dimensional examples, local arbitrary-type point realizations (BKM author-v2 Theorem 4.5 and p. 28 remark), and the local splitting/holomorphic mechanism are credited prior results. Geometry III's published Theorem 1.10 is author-v1 Theorem 1.4; its regular layers near a nonzero nilpotent block do not themselves supply the compact zero transition. Geometry IV permits singular/zero symmetries but retains functional coefficient equations. The full result's and construction's historical priority, novelty and worldwide preexisting openness are UNKNOWN. The manuscript preserves the author-v2 rigidity-proof qualification and does not identify unread publisher bytes with that version. `historical/reviews/priority_01/SOURCE_READ_LEDGER.json` gives exact reading scopes and unresolved source bodies, including the 2025 Sbornik and 2026 cohomology works.

AI tools were used extensively in solving, verification, source comparison and writing. This is unrefereed, without external human peer review, journal acceptance or formal proof-assistant certification. The complete general proof is in `paper.tex` and `paper.pdf`. Finite controls corroborate it; they are not an all-dimensional proof and do not replay or certify the original omitted programs or historical counts.

## Commands

Use Python 3.10+ and its standard library. Run from the extracted kit root. Every output target must be absent; use a fresh sibling directory or filename. Do not redirect shell output onto an input: shell redirection occurs before Python can guard it. The guards protect all program-controlled paths, reject existing destinations (including hardlink aliases), reject leaf and ancestor symlinks before resolution, reject input-tree overlap, check every existing output ancestor against the protected kit's device/inode identity (including case aliases on a case-insensitive filesystem), and create subprocess outputs only inside one fresh directory. Safe ordinary `../` sibling destinations remain supported; a symlink component followed by `..` is rejected before normalization. These are ordinary accidental-overwrite guards, not a defense against concurrent hostile filesystem mutation.

```sh
python3 -B scripts/verify_kit.py
python3 -B scripts/run_checks.py --out ../new-checks.json
python3 -B scripts/build_support.py --out ../new-support.zip
python3 -B scripts/build_pdf.py --out-dir ../new-pdf
```

Repeat with `python3 -B -O` and different absent targets. Checks use explicit exceptions and remain enabled in optimized mode. `build_pdf.py` additionally needs Tectonic and its TeX bundle; the kit does not claim to bundle that compiler/runtime. It rejects overfull boxes. Always inspect every newly changed PDF page visually. Reproducible PDF bytes were checked in the recorded preparation environment with `SOURCE_DATE_EPOCH`; other compiler/font versions can differ. Stored ZIP bytes are deterministic from this exact payload using fixed member order, timestamps and mode headers.

`verify_kit.py` first preflights all input members and the self-excluded `MANIFEST.json` as regular files with no symlink components. It verifies exact inventory/hashes, metadata equality and the historical copy partition. A manifest is an integrity inventory, not independent authentication: use the external preparation/output pins to authenticate its bytes. Historical manifests are retained as captured evidence and are not represented as live full inventories of this selected kit.

An extracted kit normally has no `../DEPOSIT_BINDING.json`: this default absence is explicitly allowed. An explicitly selected, required or present binding is always strict. For the canonical delivery folder, from the kit run:

```sh
python3 -B scripts/verify_kit.py --require-binding
python3 -B scripts/verify_kit.py --binding ../DEPOSIT_BINDING.json --require-binding
```

The strict check verifies external paper/ZIP hashes, every archive header/member and CRC, exact PDF identity, exact native uploader metadata and selected assets. A present corrupt binding cannot silently fall back to absent mode. A missing explicitly selected binding fails.

## Package and historical evidence

`CUSTODY_MAP.json` partitions every audit input captured before the 16 October 2026 repair individually into an exact selected authored copy or an exclusion. Its original 171-input stage remains intact as dated history. Selected whole-review/root evidence and the original bytes of every changed interface are appended under `historical/repair01/`; changed original paths resolve to those explicit before-repair copies. Source PDFs, extracted third-party text, images, raw private searches and duplicate snapshots are excluded. No source body is redistributed. Public source hashes and actual read scopes are retained. `historical/` contains exact dated submitted/reviewer/root evidence: its acceptance labels and pending fields retain captured-stage meaning. They do not override `CURRENT_STATUS.json` or claim that new whole-package reviews are complete. Historical executable environments are neither copied nor declared portable. The newly written `scripts/run_checks.py` is the portable checker.

`metadata.json`, `.zenodo.json` and `metadata_api.json` encode one identical Zenodo API metadata object. The external native `zenodo-deposit.json` has exactly the repository uploader's `{metadata, files}` schema and selects the paper PDF and support ZIP. Its metadata equals the bare/API objects. The external `DEPOSIT_BINDING.json` binds those exact deliverables without a hash cycle; neither descriptor is inside its own selected ZIP. No DOI, external publication or PR merge is claimed at this stage.

Copyright Alec Kriebel, 2026. Paper, authored notes and code: CC BY 4.0; see `LICENSE.txt`. Cited third-party works retain their own rights.

## Current repair checkpoint (16 October 2026 UTC)

One new complete whole-package review has finished. It accepted the complete
mathematics and conservative priority framing, with one P3 mismatch between
the advertised lexical symlink rejection and the shared path checker. This
bounded repair checks lexical prefixes before normalization and also rejects
physical input-tree aliases through differently cased existing ancestors.
The manuscript, PDF and every native bibliographic metadata field are
unchanged. The first review and original preparation receipts are exact
captured-stage history. A NEW complete independent whole-package review is
still required, with a minimum of two total new complete reviews and all
actionable findings resolved. Readiness and publication remain false, and
all external services remain held after the preceding PR #1032 disposition.
