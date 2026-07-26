# Hostile review: simplicial closed-neighborhood reduction

## Verdict

**ACCEPT — proved in the stated one-guard model.**

I found no critical, high-, medium-, or low-severity mathematical defect in
Theorem 1, Corollary 2, or Corollary 3.  The argument respects the required
quantifiers:

\[
 \forall D\in\mathcal D\ \forall r\notin D\
 \exists u\in D\cap N(r)
\]

such that exactly the guard at \(u\) moves along \(ur\), the successor is
dominating, and the successor remains in the family.  Attacks are only at
unoccupied vertices.

The literature verdict is deliberately narrower: **no exact prior match was
located in the sources searched through 2026-07-26, but novelty is unresolved**.
In particular, an unavailable 2018 manuscript has a title directly about the
hypothesis \(\gamma=\gamma^\infty\), so this review does not certify novelty or
priority.

## Frozen review object

- Target: `math/lemmas/simplicial_neighborhood_reduction.md`
- Target SHA-256:
  `87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a`
- Target Git blob:
  `9a2e5589e4eca7b6716e4ef28d6a6a7252ea07a4`
- Target size: 226 lines
- Model: finite simple graphs; attacks at unoccupied vertices; exactly one
  adjacent guard moves to the attacked vertex; every state before and after a
  move dominates.

The target was not edited during this review.

## Claim-by-claim proof audit

### 1. Equality collapse in \(G\)

The standard chain

\[
 \gamma(G)\le i(G)\le\alpha(G)\le\gamma^\infty(G)
\]

and the assumed equality of the endpoints force all four quantities to equal
\(k\).  Because the cardinality of every maximal independent set lies between
\(i(G)\) and \(\alpha(G)\), every maximal independent set of \(G\) has size
\(k\).  This step is valid.

### 2. Well-coveredness and the three static parameters of \(Q\)

Let \(Q=G-N[v]\), and let \(I\) be maximal independent in \(Q\).
Then \(I\cup\{v\}\) is independent.  It is maximal in \(G\): \(v\) blocks
\(N(v)\), and maximality of \(I\) blocks \(Q-I\).  Hence every maximal
independent set of \(Q\) has size \(k-1\), proving that \(Q\) is well-covered
and that

\[
 i(Q)=\alpha(Q)=k-1.
\]

The upper bound \(\gamma(Q)\le k-1\) follows from
\(\gamma(Q)\le i(Q)\).  Conversely, if \(A\) dominated \(Q\) with at most
\(k-2\) vertices, then \(A\cup\{v\}\) would dominate \(G\): \(v\) dominates
\(N[v]\), and \(A\) dominates \(Q\).  This contradicts \(\gamma(G)=k\).
Thus \(\gamma(Q)=k-1\).  No adjacency between \(Q\) and
\(N(v)\setminus\{v\}\) is incorrectly excluded or needed here.

### 3. Universal independent-target forcing

The proof needs more than the existence of one convenient eternal family:
it fixes an arbitrary eternal \(k\)-family \(\mathcal D\).  The claim that
every independent \(k\)-set \(T\) belongs to every such family is correct.
From any \(D\in\mathcal D\), attack a vertex of \(T-D\).  A guard already on
\(T\) cannot respond because \(T\) is independent.  Therefore every legal
family response increases \(|D\cap T|\) by exactly one and never vacates a
previously occupied target vertex.  After at most \(k\) attacks the state is
exactly \(T\).  Family closure puts every intermediate state, and hence \(T\),
in \(\mathcal D\).

Applying this to a maximum independent set \(I\) of \(Q\) proves that
\(I\cup\{v\}\in\mathcal D\), so the \(v\)-slice in (1.5) is nonempty.  This
handles the universal family quantifier rather than merely choosing a
favorable initial configuration.

### 4. Excluding a second guard from \(N(v)\)

Suppose a state \(D\in\mathcal D\) contains \(v\) and
\(u\in N(v)\).  Simpliciality makes \(N[v]\) a clique, so
\(N[v]\subseteq N[u]\).  Thus \(u\) dominates everything \(v\) dominates.
Every vertex of \(Q\) that is dominated by \(D\) is dominated by a guard
other than \(v\), since \(v\) has no neighbor in \(Q\).  Consequently
\(D-\{v\}\) dominates all of \(G\), contradicting
\(\gamma(G)=|D|=k\).  Hence every other guard in a \(v\)-state lies in \(Q\).

### 5. Exact projected-family closure

For

\[
 \mathcal E=\{D-\{v\}:D\in\mathcal D,\ v\in D\},
\]

the preceding steps establish nonemptiness, uniform size \(k-1\), containment
in \(V(Q)\), and domination of \(Q\).

Fix \(B\in\mathcal E\) and an arbitrary unoccupied attack
\(r\in V(Q)-B\).  In the corresponding state \(D=B\cup\{v\}\), global
closure supplies some responder \(u\in D\cap N_G(r)\).  Because
\(r\in Q\), \(v\notin N_G(r)\), so \(u\ne v\).  The successor still contains
\(v\), and deleting \(v\) gives exactly the one-edge, one-guard successor

\[
 (B-\{u\})\cup\{r\}\in\mathcal E.
\]

The reasoning is pointwise in both \(B\) and \(r\); it does not silently
replace the required \(\forall B\,\forall r\,\exists u\) by a weaker
reachability statement.  Therefore
\(\gamma^\infty(Q)\le k-1\).  Together with
\(\alpha(Q)=k-1\le\gamma^\infty(Q)\), this proves all of (1.1).

### 6. Clique-partition identity

The upper bound
\(\theta(G)\le\theta(Q)+1\) is immediate from the clique \(N[v]\) and a
minimum clique partition of \(Q\).

For the reverse bound, let \(s\) parts of a minimum partition meet \(N[v]\).
The part containing \(v\) is contained in \(N[v]\), because \(v\) has no
neighbor in \(Q\).  Replacing the \(s\) old parts by \(N[v]\) and their
nonempty remainders in \(Q\) uses at most \(1+(s-1)=s\) parts.  The
remainders are disjoint cliques and still partition their vertices.
Minimality forbids a strict decrease, so the new partition is minimum.
Deleting its \(N[v]\) part yields a \(\theta(G)-1\)-part clique partition of
\(Q\).  Hence \(\theta(Q)\le\theta(G)-1\), and (1.2) follows.

This argument uses clique cover in the stated partition sense.  As a
cross-check, in the complement graph \(v\) is complete to \(Q\) and
\(\overline{G}[N[v]]\) is independent, which also forces the corresponding
chromatic number to increase by exactly one.

### 7. Empty-\(Q\) boundary

If \(Q=\varnothing\), then \(N[v]=V(G)\) is a clique, so \(G\) is complete and
\(\gamma(G)=\gamma^\infty(G)=\theta(G)=1\).  It cannot be a counterexample.
Restricting Theorem 1 to nonempty \(Q\) cleanly avoids competing conventions
for parameters of the empty graph.  No unhandled substantive case remains.

### 8. Corollary 2

Since \(\theta(G)\) and \(k\) are integers, \(k<\theta(G)\) gives
\(\theta(G)\ge k+1\).  Theorem 1 then gives

\[
 \theta(Q)=\theta(G)-1\ge k>k-1
 =\gamma(Q)=\gamma^\infty(Q).
\]

Also \(Q\) is a proper induced subgraph because \(N[v]\) is nonempty.
The smaller-counterexample claim is correct.

### 9. Corollary 3 and its imported dependency

Connectedness uses the separately proved component-additivity result in
`math/reductions.md` (SHA-256
`d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13`).
That result correctly proves additivity of \(\gamma\), \(\gamma^\infty\), and
\(\theta\), including the necessary fixed component-count slice for the
eternal-family lower bound.  Equality of the sums forces
\(\gamma(G_j)=\gamma^\infty(G_j)\) in every component, while the strict
\(\theta\)-gap occurs in at least one component.  A disconnected
minimum-order counterexample is therefore impossible.

Theorem 1 and the empty-\(Q\) boundary then exclude every simplicial vertex.
A connected counterexample is not \(K_1\); a leaf would be simplicial, so
\(\delta(G)\ge2\).  Finally, a degree-two vertex whose two neighbors are
adjacent has a clique closed neighborhood and is simplicial.  The final
structural conclusions are valid.

## Hostile edge-case ledger

| Attempted failure mode | Result |
|---|---|
| \(v\) isolated but \(Q\ne\varnothing\) | Proof still works; the slice fixes the isolated guard and projects the other guards. |
| \(k=1\) with \(Q\ne\varnothing\) | Hypotheses are inconsistent; the proof's domination lower bound detects this. |
| State contains \(v\) and a neighbor | Impossible by minimum domination, not merely by eternal closure. |
| Responder to an attack in \(Q\) is \(v\) | Impossible because \(v\) has no neighbor in \(Q\). |
| Projected state fails to dominate \(Q\) | Impossible because \(v\) contributes no domination inside \(Q\). |
| Family contains multiple possible responses | Harmless; only one witness is required for each state/attack pair. |
| Occupied-vertex attacks | Out of scope by explicit model; the proof and probe do not use them. |
| “At most one” versus “exactly one” movement | Equivalent here because every legal attack is unoccupied and must be answered by moving one adjacent guard onto it. |
| Overlapping clique covers rather than partitions | Out of scope; the target and cited one-guard literature use vertex partitions into cliques. |
| Empty graph parameter conventions | Explicitly isolated in the complete-graph boundary paragraph. |

## Primary-literature audit

Searches covered exact phrases and combinations involving “simplicial
vertex,” “closed neighborhood,” `G-N[v]`, well-coveredness, eternal-family
projection, clique cover, criticality, and
\(\gamma=\gamma^\infty\).  Full text was inspected where available.  The
nearest results are:

| Source | Movement/model | Relation to the target | Match? |
|---|---|---|---|
| W. F. Klostermeyer and C. M. Mynhardt, [*Domination, Eternal Domination, and Clique Covering*](https://arxiv.org/abs/1407.5235), DMGT 35 (2015), DOI 10.7151/dmgt.1799 | Distinguishes one-guard eternal domination from all-guards \(m\)-eternal domination | Foundational parameter chains and the \(\gamma\)-\(\theta\) question; full source search found no simplicial closed-neighborhood reduction | No |
| G. MacGillivray, C. M. Mynhardt, and V. Virgile, [*Eternal Domination and Clique Covering*](https://www.ejgta.org/index.php/ejgta/article/view/1525), EJGTA 10(2) (2022), DOI 10.5614/ejgta.2022.10.2.19 | Same unoccupied-attack, one-guard model | Uses independent-set attack forcing and studies the same conjecture; full text contains no theorem projecting an arbitrary family through \(G-N[v]\) | No |
| W. F. Klostermeyer and G. MacGillivray, [*Eternal Domination: Criticality and Reachability*](https://dspace.library.uvic.ca/items/f9f07fdf-eb53-410f-8a97-7b78ec16d186), DMGT 37 (2017), DOI 10.7151/dmgt.1918 | Same unoccupied-attack, one-guard model | Proposition 11 says \(x\) is not eternal-domination critical if some \(y\) has \(N[x]\supseteq N[y]\).  Thus a vertex covering a simplicial vertex is not critical.  This concerns deletion of one vertex and neither assumes \(\gamma=\gamma^\infty\) nor proves the target's family projection, well-coveredness, or \(\theta\) identity | No |
| M. Dettlaff, M. A. Henning, and J. Topp, [*On \(\alpha\)-Excellent Graphs*](https://link.springer.com/article/10.1007/s40840-022-01456-0), BMMSS 46 (2023), article 65, DOI 10.1007/s40840-022-01456-0 | Static independence theory | Proposition 4.3 proves the general identity \(\alpha(G-N[v])=\alpha(G)-1\) for simplicial \(v\); Proposition 4.4 preserves \(\alpha\)-excellence.  It has no eternal-family or clique-partition conclusion | Partial static overlap only |
| A. Gyárfás, A. Sebő, and N. Trotignon, [*The Chromatic Gap and Its Extremes*](https://pagesperso.g-scop.grenoble-inp.fr/~seboa/sebo_files/papers/jctb12gap.pdf), JCTB 102 (2012), DOI 10.1016/j.jctb.2012.06.001 | Static \(\theta-\alpha\) gap | Proposition 3.6 proves that an induced-subgraph gap-critical graph has no simplicial vertex, using the same \(\alpha(G-N[v])\) drop.  Its criticality hypothesis and conclusion differ from the dynamic \(\gamma=\gamma^\infty<\theta\) reduction | No |
| K. Kimura, N. Matsumoto, and T. Sato, [*Note on the Eternal Domination Number of Planar Graphs and Vertex-Critical Graphs*](https://www.dmlett.com/archive/v17/DML26_v17_pp45-50.pdf), DML 17 (2026), DOI 10.47443/dml.2025.208 | Eternal domination plus static clique-cover vertex-criticality | Observations 2.2–2.3 exclude a vertex whose neighbors stay inside a clique and exclude leaves in a clique-cover vertex-critical graph.  They do not give the target reduction or its equality hypothesis | No |
| W. F. Klostermeyer and C. M. Mynhardt, [*Protecting a Graph with Mobile Guards*](https://arxiv.org/abs/1407.5228), AADM 10 (2016), DOI 10.2298/AADM151109021K | Survey treats several variants; its superficially similar \(G-N[v]\) induction is for all-guards \(m\)-eternal domination | The cited induction defends \(G-N[v]\) with \(\alpha(G)-2\) guards and \(N[v]\) with two guards under simultaneous movement.  It is not evidence for the target's exact one-guard projection | Wrong variant |
| A. Rai and S. Rana, [*\(m\)-Eternal Dominating Set Problem on Subclasses of Chordal Graphs*](https://arxiv.org/abs/2602.02135), arXiv:2602.02135 (2026) | \(m\)-eternal/all-guards model | Current simplicial/chordal work, but the principal parameter and legal movement differ | Wrong variant |
| M. Carr, N. E. Clarke, G. MacGillivray, and J. Morris, [*Eternal Domination in Cayley Graphs*](https://arxiv.org/abs/2607.04024), arXiv:2607.04024 (2026) | One guard must move to the attack, but every other guard may also move; denoted \(\gamma^\infty_{\rm all}\) | Included to cover the latest July 2026 search frontier; simultaneous relocation makes its parameter different from the target's \(\gamma^\infty\) | Wrong variant |
| V. Virgile, [*Mobile Guards' Strategies for Graph Surveillance and Protection*](https://dspace.library.uvic.ca/bitstreams/00daa6ea-ea50-404b-8a18-d2259d315c01/download), PhD dissertation (2024) | Same one-guard model in its \(\gamma^\infty\) chapters | Current broad source on the conjecture; full-text searches found no simplicial or well-covered reduction matching this theorem | No |

Two coverage cautions prevent a novelty claim:

1. W. Klostermeyer, E. Krop, and G. MacGillivray, *On graphs with domination
   number equal to eternal domination number*, manuscript (2018), is cited as
   reference 46 in Klostermeyer and Mynhardt's
   [2020 survey chapter](https://digitalcommons.unf.edu/unf_faculty_publications/727/).
   No inspectable copy was located.  Its title is directly on point.
2. Negative full-text and bibliographic search is not a proof that an
   elementary identity or unpublished argument is new.

Accordingly, the scope-safe literature conclusion is:

> The combined theorem was not located in the searched primary literature.
> Several ingredients and structurally similar static reductions are known.
> Novelty and priority remain unresolved.

## Clean-room exhaustive probe

`probe.py` independently implements graph6 decoding, domination,
independence, well-coveredness, clique partition, and the greatest fixed point
of the exact one-guard safety game.  It imports no campaign evaluator.  Nauty's
`geng` is used only to supply one graph6 representative of every unlabeled
graph.

The probe exhausted every nonempty unlabeled graph through order eight:

| Order | Graphs | \(\gamma=\gamma^\infty\) graphs | Eligible graphs | Eligible simplicial vertices | Projected states | Projected attack obligations |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 2 | 1 | 2 | 2 | 0 |
| 3 | 4 | 3 | 2 | 6 | 7 | 2 |
| 4 | 11 | 7 | 5 | 18 | 28 | 22 |
| 5 | 34 | 13 | 11 | 40 | 82 | 108 |
| 6 | 156 | 40 | 32 | 115 | 334 | 639 |
| 7 | 1,044 | 116 | 97 | 315 | 1,293 | 3,411 |
| 8 | 12,346 | 512 | 406 | 1,198 | 7,062 | 23,741 |
| **Total** | **13,598** | **694** | **554** | **1,694** | **8,808** | **27,923** |

An eligible vertex is a simplicial \(v\) in a graph satisfying
\(\gamma=\gamma^\infty\), with nonempty \(G-N[v]\).  For every one of the
1,694 eligible vertices, the probe checked all parameter conclusions,
well-coveredness of \(Q\), the clique-partition identity, nonemptiness of the
\(v\)-slice, exclusion of \(v\) together with a neighbor, domination and size
of every projected state, and directly

\[
 \forall B\in\mathcal E\ \forall r\in V(Q)-B\
 \exists u\in B\cap N_Q(r):
 (B-\{u\})\cup\{r\}\in\mathcal E.
\]

Every projected witness was also lifted and checked as an actual one-edge
successor in the original family.  Further checks covered 5,413 independent
target states, 36 simplicial vertices with empty \(Q\), and the two structural
conclusions on all 3,314 connected graphs in the range having no simplicial
vertex.  All checks passed.

There is no graph through order eight with
\(\gamma=\gamma^\infty<\theta\), so the finite counterexample-preservation
portion is necessarily vacuous; Corollary 2 is established analytically.
The probe directly projects the independently computed *greatest* eternal
family.  It does not enumerate every closed subfamily.  The proof in
Sections 3–5 above establishes the stronger arbitrary-family statement.

Reproduction:

```text
python3 reviews/simplicial_neighborhood_reduction_hostile/probe.py \
  --maximum-order 8
```

Checksums:

- `probe.py` SHA-256:
  `fad436f80642cc1291616252aadbcb1244f2c1ae869bc62bbb46a9a87267226f`
- `probe_result.json` SHA-256:
  `cbfe53e601ce6753181ac2263b2a248fb85117c429191d7ec9bdadaca154eeb7`
- `tools/nauty2_9_3/geng` SHA-256:
  `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1`

The finite probe is a falsification check, not a substitute for the analytic
proof.

## Final defect ledger

| Severity | Count | Disposition |
|---|---:|---|
| Critical | 0 | None |
| High | 0 | None |
| Medium | 0 | None |
| Low | 0 | None |
| Literature/novelty caution | 1 | Do not claim novelty until the unavailable 2018 manuscript and any later version are obtained and inspected |

The theorem and both corollaries are scope-safe for mathematical use in the
stated model.  Promotion as a **new** theorem is not scope-safe on this
literature record alone.
