# Stringy E-polynomials: audited scoped partial, 30002042

**General finiteness remains unresolved by this attempt. Status: `unsolved_by_this_attempt`, 5/5.** This is an unrefereed, AI-assisted mathematical record, with no full-solution or novelty claim.

Read [the accepted mathematical report](author/RESULT.md), [the independent audit](audit/AUDIT.md), and [the acceptance boundary](audit/ACCEPTANCE.json). The two original archives, their external manifests, their 20 extracted members, and the separately pinned author bootstrap are unchanged. No proof correction was required. Statements about pending review or publication inside the immutable originals describe earlier stages.

## What the audit accepts

- Coefficient-corner criterion; explicit reflexive triangle; zero-polynomial pyramids in every nonnegative Calabi–Yau dimension.
- Finiteness for bounded index and nonpositive Calabi–Yau dimension, with the smooth and geometric hypotheses retained.
- Scalar-growth examples and reduction to positive-Calabi–Yau integral-free-join-indecomposable factors.
- An infinite formal polynomial family satisfying the listed identities. Its realization by Gorenstein polytopes is not proved, so it is not a counterexample to finiteness.

The original OWR account leaves its `t` notation undefined beside a two-variable formula. The standard qualified degree statement is total degree `2n` or zero. Knupfer–Nill, arXiv:2609.18873v1, Theorem 1.5 was inspected as a manuscript claim; the entire Sections 3–4 decomposition proof was not independently accepted. Borisov–Li's 2015 theorem concerns the stated geometric complete-intersection setting, including the Batyrev–Borisov construction, rather than all Gorenstein polytopes. See the audit for exact source locations and public URLs.

## Verification and trust boundary

Python 3.10 or later, standard library only. Before running code, authenticate `publication_bootstrap.py` and `PUBLICATION_MANIFEST.json` against their SHA-256 values recorded outside this package in the draft PR acceptance receipt. Do not derive trust from an unverified manifest alone.

Then run, from any unrelated working directory:

    python -I -S -B /absolute/path/publication_bootstrap.py /absolute/path/package MANIFEST_SHA256 --replay
    python -I -S -B -O /absolute/path/publication_bootstrap.py /absolute/path/package MANIFEST_SHA256 --replay

Use the actual externally checked manifest hash. The publication bootstrap checks strict inventory, regular paths and ancestors, every package byte, the five original trust anchors, all archive members and extracted equivalents, and source-metadata bindings before running any archived mathematical code. It executes authenticated code bytes in isolated `-c` children; no extracted checker or sibling module is imported.

After authentication, optional additional boundary controls are:

    python -I -S -B /absolute/path/publication_controls.py /absolute/path/package MANIFEST_SHA256
    python -I -S -B -O /absolute/path/publication_controls.py /absolute/path/package MANIFEST_SHA256

The preserved audit replay has 6 positive runs, 36 negative runs, and 14 structural probes in each reviewer mode; every positive reproduces 230 author checks and 10 sanity labels. The separate independent mathematics has 4,795 exact checks per mode. The publication controls add 2 positives and 28 rejection cases per mode, including relocation, import-shadow/cache, root/ancestor/entrypoint symlinks, strict inventory, malformed manifests, and rehashed source metadata. Structural probes use explicitly test-local replacement anchors only. They never change deployment pins.

These diagnostics supplement the written mathematics. They are neither a formal proof certificate nor an OS sandbox against a malicious interpreter, trusted standard library, authenticated bootstrap, or concurrent replacement of trusted runtime components. The 10 author shortcut labels are sanity checks, not independent mathematical adversarial proofs. Source hashes authenticate retained inspected bytes; verification replay does not redownload papers or certify their proofs.

Only authored mathematics, authored audit/verification code, calculated diagnostics, and bounded public verification metadata are included. Source PDFs, extracted source text, rendered source pages, raw datasets, private sources, and private coordination are excluded. The live curated problem page was not verified. No CI success, merge, release, DOI, or external outreach is implied.

## Publication checkpoint

2026-10-06: accepted scoped partial and source correction; five approaches exhausted. Best-guess completion of a full resolution: 0% certified, because the unrestricted finiteness conclusion remains unproved. Publication packaging and remote readback are recorded separately from mathematical completion in the draft PR receipt.
