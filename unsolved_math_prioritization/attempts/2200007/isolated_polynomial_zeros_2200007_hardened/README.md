# Prior disproof disposition for Conjecture 4

Problem 2200007 / AMR-021-0007, rank 899, is **false by credited prior work**.
The counterexample is due to DannyExperiments, released on 10 August 2026:
[research release, DOI 10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290).
No new mathematical discovery or independent research approach is claimed.

The prior quartic is a sum of nine real quadratic squares in ten variables,
with 1,152 isolated real zeros. At k=2 and l=10, the proposed maximum is
2^10=1,024. This settles the universal equality in Conjecture 4 negatively.
It does not determine the exact maximum requested by the adjacent Problem 3.

## Evidence

- `SCOPE_BRIDGE.md` checks the precise source hypotheses and supplies a short,
  newly written verification of the credited certificate.
- `SOURCE_METADATA.json` separates fresh inspection from inherited evidence.
- `STATUS.json` records the terminal prior-disproof disposition and zero new
  approaches. `RESEARCH_LOG.json` bounds the searches and records limitations.
- `verify_certificate.py` performs exact arithmetic checks of the single prior
  example. `certificate_results.json` is its deterministic output.
- `verify_package.py` checks the complete frozen inventory and replays the
  certificate. Run `python3 -I -S -B verify_package.py` from any working directory,
  using the script's actual path. Only the Python standard library is needed.

The freeze contains original verification prose and code, plus public citation
and verification metadata. It contains no third-party manuscript, PDF, extract,
dataset contents, or private coordination material. No queue or remote writes
were performed while preparing it. A separate review is required before any
publication disposition is treated as accepted.

This is mathematical verification, not human peer review or proof-assistant
certification. The bounded search is not a literature-completeness or absolute
priority claim. No source is retrieved during portable replay.

## Audited replay hardening

This derivative preserves the original mathematical certificate and result.
The package verifier requires isolated, no-site Python startup, fixes the exact
nine-file inventory independently of the mutable internal manifest, and passes
its optimization mode to the child. Use `python3 -I -S -O -B verify_package.py`
for an optimized replay, or `-OO` instead of `-O` for optimization level two.
`-B` suppresses new bytecode writes; it is not by itself a cache-authenticity
control. The two entrypoint scripts run from source, and `-I -S` excludes sibling
imports, PYTHONPATH, and site startup hooks. A trusted Python installation is
still required. Compare the externally supplied archive and manifest hashes
before execution: a self-updated internal manifest is not an authenticity root.
The separate audit records the original freeze and this derivative distinctly.
