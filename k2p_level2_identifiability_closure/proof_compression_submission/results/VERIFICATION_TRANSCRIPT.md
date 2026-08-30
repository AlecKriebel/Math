# Verification transcript

This is the clean operational transcript for the PC-PARTIAL reader-derivative
rebind to the current 231-file theorem release lock.  Runtimes are informative,
not part of any byte-stable certificate.

| Command | Outcome | Stable payload | Observed wall time |
|---|---|---|---:|
| `build_compressed_release.py` | `PC-PARTIAL` | result `91583a64327f6137b0b55676861eb13ba12e7a0c269da25efb17d8880dea1cc3`; crosswalk `d2591c67eb5168b6601efa81b762e905239accd26acf69fe284f1b690de1d480` | < 1 s |
| `verify_compressed_release.py --check` | `PASS`; zero unresolved mathematical records; current C09 file/payload binding exact | result `91583a64327f6137b0b55676861eb13ba12e7a0c269da25efb17d8880dea1cc3` | < 1 s |
| `verify_old_new_equivalence.py --write` | seven commands `PASS` | `09a6976c9460c2c070f67b0bdf71403980eea44d82718a5f0832442b5f84b090` | 123.082 s |
| `verify_old_new_equivalence.py --check` | byte-identical deterministic replay `PASS` | `09a6976c9460c2c070f67b0bdf71403980eea44d82718a5f0832442b5f84b090` | 123.787 s |
| `run_compression_mutations.py --write` | twenty of twenty corruptions rejected | `684e8be68dc19f63505ecf111a02a81015d33852f01301bd0dcf2cf5c750cbe5` | 0.315 s |
| `run_compression_mutations.py --check` | byte-identical deterministic replay `PASS` | `684e8be68dc19f63505ecf111a02a81015d33852f01301bd0dcf2cf5c750cbe5` | 0.307 s |

The mutation set covers an omitted raw record, a count-preserving false-rank
reassignment, a missing restoration child, a wrong restoration parent, a
broken exact probe transport, cubic/quartic/quintic degree reassignment,
high-degree family reassignment, false promotion from `PC-PARTIAL`, and
optimized Python.  It also covers stale file and payload digests in the C09
current-artifact section, malformed, omitted, duplicated, and role-swapped
fields, and a duplicate-name coverage certificate.  Every structured case is
resealed before semantic verification, so the test does not succeed merely
because a payload hash was left stale.

The old/new result and mutation result are deterministic JSON objects.  They
deliberately omit timestamps and runtimes; this transcript is the separate
operational record.
