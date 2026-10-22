# Independent audit of 30002711

**Qualified pass for partial mathematics; retain unsolved, five approaches used.** The frozen Proposition 3.1's nonzero-section translation needs a complete coefficient DVR. This audit supplies an exact replacement, a noncomplete counterexample, and a full use sweep. Every actual lifting ring used in the five approaches is complete, so the retained conclusions and disposition survive. The qualification must accompany the unchanged author freeze.

- `AUDIT_REPORT.md`: controlling mathematical audit, correction, dependencies, source distinctions and limits.
- `BINDING.json`: immutable author manifest/archive and payload binding.
- `AUDIT_STATUS.json`: machine-readable scoped verdict.
- `SOURCE_CHECKS.json`: public-source hashes, byte counts, fresh inspection and access limits.
- `independent_controls.py`, `INDEPENDENT_RESULTS.json`: 1,987 independent finite exact checks; no author-code imports.
- `replay_audit.py`, `REPLAY_RESULTS.json`: normal, optimized and relocated author replay; twelve independent integrity challenges.
- `AUDIT_MANIFEST.json`: hashes and byte counts of the nine audit payload files; it does not hash itself.

Python 3.10+ and the standard library suffice. From this directory:

    python3 -B independent_controls.py
    python3 -B -O independent_controls.py
    python3 -B replay_audit.py /path/to/author/publication

For the replay, the unchanged `AUTHOR_PACKET.zip` must be beside the `publication` directory. The script contains the independently supplied author manifest/archive pins, verifies exact inventories, rejects corruption in temporary copies, and never modifies the originals. The audit manifest hash should be obtained from the external audit receipt, not from an untrusted copy of the bundle itself.

The 6,527 author checks and 1,987 independent checks are finite diagnostics. They do not prove the universal cyclotomic lifting assertion. There is no general counterexample, novelty or worldwide-openness certification. Source PDFs, extracts, images, dataset contents, raw records, private sources and coordination files are excluded. No remote write was performed.
