# Problem 2200006: audited partial bounds for isolated SOS zeros

**Unsolved; 5/5 substantive approaches used.** The exact maximum requested in
Shapiro's Problem 3 is not determined, including the concrete case
`1152 <= M(2,10) <= 29525`. The credited prior construction refutes the separate
Conjecture 4 formula `M(k,l)=k^l`; it is not an optimality result.

## Frozen records

- [Authored proof and exact controls](polynomial_2200006/README.md): ten frozen files.
- [Independent adversarial audit](polynomial_2200006_independent_audit/AUDIT.md):
  nine separately frozen files; scoped PASS with no required corrections.
- The two accompanying ZIPs preserve the exact author and audit archives.
- `PUBLICATION_MANIFEST.json` binds every other file in this publication directory.

The construction and even-degree family are prior work by DannyExperiments,
released 10 August 2026, [DOI 10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290).
No novelty, exact maximum, construction optimality, human peer review, formal
proof-assistant certification, or worldwide literature-completeness claim is made.

The general signed-gradient upper bound is `((2k-1)^l+1)/2`. Its written proof
handles degenerate isolated real zeros and positive-dimensional complex fibers
through perturbation, regular values, degree, and the isolated-root consequence
of Bezout. Finite arithmetic controls do not prove Sard's theorem, topological
degree, or Bezout, and do not replace the written mathematical argument.

The later low-dimensional manuscript's landing page was inspected, but the proof
was unavailable following an access denial. Its advertised results are not
certified here or used as premises. The historical source-inspection statements
remain the author/auditor's dated records; publication replay does not re-fetch
or re-inspect scholarly sources.

## Portable replay

Run Python 3.10+ with its standard library only:

    python3 -B verify_publication.py

The wrapper checks the strict inventory, all frozen hashes and sizes, exact ZIP
member equality, and author and independent-audit replays. It works from an
unrelated current directory or after relocating this complete folder, without
network access or external source files. The audit also runs five mutation
rejections and compares all 61 restricted-product values. It reports 23,681
author assertions and 12,396 independently implemented exact checks, including
1,720 Sturm-polynomial cases and 576 orientation-arithmetic cases.

The author and audit status fields describe their historical pre-publication
freezes, including audit-pending and no-remote-write fields. Their bytes are
preserved rather than rewritten to imply later actions occurred earlier.

Only authored mathematics, code, audit records, public references, and permitted
verification metadata are included. No third-party manuscript, PDF, extract,
raw dataset, private source, or private coordination file is distributed.

Publication checkpoint: 5 October 2026 UTC. Package preparation and the scoped
audit are complete. The exact mathematical target remains unresolved; no
percentage estimate of the unknown extremal theorem is asserted. The queue
change is limited to this row's Status and Turns. No merge, release, DOI,
external outreach, or automatic integration is part of this draft.
