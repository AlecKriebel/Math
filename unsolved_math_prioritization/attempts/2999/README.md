# KP-4.123: formulation counterexample only

Rank 923, ID 2999. Original stronger problem: **unsolved, 2/5**. No novelty claim.

The Hopf-product foliation on S³ × S¹ has null-homologous torus leaves and satisfies the weak differential-form condition printed in K3. Each torus is homologous to an embedded sphere, so this literal genus-minimization formulation fails. Stokes excludes every globally closed leaf-positive form for this example. It therefore does not resolve or refute Kronheimer’s original closed-positive-form question, the S² × S² subquestion, the nonzero-homology variant, or a chi-minus-only claim.

## Contents and acceptance

- `original/` and the original archive in `audit/` preserve the exact historical author package.
- `corrected/` and its archive preserve the independently accepted derivative. Only `check.py` differs, by the actual `audit/CHECKER_SCOPE_HARDENING.patch`; no mathematical correction was required.
- `audit/EXACT_ACCEPTANCE.json` and `audit/AUDIT_REPORT.md` record the first independent artifact/mathematical acceptance.
- `second_review/` contains the fresh independent mathematical/source review and the exact corrected-archive acceptance bridge.
- `AUDIT_SAFE.zip` and all external manifests are preserved byte-for-byte. Historical “no publication” and pending-review labels describe earlier stages; they are not overwritten.
- The historical author HTTP 403 for Kronheimer’s PDF is supplemented by later successful binary retrieval and visual inspection recorded in both independent reviews.

Authored proofs, audits, code, and public verification metadata only. No copied third-party documents, source extracts, datasets, private sources, personal information, or private coordination files are included. The finite identities do not mechanize the global topology or certify arbitrary edited prose.

## Reproduction

Obtain the SHA-256 of `PUBLICATION_MANIFEST.json` from a trusted external record. Invoke `python3 -I -S -B verify_publication.py --expected-manifest HASH`, then repeat with `-O`. Do not compute a fresh trust anchor from an untrusted checkout and call that authentication. The wrapper authenticates all code before running it, checks exact file and ZIP inventories, compares extracted members, actually replays the patch, and runs both author checkers and the independent tensor checker in a relocated snapshot.

Optional complete corpus replay: supply all of `--catalog FILE --problems FILE --reports FILE`. Optional local source rehashing: supply `--source-dir DIRECTORY` containing `k3.pdf`, `kronheimer.pdf`, `ozsvath_szabo.pdf`, `scorpan.pdf`, and `bowden.pdf`. These inputs remain external and undistributed. Rehashing is not a new retrieval or a new visual inspection.

Run `python3 -I -S -B test_publication.py` for isolated normal/optimized relocation and negative controls. Fresh publication-run source/corpus checks are in `PUBLICATION_SOURCE_CORPUS_VERIFICATION.json`; historical test logs retain their original meaning.
