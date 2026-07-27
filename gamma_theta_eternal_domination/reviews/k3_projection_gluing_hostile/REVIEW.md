# Hostile review: \(k=3\) projection gluing

Date: 2026-07-26 (PDT)

## Verdict

**PASS WITH ONE QUALIFICATION.**

I found no mathematical defect in Theorem 2 (the no-full-list 2-SAT
equivalence), Theorem 3 (ridge transport), the displayed graph/family
records, or the two labelled finite scans.  The stated `PROVED`,
`EXACT CHECK`, and `OBSERVED` boundaries are accurate.

One evidentiary qualification should be made explicit before this note is
integrated into a stronger claim:

> The two unsatisfiable obstruction families do not contain a nontrivial
> independent-state ridge.  The specified `FDzro` family has one independent
> family state, and `HDzruf]` has three independent family states but no pair
> sharing two vertices.  Thus “every applicable ridge covariance” is
> literally correct but vacuous in both obstruction examples.  These examples
> refute automatic gluing from full closure and the displayed local witness
> layers; they are not a nonvacuous stress test of covariance across an
> unsatisfiable ridge.

This qualification does not weaken either proved theorem or invalidate the
negative automatic-gluing countermodels.  It prevents the countermodels from
being overread as evidence that a nontrivial ridge network coexists with the
mixed-\(P_4\) obstruction.

## Material reviewed

- `math/working/k3_projection_gluing.md`, SHA-256
  `45ed60001ebaac04c499182d633f418a79649022c3d632a8a1f9b11cecb9cd8a`;
- `math/working/k3_projection_gluing_evidence/probe.py`, SHA-256
  `54f579fca116de94343a10f7180a09c839424c51fb0fbbc428dd0c71d050347d`;
- `math/working/k3_projection_gluing_evidence/probe_result.json`; and
- `math/working/k3_projection_gluing_evidence/RESEARCH_LOG.md`.

The independent replay is in:

- `reviews/k3_projection_gluing_hostile/independent_audit.py`; and
- `reviews/k3_projection_gluing_hostile/independent_result.json`.

It imports no search or transition code from the generating evidence.
It uses adjacency sets, a reverse-support dependency queue for the greatest
eternal kernel, direct list-color enumeration, and raw labelled-mask scans.

## 1. One-guard model audit

The note and both implementations use the intended model:

1. an obligation is generated only for \(r\notin D\);
2. a successor is exactly \(D-\{u\}+\{r\}\);
3. the responding guard satisfies \(ur\in E(G)\);
4. every family state is checked to dominate \(G\); and
5. no simultaneous guard moves are admitted.

The independent replay checked every displayed obligation.  The counts are:

| graph/family | states | unoccupied attack obligations |
|---|---:|---:|
| `FCZbg`, greatest | 18 | 72 |
| `FCXfO`, specified | 16 | 64 |
| `FDzro`, specified | 21 | 84 |
| `FDzro`, greatest | 33 | 132 |
| `FCpbO`, greatest | 12 | 48 |
| `HDzruf]`, displayed | 46 | 276 |

No occupied-vertex attack, all-guards move, missing domination test, or
complement reversal was found.

## 2. Theorem 2: exact 2-SAT equivalence

### 2.1 Prerequisite scope

The bipartiteness of every

\[
 B_u=\overline G[(S-\{u\})\cup W_u]
\]

is available in this setting.  The accepted frozen projection has
\(\alpha=\gamma^\infty=2\), and the accepted \(\alpha=2\) theorem gives
clique-cover number two.  The gluing theorem therefore is not silently
assuming the target conclusion at \(k=3\).

### 2.2 Signs, anchors, and units

For a component coordinate \(\pi_u\) and flip \(z_{u,K}\),

\[
 \beta_u(x)=r_u^{\pi_u(x)\oplus z_{u,K}}.
\]

Thus the event \(\beta_u(x)=v\) is exactly

\[
 z_{u,K}=\pi_u(x)\oplus\iota_u(v).
\]

Equations (2.5) and (2.7) have the correct signs.  On the anchor component,
substituting \(z=0\) gives either a satisfied constant or a unit
contradiction.  A singleton list \(\{v\}\) appears in both projections
whose frozen colors differ from \(v\), so both required parity agreements
are imposed.

### 2.3 Exhaustion of complement-edge cases

For \(xy\in E(\overline G)\), the proof covers every no-full-list pair.

- If \(O(x)\cap O(y)\ne\varnothing\), one common frozen projection contains
  both endpoints and its bipartition separates them.
- If the omission sets are disjoint and one endpoint is a singleton, the
  lists are \(\{v\}\) and \(S-\{v\}\), hence disjoint.
- Otherwise the endpoints have distinct two-lists.  Their sole common color
  is forbidden by exactly one clause (2.8).

Anchor-outside collisions are also impossible: membership of an anchor
color in a response list includes the corresponding edge of \(G\).
Anchor-anchor colors are distinct.

No singleton/two-list edge clause is missing, and no same-two-list edge
needs a cross-projection clause.

### 2.4 Independent exhaustive falsifier

The independent checker exhaustively generated all abstract systems with
three anchors and three outside vertices, every nonempty proper response
list, every allowed anchor-outside complement edge, and every outside
complement edge.  Of 46,656 systems, 40,113 had all three frozen
projections bipartite.  For every one of those 40,113 systems, the
component-flip formula produced exactly the same outside colorings as direct
anchored list-color enumeration:

\[
 \text{mismatches}=0.
\]

This finite audit is a falsifier for the proof, not an ingredient in it.
The written proof is complete independently of this enumeration.

### 2.5 Full-list boundary

The note correctly excludes \(L(x)=S\) from Theorem 2.  Such a vertex lies
in no \(W_u\), receives no projection coordinate, and its incident
constraints are absent from \(\Phi_S\).  The `FDzro` greatest-family replay
shows the distinction concretely: four visible component orientations but
eleven direct colorings after the two full-list vertices are included.

## 3. Theorem 3: ridge transport

Let \(S=C+a\), \(T=C+b\), and \(\rho=(a\ b)\).  The accepted covariance
identity gives list compatibility under

\[
 \kappa_T(y)=\rho(\kappa_S(\rho(y))).
\]

The properness argument does not assume that \(\rho\) is a graph
automorphism:

- \(L_S(b)=\{a\}\), so the old \(a\)-fiber contains both \(a\) and \(b\)
  and is setwise fixed by \(\rho\);
- every common-color fiber contains neither \(a\) nor \(b\), so it is
  pointwise fixed; and
- consequently the unlabelled fiber partition is literally unchanged.

The reverse implication uses the same involution.  List cardinalities are
also preserved, so the no-full-list hypothesis propagates along a ridge
path and Corollary 4 is sound.

As a computational falsifier, the independent checker replayed all nine
independent ridge pairs present across `FCZbg`, `FCXfO`, and `FCpbO`,
checking 36 vertex-level covariance identities and transporting ten
compatible colorings.  Every transported coloring was compatible at the
other endpoint and had exactly the same unlabelled fiber partition.

The qualification in the verdict remains important: neither unsatisfiable
countermodel contributes one of these nine ridge pairs.

## 4. Named graph and family audit

The independently decoded `HDzruf]` record has exactly the displayed
complement edges

\[
\{01,02,12,34,45,56,13,06,27,47,57,28,78\}.
\]

After deleting precisely the six forbidden swaps, the independently
computed greatest safe triple-family equals the displayed 46 triples
literally.  In particular:

\[
N_{\overline G}(4)\cap N_{\overline G}(5)=\{7\},\qquad
N_{\overline G}(2)\cap N_{\overline G}(7)=\{8\}.
\]

Its response lists are exactly

\[
\{0\},\{0,2\},\{1,2\},\{1\},\{0,1\},\{0,1\}
\]

at vertices \(3,\ldots,8\).  Direct recomputation gives

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\]

The displayed clique partition was also checked edge by edge.  The two
mixed-path units, the original middle clause, the two \(w\)-clauses, and
the same-projection \(wy\) edge behave exactly as stated; there is no
compatible response-list coloring.

All other named list records, family sizes, component-variable counts,
unit counts, cross-clause counts, and direct-coloring counts agree with the
evidence file.  As an additional check, the independently recomputed graph
parameters are:

| graph | \(\gamma\) | \(\alpha\) | \(\gamma^\infty\) | \(\theta\) |
|---|---:|---:|---:|---:|
| `FCZbg` | 3 | 3 | 3 | 3 |
| `FCXfO` | 3 | 3 | 3 | 3 |
| `FCpbO` | 3 | 3 | 3 | 3 |
| `FDzro` | 2 | 3 | 3 | 3 |
| `HDzruf]` | 2 | 3 | 3 | 3 |

## 5. Independent replay of the finite observations

The independent scanner enumerated the raw labelled masks directly rather
than using the generating script's factored neighbor loops.

### Order eight

| condition | independent count |
|---|---:|
| raw masks | 2,048 |
| required states dominate | 576 |
| preceding and \(\alpha=3\) | 552 |
| \(\gamma=\alpha=3\) | 62 |
| equality and required states dominate | 0 |
| exact family realizations | 0 |

### Order nine

| condition | independent count |
|---|---:|
| raw masks | 524,288 |
| new-vertex neighbor prefilter | 155,648 |
| required states dominate | 87,552 |
| preceding and \(\alpha=3\) | 68,688 |
| preceding and \(\gamma=3\) | 96 |
| exact family realizations | 0 |

The free-edge sets really cover the stated labelled templates:

- at order eight, the six remaining old-core edges and five possible
  \(w\)-edges give eleven bits;
- at order nine, those six edges, five possible \(w\)-edges, seven arbitrary
  edges from the extra vertex to the old core, and the \(wz\) edge give
  nineteen bits.

The six banned one-swap states enforce the four exact displayed lists.
Any proper eternal family with those bans is contained in the greatest safe
kernel, so using that kernel cannot create a false negative.  The
observations are exhaustive for these labelled templates but are not
coverage theorems for all graphs of orders eight or nine.  The note states
that limitation correctly and does not raise the campaign frontier.

## 6. Claim-boundary audit

- `PROVED`: justified for Theorems 2 and 3 and their corollary.
- `EXACT CHECK`: justified for every named graph/family record.
- `OBSERVED`: appropriately used for the two single-template scans.
- `REFUTED`: justified for automatic gluing from the stated local
  ingredients without \(\gamma=3\), subject to the vacuity qualification
  above.
- `OPEN`: correctly retained for the equality-specific
  \(\gamma=\alpha=\gamma^\infty=3\) statement and for the full-list slice.

Nothing in the note resolves the universal \(\gamma\)-\(\theta\)
conjecture, raises the certified finite frontier, or supplies an order-14
result, and the note does not claim otherwise.

## Reproduction

From the repository root:

```text
python3 gamma_theta_eternal_domination/reviews/k3_projection_gluing_hostile/independent_audit.py
```

The checked output is frozen in `independent_result.json`.

## Revised-byte addendum

The qualification was rechecked against the revised note, SHA-256
`fc7f817aa611751b9bedbb9ddebd5830d81f02719f2d8aafe914db34f4c64907`
(replacing reviewed byte
`45ed60001ebaac04c499182d633f418a79649022c3d632a8a1f9b11cecb9cd8a`).
The status summary, both obstruction discussions, and the final
`Refuted` boundary now say explicitly that `FDzro` and `HDzruf]` have no
independent ridge pair and make no nonvacuous negative covariance claim.
Those statements match the independent counts above (one independent state
for the specified `FDzro` family; three but zero ridge pairs for
`HDzruf]`).  The caveat is therefore accurately and sufficiently scoped.
The evidence source binding records the revised hash, while `probe.py` is
byte-identical, so all prior exact replays remain applicable.
