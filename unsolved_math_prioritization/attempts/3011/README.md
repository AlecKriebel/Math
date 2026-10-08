# KP-5.4 / 3011: scoped homeomorphism-group partial results

**Partial, 5/5 mathematical approaches. The compact-manifold ANR problem remains unresolved. No solution or novelty claim.**

For canonical Alexander simplex interpolation in every spatial dimension n >= 2, the authored results give linear worst-case arity amplification, m/pi <= A_m <= 2m+1. A bounded-dimensional metrizable parameter extension is proved; arbitrary metrizable parameter extension in n > 2 remains unproved. Failure of this interpolation rule does not imply non-ANR: the same failure occurs in spatial dimension two, where the ANR result is known.

The other routes give a one-dimensional extension, conditional fragmentation, an obstruction to naive Hilbert-cube slice projection, and a Hilbert-cube/Baire obstruction to finite-dimensional compact exhaustion. The noncompact escaping-twist example is attributed to Edwards–Kirby and is not a new answer to the intended compact question.

## Read the results

- [Accepted report](accepted/REPORT.md) and [parametric extension proof](accepted/PARAMETRIC_EXTENSION.md)
- [Independent final audit](audit/AUDIT.md) and [earlier adversarial review](audit/ADVERSARIAL_REVIEW.md)
- [Author source audit](accepted/SOURCE_AUDIT.md), [public source metadata](accepted/SOURCE_MANIFEST.json), and [independent source inspection history](audit/SOURCE_INSPECTION.json)
- [Explicit corrections](accepted/CORRECTIONS.md) and [authored correction patch](accepted/CORRECTIONS.patch)
- [Publication acceptance](ACCEPTANCE.md) and [public-slice accounting](PUBLIC_SLICE.json)

The correction patch's removed lines are rejected, superseded assertions. They are included solely to show the corrections, not as accepted mathematics. The full rejected reconstruction is not published. It was a retrospective reconstruction, never an authenticated historical snapshot.

This is a new public-only slice, not the complete original audit distribution. Original source-document bodies, PDFs, extracted text and private coordination material are absent. The historical mathematical and source audits are retained at their stated inspection depth. The final audit has only a publication-scope header and one packaging paragraph adapted; the correction note has its packaging explanation and original patch-hash label adapted. The patch itself has a standalone rejected-hunk preamble added; its original diff bytes are unchanged. All other included authored mathematical texts and checkers are byte-identical to their accepted originals. PUBLIC_SLICE.json identifies every such adaptation and its public mathematical input/output hashes.

## Reproduce the public-only checks

Use Python 3.12, standard library only, on Linux as UID=EUID=1000. No network, external package, `patch` utility, original source archive, reconstructed full baseline, or private input is needed. The verifier writes only temporary disposable files outside the packet. Its complete stdout/stderr record is [REPLAY_RESULTS.json](REPLAY_RESULTS.json).

Obtain the exact BOOTSTRAP.py SHA-256 from the independent PR description or acceptance handoff. Check that external pin before executing any packet script. A digest obtained only from an untrusted packet is not an external trust anchor.

    sha256sum BOOTSTRAP.py
    python -I -S -B BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -O BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -OO BOOTSTRAP.py /absolute/path/to/packet

The bootstrap pins the manifest and wrapper bytes before executing the wrapper. The wrapper enforces exact recursive files/directories, ordinary-file-only access, no linked roots or ancestors, strict JSON including duplicate/nonfinite rejection, exact integer types, independent accepted-byte pins, and full native-output equality. The manifest intentionally excludes itself and BOOTSTRAP.py to avoid circular hashes; the bootstrap and external pin provide those bindings.

To run publication attacks as well, first authenticate the externally pinned bootstrap and use its manifest to authenticate mutation_tests.py; then run:

    python -I -S -B mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 EXTERNAL_PIN
    python -I -S -B -O mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 EXTERNAL_PIN
    python -I -S -B -OO mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 EXTERNAL_PIN

Each mode runs the full public-only protocol, rejects malformed inventories and self-consistent repinning attacks, and repeats the protocol from a relocated read-only packet with a hostile working directory and Python environment. No mathematical or security condition relies on Python assert.

## Exact replay scope

Each public-only replay executes 60 subprocesses: six byte-exact native author/independent runs; three physical read-only probes, each attempting creation, existing-file writes and mkdir; nine external-output, internal-output-refusal and writable-tree controls; 39 semantic-mutant runs (13 distinct mutants in all three modes); and three input-guard runs covering five rejected input classes each.

The original author counts are 1,280 Alexander cases, 900 interval-convexity cases, two rotation witnesses, 78 homology twists, 270 cube-family cases, 30 symbolic noncommutative cases, and eight radial-amplification cases. The independent actual-map implementation checks 400 group/scale cases and 29 simplex cases, including 17 zero-face cases; reversed factor order is distinguished in 22 cases.

Fresh source retrieval, source inspection, PDF-byte verification and replay against the omitted full reconstructed baseline are all **NOT_RUN**. Historical records are not a substitute for those absent operations. These finite computations do not certify ANR/non-ANR, arbitrary metrizable extensions, comprehensive current literature or novelty.
