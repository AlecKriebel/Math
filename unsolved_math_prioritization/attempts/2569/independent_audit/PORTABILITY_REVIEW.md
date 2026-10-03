# Narrow publication-portability review: PASS

Reviewed the exact 25-file publication allowlist in `PUBLICATION_FROZEN.local.json`, SHA-256:

`a8e10eb883245a6a371f6d780623e060dc8c9ecbaa1fa4e6d837f287899db319`.

This is a packaging/input-portability review of the already-audited candidate. It is not another author attempt, a new mathematical search, human specialist verification, or authorization for remote writes. No publication files or original frozen files were changed.

## Checks completed

1. Every public allowlist entry matches its recorded byte length and SHA-256. The public `MANIFEST.json` describes exactly the same files, excluding itself. The main proof is byte-identical to the original frozen proof, with SHA-256 `3ceab2f387baa3d61c15805cdde7d8154c8350e2b3b4bf2ce187ec53b99ec299`.

2. Re-ran the original Table 5 extraction against the previously audited local source. The portable JSON contains exactly the same **60 ordered permutation records and 180 exact rational coefficients**. It properly specifies zero-based permutation images and credits Johnston–Rumynin, arXiv:2507.21316v2, Table 5, with its source URL. No coefficient was added, dropped, reordered, or changed.

3. Compared the original and portable verifier text. All mathematical code regions are byte-identical: quaternion generation and isomorphism checks, actual representations and character orthogonality, FS indicators, modular representations and matrix spans, Cartan calculation, idempotent multiplication and simple-top checks, explicit projectives and central ranks, rational witnesses, and mathematical output construction. There are 47 assertions in each script. The only substantive input changes are the verified JSON in place of the source-text parser and the unchanged-proof hash in place of private snapshot-manifest bookkeeping. No mathematical check was removed.

4. Compared every original mathematical output field with the portable output; they agree exactly. The removed fields are only `manifest_sha256` and `allowlist_files_checked`; the sole new field is `proof_sha256`.

5. Copied only the 25 allowed files into an isolated replay directory, without source text, source PDFs, the private frozen manifests, or other original audit inputs. The portable verifier completed successfully. Its generated JSON is byte-identical to the proposed public `independent_results.json`. Thus the documented Python/SymPy replay genuinely works from the published inputs alone.

6. Reviewed the adapted audit report, README, status, research log, publication note, portability note, and public manifest. They preserve the candidate status, separate contributor from fresh reviewer, acknowledge AI involvement, explicitly exclude human specialist/formal certification, and make no priority claim. The C₂ warning and its qualification remain intact. The stated completion percentage is expressly limited to production of the candidate artifact. The author argument and original review remain unchanged separately.

7. The public allowlist contains mathematical deliverables, cited coefficient data, code, result JSON, and attribution/review material. It contains no source PDFs, extracted source text, source screenshots, operational receipts, or private source/manifest paths. A targeted scan found no embedded workspace/root paths or private bookkeeping identifiers.

## Required repairs and publication boundary

**Required repairs: none.** The exact 25-file package passes this narrow review.

One extra file exists on disk: `independent_audit/__pycache__/independent_audit.cpython-312.pyc`. It is **not** in either allowlist and was excluded from the isolated replay. Publish the exact allowlist; do not recursively include this cache or any other unlisted files. The narrow review itself is outside the reviewed publication allowlist.

A minor README pronoun (“It reconstructs” after naming two commands) could be polished later, but it does not alter the mathematics, reproducibility, or qualifications and is not a blocker. No editing/re-freezing is required for this review's PASS.
