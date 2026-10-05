# 30001408: extended-valued homogeneous valuations

**Unsolved; five of five substantive approaches used. Unrefereed, AI-assisted partial research.**

## CONTROLLING mathematical correction: read first

This publication explicitly adopts [CORRECTION.md](audit/CORRECTION.md) as the **authoritative, complete replacement** of the bound paragraph in [the frozen RESULT.md, Section 5](author/RESULT.md#5-curvature-density-approach-what-it-excludes-and-what-it-assumes). The original paragraph is mathematically false as written. This is a required mathematical repair, not a citation clarification or an unconditional audit pass.

Concavity, g(0)=0, and sublinear growth alone do not exclude alpha=0: g(0)=0 with g(s)=c>0 for s>0 is a counterexample. The finite representation theorem separately requires the actual right limit g(s) -> 0 as s decreases to zero. That missing condition must be imposed. It is not established here for arbitrary extended-valued valuations.

### Full controlling replacement

For c>0 and g(s)=c s^alpha on s>0, impose the finite representation theorem's actual endpoint assumptions: g is concave on [0,infinity), g(0)=0, lim(s down to 0) g(s)=0, and lim(s to infinity) g(s)/s=0. These conditions hold exactly when 0<alpha<1, equivalently -n<q<n for alpha=(n-q)/(2n). Indeed, on s>0 the second derivative has the sign of alpha(alpha-1), so concavity requires 0<=alpha<=1. The right-limit condition at zero excludes alpha=0 because c>0, and sublinear growth at infinity excludes alpha=1 because g(s)/s=c. Conversely, when 0<alpha<1 the power is concave, extends continuously by zero at zero, and has sublinear growth. The right-limit condition is essential: assigning g(0)=0 alone does not imply it. These are additional hypotheses of the finite representation theorem, not consequences established here for an arbitrary extended-valued valuation.

The [correction](audit/CORRECTION.md) proves the replacement, gives the exact counterexample, and traces all downstream dependencies. The alpha=0 exclusion from the separate superellipsoid argument remains valid independently. The original files are immutable provenance, not a competing authoritative version. The original paragraph is exactly 275 UTF-8 bytes, excluding its terminating newline, at line 127; SHA-256 `9e99172a34672df479a076a0470045f6d69cbd6b578422c2d941b1adec1c8f8e`. The replacement is 869 bytes with SHA-256 `448c4ecb1a4c9baa7deb7c3d2b054b59750b8ca2dd7ffafa7909c0a042edc7dc`. [BINDING.json](audit/BINDING.json) records the exact binding.

## What remains established, and what remains open in this attempt

- The literal source asks for upper semicontinuity. Ludwig's neighboring conjectures use lower semicontinuity; no source correction is assumed.
- Strictly positive and nonnegative codomains are kept distinct. Only positive dilations and origin-interior bodies are used.
- The higher-dimensional result is a Boolean infinite-support reduction, explicit rejected constructions, and conditional curvature-ansatz exclusions. It is not a higher-dimensional classification or a construction of a mixed finite/infinite example.
- A complete one-dimensional classification is proved separately. It does not resolve n >= 2.
- The unresolved task is to classify proper closed GL^+-invariant Boolean supports and compatible finite parts, or prove that a valuation finite anywhere is finite everywhere. Neither has been achieved.
- No historical novelty, first-resolution, or global-open-status claim is made. Long cited geometric proofs remain trusted published dependencies.

## Reading order and preservation

1. [Controlling correction](audit/CORRECTION.md), then [independent audit](audit/AUDIT.md).
2. [Frozen authored result](author/RESULT.md), read with the correction authoritative; [five-approach log](author/APPROACH_LOG.md).
3. [Public source-verification metadata](author/SOURCE_VERIFICATION.md), [author manifest](author/AUTHOR_MANIFEST.json), and [audit manifest](audit/AUDIT_MANIFEST.json).
4. [Current release status](RELEASE_STATUS.json), [publication manifest](PUBLICATION_MANIFEST.json), and [portable verifier](verify_publication.py).

All eight author files and all seven audit files are preserved byte-for-byte. Frozen references to a pending audit are historical; the current verdict is PASS_WITH_REQUIRED_CORRECTION, with that correction adopted here. Audit limitations and the local-versus-global finiteness qualification in audit Section 7 also govern interpretation.

Author manifest SHA-256: `938d14791569ca0c77c9f19b13a71bd33219df81395d778c86e6703300c9bb34`.
Audit manifest SHA-256: `5500994baaca7f9a25bd5a8510a8aba3ead206f063e23188e12a41a0ace9c991`.
Controlling correction SHA-256: `c865aab4da0e409cc62ae9c444c3a38d73a4c4ac4d12f88a71eb0895edb85b01`.

## Portable replay

Run `python3 verify_publication.py` from any working directory, using this script's path as needed. Python standard library only; no source files, network, or external packages are required. The verifier also works when invoked with `python3 -O`; it runs frozen assertion-based checks in nonoptimized child interpreters. Use `--expected-manifest-sha256 HASH` with the independently recorded publication-manifest hash to authenticate that manifest. A manifest alone cannot authenticate a coordinated rewrite of itself and its verifier.

The controls reproduce 15,200 author assertions and 28,270 independent audit checks, including ten deliberately false mathematical alternatives and eight in-memory tamper cases. These counts include consistency and integrity checks. They are not 43,470 independent mathematical proofs, a correctness probability, formal verification, human peer review, or evidence of a complete classification. Finite controls supplement the written proofs and credited sources.

Only authored analysis, code, and public bibliographic/integrity metadata are included. No source PDFs, extracted source text, source images, raw datasets, or private coordination files are included. The queue patch changes this row's Status to `unsolved` and Turns to `5/5` only; all other queue bytes, including the pre-existing header, are preserved. There is no merge, release, DOI registration, or external outreach in this publication.
