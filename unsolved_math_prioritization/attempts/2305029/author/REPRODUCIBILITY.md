# Reproducibility and integrity

This is a source-free literature acceptance packet. It has no numerical experiment, generated dataset, or finite search purporting to establish the theorem.

## Required external trust anchor

The caller must obtain the SHA-256 of MANIFEST.json from an independent handoff or a trusted version-control commit. Pass that value explicitly:

    python3 verify_packet.py --expected-manifest-sha256 TRUSTED_HASH

The verifier checks the manifest against that external value before trusting the manifest's file hashes. A hash stored only beside the files it authenticates is not an external trust anchor. This packet does not certify its own origin, and a changed verifier is not trusted merely because it executes successfully; review or obtain it from the same trusted publication.

## Optional source-byte check

The PDF byte streams are intentionally excluded. Retrieve the three exact public URLs in SOURCES.json separately and save them using the listed filenames. Then run:

    python3 verify_packet.py --expected-manifest-sha256 TRUSTED_HASH --source-dir DIRECTORY_WITH_PDFS

This optional operation reads the separately supplied files; the verifier itself never fetches, uploads, or publishes anything. It requires both the recorded byte counts and SHA-256 values to match. A future publisher-side PDF rebuild could change bytes without changing mathematical content; such a mismatch needs a new inspection, not silent acceptance.

## Scope of checks

The manifest covers every public payload file except MANIFEST.json itself. Unknown extra files are rejected, including PDFs, hidden files, and directories. Missing files, altered bytes, invalid filenames, malformed manifest entries, and a wrong external manifest pin are rejected.

The local validation included an intact-copy pass, a payload mutation rejected under the original external pin, a manifest mutation rejected under that pin, and a separately supplied reference-PDF identity check. These are finite integrity controls only.

## Literature checks

The source's own update and Danielyan's theorem were inspected before any new research. A bounded present-day search for corrections returned no correction to the target theorem. This is a description of the search, not a guarantee that all literature was exhausted. The theorem's published status, exact scope match, and the source's affirmative update are the positive evidence supporting acceptance.
