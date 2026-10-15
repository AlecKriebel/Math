# Maximal norm discontinuity for a bounded-region continuum fermion interaction

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. Research note v1.0,
14 October 2026. Extensive AI assistance; unrefereed; no independent human
peer review is claimed.

The note proves an explicit existential result in dimension three. A single
smooth compactly supported radial potential and the fixed interaction ball
B(0,4), with kinetic energy on all of R3, give a fixed annihilation operator
whose Heisenberg norm differences tend to the maximal value2. Explicit changing
finite-particle Slaters witness the same vector-norm limit and state expectation4.
Both diagonal-density and normal-ordered conventions are covered, with no
ultraviolet smearing and coefficient1 in the ordered-pair sum. The ordering flag
kappa is distinct from a UV regularization parameter. Every fixed vector and
every fixed normal state remains continuous. No all-potential, all-region,
dimension1/2, fixed-density/energy, thermodynamic, or CAR-invariance claim is made.

This answers the existential question on printed p371 of Oberwolfach Report
7/2025, with norm topology explained on p365. First priority and continued open
status are not asserted. Read PRIORITY_FRAMING.md and the independent priority
and mapping audits for the precise relationship to the September2026 Siebert
preprint and earlier work. The explicit quantitative proof is the primary
artifact; finite controls are supplementary evidence, not formal certification.

## Contents and provenance

- note.pdf and note.tex: identical authored PDF to the separate upload and its source.
- original_packet/: all26 original bounded_region_v2 files, unchanged from PR908
  head a35667b1bb0bafed69916709997a4684223ecc93; original1/5 candidate turns preserved.
- reviews/: independently authored analytic, operator-algebra, computational,
  source/model, priority, and priority-mapping reports and their public manifests.
- Root provenance, bibliographic identities, and publication qualifications.
- verify_package.py and run_checked.py: current guarded reproduction entry points.
- PACKAGE_MANIFEST.json: closed file inventory and SHA-256 fingerprints.

No copied third-party PDFs, extracted source text, screenshots, private source
records, search/API payloads, or data corpora are distributed. Authored source
manifests describe inspected versions and access limitations. Fingerprints
check consistency; they are not signatures, proof certificates, or evidence
of authorship. Authenticate the package-manifest SHA-256 independently from
the publication record's Notes. Replacing both software and its trust anchor
defeats consistency checking. Concurrent ancestor-directory renaming is outside
the verifier's threat model; final-entry races are guarded with regular-file
checks, nonblocking/no-follow opens, and inode/mtime comparisons.

## Reproduce

Install the versions in requirements.txt in a disposable Python environment.
The recorded replay used Python3.14.6, NumPy2.3.5, SciPy1.17.0, SymPy1.14.0,
and mpmath1.3.0. Run from the extracted archive, substituting the externally
authenticated manifest hash and a work directory outside the closed package:

```
python verify_package.py --expected-manifest SHA_FROM_PUBLICATION_NOTES --integrity-only
python verify_package.py --expected-manifest SHA_FROM_PUBLICATION_NOTES --workdir /absolute/path/outside/package
python -O verify_package.py --expected-manifest SHA_FROM_PUBLICATION_NOTES --workdir /absolute/path/outside/package
python -OO verify_package.py --expected-manifest SHA_FROM_PUBLICATION_NOTES --workdir /absolute/path/outside/package
```

An integrity-only run needs the standard library. Full replay needs the pinned
numerical dependencies. Python-version metadata is reported separately; logical
statuses, integer counts and strings compare exactly, with bool/numeric type
separation. Floating replay values use relative tolerance1e-9 and absolute
tolerance1e-10, in addition to each checker's own active acceptance tests.
Historical source-byte checks are explicitly omitted, never synthesized as
fresh verification. The source/model and priority families independently
authenticate the primary texts; runtime mathematical replay does not retrieve them.

The outer entry point always launches isolated nonoptimized workers and checker
processes, even if the outer invocation uses -O, -OO or inherited PYTHONOPTIMIZE.
All assertion-based historical and fresh analytic controls therefore remain
active. PYTHONPATH and PYTHONHOME are cleared and isolated imports are enforced.
The worker reports actual optimization/isolation flags. Reproduction occurs in
automatically removed copies inside the specified work directory, with nested
TMPDIR confined there. The original packet and extracted archive stay unchanged.

The new computation-family packet checker independently anchors the original
outer manifest (SHA828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795),
proof and all three nested manifests, and rejects extra directories, symlinks,
FIFOs/sockets, ambiguous layouts, unsafe paths and malformed JSON. The current
outer verifier also authenticates every published payload and directory and
the separate PDF when --pdf is supplied. An external manifest anchor is required
for a full replay.

## Evidence and historical limitations

The universal continuum result follows from the written fixed-cutoff commutator,
Slater second moment, uniform two-sector Duhamel estimate and CAR phase proof.
The localization family additionally checks8 exact finite Slater cases,22952
sector identities,20000 phase identities and15 packing cases. The operator
family has148 finite algebra controls, including floating diagnostics at
tolerance3e-11. The computational family has2668 exact finite predicates and558
floating diagnostics at tolerance2e-11; these are not rigorous floating enclosures.
Predicate counts do not mean statistical independence or exhaustive continuum coverage.

The historical author's4288 and audit B's16768 sector cases are finite samples.
Audit A's5659 calls consist of5000 integer predicates,2 symbolic predicates and657
floating or mixed predicates. No claim of5659 independent exact tests is made.
Historical saved outputs and the current replay differ at roundoff scale and in
Python/source-check metadata; no byte/JSON identity of those outputs is asserted.

The original wrapper is retained for provenance, not used as the publication
gate. Its child assertions can be disabled by inherited PYTHONOPTIMIZE, and its
inventory accepts certain unlisted special entries and directories. The fresh
computation audit reproduces20 historical executions,24 optimization controls
and22 historical boundaries, and tests the replacement packet checker with104
hostile cases and12 positive layout cases. Read that audit before interpreting
any historical PASS. The current outer wrapper and execution safeguards repair
these publication-tooling defects while preserving all original bytes.

To rebuild the standalone note, use Tectonic on note.tex. It requires no
additional project files. Render every output page for layout verification.

License for the authored note and verification materials: CC BY4.0. This does
not grant rights in cited third-party sources, which are not included.
