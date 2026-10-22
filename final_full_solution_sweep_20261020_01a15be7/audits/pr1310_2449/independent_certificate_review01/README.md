# PR1310 independent certificate audit

Read `REPORT.md` for conclusions and limits. Both numerical obligations were freshly reconstructed; whole analytic/priority/publication acceptance is reserved to the root's separate adoption.

The code uses Python3 standard library only. It imports no author code. Run in this folder or use absolute program paths:

    python3 -B verify_review.py
    python3 -B verify_review.py --full

The default checks the closed byte inventory, complete privately captured PR/source identities, all three mode receipts and fresh exact/corruption controls. `--full` additionally repeats every global-family check and all 627 accepted block slabs; allow a few minutes. Both commands write no files. Supply `--manifest-sha256 DIGEST` using the independently received final digest to authenticate the manifest itself.

Individual commands:

    python3 -B check_certificate.py --global-family
    python3 -B check_block_certificate.py --replay block_result.json
    python3 -B check_block_certificate.py --full
    python3 -B check_controls.py

`--full` on the block program regenerates an adaptive cover; `--replay` freshly recomputes every stored accepted slab and compares its exact mathematical record. They can have different total guard-call counts because rejected proposal attempts occur only during regeneration. All final mode comparisons used complete numerical replay, not saved PASS fields.

The closed tail is in the family output. The block output is conditional on the separately audited analytic comparison and on global family minimality. Neither executable proves the analytic reductions, priority, all-r EHP question, arbitrary-measure theorem or supremum.

`private_sources/` contains raw third-party/PR/ledger research captures and must not be redistributed as authored work. Its gzip JSON bundle contains full source bodies, raw metadata and every exact pin; it need not be extracted to disk. `SOURCE_INDEX.json` is the compact, non-body index. Top-level `MANIFEST.json` excludes only itself and covers nested source-manifest bytes inside the private bundle. No services, Git, comments, publication records or spreadsheet rows were modified.

Extensive AI assistance; unrefereed; no external human peer review or formal proof-assistant certification.
