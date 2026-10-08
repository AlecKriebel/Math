# Sticky Cantor sets: known dimension classification

Rank 1059; problem 3422 / OPG-37293. **Already solved in the cited literature, 0/5 substantive proof-search approaches. No novelty claim.** For positive integers n, sticky Cantor sets in Euclidean n-space exist exactly when n >= 4.

Read [the complete report](author/REPORT.md), [the independent mathematical audit](audit/ACCEPTANCE_AUDIT.md), and [publication acceptance](ACCEPTANCE.md). The author payload and independent audit are byte-preserved. Their chronology matters: `author/STATUS.json` says independent audit pending because that was true at its freeze; `audit/ACCEPTANCE.json` records the subsequent acceptance. Neither historical `publication_performed: false` field is a statement about this later repository publication.

## Exact mathematical scope

- Dimensions 1 and 2 have direct displacement proofs; the planar proof uses Jordan-Schoenflies.
- Dimension 3 imports Sher's separation theorem through the directly inspected statement in Frolkina, arXiv:2203.03267v2, section 3.2, with its global epsilon-homeomorphism convention in section 1.6. Sher's original proof was not inspected. Requesting epsilon/2 handles the source's non-strict bound.
- For n >= 4, Krushkal's original construction and argument were inspected. Spun-Bing shrinkability, geometric meridian identifications, Alexander duality and Stallings remain imported established inputs.
- The explicit bridge H_t(x)=t f(x/t), H_0=id, has joint forward/inverse continuity, displacement tD and point-track diameter at most 2D. It does not assert a path continuous in the global uniform metric at positive t.
- Distinct-generator Magnus induction supplies the nonvanishing argument; syntactic commutator length alone does not.

The finite programs support these arguments. They do not decide wild embedding topology, reconstruct the imported theorems, certify novelty, or establish exhaustive literature coverage.

## Authenticate before executing

Obtain the SHA-256 of `BOOTSTRAP.py` from the draft PR body or another independently trusted channel. Check that external value before running any packet code. A hash obtained only from the packet itself is not an external trust anchor.

After authenticating the bootstrap, run from any working directory:

    python -I -S -B /absolute/path/to/BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -O /absolute/path/to/BOOTSTRAP.py /absolute/path/to/packet
    python -I -S -B -OO /absolute/path/to/BOOTSTRAP.py /absolute/path/to/packet

The externally authenticated bootstrap contains exact manifest and wrapper pins. It authenticates both before executing the wrapper. The wrapper checks the exact recursive file/directory set, rejects links and special files, validates every JSON file with duplicate/nonfinite guards, enforces typed integer/hash schemas, and checks independently embedded accepted-evidence pins. Only then does it execute any checker. The original inner manifests and checks are retained but are not the external trust boundary.

Use actual UID=EUID=1000 on Linux with a writable temporary directory. No network, source documents, dataset bodies, shell commands, third-party packages, or repository checkout are required. Python 3.12 is the recorded runtime. This is an exact-output replay, so implementation-dependent receipt or error changes can fail the comparison on another interpreter/platform.

To exercise publication boundary attacks, authenticate the same bootstrap first, then run the manifest-authenticated driver:

    python -I -S -B /absolute/path/to/mutation_tests.py --root /absolute/path/to/packet --bootstrap-sha256 EXTERNALLY_VERIFIED_SHA256

Repeat with `-O` and `-OO`. Each driver run performs the full replay twice: once normally and once from a relocated 0555/0444 packet with a read-only hostile working directory and hostile Python environment variables. Hostile import files must not execute, all original input bytes must remain unchanged, and 50 negative controls must be rejected. The entire driver has additionally been tested from a read-only packet and working directory in all three modes.

## Fresh source-free replay

`REPLAY_RESULTS.json` retains complete native and control stdout/stderr, complete independent native receipts and expected errors. The wrapper recomputes and compares the entire typed result, without selecting only favorable fields. Only disposable execution-path prefixes are normalized.

Each full replay has 39 top-level subprocesses plus 36 nested executions by the unchanged independent harness:

- Author checker under normal, -O and -OO; byte-exact output matches the independently recorded native outputs.
- Complete independent harness under all three modes; all receipt fields match the historical normal receipt with only the explicit harness optimization field varying. The -OO receipt also matches the separately retained original optimized receipt.
- Each independent harness run contains three read-only author runs, five repinned semantic mutations, full native outputs, output-path and writable-tree controls, and the independent integral-matrix checks of all 626 ordered binary tree shapes through eight leaves, each in two variants.
- Nine additional physical create/open-existing/mkdir write attempts are denied across the three modes.
- Nine additional explicit-external-output, forbidden-internal-output and writable-tree branch runs.
- Five author mathematical mutations, with checker pins refreshed, are rejected for the expected mathematical reason in all three modes: 15 executions.
- Two mutations of the independent implementation itself are rejected in all three modes: six executions. They remove a matrix generator and destroy the uniform-topology counterexample witness.

All top-level subprocesses use isolated/no-site/no-bytecode flags and a minimal clean environment. The historical independent harness is unchanged; its own nested invocations retain their original `-B` command protocol. They run inside the wrapper's clean environment and read-only working directory against an exact authenticated author directory with no extra import files. Publication controls reject a hostile import added to that directory before execution.

## Historical checks and omitted inputs

The audit includes historical public verification metadata for retained PDFs, source pages, dataset hashes/match results, the original source-free archive and the author's correction-patch replay. This is not a fresh network retrieval or fresh inspection of those sources. The source/PDF/corpus bodies, archives, earlier full report and external freeze receipts are omitted. Fresh retrieval, source inspection, PDF byte binding, dataset byte binding, full-baseline patch replay and archive reconstruction all report **NOT_RUN** in this public-only replay.

The correction patch preserves only authored mathematical clarification hunks, including removed wording as historical context. The corrected report controls. No stale manifest authorizes excluded input files: the native author and audit manifests describe exactly their respective included directories. No private workflow or coordination material, or identifying metadata for such material, is included.

## Public sources

- [Open Problem Garden target](https://www.openproblemgarden.org/op/sticky_cantor_sets)
- [Krushkal, Sticky Cantor Sets in R^d](https://arxiv.org/pdf/1602.01035v1)
- [Frolkina, disjoint compacta, v2](https://arxiv.org/pdf/2203.03267v2)
- [Sher, Families of arcs in E^3](https://doi.org/10.1090/S0002-9947-1969-0251705-4)

Draft publication only. No merge, release, DOI or external outreach.
