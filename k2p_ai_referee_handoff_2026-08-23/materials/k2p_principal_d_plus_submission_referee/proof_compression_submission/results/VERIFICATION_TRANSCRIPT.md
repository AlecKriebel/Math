# Verification transcript

This is the clean operational transcript for the first complete PC-PARTIAL
integration on the local Apple-silicon workstation.  Runtimes are informative,
not part of any byte-stable certificate.

| Command | Outcome | Stable payload | Observed wall time |
|---|---|---|---:|
| `build_compressed_release.py` | `PC-PARTIAL` | result `51ffacd91269975c22379d68c40edc5402519917f4d904f81a924f78dea9cd6d`; crosswalk `d2591c67eb5168b6601efa81b762e905239accd26acf69fe284f1b690de1d480` | < 1 s |
| `verify_compressed_release.py --check` | `PASS`; zero unresolved mathematical records | result `51ffacd91269975c22379d68c40edc5402519917f4d904f81a924f78dea9cd6d` | < 1 s |
| `verify_old_new_equivalence.py --write` | seven commands `PASS` | `9fcc15a8f6a5559e1aea7ed120e2456246bf9784b19d38af0948768f9206c915` | 75.765 s |
| `verify_old_new_equivalence.py --check` | byte-identical deterministic replay `PASS` | `9fcc15a8f6a5559e1aea7ed120e2456246bf9784b19d38af0948768f9206c915` | 75.360 s |
| `run_compression_mutations.py --write` | eleven of eleven corruptions rejected | `eef0bba326d3e9dff0d26add67ec01717aa254a434f51f057333a39f21bbe075` | 0.346 s |
| `run_compression_mutations.py --check` | byte-identical deterministic replay `PASS` | `eef0bba326d3e9dff0d26add67ec01717aa254a434f51f057333a39f21bbe075` | 0.315 s |

The mutation set covers an omitted raw record, a count-preserving false-rank
reassignment, a missing restoration child, a wrong restoration parent, a
broken exact probe transport, cubic/quartic/quintic degree reassignment,
high-degree family reassignment, false promotion from `PC-PARTIAL`, and
optimized Python.  Every case is resealed before semantic verification, so
the test does not succeed merely because a payload hash was left stale.

The old/new result and mutation result are deterministic JSON objects.  They
deliberately omit timestamps and runtimes; this transcript is the separate
operational record.
