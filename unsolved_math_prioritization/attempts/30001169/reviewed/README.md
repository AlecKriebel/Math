# Yamabe heat-trace monotonicity: independent audit

ID 30001169, rank 822. **Accepted partial results; full problem unresolved.**

The accepted 16017-byte author public derivative is reproduced under `author/`. Its outer SHA-256 is `3f73854c0fb2b1aaaa1b807f903e681efb31be5c980feb071ca90b29c969b821`. An editorial-only change leaves the mathematics, code and results unchanged. This separate audit derivative is rebound to that exact author packet. Audit material is under `audit/`; no third-party documents or corpus content are bundled.

Read `audit/AUDIT.md` for the mathematical verdict and `audit/DERIVATIVE_REMAINDER.md` for the explicit differentiated-asymptotic justification. The independent rational implementation certifies all 750 intervals using a different exponential enclosure from the author's. The 42-record numerical scan reproduced byte-for-byte but remains uncertified numerical evidence.

Replay using standard-library Python:

- `python -I -B verify_audit.py`
- `python -I -B -O verify_audit.py`
- `python -I -B audit/replay_mutations.py`

Scripts resolve sibling paths from their own location and can run from another working directory. The envelope verifier checks a strict inventory, rejects nonregular nodes and unlisted bytecode/cache files, verifies all file hashes and the pinned author manifest, then replays both exact certificates. Passing computation is not a formalization of the analytic proof. Independently pin the final audit ZIP hash; a rewritable manifest alone cannot establish authenticity.

Safe contents: authored mathematics, source code, derived results and public-source verification metadata. No PDFs, source extracts, datasets, private sources, personal data, or private coordination.
