# Independent v1.0.9 preprint rereview

Start with `REFEREE_REPORT.md`. The recommendation is minor revision in four bounded areas, with no new defect found in the central theorems. The report identifies exact repairs and scopes every validation claim.

The only manuscript version evaluated is commit `94d5177485b9680be8b77f13448abf1f923963e8`. Later commits containing this referee packet do not change that target. No paper source or immutable release was changed by the review.

## Recreating the evidence

The source snapshot and disposable build/rendering directories are intentionally excluded from Git. In a checkout containing the target commit, run `python3 recreate_snapshot.py` from this folder to recreate and verify the 1,372-file source snapshot. This reads the local Git archive, checks the complete archive and per-file SHA-256 values, and refuses to replace an existing snapshot.

The algebra and PDE programs are standalone SymPy checks that import no production implementation. Run the `.py` programs named in their respective reports using Python with SymPy. Saved results and logs document the completed runs; the finite checks are distinguished from the general proofs.

`check_audit_evidence.py` checks every snapshot byte and independently reconstructs the near-threshold cubic and crossing Bernstein-basis evidence by solving for coefficients. It also checks the compact document and release-asset counts. Its recorded result is `ROOT_EVIDENCE_CHECK.json`.

`documents/render_and_inventory.py` recreates the PDF contact sheets using Poppler and Pillow. Rendered images are local inspection products, not released manuscript edits. The saved extracted text and `PDF_INVENTORY.json` identify all 96 inspected pages.

For the software replay, read `software/SOFTWARE_REPORT.md` and the recorded pinned environment first. Its driver exposes setup, tests, verifiers, portable, packages and detached actions. Override the documented environment paths when reproducing on a different machine. The mathematical witness `software/check_variable_order.py` uses a disposable copy, and `software/check_pdf_gate.py` additionally needs the previous commit's supplement for its historical collision control.

The remote GitHub release checks read and downloaded assets; they did not change the release. `software/RELEASE_ASSET_INTEGRITY.json` records all nine byte comparisons. The optional historical-lineage inputs were unavailable; the separate current replay completed successfully.

The timestamps and completion estimates in the research logs refer to completion of this referee round, not to a percentage certainty that a theorem is true.
