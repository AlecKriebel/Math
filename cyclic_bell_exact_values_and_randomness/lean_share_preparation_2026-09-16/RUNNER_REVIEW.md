# Bounded adversarial review: fresh-build axiom reports

2026-09-16 Pacific. Completion estimate: 100% of this bounded review. This is
an agent review of the runner change, not an independent human mathematical
audit or a replacement for the final clean standalone-package run.

## Finding

No trust weakening was found in parsing the mandatory AxiomAudit reports from
the fresh clean `lake build` rather than requiring a duplicate standalone
AxiomAudit invocation. The optional repeat still compares the entire parsed
mapping for equality.

## Evidence

The current `scripts/check.py` parser was imported read-only with Python
bytecode writing disabled. It was applied to the prior completed run's actual
archived clean-build log `022.log` and standalone audit log `048.log`, under
`lean_formalization_development_archive_2026-09-16/logs/runs/20260915T041758190218Z/`.
Both log byte hashes were checked against their archived command receipts.

- Current expected inventory: 1,852 unique names.
- Parsed clean-build output: 1,852 reports.
- Parsed standalone output: 1,852 reports.
- Both complete parsed dictionaries are equal, including every axiom list.
- Both are equal to the archived machine-readable axiom receipt.
- A multiline permitted report and an axiom-free report parse correctly.
- Mutations deleting a report, adding a report, duplicating a report, adding a
  custom axiom, adding sorryAx, adding Lean.ofReduceBool, or corrupting the
  report bracket syntax were all rejected.

## Dependency and freshness review

The static audit requires AxiomAudit in the complete root import graph and
requires its ordered query list to equal both the expected inventory and all
explicitly named source declarations. Duplicate query names are rejected.
The runner removes the companion's .lake/build directory before invoking the
ordinary library build and then parses the actual captured build output.
Missing or duplicate reports therefore fail even if Lake returns success.
Compiler/dependency identities, resource/diagnostic checks, and before/after
protected-input fingerprints remain in force. The declaration parser's use of
set equality does not discard expected duplicates silently: the preceding
static check rejects those duplicates explicitly.

This change does not rebuild upstream cached Mathlib artifacts from source;
that artifact trust already existed in the former standalone-audit workflow
and is now explicit in AXIOMS.md. No claim of a second kernel implementation
or general manuscript correspondence follows from these runner checks.

## Documentation update

README.md and AXIOMS.md now state Python 3.10+ and link the official elan
installation instructions at https://github.com/leanprover/elan#installation.
The command `elan toolchain install leanprover/lean4:v4.19.0` was checked against
local elan help and the pinned toolchain file. Documentation edits were frozen
before this review. No scripts or Lean files were edited by this task.

## Checked archive identities
Archived run: `20260915T041758190218Z`.
- Command: `lake build`; log `022.log`; exit `0`; SHA-256 `73e835dbb2c61155688bf8f41b644f471fece73ed39f05a2fa3966fccd0f7bdc`.
- Command: `lake env lean CyclicBell/AxiomAudit.lean`; log `048.log`; exit `0`; SHA-256 `d7221e3947200efef403c49ba671af79a49a64432c1b45df071247642a36bdaf`.

The planned final staged run may clone the pinned dependency cache to avoid
a duplicate download; this review concerns the fresh companion rebuild and
complete reports, not a fresh source rebuild of upstream dependencies. Its
actual outcome and environment must be recorded by the parent verification.
