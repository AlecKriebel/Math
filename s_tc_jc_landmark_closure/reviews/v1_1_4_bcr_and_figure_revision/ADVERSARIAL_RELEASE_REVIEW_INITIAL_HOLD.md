# Initial adversarial release review

Status: **HOLD — preserved pre-repair verdict**

The independent release reviewer found one fail-open verifier boundary and
two audit-provenance defects in the first v1.1.4 candidate.

1. `verify_submission_source_archives.py` accepted any internally
   self-consistent verifier capsule.  Deleting
   `reproducibility/verify_active_release.py` and recomputing the capsule's
   internal `SHA256SUMS` therefore escaped.  The reviewer required an
   independently declared exact mandatory-member set and a mutation test that
   removes and re-seals one required inner member.
2. `PDF_VISUAL_AUDIT.md` incorrectly said that source ZIPs reproduced all
   eight PDFs.  The ZIPs reproduce six article/supplement PDFs; the two
   standalone cover-letter TeX sources reproduce the remaining PDFs.
3. The visual audit named its renderers but did not record exact versions and
   rendering options.  The reviewer required those details or retention of
   every individual rendered page.

The reviewer independently confirmed that the source archives reproduced the
delivered PDFs, Figure 7 was fixed in all manuscript variants, the
bibliography changes propagated, fonts were embedded, package manifests were
internally coherent, v1.1.3 history was unchanged, all seven targeted v1.1.4
mutations were rejected, the upload routes were coherent, and no unissued DOI
was claimed.

This HOLD is part of the correction record.  It is not a release verdict.

HOLD
