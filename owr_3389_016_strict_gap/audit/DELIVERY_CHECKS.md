# Artifact delivery checks

Local artifact checkpoint: 2026-09-23T04:04:43Z. Publication preparation: 95% complete; remote deployment remains to be checked.

- Final paper: three pages; all rendered pages visually inspected. No clipped text or equations. One benign underfull line warning in a reference URL; no overfull boxes.
- Proof, source, and scoped priority audits completed; source typo and the limits of novelty checking are explicit.
- Parent rerun reproduced the 7,016 exact checks and byte-identical results.json.
- ZIP integrity, all internal SHA-256 entries, embedded paper, and nested source archive verified. No third-party PDF, source-page image, private downloaded TeX, scratch environment, or build log is distributed.
- CFF citation file validated against the official versioned 1.2.0 JSON schema using PyYAML/jsonschema in an ignored temporary environment. The research verifier itself has no third-party dependencies.
- Zenodo metadata object and API wrapper agree; the author ORCID, date, version, licensing, and related identifiers were checked. This is local validation, not an actual Zenodo submission.
- Local website reviewed in browser at the default viewport, including a full-page screenshot. No horizontal overflow. Every local download link returned HTTP 200 with the expected content type.
- Only this new top-level research folder and its dedicated docs/papers/strict-dirichlet-gap deployment directory are staged for publication.

Remote deployment evidence will be recorded separately in DEPLOYMENT.md after push, so the archived preparation checkpoint remains a stable record.
