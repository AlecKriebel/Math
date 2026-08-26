# Verification transcript

This is the clean operational transcript for the PC-PARTIAL reader-derivative
rebind to the current 230-file theorem release lock.  Runtimes are informative,
not part of any byte-stable certificate.

| Command | Outcome | Stable payload | Observed wall time |
|---|---|---|---:|
| `build_compressed_release.py` | `PC-PARTIAL` | result `9bcac0f0d8d645393c456807d05eb27bf9a3fce068fa7c8c18f399c18cf993fa`; crosswalk `d2591c67eb5168b6601efa81b762e905239accd26acf69fe284f1b690de1d480` | < 1 s |
| `verify_compressed_release.py --check` | `PASS`; zero unresolved mathematical records | result `9bcac0f0d8d645393c456807d05eb27bf9a3fce068fa7c8c18f399c18cf993fa` | < 1 s |
| `verify_old_new_equivalence.py --write` | seven commands `PASS` | `b20831ebf10e83a5d0984d6c1ab8a5dd4cfd5ea85f72520e95e564d9ccf9b3f3` | 70.887 s |
| `verify_old_new_equivalence.py --check` | byte-identical deterministic replay `PASS` | `b20831ebf10e83a5d0984d6c1ab8a5dd4cfd5ea85f72520e95e564d9ccf9b3f3` | 72.409 s |
| `run_compression_mutations.py --write` | eleven of eleven corruptions rejected | `eef0bba326d3e9dff0d26add67ec01717aa254a434f51f057333a39f21bbe075` | 0.295 s |
| `run_compression_mutations.py --check` | byte-identical deterministic replay `PASS` | `eef0bba326d3e9dff0d26add67ec01717aa254a434f51f057333a39f21bbe075` | 0.321 s |

The mutation set covers an omitted raw record, a count-preserving false-rank
reassignment, a missing restoration child, a wrong restoration parent, a
broken exact probe transport, cubic/quartic/quintic degree reassignment,
high-degree family reassignment, false promotion from `PC-PARTIAL`, and
optimized Python.  Every case is resealed before semantic verification, so
the test does not succeed merely because a payload hash was left stale.

The old/new result and mutation result are deterministic JSON objects.  They
deliberately omit timestamps and runtimes; this transcript is the separate
operational record.
