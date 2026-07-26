# Hostile audit of the C-057 acceptance wrapper

**Audit date:** 2026-07-26  
**Verdict:** `ACCEPT_EXACT_C057_ACCEPTANCE_WRAPPER`

## Exact scope

This verdict accepts exactly:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `results/order13_k3_hole9_certificate_acceptance.json` | 8,249 | `f9ee1ce8657206a23353f52cc64210fb015149f12fdb3f7eeeac11a6948c32b7` |
| `repro/c057/replay.py` | 13,150 | `83497204ee32158f123a873d2b682373c04d5dd63999fdcfcad2e85197301d88` |
| `repro/c057/README.md` | 1,183 | `abd3fcf4df966645d2c3c9585e6667e36307ed2a127376535f5e667ec83a74e4` |

The acceptance JSON is the sole promotion record from the immutable
candidate-only proof bundle to claim C-057. The candidate manifest itself
remains

```text
CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT
```

and the original production attempt remains

```text
RETRYABLE_NONCLAIM
NO_SAT_OR_UNSAT_CLAIM
RAW_FORWARD_REJECTED_NONCLAIM
```

No historic status was rewritten in place.

The exact accepted claim is:

> Relative to C-050 and the accepted inputs of C-055, no order-13 graph
> \(G\) with
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\) has a complement containing a
> hub-free induced \(C_9\).

Together with C-053, only the overlapping complement-\(C_5\) and
complement-\(C_7\) branches remain in the order-13 parameter-three cover.
The record explicitly does not exclude either remaining branch, complete the
parameter-three slice, exclude the parameter-four or parameter-five slices,
exclude all order-13 counterexamples, raise the lower bound to 14, or resolve
the universal conjecture. It makes no novelty or priority claim.

## Trust root and recursive coverage

The replay binds the acceptance record before parsing it by exact size and
SHA-256. The acceptance record contains 25 artifact bindings at 25 distinct
repository-relative paths. The hostile audit independently enumerated the
expected path universe and verified that every occurrence is:

- a safe relative path with no empty, absolute, `.` or `..` component;
- a nonsymlink regular file under the campaign directory;
- bound by a nonnegative exact-integer byte count and lowercase 64-digit
  SHA-256; and
- byte-identical to the record.

The 25 paths cover:

1. C-050, C-053, C-055, and the assembled branch theorem;
2. the exact formula, complete coloring bank, and constructor manifest;
3. the immutable candidate manifest and README, formula copy, additions-only
   RUP proof, and LRAT;
4. verifier B, its focused tests, review, evidence, and corrected tool-source
   provenance;
5. the external exact-byte verifier-code review, evidence, and replay;
6. the hostile mathematical coverage review, audit, and evidence; and
7. the original production outcome and its frozen nonclaim audit.

The child audits recursively bind the proof-checker executables and C sources,
the underlying mathematical and constructor acceptances, and the exact
formula semantics. Thus the wrapper does not rely on an unbound statement
that a nested audit once passed.

The replay does not explicitly require the count 25, but its immutable
acceptance-record hash fixes the complete record. This hostile audit
additionally requires the exact count, uniqueness, and expected path set, so
an omitted, duplicated, or substituted binding cannot pass the accepted
wrapper package.

## Strict JSON and path handling

The acceptance record and every parsed nested JSON output use a duplicate-key
rejecting object hook and reject `NaN` and other nonfinite constants.
Definition-level probes confirmed rejection of:

- duplicate JSON keys;
- nonfinite JSON;
- absolute paths;
- parent traversal at the beginning or inside a path;
- empty paths;
- Boolean values masquerading as byte counts; and
- a static final symlink.

Private process tests also confirmed that a symlink substituted for the exact
formula is rejected before any child replay.

The target performs static component checks followed by `Path.read_bytes`.
This leaves a narrow check/read race against a concurrent local filesystem
attacker. The campaign replay threat model assumes a quiescent local
repository; the present external audit itself uses descriptor-stable,
`O_NOFOLLOW` reads. Replacing the target reads with descriptor-stable reads
would be a defense-in-depth improvement, not a blocker for the frozen
single-user replay.

## Claim and nested-verdict audit

The acceptance scope is checked both by its immutable hash and by explicit
field validation. The hostile audit independently requires the exact claim,
consequence, seven scope exclusions, C-050 published-premise boundary,
formula census, 2,295-row coloring bank, and additions-only proof census.

The nested records have the exact expected statuses:

| record | required status/verdict |
|---|---|
| candidate manifest | `CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT` |
| original outcome | `RETRYABLE_NONCLAIM`; `NO_SAT_OR_UNSAT_CLAIM` |
| original attempt audit | `RETRYABLE_NONCLAIM`; no fresh proof replay |
| verifier B | `VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE` |
| external code audit | `ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER` |
| mathematical coverage audit | `ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION` |
| C-050 acceptance | explicit published-through-order-11 premise |

The constructor and certificate copies of the formula are also required to
be byte-identical.

## Subprocess and solver audit

The wrapper has one `subprocess.run` site inside a bounded helper. It uses no
shell, closes child stdin, captures both output streams, requires exit zero
and empty stderr, parses stdout as strict JSON, and imposes wall timeouts.
Its three direct child commands are exact argument arrays invoking:

1. the SHA-bound independent certificate verifier;
2. the SHA-bound external exact-byte code replay; and
3. the SHA-bound mathematical coverage audit.

The exact transitive non-Python child allowlist is:

```text
/usr/bin/cc
private SHA-bound drat-trim
private SHA-bound lrat-check
```

The compiler rebuilds the two proof checkers; `drat-trim` checks the
addition-only RUP proof; `lrat-check` checks the LRAT. No SAT solver is in the
exact call graph.

The documented one-command invocation was run afresh under a minimal
environment and returned:

```text
VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS
```

It checked 25 artifacts, replayed all 24 verifier mutations, preserved the
candidate and production nonclaim statuses, and left exactly `hole5` and
`hole7` live. A second invocation with Python isolated mode (`-I`) returned
byte-identical JSON.

The README and child commands do not themselves request `-I` and inherit the
caller environment. This is a nonblocking defense-in-depth caveat for a
single-user local replay. A publication wrapper could require isolated mode
and pass a minimal environment to each child.

## Coordinated-mutation audit

Thirteen hostile cases were exercised in private campaign copies. Every case
returned nonzero and emitted no success verdict:

1. acceptance-record bit flip;
2. acceptance scope changed to a universal overclaim;
3. duplicate key in the acceptance JSON;
4. nonfinite acceptance JSON;
5. formula bit flip;
6. mathematical-evidence bit flip;
7. candidate-status rewrite;
8. production-nonclaim rewrite;
9. external-code-verdict rewrite;
10. formula replaced by a symlink;
11. formula mutation coordinated with its hash change in the acceptance
    record;
12. acceptance record replaced by a symlink; and
13. simultaneous wrapper/acceptance replacement tested against this
    external audit's trust root.

A mutation of a bound artifact together with the corresponding acceptance
hash still changes the acceptance bytes and is rejected by the exact
acceptance hash hardcoded in the immutable wrapper.

Like every executable trust root, the wrapper cannot authenticate maliciously
replaced code after that replacement has already been loaded. The external
review closes this unavoidable self-reference boundary by binding both the
wrapper and acceptance record. A coordinated wrapper/acceptance replacement
therefore does not belong to the accepted package and fails this hostile
audit's exact target bindings.

No coordinated mutation was found that the accepted exact bytes falsely
promote.

## Defect ledger

- Blocking mathematical-scope defects: **0**
- Blocking artifact-coverage defects: **0**
- Blocking certificate/replay defects: **0**
- Blocking candidate/nonclaim-history defects: **0**
- Blocking path or JSON defects: **0**
- Blocking subprocess/solver defects: **0**
- Nonblocking loaded-code self-authentication caveats: **1**
- Nonblocking static-symlink race caveats: **1**
- Nonblocking environment-isolation caveats: **1**

## Reproduction

From the campaign directory:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
python3 -I -B -W error \
  reviews/c057_acceptance_wrapper_hostile/audit.py |
cmp - reviews/c057_acceptance_wrapper_hostile/evidence.json
```

The replay is read-only with respect to repository inputs, uses private
temporary directories for all mutation fixtures and checker builds, and
launches no SAT solver. It ordinarily takes about 30 seconds on the campaign
MacBook.

The hostile-audit artifacts are:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `audit.py` | 36,574 | `4e4d2ff737d5c8731a9e8b0ff02c3e2884bb346d800c6a2f68ab222c47818a3e` |
| `evidence.json` | 9,052 | `d0fa9b726528dc43bc65a42773a617f6f51065ee9ee68ef9391f4466485b9d1d` |
