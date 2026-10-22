# PR789 structural priority packet

Read REPORT.md and VERDICT.json for the bounded outcome. The exact priority remains unresolved; no earlier full negative answer was verified. This packet contains original normalized notes, custody metadata and checkers only. Full third-party PDFs, extracts, renders and HTML are in owned scratch and must not enter Git or the preprint source package.

Authenticate MANIFEST.json and verify_priority.py using the SHA-256 pins reported outside this packet before executing the checker. Use a regular, nonsymlinked path. Example (replace both external pins):

```sh
python3 -I -B /absolute/priority_structural/verify_priority.py --packet-root /absolute/priority_structural --input-root /absolute/intake --manifest-sha256 EXTERNAL_MANIFEST_SHA256 --checker-sha256 EXTERNAL_CHECKER_SHA256
```

Optional `--primary-root /absolute/scratch_priority_structural` checks every recorded primary-body binding. Without it, the checker explicitly reports zero primary files rehashed. The61 intake bindings are required in either mode. Metadata/path checks do not prove mathematical correctness, novelty or absence of earlier work.

control_runner.py replays four positive and all recorded negative custody/scope controls in disposable subdirectories under a caller-owned scratch directory. Its output must be outside the sealed packet. The manifest excludes only MANIFEST.json itself, and includes all other authored packet files.

No Git, PR, publication, tracker or external-individual communication was performed by this reviewer. No other repository candidate was processed.
