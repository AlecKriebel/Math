# Constraint sets after adjoining a differential indeterminate

Numeric ID **30001988**, code **OWR-11575-015**, queue rank **654**.

**Disposition: unsolved, 5/5 approaches; independently audited partial results.**
The full constraint-set Turing reduction is not proved or refuted. No novelty
claim is certified. Five approaches count distinct mechanisms, not measured
research time or exhaustion of every possible idea.

## Verified scope and specialization clarification

For an ordinary characteristic-zero differential field `K`, a coefficient
`a in K`, and `z` differentially transcendental over `K`, the pair
`(delta Y - a z, 1)` is constrained over `K<z>` exactly when `a != 0`.
The coefficient need not be constant under the derivation. This classification
includes constant and differentially closed bases. It does not extend unchanged
to positive characteristic, coefficients from all of `K<z>`, or an element
that is merely algebraically transcendental. The audit supplies boundary attacks.

Here **specialization evaluates polynomial coefficient formulas in `K{z}`**
(or a suitable coefficient subring/localization). It is not a `K`-field
homomorphism from the whole field `K<z>` to `K`: the nonzero element `z-c`
is invertible in the former. For the audited denominator-free pair, evaluation
at every `c in K` is defined. Over a differentially closed base, each resulting
pair `(delta Y-c, 1)` is unconstrained, although `(delta Y-z, 1)` is constrained.
This obstructs a proposed specialization shortcut; it is not a counterexample
to the full reduction.

The general arbitrary-pair reduction remains unresolved by this investigation,
including the differentially closed-base branch and the complete constant-base
oracle-transfer dependency. The explicit hypotheses of the 2014 theorem remain
in force; a later primitive-element improvement alone does not remove them.

## Frozen artifacts and audit

- `packet/` preserves all twelve author files byte-for-byte, including its manifest.
- `audit/` preserves all ten independent-audit files byte-for-byte, including its binding.
- `audit/AUDIT.md` contains the full independent proof review and source limits.
- `LIVE_GATE.json` records the fresh publication gate separately from historical checks.
- `RELEASE_MANIFEST.json` binds every publication file other than itself.

Statements such as "audit pending" inside the frozen author packet describe
its original checkpoint; the completed independent audit is supplied separately.
The author manifest SHA-256 is
`767185ee51afce74a4227eb090aa4e896503ddbf186cc236e5deedadb4b51ab2`.
The independent binding SHA-256 is
`aed1a4ef5836440f76c31e73048f4f3378d91d8b3fc1846a05a6d2e460f8df7f`.

## Portable replay

Use Python 3 with the dependency in `audit/requirements.txt` (SymPy 1.14.0), then
run from any working directory:

```sh
python3 -B path/to/30001988/verify_release.py
```

The wrapper checks exact inventories before running code and rejects `-O`, `-OO`,
and effective `PYTHONOPTIMIZE`. It launches replays with assertions enabled and
without bytecode writes. The frozen author checks use assertions and must not be
run directly under optimized Python. Finite exact controls are regression tests,
not a proof by enumeration or an arbitrary-pair decision procedure.

Only authored mathematics/code, audit material, and public verification metadata
are published. Source PDFs, source text, corpus contents, and private coordination
files are excluded. Dataset revision binding and bounded literature-check limits
remain as stated in the audit. This is a draft research record, not a release or
DOI publication.
