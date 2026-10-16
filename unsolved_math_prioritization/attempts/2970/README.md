# Horikawa surface equivalence: audited partial results

KP-4.94 / problem 2970, rank 1050. **Unsolved; five of five mathematical approaches.** Neither diffeomorphism nor canonical symplectomorphism is established or obstructed for an odd-r target pair.

## Contents and trust boundaries

- `original/REPORT.md`: the unchanged mathematical report and its complete frozen nine-file public slice.
- `audit/AUDIT.md`: the independent acceptance audit and unchanged ten-file public slice.
- `corrected_v1/`: a separately pinned adoption of the supplied two-line orbit-cardinality guard, with its own manifest and provenance.
- `ACCEPTANCE.md`: reconciled mathematical and executable disposition.
- `REPLAY_RESULTS.json`: fresh genuine UID=EUID=1000 read-only execution receipts with complete stdout/stderr, including all original false-PASS controls.
- `BOOTSTRAP.py`, `verify_publication.py`, and `mutation_tests.py`: externally anchored, strict publication verification and adversarial controls.

The original report and audit were independently accepted without a mathematical correction. The optional executable guard is adopted only in `corrected_v1`; nothing silently replaces the historical original.

## Reproduce, with an external trust anchor

First obtain the bootstrap SHA-256 from the reviewed publication receipt or PR description, outside this directory. Do not treat a newly computed local hash, a hash in a mutable adjacent file, or an unverified script's assertion as authorization to execute it. From this directory:

```sh
printf '%s  BOOTSTRAP.py\n' "$BOOTSTRAP_SHA256" | sha256sum -c - && \
python -I -S -B BOOTSTRAP.py "$PWD" > /tmp/horikawa-publication-replay.json
```

Repeat the Python command with `-O` and `-OO` after authenticating the same bootstrap. It pins the manifest and verifier before executing the latter. The verifier enforces an exact recursive file/directory allowlist, strict JSON types and keys, preserved evidence pins, actual patch bytes, and all fresh mathematical replays. It rejects links, special files, missing files, extra files, and reanchored evidence substitutions. There are no third-party dependencies.

Run the publication-adversarial suite in all three interpreter modes after authenticating the release:

```sh
python -I -S -B mutation_tests.py --root "$PWD" --bootstrap-sha256 "$BOOTSTRAP_SHA256"
```

Use UID=EUID=1000. Replays create disposable external temporary directories and set executed inputs to 0444 in 0555 directories. They confirm real write denial and unchanged contents. The delivered directory itself can be read-only. Output goes to stdout; redirect it outside the delivered tree.

## Exact limits

The original truncated-orbit mutant exits zero with `status: passed`; strict saved-output comparison rejects it. The corrected script directly rejects it through the new cardinality guard. The valid outputs are unchanged. The independent permutation-based check exhausts 360 generating identity quadruples into disjoint orbits of sizes 216 and 144.

This finite PSL(2,F3) example is not a quotient of the actual Horikawa monodromies. The lattice and fiber arguments remain marked, the Lagrangian-span obstruction conditional, smooth spheres are not asserted canonical-symplectic, r=4 is outside the odd-r target, and the AEHK r=3 normal degeneration bridge does not settle either equivalence.

Fresh source retrieval, source inspection, and PDF-byte binding are **NOT_RUN** by the source-free publication verifier. Historical inspection and bibliographic verification metadata are retained with their original scope. No scholarly PDFs, screenshots, extracted source bodies, external datasets, private sources, or coordination records are included. The existing repository QUEUE is changed only in this problem's Status, Turns, and Findings cells.
