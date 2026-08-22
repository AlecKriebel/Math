# Response to the independent referee audit of 2026-08-22

Manuscript: *A fitness-independent family of simultaneous amplifiers beyond
relative fitness 3/2*

The report was treated as a set of claims to be checked.  Each finding was
reproduced or independently re-derived before revision.  The dispositions
below distinguish mathematical corrections from verifier and packaging
hardening.

## MATH-01: unstopped pendant waiting times

**Disposition: accepted.**  The two displayed expectations were literally
false: from an allowed near-fixation state, global extinction can occur before
the next pendant-count change with positive probability, making the
unstopped time infinite.

Lemma 9 now introduces the upper-strip exit time explicitly, stops every
pendant phase at the next pendant-count change or that exit, and assigns exit
the favorable terminal level in the trace comparison.  A bounded stopped
submartingale gives an `O(m)` expected number of stopped pendant outcomes;
the phase calculation gives `O(C)` expected calendar time per outcome.  The
resulting estimate is exactly for synchronization or upper-strip exit, which
is the stopping time used by the later regeneration blocks.

The independent re-derivation also found a boundary qualification not stated
in the report: the resident-hub loss lower bound requires `1 <= ell < m`
because its loss rate vanishes at `ell=0`.  The revised proof handles
`ell=0` by grouping the resident-hub activation phase with the following
mutant-hub phase.  This preserves the `O(C)` phase-block estimate.

## CODE-01: optimized Python removes bare assertions

**Disposition: accepted.**  The false-pass behavior under
`PYTHONOPTIMIZE=1` was reproduced.  Every verification-critical bare
assertion in the scientific certifiers, integration audit, bootstrap version
gates, and private submission validator has been replaced by an explicit
condition that raises on failure.  All Python entry points reject optimized
execution using `sys.flags.optimize`.

The replay now ends with one whole-replay success sentinel only after every
component succeeds.  A standard-library regression test checks the delivered
verifiers for `ast.Assert`, exercises optimized invocations, mutates an exact
load-bearing identity and a final integration marker in disposable copies,
and confirms nonzero failure propagation with no global success sentinel.

## CODE-02: Git identity and unsigned tag

**Disposition: accepted as a provenance limitation, not a certificate or
theorem defect.**  Local manifests and hashes establish internal byte
consistency; they do not authenticate an author or remote repository.  The
superseding source is frozen at a new annotated tag, described explicitly as
unsigned.  The referee instructions retain an optional independent remote
tag/blob/mode comparison and no longer describe that check as cryptographic
authentication.  No signature was fabricated: a signed tag would be useful
only with an already trusted signing key controlled by the human author.

## REPRO-01: dependency artifacts were not frozen offline

**Disposition: accepted and strengthened beyond the minimum request.**  The
pure-Python SymPy 1.14.0 and mpmath 1.3.0 wheels are now included in the
scientific archive, their SHA-256 hashes are pinned in `requirements.txt`,
and the bootstrap installs only from the bundled wheel directory with index
access disabled and hash checking required.  The wheel provenance and
license locations are documented.

The document build remains deliberately externally provisioned: Tectonic and
Poppler binaries are not bundled, and Tectonic may require its standard
resource cache or endpoint.  Documentation now distinguishes the offline
Python theorem replay from the non-hermetic PDF rebuild and avoids calling
the entire handoff self-contained.

## REPRO-02: release builder ignored the selected interpreter

**Disposition: accepted.**  The release path now resolves one supported
Python 3.14.6 interpreter, passes it to the replay, and uses the same
interpreter for archive construction.  The clean bootstrap passes its newly
created virtual-environment interpreter explicitly.

## CODE-03: executable modes were not checked

**Disposition: accepted.**  The source bundler now has an explicit list of
entry points, rejects unexpected source modes, emits exactly mode `0755` for
those entry points and `0644` for every other member, and verifies those
modes after archive construction.  The outer referee-package verifier checks
its own expected modes and checks byte-and-mode equality between every source
archive member and the delivered extracted tree.

## Remaining disclosed limitations

No endpoint result at `r=R_hyb`, uniformity as `r` tends to one, unrestricted
optimality over singular or size-dependent response choices, or explicit
bound on the least dyadic exponent is claimed.  The stochastic asymptotics
remain analytic proofs rather than machine-formal proofs.  The targeted
literature search is not represented as an exhaustive priority search.

The revised theorem statement, construction, response functions, sextic
threshold, rational specialization, and quantifier order are unchanged.
