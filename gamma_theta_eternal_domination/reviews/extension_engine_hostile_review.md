# Hostile review: one-vertex-extension engine

## Verdict

**ACCEPTED for a validation-gated search of the precisely delimited
110,537-origin one-vertex-extension universe.**

No open critical-, high-, or medium-severity correctness defect remains in
the reviewed engine.  The coverage loop, global deduplication invariant,
transactional resume logic, exact filter, and fail-closed candidate handling
match the mathematical protocol.

This verdict is **not** a `CERTIFIED-FINITE` result and does not assert that
the full search has run.  A negative result still requires the separately
specified independent post-run coverage audit, including reconstruction of
all raw extensions and an isomorphism check for every raw-to-canonical pair.

Review date: 2026-07-25.

Reviewed artifact SHA-256 digests:

- `src/search/extension_killtest.py`:
  `44c6db503a41def3074099cfedd098ba3138cfc22b6cf12676c57c2081f1295d`;
- `tests/test_extension_killtest.py`:
  `b74f670af8a889cbb862430f3fc406315e4f2f17577d41c75ec7ea8c9c834d02`;
- `math/extension_engine_protocol.md`:
  `081e10c6eb9eb379f663b126eff5c6ebfc650a88229b85efa62d89fdeb99a613`;
- `math/extension_search_scope.md`:
  `862101dd76d98b590cfd1373680974a92038ef882a2472cdf602f79a542d6c5c`;
- `reviews/extension_engine_hostile_probe.py`:
  `ca16636c3b55a45e312ea93241f563e6de0e293244087f32cacaa0da60e819bc`;
- `instances/mmv2022_table9.csv`:
  `801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d`;
- `results/mmv2022_parameters.csv`:
  `ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6`;
- local `labelg` executable:
  `ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0`;
- nauty/Traces 2.9.3 source archive:
  `9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b`.

## Reviewed scope

The review traced and adversarially probed:

- the certified-host join and the exact mask interval for every host;
- raw-origin retention, canonical-graph deduplication, and one-evaluation-per-
  canonical-key behavior;
- SQLite initialization, batch commits, final-host commits, replay, and
  completed-host validation;
- canonicalizer input/output checks and executable/source pins;
- candidate freezing, inconsistent candidate states, and completion blocking;
- wall/memory gates and malformed numeric inputs;
- writable/trusted path aliasing;
- the distinction between an engine completion record and a certificate-
  backed finite theorem.

The bounded hostile probe is
`reviews/extension_engine_hostile_probe.py`.  It does not launch the full
campaign.  It checks the counterfeit-`labelg` rejection, malformed candidate
state, non-finite gates, path alias rejection, and an injected final-batch
failure followed by exact-mask replay.

All 16 extension-engine unit tests and the hostile probe passed with
`PYTHONWARNINGS=error`.  The entire campaign suite passed 77 of 77 tests.

## Coverage and pruning audit

The byte-pinned catalog and parameter table select exactly 55 distinct,
connected hosts with the required distribution:

| order | host domination number | count |
|---:|---:|---:|
| 10 | 2 | 2 |
| 11 | 2 | 51 |
| 11 | 1 | 2 |

For a host of order \(n\), the engine iterates exactly the integer masks
\(1,\ldots,2^n-1\).  The new vertex is adjacent to exactly the vertices whose
bits occur in the mask.  Therefore the raw cover has

\[
2(2^{10}-1)+53(2^{11}-1)=110{,}537
\]

origins.  The empty-neighborhood extension is correctly omitted because the
search universe is connected.

The two domination-one hosts remain in the raw ledger but are soundly pruned
from the decisive eternal-game filter.  Every globally new canonical graph
receives exact \(\gamma\) and \(\alpha\) values.  Every graph reaching
\(\gamma=\alpha=3\) is run through both one-guard implementations; the
decisions and greatest closed families must agree.  The private-region
obstruction is recorded only as an additional checked witness and never
replaces an eternal-game decision.

Canonical Graph6 strings, not cryptographic hashes, are the global
deduplication keys.  Every `(host_id, neighborhood_mask)` remains a separate
origin row, and each origin increments the representative's multiplicity in
the same transaction.  Thus deduplication cannot itself erase coverage.

The internal completion audit checks count, minimum, maximum, next mask,
status, stream hash, and origin multiplicities.  Because the origin primary
key makes masks distinct, `count = maximum = 2^n-1` together with
`minimum = 1` proves that the complete integer interval is present.

## Checkpoint and crash-safety audit

Schema creation, configuration metadata, all host rows, and the schema
version are now enclosed in one explicit transaction.  The injected
initialization-failure test confirms that neither versioned metadata nor
partial tables survive rollback.

The resume digest binds the engine and every local runtime module used by
both evaluators and the private-obstruction check, as well as the Python
implementation, version, and executable.  A dependency edit therefore cannot
silently mix old and new evaluations in one ledger.

For each batch, canonical rows, origin rows, multiplicities, and the next
mask are one transaction.  For a final host batch, the completed status and
canonical-stream hash are computed and committed in that same transaction.
An injected failure while computing the final stream hash rolled the complete
batch back to its previous next mask; a replay then processed the exact same
mask interval and stored a non-null stream hash.  A defensive resume path
also repairs the legacy state in which a fully counted completed host has a
NULL stream hash, while rejecting a non-NULL mismatch or inconsistent count.

The JSON checkpoint and per-host JSON files are atomic, human-readable
mirrors.  They are not the source of truth.  A crash after a SQLite commit but
before a JSON replacement therefore loses no origin.

## Candidate-state audit

A first positive eternal decision is frozen before any later graph is
evaluated.  The resulting artifact is explicitly marked
`FROZEN-UNREVIEWED-CANDIDATE`, contains both eternal-family representations,
and does not claim conjecture resolution.

Candidate state is detected redundantly from:

1. the frozen-artifact marker;
2. canonical rows categorized `candidate_eternal_3`; and
3. provenance rows categorized `candidate_eternal_3`.

Any one of these blocks every resume and blocks the completion audit.  The
summary retains either the artifact path or an explicit candidate digest and
reports missing-marker, missing-row, or missing-file inconsistencies.  The
former `continue_after_candidate` escape has been removed; there is no
unauthenticated way to advance the search past an unreviewed candidate.

If a crash leaves only an orphan frozen file before the SQLite transaction
commits, the next run reprocesses the same authoritative mask, reuses the
atomic file, records the redundant database indicators, and stops.  It does
not advance to a later origin first.

## Canonicalization and malformed-input audit

The engine now requires both the nauty/Traces 2.9.3 source-archive pin and the
exact audited local `labelg` executable hash.  A counterfeit executable in a
correctly named directory was rejected.  For every invocation, the number of
returned records must equal the number of input records, every Graph6 record
must parse strictly, and order and size must be preserved.

These checks make accidental executable substitution and malformed output
fail closed.  They do not constitute the independent isomorphism proof
required after a full empty run; the protocol correctly preserves that as a
certification gate.

Boolean, noninteger, nonpositive, NaN, and infinite resource/batch controls
are rejected before a database is opened.  Resolved writable paths are
checked for equality and nesting, including symbolic-link aliases, so a JSON
checkpoint cannot replace its SQLite ledger and the two final exports cannot
overwrite one another or a trusted input.

## Findings resolved during review

The following issues were reproduced, reported, and fixed before this
verdict:

1. **High, candidate state:** an unauthenticated continuation flag could
   obscure an unreviewed candidate on eventual completion.  The flag was
   removed and candidate indicators are now redundant and fail closed.
2. **Medium, canonicalizer provenance:** a suitably named directory could
   spoof the `labelg` provenance check.  The exact executable hash is now
   pinned.
3. **Medium, final-host crash window:** completed status could commit before
   the canonical-stream hash.  Both values now share the final-batch
   transaction, with a defensive legacy repair.
4. **Medium, initialization crash window:** schema/version publication could
   precede configuration and host metadata.  Initialization is now one
   rollback-safe transaction.
5. **Medium, path aliases:** output roles could overwrite the SQLite ledger,
   one another, or trusted inputs.  Resolved path-role validation now runs
   before writable state is opened.
6. **Medium, resource controls:** NaN values disabled comparison-based gates.
   All numeric controls now require appropriate finite types and ranges.
7. **Medium, source provenance:** a missing nauty archive was previously
   accepted while the configuration still recorded its expected digest.  The
   exact archive is now required as well as hashed.
8. **Medium, mixed evaluator versions:** imported evaluator dependencies were
   not part of the resume digest.  A deterministic runtime-source manifest
   and Python-runtime identity now prevent cross-version ledger reuse.

## Remaining nonblocking limitations

- **Low, advisory resource envelope.**  Resident memory is sampled after a
  committed batch from the parent Python process, and the wall gate
  deliberately drains the current host.  It is not an operating-system hard
  cap and does not include a transient child-process peak.  With the pinned
  `labelg`, small order, batch size 256, one-process launch, and documented
  one-host overshoot, this does not threaten coverage correctness.  Resource
  telemetry should still be watched during the first production host.
- **Low, pre-existing candidate artifact.**  If a candidate filename already
  exists, reuse checks its full canonical-graph digest but does not replay
  every field of the old artifact before stopping.  This cannot produce a
  false negative or allow further search: it leaves the run pending review.
  Starting production with a clean/versioned candidate directory, then using
  the independent candidate checker, is sufficient.
- **Certification gate.**  The internal audit does not independently prove
  that `labelg` preserved isomorphism, reconstruct every raw record, or
  independently repeat every stored exact evaluation.  The protocol already
  requires those checks before any `CERTIFIED-FINITE` claim.  This is the
  principal remaining artifact, not an engine flaw.

## Final conclusion

The engine can be launched after the campaign's first-72-hour validation gate
opens.  Its output may be used as exploratory search evidence and as input to
the independent coverage/certificate checker.  Neither an empty engine run
nor this review alone is a mathematical result.
