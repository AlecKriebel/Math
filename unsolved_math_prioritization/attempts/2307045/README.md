# Equal radial slits: published prior resolution

Problem **2307045 / AMR-022-7045**, rank **690**, Hayman–Lingham Problem 7.45.
Disposition: **already_solved**, authored effort **1/5**. No novelty claim.

V. N. Dubinin's Theorem A (Russian original 1984; English translation 1985)
settles the full original equal-length radial-slit problem. For p distinct
boundary-attached straight radial cuts of common length 0 < ell < 1, equally
spaced directions uniquely minimize outer-circle harmonic measure at zero,
up to rotation and relabeling. The minimum is

    (4/pi) arctan((1-ell)^(p/2)).

There is no endpoint uniqueness claim: ell = 0 gives an uncut disk, and ell = 1
removes the evaluation point. Unequal, curved, interior or disconnected cuts
are outside scope. The [authored proof](author/PROOF.md) gives normalization,
boundary complementation and the regular-configuration value; arbitrary-angle
comparison and its equality classification rely on the cited published theorem.

The [complete independent audit](audit/AUDIT.md) passes source matching,
mathematical normalization, branch choice, harmonic pullback at the critical
origin, multiplicity and endpoints. **The original comparison proof was inspected
through OCR-damaged primary text, not fully symbol-by-symbol audited.** Dubinin
PDF-byte retrieval and page-image inspection failed; neither is claimed here.
The [source audit](audit/PUBLIC_SOURCE_AUDIT.json) preserves those limitations.

## Reproduce

Only Python 3.10+ and its standard library are needed. From any working directory:

    python3 path/to/2307045/verify_publication.py --replay --selftest
    python3 -O path/to/2307045/verify_publication.py --replay --selftest

The strict wrapper checks exact inventories, manifests, bytes, hashes and claim
metadata. It invokes frozen assertion-based controls in isolated, unoptimized
subprocesses, including when the wrapper is run with -O. Replay writes occur in
disposable copies. It reproduces 3,186 authored exact control instances and 25
separately labeled floating configurations, plus 15,217 independent exact
assertions and six certified rational value intervals. The original checker's
two floating diagnostics retain its documented platform tolerance. These are
finite controls, not a formal proof or a replacement for the global comparison.

All nine author files and nine independent-audit files are preserved byte for
byte. Their older pending/remote-write fields describe their original freeze;
[BINDING.json](BINDING.json) records this later publication assembly. The
[publication manifest](PUBLICATION_MANIFEST.json) binds the entire safe package.
The independent audit archive hash is metadata only; the complete safe audit is
included in expanded form. No source PDF, page image, extracted source text,
dataset contents, private sources or coordination files are redistributed.

Fresh bounded repository searches found no prior target attempt. They do not
establish exhaustive absence in deleted refs, private chats or unindexed files.
Expected dataset hashes remain metadata, with no fresh full-corpus match claim.
Only the target QUEUE row's Status, Turns and previously blank Findings change.

Sources: [Hayman–Lingham, Problem/Update 7.45, p. 174](https://arxiv.org/abs/1809.07200v2);
[Dubinin, journal theorem](https://www.mathnet.ru/eng/sm2051);
[English paper DOI](https://doi.org/10.1070/SM1985v052n01ABEH002888).
