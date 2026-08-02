# Release record: universal-db-obstruction-v1.0.0

## Public record

- Release:
  <https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>
- Reader-facing page:
  <https://aleckriebel.github.io/Math/papers/no-universal-death-birth-amplifier/>
- Version DOI: <https://doi.org/10.5281/zenodo.21753405>
- Concept DOI: <https://doi.org/10.5281/zenodo.21753404>
- Published: 2026-08-02 02:09:10 UTC (2026-08-01 19:09:10 PDT)
- Tag target: `cf61bfdffb1531b328fb0dcd147714782932036b`
- GitHub state: public, non-draft, non-prerelease

The release tag and the pushed `main` commit resolved to the same object at the
publication check.

Zenodo record 21753405 was created at 2026-08-02 02:10:07 UTC. Its public
metadata reports version `universal-db-obstruction-v1.0.0`, creator Alec
Kriebel, and the exact GitHub tag as its related identifier. The automatic
Zenodo snapshot preserves the public monorepository; the smaller, scoped
GitHub assets above are the direct reproduction package for this paper.

## Frozen manuscript hashes

```text
b0e066fa5c9db3b255b86ef8bd8f7330d071e2f0876b5e155e9f3b339e14a1f0  paper/main.tex
c27538ccc00ae6816020e39599a3a81ea7f81df58f1b0df543c1c14ff9e9d69b  paper/n4_certificate.tex
1572d2fd4abd495c4eed61075afdc1dbd74a7d90fb0fe1f379bfa12c50fbf69b  no_universal_death_birth_amplifier_v1.0.0.pdf
```

The PDF build epoch is pinned. Two independent release builds were
byte-for-byte identical. All 13 rasterized pages also matched the final hostile
audit's visually inspected PDF, whose only byte-level difference was its
earlier embedded creation time.

## Release assets

```text
fa929f0dd91e845199978a3e60d639260c3b4c21b44976ddc8539fff6ab33322  clean_archive_reproduction.log
6d018e1bf7c7f93f763f0185d2e35d249e4a47c5eb0d9e3e3a444ebfe6aac6c9  no_universal_death_birth_amplifier_source_v1.0.0.zip
1572d2fd4abd495c4eed61075afdc1dbd74a7d90fb0fe1f379bfa12c50fbf69b  no_universal_death_birth_amplifier_v1.0.0.pdf
b52923037809d5f0550aeda7a7dd246f03f69b93e4e793c3b0ed0d3d5811d1aa  universal_db_obstruction_reproducibility_v1.0.0.tar.gz
```

GitHub's release API reported the same digest for every asset. The source ZIP
and reproducibility tarball passed their archive-integrity checks. The full
archive contains 82 entries and excludes `.venv`, caches, temporary files,
`.DS_Store`, and `.git` metadata.

## Verification

The complete `make paper1` target was run from a clean Git archive using
Python 3.14.6, SymPy 1.14.0, and Tectonic 0.16.9. It passed:

- six exact Markov-chain unit tests;
- the general fixed-graph obstruction verifier;
- the asymmetric directed strong-selection and column-scaling checks;
- the triangle derivation, independent subset-chain solver, and no-import
  hostile replay;
- both symmetric `K_4` orbit certificates and independent full 14-state
  cross-checks;
- exact two-class and windmill lumpability checks under Bd and dB;
- the deterministic 13-page manuscript build.

The public project page and PDF returned HTTP 200 after deployment, and a
fresh public release-asset download reproduced the frozen PDF hash.

## Publication boundaries

This is a public independent-research release, not a journal submission. No
external specialist review or external outreach occurred. The automatic
Zenodo deposit is verified at version DOI `10.5281/zenodo.21753405`.
