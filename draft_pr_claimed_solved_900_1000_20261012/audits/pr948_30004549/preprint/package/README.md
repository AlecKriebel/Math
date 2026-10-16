# Three anti-invariant classes on a nonintegrable four-manifold

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.
Version 1.0, October 16, 2026. CC BY 4.0.

The research note constructs a closed smooth real four-manifold with a
nonintegrable almost complex structure and three independent real closed
anti-invariant de Rham classes. It answers the unrestricted Draghici--Li--Zhang
integrability conjecture negatively. It also gives a family converging smoothly
to a product complex structure, with deformation supported in one ball.
The earlier generic-vanishing theorem belongs to Tan, Wang, Zhang and Zhu.

The note and supporting package are unrefereed. AI tools were used extensively
for construction, drafting, literature search, symbolic checks and adversarial
review. No independent human peer review, formal proof certification, first
priority, novelty or present-open-status certification is asserted. The bounded
priority audit found no verified qualifying predecessor and records substantial
version and access limitations. An earlier qualifying result would affect
priority even if it lacked this construction's support or convergence features.

## Contents and evidence

In the supporting archive, `paper/note.pdf` and `paper/note.tex` contain the
complete mathematical argument. `original/` contains all 24 files at PR948
head `be4313efafa1af5962394e07d8a4debff2e94d92`, unchanged in bytes and in
their recorded Git regular-file mode. `audit/` contains selected independent
AI audit reports, finite checks, source maps and actual query/reading records.
It excludes raw corpus records, copied third-party manuscript bodies, private
fixtures, credentials, external runtimes and caches.

`profile/` is a new strict finite verification entry point, separate from the
historical wrapper in `original/`. Its development history retains the first
known directory-alias defect and the corrected 85-event test run. Historical
reports and copied seals describe their original scope, time, absolute paths
and disk modes; they are evidence records, not fresh approvals of this note.
Package copies are regular files with permission 0644. Copying a report does
not recreate its private inputs or imply that every hashed source was read.

The PR declares 4/5 author turns. The earlier native per-turn history and total
were not authenticated; the audit adds zero substantive author proof responses.
See `AUTHORSHIP_PROVENANCE.md`, `AUDIT_LIMITS.md` and `FINDING_DISPOSITIONS.json`.
The separate `FULL_PACKAGE_REVIEW_DISPOSITIONS.json` tracks findings from
complete publication-package reviews in addition to the 50 earlier findings.
`audit/full_package_01/` preserves the first complete adverse review of the
previous candidate. It verified the theorem and found a workflow recovery
defect; its verdict is not an acceptance of this corrected candidate. Copied
historical probes describe the exact earlier repository inputs and outputs.
They are evidence to inspect, rather than current verification entry points.
The post-review comparison-base amendment of the existing ROOT02 finding is
documented in `audit/root_status_context/`. Its synthetic witnesses concern
which PR is eligible for review; no excluded PR or mathematical source was
processed. The unchanged manuscript needs no mathematical repair for it.
A later live check and exact-code witness in audit/root_live_base_context/
distinguish the PR associated baseRefOid from the live branch pointer
baseRef.target.oid. Only a matching independently recorded head and live
branch pointer justify reusing a cached identity; otherwise complete current
filenames must be derived. Earlier gate versions remain historical evidence,
including the initially insufficient associated-base-only fix.

## Reproduce the finite checks

Obtain the package-manifest SHA256 from an independent release record, such as
the repository's externally anchored build/freeze receipt or the publication
record description. Do not trust a rewritten manifest or a checksum supplied
only alongside rewritten payloads. Independently authenticate the driver too.
After extracting into a real directory with regular single-link 0644 files:

```text
TRUSTED_PYTHON -I -S -B profile/verify_package.py --root /absolute/package --manifest-sha256 EXTERNALLY_OBTAINED_64_LOWERCASE_HEX
TRUSTED_PYTHON -I -S -B profile/verify_package.py --root /absolute/package --manifest-sha256 EXTERNALLY_OBTAINED_64_LOWERCASE_HEX --run-checkers
```

Default inventory verification uses the Python standard library. Replaying the
three fixed checkers needs trusted installed SymPy 1.14.0. Actual execution was
tested on CPython 3.14.6 and SymPy 1.14.0; other interpreters and platforms are
untested. Child interpreters use `-I -B` and allow trusted installed site
packages. There is no hostile-dependency or operating-system sandbox. Read
`profile/README.md` for exact limits and the development-test invocation.
All test output must go outside the closed package tree.

The finite symbolic checks corroborate local identities. They do not prove
global smooth gluing, compactness, cohomological independence or literature
priority. Those claims require the written proof and bounded source analysis.

## Rebuild the note

Use a trusted LaTeX installation with amsmath, amssymb, amsthm, geometry and
hyperref. For example, from a writable directory outside the closed package:

```text
tectonic --untrusted --outdir /absolute/output /absolute/package/paper/note.tex
```

The audit build used Tectonic with `--only-cached --untrusted --keep-logs`,
then rendered and personally inspected all five PDF pages. PDF bytes may vary
with compiler and font versions. The archived source is the mathematical
reference; byte identity is expected only for the distributed PDF itself.

Reviews of this corrected candidate, acceptance and publication/readback
receipts are externally anchored repository evidence. They remain outside
this closed tree to avoid recursive self-approval and self-hashing. At least
two new consecutive complete clean reviews are required after every repair;
earlier unfinished, failed and adverse records must remain honestly preserved.
