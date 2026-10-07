# Random square-tiling crossings: corrected partial work

Problem 10000051 / AMR-099-0051, queue rank 988. **Unsolved, 5/5 substantive approaches.** Neither the uniform fair-color lower bound nor the fair-color small-mesh limit is proved.

Start with [the corrected candidate](corrected/CANDIDATE.md), [the independent audit](audit/AUDIT.md), and [the acceptance report](ACCEPTANCE.md). The seven-square example has horizontal crossing probability 65/128 and vertical probability 63/128. It refutes only a stronger finite exact-half shortcut. The explicit high-density theorem depends on Ron Peled's credited square-packing theorem at p >= 1-exp(-26); it does not apply at p=1/2.

## Packet layout

- `original/`: unchanged author freeze, including its contextual documents and chronological five-approach ledger. The scripts here are preserved historically and must not be used with optimization.
- `audit/`: unchanged independent audit freeze, actual correction patch, corrected candidate, public-source metadata and independent checks.
- `corrected/`: the corrected candidate and its exact-check files, obtained by applying `audit/CORRECTION.patch` to the original. This adoption slice has a separate manifest. The original contextual documents remain in `original/`.
- `verify_publication.py`: verifies the externally supplied root-manifest hash, all inventories and embedded pins, exact patch reconstruction, independent checks, ordinary author/corrected replays and direct optimized-script rejection. Uses explicit validation, not assertions.
- `mutation_tests.py`: thirteen negative controls in each of normal, -O and -OO modes. All mutation and generated result writes occur in temporary copies.

## Reproduce

Requirements: Python 3.10 or newer, standard library, and the conventional `patch` command. No network, random sampling or external Python package is needed.

Obtain HASH and VERIFIER_HASH from the draft PR's acceptance record, outside this packet. Before first execution, compare verify_publication.py with VERIFIER_HASH using sha256sum or an equivalent trusted tool. The mutation driver also requires that external verifier hash before executing the wrapper. Do not replace it by a hash freshly computed from an untrusted manifest.

    python3 verify_publication.py --manifest-sha256 HASH
    python3 -O verify_publication.py --manifest-sha256 HASH
    python3 -OO verify_publication.py --manifest-sha256 HASH
    python3 mutation_tests.py --manifest-sha256 HASH --verifier-sha256 VERIFIER_HASH

The wrapper always launches assertion-based scripts with ordinary, isolated Python (`-I -B`), even if the wrapper itself is optimized or PYTHONOPTIMIZE is set. Direct optimized runs of the corrected scripts must fail. The supplied exact computations check finite examples and arithmetic; they do not prove the general conjectures. Original/audit documents are dated snapshots, including statements about their publication state when frozen.

Only authored mathematical text, exact-check programs and constructed examples/results, and public-source provenance are included. Third-party PDFs/extracts, research-corpus contents and private material are excluded. No novelty, priority, conventional human peer review, or full solution is claimed. The work and audit used extensive AI assistance.
