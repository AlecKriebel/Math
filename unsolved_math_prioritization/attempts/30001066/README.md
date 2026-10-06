# Isolated line transversals: audited partial results

Problem **30001066 / OWR-2090-019**, rank **819**. Status: **unsolved**, **5/5** proof-attempt turns used.

## Accepted result and remaining question

For every integer `d >= 2`, an explicit family of `3d-3` compact, full-dimensional, strictly pairwise-disjoint boxes minimally pins a line. The proof establishes a unique global transversal and continuous nontrivial motions after every deletion. Consequently the numerical `2d-1` bound for balls cannot extend to arbitrary disjoint convex bodies when `d >= 3`.

The existence of some finite dimension-dependent bound `h(d)` for arbitrary pairwise-disjoint convex bodies **remains unresolved in this work**. The primary OWR contribution asks about broader generalization; it does not explicitly conjecture the same `2d-1` number for general convex bodies. The catalog supplies that number as an illustrative candidate.

The conditional `4d-4` upper bound is valid only when the linearized feasible cone is trivial. Pinning alone does not imply that hypothesis. The known six-object obstruction is credited to Günter Rote; no novelty claim is made for the lower-bound phenomenon or coordinate-block construction.

Read the [complete proof](author/proof.md), [five approach gaps](author/approach_audit.md), and [independent audit](audit/INDEPENDENT_AUDIT.md).

## Mandatory integrity correction

The preserved author directory checker has a confirmed `__pycache__` exemption that accepts unlisted files. It must not be used alone as the publication gate. The reviewed ZIP is clean. This package makes [the strict archive/directory checker](audit/strict_inventory.py) mandatory, pins both archive identities, validates the exact publication inventory, and compares every extracted member with its archive bytes before executing package code.

[The separate patch](audit/verify_package_strict.patch) removes the exemption. The publication replay applies the actual patch only to a disposable derived copy, recomputes that copy's manifest, and tests both clean acceptance and rejection of synthetic cache/root additions. Neither supplied archive is rewritten by replay. Unmanifested directories, bytecode, symlinks and files are rejected before local audit modules are loaded. Bytecode creation is disabled in every subprocess.

## Reproduce

Requirements: Python 3 standard library and the `patch` utility. No network or source documents are needed for the mathematical/inventory checks.

```sh
python -B verify_publication.py
python -B -O verify_publication.py
python -B package_mutation_tests.py
```

The wrapper also supports `--integrity-only`. Its pinned manifest covers every payload except the manifest and wrapper themselves; authenticate the wrapper through its Git commit or an independently verified external hash. Run result-producing commands outside the manifested packet, or redirect output outside it.

Independent geometry covers dimensions 2, 3, 4, 5, 8, 12, 16, 24 and 32, with 16,944 whole-real-parameter interval checks and 34,470 exact clipping checks. Author implementation replay includes dimension 64, thirty adversarial semantic mutations per mode, four valid generalized variants per mode and eighteen strict-inventory mutations. Finite computation supplements the all-dimensional proofs.

## Artifact identity and provenance

- Public author editorial derivative: `archives/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip`, 17,217 bytes, SHA-256 `be4dabaf22028561681c76c353bd537d0b240cfd67d52aa7ed9531f435905034`.
- Re-bound public audit derivative: `archives/ISOLATED_TRANSVERSAL_30001066_PUBLIC_AUDIT_DERIVATIVE.zip`, 26,759 bytes, SHA-256 `12b8c6d00a91d8e5244fed83053fa462f403d9d32ba16f6d099e858c972054e6`.

The author material is a public editorial derivative of version `1-reconstructed`, not a byte-identical restoration of an earlier freeze. The editorial metadata change leaves the mathematics, geometry, code and author results unchanged. The independent audit is explicitly bound to this exact public derivative and reran its complete controls. The author's historical source notes remain historical. Fresh complete three-corpus identity and target-record checks are recorded separately in [CORPUS_REPLAY.json](audit/CORPUS_REPLAY.json); the target research report is absent. These observations refer to the pinned corpus snapshot, not an assertion that the repository's current catalog is byte-identical.

Only authored mathematical work, code, audit reports/results and public verification/source metadata are included. Scholarly PDFs, extracts, datasets and private coordination are excluded.

The queue change affects only this problem's Status and Turns cells; [QUEUE_DELTA.json](QUEUE_DELTA.json) records its exact byte-level boundary. This is a draft research record, with no merge, release, DOI or external outreach.

## Public references

1. Xavier Goaoc, “Helly numbers and geometric permutations,” Oberwolfach Report 44/2008, printed p. 2543: https://doi.org/10.4171/owr/2008/44
2. Cheong, Goaoc, Holmsen and Petitjean, “Helly-Type Theorems for Line Transversals to Disjoint Unit Balls,” section 6 of the inspected preprint: https://www.ens-lyon.fr/LIP/Arenaire/SYMB/teams/vegas/vegas2.pdf
3. Aronov, Cheong, Goaoc and Rote, “Lines Pinning Lines,” Theorem 1 and section 7: https://arxiv.org/abs/1002.3294

The limited literature searches in the audit found no later resolution. That negative search is not proof of present-day open status.
