# PR946 / 6000001 global Hessian audit capsule

Verdict: PASS for the assigned independent global differential geometry family. Read `RESULT.json` for structured scope and `REPORT.md` for the proof reconstruction, controls, findings and exact limitations. Authentication binds the original 33 files to immutable Git objects; it does not adopt old review verdicts.

Run the independently authored control in any directory with Python3's standard library:

    python3 independent_controls.py /absolute/path/outside/public/CONTROL_REPLAY.json

Compare the resulting JSON with `CONTROL_RESULTS.json` after dropping only `utc`. No original candidate program is imported or executed. This control is supplementary; the universal mathematical argument is written in the report.

The public release allowlist is exactly these eight files plus `MANIFEST.json` itself:

- `AUTHENTICATION.json`
- `CONTROL_RESULTS.json`
- `independent_controls.py`
- `SOURCE_AUTHENTICATION.json`
- `REPORT.md`
- `RESULT.json`
- `RESEARCH_LOG.md`
- `README.md`

`MANIFEST.json` gives byte sizes and SHA-256 digests for those eight files. Its own digest is returned outside the capsule as the final seal, avoiding circular self-hashing. Everything under `private/`, including original source bodies, extracted text, screenshots and replay scratch, is excluded. There is no wildcard publication permission. No artifact in this capsule authorizes publication, a merge or a novelty claim.

All files in this capsule are final after the external seal. Overall source interpretation, other-family adjudication, reproduction and priority remain root gates.
