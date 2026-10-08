# Simple polygonalizations: accepted partial results

Problem 5500016 / AMR-054-0016, TOPP Problem 16, rank 1062. Disposition: **exhausted, 5/5**. The unrestricted exact-counting problem remains unresolved. This is an AI-assisted, unrefereed research note and independent agent audit, not conventional human peer review. No novelty is asserted.

## Mathematical contents

- [Author report](author/REPORT.md): continuation-state counterexample, nonuniform triangulation extensions, crossing-event inclusion–exclusion and forced-path formula, restricted positivity obstruction, and the exact hull-gap candidate count.
- [Independent audit](audit/AUDIT.md): all five partial claims accepted without a mathematical correction, with independent rational segment geometry and bounded exhaustive checks.
- [Acceptance](ACCEPTANCE.md) and [public scope](PUBLIC_SCOPE.json): exact acceptance and remaining gaps.

The author package (8 files) and accepted audit package (21 files) are preserved byte for byte. Their original manifests and historical receipts remain intact. All point sets are authored synthetic mathematical fixtures. Public source metadata gives public titles, URLs, sizes, hashes and bounded inspection history; no source document, copied source extract or dataset is distributed. No private coordination material or its identifying metadata is included.

## Reproduce the entire delivery

Python 3.10+ and the standard library suffice. The recorded runs used Python 3.12.14 with actual real/effective UID 1000. The exact audit is intentionally bounded and exponential/factorial; it is not a fast general counter.

1. Obtain `BOOTSTRAP.py` and its SHA-256 through a trusted independent channel. The PR description supplies the reviewed bootstrap hash. Verify that hash before execution. Keep this trusted copy outside the candidate packet, for example as `/tmp/trusted_polygon_bootstrap.py`. A hash recomputed solely from a candidate package is not an independent trust anchor.
2. Let `PACKET` name this directory and `QUEUE` name the exact accompanying `unsolved_math_prioritization/QUEUE.md`. The bootstrap binds the complete queue, including the literal initial SHA line, and the complete recursive packet inventory. A later unrelated queue change intentionally requires a new trusted anchor or checking out the original published commit.
3. Prepare a disposable copy of the packet with directories mode 0555 and files mode 0444. Set the disposable queue copy to mode 0444. Run as real/effective UID 1000. Capture outputs outside the input directories.
4. Run each command below, substituting those explicit paths:

```
python -I -S -B /tmp/trusted_polygon_bootstrap.py PACKET QUEUE
python -I -S -B -O /tmp/trusted_polygon_bootstrap.py PACKET QUEUE
python -I -S -B -OO /tmp/trusted_polygon_bootstrap.py PACKET QUEUE
```

The fixed external bootstrap verifies the candidate bootstrap itself, the complete publication manifest, the verifier and exact queue before executing any candidate verifier. The manifest binds all other deliverables, including this README, acceptance, scope, all original manifests/receipts, complete new replay and controls references, and all code. Exact inventory rejects extra or missing files/directories, symbolic/hard links, FIFOs and nonordinary entries. This provides static integrity, not a general malicious-code sandbox or trusted-Python guarantee.

The verifier makes actual denied-write probes on every input file/directory plus the queue. It then copies every original public author/audit input into a separately relocated read-only tree and runs both mathematical programs in normal, `-O` and `-OO` modes. The working directory and environment contain hostile import sentinels. Isolated Python flags `-I -S -B` prevent those imports. It compares every fresh stdout/stderr byte against fixed original full references and compares all recursively typed output objects; booleans and floats cannot substitute for integers. It then compares the entire fresh replay with [REPLAY_RESULTS.json](REPLAY_RESULTS.json), without stripping paths, timestamps, keys, bytes or values. Inputs are rehashed after execution. The complete outer stdout, including every entire-delivery probe, is separately pinned byte-for-byte and recursively by type in [VERIFICATION_RESULTS.json](VERIFICATION_RESULTS.json).

Run the separate adversarial controls after anchored verification, using the same verified external bootstrap and its independently verified SHA-256:

```
python -I -S -B PACKET/controls.py /tmp/trusted_polygon_bootstrap.py TRUSTED_SHA256 PACKET QUEUE
```

Repeat with `-O` and `-OO`. Compare every output byte and its recursively typed JSON to [CONTROL_RESULTS.json](CONTROL_RESULTS.json). Controls cover delivery mutations, self-consistent candidate-side repinning, exact inventory and strict JSON/schema/type behavior. The twelve mathematical semantic mutations are rerun inside every audit execution and their full rejection records are included in the replay.

## What was not rerun

Fresh source retrieval, source text/PDF byte verification, current-source inspection and corpus/dataset replay are explicitly `NOT_RUN`. The absent source/corpus bodies are outside the scope of this publication replay. Historical source checks remain historical. No exhaustive literature coverage, formal proof-assistant verification, priority finding, solution, release or DOI is claimed.
