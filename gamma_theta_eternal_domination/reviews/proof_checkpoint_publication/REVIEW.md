# Pre-publication plan for the proof-first checkpoint

Date: 2026-07-26 (PDT)

## Verdict

**ACCEPT A PUBLIC WORKSTREAM UPDATE; DO NOT ISSUE A SECOND PAPER YET.**

The three new proof lanes are substantial enough for `CLAIMS.md`,
`STATE.md`, the campaign overview, and a carefully scoped update to the
active research page.  They do not prove the \(k=3\) slice, raise the
finite counterexample frontier, produce a counterexample, or resolve the
universal conjecture.

The existing order-12 frontier paper should remain the sole current paper.
The new results are mutually dependent working theorems around an open
global gluing problem, rather than a completed parameter slice, graph-class
theorem, or coherent second manuscript.  Public source notes plus the active
workstream page are the appropriate release level now.

## Evidence reviewed

The following independent verdicts are complete:

- `reviews/forced_c5_contradiction_hostile/REVIEW.md`: `PASS`;
- `reviews/k3_twosat_bicycle_hostile/REVIEW.md`: `PASS`; and
- `reviews/k3_full_list_slice_hostile/REVIEW.md`: `PASS`.

The last review independently reproduced every connected graph-stream hash
and count through order nine and independently verified the order-12
full-list control.  It accepts the finite census only for the exact
connected-unlabeled predicate stated below.

## Maturity and publication classification

| material | central ledger | active page | exact boundary |
|---|---|---|---|
| End-edge witness separation for the exact mixed \(P_4\) | `PROVED` | yes | The exact lists \(\{a\},\{a,c\},\{b,c\},\{b\}\), in an arbitrary specified family under \(\gamma=\alpha=\gamma^\infty=3\), force five distinct external witnesses and hence \(n\ge12\). This is a floor for that response pattern, not for every counterexample. |
| Minimal-unsatisfiable 2-CNF trichotomy and connector parity | `PROVED` | yes, briefly | The logical terminal types are two-unit chain, one-unit lollipop, and unit-free bicycle. The physical expansion need not be induced or disjoint. |
| Canonical lollipop and canonical two-variable bicycle exclusions | `PROVED` | yes | Only the displayed shortest geometries are excluded. Arbitrary subdivisions, longer two-unit chains, and bicycles with at least three component variables remain open. |
| `GFznc{` control | `CERTIFIED-FINITE` or a narrowly worded `REFUTED` strengthening | source/ledger, optional on page | It has \((\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3)\), a checked 35-state family, and nonvacuous ridge covariance on two unsatisfiable no-full-list formulas. It shows why \(\gamma=3\) remains essential. The canonical graph6 representative is `G@~~fc`; `GFznc{` is only a valid labeled record. |
| Full-list deletion and augmented 2-SAT reduction | `PROVED` | yes | Avoiding a vertex preserves the specified family and remaining lists in \(G-x\). Coloring the full-list core followed by augmented 2-SAT is an exact equivalence. One full vertex gives exactly three tests, but no theorem says one test is satisfiable. |
| Full-list spoke, witness-layer, and link theorems | `PROVED` | yes | A full target forces three disjoint clique spokes, an external second clique layer, a bipartite nonisolated complement link, componentwise responder rigidity, and cross-spoke side separation. Every color is feasible on the local link only; global extension through residual vertices remains open. |
| Connected full-list census through order nine | `CERTIFIED-FINITE` | normally omit | Exactly 273,193 connected unlabeled graphs were covered. Among 15 equality candidates with 24 static-full incidences, no greatest-family incidence was full. This says nothing about disconnected graphs or order ten and does not advance the counterexample frontier. Singleton collapse is exact inside this census but only an `OBSERVED` pattern beyond it. |
| Order-12 full-list equality control `K{eYptMJynEn` | `CERTIFIED-FINITE`; it also `REFUTES` a no-full-list lemma | yes, as a positive control | The independent replay gives \(\gamma=\alpha=\gamma^\infty=\theta=3\), 127 greatest-family states, 1,143 obligations, one full target, and one compatible anchored coloring. It is not a counterexample. |
| Order-eight two-list zero count | `OBSERVED` | omit | The hostile reviewer retained the source classification: exact-two-list restrictions at order exactly eight only, not a proof-logged finite frontier. |

The following must remain working-only:

- the conjectural claim that one of the three color-restricted safety
  kernels is always nonempty;
- all mutation counts and local-repair counts not frozen in an independently
  reviewed artifact;
- exploratory synthesis `UNSAT` returns at orders \(7\)--\(12\), the
  two-full-target experiments, and the order-13 CEGAR cut limit;
- any claim excluding a general subdivided or long 2-SAT bicycle;
- any claim that the full-list local coloring extends globally; and
- any lower bound of 14, complete order-13 exclusion, \(k=3\) theorem, or
  universal resolution.

## Suggested claim decomposition

Using the next available identifiers after C-071:

1. `PROVED`: exact mixed-\(P_4\) end-witness separation and its
   pattern-specific \(n\ge12\) corollary.
2. `PROVED`: vertex-avoidance restriction and exact full-core
   coloring-plus-augmented-2-SAT equivalence.
3. `PROVED`: full-target spoke/link geometry and local three-color
   feasibility.
4. `CERTIFIED-FINITE`: the connected through-order-nine full-list census
   and the separately checked positive order-12 control, with the two
   universes stated separately in the row.
5. `PROVED`: the normalized minimal-unsatisfiable 2-CNF trichotomy and
   connector parity law.
6. `PROVED`: the two exact canonical dynamic exclusions.
7. Optionally, `REFUTED`: automatic global gluing from closure,
   restoration, Hall, frozen bipartiteness, and nonvacuous covariance,
   witnessed by the exact gamma-two graph `GFznc{`.
8. Optionally, `OBSERVED`: the order-exactly-eight two-list scan.  It can
   instead remain only in the acceptance record to avoid inflating the
   central claim ledger.

Do not combine the mixed-pattern \(n\ge12\) conclusion with C-050's
counterexample frontier.  They quantify over different universes.

## Exact safe wording for the public page

The page may say:

> The universal conjecture remains unresolved, and the certified finite
> frontier remains 13. For the exact mixed four-vertex response pattern,
> domination equality forces two additional disjoint end-witness cliques
> and separates them from the previously forced witness systems. Five
> mutually distinct external witnesses are therefore required, so this
> pattern cannot occur below order 12. This is a bound on one response
> pattern, not on all counterexamples.

> In the no-full-list branch, every minimal inconsistent normalized 2-SAT
> core is a two-unit chain, a one-unit lollipop, or a unit-free bicycle.
> One-guard closure now excludes the canonical lollipop and canonical
> two-variable bicycle, but longer chains, subdivisions, and larger
> bicycles remain open.

> Full family-response lists genuinely occur under
> \(\gamma=\alpha=\gamma^\infty=3\), so they cannot simply be forbidden.
> A full target nevertheless forces three disjoint clique spokes, a second
> external witness layer, and a rigid bipartite complement link. All three
> colors work locally on that link, while global extension is exactly three
> augmented 2-SAT tests in the single-full-target case. Proving that at
> least one test succeeds is the remaining full-list problem.

If the order-12 control is named, add:

> The checked order-12 control has
> \(\gamma=\alpha=\gamma^\infty=\theta=3\); it is a positive example of the
> structure, not a counterexample.

The page should preserve its prominent unresolved notice, the explicit
one-guard model, the conditional published-through-order-11 premise for
C-050, the unchanged frontier of 13, and the statement that order 14 has
not begun.

## Attribution and disclosure audit

`docs/research/gamma-theta-conjecture/index.html`, SHA-256
`55e39483236d6d9fb6dd0babdbecd7735f8ecaa3667416aef470e274b76e02ae`,
passes the attribution check:

- the HTML author metadata names Alec Kriebel;
- JSON-LD names Alec Kriebel as the `Person` author and the model as a
  contributor;
- the visible byline calls this a research program led by Alec Kriebel;
- the disclosure says the work was developed with heavy ChatGPT 5.6 Sol
  assistance under Alec Kriebel's direction; and
- it states that no external expert has reviewed the work and that exact
  verification is not peer review.

No attribution correction is needed.  If the page prose is edited,
“not externally peer-reviewed” would be slightly more precise than the
shorter word “unreviewed,” but this is editorial rather than blocking.

## Required archive and acceptance bindings

Before the checkpoint is called public and frozen:

1. Add manifest rows for all three target notes, logs, evidence programs and
   results, all three hostile reviews, and every independent replay source
   and result. Record the exact hashes from the reviews, not reconstructed
   hashes from prose.
2. Freeze a machine-readable proof-checkpoint acceptance object containing:
   the one-guard model; proposed claim statuses; the explicit unresolved,
   no-counterexample, frontier-13, no-order-14, no-priority, and
   no-second-paper boundaries; artifact hashes; and independent replay
   verdicts.
3. Record the full-list cleanup issue before archival release: the target
   probe can emit shutdown `ResourceWarning`s and its research log names a
   temporary output path. Either preserve the already reviewed bytes and
   disclose these nonmathematical defects, or make a cleanup-only patch and
   obtain a new hash-bound reviewer addendum. Do not silently change the
   reviewed source.
4. Update `CLAIMS.md`, `STATE.md`, the campaign `README.md`,
   `RESEARCH_LOG.md`, and the active page with one mutually consistent scope
   boundary. Have a separate integration audit check those final bytes.
5. After commit and push, freeze a public-workstream acceptance record with
   the source commit, Pages run, local and HTTPS page hashes, byte-identity
   result, Alec Kriebel attribution, AI disclosure, exact one-guard model,
   unchanged frontier, unresolved status, and sole-current-paper status.

No new PDF, paper directory, release tag, or paper-page entry should be
created for this checkpoint.
