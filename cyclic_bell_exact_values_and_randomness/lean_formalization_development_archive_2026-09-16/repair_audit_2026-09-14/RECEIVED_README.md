# Cyclic Bell Lean companion — source candidates only

**UNCOMPILED: zero kernel-certified endpoints.** This is the accumulated source
handoff, with a focused settings-appendix extension and a repaired offline
negative-control runner. It is not a proof certificate or whole-paper completion.

Start with `REVIEWER_GUIDE.md`, `COVERAGE.md`, `OFFLINE_HANDOFF.md`, and
`SETTINGS_STATEMENT_CONTRACT.md`. Earlier physical contracts remain in force.
The canonical manuscript and unrelated qubit project are neither edited nor
bundled. All dependency locks remain unchanged.

From this directory, with the pinned Lean/Lake installed:

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Lean 4.19.0 and Mathlib's exact locked revisions remain the targets. The default
build reaches all 81 Lean files, including the statement and axiom audits.
1,538 axiom queries and 25 positive/negative control files are prepared, not run.

The new appendix source starts from explicit normalized PVMs and Phi_d, derives
the four standard tables and the particular perfect-anchor cross tables,
proves source candidates for their attained peaks and nonuniformity, handles
the uniform d=2 anchor exception, and supplies the observed entropy asymptotic.
No general no-go or adversarial privacy conclusion follows from those tables.

The runner no longer accepts a crashed, killed, timed-out, or resource-exhausted
negative control as a mathematical rejection. Reproductions and reporting tests
use mocked compiler outputs and are not real Lean results. See
`SETTINGS_SELF_AUDIT.md` for the defect, scope, tests and remaining risks.

No Lean process, remote push, independent-agent audit, correspondence, manuscript
change, release or DOI occurred. Earlier reports under `history/` describe their
own frozen snapshots; they do not certify this one.
