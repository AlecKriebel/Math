# Final-audit research log

## 2026-08-01 18:15--18:30 PDT

- Began hostile audit of the expanded Paper I and the included symmetric
  `K_4` certificate.
- Compared the orbit formulas and all displayed `F_13`, `P_13`, `C_k`
  coefficients against `phase2_n4/n4_symmetric_classification.md` and its
  hostile audit.
- Ran `phase2_n4/derive_lumped_certificates.py` and
  `phase2_n4/crosscheck_full_chain.py`; both passed exactly.
- Compared the new support-degree proposition against
  `phase3_asymptotic/REPORT.md` and its hostile audit.
- Identified two scope omissions in the then-current draft: the sequence
  proposition did not restate the connected-undirected graph class, and the
  repeated-gadget consequence omitted the bounded-total-support caveat.
- Reported both defects to the parent researcher. They were repaired in the
  frozen source.

## 2026-08-01 18:30--18:43 PDT

- Rebased the audit several times while publication metadata and layout
  changes were integrated concurrently.
- Confirmed the final mathematical source hash
  `b0e066fa...` and final `K_4` fragment hash `c27538cc...`.
- Audited the newly added `G_13` and `G_22` TikZ diagrams edge by edge.
- Compiled the final source with Tectonic. The two-pass log was clean.
- Rendered every PDF page to PNG and visually inspected all 13 pages.
- Compared independent-build and checked-in PDF rasters; all 13 page images
  were byte-identical at the audit resolution.

## 2026-08-01 18:43--18:51 PDT

- Ran the full non-PDF verification aggregate:
  `make test verify directed triangle n4 phase3-check`. All targets passed.
- Verified that the checked-in paper PDF and installed output PDF have the
  same SHA-256, `d77a0018...`.
- Checked the manuscript's newly added release-availability claim. GitHub
  reported `release not found`, and no local release tag exists. Recorded
  actual release creation (or a tense change) as the sole publication
  precondition.
- Final mathematical and TeX verdict: PASS.
