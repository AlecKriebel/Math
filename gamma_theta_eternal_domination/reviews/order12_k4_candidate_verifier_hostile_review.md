# Hostile review: independent order-12, parameter-four candidate verifier

**Review date:** 2026-07-26  
**Overall verdict:** `ACCEPT`  
**Mathematical verdict:** `ACCEPT_DEFINITION_LEVEL_CERTIFICATE_SOUNDNESS`  
**Operational verdict:** `ACCEPT_RELEASE_CLI_AND_TRACE_BOUNDARY`

No accepted counterexample is asserted to exist.  This review establishes only
the conditional claim: if the frozen verifier accepts a strict candidate JSON
file, the graph encoded by that file really satisfies

\[
  \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=4<\theta(G)
\]

in the one-guard-moves model.  Rejection remains explicitly non-exhaustive.

## 1. Frozen source set

| Artifact | SHA-256 |
|---|---|
| `src/verifier_k4_candidate/checker.py` | `d9466268e22027fd61d82c92a96645bb84201795160f22ee4d6bcb9f2115be9e` |
| `src/verifier_k4_candidate/cli.py` | `2f7f7a640acdfb8dc38e08163d662f8fdf6cbcb930970cd3b8856d5253493133` |
| `src/verifier_k4_candidate/__init__.py` | `44776c9d6814bf4947e1b6440abb66e1087d81867f09b8f342d8585e02c61aca` |
| `src/verifier_k4_candidate/__main__.py` | `0f7d54f3fbb1f79a85eb8110f11793db99da6f3c61ee979de5abe9a1b5f3fdb3` |
| `src/verifier_k4_candidate/README.md` | `80a8a90e95e65375e01174d164326561750e886226966ca6eeef96257d0dc421` |
| `tests/test_verifier_k4_candidate.py` | `41d981227e8f23b98974aaf4ce7deb2c652f728deb12d656ba01d005db1dc113` |
| `math/lemmas/order12_k4_candidate_certificate.md` | `380ec85af4e8104fb8725d2875809385de912a01268042f7ce9a3ba3c4035bd2` |

The package imports only the Python standard library.  It imports neither the
search encoder nor either earlier campaign verifier core.

The theorem and CLI are correctly scoped to a JSON file passed through
`load_candidate` and `parse_candidate`.  The low-level `Candidate` dataclass
is also exported for programmatic use, but callers that construct one by hand
are responsible for the parser's structural invariants.  This does not weaken
the reviewed JSON acceptance implication.

## 2. Strict input and graph identity

The loader limits the source to 2,000,000 bytes, hashes the exact bytes read,
requires UTF-8 JSON, rejects duplicate object keys and non-finite constants,
and passes the decoded object through an exact-key schema.  Integer positions
use `type(value) is int`, so JSON Booleans cannot masquerade as vertices or
claims.  Edges, states, branch sets, and cycle witnesses receive the stated
range, uniqueness, cardinality, and ordering checks.

The graph is reconstructed solely from the sorted edge array.  The verifier
then recomputes:

- the labeled graph6 record;
- SHA-256 of that exact ASCII record, without a newline; and
- SHA-256 of the compact canonical edge-array serialization.

Acceptance requires all three declared identity fields to agree.  A separate
implementation of the graph6 bit order agreed on 2,048 deterministic
order-12 graphs.  The encoding uses the standard higher-endpoint-major order
\((0,1),(0,2),(1,2),(0,3),\ldots\), and its padding and order byte are
correct.

The verifier deliberately makes no canonical-label claim.  This is accurately
documented.  A final campaign witness would still need a separately produced
canonical graph6 record for packaging, but lack of canonicalization does not
affect the graph's mathematical properties.

## 3. Exact domination-number proof

The checker finds the first dominating set by exhaustive enumeration from
size zero upward.  It independently checks the supplied four-set and records
all dominating triples.  The decisive check passes only if the exact
enumeration returns four, the declared four-set dominates, and no triple
dominates.

The proof in `order12_k4_candidate_certificate.md` is correct even using only
the latter two facts: domination is upward closed, so a dominating set of
size at most three could be extended to a dominating three-set on twelve
vertices.  Thus the declared witness gives \(\gamma(G)\le4\), while the 220
triple checks give \(\gamma(G)\ge4\).

A clean-room mask evaluator agreed with the verifier's exact \(\gamma\),
\(\alpha\), and maximal-independent-set profile on 256 deterministic random
graphs.

## 4. Literal one-guard eternal-family audit

The supplied family must be nonempty and consist of unique, sorted four-sets.
For each valid state \(D\), the verifier first checks domination.  It then
executes the exact quantifier order

\[
  \forall D\in\mathcal D\
  \forall r\in V(G)\setminus D\
  \exists u\in D\cap N_G(r):
  (D-\{u\})\cup\{r\}\in\mathcal D.
\]

The implementation has all four high-risk details right:

1. vertices already occupied by guards are skipped;
2. the responding guard is selected from the current state;
3. `graph.has_edge(guard, attacked)` is required; and
4. the successor is constructed by removing exactly that guard and adding
   exactly the attacked vertex.

Every successor belongs to the same supplied family and hence is among the
states separately checked to dominate.  No reachability-only closure, token
teleportation, all-guards move, or all-guards-move model is admitted.

An independent integer-mask predicate agreed on 4,096 graph/family pairs.
Targeted mutants whose sole transition used a nonedge, or whose two listed
states could only be related by moving multiple guards, were both rejected.
For a valid family the report separately counts \(8|\mathcal D|\) unoccupied
attacks and \(4|\mathcal D|\) occupied attacks excluded.

Therefore an accepted family proves \(\gamma^\infty(G)\le4\).  The already
proved elementary inequality \(\gamma(G)\le\gamma^\infty(G)\), together with
the preceding exact \(\gamma(G)=4\), proves
\(\gamma^\infty(G)=4\).

## 5. Complete complement-coloring exclusion

The coloring normalization is sound.  The checker first verifies from the
graph itself—not merely from a declaration—that vertices \(0,1,2,3\) are
independent in \(G\).  They are consequently a \(K_4\) in
\(\overline G\).  Every proper four-coloring of \(\overline G\) gives these
four vertices distinct colors, and one unique color permutation sends their
colors to \(0,1,2,3\).

The remaining search space is therefore exactly

\[
  \{0,1,2,3\}^{\{4,\ldots,11\}},
\]

containing \(4^8=65{,}536\) rows.  For each row the checker tests every
nonedge of \(G\), which is exactly every edge of \(\overline G\).  A row is
proper precisely when no such edge is monochromatic.  The loop does not stop
after finding a proper row.  Acceptance requires zero proper rows, proving

\[
  \chi(\overline G)\ge5
  \quad\Longleftrightarrow\quad
  \theta(G)\ge5.
\]

A structurally different recursive coloring implementation agreed on both
the number of proper rows and the first lexicographic proper coloring for 64
order-12 graphs with the fixed anchor.  This also killed the mutation that
colors \(G\) rather than \(\overline G\).

## 6. Coloring trace

The optional trace is created with exclusive-create semantics.  It binds the
computed graph6 record, the anchor, all outer vertices, every row index and
eight-digit assignment, a conflict or proper marker for each row, and a final
row/proper count.  The SHA-256 in the report covers the complete byte stream.

The hostile probe parsed two independently generated traces row by row:
one with 65,536 proper rows and one with none.  Across 131,072 rows it checked:

- consecutive row indices and the corresponding base-four assignments;
- every declared conflict is an actual monochromatic edge of
  \(\overline G\);
- the conflict is the lexicographically first such edge, as documented;
- every `proper` line has no complement-edge conflict;
- the summary and line count; and
- the reported SHA-256 against the file bytes.

All checks passed.  Existing trace paths are rejected without overwrite, and
a trace created during a failed internal write is removed.

## 7. Independent-set consequences

The decisive core does not need to trust the separate \(\alpha\) or
independent-domination routines.  From

\[
  \gamma(G)\le i(G)\le\alpha(G)\le\gamma^\infty(G)
\]

and the now established endpoint value four, one obtains
\(i(G)=\alpha(G)=4\).  Every maximal independent set then has size four, so
\(G\) is well-covered.

The verifier nevertheless recomputes these statements directly:

- it exhausts all 792 five-sets and runs a complete descending
  maximum-independent-set search;
- it enumerates all \(2^{12}\) subsets to obtain every maximal-independent-set
  size; and
- it confirms that every independent four-set appears in the supplied
  eternal family.

These are correctly classified as consistency checks.  A defect in a
redundant check cannot erase a definition-level counterexample.

## 8. Ancillary certificates and separation

Connectedness, a triangle, a four-cycle, maximum degree at least four,
nonplanarity, and an induced odd hole or antihole are not used to establish
the defining counterexample inequalities.

The nonplanarity certificate is nevertheless rigorous at the strict-JSON
boundary.  Parsing enforces nonempty, pairwise-disjoint branch sets.  The
checker verifies each branch set is connected and every required pair is
joined for a \(K_5\) model, or every cross-part pair for a \(K_{3,3}\) model.
Extra edges are harmless.  Wagner's theorem then proves nonplanarity.

The declared imperfection witness is checked pair by pair in the stated cyclic
order, with the edge predicate complemented exactly for an antihole.  A
separate degree-two induced-subgraph search independently looks for an odd
hole or antihole.

The classification boundary is mathematically appropriate:

- the four decisive checks are graph identity, exact \(\gamma=4\), the
  literal eternal family, and \(\theta\ge5\);
- all other checks are consistency checks;
- all decisive checks passing yields
  `mathematical_counterexample_verified=true`; and
- an ancillary failure changes the status to
  `VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS` but does not convert a
  proved counterexample into a rejection.

The hostile probe exhaustively tested all 32 combinations of the four
decisive truth values and one ancillary truth value.  Only the all-four-true
rows were classified as mathematical counterexamples, and ancillary status
affected only campaign completeness.

For publication under the campaign's stronger packaging requirements, the
desired state remains `campaign_consistency_complete=true`.  The alert status
is correctly an escalation/freeze condition rather than permission to ignore
a contradictory published restriction.

## 9. CLI behavior and resolved hostile finding

The CLI has the documented result-code split:

- `0` when the mathematical counterexample is verified, including consistency
  alerts;
- `1` when no counterexample is verified; and
- `2` for malformed input or an I/O failure.

The unit suite exercises rejection, malformed input, trace creation, and
no-overwrite behavior.  The hostile probe separately exercised the accepted
and consistency-alert branch with a synthetic report.

During this review, the original frozen loader allowed a deeply nested,
schema-invalid JSON value to raise an uncaught `RecursionError`; the process
then exited 1 with a traceback rather than the documented JSON error and exit
2.  The author fixed that finding before this final freeze.  In the now
reviewed checker hash, `load_candidate` translates `RecursionError` to
`CandidateFormatError`.

The exact original reproducer—500,000 nested arrays around one value,
1,000,001 bytes total—now returns:

- exit status 2;
- no stderr traceback; and
- a JSON report with `accepted=false`,
  `status=MALFORMED_OR_IO_ERROR`, and
  `candidate JSON nesting is too deep`.

The regression is present in the authored test suite and passed independently.
No unresolved CLI defect remains from this audit.

## 10. False-positive and false-negative analysis

### False acceptance

I found no path to `accepted=true` that omits a defining property.  Acceptance
forces an identified simple graph, exact \(\gamma=4\), a literal closed
one-guard eternal four-family, and exhaustive non-four-colorability of the
complement.  These four facts alone prove the conjecture's negation for that
graph.  Ancillary checks cannot manufacture one of these facts.

### False rejection

Rejection deliberately proves no nonexistence statement.  Strict formatting,
an invalid redundant certificate, or an unavailable trace destination can
therefore cause only a non-mathematical rejection or I/O result.

The fixed anchor does not omit mathematical candidates in principle: every
target has \(\alpha(G)=4\), so any independent four-set can be relabeled to
\(\{0,1,2,3\}\).  Any eternal family can be sorted and deduplicated, and its
size is at most \({12\choose4}=495\).  Thus a genuine order-12,
parameter-four counterexample can be represented in this schema after
relabeling.

The verifier checks a decoded witness only.  It neither validates the SAT
assignment that produced it nor certifies that no other graph exists.  This
boundary is stated consistently in the README, mathematical note, report,
and CLI behavior.

## 11. Tests and independent probes

The authored suite passed all 13 tests under Python 3.14.6.

The clean-room hostile probe is
`reviews/order12_k4_candidate_verifier_hostile_probe.py`, SHA-256
`726d9dabe130b4874e23d3f33444124ba3b50c65a3824fc6f685da963b79f1e4`.
Its canonical output is
`reviews/order12_k4_candidate_verifier_hostile_probe.log`.

It completed the following deterministic checks:

| Probe | Coverage | Result |
|---|---:|---|
| graph6 differential | 2,048 graphs | `PASS` |
| exact static-parameter differential | 256 graphs | `PASS` |
| literal one-guard family differential | 4,096 graph/family pairs | `PASS` |
| nonedge/all-guards mutations | 2 targeted mutants | `KILLED` |
| complement-coloring differential | 64 graphs | `PASS` |
| independent trace verification | 131,072 rows | `PASS` |
| decisive/ancillary classifier | 32 truth rows | `PASS` |
| accepted/rejected CLI branches | both | `PASS` |
| deeply nested malformed JSON | exact prior reproducer | `PASS` |

The probe used at most approximately 50 MB resident memory and completed in
under eight seconds on the campaign laptop.

## 12. Final decision

| Reviewed claim | Verdict |
|---|---|
| Strict JSON and graph identity | `ACCEPT` |
| Exact \(\gamma=4\) certificate | `ACCEPT` |
| One-guard eternal-family semantics | `ACCEPT` |
| Complete complement-color exclusion | `ACCEPT` |
| Coloring trace and hash | `ACCEPT` |
| Derived \(i=\alpha=4\) and well-coveredness | `ACCEPT` |
| Ancillary certificate checks | `ACCEPT_AT_STRICT_JSON_BOUNDARY` |
| Definition/consistency separation | `ACCEPT` |
| CLI codes, no-overwrite, malformed-input handling | `ACCEPT` |
| Mathematical certificate theorem | `ACCEPT` |

**Final verdict:** `ACCEPT`.
