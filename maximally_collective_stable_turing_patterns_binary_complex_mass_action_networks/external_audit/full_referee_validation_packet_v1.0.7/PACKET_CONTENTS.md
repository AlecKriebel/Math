# Packet contents

| Path | Purpose | Evidentiary status |
|---|---|---|
| `REFEREE_PROMPT.md` | Neutral review assignment and required report format | Review instructions |
| `paper/main.pdf` | Definitive rendered manuscript | Object of review |
| `paper/supplement.pdf` | Definitive rendered supplement | Object of review |
| `review_maps/` | Theorem summary, proof skeleton, claim ledger, and dependency maps | Author-provided navigation aids; verify independently |
| `repository/` | Exact portable source, proof, data, tests, figures, certificates, and full replay | Author-provided executable evidence |
| `minimal_verifier/` | Smaller exact replay and verifier subset | Convenience copy sharing the repository's verifier source |
| `RUN_COMPLETE_AUDIT.sh` | Preserving wrapper for the two replays, all verifier entrypoints, and audits | Orchestration only |
| `RUN_ALL_VERIFIERS.py` | Explicit fail-fast runner for all 38 verifier entrypoints | Orchestration only |
| `TESTED_ENVIRONMENT.md` | Required tools and recorded successful versions | Reproducibility metadata |
| `PROVENANCE.md` | Tag, commit, DOI, and definitive source hashes | Integrity/provenance metadata |
| `SHA256SUMS.txt` | Hash of every supplied file except itself | Initial packet-integrity check |

The packet deliberately excludes previous AI verdicts, author feedback
dispositions, and specialist recommendations so that they do not anchor the
referee's conclusion.  Stored program outputs inside `repository/` are retained
for provenance and reproducibility comparison; they must not be counted as an
independent replay.

Third-party publications cited by the paper are not redistributed here.  They
should be obtained through normal scholarly channels when their content must be
checked.
