# Trisection invariants and four-dimensional TQFTs: accepted partial results

Problem **30006636 / OWR-14299913-005**, rank 1055. Mathematical question **unresolved**; queue **exhausted, 5/5 substantive approaches**. Read [ACCEPTANCE.md](ACCEPTANCE.md), the accepted [corrected report](evidence/FIVE_APPROACH_REPORT.md), and the unchanged [first-stage proof](evidence/PROOF.md).

The standard untwisted finite-group/transitive-set subclass has an unchanged-value extension-existence classification and an explicit boundary-color functor. The normalization-unspecified general source question remains unresolved. No general fusion-2-category extension, uniqueness classification, novelty or external peer acceptance is claimed.

## Current public packet

Only the accepted corrected report and explicitly contextualized mathematical correction are distributed. Connectedness of Y is mandatory; the patch's removed line is a rejected historical claim. The full superseded report, stale release README and superseded author inventory are not delivered.

Seventeen original release members remain byte-identical, including accepted mathematical reports, both audits, authored checkers, their arithmetic outputs and the exact execution-hardening patches. The mathematical correction diff is unchanged beneath its explicit rejected-scope preamble. `evidence/PUBLIC_SLICE.json` records these narrow changes and necessary public verification provenance. `PUBLICATION_MANIFEST.json` is the **sole current deliverable inventory**.

Historical author-validation, audit and hardening metadata are delivered as labeled `.public.json` derivatives. Stale artifact inventories and inventory assertions were removed; the hardening patch paths were mapped to their current basenames. All arithmetic outputs, rejection diagnostics and accepted mathematical findings remain unchanged. Each derivative states its original hash/size and exact removed fields. References in unchanged mathematical audit prose to historical metadata filenames correspond to these public derivatives. Neither the derivative records nor PUBLIC_SLICE authorize an excluded file.

`AUTHOR_RELEASE_VALIDATION.public.json` records the historical combined arithmetic validation. Six complete mode-specific first-two-checker outputs are retained under `expected/`; the independent checkers reproduce their historical arithmetic result files exactly. The original local freezes were not modified.

Only authored mathematics, code, mathematical audits and public verification metadata are included. Source PDFs, copied scholarly text/images, corpus contents and private coordination material are absent. The two historical .py.txt files contain authored checker code. Four generic randomized temporary test paths in the public hardening receipt remain unchanged as diagnostic provenance; they contain no personal or coordination information.

## Trust and reproduction

Authenticate `BOOTSTRAP.py` against the SHA-256 in the separately reviewed draft PR body before running it. Calculating a new hash of an untrusted copy does not establish trust. The bootstrap pins the exact current publication manifest and verifier before the latter executes. The manifest binds every delivered payload, and the verifier independently pins each accepted evidence file and the exact recursive inventory. Self-consistent rewriting of a payload and inner metadata cannot substitute different evidence.

Use a real UID/EUID 1000 account. Make a disposable complete packet copy, set files to `0444` and directories to `0555`, and use a separate cwd set to `0555`. Keep a temporary-output location elsewhere writable. Run from the read-only cwd, using the authenticated bootstrap:

    python3 -I -S -B /trusted/BOOTSTRAP.py /absolute/read-only/packet
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /absolute/read-only/packet
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /absolute/read-only/packet

The trusted bootstrap must have bytes identical to the packet's bootstrap. Every invocation requires every expected file and read-only packet/cwd, probes real denied writes, replays all four checkers in that mode, and compares complete positive stdout bytes. For external output, the two authored checkers explicitly change their `writes` field; the complete expected external payload is reconstructed and byte-compared. No positive fields are ignored or silently normalized.

Each mode requires four clean positives, 27 semantic rejections, four explicit external outputs, 12 output/overwrite rejections and six historical controls. Across normal/-O/-OO: 12 positives, 81 semantic rejections, 12 external outputs, 36 output safeguards and 18 historical controls. Semantic rejections must reproduce the exact invariant diagnostic in the public author receipt. Absolute-path-dependent negative traceback bodies are not byte-compared. Missing inputs and unrun source checks cannot become PASS.

For separate trust-boundary controls, authenticate the bootstrap and the manifest-bound test driver first. From the read-only cwd, run each mode with the externally authenticated bootstrap digest:

    python3 -I -S -B /absolute/read-only/packet/mutation_tests.py --root /absolute/read-only/packet --bootstrap-sha256 DIGEST

Repeat with `-O` and `-OO`. The driver tests 61 negative cases per mode, including inventory changes, links/FIFOs, exact-type JSON, substituted payloads/wrappers and complete-output corruption. It replays the full checker suite after read-only relocation into a hostile import environment. Disposable mutation copies and explicit historical outputs remain separate from frozen inputs. Standard-library Python suffices; no source files, network, private state or package installation is needed.

## Limits and historical defects

Fresh scholarly-source and corpus binding are **NOT_RUN**. Source hashes, sizes, public URLs, inspection history and manuscript status are historical metadata. Finite arithmetic tests support the written proofs; they do not machine-certify imported theorems, all bordism realizability statements, all TQFT axioms, or novelty.

The old normalization checker demonstrably false-passes a corrupted stabilization value 32 under optimization. The old follow-up checker explicitly refuses optimized execution. Both old scripts fail genuine read-only execution at implicit adjacent writes. The hardened variants repair these execution safeguards while preserving accepted mathematics. Historical limitations are reproduced as limitations, never reported as valid optimized arithmetic.
